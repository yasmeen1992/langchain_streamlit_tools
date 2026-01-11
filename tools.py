# tools.py
from langchain_community.tools import DuckDuckGoSearchRun, YouTubeSearchTool
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    WikipediaAPIWrapper,
    ArxivAPIWrapper,
    OpenWeatherMapAPIWrapper,
)
from langchain_core.tools import tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()




# -----------------------
#  Multi Web Search
# -----------------------
@tool
def multi_web_search(topic: str) -> str:
    """
    Search the web for a topic using DuckDuckGo, Wikipedia, and Arxiv.
    Input must be a clear search topic or question.
    """
    try:
        wrapper = DuckDuckGoSearchAPIWrapper(backend="lite")
        ddg_search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        wiki = WikipediaAPIWrapper()
        arxiv = ArxivAPIWrapper()

        results = []
        results.append("DuckDuckGo: " + ddg_search.run(topic))
        results.append("Wikipedia: " + wiki.run(topic))
        results.append("Arxiv: " + arxiv.run(topic))

        return "\n\n".join(results)
    except Exception as e:
        return f"Search error: {e}"


# -----------------------
#  Video Search
# -----------------------
@tool
def youtube_search(topic: str) -> str:
    """
    Search YouTube for videos about a specific topic.
    Input should be a video topic or keywords.
    """
    try:
        yt = YouTubeSearchTool()
        return yt.run(topic)
    except Exception as e:
        return f"YouTube error: {e}"


# -----------------------
#  Weather Tool
# -----------------------
@tool
def weather_search(city: str) -> str:
    """
    Get the current weather for a specific city.
    The input must be a city name, for example: Cairo, Mansoura, Paris.
    """
    try:
        WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        weather = OpenWeatherMapAPIWrapper(api_key=WEATHER_API_KEY)
        return weather.run(city)
    except Exception as e:
        return f"Weather error: {e}"


# -----------------------
#  News Tool
# -----------------------
@tool
def news_search(query: str) -> str:
    """Fetch latest news for a given topic."""
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "pageSize": 5,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    articles = data.get("articles", [])
    out = []
    for art in articles:
        title = art.get("title")
        url = art.get("url")
        out.append(f"{title} — {url}")
    return "\n".join(out) or "No news found."
