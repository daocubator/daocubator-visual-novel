"""Create soft watercolor halo overlays for the world overview scenario cards."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "game" / "images"
SIZE = (600, 340)
PALETTE = {
    "uncleared": (224, 91, 78),  # coral red used in the timing preview
    "cleared": (113, 166, 122),  # sage green used in the timing preview
}
GLOW_LAYERS = {
    "outer": (0.54, 8),
    "middle": (0.72, 5),
    "inner": (0.52, 3),
}
CARD_VARIANTS = {
    "ep1_keys": "ep1",
    "ep2_lisbon": "ep2",
    "ep3_agreements": "ep3",
    "ep4_apothecary": "ep4",
}
CARD_RADIUS = 12


def make_aura(name: str, rgb: tuple[int, int, int]) -> None:
    """Build three compact, feathered copies of the card silhouette as glows."""
    width, height = SIZE
    card_box = (44, 27, width - 45, height - 28)
    for layer, (peak_alpha, blur) in GLOW_LAYERS.items():
        mask = Image.new("L", SIZE, 0)
        ImageDraw.Draw(mask).rounded_rectangle(card_box, radius=CARD_RADIUS, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
        alpha = mask.point(lambda value: round(value * peak_alpha))
        image = Image.new("RGBA", SIZE, (*rgb, 0))
        image.putalpha(alpha)
        image.save(OUTPUT / f"scenario_aura_{name}_{layer}.png", optimize=True)


def make_card_surfaces() -> None:
    """Precompose each thumbnail and title wash, then round all four corners once."""
    scale = 3
    width, height = 512, 285

    card = Image.new("L", (width * scale, height * scale), 0)
    ImageDraw.Draw(card).rounded_rectangle(
        (0, 0, width * scale - 1, height * scale - 1), radius=CARD_RADIUS * scale, fill=255
    )
    card_mask = card.resize((width, height), Image.Resampling.LANCZOS)

    for ep_id, short_id in CARD_VARIANTS.items():
        for mood, suffix in (("disaster", "disaster"), ("happy", "happy")):
            source = Image.open(OUTPUT / f"cg_{short_id}_{suffix}_thumb.png").convert("RGBA")
            surface = source.crop((102, 0, 378, 154)).resize((width, height), Image.Resampling.LANCZOS)
            title_h = 70
            title = Image.new("RGBA", (width, title_h), (20, 7, 2, 217))
            surface.alpha_composite(title, (0, height - title_h))
            surface.putalpha(card_mask)
            surface.save(OUTPUT / f"scenario_card_{ep_id}_{mood}.png", optimize=True)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    make_card_surfaces()
    for name, color in PALETTE.items():
        make_aura(name, color)
