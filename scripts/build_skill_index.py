#!/usr/bin/env python3
"""Keep the public read-only skill discovery digest in sync with exact bytes."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills-source/tutorial-reading.txt'
TARGET = ROOT / '.well-known/agent-skills/index.json'


def artifact():
    source = SOURCE.read_text()
    raw, suffix = source.split('{% raw %}', 1)[1].rsplit('{% endraw %}', 1)
    return (raw + suffix).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    body = artifact()
    description = next(line.removeprefix('description: ') for line in body.decode().splitlines() if line.startswith('description: '))
    data = {'$schema': 'https://schemas.agentskills.io/discovery/0.2.0/schema.json', 'skills': [{
        'name': 'tutorial-reading', 'type': 'skill-md', 'description': description,
        'url': '/.well-known/agent-skills/tutorial-reading/SKILL.md',
        'digest': 'sha256:' + hashlib.sha256(body).hexdigest()}]}
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert TARGET.read_text() == text, 'Public skill index is stale; run scripts/build_skill_index.py'
        rendered = ROOT / '_site/.well-known/agent-skills/tutorial-reading/SKILL.md'
        assert rendered.read_bytes() == body, 'Published SKILL.md bytes differ from the advertised digest'
        print('PASS: public skill schema, metadata and exact published SHA-256 digest')
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        if not TARGET.exists() or TARGET.read_text() != text:
            TARGET.write_text(text)
        print('Public skill index ready')


if __name__ == '__main__':
    main()
