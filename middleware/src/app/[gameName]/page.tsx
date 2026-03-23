import { Metadata } from "next";
import kairosImage from "../kairos.png";
import { createClient } from "@libsql/client";
import Link from 'next/link';
interface NewsData {
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
export async function generateMetadata({
  params,
  searchParams,
}: {
  params: Promise<{ gameName?: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}): Promise<Metadata> {
  const resolvedParams = await params;
  const resolvedSearchParams = await searchParams;
  let gameName = resolvedParams.gameName || "news";
  const postId = resolvedSearchParams.post as string | undefined;
  const lang = resolvedSearchParams.lang as string | undefined;
  const apiUrlBase = process.env.NEXT_PUBLIC_API_URL;

  if (!postId) {
    return {
      title: `${gameName} News`,
      description: `Browse the latest updates for ${gameName}`,
    };
  }

  try {
    let fetchUrl = `${apiUrlBase}/${gameName}_news.json`;
    if (gameName === "news") {
      fetchUrl = `${apiUrlBase}/news.json`;
    }
    const res = await fetch(fetchUrl);
    if (!res.ok) throw new Error("Failed to fetch");
    const data = await res.json();
    const newsPosts = data.news_posts;
    const matchingPost = newsPosts.find((news: any) => {
      const contentHash =
        news.content.split("").reduce((hash: number, char: string) => {
          return (hash << 5) + hash + char.charCodeAt(0);
        }, 5381) >>> 0;
      const headlineHash =
        (news.headline || "null")
          .split("")
          .reduce(
            (hash: number, char: string) =>
              (hash << 5) + hash + char.charCodeAt(0),
            5381,
          ) >>> 0;
      const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${headlineHash.toString(16)}`;
      return newsId === postId;
    });
    if (!matchingPost) {
      try {
        const client = createClient({
          url: process.env.SQLITE_DB!,
          authToken: process.env.REMOTE_AUTH_TOKEN!,
        });
        const result = await client.execute({
          sql: `SELECT
            news_id, date, identifier, type, timestamp,
            headline, content, url, is_ai_summary,
            en_headline, en_content
          FROM news
          WHERE news_id = ?`,
          args: [postId],
        });

        if (result.rows.length === 0) {
          return { title: "Post not found" };
        }
        const row = result.rows[0];
        const imagesResult = await client.execute({
          sql: `SELECT image_url, link_url FROM news_images WHERE news_id = ?`,
          args: [postId],
        });

        const images = imagesResult.rows.map((img) => ({
          image: img.image_url,
          link: img.link_url,
      }));
        const dbPost = {
          news_id: row.news_id,
          date: row.date,
          identifier: row.identifier,
          type: row.type,
          timestamp: row.timestamp,
          headline: row.headline,
          content: row.content,
          url: row.url,
          is_ai_summary: Boolean(row.is_ai_summary),
          en_headline: row.en_headline,
          en_content: row.en_content,
          images,
        };
        if (lang === "en") {
          if (dbPost.en_headline !== null) {
            dbPost.headline = dbPost.en_headline;
          }
          if (dbPost.en_content !== null) {
            dbPost.content = dbPost.en_content;
          }
        }

        if (!dbPost.headline) {
          dbPost.headline = dbPost.content;
        }
        return {
          title: String(dbPost.headline || "Untitled"),
          description: String(dbPost.content || "").slice(0, 300),
          openGraph: {
            title: String(dbPost.headline || "Untitled"),
            description: String(dbPost.content || "").slice(0, 300),
            images: dbPost.images?.[0]?.image
              ? [String(dbPost.images[0].image)]
              : [],
          },
        };
      } catch (dbErr) {
        console.error("Database fallback error:", dbErr);
        return { title: "Post not found" };
      }
    }
    if (lang === "en") {
      if (matchingPost.en_headline !== null) {
        matchingPost.headline = matchingPost.en_headline;
      }
      if (matchingPost.en_content !== null) {
        matchingPost.content = matchingPost.en_content;
      }
    }
    if (!matchingPost.headline) {
      matchingPost.headline = matchingPost.content;
    }
    return {
      title: matchingPost.headline,
      description: matchingPost.content.slice(0, 300),
      openGraph: {
        title: matchingPost.headline,
        description: matchingPost.content.slice(0, 300),
        images: matchingPost.images?.[0]?.image
          ? [matchingPost.images[0].image]
          : [],
      },
    };
  } catch (err) {
    console.error(err);
    return {
      title: "Error loading post",
      description: "There was a problem loading this news post.",
    };
  }
}

export default async function GamePage({
  params,
  searchParams,
}: {
  params: Promise<{ gameName?: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const resolvedParams = await params;
  const resolvedSearchParams = await searchParams;
  const gameName = resolvedParams.gameName || "news";
  const postId = resolvedSearchParams.post as string | undefined;
  const lang = resolvedSearchParams.lang as string | undefined;
  const mainNewsUrl = process.env.NEXT_PUBLIC_MAIN_NEWS_URL;
  const apiUrlBase = process.env.NEXT_PUBLIC_API_URL;

  if (postId) {
    let newsPost: NewsData | null = null;

    try {
      let fetchUrl = `${apiUrlBase}/${gameName}_news.json`;
      if (gameName === "news") {
        fetchUrl = `${apiUrlBase}/news.json`;
      }
      const res = await fetch(fetchUrl);
      if (res.ok) {
        const data = await res.json();
        const newsPosts = data.news_posts;
        const matchingPost = newsPosts.find((news: any) => {
          const contentHash =
            news.content.split("").reduce((hash: number, char: string) => {
              return (hash << 5) + hash + char.charCodeAt(0);
            }, 5381) >>> 0;
          const headlineHash =
            (news.headline || "null")
              .split("")
              .reduce(
                (hash: number, char: string) =>
                  (hash << 5) + hash + char.charCodeAt(0),
                5381,
              ) >>> 0;
          const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${headlineHash.toString(16)}`;
          return newsId === postId;
        });

        if (matchingPost) {
          newsPost = matchingPost;
        }
      }

      // If not found in JSON, try database
      if (!newsPost) {
        const client = createClient({
          url: process.env.SQLITE_DB!,
          authToken: process.env.REMOTE_AUTH_TOKEN!,
        });

        const result = await client.execute({
          sql: `SELECT
            news_id, date, identifier, type, timestamp,
            headline, content, url, is_ai_summary,
            en_headline, en_content
          FROM news
          WHERE news_id = ?`,
          args: [postId],
        });

        if (result.rows.length > 0) {
          const row = result.rows[0];

          // Get images for this news post
          const imagesResult = await client.execute({
            sql: `SELECT image_url, link_url FROM news_images WHERE news_id = ?`,
            args: [postId],
          });

          const images = imagesResult.rows.map((img) => ({
            image: img.image_url,
            link: img.link_url,
          }));

          newsPost = {
            identifier: row.identifier as string,
            type: row.type as string | null,
            timestamp: row.timestamp as number,
            headline: row.headline as string | null,
            content: row.content as string,
            url: row.url as string | null,
            is_ai_summary: Boolean(row.is_ai_summary),
            en_headline: row.en_headline as string | null,
            en_content: row.en_content as string | null,
            images: images.map(img => ({
              image: String(img.image),
              link: img.link ? String(img.link) : null
            })),
          };
        }
      }
    } catch (err) {
      console.error("Error fetching news post:", err);
    }

    // If we found the post, render it
    if (newsPost) {
      return (
        <NewsPostPage
          newsPost={newsPost}
          lang={lang}
          gameName={gameName}
          postId={postId}
          mainNewsUrl={mainNewsUrl}
        />
      );
    }
  }

  // Default fallback page
  const redirectUrl =
    postId && mainNewsUrl
      ? gameName === "news"
        ? `${mainNewsUrl}/#${postId}`
        : `${mainNewsUrl}/game/${gameName}#${postId}`
      : mainNewsUrl;

  return (
    <main className="main">
      <div className="content-wrapper">
        <h1 className="title">573 UPDATES</h1>
        <img
          src={kairosImage.src}
          alt="Updates image"
          className="updates-image"
        />
        {postId && !redirectUrl && (
          <p style={{ color: "red", margin: "20px 0" }}>Post not found</p>
        )}
        {redirectUrl && (
          <>
            <br />
            <a href={redirectUrl} className="redirect-link">
              click here if not redirected
            </a>
          </>
        )}
      </div>
    </main>
  );
}

// Component to render a single news post
function NewsPostPage({
  newsPost,
  lang,
  gameName,
  postId,
  mainNewsUrl,
}: {
  newsPost: NewsData;
  lang?: string;
  gameName: string;
  postId: string;
  mainNewsUrl?: string;
}) {
  let displayHeadline = newsPost.headline;
  let displayContent = newsPost.content;

  if (lang === "en") {
    if (newsPost.en_headline !== null) {
      displayHeadline = newsPost.en_headline;
    }
    if (newsPost.en_content !== null) {
      displayContent = newsPost.en_content;
    }
  }

  if (!displayHeadline) {
    displayHeadline = displayContent;
  }

  const date = new Date(newsPost.timestamp * 1000).toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  const redirectUrl = mainNewsUrl
    ? gameName === "news"
      ? `${mainNewsUrl}/#${postId}`
      : `${mainNewsUrl}/game/${gameName}#${postId}`
    : null;

  const createToggleUrl = () => {
    const params = new URLSearchParams();
    params.set('post', postId);

    if (lang === 'en') {
    } else {
      params.set('lang', 'en');
    }

    const baseUrl = gameName === "news" ? "/news" : `/game/${gameName}`;
    const queryString = params.toString();
    return queryString ? `${baseUrl}?${queryString}` : baseUrl;
  };

  return (
    <main className="min-h-screen text-white font-sans bg-black">
      <div className="w-full max-w-xl mx-auto px-3 sm:px-4 py-5 box-border">
        <div className="w-full bg-slate-800 border border-slate-700 rounded-lg shadow-xl shadow-black/30 overflow-hidden box-border">
          {/* Post Header */}
          <div className="p-3 border-b border-slate-600">
            <div className="text-[13px] text-slate-400/80 mb-1.5">
              {date}
            </div>
            {newsPost.type && (
              <div className="inline-block text-[12px] italic text-slate-400 bg-slate-700 px-1.5 py-0.5 rounded">
                {newsPost.type}
              </div>
            )}
          </div>

          {/* Content */}
          <div className="p-3 min-h-[120px]">
            {displayHeadline && (
              <h2 className="font-bold text-base sm:text-lg mb-3 leading-snug text-slate-50 break-words">
                {displayHeadline}
              </h2>
            )}

            <div className="text-[13px] sm:text-sm whitespace-pre-line mb-3 leading-relaxed text-slate-200">
              {displayContent
                .split(/(\[.*?\]\(.*?\)|https?:\/\/[^\s]+)/g)
                .map((part, idx) => {
                  const linkMatch = part.match(/\[(.*?)\]\((.*?)\)/);
                  const urlMatch = part.match(/https?:\/\/[^\s]+/);

                  if (linkMatch) {
                    return (
                      <Link
                        key={idx}
                        href={linkMatch[2]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sky-400 underline decoration-blue-500 underline-offset-2 font-medium"
                      >
                        {linkMatch[1]}
                      </Link>
                    );
                  }

                  if (urlMatch) {
                    return (
                      <Link
                        key={idx}
                        href={urlMatch[0]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sky-400 underline decoration-blue-500 underline-offset-2 font-medium"
                      >
                        {urlMatch[0]}
                      </Link>
                    );
                  }

                  return (
                    <span key={idx}>
                      {part}
                    </span>
                  );
                })}
            </div>
          </div>

          {/* AI Disclaimer */}
          {newsPost.is_ai_summary && (
            <div className="bg-slate-600 px-4 py-2.5 text-[12px] text-center text-slate-300">
              This content was generated using AI and may contain inaccuracies
            </div>
          )}

          {/* Machine Translation Disclaimer */}
          {(newsPost.en_headline || newsPost.en_content) && lang === "en" && (
            <div className="bg-slate-600 px-4 py-2.5 text-[12px] text-center text-slate-300">
              This is a machine translation and may contain errors
            </div>
          )}

          {/* Images */}
          {newsPost.images && newsPost.images.length > 0 && (
            <div className="w-full overflow-hidden">
              <img
                src={newsPost.images[0].image}
                alt="News visual"
                className="w-full h-auto max-h-[400px] object-contain block"
              />
            </div>
          )}

          {/* Read More Link */}
          {newsPost.url && (
            <div className="bg-slate-600 px-4 py-3 text-center">
              <Link
                href={newsPost.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[15px] font-semibold text-sky-400 underline decoration-sky-400 underline-offset-2"
              >
                READ MORE
              </Link>
            </div>
          )}
        </div>

        {/* About 573 UPDATES */}
        <div className="mt-6 mb-4 p-3 text-center bg-slate-700 rounded-md border border-slate-600">
          <h3 className="text-[15px] font-semibold mb-1.5 text-slate-50">
            This is a perma-link hosted on 573 UPDATES
          </h3>
          <p className="text-[12px] text-slate-300 leading-tight">
            A news aggregator for some arcade (and some not-so arcade) games.
            Image data is loaded from external sources, and as such may not
            always be available.
          </p>
        </div>

        {/* Navigation Buttons */}
        <div className="mt-3 flex flex-col items-center gap-2.5 text-center">
          {/* Language Toggle Button */}
          {(newsPost.en_headline || newsPost.en_content) && (
            <Link
              href={createToggleUrl()}
              className="block w-full max-w-xs bg-linear-to-br from-purple-500 to-purple-700 text-white px-5 py-3.5 rounded-md text-sm font-semibold shadow-md shadow-purple-500/30 no-underline border-0 transition-all duration-200 text-center hover:brightness-110 active:translate-y-px"
            >
              {lang === "en" ? "日本語で読む" : "Read in English"}
            </Link>
          )}

          <Link
            href="/"
            className="block w-full max-w-xs bg-linear-to-br from-blue-500 to-blue-700 text-white px-5 py-3.5 rounded-md text-sm font-semibold shadow-md shadow-blue-500/30 no-underline border-0 transition-all duration-200 text-center hover:brightness-110 active:translate-y-px"
          >
            {lang === "en" ? "Back to 573 UPDATES" : "573 UPDATESに戻る"}
          </Link>
        </div>
      </div>
    </main>
  );
}
