import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config.settings import REPORT_OUTPUT_DIR


def generate_html_report(categorized: dict, date: str = None) -> str:
    """카테고리별 데이터를 HTML 리포트로 생성하고 파일로 저장합니다."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    total_items = sum(len(v) for v in categorized.values())

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    html = template.render(
        date=date,
        total_items=total_items,
        categorized=categorized,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(REPORT_OUTPUT_DIR, f"{date}_ai_report.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"리포트 저장 완료: {output_path}")
    return output_path
