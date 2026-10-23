#!/usr/bin/env python3
"""Repeat the public, unauthenticated stateless MCP scan; writes only local evidence."""
import argparse
import datetime
import json
from pathlib import Path
import urllib.request

ENDPOINT = 'https://isitagentready.com/mcp'
PROTOCOL = '2025-03-26'


def rpc(payload):
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method='POST', headers={
        'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream', 'MCP-Protocol-Version': PROTOCOL,
    })
    with urllib.request.urlopen(request, timeout=55) as response:
        raw = response.read().decode('utf-8')
        headers = dict(response.headers)
        status = response.status
    if headers.get('Content-Type', '').startswith('application/json'):
        parsed = json.loads(raw)
    else:
        events = []
        for block in raw.replace('\r\n', '\n').split('\n\n'):
            data = '\n'.join(line[5:].lstrip(' ') for line in block.splitlines() if line.startswith('data:'))
            if data:
                events.append(json.loads(data))
        if not events:
            raise RuntimeError('The MCP endpoint returned no JSON-RPC event.')
        parsed = events[-1]
    return parsed, raw, headers, status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='https://allluckly.cn')
    parser.add_argument('--profile', choices=['content', 'all', 'apiApp'], default='content')
    parser.add_argument('--checks', help='Comma-separated actual scanner check IDs; overrides the profile.')
    parser.add_argument('--output', type=Path, default=Path('output/agent-readiness/post-deploy.json'), help='Evidence JSON path; raw SSE and scan metadata are saved beside it.')
    args = parser.parse_args()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    initialized, _, _, _ = rpc({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
        'protocolVersion': PROTOCOL, 'capabilities': {},
        'clientInfo': {'name': 'PublicBlogReadinessResearch', 'version': '1.0'},
    }})
    if 'error' in initialized:
        raise RuntimeError(json.dumps(initialized['error']))
    arguments = {'url': args.url, 'profile': args.profile}
    if args.checks:
        arguments['enabledChecks'] = [check.strip() for check in args.checks.split(',') if check.strip()]
    payload = {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {
        'name': 'scan_site', 'arguments': arguments,
    }}
    parsed, raw, headers, status = rpc(payload)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + '\n')
    output.with_suffix('.sse.txt').write_text(raw)
    output.with_name(output.stem + '-meta.json').write_text(json.dumps({
        'started_at_utc': started, 'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'endpoint': ENDPOINT, 'request': payload, 'status': status, 'headers': headers,
        'limitations': ['Point-in-time public external scan; Cloudflare caches and deployment timing may affect results.',
                        'Selected profiles/checks determine what was evaluated; this does not audit every article or establish browser support.'],
    }, ensure_ascii=False, indent=2) + '\n')
    print('Saved:', output)
    for block in parsed.get('result', {}).get('content', []):
        if block.get('type') == 'text':
            print(block['text'])
    if 'error' in parsed or parsed.get('result', {}).get('isError'):
        raise SystemExit('MCP returned an error; inspect the saved raw response.')


if __name__ == '__main__':
    main()
