// Aggressive Cache-Buster & Self-Unregister Service Worker
self.addEventListener('install', function(e) {
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          console.log('[SW] Purging cache:', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).then(function() {
      return self.clients.claim();
    }).then(function() {
      return self.registration.unregister();
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request, { cache: 'no-store' }).catch(function() {
      return fetch(event.request);
    })
  );
});
