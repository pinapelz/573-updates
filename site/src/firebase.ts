import { initializeApp } from "firebase/app";
import { getMessaging, Messaging, onMessage } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyAkxH71PlZJxhD7vuN_Q8kn3TtNnB09_cU",
  authDomain: "updates-9eab8.firebaseapp.com",
  projectId: "updates-9eab8",
  storageBucket: "updates-9eab8.firebasestorage.app",
  messagingSenderId: "347275855103",
  appId: "1:347275855103:web:fb59a7504792c2736538ca"
};

const app = initializeApp(firebaseConfig);

export const messaging: Messaging = getMessaging(app);

// Handle foreground messages
export const initializeForegroundNotifications = () => {
  onMessage(messaging, (payload) => {
    console.log('[firebase.ts] Message received in foreground:', payload);

    // Check if browser supports notifications
    if (!("Notification" in window)) {
      console.log("This browser does not support desktop notifications");
      return;
    }

    // Check notification permission
    if (Notification.permission === "granted") {
      // Create notification
      const notificationTitle = payload.notification?.title || 'New Update';
      const notificationOptions: NotificationOptions = {
        body: payload.notification?.body || 'You have a new notification',
        icon: payload.notification?.icon || '/android/android-launchericon-192-192.png',
        badge: '/android/android-launchericon-72-72.png',
        tag: payload.data?.tag || 'default-tag',
        requireInteraction: payload.data?.requireInteraction === 'true',
        silent: false,
        data: {
          url: payload.data?.url || '/',
          gameId: payload.data?.gameId,
          ...payload.data
        }
      };

      // Add image if provided
      if (payload.notification?.image) {
        notificationOptions.badge = payload.notification.image;
      }

      // Create and show the notification
      const notification = new Notification(notificationTitle, notificationOptions);

      // Handle notification click
      notification.onclick = (event) => {
        event.preventDefault();
        notification.close();

        // Navigate to the URL if provided
        const url = payload.data?.url || '/';
        window.open(url, '_blank');
      };

      // Handle notification error
      notification.onerror = (event) => {
        console.error('[firebase.ts] Notification error:', event);
      };

      // Auto-close notification after 10 seconds if not require interaction
      if (payload.data?.requireInteraction !== 'true') {
        setTimeout(() => {
          notification.close();
        }, 10000);
      }
    } else {
      console.log('[firebase.ts] Notification permission not granted');
    }
  });

  console.log('[firebase.ts] Foreground notification handler initialized');
};
