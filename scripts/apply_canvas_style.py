#!/usr/bin/env python3
"""
Apply the approved Pass 3A Macro-Canvas Weave & Tone Composite to any Stage-1
wet-on-wet coffee/tea watercolor background image, and output a finalized
1920x1080 PNG32 asset ready for Ren'Py.

Reads canonical parameters from:
  vault/06 Assets/background_style_spec.json

Usage:
  python3 scripts/apply_canvas_style.py <input_wash_image> <output_png_path>
"""

import argparse
import json
import math
import os
import random
import shutil
import subprocess
import tempfile
from PIL import Image, ImageFilter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPEC_PATH = os.path.join(REPO_ROOT, "vault", "06 Assets", "background_style_spec.json")
MAGICK_BIN = "/opt/homebrew/bin/magick" if os.path.exists("/opt/homebrew/bin/magick") else shutil.which("magick")


def load_rgb(path, width, height):
    if MAGICK_BIN:
        raw = subprocess.check_output([
            MAGICK_BIN, path,
            "-filter", "Lanczos",
            "-resize", f"{width}x{height}!",
            "-depth", "8",
            "rgb:-"
        ])
        return bytearray(raw)
    with Image.open(path) as img:
        resized = img.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        return bytearray(resized.tobytes())


def get_px(buf, w, x, y):
    idx = (y * w + x) * 3
    return buf[idx], buf[idx + 1], buf[idx + 2]


def synthesize_macro_canvas(p1_buf, w, h, quilt_cfg):
    pw = quilt_cfg["patch_width"]
    ph = quilt_cfg["patch_height"]
    ox = quilt_cfg["overlap_x"]
    oy = quilt_cfg["overlap_y"]
    step_x = pw - ox
    step_y = ph - oy
    sx_min, sx_max = quilt_cfg["source_strip_x_range"]
    sy_min, sy_max = quilt_cfg["source_strip_y_range"]

    canvas_rgb = [0.0] * (w * h * 3)
    canvas_wgt = [0.0] * (w * h)

    rng = random.Random(quilt_cfg["random_seed"])
    sources = []
    for sy in range(sy_min, sy_max - ph, 18):
        for sx in range(sx_min, sx_max - pw, 12):
            for fx in (False, True):
                for fy in (False, True):
                    sources.append((sx, sy, fx, fy))

    for gy in range(-oy, h + oy, step_y):
        for gx in range(-ox, w + ox, step_x):
            sx, sy, flip_x, flip_y = rng.choice(sources)
            for py in range(ph):
                dy = gy + py
                if dy < 0 or dy >= h:
                    continue
                if py < oy:
                    wy = 0.5 * (1.0 - math.cos(math.pi * (py + 0.5) / oy))
                elif py >= ph - oy:
                    wy = 0.5 * (1.0 - math.cos(math.pi * (ph - py - 0.5) / oy))
                else:
                    wy = 1.0

                src_y = sy + (ph - 1 - py if flip_y else py)
                for px in range(pw):
                    dx = gx + px
                    if dx < 0 or dx >= w:
                        continue
                    if px < ox:
                        wx = 0.5 * (1.0 - math.cos(math.pi * (px + 0.5) / ox))
                    elif px >= pw - ox:
                        wx = 0.5 * (1.0 - math.cos(math.pi * (pw - px - 0.5) / ox))
                    else:
                        wx = 1.0
                    weight = wx * wy
                    src_x = sx + (pw - 1 - px if flip_x else px)
                    r, g, b = get_px(p1_buf, w, src_x, src_y)
                    idx = dy * w + dx
                    cidx = idx * 3
                    canvas_rgb[cidx] += r * weight
                    canvas_rgb[cidx + 1] += g * weight
                    canvas_rgb[cidx + 2] += b * weight
                    canvas_wgt[idx] += weight

    for i in range(w * h):
        weight = canvas_wgt[i]
        if weight > 0:
            cidx = i * 3
            canvas_rgb[cidx] /= weight
            canvas_rgb[cidx + 1] /= weight
            canvas_rgb[cidx + 2] /= weight

    return canvas_rgb


def apply_pass3a_composite(wash_path, output_path, tone_mix=None, weave_strength=None, valley_boost=None):
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        spec = json.load(f)

    gen_w, gen_h = spec["target_output"]["generation_resolution"]
    stage2 = spec["stage_2_canvas_composite"]
    params = stage2["parameters"]

    tone_mix = params["tone_mix"] if tone_mix is None else tone_mix
    weave_strength = params["weave_strength"] if weave_strength is None else weave_strength
    valley_boost = params["valley_boost"] if valley_boost is None else valley_boost

    texture_path = os.path.join(REPO_ROOT, stage2["reference_assets"]["macro_canvas_texture"])
    texture_buf = load_rgb(texture_path, gen_w, gen_h)
    wash_buf = load_rgb(wash_path, gen_w, gen_h)

    canvas_rgb = [float(value) for value in texture_buf]

    mean_r = sum(canvas_rgb[0::3]) / (gen_w * gen_h)
    mean_g = sum(canvas_rgb[1::3]) / (gen_w * gen_h)
    mean_b = sum(canvas_rgb[2::3]) / (gen_w * gen_h)

    wg_r, wg_g, wg_b = params["white_ground_rgb"]
    wp_r, wp_g, wp_b = params["wash_white_point_rgb"]

    base_r = wg_r * (1.0 - tone_mix) + mean_r * tone_mix
    base_g = wg_g * (1.0 - tone_mix) + mean_g * tone_mix
    base_b = wg_b * (1.0 - tone_mix) + mean_b * tone_mix

    out = bytearray(gen_w * gen_h * 3)
    for i in range(gen_w * gen_h):
        cidx = i * 3
        dr = (canvas_rgb[cidx] - mean_r) * weave_strength
        dg = (canvas_rgb[cidx + 1] - mean_g) * weave_strength
        db = (canvas_rgb[cidx + 2] - mean_b) * weave_strength

        cr = max(0.0, min(255.0, base_r + dr))
        cg = max(0.0, min(255.0, base_g + dg))
        cb = max(0.0, min(255.0, base_b + db))

        p2r = min(1.0, wash_buf[cidx] / wp_r)
        p2g = min(1.0, wash_buf[cidx + 1] / wp_g)
        p2b = min(1.0, wash_buf[cidx + 2] / wp_b)

        stain_depth = 1.0 - p2g
        v_boost = 1.0 + valley_boost * stain_depth * max(0.0, -dg / 25.0)

        fr = cr * (p2r ** v_boost)
        fg = cg * (p2g ** v_boost)
        fb = cb * (p2b ** v_boost)

        out[cidx] = int(max(0, min(255, round(fr))))
        out[cidx + 1] = int(max(0, min(255, round(fg))))
        out[cidx + 2] = int(max(0, min(255, round(fb))))

    upscale_cfg = params["upscale_1080p"]
    final_w = upscale_cfg["width"]
    final_h = upscale_cfg["height"]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if MAGICK_BIN:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            p = subprocess.Popen(
                [MAGICK_BIN, "-size", f"{gen_w}x{gen_h}", "-depth", "8", "rgb:-", tmp_path],
                stdin=subprocess.PIPE
            )
            p.communicate(input=bytes(out))
            if p.returncode != 0:
                raise RuntimeError("Failed encoding intermediate composite image")

            subprocess.check_call([
                MAGICK_BIN,
                tmp_path,
                "-filter", upscale_cfg["filter"],
                "-resize", f"{final_w}x{final_h}!",
                "-unsharp", upscale_cfg["unsharp_mask"],
                "-alpha", "set",
                "PNG32:" + output_path
            ])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    else:
        img = Image.frombytes("RGB", (gen_w, gen_h), bytes(out))
        img_up = img.resize((final_w, final_h), Image.Resampling.LANCZOS)
        img_sharp = img_up.filter(ImageFilter.UnsharpMask(radius=0.75, percent=45, threshold=2))
        img_sharp.convert("RGBA").save(output_path, format="PNG")

    print(f"Saved Pass 3A 1920x1080 background -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Apply Pass 3A macro-canvas composite and 1080p upscale.")
    parser.add_argument("input_wash", help="Path to Stage-1 wet-on-wet wash image")
    parser.add_argument("output_png", help="Destination path for finalized 1920x1080 PNG")
    parser.add_argument("--tone-mix", type=float, default=None, help="Override tone_mix (default from spec: 0.50)")
    parser.add_argument("--weave-strength", type=float, default=None, help="Override weave_strength (default from spec: 0.75)")
    parser.add_argument("--valley-boost", type=float, default=None, help="Override valley_boost (default from spec: 0.35)")
    args = parser.parse_args()

    apply_pass3a_composite(
        args.input_wash,
        args.output_png,
        tone_mix=args.tone_mix,
        weave_strength=args.weave_strength,
        valley_boost=args.valley_boost,
    )


if __name__ == "__main__":
    main()
