#!/usr/bin/env python3
"""Validate API discovery and contracts against the actual Jekyll build.

Run after `bundle exec jekyll build`. Uses jsonschema from
scripts/requirements-agents.txt; does not contact external services.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:
    sys.exit('Install scripts/requirements-agents.txt to run this check (jsonschema is required).')


BASE = 'https://allluckly.cn'
ROOT = Path(__file__).resolve().parents[1]


class PageIds(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == 'id':
                self.ids.add(value)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(site, address):
    url = urlsplit(urljoin(BASE + '/', address))
    require(url.scheme == 'https' and url.netloc == urlsplit(BASE).netloc,
            'Resource must resolve to this public HTTPS site: ' + address)
    require(not url.query, 'Static resource must not require query parameters: ' + address)
    target = (site / unquote(url.path).lstrip('/')).resolve()
    require(target == site or site in target.parents, 'Resource escapes the site root: ' + address)
    if url.path.endswith('/'):
        target = target / 'index.html'
    elif not target.is_file():
        target = Path(str(target) + '.html')
    require(target.is_file(), 'Built resource missing: ' + address)
    if url.fragment:
        require(unquote(url.fragment) in PageIds(target.read_text()).ids,
                'Documentation fragment missing: ' + address)
    return target


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-dir', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    site = args.site_dir.resolve()
    spec_file = local_file(site, '/api/openapi.json')
    spec = json.loads(spec_file.read_text())
    catalog_file = local_file(site, '/.well-known/api-catalog')
    catalog = json.loads(catalog_file.read_text())
    require(spec_file.read_bytes() == (ROOT / 'api/openapi.json').read_bytes(),
            'Build changed the OpenAPI JSON bytes')
    require(catalog_file.read_bytes() == (ROOT / '.well-known/api-catalog').read_bytes(),
            'Build changed the Linkset JSON bytes')
    require(spec['openapi'] == '3.1.0' and spec['servers'] == [
        {'url': BASE, 'description': 'Public blog'}], 'Unexpected contract version or server')
    require(spec.get('security') == [] and not spec['components'].get('securitySchemes'),
            'Public static resources must not advertise credentials')

    # Resolve every local OpenAPI reference, including unused schemas and parameters.
    for node in walk(spec):
        if '$ref' in node:
            ref = node['$ref']
            require(ref.startswith('#/'), 'Unexpected external contract reference: ' + ref)
            target = spec
            for key in ref[2:].split('/'):
                target = target[key.replace('~1', '/').replace('~0', '~')]
    for schema in spec['components']['schemas'].values():
        Draft202012Validator.check_schema(schema)
    registry = Registry().with_resource(
        'urn:bison:openapi', Resource.from_contents(spec, default_specification=DRAFT202012))

    # A field added to the actual Liquid payload must also be described in the contract.
    include = (ROOT / '_includes/search-entry.json').read_text()
    emitted_keys = set(re.findall(r'"([a-z_]+)":\s*{{', include))
    described_keys = set(spec['components']['schemas']['SearchEntry']['properties'])
    require(emitted_keys == described_keys,
            'SearchEntry fields differ from the source Liquid include')

    expected = {'/search.json': 'zh-CN', '/en/search.json': 'en',
                '/.well-known/agent-skills/index.json': None}
    require(set(spec['paths']) == set(expected), 'Contract advertises an unexpected resource')
    article_count = 0
    skill_count = 0
    operation_ids = set()
    for resource, language in expected.items():
        path = spec['paths'][resource]
        methods = {key for key in path if key in {
            'get', 'head', 'post', 'put', 'patch', 'delete', 'options', 'trace'}}
        require(methods == {'get', 'head'}, 'Only actual GET and HEAD operations are allowed')
        for method in methods:
            operation = path[method]
            require(operation['operationId'] not in operation_ids, 'Duplicate operationId')
            operation_ids.add(operation['operationId'])
            require('requestBody' not in operation, 'Static reads cannot accept a request body')
            for parameter in operation.get('parameters', []):
                if '$ref' in parameter:
                    parameter = spec['components']['parameters'][parameter['$ref'].rsplit('/', 1)[1]]
                require(parameter['in'] == 'header', 'Static resources have no query parameters')
            require('content' not in operation['responses']['304'], '304 cannot have a body')
        require('content' not in path['head']['responses']['200'], 'HEAD cannot have a body')
        schema = path['get']['responses']['200']['content']['application/json']['schema']
        payload = json.loads(local_file(site, resource).read_text())
        contract_ref = 'urn:bison:openapi' + schema['$ref']
        validator = Draft202012Validator({'$ref': contract_ref}, registry=registry,
                                        format_checker=FormatChecker())
        validator.validate(payload)
        if language:
            seen = set()
            for article in payload:
                require(article['lang'] == language, 'Index language mismatch')
                require(article['url'] not in seen, 'Duplicate article URL in ' + resource)
                seen.add(article['url'])
                require(urlsplit(article['url']).path.startswith('/en/') == (language == 'en'),
                        'Article URL does not match the index language')
                local_file(site, article['url'])
                markdown = local_file(site, article['markdown_url'])
                require(markdown.name == 'index.md', 'Expected direct Markdown URL')
                require(markdown.read_bytes().startswith(b'# '), 'Markdown URL is not a body')
                require(datetime.fromisoformat(article['date'].replace('Z', '+00:00')).tzinfo,
                        'Article publication time must include its timezone')
                article_count += 1
        else:
            for skill in payload['skills']:
                skill_file = local_file(site, skill['url'])
                require(skill['digest'] == 'sha256:' + hashlib.sha256(skill_file.read_bytes()).hexdigest(),
                        'Reading skill digest does not match the published file')
                skill_count += 1
        print('PASS: GET/HEAD contract and built payload ' + resource)

    require(set(catalog) == {'linkset'} and isinstance(catalog['linkset'], list),
            'Catalog must be an RFC 9264 JSON Linkset')
    contexts = {entry['anchor']: entry for entry in catalog['linkset']}
    require(len(contexts) == len(catalog['linkset']), 'Duplicate Linkset context')
    endpoints = {BASE + resource for resource in expected}
    require(set(contexts) == endpoints | {BASE + '/.well-known/api-catalog'},
            'Catalog context does not match the real public data resources')
    directory = contexts[BASE + '/.well-known/api-catalog']
    require({link['href'] for link in directory['item']} == endpoints,
            'Catalog item links do not match the OpenAPI paths')
    for endpoint in endpoints:
        context = contexts[endpoint]
        require(context['service-desc'] == [{
            'href': BASE + '/api/openapi.json', 'type': 'application/vnd.oai.openapi+json'}],
            'Catalog must link each resource to its actual OpenAPI description')
        require(context['service-doc'], 'Missing human-readable documentation link')
    for context in contexts.values():
        for relation, targets in context.items():
            if relation == 'anchor':
                local_file(site, targets)
                continue
            require(isinstance(targets, list), 'Link relation targets must be arrays')
            for target in targets:
                local_file(site, target['href'])
    local_file(site, '/auth.md')
    print('PASS: RFC 9727 catalog, OpenAPI links and visible documentation fragments')
    print('Validated {} article records, {} reading skill(s), {} read operations.'.format(
        article_count, skill_count, len(operation_ids)))
    print('HTTP content types and live HEAD behavior require separate deployed checks.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        sys.exit('API catalog check failed: ' + str(error))
