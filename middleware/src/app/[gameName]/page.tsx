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

  return (
    <main
      style={{
        minHeight: "100vh",
        color: "white",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <div style={{
        width: '100%',
        maxWidth: '600px',
        margin: '0 auto',
        padding: '10px',
        paddingTop: '20px',
        paddingBottom: '20px',
        boxSizing: 'border-box'
      }}>
        <div style={{
          backgroundColor: '#1e293b',
          border: '1px solid #334155',
          borderRadius: '8px',
          boxShadow: '0 10px 20px -5px rgba(0, 0, 0, 0.3)',
          overflow: 'hidden',
          width: '100%',
          boxSizing: 'border-box'
        }}>
          {/* Post Header */}
          <div style={{
            padding: '12px',
            borderBottom: '1px solid #475569'
          }}>
            <div style={{
              fontSize: '13px',
              opacity: 0.8,
              marginBottom: '6px',
              color: '#94a3b8'
            }}>
              {date}
            </div>
            {newsPost.type && (
              <div style={{
                fontSize: '12px',
                fontStyle: 'italic',
                opacity: 0.8,
                color: '#64748b',
                backgroundColor: '#334155',
                padding: '3px 6px',
                borderRadius: '3px',
                display: 'inline-block'
              }}>
                {newsPost.type}
              </div>
            )}
          </div>

          {/* Content */}
          <div style={{
            padding: '12px',
            minHeight: '120px'
          }}>
            {displayHeadline && (
              <h2 style={{
                fontWeight: '700',
                fontSize: '16px',
                marginBottom: '12px',
                margin: '0 0 12px 0',
                lineHeight: '1.3',
                color: '#f1f5f9',
                wordWrap: 'break-word',
                overflowWrap: 'break-word'
              }}>
                {displayHeadline}
              </h2>
            )}
            <div style={{
              fontSize: '13px',
              whiteSpace: 'pre-line',
              marginBottom: '12px',
              margin: '0 0 12px 0',
              lineHeight: '1.5',
              color: '#e2e8f0'
            }}>
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
                        style={{
                          color: "#60a5fa",
                          textDecoration: "underline",
                          textDecorationColor: "#3b82f6",
                          fontWeight: "500",
                        }}
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
                        style={{
                          color: "#60a5fa",
                          textDecoration: "underline",
                          textDecorationColor: "#3b82f6",
                          fontWeight: "500",
                        }}
                      >
                        {urlMatch[0]}
                      </Link>
                    );
                  }
                  return part;
                })}
            </div>
          </div>

          {/* AI Disclaimer */}
          {newsPost.is_ai_summary && (
            <div
              style={{
                backgroundColor: "#475569",
                padding: "10px 16px",
                fontSize: "12px",
                textAlign: "center",
                color: "#cbd5e1",
              }}
            >
              This content was generated using AI and may contain inaccuracies
            </div>
          )}

          {/* Machine Translation Disclaimer */}
          {(newsPost.en_headline || newsPost.en_content) && lang === "en" && (
            <div
              style={{
                backgroundColor: "#475569",
                padding: "10px 16px",
                fontSize: "12px",
                textAlign: "center",
                color: "#cbd5e1",
              }}
            >
              This is a machine translation and may contain errors
            </div>
          )}

          {/* Images */}
          {newsPost.images && newsPost.images.length > 0 && (
            <div
              style={{
                width: "100%",
                overflow: "hidden",
              }}
            >
              <img
                src={newsPost.images[0].image}
                alt="News visual"
                style={{
                  width: "100%",
                  height: "auto",
                  maxHeight: "400px",
                  objectFit: "contain",
                  display: "block",
                }}
              />
            </div>
          )}

          {/* Read More Link */}
          {newsPost.url && (
            <div
              style={{
                backgroundColor: "#475569",
                padding: "12px 16px",
                textAlign: "center",
              }}
            >
              <Link
                href={newsPost.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  fontSize: "15px",
                  textDecoration: "underline",
                  textDecorationColor: "#60a5fa",
                  fontWeight: "600",
                  color: "#60a5fa",
                }}
              >
                READ MORE
              </Link>
            </div>
          )}
        </div>

        {/* About 573 UPDATES */}
        <div style={{
          textAlign: 'center',
          marginTop: '24px',
          marginBottom: '16px',
          padding: '12px',
          backgroundColor: '#334155',
          borderRadius: '6px',
          border: '1px solid #475569'
        }}>
          <h3 style={{
            fontSize: '15px',
            fontWeight: '600',
            margin: '0 0 6px 0',
            color: '#f1f5f9'
          }}>
            This is a perma-link hosted on 573 UPDATES
          </h3>
          <p style={{
            fontSize: '12px',
            color: '#cbd5e1',
            margin: 0,
            lineHeight: '1.4'
          }}>
            A news aggregator for some arcade (and some not-so arcade) games.
            Image data is loaded from external sources, and as such may not
            always be available.
          </p>
        </div>

        {/* Navigation Buttons */}
        <div style={{
          textAlign: 'center',
          marginTop: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          alignItems: 'center'
        }}>
          <Link
            href="/"
            style={{
              display: 'block',
              background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
              color: 'white',
              padding: '14px 20px',
              borderRadius: '6px',
              textDecoration: 'none',
              fontSize: '14px',
              fontWeight: '600',
              boxShadow: '0 4px 12px rgba(59, 130, 246, 0.3)',
              border: 'none',
              transition: 'all 0.2s ease',
              width: '100%',
              maxWidth: '280px',
              textAlign: 'center'
            }}
          >
            Back to 573 UPDATES
          </Link>
        </div>
      </div>
    </main>
  );
}
