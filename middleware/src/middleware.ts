import { NextRequest, NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
  const url = request.nextUrl
  const pathname = url.pathname
  if(pathname.startsWith("/_") || pathname.startsWith("/favicon")){
    return;
  }
  const searchParams = url.searchParams
  const gameName = pathname.split('/')[1] || 'news'
  const postId = searchParams.get('post')
  const apiUrlBase = process.env.NEXT_PUBLIC_API_URL
  if (postId) {
    try {
      console.log(`Game: ${gameName}, Post ID: ${postId}`)
      const newsDataUrl = apiUrlBase+"/"+gameName+"_news.json";
      const res = await fetch(newsDataUrl)
      if (res.ok) {
        const data = await res.json()
        const newsPosts = data["news_posts"];
        const matchingPost = newsPosts.find((news: any) => {
          const contentHash = news.content.split('').reduce((hash: number, char: string) => ((hash << 5) + hash) + char.charCodeAt(0), 5381) >>> 0;
          const newsId = `${news.identifier}-${news.timestamp}-${contentHash.toString(16)}-${news.headline}`;
          return newsId === postId;
        });
        const response = NextResponse.next()
        if(matchingPost.headline){
          response.headers.set('x-post-headline', encodeURIComponent(matchingPost.headline));
        }
        if(matchingPost.images && matchingPost.images.length >= 1 ){
          response.headers.set('x-post-heroImage', matchingPost.images[0].image);
        }
        response.headers.set('x-post-content', encodeURIComponent(matchingPost.content));
        response.headers.set('x-post-timestamp', matchingPost.timestamp);
        return response
      }
    } catch (e) {
      console.warn('Failed to fetch post metadata:', e)
    }
  }
  return NextResponse.next()
}
