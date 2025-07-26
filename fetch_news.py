import feedparser
import json
import os
from collections import defaultdict
from datetime import datetime

# RSS feed URL
url = "https://techcrunch.com/feed/"

# Output file
output_file = "techcrunch_categorized_news.json"

# Remove old file if exists
if os.path.exists(output_file):
    os.remove(output_file)

# Parse feed
feed = feedparser.parse(url)
categorized_news = defaultdict(list)

for entry in feed.entries:
    # Use tags if available, else put under 'Uncategorized'
    tags = [tag.term for tag in entry.get("tags", [])] or ["Uncategorized"]

    news_item = {
        "title": entry.title,
        "summary": entry.summary,
        "link": entry.link,
        "published": entry.published,
        "fetched_at": datetime.now().isoformat(),
        "tags": tags  # ✅ Add this line
    }

    for tag in tags:
        categorized_news[tag].append(news_item)



# Save categorized news to JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(categorized_news, f, indent=4, ensure_ascii=False)

print("✅ Categorized news saved to techcrunch_categorized_news.json")
