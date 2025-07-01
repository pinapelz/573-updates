import { useEffect, useState } from "react";
import { NewsData, NewsFeed } from "../components/NewsFeed";
import { useParams, useSearchParams } from "react-router-dom";
import { getGameTitle } from "../utils.ts";
import TitleBar from "../components/TitleBar";
import { GameNotes } from "../components/GameNotes";

interface ArcadeNewsAPIData {
  fetch_time: number;
  news_posts: Array<NewsData>;
}

export default function Home() {
  const { gameId } = useParams<{ gameId?: string }>();
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");
  const newsAPIBase = import.meta.env.VITE_NEWS_BASE_URL

  const [newsFeedData, setNewsFeedData] = useState<ArcadeNewsAPIData | null>(
    null,
  );
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      const newsDataFileName = gameId ? `${gameId}_news.json` : "news.json";
      try {
        const response = await fetch(
          newsAPIBase+"/" + `${newsDataFileName}`,
        );
        if (!response.ok) {
          throw new Error(`Failed to fetch news: ${response.statusText}`);
        }
        const data: ArcadeNewsAPIData = await response.json();
        setNewsFeedData(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, [gameId]); // Re-fetch when gameId changes

  if (loading || newsFeedData === null) {
    return (
      <>
        <TitleBar />
        <div
          className={`flex items-center justify-center h-screen ${isMoe ? "bg-pink-100" : "bg-black"}`}
        >
          <div
            className={`animate-spin rounded-full h-16 w-16 border-t-4 ${isMoe ? "border-pink-500" : "border-purple-600"}`}
          ></div>
        </div>
      </>
    );
  }

  return (
    <>
      <TitleBar />
      <div
        className={`${isMoe ? "bg-pink-100 text-pink-900 font-[Zen_Maru_Gothic]" : "bg-gray-950"} min-h-screen py-6`}
      >
        <div className="max-w-[600px] mx-auto px-4">
          {gameId ? (
            <div
              className={`${isMoe ? "bg-pink-200 text-pink-900" : "bg-gray-800 text-white"} rounded-lg p-6 text-center shadow-lg`}
            >
              <h1 className="text-2xl font-bold mb-2">
                {getGameTitle(gameId)} News
              </h1>
              {GameNotes(isMoe)[gameId] && (
                <div className="text-left">{GameNotes(isMoe)[gameId]}</div>
              )}
            </div>
          ) : (
            <div
              className={`${isMoe ? "bg-pink-200 text-pink-900" : "bg-gray-800 text-white"} rounded-lg p-6 text-center shadow-lg`}
            >
              <h1 className="text-2xl font-bold">Welcome to 573-UPDATES</h1>
              <div className="floating">
                <img
                  src="/xiatian.webp"
                  className="w-48 mx-auto mb-2 object-contain rounded-2xl"
                />
              </div>
              <p>
                News and Information for various arcade games is aggregated
                here!
              </p>
              <p className="mt-2">
                Please see the{" "}
                <a
                  href="https://github.com/pinapelz/573-updates"
                  className="text-blue-500 hover:underline"
                >
                  GitHub
                </a>{" "}
                for API information
              </p>
            </div>
          )}
          <NewsFeed newsItems={newsFeedData.news_posts}/>
        </div>
        <footer
          className={`mt-8 text-center text-sm ${isMoe ? "text-pink-800" : "text-gray-400"}`}
        >
          <p>
            Last updated:{" "}
            {new Date(newsFeedData.fetch_time * 1000).toLocaleString()}
          </p>
          <p>
            <a
              href="https://moekyun.me/"
              className={`${isMoe ? "text-pink-600 hover:text-pink-400" : "hover:underline"}`}
            >
              a moekyun service
            </a>
          </p>
        </footer>
      </div>
    </>
  );
}
