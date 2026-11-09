"""Verify generated SEO, schemas, links, and crawler files without dependencies."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from seo import BASE, PATHS, url

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []; self.schemas = []; self.in_schema = False; self.schema = ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); self.tags.append((tag, attrs))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema = True; self.schema = ''
    def handle_data(self, text):
        if self.in_schema: self.schema += text
    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.schema)); self.in_schema = False

for name, key in [('index.html','home'), ('index_personal.html','home'), ('resume.html','resume'), ('works.html','works'), ('contacts.html','contacts')]:
    text = (ROOT / name).read_text(encoding='utf-8')
    page = Page(text)
    assert sum(t == 'title' for t,a in page.tags) == 1, name
    assert sum(t == 'h1' for t,a in page.tags) == 1, name
    canonical = [a['href'] for t,a in page.tags if t == 'link' and a.get('rel') == 'canonical']
    assert canonical == [url(PATHS[key])], (name,canonical)
    metas = {a.get('name', a.get('property')): a.get('content') for t,a in page.tags if t == 'meta'}
    for field in ['description','author','robots','og:title','og:description','og:url','og:image','og:image:alt','twitter:card','twitter:image']:
        assert metas.get(field), (name,field)
    assert metas['author'] == 'Harish V'
    assert metas['og:url'] == canonical[0]
    assert len(page.schemas) == 1
    graph = page.schemas[0]['@graph']
    assert graph[0]['@type'] == 'WebSite' and graph[1]['@type'] == 'Person'
    assert graph[1]['name'] == 'Harish V' and graph[2]['url'] == canonical[0]
    if key == 'works':
        items = graph[2]['mainEntity']
        assert items['numberOfItems'] == 10 == len(items['itemListElement'])
        for item in items['itemListElement']:
            assert item['item']['name'] in text
    for tag, attrs in page.tags:
        for field in ['src','href']:
            link = attrs.get(field, '')
            parsed = urlsplit(link)
            if not link or parsed.scheme in ('mailto','tel','data'): continue
            if parsed.scheme:
                if not link.startswith(BASE): continue
                path = unquote(link[len(BASE):].split('#')[0].split('?')[0])
            else: path = unquote(parsed.path)
            if not path: continue
            assert (ROOT / path).is_file(), (name,link)
    assert not any(t == 'script' and a.get('src', '').startswith(('https:', 'http:', '//')) for t,a in page.tags), name
    print(name + ': metadata, schema, canonical URL, and asset links passed')

tree = ET.parse(ROOT / 'sitemap.xml')
locations = [node.text for node in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert locations == [url(path) for path in PATHS.values()]
assert 'index_personal.html' not in (ROOT / 'sitemap.xml').read_text()
assert 'Sitemap: ' + url('sitemap.xml') in (ROOT / 'robots.txt').read_text()
llms = (ROOT / 'llms.txt').read_text(encoding='utf-8')
assert llms.startswith('# Harish V') and all(location in llms for location in locations)
assert (ROOT / 'index.html').read_bytes() == (ROOT / 'index_personal.html').read_bytes()
for folder in ['css','js']:
    for path in (ROOT / folder).rglob('*'):
        if path.is_file():
            text = path.read_text(encoding='utf-8-sig')
            assert not re.search(r'https?://', text), path
            for resource in re.findall(r'url\([\'"]?([^\)\'\"]+)', text) if folder == 'css' else []:
                if not resource.startswith(('data:','http:', 'https:','#')):
                    assert (path.parent / resource).is_file(), (path,resource)
print('Sitemap, robots.txt, llms.txt, asset references, and author-reference audit passed.')
