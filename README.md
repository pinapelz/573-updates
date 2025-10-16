# 573 UPDATES
A scraper and aggregator of information/news for various arcade games. Despite the name, there are plans to add more than just Konami games. There are multiple components to this app.

By default we only provide "recent" news, this usually means its the first page of news for whatever the site is willing to provide

Frontend: https://arcade.moekyun.me/

API: `https://arcade-news.pinapelz.com/<game_id>.json`

Setting `game_id` to `news` provides an aggregate feed of all news from games that are within a 14 day range of scraping

Currently Supported:
- beatmania IIDX (`iidx_news`)
- SOUND VOLTEX (`sdvx_news`)
- DanceDanceRevolution (`ddr_news`)
- pop'n music (`popn_music_news`)
- jubeat (`jubeat_news`)
- GITADORA (`gitadora_news`)
- NOSTALGIA (`nostalgia_news`)
- DanceRush (`dance_rush_news`)
- DANCE aROUND (`dance_around_news`)
- CHUNITHM (JPN) (`chunithm_jpn_news`)
- CHUNITHM (INTL) (`chunithm_intl_news`)
- maimai DX (JPN) (`maimaidx_jp_news`)
- maimai DX (INTL) (`maimaidx_intl_news`)
- O.N.G.E.K.I (JPN) (`ongeki_jp_news`)
- MUSIC DIVER (`music_diver_news`)
- STREET FIGHTER TYPE ARCADE (`street_fighter_news`)
- Taiko no Tatsujin (`taiko_news`) -> Only official blog title and headings

![image](https://files.catbox.moe/vg03om.png)

# News Scraper
The news scraper is in the root directory of the repo. Running `python generate.py` will generate the news for all known games (exclude or include games by editing the files). Most games can be scrapped without further configuration, however some features require secrets to be configured (`.env` file, use the `.env.template` included)
- Translation -> requires Google Cloud API key with Translation feature enabled
- AI Summarization (for sites who may only provide promo images) -> requires OpenAI API Key

```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
python generate.py
```

This will generate JSONs for each scraped news site in the `news` directory

> [!IMPORTANT]
> The scraper codebase will always attempt to keep legacy code for compatability reasons. Please check `DEPREACATIONS.md` to see if there is a better way of getting some source of information.
>
> If there is no note for your game, it means that all modules only have up-to-date functionality

# Site
The frontend acts as a news site that serves the scraped information. You'll need to configure the `.env` file using the template for it to work properly.
```
VITE_NEWS_BASE_URL - The URL where news is served. The expected format is that the news json must be accessible at YOUR_BASE_URL/{game_id}_news.json (the same filename as generate script output)
VITE_MIDDLEWARE_BASE_URL - {OPTIONAL} but required if you want OpenGraph tags for linking to posts (should be domain of middleware)
VITE_PFP_BASE_URL - {OPTIONAL} but required if you want to set game specific (Expected image should be at PFP_URL/game_id.webp)
```

```
pnpm install
pnpm run dev
```

# Middleware
The middleware dynamically generated OpenGraph and other metadata tags for posts. This is optional. Only deploy if you need this functionality (aka Discord previews)

# Notifications
**Requires Middleware to be running**

Foreground and Background + PWA notifications are available using Firebase Cloud Messaging. Replace the credentials in `site/public/firebase-messaging-sw.js` as well as the necessary Firebase environment variables as shown in `site/.env.template`

Subscription to individual games are tracked in Redis/Vercel KV as an edge funtion. This is necessary to both track which devices are subscribed to what topic. There is also no existing way in FCM to send a notification to every device without having the tokens stored somewhere.

Notifications are only sent out each run of `generate.py` for uniquely hashed news entries.
