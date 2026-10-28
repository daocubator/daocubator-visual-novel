"""
process_gold_sprite.py
Utility script to process raw 3D gold character renders into game-ready Ren'Py sprites:
1. Removes outer black background.
2. Identifies and cleans genuine pass-through voids (e.g. between arms and torso) while protecting all interior clothing creases, lapels, cuffs, and shadows from becoming transparent.
3. Applies soft anti-aliased alpha edging (1px erode + 3x3 Gaussian feather).
4. Centers and scales to standard Ren'Py sprite resolution (560x880 RGBA PNG, anchored to bottom).
5. Optionally composites onto the conference stage (1920x1080) for visual quality review.
6. Optionally outputs a high-contrast magenta check image to verify 100% solid opacity inside garments.
"""

import os
import sys
import argparse
import cv2
import numpy as np
from PIL import Image

_BIREFNET_MODEL = None

def get_birefnet_model():
    global _BIREFNET_MODEL
    if _BIREFNET_MODEL is not None:
        return _BIREFNET_MODEL
    try:
        import torch
        from transformers import AutoModelForImageSegmentation
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[BIREFNET] Loading BiRefNet on {device}...")
        model = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet",
            trust_remote_code=True,
            local_files_only=True
        )
        model.to(device, dtype=torch.float32)
        model.eval()
        _BIREFNET_MODEL = (model, device)
        print("[BIREFNET] Model loaded successfully!")
        return _BIREFNET_MODEL
    except Exception as e:
        print(f"[WARN] Could not load BiRefNet ({e}), falling back to classical CV.")
        return None

def process_sprite(
    src_path: str,
    out_sprite_path: str,
    stage_preview_path: str = None,
    magenta_check_path: str = None,
    min_void_area: int = 1000,
    black_threshold: int = 32
):
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source image not found: {src_path}")

    img = cv2.imread(src_path)
    h, w, _ = img.shape
    b, g, r = cv2.split(img)

    # 1. DETECT BACKGROUND TYPE: CHROMA MAGENTA (#FF00FF) VS LEGACY BLACK
    corner_b = int(b[10, 10])
    corner_g = int(g[10, 10])
    corner_r = int(r[10, 10])
    is_chroma_magenta = (corner_r > 150 and corner_b > 150 and corner_g < 100)

    if is_chroma_magenta:
        print("[PROCESS] Detected Chroma Key Magenta (#FF00FF) background.")
        # ROBUST EXTERIOR-ONLY CHROMA MATTING:
        # 1. Identify true magenta background (R > 130, B > 130, G < 90, B - G > 30).
        #    On the solid gold character, specular highlights have G > 200 and shadows have R >> B,
        #    so this matches ZERO pixels inside the character body, face, nose, curls, or clothing folds.
        # 2. Invert to get the solid character mask.
        # 3. Erode ONLY from the outer boundary by 2-3px using an elliptical kernel to eliminate
        #    the anti-aliased magenta edge fringe completely.
        # 4. Smooth with a 3x3 Gaussian blur for sub-pixel anti-aliasing.
        # 5. Keep character RGB pixels 100% original and untouched (no despill / hue replacement).

        is_magenta_bg = (r > 130) & (b > 130) & (g < 90) & (b.astype(float) - g.astype(float) > 30)
        char_mask = (~is_magenta_bg).astype(np.uint8) * 255

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        choked = cv2.erode(char_mask, kernel, iterations=1)
        alpha = cv2.GaussianBlur(choked, (3, 3), 0)

        # Combine with ORIGINAL UNTOUCHED RGB
        rgba = np.dstack([img, alpha])
        rgba_pil = Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA))

    else:
        print("[PROCESS] Detected Legacy Black (#000000) background.")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        biref_info = get_birefnet_model()
        if biref_info is not None:
            model, device = biref_info
            import torch
            from torchvision import transforms

            pil_img = Image.open(src_path).convert("RGB")
            orig_size = pil_img.size

            transform_image = transforms.Compose([
                transforms.Resize((1024, 1024)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

            input_tensor = transform_image(pil_img).unsqueeze(0).to(device, dtype=torch.float32)
            with torch.no_grad():
                preds = model(input_tensor)[-1].sigmoid().cpu()

            pred = preds[0].squeeze()
            pred_pil = transforms.ToPILImage()(pred).resize(orig_size, Image.Resampling.BILINEAR)
            biref_mask = np.array(pred_pil)

            # HEAD VOLUME PROTECTION
            head_region = (biref_mask > 20).astype(np.uint8)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
            closed_head = cv2.morphologyEx(head_region, cv2.MORPH_CLOSE, kernel)

            solid_mask = biref_mask.copy()
            head_y_limit = int(h * 0.52)
            for y in range(0, head_y_limit):
                mask_row = closed_head[y] > 0
                solid_mask[y, mask_row] = 255

            # TARGETED LIMB VOID PUNCHOUT
            is_dark = (gray < black_threshold).astype(np.uint8)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(is_dark)

            for i in range(2, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                cx, cy = centroids[i]
                if area > min_void_area and cy > 250 and (cx > w * 0.55 or cx < w * 0.35):
                    solid_mask[labels == i] = 0
                    void_dilated = cv2.dilate((labels == i).astype(np.uint8) * 255, np.ones((3, 3), np.uint8))
                    solid_mask[void_dilated == 255] = 0

            alpha = cv2.GaussianBlur(solid_mask, (3, 3), 0)

            # DE-FRINGING
            alpha_f = alpha.astype(float) / 255.0
            clean_rgb = img.copy().astype(float)
            valid = alpha_f > 0.02
            for c in range(3):
                clean_rgb[:, :, c] = np.where(valid, np.clip(clean_rgb[:, :, c] / np.maximum(alpha_f, 0.5), 0, 255), 0)
            img = clean_rgb.astype(np.uint8)
        else:
            is_black = (gray < 15).astype(np.uint8)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(is_black)
            bg_mask = np.zeros((h, w), dtype=np.uint8)
            bg_mask[labels == 1] = 255

            for i in range(2, num_labels):
                area = stats[i, cv2.CC_STAT_AREA]
                cy = centroids[i][1]
                cx = centroids[i][0]
                if area > min_void_area and cy > 350 and (cx > w * 0.55 or cx < w * 0.35):
                    bg_mask[labels == i] = 255

            fg_mask = cv2.bitwise_not(bg_mask)
            kernel = np.ones((3, 3), np.uint8)
            fg_eroded = cv2.erode(fg_mask, kernel, iterations=1)
            alpha = cv2.GaussianBlur(fg_eroded, (3, 3), 0)

        # Merge RGBA
        b, g, r = cv2.split(img)
        rgba = cv2.merge([b, g, r, alpha])
        rgba_pil = Image.fromarray(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA))

    # Scale and center on 560x880 sprite canvas
    target_w, target_h = 560, 880
    sprite_canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

    aspect = rgba_pil.width / rgba_pil.height
    scaled_w = int(target_h * aspect)
    resized_character = rgba_pil.resize((scaled_w, target_h), Image.Resampling.LANCZOS)

    offset_x = (target_w - scaled_w) // 2
    offset_y = target_h - target_h  # Anchored to bottom
    sprite_canvas.alpha_composite(resized_character, (offset_x, offset_y))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(out_sprite_path)), exist_ok=True)
    sprite_canvas.save(out_sprite_path)
    print(f"[OK] Saved clean sprite: {out_sprite_path}")

    # Stage preview
    if stage_preview_path:
        stage_bg_path = "game/images/bg conference.png"
        if os.path.exists(stage_bg_path):
            bg = Image.open(stage_bg_path).convert("RGBA")
            stage_comp = bg.copy()
            # Ren'Py character default stage position: x=1160, bottom anchored
            stage_comp.alpha_composite(sprite_canvas, (1160, 1080 - target_h))
            os.makedirs(os.path.dirname(os.path.abspath(stage_preview_path)), exist_ok=True)
            stage_comp.save(stage_preview_path)
            print(f"[OK] Saved stage preview: {stage_preview_path}")

    # Magenta verification backing
    if magenta_check_path:
        sprite_np = np.array(sprite_canvas)
        a_norm = (sprite_np[:, :, 3].astype(float) / 255.0)[:, :, None]
        magenta_bg = np.zeros_like(sprite_np[:, :, :3])
        magenta_bg[:, :] = [255, 0, 255] # RGB magenta
        check_comp = (sprite_np[:, :, :3] * a_norm + magenta_bg * (1 - a_norm)).astype(np.uint8)
        # Crop midsection
        torso_crop = check_comp[350:850, 80:480]
        os.makedirs(os.path.dirname(os.path.abspath(magenta_check_path)), exist_ok=True)
        Image.fromarray(torso_crop).save(magenta_check_path)
        print(f"[OK] Saved magenta verification: {magenta_check_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process 3D gold character renders into Ren'Py sprites")
    parser.add_argument("src", help="Path to raw source render")
    parser.add_argument("dest", help="Destination path for 560x880 sprite")
    parser.add_argument("--preview", help="Optional path for stage composite preview")
    parser.add_argument("--check", help="Optional path for magenta verification crop")
    parser.add_argument("--min-void", type=int, default=600, help="Minimum area for arm/limb void pass-throughs")

    args = parser.parse_args()
    process_sprite(args.src, args.dest, args.preview, args.check, args.min_void)
