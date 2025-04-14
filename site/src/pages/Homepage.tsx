import { useEffect, useState } from "react";
import { NewsData, NewsFeed } from "../components/NewsFeed";
import { useParams } from "react-router-dom";
import { getGameTitle } from "../utils.ts";
import TitleBar from "../components/TitleBar";

interface ArcadeNewsAPIData {
    fetch_time: number;
    news_posts: Array<NewsData>;
}

export default function Home() {
    const { gameId } = useParams<{ gameId?: string }>();
    const [newsFeedData, setNewsFeedData] = useState<ArcadeNewsAPIData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchNews = async () => {
            setLoading(true);
            const jsonFile = gameId ? `${gameId}_news.json` : "news.json";
            try {
                const response = await fetch("https://arcade-news.pinapelz.com/"+`${jsonFile}`);
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
                <div className="flex items-center justify-center h-screen bg-black">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-purple-600"></div>
                </div>
            </>
        );
    }

    return (
        <>
            <TitleBar />
            <div className="bg-gray-950 min-h-screen py-6">
                <div className="max-w-[600px] mx-auto px-4">
                    {gameId && (
                        <h1 className="text-2xl font-bold text-center text-white mb-6">
                            {getGameTitle(gameId)} News
                        </h1>
                    )}
                    <NewsFeed newsItems={newsFeedData.news_posts} />
                </div>
            </div>
        </>
    );
}
