import { useEffect, useState } from "react";
import { NewsData, NewsFeed } from "../components/NewsFeed";
import { useParams } from "react-router-dom";
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
            let jsonFile = "news.json";
            if (gameId) {
                switch(gameId) {
                    case "sdvx":
                        jsonFile = "sdvx_news.json";
                        break;
                    case "iidx":
                        jsonFile = "iidx_news.json";
                        break;
                    case "chunithm_jp":
                        jsonFile = "chunithm_jp_news.json";
                        break;
                    default:
                        jsonFile = "news.json";
                }
            }
            
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

    // Game-specific title mapping
    const getGameTitle = () => {
        if (!gameId) return null;
        
        switch(gameId) {
            case "sdvx": return "SOUND VOLTEX";
            case "iidx": return "beatmania IIDX";
            case "chunithm_jp": return "CHUNITHM (JAPAN)";
            default: return gameId.toUpperCase();
        }
    };

    return (
        <>
            <TitleBar />
            <div className="bg-gray-950 min-h-screen py-6">
                <div className="max-w-[600px] mx-auto px-4">
                    {gameId && (
                        <h1 className="text-2xl font-bold text-center text-white mb-6">
                            {getGameTitle()} News
                        </h1>
                    )}
                    <NewsFeed newsItems={newsFeedData.news_posts} />
                </div>
            </div>
        </>
    );
}