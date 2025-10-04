import { initializeApp } from "firebase/app";
import { getMessaging, Messaging, onMessage } from "firebase/messaging";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);

export const messaging: Messaging = getMessaging(app);
let foregroundInitialized = false;

// Handle foreground messages
export const initializeForegroundNotifications = () => {
  if (foregroundInitialized) return; // Prevent double registration
  foregroundInitialized = true;

  onMessage(messaging, (payload) => {
    console.log("[firebase.ts] Foreground message received", payload);

    if (Notification.permission !== "granted") return;

    const data = payload.data || {};
    const title = data.title || "New Update";
    const options: NotificationOptions = {
      body: data.body || "You have a new notification",
      icon: data.icon || "/android/android-launchericon-192-192.png",
      badge: data.badge || "/android/android-launchericon-72-72.png",
      tag: data.tag || "default-tag",
      requireInteraction: data.requireInteraction === "true",
      silent: false,
      data,
    };

    const notification = new Notification(title, options);

    notification.onclick = (event) => {
      event.preventDefault();
      notification.close();
      const url = data.url || "/";
      window.open(url, "_blank");
    };

    if (data.requireInteraction !== "true") {
      setTimeout(() => notification.close(), 10000);
    }
  });

  console.log("[firebase.ts] Foreground notification handler initialized");
};
