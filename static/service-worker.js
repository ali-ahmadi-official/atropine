const CACHE_NAME = 'atropine';
const ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/images/favicon.ico'
];

// نصب سرویس‌کار و کش کردن فایل‌ها
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

// پاسخ دادن از کش در صورت نبود اینترنت
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
