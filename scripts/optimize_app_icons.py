#!/usr/bin/env python3
"""Generate responsive app icons without changing the catalog's source images.

Requires Pillow 11.3+ with WebP support. Run from any directory:
    python3 scripts/optimize_app_icons.py
    python3 scripts/optimize_app_icons.py --check

Only local app icons named by _data/apps.yml are read, including PNG and JPEG
sources. Images are downsampled with Lanczos,
never enlarged, then saved as optimized PNG and lossless WebP. Both encodings
are checked against the same resized pixels. Original PNGs remain available
for structured data, Markdown and existing external links. Use --only with app
IDs to generate variants for newly added products without rewriting other icons.
"""

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
import yaml


ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "assets/images/apps"
SIZES = (128, 256, 512)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed variants without writing files")
    parser.add_argument("--only", nargs="+", metavar="APP_ID", help="Process only these catalog app IDs")
    args = parser.parse_args()
    catalog = yaml.safe_load((ROOT / "_data/apps.yml").read_text())
    names = {app['id'] for app in catalog}
    if args.only and not set(args.only) <= names:
        parser.error("Unknown app IDs: " + ", ".join(sorted(set(args.only) - names)))
    selected = [app for app in catalog if not args.only or app['id'] in args.only]
    destination = ICONS / "display"
    failures = []
    total_source = 0
    total_128_webp = 0
    for app in selected:
        name = app['id']
        source = ROOT / app['icon'].lstrip('/')
        if source.resolve().parent != ICONS.resolve():
            raise ValueError(f"Expected a local app icon under {ICONS}: {source}")
        total_source += source.stat().st_size
        with Image.open(source) as original:
            original.load()
            if original.width != original.height:
                raise ValueError(f"Expected a square app icon: {source}")
            for size in SIZES:
                if size > original.width:
                    continue
                resized = original.resize((size, size), Image.Resampling.LANCZOS)
                for extension, image_format, options in (
                    ("png", "PNG", {"optimize": True, "compress_level": 9}),
                    ("webp", "WEBP", {"lossless": True, "method": 6, "exact": True}),
                ):
                    buffer = BytesIO()
                    resized.save(buffer, format=image_format, **options)
                    encoded = buffer.getvalue()
                    with Image.open(BytesIO(encoded)) as decoded:
                        if decoded.size != resized.size or ImageChops.difference(
                            decoded.convert("RGBA"), resized.convert("RGBA")
                        ).getbbox(alpha_only=False) is not None:
                            raise ValueError(f"Pixel mismatch: {name}-{size}.{extension}")
                    target = destination / f"{name}-{size}.{extension}"
                    if args.check:
                        if not target.is_file() or target.read_bytes() != encoded:
                            failures.append(str(target.relative_to(ROOT)))
                    elif not target.is_file() or target.read_bytes() != encoded:
                        destination.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(encoded)
                    if size == 128 and extension == "webp":
                        total_128_webp += len(encoded)
                    print(f"{name}-{size}.{extension}: {len(encoded):,} bytes")
    print(f"{len(selected)} original icons: {total_source:,} bytes")
    print(f"{len(selected)} 128px lossless WebP icons: {total_128_webp:,} bytes")
    print(f"128px request reduction: {100 * (1 - total_128_webp / total_source):.1f}%")
    if failures:
        raise SystemExit("Missing or outdated app icon variants:\n" + "\n".join(failures))


if __name__ == "__main__":
    main()
