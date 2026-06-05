self.addEventListener('install', (event) => {
  console.log('SW installed');
  self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  // Basic pass-through fetch to satisfy PWA requirements
  event.respondWith(fetch(event.request).catch(() => {
    return new Response('Offline mode: Please connect to the internet.');
  }));
});
