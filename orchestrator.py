"""
Agent Team Orchestrator
Run the complete AI Daily Report agent team workflow
"""

import json
import os
from datetime import datetime
from agents import (
    load_agent_config,
    setup_agent_team,
    run_agent_team,
)


def main():
    """Main orchestrator function."""
    print("\n" + "=" * 70)
    print(" " * 15 + "🤖 AI Daily Report - Agent Team Orchestrator")
    print("=" * 70 + "\n")

    # Check if agent team is already configured
    if os.path.exists(".agent_team_config.json"):
        print("📋 Found existing agent team configuration\n")
        with open(".agent_team_config.json", "r", encoding="utf-8") as f:
            agent_config = json.load(f)
        print(f"   Environment: {agent_config['environment_id']}")
        print(f"   Coordinator: {agent_config['coordinator']['id']}\n")
    else:
        print("🚀 Setting up new agent team...\n")
        agent_config = setup_agent_team()

    # Define the main task
    task = f"""
당신은 AI 일일 리포트 생성의 조율자입니다.
오늘 날짜: {datetime.now().strftime('%Y-%m-%d')}

다음 순서로 작업을 진행해주세요:

1️⃣ **브리핑 생성** (BriefingGenerator)
   - 최신 AI 동향 수집 (글로벌 3회 + 국내 3회)
   - HTML 브리핑 생성
   - 파일: reports/{datetime.now().strftime('%Y-%m-%d')}_ai_report.html

2️⃣ **품질 검증** (BriefingValidator)
   - 30일 초과 자료 제거
   - 수치 오류 검증
   - 국내 항목 30% 이상 확인
   - 카테고리 균형 확인
   - 중복 기사 제거

3️⃣ **이슈 처리** (IssueProcessor)
   - 검증 중 발견된 문제를 GitHub 이슈로 등록
   - 열린 이슈 확인 및 처리
   - 각 이슈마다:
     * 처리 계획 댓글 작성
     * 문제 수정
     * 커밋 및 푸시 (closes #N)

4️⃣ **문서 최적화** (DocumentOptimizer)
   - SOUL.md, README.md, CLAUDE.md 검토
   - 역할 분리: 왜/목표 | 무엇/어떻게 | 규칙
   - 중복 제거 및 링크 참조로 통일
   - 낡은 내용 정리

각 단계가 완료되면 다음 단계로 진행하고, 최종 결과를 보고해주세요.
"""

    print("\n" + "=" * 70)
    print("📋 Task Execution Plan")
    print("=" * 70)
    print(task)
    print("=" * 70 + "\n")

    # Run the agent team
    print("🚀 Starting Agent Team Execution...\n")
    result = run_agent_team(task, agent_config)

    # Save result
    result_file = f"logs/agent_team_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs("logs", exist_ok=True)
    with open(result_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"Agent Team Execution Result - {datetime.now().isoformat()}\n")
        f.write("=" * 70 + "\n\n")
        f.write(result)

    print("\n" + "=" * 70)
    print("✨ Agent Team Execution Complete")
    print("=" * 70)
    print(f"\n📁 Result saved to: {result_file}\n")


if __name__ == "__main__":
    main()
