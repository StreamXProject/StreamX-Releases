'use strict';
(() => {
  let collection = [], selected = 'apple-music', screen = 'home', mode = 'dark';
  const $ = id => document.getElementById(id);
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const songs = [['Afterglow', 'The evening edit', 'sunset'], ['Blue hour', 'Slow mornings', 'ocean'], ['In motion', 'Your daily rotation', 'orchid'], ['Sunday kind of love', 'A softer side', 'sand']];
  const art = (type, extra = '') => `<div class="cover cover-${type} ${extra}"><span></span></div>`;
  const heading = (skin, title, sub) => `<div class="mock-heading"><small>${escape(sub)}</small><h4>${escape(title)}</h4><span class="mock-avatar">S</span></div>`;
  const rows = (limit = 4) => `<div class="mock-rows">${songs.slice(0, limit).map(([title, artist, cover], i) => `<div class="mock-row">${art(cover)}<div><b>${title}</b><small>${artist}</small></div><span>${i === 0 ? '♫' : '⋮'}</span></div>`).join('')}</div>`;
  const nav = () => `<div class="mock-nav"><span class="${screen === 'home' ? 'selected' : ''}">⌂<small>Home</small></span><span>⌕<small>Search</small></span><span class="${screen === 'library' ? 'selected' : ''}">▥<small>Library</small></span></div>`;
  const mini = () => `<div class="mock-mini">${art('sunset')}<div><b>Afterglow</b><small>The evening edit</small></div><span>▷</span></div>`;
  function home(skin) {
    const titles = {'apple-music':['Listen Now','Made for you'],spotui:['Good evening','Your music, your way'],comic:['MAKE SOME NOISE!','ISSUE 01 / YOUR MUSIC'],dot:['YOUR FREQUENCY','STREAMX / 001'],meridian:['The evening edit','A MOMENT FOR MUSIC'],looper:['Hey, music lover.','Find your next favourite'],'material-expressive':['Hello, listener','A little more you'],'material-ui-3':['For you','Welcome back']};
    const [title, sub] = titles[skin.id];
    const quick = `<div class="mock-chips"><span>Music</span><span>Playlists</span><span>Albums</span></div>`;
    const tiles = `<div class="mock-quick">${songs.map(([title, , cover])=>`<div>${art(cover)}<b>${title}</b></div>`).join('')}</div>`;
    const shelves = `<h5>${skin.id === 'meridian' ? 'Selected for this moment' : 'Made for your mood'} <span>›</span></h5><div class="mock-shelf">${songs.slice(0,2).map(([title,artist,cover])=>`<div>${art(cover)}<b>${title}</b><small>${artist}</small></div>`).join('')}</div>`;
    return heading(skin,title,sub) + (skin.id === 'apple-music' ? shelves + '<h5>Recently played <span>›</span></h5>' + rows(2) : quick + tiles + shelves) + mini() + nav();
  }
  function library(skin) {
    return heading(skin, skin.id==='dot'?'COLLECTION_':'Your Library', skin.id==='comic'?'THE GOOD STUFF':'Your music, all together') + '<div class="mock-library-actions"><b>＋ New playlist</b><span>⇅</span></div><div class="mock-chips"><span>Playlists</span><span>Albums</span><span>Artists</span></div><div class="mock-favourite"><span>♥</span><div><b>Liked songs</b><small>All your favourites</small></div><span>›</span></div>' + rows(3) + mini() + nav();
  }
  function player(skin) {
    return `<div class="mock-player-top"><span>⌄</span><div><small>${skin.id==='dot'?'NOW_PLAYING':'PLAYING FROM YOUR LIBRARY'}</small><b>The evening edit</b></div><span>···</span></div>${art('sunset','player-cover')}<div class="mock-track"><div><h4>Afterglow</h4><p>The evening edit</p></div><span>♡</span></div><div class="mock-timeline"><div><span></span></div><p><span>1:24</span><span>3:42</span></p></div><div class="mock-controls"><span>⤨</span><span>◀</span><span class="mock-play">▶</span><span>▶</span><span>↻</span></div><div class="mock-player-bottom"><span>▤ Lyrics</span><span>☷ Queue</span></div><div class="mock-lyrics"><small>UP NEXT</small><b>Blue hour</b><p>Slow mornings</p></div>`;
  }
  function update(announce = true) {
    const skin = collection.find(s => s.id === selected);
    const phone = $('preview-phone'), palette = skin[mode];
    phone.className = `preview-phone skin-${skin.id} screen-${screen}`;
    phone.dataset.mode = mode;
    for (const [key,value] of Object.entries(palette)) phone.style.setProperty(`--skin-${key}`,value);
    phone.style.setProperty('--skin-radius', `${Math.min(skin.cornerRadiusDp,28)*.65}px`);
    phone.style.setProperty('--art-radius', `${skin.layout.artworkRadiusDp*.65}px`);
    phone.style.setProperty('--mini-radius', `${skin.layout.miniPlayerRadiusDp*.65}px`);
    phone.setAttribute('aria-label', `${skin.name}, ${screen} layout in ${mode} mode. Illustrative web preview.`);
    $('phone-content').innerHTML = screen === 'home' ? home(skin) : screen === 'library' ? library(skin) : player(skin);
    for (const element of document.querySelectorAll('button[data-skin]')) element.setAttribute('aria-pressed', String(element.dataset.skin === selected));
    for (const element of document.querySelectorAll('button[data-screen]')) element.setAttribute('aria-pressed', String(element.dataset.screen === screen));
    for (const element of document.querySelectorAll('button[data-mode]')) element.setAttribute('aria-pressed', String(element.dataset.mode === mode));
    $('skin-name').textContent=skin.name;
    $('skin-tagline').textContent=skin.tagline;
    $('skin-description').textContent=skin.description;
    $('skin-navigation').textContent=skin.layout.navigation === 'FLOATING' ? 'Floating bar' : 'Flat bar';
    $('skin-artwork').textContent=skin.layout.artworkRadiusDp === 0 ? 'Square corners' : `Rounded · ${skin.layout.artworkRadiusDp} dp`;
    $('skin-download').href=skin.download;
    $('skin-source').href=skin.source;
    $('skin-version').textContent=`v${skin.version} · Android skin APK`;
    if (announce) $('skin-status').textContent=`${skin.name} · ${screen.charAt(0).toUpperCase()+screen.slice(1)} · ${mode} mode`;
  }
  async function init() {
    try {
      const response = await fetch('skins.json');
      if (!response.ok) throw Error('Skin collection unavailable');
      collection = await response.json();
      if (!Array.isArray(collection) || !collection.length) throw Error('No skins');
      for (const skin of collection) {
        if (!/^[a-z0-9-]+$/.test(skin.id)) throw Error('Invalid skin');
        for (const palette of [skin.dark, skin.light]) {
          if (!['background','surface','surfaceVariant','text','secondary','accent'].every(key => /^#[0-9a-f]{6}$/i.test(palette[key]))) throw Error('Invalid palette');
        }
        const url = new URL(skin.download);
        if (url.origin !== 'https://github.com' || !url.pathname.startsWith('/StreamXProject/Skins/releases/download/')) throw Error('Invalid download');
        const button=document.createElement('button');
        button.type='button';button.className='skin-choice';button.dataset.skin=skin.id;
        button.innerHTML=`<span class="skin-swatch" aria-hidden="true"><i style="background:${skin.dark.background}"></i><i style="background:${skin.dark.surfaceVariant}"></i><i style="background:${skin.dark.accent}"></i></span><span>${escape(skin.name)}</span><span class="skin-check" aria-hidden="true">✓</span>`;
        button.addEventListener('click',()=>{selected=skin.id;update()});
        $('skin-choices').append(button);
      }
      document.querySelectorAll('button[data-screen]').forEach(button=>button.addEventListener('click',()=>{screen=button.dataset.screen;update()}));
      document.querySelectorAll('button[data-mode]').forEach(button=>button.addEventListener('click',()=>{mode=button.dataset.mode;update()}));
      update(false);$('skin-explorer').hidden=false;$('skin-fallback').hidden=true;
    } catch (error) { console.info('Skin preview unavailable.', error.message); }
  }
  init();
})();
