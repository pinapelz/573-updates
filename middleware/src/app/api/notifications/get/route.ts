import { Redis } from "@upstash/redis";

export const runtime = "edge";

const redis = new Redis({
  url: process.env.KV_REST_API_URL!,
  token: process.env.KV_REST_API_TOKEN!,
});

// /api/notification/get?topic=<topic>
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topic = searchParams.get("topic");

  if (!topic) {
    return new Response(JSON.stringify({ error: "Missing topic" }), { status: 400 });
  }

  const key = `fcm-${topic}`;
  const tokens = await redis.smembers<string[]>(key);

  return new Response(JSON.stringify({ topic, tokens }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
