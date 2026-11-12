#!/usr/bin/env python3
"""Make a standalone, seamless macro-canvas texture from Pass 1's clean margin."""

import argparse
import json
from pathlib import Path

from PIL import Image

from apply_canvas_style import synthesize_macro_canvas


ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "vault" / "06 Assets" / "background_style_spec.json"
DEFAULT_OUTPUT = ROOT / "vault" / "06 Assets" / "style_references" / "pass3a_canvas_texture_only.png"


def generate(output_path: Path) -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    stage2 = spec["stage_2_canvas_composite"]
    width, height = spec["target_output"]["generation_resolution"]
    old_source = ROOT / stage2["reference_assets"]["pass1_macro_canvas_source"]

    # The spec's source range uses only the far-right weave-only margin of Pass 1.
    quilt = dict(stage2["parameters"]["patch_quilting"])

    with Image.open(old_source) as source:
        source = source.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        woven = synthesize_macro_canvas(source.tobytes(), width, height, quilt)
    pixels = bytes(max(0, min(255, round(value))) for value in woven)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.frombytes("RGB", (width, height), pixels).save(output_path, format="PNG")
    print(f"Saved standalone {width}x{height} macro-canvas texture -> {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
