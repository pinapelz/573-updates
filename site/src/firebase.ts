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
