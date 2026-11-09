"""Generate search, social, structured-data, and crawler metadata."""
import json
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'site_config.json').read_text(encoding='utf-8'))
BASE = CONFIG['site_url'].rstrip('/') + '/'
assert urlsplit(BASE).scheme == 'https' and urlsplit(BASE).netloc
PATHS = {'home': '', 'resume': 'resume.html', 'works': 'works.html', 'contacts': 'contacts.html'}
LABELS = {'home': 'Home', 'resume': 'Experience & Skills', 'works': 'AI & Automation Projects', 'contacts': 'Contact'}
IMAGE = 'images/harish-dark-background.png'
PDF = 'Harish_V_Technical_Project_Manager_Resume.pdf'

def url(path=''):
    return urljoin(BASE, path)

def head(key, title, description, projects=()):
    canonical = url(PATHS[key])
    person = {
        '@type': 'Person', '@id': url('#harish-v'), 'name': 'Harish V',
        'url': url(), 'jobTitle': 'Technical Project Manager', 'image': url(IMAGE),
        'sameAs': ['https://www.linkedin.com/in/vharishv/'],
        'description': 'Technical Project Manager working in software development and AI automation, with hands-on Python, PHP, and Next.js development and 10-member team leadership.',
        'knowsAbout': ['AI automation', 'AI calling agents', 'OpenAI APIs', 'Python', 'PHP', 'Next.js', 'Team leadership', 'Workflow automation'],
    }
    website = {'@type': 'WebSite', '@id': url('#website'), 'url': url(), 'name': 'Harish V', 'inLanguage': 'en-IN', 'publisher': {'@id': person['@id']}}
    page = {
        '@type': {'home': 'ProfilePage', 'resume': 'ProfilePage', 'works': 'CollectionPage', 'contacts': 'ContactPage'}[key],
        '@id': canonical + '#webpage', 'url': canonical, 'name': title,
        'description': description, 'inLanguage': 'en-IN',
        'isPartOf': {'@id': website['@id']}, 'about': {'@id': person['@id']},
    }
    if key in ('home', 'resume'):
        page['mainEntity'] = {'@id': person['@id']}
    if key == 'contacts':
        person.update({'email': 'vharishv@yahoo.com', 'telephone': '+919809158308', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Cherpulassery, Palakkad', 'addressRegion': 'Kerala', 'addressCountry': 'IN'}})
    if key == 'works':
        page['mainEntity'] = {'@type': 'ItemList', 'numberOfItems': len(projects), 'itemListElement': [
            {'@type': 'ListItem', 'position': index, 'item': {'@type': 'CreativeWork', 'name': name, 'description': desc, 'keywords': stack, 'creator': {'@id': person['@id']}}}
            for index, (name, kind, stack, desc) in enumerate(projects, 1)
        ]}
    graph = json.dumps({'@context': 'https://schema.org', '@graph': [website, person, page]}, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    values = {k: escape(v, quote=True) for k, v in {'title': title, 'description': description, 'url': canonical, 'image': url(IMAGE)}.items()}
    return f'''<title>{values['title']}</title>
  <meta name="description" content="{values['description']}">
  <meta name="author" content="Harish V">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#101010">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{values['url']}">
  <link rel="sitemap" type="application/xml" href="{url('sitemap.xml')}">
  <link rel="describedby" type="text/plain" href="llms.txt">
  <meta property="og:type" content="{'profile' if key == 'home' else 'website'}">
  <meta property="og:site_name" content="Harish V">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{values['title']}">
  <meta property="og:description" content="{values['description']}">
  <meta property="og:url" content="{values['url']}">
  <meta property="og:image" content="{values['image']}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1254">
  <meta property="og:image:height" content="1254">
  <meta property="og:image:alt" content="Harish V, Technical Project Manager working in software development and AI automation">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{values['title']}">
  <meta name="twitter:description" content="{values['description']}">
  <meta name="twitter:image" content="{values['image']}">
  <meta name="twitter:image:alt" content="Portrait of Harish V">
  <script type="application/ld+json">{graph}</script>'''

def write_discovery(projects):
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap = ET.Element(f'{{{ns}}}urlset')
    for path in PATHS.values():
        ET.SubElement(ET.SubElement(sitemap, f'{{{ns}}}url'), f'{{{ns}}}loc').text = url(path)
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {url("sitemap.xml")}\n', encoding='utf-8')
    lines = [
        '# Harish V - Technical Project Manager', '',
        '> Software Development & AI Automation. Hands-on Python, PHP, and Next.js development and 10-member team leadership.', '',
        'Based in Cherpulassery, Palakkad, Kerala, India. 14+ years in software development, with project management experience since 2019.', '',
        '## Portfolio', '',
        *[f'- [{LABELS[key]}]({url(path)}): ' + {
            'home': 'Profile and professional focus.', 'resume': 'Professional experience, skills, and education.',
            'works': 'AI agents, automation tools, and software projects, with roles and results.',
            'contacts': 'Email, telephone, LinkedIn, and resume download.'}[key] for key, path in PATHS.items()],
        f'- [Technical Project Manager resume]({url(PDF)}): Downloadable PDF supplied by Harish V.', '',
        '## Supported achievements', '',
        '- Independently developed an AI sales calling agent using Python, OpenAI APIs, Twilio, and Retell AI; completed 1,000+ calls.',
        '- Independently developed Amazon SES email automation; sent 100,000+ emails cumulatively.',
        '- Built a separate bulk email validation tool that reduced campaign spam rate by approximately 80%.',
        '- Leads a 10-member development team, including client discussions, scope, task allocation, and code reviews.', '',
        '## Selected projects', '',
        *[f'- {name} ({stack}): {desc}' for name, kind, stack, desc in projects], '',
        '## Contact', '',
        '- [Email](mailto:vharishv@yahoo.com): vharishv@yahoo.com',
        '- [LinkedIn](https://www.linkedin.com/in/vharishv/): Professional profile.', '',
        '## Accuracy notes', '',
        'The 100,000+ email count is cumulative, not monthly. The approximately 80% reduction concerns campaign spam rate through a separate email validation tool. The 14+ years refer to software development, not years in AI. Project descriptions distinguish independent development from project management.', '',
    ]
    (ROOT / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8')
