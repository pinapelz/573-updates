import os
import json
import requests
import mimetypes
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
from constants import RSS_FEED_URL


def build_rss_from_news_feed(title: str, description: str, json_file_path: str, output_path: str, limit: int = 12):
    """
    Build RSS from an existing JSON file containing news_posts.
    Reads the JSON, extracts posts, and generates a valid RSS XML.
    """
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found: {json_file_path}")

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    news_feeds = data.get("news_posts", [])[:limit]

    file_name = os.path.basename(output_path)
    url_to_feed = f"{RSS_FEED_URL}/{file_name}"

    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:atom": "http://www.w3.org/2005/Atom"
    })
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "link").text = url_to_feed
    ET.SubElement(channel, "{http://www.w3.org/2005/Atom}link", {
        "href": url_to_feed,
        "rel": "self",
        "type": "application/rss+xml"
    })

    for post in news_feeds:
        item = ET.SubElement(channel, "item")

        # Title
        post_title = post.get("headline") or post.get("en_headline") or post.get("content", "")[:50]
        ET.SubElement(item, "title").text = post_title

        # Link
        ET.SubElement(item, "link").text = post.get("url") or "https://arcade.moekyun.me"

        # Description (JP + EN combined)
        jp_content = post.get("content", "")
        en_headline = post.get("en_headline")
        en_content = post.get("en_content")

        desc_parts = []
        if jp_content:
            desc_parts.append(jp_content.strip().replace("\n", "<br/>"))
        if en_headline or en_content:
            desc_parts.append("<hr/><b>English Translation</b><br/>")
            if en_headline:
                desc_parts.append(f"<i>{en_headline.strip()}</i><br/>")
            if en_content:
                desc_parts.append(en_content.strip().replace("\n", "<br/>"))

        desc_combined = "\n".join(desc_parts)

        # Placeholder for CDATA
        desc_el = ET.SubElement(item, "description")
        desc_el.text = f"__CDATA_PLACEHOLDER__{desc_combined}__END__"

        # pubDate
        if "timestamp" in post and post["timestamp"]:
            pub_date = datetime.fromtimestamp(
                post["timestamp"], timezone.utc
            ).strftime("%a, %d %b %Y %H:%M:%S +0000")
            ET.SubElement(item, "pubDate").text = pub_date

        # First image enclosure (if any)
        images = post.get("images", [])
        if images:
            image_url = images[0].get("image")
            if image_url:
                mime = mimetypes.guess_type(image_url)[0] or "application/octet-stream"
                length = "0"
                try:
                    r = requests.head(image_url, timeout=5, allow_redirects=True)
                    if "Content-Length" in r.headers:
                        length = r.headers["Content-Length"]
                except Exception:
                    pass
                ET.SubElement(item, "enclosure", url=image_url, type=mime, length=length)

    # Serialize XML
    rough_xml = ET.tostring(rss, encoding="utf-8", xml_declaration=True)

    # Replace placeholders with real CDATA
    final_xml = rough_xml.decode("utf-8").replace(
        "__CDATA_PLACEHOLDER__", "<![CDATA[").replace("__END__", "]]>"
    )

    # Pretty print
    dom = minidom.parseString(final_xml)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dom.toprettyxml(indent="  "))
