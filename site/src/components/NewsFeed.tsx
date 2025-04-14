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
}

interface NewsFeedProps {
  newsItems: NewsData[];
}

export const NewsFeed: React.FC<NewsFeedProps> = ({ newsItems }) => {
  return (
    <div className="max-w-[600px] w-full mx-auto py-8 space-y-4">
      {newsItems.map((news) => {
        const formattedDate = new Date(news.timestamp * 1000).toLocaleDateString("ja-JP", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
        });

        const gameId = news.identifier;

        return (
          <div
            key={news.identifier + "-" + news.timestamp + "-" + news.content}
            className="bg-gray-900 border border-gray-800 rounded-lg shadow-lg overflow-hidden"
          >
            {/* Header (Game Icon + Info) */}
            <div className="flex items-center p-3">
              <div className="flex items-center space-x-3">
                {/* Game Icon */}
                <div className="bg-purple-700 rounded-full h-8 w-8 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                  {gameId.substring(0, 1)}
                </div>

                <div className="flex flex-col leading-tight">
                  <span className="text-sm font-semibold text-gray-200">
                    {getGameTitle(news.identifier)}
                  </span>
                  <span className="text-xs text-gray-400">
                    {formattedDate}
                  </span>
                  {/* Display News Type */}
                  {news.type && (
                    <span className="text-xs text-gray-500 italic bold">
                      {news.type}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Content Area */}
            <div className="px-3 pt-1 pb-3">
              {/* Headline */}
              {news.headline && (
                <p className="font-semibold text-white text-sm mb-2">
                  {news.headline}
                </p>
              )}

              {/* Content */}
              <p className="text-sm text-gray-200 whitespace-pre-line mb-2">
                {news.content.split(/(\[.*?\]\(.*?\)|https?:\/\/[^\s]+)/g).map((part, index) => {
                  const match = part.match(/\[(.*?)\]\((.*?)\)/);
                  const urlMatch = part.match(/https?:\/\/[^\s]+/);
                  if (match) {
                    return (
                      <a key={index} href={match[2]} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                        {match[1]}
                      </a>
                    );
                  } else if (urlMatch) {
                    return (
                      <a key={index} href={urlMatch[0]} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">
                        {urlMatch[0]}
                      </a>
                    );
                  }
                  return part;
                })}
              </p>
            </div>

            {/* Post Image(s) */}
              <div className="w-full">
                {news.images.map((img, i) => (
                  img.link ? (
                    <a
                      key={i}
                      href={img.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block hover:opacity-75"
                    >
                      <img
                        src={img.image}
                        alt="news visual"
                        className="w-full object-cover py-2"
                      />
                    </a>
                  ) : (
                    <div key={i} className="block">
                      <img
                        src={img.image}
                        alt="news visual"
                        className="w-full object-cover py-2"
                      />
                    </div>
                  )
                ))}
              </div>

            {/* Footer with Read More Link */}
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
