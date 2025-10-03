import { useEffect, useState } from "react";
import { NewsData, NewsFeed } from "../components/NewsFeed";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { getGameTitle } from "../utils.ts";
import TitleBar from "../components/TitleBar";
import { GameNotes } from "../components/GameNotes";
import NotificationButton from "../components/NotificationButton";

interface ArcadeNewsAPIData {
  fetch_time: number;
  news_posts: Array<NewsData>;
}

export default function Home() {
  const { gameId } = useParams<{ gameId?: string }>();
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");
  const rssFeedUrl =
    import.meta.env.VITE_NEWS_BASE_URL + "/" + gameId + "_news.xml";
  const newsAPIBase = import.meta.env.VITE_NEWS_BASE_URL;

  const [newsFeedData, setNewsFeedData] = useState<ArcadeNewsAPIData | null>(
    null,
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);
  const [subscribedGames, setSubscribedGames] = useState<string[]>([]);
  const [showSubscribedDropdown, setShowSubscribedDropdown] = useState(false);

  useEffect(() => {
    // Load subscribed games from localStorage
    const loadSubscribedGames = () => {
      const topics = JSON.parse(localStorage.getItem('subscribed_topics') || '[]');
      setSubscribedGames(topics);
    };

    loadSubscribedGames();

    // Listen for storage changes to update subscribed games list
    const handleStorageChange = () => {
      loadSubscribedGames();
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      setError(false);
      const newsDataFileName = gameId ? `${gameId}_news.json` : "news.json";
      try {
        const response = await fetch(newsAPIBase + "/" + `${newsDataFileName}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch news: ${response.statusText}`);
        }
        const data: ArcadeNewsAPIData = await response.json();
        setNewsFeedData(data);
      } catch (e) {
        console.error(e);
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, [gameId, newsAPIBase]); // Re-fetch when gameId changes

  // Update subscribed games when localStorage changes locally
  useEffect(() => {
    const checkSubscriptions = () => {
      const topics = JSON.parse(localStorage.getItem('subscribed_topics') || '[]');
      setSubscribedGames(topics);
    };

    const interval = setInterval(checkSubscriptions, 500);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
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

  if (error || newsFeedData === null) {
    return (
      <>
        <TitleBar />
        <div
          className={`${isMoe ? "bg-pink-100" : "bg-gray-950"} min-h-screen flex items-center justify-center`}
        >
          <div className="text-center px-4">
            <div
              className={`${isMoe ? "text-pink-500" : "text-purple-500"} text-8xl font-bold mb-4`}
            >
              404
            </div>
            <h1
              className={`${isMoe ? "text-pink-900" : "text-white"} text-3xl font-bold mb-4`}
            >
              News Not Found
            </h1>
            <p
              className={`${isMoe ? "text-pink-700" : "text-gray-400"} text-lg mb-8`}
            >
              {gameId
                ? `Unable to fetch news for ${getGameTitle(gameId)}`
                : "Unable to fetch news feed"}
            </p>
            <div
              className={`${isMoe ? "bg-pink-200" : "bg-gray-800"} rounded-lg p-6 max-w-md mx-auto`}
            >
              <p
                className={`${isMoe ? "text-pink-800" : "text-gray-300"} mb-4`}
              >
                The news feed you're looking for might be temporarily
                unavailable or doesn't exist.
              </p>
              <a
                href="/"
                className={`inline-block px-6 py-3 rounded-lg font-semibold transition-colors ${
                  isMoe
                    ? "bg-pink-500 text-white hover:bg-pink-600"
                    : "bg-purple-600 text-white hover:bg-purple-700"
                }`}
              >
                Return Home
              </a>
            </div>
          </div>
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
              {/* <div className="mt-4">
                <NotificationButton gameId={gameId} isMoe={isMoe} />
              </div>
              <p className="text-left">
                Currently in testing, not all games will receive updates via notifications yet.
              </p> */}
              <div className="mt-2">
                <a href={rssFeedUrl} className="text-blue-400 hover:underline">
                  Subscribe via RSS
                </a>
              </div>
            </div>
          ) : (
            <>
              <div
                className={`${isMoe ? "bg-pink-200 text-pink-900" : "bg-gray-800 text-white"} rounded-lg p-6 text-center shadow-lg`}
              >
                <h1 className="text-2xl font-bold">Welcome to 573-UPDATES</h1>
                <h2
                  className={`text-2xl font-extrabold mb-4 tracking-widest text-center uppercase glow-neon ${
                    isMoe ? "text-pink-500" : "text-[#00FF00]"
                  }`}
                >
                  SECOND STYLE
                </h2>
                <div className="floating">
                  <img
                    src="/liris.webp"
                    className="w-48 mx-auto mb-2 object-contain rounded-2xl"
                  />
                </div>
                <p>
                  News and Information for various arcade games is aggregated
                  here!
                </p>
                <p className="mt-2">
                  RSS feeds are available on each game's individual page
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
                <div className="mt-6">
                  <div className="mt-4">
                    {/* <NotificationButton isMoe={isMoe} /> */}

                    {/* Subscribed Games Display */}
                    {subscribedGames.length > 0 && (
                      <div className="mt-3">
                        <button
                          onClick={() => setShowSubscribedDropdown(!showSubscribedDropdown)}
                          className={`text-sm ${
                            isMoe ? "text-pink-700 hover:text-pink-500" : "text-gray-300 hover:text-white"
                          } flex items-center gap-1 mx-auto transition-colors`}
                        >
                          <span>Subscribed to {subscribedGames.length} game{subscribedGames.length !== 1 ? 's' : ''}</span>
                          <svg
                            className={`w-4 h-4 transition-transform ${showSubscribedDropdown ? 'rotate-180' : ''}`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                        </button>

                        {showSubscribedDropdown && (
                          <div className={`mt-2 p-3 rounded-lg ${
                            isMoe ? "bg-pink-300 bg-opacity-50" : "bg-gray-700 bg-opacity-50"
                          }`}>
                            <div className="grid grid-cols-2 gap-2 text-sm">
                              {subscribedGames.map((gameId) => (
                                <Link
                                  key={gameId}
                                  to={`/game/${gameId}`}
                                  className={`${
                                    isMoe
                                      ? "text-pink-700 hover:text-pink-500 hover:bg-pink-200"
                                      : "text-gray-300 hover:text-white hover:bg-gray-600"
                                  } px-2 py-1 rounded transition-all`}
                                >
                                  {getGameTitle(gameId)}
                                </Link>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
          <NewsFeed newsItems={newsFeedData.news_posts} />
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
