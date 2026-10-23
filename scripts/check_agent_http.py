#!/usr/bin/env python3
"""Probe real agent-reading HTTP behavior; no synthetic GEO or citation score."""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import ProxyHandler, Request, build_opener


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='https://allluckly.cn/')
    parser.add_argument('--proxy', help='Optional HTTP(S) proxy; TLS verification stays enabled')
    parser.add_argument('--output', type=Path, help='Save timestamped observations as JSON')
    parser.add_argument('--require-edge', action='store_true', help='Fail unless same-URL negotiation and edge headers are live')
    args = parser.parse_args()
    opener = build_opener(ProxyHandler({'http': args.proxy, 'https': args.proxy})) if args.proxy else build_opener()
    base = args.base_url.rstrip('/') + '/'
    observations = []

    def get(path, accept='*/*', method='GET'):
        request = Request(urljoin(base, path.lstrip('/')), headers={'Accept': accept, 'User-Agent': 'Bison-Agent-Reading-Check/1.0'}, method=method)
        try:
            response = opener.open(request, timeout=30)
        except HTTPError as error:
            response = error
        body = response.read()
        entry = {'url': request.full_url, 'accept': accept, 'method': method,
                 'status': response.status, 'final_url': response.url,
                 'content_type': response.headers.get('Content-Type', ''),
                 'vary': response.headers.get('Vary', ''), 'link': response.headers.get('Link', ''),
                 'content_signal': response.headers.get('Content-Signal', ''),
                 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}
        observations.append(entry)
        return entry, body

    checks = {}
    html, html_body = get('/', 'text/html')
    md, md_body = get('/', 'text/markdown')
    explicit, explicit_body = get('/index.md')
    robots, robots_body = get('/robots.txt')
    llms, llms_body = get('/llms.txt')
    english, english_body = get('/en/index.md')
    skill_index, skill_index_body = get('/.well-known/agent-skills/index.json')
    skill = json.loads(skill_index_body)['skills'][0]
    artifact, artifact_body = get(skill['url'])
    missing, _ = get('/__agent_reading_missing_resource__/index.md')
    checks['html_default'] = html['status'] == 200 and 'text/html' in html['content_type'] and b'<html' in html_body
    checks['explicit_markdown'] = explicit['status'] == 200 and explicit_body.startswith(b'# ') and b'<html' not in explicit_body[:200]
    checks['english_markdown'] = english['status'] == 200 and english_body.startswith(b'# ') and b'Language: en' in english_body
    checks['reading_index'] = llms['status'] == 200 and llms_body.startswith(b'# ') and b'/guides/llms.txt' in llms_body
    checks['robots_content_signals'] = robots['status'] == 200 and b'search=yes' in robots_body and b'ai-input=yes' in robots_body and b'ai-train=no' in robots_body
    checks['skill_digest'] = skill_index['status'] == artifact['status'] == 200 and skill['digest'] == 'sha256:' + hashlib.sha256(artifact_body).hexdigest() and artifact_body.startswith(b'---\nname:')
    checks['real_404'] = missing['status'] == 404
    edge_checks = {
        'markdown_negotiation': md['status'] == 200 and 'text/markdown' in md['content_type'] and md_body == explicit_body,
        'vary_accept': 'accept' in [v.strip().lower() for v in md['vary'].split(',')],
        'discovery_link_header': '/llms.txt' in html['link'] and 'rel="describedby"' in html['link'],
        'response_content_signals': all(x in md['content_signal'] for x in ['search=yes', 'ai-input=yes', 'ai-train=no']),
    }
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'base_url': base,
              'checks': checks, 'edge_checks': edge_checks, 'observations': observations,
              'limits': 'Point-in-time HTTP probes, not actual crawler identity, indexing, citation or recommendation metrics. Native WebMCP is not tested.'}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for key, passed in checks.items():
        print(('PASS' if passed else 'FAIL') + ': ' + key)
    for key, passed in edge_checks.items():
        print(('PASS' if passed else 'NOT LIVE') + ': ' + key)
    return 0 if all(checks.values()) and (not args.require_edge or all(edge_checks.values())) else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, URLError, ValueError, KeyError) as error:
        sys.exit('HTTP check could not complete: ' + str(error))
