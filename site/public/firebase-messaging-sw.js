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

// Handle background messages
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message', payload);
  
  // Extract notification data
  const notificationTitle = payload.notification?.title || 'New Update';
  const notificationBody = payload.notification?.body || 'You have a new notification';
  
  // Build notification options with enhanced features
  const notificationOptions = {
    body: notificationBody,
    icon: payload.notification?.icon || '/android/android-launchericon-192-192.png',
    badge: '/android/android-launchericon-72-72.png',
    vibrate: [200, 100, 200],
    tag: payload.data?.tag || 'default-tag',
    requireInteraction: payload.data?.requireInteraction === 'true',
    renotify: true,
    silent: false,
    timestamp: Date.now(),
    data: {
      url: payload.data?.url || '/',
      gameId: payload.data?.gameId,
      ...payload.data
    }
  };

  // Add image if provided
  if (payload.notification?.image) {
    notificationOptions.image = payload.notification.image;
  }

  // Add actions if provided
  if (payload.data?.actions) {
    try {
      notificationOptions.actions = JSON.parse(payload.data.actions);
    } catch (e) {
      console.error('Failed to parse notification actions:', e);
    }
  }

  // Show the notification
  return self.registration.showNotification(notificationTitle, notificationOptions);
});

// Handle notification clicks
self.addEventListener('notificationclick', function(event) {
  console.log('[firebase-messaging-sw.js] Notification click received.', event);
  
  event.notification.close();

  // Handle action clicks
  if (event.action) {
    console.log('Action clicked:', event.action);
    // You can handle different actions here
    if (event.action === 'view') {
      event.waitUntil(
        clients.openWindow(event.notification.data?.url || '/')
      );
    } else if (event.action === 'dismiss') {
      // Just close the notification
      return;
    }
  } else {
    // Default click behavior - open the URL
    const clickUrl = event.notification.data?.url || '/';
    
    event.waitUntil(
      clients.matchAll({
        type: 'window',
        includeUncontrolled: true
      }).then(function(clientList) {
        // Check if there's already a window/tab open with the target URL
        for (const client of clientList) {
          if (client.url === clickUrl && 'focus' in client) {
            return client.focus();
          }
        }
        // If no existing window/tab, open a new one
        if (clients.openWindow) {
          return clients.openWindow(clickUrl);
        }
      })
    );
  }
});

// Handle notification close
self.addEventListener('notificationclose', function(event) {
  console.log('[firebase-messaging-sw.js] Notification was closed', event);
  // You can track notification dismissals here if needed
});

// Handle service worker installation
self.addEventListener('install', function(event) {
  console.log('[firebase-messaging-sw.js] Service Worker installing.');
  self.skipWaiting();
});

// Handle service worker activation
self.addEventListener('activate', function(event) {
  console.log('[firebase-messaging-sw.js] Service Worker activated.');
  event.waitUntil(clients.claim());
});

// Handle push events (for debugging)
self.addEventListener('push', function(event) {
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

// Error handling
self.addEventListener('error', function(event) {
  console.error('[firebase-messaging-sw.js] Service Worker error:', event);
});

// Fetch event handler for offline support (optional)
self.addEventListener('fetch', function(event) {
  // You can add offline caching strategies here if needed
  // For now, just pass through the request
  return;
});