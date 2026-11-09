"""Copy only public portfolio files into the GitHub Pages artifact."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'dist'
assert DEST.resolve().parent == ROOT.resolve()
if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir()
files = [
    'index.html', 'resume.html', 'works.html', 'contacts.html',
    'sitemap.xml', 'robots.txt', 'llms.txt', '.nojekyll',
    'Harish_V_Technical_Project_Manager_Resume.pdf',
    'css/layout.css', 'css/portfolio.css', 'css/personal-home.css', 'css/site-header.css',
    'js/personal-home.js', 'images/harish-dark-background.png', 'images/harish-monogram.svg',
]
for name in files:
    target = DEST / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
print(f'Packaged {len(files)} public files in dist/.')
