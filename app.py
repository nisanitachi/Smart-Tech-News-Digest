import os
import json
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"  
)


with open("techcrunch_genre_filtered.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)


genres = list(news_data.keys())


st.title("📰 Smart Tech News Digest (Groq LLM)")
st.sidebar.header("📂 Choose a Tech Genre")

selected_genre = st.sidebar.selectbox("Genre", sorted(genres))


articles = news_data.get(selected_genre, [])

st.markdown(f"## 📚 {selected_genre} — {len(articles)} Articles")

if not articles:
    st.warning("No articles found in this category.")
else:
    with st.expander("🔎 Preview Top Articles"):
        for article in articles[:5]:
            st.markdown(f"""
**{article['title']}**  
{article['summary']}  
[🔗 Read More]({article['link']})  
*Published: {article['published']}*
""")
            st.markdown("---")

   
    if st.button("🧠 Generate Summary with AI"):
        # Prepare content
        content = "\n".join([
            f"- {item['title']}: {item['summary']}"
            for item in articles[:5]
        ])

        prompt = f"""
You're a professional tech journalist.

Summarize the following **{selected_genre}** news articles into 2–3 bullet points or short paragraphs that are:
- Crisp
- Informative
- Easy to skim

Here are the articles:

{content}
""".strip()

        with st.spinner("Summarizing with Groq LLM..."):
            try:
                response = llm.invoke(prompt)
                st.success(" Summary Ready:")
                st.markdown(response.content.strip())
            except Exception as e:
                st.error(f" Groq API Error: {e}")
