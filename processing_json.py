import json
from collections import defaultdict


with open("techcrunch_categorized_news.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Whitelist of genre tags
genre_tags_whitelist = {
    "AI", "Artificial Intelligence", "Machine Learning", "Robotics",
    "Startups", "Venture Capital", "Apps", "Transportation",
    "Space", "Hardware", "Security", "Social", "Finance",
    "Crypto", "SaaS", "Mobile", "Enterprise", "Energy"
}


all_articles = []
for articles in data.values():
    all_articles.extend(articles)


filtered_by_genre = defaultdict(list)

for article in all_articles:
    article_tags = article.get("tags", [])

   
    genre_tags = [tag for tag in article_tags if tag in genre_tags_whitelist]

    if genre_tags:
        article["tags"] = genre_tags 
        for tag in genre_tags:
            filtered_by_genre[tag].append(article)

# Save filtered JSON
with open("techcrunch_genre_filtered.json", "w", encoding="utf-8") as f:
    json.dump(filtered_by_genre, f, indent=4, ensure_ascii=False)


