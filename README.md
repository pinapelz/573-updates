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

![image](https://github.com/user-attachments/assets/3fe4691f-610c-487c-84ef-8edfb045c000)

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

# Middlware
The middleware dynamically generated OpenGraph and other metadata tags for posts. This is optional. Only deploy if you need this functionality (aka Discord previews)
