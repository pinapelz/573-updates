import { Metadata } from "next";
import kairosImage from '../kairos.png';
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
  const apiUrlBase = process.env.NEXT_PUBLIC_API_URL;
  const mainNewsUrl = process.env.NEXT_PUBLIC_MAIN_NEWS_URL;

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
      const headlineHash = (news.headline || 'null').split('').reduce((hash: number, char: string) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
      const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${headlineHash.toString(16)}`;
      return newsId === postId;
    });
    if (!matchingPost) {
      return { title: "Post not found" };
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
  const mainNewsUrl = process.env.NEXT_PUBLIC_MAIN_NEWS_URL;
  const { headers } = await import("next/headers");
  const { userAgent } = await import("next/server");
  const headersList = await headers();
  const ua = userAgent({ headers: headersList });

  if (postId && mainNewsUrl && !ua.isBot) {
    const { redirect } = await import("next/navigation");
    if(gameName === "news"){
      redirect(`${mainNewsUrl}/#${postId}`);
    }
    redirect(`${mainNewsUrl}/game/${gameName}#${postId}`);
  }

  const redirectUrl =
    postId && mainNewsUrl ? (gameName === "news" ? `${mainNewsUrl}/#${postId}` : `${mainNewsUrl}/game/${gameName}#${postId}`) : mainNewsUrl;

  return (
    <main className="main">
      <div className="content-wrapper">
        <h1 className="title">573 UPDATES</h1>
        <img
          src={kairosImage.src}
          alt="Updates image"
          className="updates-image"
        />
        {redirectUrl && (
          <>
            <br/>
          <a href={redirectUrl} className="redirect-link">
            click here if not redirected
          </a>
          </>
        )}
      </div>
    </main>
  );
}
