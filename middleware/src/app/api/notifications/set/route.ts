import { Redis } from "@upstash/redis";

export const runtime = "edge";
const redis = new Redis({
  url: process.env.KV_REST_API_URL!,
  token: process.env.KV_REST_API_TOKEN!,
});

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};
export async function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: corsHeaders,
  });
}

// /api/notification/set?topic=<topic>&token=<fcm_token>&action=subscribe|unsubscribe
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topic = searchParams.get("topic");
  const token = searchParams.get("token");
  const action = searchParams.get("action"); // "subscribe" | "unsubscribe"

  if (!topic || !token || !action) {
    return new Response(JSON.stringify({ error: "Missing params" }), {
      status: 400,
      headers: corsHeaders,
    });
  }

  const key = `fcm-${topic}`;

  if (action === "subscribe") {
    await redis.sadd(key, token);
  } else if (action === "unsubscribe") {
    await redis.srem(key, token);
  } else {
    return new Response(JSON.stringify({ error: "Invalid action" }), {
      status: 400,
      headers: corsHeaders,
    });
  }

  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: corsHeaders,
  });
}
