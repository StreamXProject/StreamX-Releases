'use strict';
window.streamxExtensionManifest = (async () => {
  const response = await fetch('extensions/index.json', {cache: 'no-cache'});
  if (!response.ok) throw new Error(`Manifest HTTP ${response.status}`);
  const manifest = await response.json();
  if (manifest.schemaVersion !== 1 || !Array.isArray(manifest.extensions) || manifest.extensions.length > 500) throw new Error('Invalid extension manifest');
  for (const entry of manifest.extensions) {
    const url = new URL(entry.apkUrl);
    if (!['plugin', 'skin'].includes(entry.type) || url.origin !== 'https://github.com' ||
        !url.pathname.startsWith('/StreamXProject/StreamX-Releases/releases/download/')) throw new Error('Invalid public extension');
  }
  return manifest;
})();
(async () => {
  const input = document.getElementById('repository-url');
  document.getElementById('copy-repository').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(input.value);
      document.getElementById('copy-status').textContent = 'Repository link copied.';
    } catch {
      input.focus(); input.select();
      document.getElementById('copy-status').textContent = 'Link selected. Copy it from the address box.';
    }
  });
  try {
    const manifest = await window.streamxExtensionManifest;
    const groups = new Map();
    for (const entry of manifest.extensions) {
      if (!groups.has(entry.packageName)) groups.set(entry.packageName, []);
      groups.get(entry.packageName).push(entry);
    }
    const plugins = [], skins = [];
    for (const variants of groups.values()) {
      const newest = Math.max(...variants.map(entry => entry.versionCode));
      const current = variants.filter(entry => entry.versionCode === newest);
      const first = current[0];
      if (first.type === 'plugin') {
        const article = document.createElement('article'); article.className = 'public-plugin card';
        const name = document.createElement('h3');
        name.textContent = ({applemusic: 'Apple Music', spotify: 'Spotify', cloudstream: 'CloudStream', amazonmusic: 'Amazon Music'})[first.id] || first.name;
        const detail = document.createElement('p'); detail.textContent = `v${first.versionName} · Android music source`;
        const links = document.createElement('div'); links.className = 'asset-links';
        for (const entry of current) {
          const a = document.createElement('a'); a.href = entry.apkUrl;
          a.textContent = `${entry.abis.length ? entry.abis.join(', ') : 'Download APK'} · ${(entry.size / 1048576).toFixed(1)} MB ↓`;
          links.append(a);
        }
        article.append(name, detail, links); plugins.push(article);
      } else {
        const a = document.createElement('a'); a.href = first.apkUrl;
        a.textContent = `${first.name} ↓`; skins.push(a);
      }
    }
    if (plugins.length) document.getElementById('public-plugins').replaceChildren(...plugins);
    if (skins.length) {
      document.getElementById('public-skins').replaceChildren(...skins);
      document.getElementById('public-skin-count').textContent = `(${skins.length})`;
    }
  } catch (error) { console.info('Extension downloads unavailable.', error.message); }
})();
