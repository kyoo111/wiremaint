import anthropic
from config.settings import ANTHROPIC_API_KEY, CATEGORIES, MAX_ITEMS


def analyze_and_categorize(items: list) -> dict:
    """Claude API를 사용해 수집된 항목을 분석하고 카테고리별로 분류합니다."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    items_text = "\n".join([
        f"- [{i+1}] {item['title']} ({item['source']})\n  {item['summary'][:200]}\n  URL: {item['link']}"
        for i, item in enumerate(items[:30])
    ])

    prompt = f"""다음 AI 관련 뉴스/논문 목록을 분석하여 카테고리별로 분류하고 요약해주세요.

카테고리: {', '.join(CATEGORIES)}

항목 목록:
{items_text}

각 항목에 대해 다음 형식으로 응답해주세요 (총 {MAX_ITEMS}개 선별):
카테고리|제목|2~3줄 요약|시사점(업계에 미치는 영향)|출처URL|글로벌or국내

응답은 위 형식의 줄바꿈으로 구분된 텍스트로만 작성해주세요."""

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    return parse_response(message.content[0].text, items)


def parse_response(text: str, original_items: list) -> dict:
    """Claude 응답을 파싱하여 카테고리별 딕셔너리로 변환합니다."""
    categorized = {cat: [] for cat in CATEGORIES}

    for line in text.strip().split("\n"):
        parts = line.split("|")
        if len(parts) >= 5:
            category = parts[0].strip()
            for cat in CATEGORIES:
                if cat in category or category in cat:
                    categorized[cat].append({
                        "title": parts[1].strip() if len(parts) > 1 else "",
                        "summary": parts[2].strip() if len(parts) > 2 else "",
                        "insight": parts[3].strip() if len(parts) > 3 else "",
                        "url": parts[4].strip() if len(parts) > 4 else "",
                        "region": parts[5].strip() if len(parts) > 5 else "글로벌",
                    })
                    break

    return categorized
