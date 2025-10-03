import { useState, useEffect } from "react";
import { messaging, initializeForegroundNotifications } from "../firebase.ts";
import { getToken, deleteToken } from "firebase/messaging";

const VAPID_KEY =
  "BK7tpLF5Loy8Ew8bKxhTi-vOEJdxJSnu-jPyagWecLdD_SrEAt_OQS7nu0Xu3hR7AQpn0cOmgcdeeQd5zq5-Gyo";

interface NotificationButtonProps {
  className?: string;
  isMoe?: boolean;
}

export default function NotificationButton({ className = "", isMoe = false }: NotificationButtonProps) {
  const [permission, setPermission] = useState<NotificationPermission>("default");
  const [isRegistered, setIsRegistered] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check initial permission status
    setPermission(Notification.permission);

    // Check if service worker is registered
    const checkRegistration = async () => {
      if ('serviceWorker' in navigator) {
        const registration = await navigator.serviceWorker.getRegistration('/firebase-messaging-sw.js');
        setIsRegistered(!!registration);
        
        // Initialize foreground notifications if already registered
        if (registration && Notification.permission === "granted") {
          initializeForegroundNotifications();
        }
      }
    };

    checkRegistration();
  }, []);

  const handleEnableNotifications = async () => {
    setLoading(true);
    setError(null);

    try {
      const permissionResult = await Notification.requestPermission();
      setPermission(permissionResult);

      if (permissionResult === "granted") {
        // Register service worker
        const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
        console.log("Service Worker registered:", registration);
        const token = await getToken(messaging, { vapidKey: VAPID_KEY });
        console.log("FCM Token:", token);
        // Store token locally (you might want to send this to your server)
        localStorage.setItem('fcm_token', token);

        // Initialize foreground notification handler
        initializeForegroundNotifications();

        setIsRegistered(true);
      } else {
        setError("Notification permission was denied");
      }
    } catch (err) {
      console.error("Error enabling notifications:", err);
      setError("Failed to enable notifications. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDisableNotifications = async () => {
    setLoading(true);
    setError(null);

    try {
      await deleteToken(messaging);
      console.log("FCM token deleted");
      localStorage.removeItem('fcm_token');
      if ('serviceWorker' in navigator) {
        const registration = await navigator.serviceWorker.getRegistration('/firebase-messaging-sw.js');
        if (registration) {
          await registration.unregister();
          console.log("Service Worker unregistered");
        }
      }

      setIsRegistered(false);
    } catch (err) {
      console.error("Error disabling notifications:", err);
      setError("Failed to disable notifications. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Determine button state and action
  const getButtonContent = () => {
    if (loading) {
      return (
        <>
          <svg className="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {isRegistered ? "Disabling..." : "Enabling..."}
        </>
      );
    }

    if (permission === "denied") {
      return (
        <>
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
          </svg>
          Notifications Blocked
        </>
      );
    }

    if (isRegistered && permission === "granted") {
      return (
        <>
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          Disable Notifications
        </>
      );
    }

    return (
      <>
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        Enable Notifications
      </>
    );
  };

  const handleClick = () => {
    if (permission === "denied") {
      // Can't re-request permission if denied
      alert("Notifications are blocked. Please enable them in your browser settings.");
      return;
    }

    if (isRegistered && permission === "granted") {
      handleDisableNotifications();
    } else {
      handleEnableNotifications();
    }
  };

  // Determine button styles
  const getButtonStyles = () => {
    if (loading || permission === "denied") {
      return isMoe
        ? `bg-pink-300 cursor-not-allowed opacity-60`
        : `bg-gray-600 cursor-not-allowed opacity-60`;
    }

    if (isMoe) {
      return isRegistered
        ? `bg-pink-600 text-white hover:bg-pink-700`
        : `bg-pink-500 text-white hover:bg-pink-600`;
    } else {
      return isRegistered
        ? `bg-purple-700 text-white hover:bg-purple-800`
        : `bg-purple-600 text-white hover:bg-purple-700`;
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <button
        onClick={handleClick}
        disabled={loading || permission === "denied"}
        className={`flex items-center justify-center px-4 py-2 rounded-lg font-semibold transition-colors ${getButtonStyles()} ${className}`}
      >
        {getButtonContent()}
      </button>
      {error && (
        <p className={`text-sm ${isMoe ? "text-pink-600" : "text-red-500"}`}>
          {error}
        </p>
      )}
      {permission === "denied" && (
        <p className={`text-xs ${isMoe ? "text-pink-600" : "text-gray-400"}`}>
          To enable notifications, update your browser settings
        </p>
      )}
    </div>
  );
}
