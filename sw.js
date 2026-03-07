const CACHE_NAME = 'caneta-segura-v1';
const urlsToCache = [
  '/',
  '/manifest.json'
];

// Instala o robô e guarda os arquivos na memória do celular
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Faz o aplicativo carregar mais rápido interceptando os pedidos
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // Retorna da memória se tiver
        }
        return fetch(event.request); // Se não, busca na internet
      })
  );
});