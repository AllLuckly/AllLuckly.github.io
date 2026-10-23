#!/usr/bin/env python3
"""Package the Worker and public route manifest as one dashboard-uploadable module."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/agent-readiness/worker-upload.mjs')
    args = parser.parse_args()
    source = (ROOT / 'cloudflare/agent-access.mjs').read_text()
    manifest = json.loads((ROOT / 'agent-markdown/manifest.json').read_text())
    declaration = "import manifest from '../agent-markdown/manifest.json' with {type: 'json'};"
    assert source.count(declaration) == 1, 'Worker import changed; update the packager deliberately'
    source = source.replace(declaration, 'const manifest = ' + json.dumps(manifest, ensure_ascii=False, separators=(',', ':')) + ';')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(source)
    print(f'Packaged {len(manifest["routes"])} real routes into {args.output}')


if __name__ == '__main__':
    main()
