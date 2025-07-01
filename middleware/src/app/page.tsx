"use client";
import { useEffect } from 'react';

export default function RedirectPage() {
  useEffect(() => {
    const mainNewsUrl = process.env.NEXT_PUBLIC_MAIN_NEWS_URL;
    if (mainNewsUrl) {
      window.location.href = mainNewsUrl;
    }
  }, []);

  return null;
}
