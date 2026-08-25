// Production PWA Service Worker for Kinslow Regulatory Archive (kinslow-regulatory-archive.org)
const CACHE_NAME = 'kinslow-archive-v5-network-first';

// Install: Immediately activate new service worker without waiting
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

// Activate: Immediately purge ALL old caches and take control of all open tabs
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: NETWORK-FIRST strategy so live CSS and HTML changes appear immediately
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // Fallback to cache ONLY when offline
        return caches.match(event.request);
      })
  );
});
