import { useState, useEffect } from "react";
import { getGameTitle, getShortenedGameName } from "../utils.ts";
import { useSearchParams } from "react-router-dom";

export interface NewsData {
  date: string;
  identifier: string;
  type: string | null;
  timestamp: number;
  headline: string | null;
  content: string;
  url: string | null;
  images: Array<{
    image: string;
    link: string | null;
  }>;
  en_headline: string | null;
  en_content: string | null;
  is_ai_summary: boolean | null;
}

interface NewsFeedProps {
  newsItems: NewsData[];
}

export const NewsFeed: React.FC<NewsFeedProps> = ({ newsItems }) => {
  const [showEnglish, setShowEnglish] = useState<Record<string, boolean>>({});
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const [currentImageIndex, setCurrentImageIndex] = useState<Record<string, number>>({});
  const [loadingImages, setLoadingImages] = useState<Record<string, boolean>>({});
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");

  const toggleLanguage = (id: string) => setShowEnglish((prev) => ({ ...prev, [id]: !prev[id] }));
  const toggleExpand = (id: string) => setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  const changeImage = (id: string, i: number) => {
    if (currentImageIndex[id] == i)
      return
    setCurrentImageIndex((p) => ({ ...p, [id]: i }));
    setLoadingImages((p) => ({ ...p, [id]: true }));
  };
  const handleImageLoad = (id: string) => setLoadingImages((p) => ({ ...p, [id]: false }));
  const PREVIEW_CHAR_LIMIT = 600;

  useEffect(() => {
    const initialImageIndex: Record<string, number> = {};
    newsItems.forEach((news) => {
      const contentHash = news.content.split('').reduce((hash, char) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
      const headlineHash = (news.headline || 'null').split('').reduce((hash, char) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
      const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${headlineHash.toString(16)}`;
      initialImageIndex[newsId] = 0;
    });
    setCurrentImageIndex(initialImageIndex);
  }, [newsItems]);

  useEffect(() => {
    const fragment = window.location.hash.slice(1);
    if(fragment){
      const el = document.getElementById(fragment);
      if(el){
        el.scrollIntoView({behavior: "smooth", block: "start"});
      }
      else{
        alert("News Post doesn't or no longer exists...");
      }
    }
  }, [newsItems]);

  return (
    <div className="max-w-[600px] w-full mx-auto py-8 space-y-4 font-[Zen_Maru_Gothic]">
      {newsItems.map((news) => {
        const date = new Date(news.timestamp * 1000).toLocaleDateString("ja-JP", { year: "numeric", month: "2-digit", day: "2-digit" });
        const contentHash = news.content.split('').reduce((hash, char) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
        const headlineHash = (news.headline || 'null').split('').reduce((hash, char) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
        const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${headlineHash.toString(16)}`;
        const isEnglish = !!showEnglish[newsId];
        const hasTranslation = news.en_headline || news.en_content;
        const displayHeadline = isEnglish && news.en_headline ? news.en_headline : news.headline;
        const displayContent = isEnglish && news.en_content ? news.en_content : news.content;
        const isLong = displayContent.length > PREVIEW_CHAR_LIMIT;
        const isExpanded = !!expanded[newsId];
        const contentToShow = isLong && !isExpanded ? displayContent.slice(0, PREVIEW_CHAR_LIMIT) + "…" : displayContent;

        return (
          <div id={newsId} key={newsId} className={`${isMoe ? "bg-pink-100 border-pink-300 text-pink-900 font-[Zen_Maru_Gothic]" : "bg-gray-900 border-gray-800 text-white font-sans"} border rounded-lg shadow-lg overflow-hidden`}>
            <div className="flex items-center p-3 justify-between">
              <div className="flex items-center space-x-3">
                <a href={`/game/${getShortenedGameName(news.identifier)}`}>
                  <img
                    src={`https://arcade-news.pinapelz.com/`+getShortenedGameName(news.identifier)+`.webp`}
                    alt={getGameTitle(news.identifier) || ''}
                    className="hover:animate-pulse rounded-full h-8 w-8 object-cover"
                  />
                </a>
                <div className="flex flex-col leading-tight">
                  <span className="text-sm font-semibold hover:underline"><a href={`/game/${getShortenedGameName(news.identifier)}`}>{getGameTitle(news.identifier)}</a></span>
                  <span className="text-xs opacity-80">{date}</span>
                  {news.type && <span className="text-xs italic">{news.type}</span>}
                </div>
              </div>
              {hasTranslation && (
                <button onClick={() => toggleLanguage(newsId)} className={`${isMoe ? "bg-pink-200 hover:bg-pink-300" : "bg-gray-800 hover:bg-gray-700"} text-xs py-1 px-2 rounded`}>
                  {isEnglish ? "View Original" : "View in English"}
                </button>
              )}
            </div>

            <div className="px-3 pt-1 pb-3">
              {displayHeadline && <p className="font-semibold text-sm mb-2">{displayHeadline}</p>}
              <p className="text-sm whitespace-pre-line mb-2">
                {contentToShow.split(/(\[.*?\]\(.*?\)|https?:\/\/[^\s]+)/g).map((part, idx) => {
                  const m = part.match(/\[(.*?)\]\((.*?)\)/);
                  const u = part.match(/https?:\/\/[^\s]+/);
                  if (m) return <a key={idx} href={m[2]} className="text-blue-500 underline" target="_blank">{m[1]}</a>;
                  if (u) return <a key={idx} href={u[0]} className="text-blue-500 underline" target="_blank">{u[0]}</a>;
                  return part;
                })}
              </p>
              {isLong && (
                <button onClick={() => toggleExpand(newsId)} className="text-sm text-blue-500 hover:underline">
                  {isExpanded ? "Show less" : "Show more"}
                </button>
              )}
            </div>

            {/* Copy Link to Post */}
            <div className="px-3 pb-2 text-right">
              <a
                href={`#${newsId}`}
                onClick={(e) => {
                  e.preventDefault();
                  const url = `${window.location.origin}${window.location.pathname}#${newsId}`;
                  navigator.clipboard.writeText(url);
                  alert("Copied Direct Link to Post (Older news are automatically culled after some time)");
                }}
                title="Copy permalink"
                className="text-xs text-blue-400 hover:underline cursor-pointer"
              >
                🔗 Copy Link to Post
              </a>
            </div>

            {/* AI Disclaimer */}
            {news.is_ai_summary && (
              <div className={`${isMoe ? "bg-pink-200 text-pink-800" : "bg-gray-800 text-white"} px-3 py-2 text-xs text-center`}>
              The information above is written by AI / 上記の情報はAIによって生成されました。
              </div>
            )}

            {/* Machine TL Disclaimer */}
            {hasTranslation && isEnglish &&  (
              <div className={`${isMoe ? "bg-pink-200 text-pink-800" : "bg-gray-800 text-white"} px-3 py-2 text-xs text-center`}>
                The information above is machine translated and may contain inaccuracies
              </div>
            )}

            {/* Images */}
            {news.images.length > 0 && (
              <div className="w-full">
                {(() => {
                  const idx = currentImageIndex[newsId] || 0;
                  const img = news.images[idx];
                  return (
                    <div className="relative">
                      {loadingImages[newsId] && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                          <div className="loader border-t-2 border-b-2 border-white w-6 h-6 rounded-full animate-spin" />
                        </div>
                      )}
                      <img
                        src={img.image}
                        alt="news visual"
                        className={`w-full object-cover py-2 ${loadingImages[newsId] ? "opacity-0" : "opacity-100"}`}
                        onLoad={() => handleImageLoad(newsId)}
                      />
                    </div>
                  );
                })()}

                {news.images.length > 1 && (
                  <div className="pb-3 overflow-x-auto px-3">
                    <div className="flex space-x-2 w-max mx-auto">
                      {news.images.map((_, idx) => (
                        <button
                          key={idx}
                          onClick={() => changeImage(newsId, idx)}
                          className={`w-9 h-9 flex-shrink-0 rounded-sm flex items-center justify-center ${
                            currentImageIndex[newsId] === idx
                              ? isMoe ? "bg-pink-500 text-white" : "bg-blue-600 text-white"
                              : isMoe ? "bg-pink-200 text-pink-800 hover:bg-pink-300" : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                          }`}
                        >
                          {idx + 1}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {news.url && (
              <div className={`${isMoe ? "bg-pink-200" : "bg-gray-800"} px-3 py-2 text-center`}>
                <a href={news.url} target="_blank" rel="noopener noreferrer" className="text-sm underline font-bold">
                  READ MORE
                </a>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
