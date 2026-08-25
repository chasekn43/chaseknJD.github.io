// Production PWA Service Worker for Kinslow Regulatory Archive (kinslow-regulatory-archive.org)
const CACHE_NAME = 'kinslow-archive-v4';
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/index.css',
  '/manifest.json',
  '/favicon.ico',
  '/thumbnail.webp',
  '/icon-192.png',
  '/icon-512.png',
  '/tools/bnpl-refund-delay-diagnostic.html',
  '/tools/affirm-bot-bypass-cheat-sheet.html',
  '/tools/underwriting-credit-impact-calculator.html',
  '/tools/reddit-community-response-toolkit.html'
];

// Install: Pre-cache core assets for offline PWA compliance
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.debug('Pre-caching skipped non-critical assets:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Stale-while-revalidate strategy for maximum speed and offline support
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        return cachedResponse;
      });
      return cachedResponse || fetchPromise;
    })
  );
});
