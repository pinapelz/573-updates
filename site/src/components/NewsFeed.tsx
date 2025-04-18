import { useState } from "react";
import { getGameTitle } from "../utils.ts";

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
}

interface NewsFeedProps {
  newsItems: NewsData[];
}

export const NewsFeed: React.FC<NewsFeedProps> = ({ newsItems }) => {
  // Track which items are showing English content
  const [showEnglish, setShowEnglish] = useState<Record<string, boolean>>({});
  // Track which items are expanded beyond the preview
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  // Track the current image index for each news item
  const [currentImageIndex, setCurrentImageIndex] = useState<Record<string, number>>({});
  // Track loading state for images
  const [loadingImages, setLoadingImages] = useState<Record<string, boolean>>({});

  const toggleLanguage = (itemId: string) => {
    setShowEnglish((prev) => ({ ...prev, [itemId]: !prev[itemId] }));
  };

  const toggleExpand = (itemId: string) => {
    setExpanded((prev) => ({ ...prev, [itemId]: !prev[itemId] }));
  };

  const changeImage = (itemId: string, index: number) => {
    setCurrentImageIndex((prev) => ({ ...prev, [itemId]: index }));
    setLoadingImages((prev) => ({ ...prev, [itemId]: true })); // Set loading state for the image
  };

  const handleImageLoad = (itemId: string) => {
    setLoadingImages((prev) => ({ ...prev, [itemId]: false })); // Clear loading state when image loads
  };

  const PREVIEW_CHAR_LIMIT = 600;

  return (
    <div className="max-w-[600px] w-full mx-auto py-8 space-y-4">
      {newsItems.map((news) => {
        const formattedDate = new Date(news.timestamp * 1000).toLocaleDateString("ja-JP", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
        });

        const newsId = `${news.identifier}-${news.timestamp}-${news.content.substring(0, 20)}`;
        const isEnglish = !!showEnglish[newsId];
        const hasTranslation = news.en_headline || news.en_content;

        const displayHeadline = isEnglish && news.en_headline ? news.en_headline : news.headline;
        const displayContent = isEnglish && news.en_content ? news.en_content! : news.content;

        // Read‑more logic
        const isLong = displayContent.length > PREVIEW_CHAR_LIMIT;
        const isExpanded = !!expanded[newsId];
        const contentToShow = isLong && !isExpanded
          ? displayContent.slice(0, PREVIEW_CHAR_LIMIT) + "…"
          : displayContent;

        return (
          <div
            key={newsId}
            className="bg-gray-900 border border-gray-800 rounded-lg shadow-lg overflow-hidden"
          >
            {/* Header (Game Icon + Info) */}
            <div className="flex items-center p-3 justify-between">
              <div className="flex items-center space-x-3">
                <div className="bg-purple-700 rounded-full h-8 w-8 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                  {news.identifier.charAt(0)}
                </div>
                <div className="flex flex-col leading-tight">
                  <span className="text-sm font-semibold text-gray-200">
                    {getGameTitle(news.identifier)}
                  </span>
                  <span className="text-xs text-gray-400">{formattedDate}</span>
                  {news.type && (
                    <span className="text-xs text-gray-500 italic bold">{news.type}</span>
                  )}
                </div>
              </div>
              {hasTranslation && (
                <button
                  onClick={() => toggleLanguage(newsId)}
                  className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 py-1 px-2 rounded"
                >
                  {isEnglish ? "View Original" : "View in English"}
                </button>
              )}
            </div>

            {/* Content Area */}
            <div className="px-3 pt-1 pb-3">
              {displayHeadline && (
                <p className="font-semibold text-white text-sm mb-2">{displayHeadline}</p>
              )}
              <p className="text-sm text-gray-200 whitespace-pre-line mb-2">
                {contentToShow.split(/(\[.*?\]\(.*?\)|https?:\/\/[^\s]+)/g).map((part, idx) => {
                  const m = part.match(/\[(.*?)\]\((.*?)\)/);
                  const u = part.match(/https?:\/\/[^\s]+/);
                  if (m) {
                    return (
                      <a
                        key={idx}
                        href={m[2]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 hover:underline"
                      >
                        {m[1]}
                      </a>
                    );
                  } else if (u) {
                    return (
                      <a
                        key={idx}
                        href={u[0]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 hover:underline"
                      >
                        {u[0]}
                      </a>
                    );
                  }
                  return part;
                })}
              </p>

              {isLong && (
                <button
                  onClick={() => toggleExpand(newsId)}
                  className="text-m text-blue-400 hover:underline"
                >
                  {isExpanded ? "Show less" : "Show more"}
                </button>
              )}
            </div>

            {/* Images */}
            <div className="w-full">
              {news.images.length > 0 && (
                <>
                  {/* Display only the current image */}
                  {(() => {
                    const currentIdx = currentImageIndex[newsId] || 0;
                    const img = news.images[currentIdx];

                    return (
                      <div className="relative">
                        {loadingImages[newsId] && (
                          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
                            <div className="loader border-t-2 border-b-2 border-white w-6 h-6 rounded-full animate-spin"></div>
                          </div>
                        )}
                        <img
                          src={img.image}
                          alt="news visual"
                          className={`w-full object-cover py-2 ${
                            loadingImages[newsId] ? "opacity-0" : "opacity-100"
                          }`}
                          onLoad={() => handleImageLoad(newsId)}
                        />
                      </div>
                    );
                  })()}

                  {/* Image selector buttons (only shown if there are multiple images) */}
                  {news.images.length > 1 && (
                    <div className="flex justify-center gap-2 pb-3">
                      {news.images.map((_, idx) => (
                        <button
                          key={idx}
                          onClick={() => changeImage(newsId, idx)}
                          className={`px-3 py-1 rounded ${
                            (currentImageIndex[newsId] || 0) === idx
                              ? "bg-blue-600 text-white"
                              : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                          }`}
                        >
                          {idx + 1}
                        </button>
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Footer */}
            {news.url && (
              <div className="px-3 py-2 bg-gray-800 text-center">
                <a
                  href={news.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 text-sm hover:text-white inline-flex items-center font-bold underline"
                >
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
