import json
import openai
import os

# Load the categorized news file
source_file = "techcrunch_categorized_news.json"
if not os.path.exists(source_file):
    print(f"❌ Source file '{source_file}' not found.")
    exit()

with open(source_file, "r", encoding="utf-8") as f:
    news_data = json.load(f)

if not news_data:
    print("⚠️ Source JSON is empty!")
    exit()

# Configure OpenAI API (Replace with your key)
openai.api_key = "your-key-here"  # Replace safely

def generate_summary(category, articles):
    if not articles:
        print(f"⚠️ No articles found in category: {category}")
        return "No articles available."

    combined_content = "\n".join(
        [f"- {item.get('title', '')}: {item.get('summary', '')}" for item in articles[:5]]
    )

    prompt = f"""You are a professional tech news summarizer.
Summarize the following articles under the category: {category}.
Keep the tone crisp, informative, and engaging.
Use bullet points or 2–3 short paragraphs.\n\n{combined_content}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"].strip()

    except openai.error.OpenAIError as e:
        print(f"❌ OpenAI API Error for {category}: {e}")
        return f"Error: {str(e)}"

    except Exception as e:
        print(f"⚠️ General Error for {category}: {e}")
        return f"Error: {str(e)}"
