/* ─────────────────────────────────────────
   Launchpad — Service Worker v1.0
   Cache shell + network-first for API
───────────────────────────────────────── */
const CACHE  = 'launchpad-v1';
const SHELL  = ['./', './index.html', './manifest.json', './icon-192.svg', './icon-512.svg'];

// Install: cache shell assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: network-first for API, cache-first for shell
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Always network-first for GitHub API
  if (url.hostname === 'api.github.com' || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(
      fetch(e.request)
        .catch(() => new Response('{"error":"offline"}', {
          headers: { 'Content-Type': 'application/json' }
        }))
    );
    return;
  }

  // Cache-first for shell
  e.respondWith(
    caches.match(e.request)
      .then(cached => cached || fetch(e.request).then(res => {
        if (res.ok && e.request.method === 'GET') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }))
      .catch(() => caches.match('./index.html'))
  );
});
