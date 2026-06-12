import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import fetch_rss_feeds, fetch_arxiv
from analyzer import analyze_and_categorize
from generator import generate_html_report
from config.settings import RSS_FEEDS


def main():
    print("AI 일일 리포트 생성 시작...")

    print("1/3 뉴스 수집 중...")
    rss_items = fetch_rss_feeds(RSS_FEEDS)
    arxiv_items = fetch_arxiv()
    all_items = rss_items + arxiv_items
    print(f"   수집 완료: {len(all_items)}개 항목")

    print("2/3 AI 분석 및 카테고리 분류 중...")
    categorized = analyze_and_categorize(all_items)

    print("3/3 HTML 리포트 생성 중...")
    output_path = generate_html_report(categorized)

    print(f"\n완료! 리포트: {output_path}")


if __name__ == "__main__":
    main()
