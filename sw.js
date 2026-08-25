// Production PWA Service Worker for Kinslow Regulatory Archive (kinslow-regulatory-archive.org)
const CACHE_NAME = 'kinslow-archive-v2';
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/thumbnail.webp',
  '/icon-192.png',
  '/icon-512.png',
  '/thumbnail.jpg'
];

// Install: Pre-cache core assets for offline PWA compliance
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.debug('Pre-caching skipped non-critical asset:', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate: Clean up any old caches immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch: Network-First with Cache Fallback for PWA offline compliance
// NEVER intercepts or blocks video, audio, media streaming, or Range requests
self.addEventListener('fetch', (event) => {
  const request = event.request;

  // 1. Only handle GET requests
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // 2. DO NOT intercept media/video streaming or HTTP Range requests
  // HTML5 videos require HTTP 206 Partial Content which native browser networking handles
  const isMedia = /\.(mp4|webm|ogg|mov|mp3|wav|m4a)$/i.test(url.pathname);
  const isRangeRequest = request.headers.has('range');
  const isVideoDestination = request.destination === 'video' || request.destination === 'audio';

  if (isMedia || isRangeRequest || isVideoDestination) {
    return; // Pass through directly to native network
  }

  // 3. DO NOT intercept cross-origin third-party requests
  if (url.origin !== location.origin) {
    return; // Pass through directly to network
  }

  // 4. Network-First Strategy for all HTML, CSS, JS, and Images
  // Always fetches the fresh asset over the network first, updating cache in background.
  // Falls back to cache ONLY if user is offline (preserving 100% PWA score).
  event.respondWith(
    fetch(request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // Offline fallback
        return caches.match(request);
      })
  );
});


