import feedparser
import requests
from datetime import datetime, timedelta


def fetch_rss_feeds(feed_urls: list) -> list:
    """RSS 피드에서 최신 AI 뉴스를 수집합니다."""
    items = []
    since = datetime.now() - timedelta(days=1)

    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                items.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", url),
                    "published": entry.get("published", ""),
                })
        except Exception as e:
            print(f"피드 수집 오류 ({url}): {e}")

    return items


def fetch_arxiv(query: str = "artificial intelligence LLM", max_results: int = 5) -> list:
    """arXiv에서 최신 AI 논문을 수집합니다."""
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    try:
        feed = feedparser.parse(url)
        return [
            {
                "title": e.title,
                "summary": e.summary[:300] + "...",
                "link": e.link,
                "source": "arXiv",
                "published": e.get("published", ""),
            }
            for e in feed.entries
        ]
    except Exception as e:
        print(f"arXiv 수집 오류: {e}")
        return []
