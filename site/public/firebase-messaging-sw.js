importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyAkxH71PlZJxhD7vuN_Q8kn3TtNnB09_cU",
  authDomain: "updates-9eab8.firebaseapp.com",
  projectId: "updates-9eab8",
  storageBucket: "updates-9eab8.firebasestorage.app",
  messagingSenderId: "347275855103",
  appId: "1:347275855103:web:fb59a7504792c2736538ca"
});

const messaging = firebase.messaging();

// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  console.log('[firebase-messaging-sw.js] Notification click received.', event);
  event.notification.close();

  const clickUrl = event.notification.data?.url || '/';

  if (event.action) {
    if (event.action === 'view') {
      event.waitUntil(clients.openWindow(clickUrl));
    }
    return;
  }

  // Default click behavior
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
      for (const client of clientList) {
        if (client.url === clickUrl && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(clickUrl);
      }
    })
  );
});

// Handle notification close
self.addEventListener('notificationclose', function(event) {
  console.log('[firebase-messaging-sw.js] Notification was closed', event);
});

// Install & activate
self.addEventListener('install', event => {
  console.log('[firebase-messaging-sw.js] Service Worker installing.');
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  console.log('[firebase-messaging-sw.js] Service Worker activated.');
  event.waitUntil(clients.claim());
});

// Debugging push events
self.addEventListener('push', event => {
  console.log('[firebase-messaging-sw.js] Push event received', event);
  if (event.data) {
    try {
      const data = event.data.json();
      console.log('[firebase-messaging-sw.js] Push data:', data);
    } catch (e) {
      console.log('[firebase-messaging-sw.js] Push data text:', event.data.text());
    }
  }
});
