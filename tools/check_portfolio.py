"""Check local navigation, responsive layouts, and the resume download."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'playwright'
OUT.mkdir(parents=True, exist_ok=True)
PAGES = ['index_personal.html', 'resume.html', 'works.html', 'contacts.html']
BASE = 'http://127.0.0.1:8080/'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    for label, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844), ('small', 320, 700)]:
        menu_reference = None
        page.set_viewport_size({'width': width, 'height': height})
        for name in PAGES:
            page.goto(BASE + name)
            if name == 'index_personal.html':
                page.wait_for_timeout(3500)
            assert page.locator('h1').is_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (name, width)
            menu_signature = page.locator('.header .menu a').evaluate_all('''links => links.map(link => {
                const style = getComputedStyle(link);
                const rect = link.getBoundingClientRect();
                return [link.getAttribute('href'), style.fontFamily, style.fontSize,
                        style.lineHeight, style.padding, Math.round(rect.x), Math.round(rect.y)];
            })''')
            if menu_reference is None:
                menu_reference = menu_signature
            assert menu_signature == menu_reference, ('Menu differs', name, width, menu_signature, menu_reference)
            if label != 'small':
                page.screenshot(path=str(OUT / (name.replace('.html', '') + '-' + label + '.png')), full_page=True)
            print(f'{name}: {width}px layout passed')
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.goto(BASE + 'index_personal.html')
    page.locator('.top-menu a[href="works.html"]').click()
    page.wait_for_url('**/works.html')
    assert page.url.endswith('works.html')
    page.get_by_role('link', name='Resume', exact=True).click()
    page.wait_for_url('**/resume.html')
    assert page.url.endswith('resume.html')
    with page.expect_download() as info:
        page.get_by_role('link', name='Download full resume').click()
    assert info.value.suggested_filename == 'Harish_V_Technical_Project_Manager_Resume.pdf'
    print('Home, Projects, Experience navigation and PDF download passed')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.goto(BASE + 'contacts.html')
    toggle = page.get_by_role('button', name='Menu')
    toggle.click()
    assert toggle.get_attribute('aria-expanded') == 'true'
    assert page.get_by_role('link', name='Projects', exact=True).is_visible()
    page.keyboard.press('Escape')
    assert toggle.get_attribute('aria-expanded') == 'false'
    toggle.click()
    page.get_by_role('link', name='Home', exact=True).click()
    page.wait_for_url('**/index_personal.html')
    assert page.url.endswith('index_personal.html')
    assert page.get_by_role('button', name='Menu').get_attribute('aria-expanded') == 'false'
    page.wait_for_timeout(3500)
    toggle = page.get_by_role('button', name='Menu')
    toggle.click()
    assert toggle.get_attribute('aria-expanded') == 'true'
    page.keyboard.press('Escape')
    assert toggle.get_attribute('aria-expanded') == 'false'
    print('Mobile menu opening, Escape, and navigation passed')
    assert not errors, errors
    print('No browser JavaScript errors')
    browser.close()
