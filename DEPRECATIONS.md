# IIDX
`bemani/iidx.py` is only tested to work with Pinky Crush, should not be used as scraping the eamusement news app feed provides better information, as well as images (see `konami/eamuse_app.py`)

# e-amusement App Feed
`parse_news_page()` in `konami/eamuse_app.py` requires rendering Javascript to get the information.
- Instead use `parse_news_api_route()` instead. Which is much faster (doesn't require JS and is already in JSON format)

# SDVX
Scraping the actual site itself is preferred here as the e-amusement app feed for SDVX is not really updated
