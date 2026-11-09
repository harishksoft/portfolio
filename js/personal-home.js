/* Portfolio interactions: no external libraries, analytics, or trackers. */
(() => {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.menu-btn');
  const nav = document.querySelector('#personal-nav');
  function setMenu(open) {
    header.classList.toggle('active', open);
    toggle.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('menu-open', open);
  }
  toggle.addEventListener('click', event => {
    event.preventDefault();
    setMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });
  toggle.addEventListener('keydown', event => {
    if (event.key === ' ') { event.preventDefault(); toggle.click(); }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && header.classList.contains('active')) {
      setMenu(false); toggle.focus();
    }
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.querySelectorAll('.hover-masks a').forEach(link => {
    const label = document.createElement('span');
    label.className = 'mask-lnk';
    label.textContent = link.textContent;
    const hover = label.cloneNode(true);
    hover.classList.add('mask-lnk-hover');
    hover.setAttribute('aria-hidden', 'true');
    link.replaceChildren(label, hover);
  });
  const follower = document.querySelector('.cursor-follower');
  if (follower && !reducedMotion && matchMedia('(pointer: fine)').matches) {
    document.addEventListener('pointermove', event => {
      follower.style.transform = `translate3d(${event.pageX}px,${event.pageY}px,0)`;
    });
  }
  const grain = document.querySelector('#grained_container');
  if (grain && !reducedMotion) {
    const canvas = document.createElement('canvas');
    canvas.width = canvas.height = 160;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      for (let x = 0; x < 160; x += 3) for (let y = 0; y < 160; y += 3) {
        const shade = Math.floor(Math.random() * 256);
        ctx.fillStyle = `rgba(${shade},${shade},${shade},0.15)`;
        ctx.fillRect(x,y,1,1);
      }
      grain.style.backgroundImage = `url(${canvas.toDataURL()})`;
    }
  }
  const target = document.querySelector('.typed-subtitle');
  const source = document.querySelector('.typing-subtitle');
  if (!target || !source) return;
  const phrases = Array.from(source.querySelectorAll('p')).map(p => Array.from(p.childNodes).map(node => ({ text: node.textContent, strong: node.nodeName === 'STRONG' })));
  let phraseIndex = 0, length = 0, deleting = false;
  function draw(parts, count) {
    const fragment = document.createDocumentFragment();
    for (const part of parts) {
      const text = part.text.slice(0, Math.max(0, count));
      const element = part.strong ? document.createElement('strong') : document.createTextNode(text);
      if (part.strong) element.textContent = text;
      fragment.append(element);
      count -= part.text.length;
    }
    target.replaceChildren(fragment);
  }
  function tick() {
    const parts = phrases[phraseIndex];
    const total = parts.reduce((sum, part) => sum + part.text.length, 0);
    length += deleting ? -1 : 1;
    draw(parts, length);
    let delay = deleting ? 35 : 65;
    if (!deleting && length === total) { deleting = true; delay = 1800; }
    else if (deleting && length === 0) { deleting = false; phraseIndex = (phraseIndex + 1) % phrases.length; delay = 250; }
    setTimeout(tick, delay);
  }
  if (reducedMotion) draw(phrases[0], Infinity);
  else tick();
})();
