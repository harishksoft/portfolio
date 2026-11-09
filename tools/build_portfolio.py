"""Build the static portfolio pages using facts from the supplied resume."""
from pathlib import Path
from html import escape
from seo import head as seo_head, write_discovery

ROOT = Path(__file__).resolve().parents[1]
PDF = 'Harish_V_Technical_Project_Manager_Resume.pdf'
LINKEDIN = 'https://www.linkedin.com/in/vharishv/'

projects = [
    ('Schic', 'Ecommerce · Bahrain', 'WooCommerce / AWS', 'Independently rebuilt and migrated an ecommerce platform with 1,000+ products and 90,000+ customer records. Built the replacement alongside the live site and switched over in approximately one month. Hosted on AWS with auto scaling.'),
    ('GoPit', 'Search platform', 'PHP / Flutter / Python', 'Managed Flutter mobile app development by another developer. Independently built the remaining search engine components: the PHP website, Python scraping, search provider APIs, Skyscanner integration, and Leaflet maps.'),
    ('LeaseLark', 'Property management SaaS', 'Next.js / PHP / Python / MySQL', 'Managed the project end to end, covering client interaction, requirements gathering, scope preparation, task allocation, integration, and deployment.'),
    ('Visio Square', 'Ecommerce · United States', 'PHP / MySQL / Razorpay / FedEx', 'Independently built a contact lens store end to end, with patient-to-manufacturer ordering, Razorpay payments, and FedEx shipping integration.'),
    ('News Scraping', 'News collection', 'Playwright / OpenAI', 'Independently built a client news portal tool end to end, collecting news from 64+ providers without APIs or RSS feeds using Playwright and OpenAI.'),
    ('AI Video Chatbot', 'Conversational AI · Telecom', 'Python / Next.js / MongoDB', 'Independently built an AI video chatbot end to end that acts as a company representative and guides users through a Ready for Next (RFN) form.'),
]

skills = [
    ('Technical leadership', '10-member team leadership, client meetings, project scope preparation, task allocation, code reviews, Jira, Trello, internal task tracker'),
    ('Languages & frontend', 'Python, PHP, JavaScript, HTML5, CSS3, jQuery'),
    ('Frameworks & backend', 'Next.js, CodeIgniter, Node.js, PHP and Python API development'),
    ('AI and LLM Integration', 'OpenAI APIs, retrieval-augmented generation (RAG), Model Context Protocol (MCP) server development, Claude agentic programming, API integration, automation, skills and connectors, Ollama setup and configuration'),
    ('AI Agents and Workflow Automation', 'AI cold calling agents, AI front-office call agent setup, Twilio, Retell AI, n8n, Make.com appointment booking automation, Square automation, Autodesk Revit automation, data and web scraping'),
    ('APIs & integrations', 'REST and third-party APIs, maps, Firebase, WhatsApp APIs, chatbots, automation and lead capture, Razorpay, PayU Money, Stripe, PayPal'),
    ('Databases', 'MySQL, PostgreSQL, MongoDB'),
    ('Cloud & deployment', 'AWS EC2, AWS Lightsail, Amazon SES, AWS server setup and configuration, cPanel, custom server configuration'),
    ('Ecommerce & CMS', 'WordPress, WooCommerce, Shopify, Magento setup and basic configuration, custom WordPress plugin development and existing plugin customization'),
    ('Development tools', 'Git, Bitbucket, Sourcetree, Chrome extension development'),
]

# Lead with the automation work; retain the full software delivery portfolio.
skills.sort(key=lambda item: 0 if item[0] == 'AI and LLM Integration' else 1 if item[0] == 'AI Agents and Workflow Automation' else 2)
automation_projects = [
    ('AI Sales Calling Agent', 'AI agents · Sales automation', 'Python / OpenAI APIs / Twilio / Retell AI', 'Independently developed an AI sales calling agent that completed 1,000+ calls, automating calling work previously handled by a three-person sales calling team.'),
    projects[5],
    projects[4],
    ('WhatsApp Chatbot & Campaign Tools', 'Chatbots · Workflow automation', 'Next.js / Python / MySQL / Meta WhatsApp APIs', 'Built internal WhatsApp chatbot and campaign tools, and set up a separate internal campaign automation tool.'),
    ('Email Automation & Validation', 'Campaign automation', 'Amazon SES / Multiple SMTP providers', 'Independently developed email automation with campaign scheduling and sender configuration, sending 100,000+ emails cumulatively. Built a separate bulk email validation tool that reduced campaign spam rate by approximately 80%.'),
    ('Lead Collection Automation', 'Data & web scraping', 'Python / Excel', 'Independently developed tools that read Excel inputs, collect contact details from websites, and export results to Excel, reducing manual collection work.'),
]

def button(href, label, primary=False, download=False):
    return f'<a class="button{" primary" if primary else ""}" href="{href}"{" download" if download else ""}>{label}<span aria-hidden="true">↗</span></a>'

def cards(items):
    return '<div class="project-grid">' + ''.join(f'''<article class="project-card"><p class="eyebrow">{escape(kind)}</p><h3>{escape(name)}</h3><p>{escape(desc)}</p><p class="stack">{escape(stack)}</p></article>''' for name, kind, stack, desc in items) + '</div>'

def intro(kicker, title, desc):
    return f'<section class="page-intro"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{desc}</p></section>'

def site_header(active):
    items = []
    for key, url, label in [('home','index.html','Home'), ('resume','resume.html','Resume'), ('works','works.html','Projects'), ('contacts','contacts.html','Contact')]:
        current = ' aria-current="page"' if active == key else ''
        css_class = 'menu-item current-menu-item' if active == key else 'menu-item'
        items.append(f'<li class="{css_class}"><a href="{url}"{current}>{label}</a></li>')
    return (ROOT / 'tools' / 'site_header.html').read_text(encoding='utf-8').replace('{{MENU_ITEMS}}', '\n      '.join(items))


def page(active, title, description, body):
    header = site_header(active)
    metadata = seo_head(active, f"{title} | Harish V", description, automation_projects + projects[:4])
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {metadata}
  <link rel="icon" href="images/harish-monogram.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/layout.css">
  <link rel="stylesheet" href="css/portfolio.css">
  <link rel="stylesheet" href="css/site-header.css">
  <script src="js/personal-home.js" defer></script>
</head>
<body class="inner-page grained-off">
  <a class="skip-link" href="#main">Skip to content</a>
  {header}
  <main id="main">{body}</main>
  <footer class="site-footer"><div><a class="brand" href="index.html">Harish <strong>V.</strong></a><p>Technical Project Manager · Software Development &amp; AI Automation</p></div><div class="footer-links"><a href="mailto:vharishv@yahoo.com">Email <span aria-hidden="true">↗</span></a><a href="tel:+919809158308">Call <span aria-hidden="true">↗</span></a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a></div></footer>
</body>
</html>
'''

home = (ROOT / 'tools' / 'personal_home.html').read_text(encoding='utf-8')

experience = intro('Experience / Skills / Education','Software development.<br>AI automation.','Technical Project Manager with 14+ years in software development and project management experience since 2019. I lead a 10-member team and combine hands-on Python, PHP, and Next.js development with AI automation.') + '''<section class="content-section"><div class="section-heading heading-row"><div><p class="eyebrow">01 / Career</p><h2>Professional experience</h2></div>''' + button(PDF, 'Download full resume',download=True) + '''</div><div class="timeline">
<article class="role"><div class="role-date">2019 — Present</div><div><p class="eyebrow">Ksoft Technologies · Cherpulassery, Palakkad</p><h3>Project Manager</h3><ul class="experience-list"><li>Lead 10 developers for custom software and ERP projects, handling client meetings, project scope, and task allocation.</li><li>Review code alongside hands-on Python, PHP, and Next.js development. Manage tasks with the internal tracker and client-required Jira or Trello.</li><li>Independently developed an AI sales calling agent using Python, OpenAI APIs, Twilio, and Retell AI; completed 1,000+ calls and automated calling work previously handled by a three-person sales calling team.</li><li>Independently developed Amazon SES email automation that sent 100,000+ emails cumulatively. Built a separate validation tool that reduced campaign spam rate by approximately 80%.</li><li>Built internal WhatsApp chatbot and campaign tools using Next.js, Python, MySQL, and Meta’s WhatsApp APIs; also set up a separate internal campaign automation tool.</li><li>Independently developed Python lead scraping tools that read Excel inputs, collect website contact details, and export results to Excel.</li><li>Independently rebuilt and migrated Schic, a Bahrain WooCommerce platform with 1,000+ products and 90,000+ customer records, switching over in approximately one month.</li></ul></div></article>
<article class="role"><div class="role-date">2014 — 2019</div><div><p class="eyebrow">Ksoft Technologies · Cherpulassery, Palakkad</p><h3>PHP Developer</h3><p>Developed PHP web applications; progressed to Project Manager in 2019.</p></div></article>
<article class="role"><div class="role-date">2012 — 2014</div><div><p class="eyebrow">Safe Technologies · Palakkad</p><h3>PHP Developer</h3><p>Developed PHP web applications before joining Ksoft Technologies in 2014.</p></div></article></div></section>
<section class="content-section"><div class="section-heading"><p class="eyebrow">02 / Toolkit</p><h2>Technical &amp; leadership skills</h2></div><dl class="skills-grid">''' + ''.join(f'<div><dt>{escape(name)}</dt><dd>{escape(value)}</dd></div>' for name, value in skills) + '''</dl></section>
<section class="content-section"><div class="section-heading"><p class="eyebrow">03 / Education</p><h2>Diploma in Computer Engineering</h2></div><p class="lead">IPT &amp; GPTC, Shoranur, Kerala</p><p>2012</p></section>'''

work = intro('AI agents / Automation / Selected work','AI automation.<br>Selected projects.','Independently developed an AI sales calling agent, email automation, and lead scraping tools. Built internal WhatsApp chatbot and campaign tools, alongside hands-on software delivery and project leadership.') + '<section class="content-section project-section" aria-label="AI and automation projects"><div class="section-heading"><p class="eyebrow">01 / AI &amp; automation</p><h2>AI agents &amp; automation tools</h2></div><div class="stats project-highlights"><div><strong>1,000+</strong><span>Calls completed by the AI sales calling agent</span></div><div><strong>100,000+</strong><span>Emails sent cumulatively through email automation</span></div><div><strong>~80%</strong><span>Lower campaign spam rate through a separate email validation tool</span></div></div>' + cards(automation_projects) + '</section><section class="content-section project-section" aria-label="Other software projects"><div class="section-heading"><p class="eyebrow">02 / Software delivery</p><h2>Software development &amp; project management</h2></div>' + cards(projects[:4]) + '<p class="section-note">Additional work includes project management and team leadership for custom software and ERP projects, plus custom websites, WooCommerce, and Shopify stores.</p></section><section class="contact-banner"><p class="eyebrow">Let’s automate</p><h2>What could your team automate?</h2>' + button('contacts.html','Discuss automation',True) + '</section>'

contact = intro('Contact','AI automation &amp;<br>software delivery.','Contact me about AI calling agents, chatbot and workflow automation, Python, PHP, or Next.js development, and technical project management.') + f'''<section class="content-section contact-layout" aria-label="Contact details"><div class="contact-methods"><a href="mailto:vharishv@yahoo.com"><span class="eyebrow">Email</span><span class="contact-value">vharishv@yahoo.com <span class="accent" aria-hidden="true">↗</span></span></a><a href="tel:+919809158308"><span class="eyebrow">Phone</span><span class="contact-value">+91 9809158308 <span class="accent" aria-hidden="true">↗</span></span></a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">LinkedIn</span><span class="contact-value">Connect with Harish V <span class="accent" aria-hidden="true">↗</span></span></a></div><aside class="contact-aside"><div class="small-monogram" aria-hidden="true">HV</div><h2>Harish V</h2><p>Technical Project Manager<br>Software Development &amp; AI Automation</p><p>Cherpulassery, Palakkad,<br>Kerala, India</p>{button(PDF,'Download resume',download=True)}</aside></section>'''

for filename, active, title, desc, content in [
    ('index.html','home','Technical Project Manager & AI Automation','Harish V — Technical Project Manager, Software Development & AI Automation. Python, PHP & Next.js and 10-member team leadership.',home),
    ('resume.html','resume','Experience & Skills','Explore Harish V’s AI automation skills, hands-on software development, project leadership, and education.',experience),
    ('works.html','works','AI & Automation Projects','Explore Harish V’s AI calling agents, chatbots, workflow automation, and software projects.',work),
    ('contacts.html','contacts','Contact','Contact Harish V about AI agents, chatbots, workflow automation, and technical project leadership.',contact),
]:
    output = content.replace('{{SITE_HEADER}}', site_header('home')).replace('{{SEO_HEAD}}', seo_head('home', 'Harish V | Technical Project Manager & AI Automation', desc)) if active == 'home' else page(active, title, desc, content)
    (ROOT / filename).write_text(output, encoding='utf-8')
write_discovery(automation_projects + projects[:4])
print('Built portfolio pages, SEO metadata, schemas, sitemap, robots, and llms.txt.')
