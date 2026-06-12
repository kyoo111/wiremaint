import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "reports")
MAX_ITEMS = int(os.getenv("MAX_ITEMS", 15))

CATEGORIES = [
    "LLM 모델 출시/업데이트",
    "기업 AI 전략",
    "규제/정책",
    "AI 기술 트렌드",
    "AI 스타트업/펀딩",
    "빅테크 AI 동향",
]

RSS_FEEDS = [
    # Global
    "https://techcrunch.com/feed/",
    "https://venturebeat.com/feed/",
    "https://www.technologyreview.com/feed/",
    # Domestic
    "https://www.zdnet.co.kr/rss/all.xml",
    "https://www.itworld.co.kr/rss/feed/index.php",
    "https://www.ciokorea.com/rss/feed/index.php",
    "https://www.bloter.net/rss/all.xml",
]
