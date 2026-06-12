"""
Agent Team Orchestrator with Harness Hooks
Run the complete AI Daily Report agent team workflow
"""

import json
import os
import time
import logging
from datetime import datetime
from agents import (
    load_agent_config,
    setup_agent_team,
    run_agent_team,
)
from hooks import (
    HarnessHooks,
    DefaultHooks,
    StateTrackingHook,
    MetricsHook,
    AlertHook,
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/orchestrator.log'),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main orchestrator function with Harness Hooks."""

    # 디렉토리 생성
    os.makedirs("logs", exist_ok=True)

    # Hook 시스템 초기화
    hooks = HarnessHooks()
    state_hook = StateTrackingHook()
    metrics_hook = MetricsHook()
    alert_hook = AlertHook()

    # 기본 Hook 등록
    hooks.register('on_start', DefaultHooks.on_start)
    hooks.register('before_phase', DefaultHooks.before_phase)
    hooks.register('after_phase', DefaultHooks.after_phase)
    hooks.register('on_phase_error', DefaultHooks.on_phase_error)
    hooks.register('on_retry', DefaultHooks.on_retry)
    hooks.register('on_fallback', DefaultHooks.on_fallback)
    hooks.register('on_complete', DefaultHooks.on_complete)

    # 상태 추적 Hook 등록
    hooks.register('on_start', state_hook.on_start)
    hooks.register('before_phase', state_hook.before_phase)
    hooks.register('after_phase', state_hook.after_phase)
    hooks.register('on_phase_error', state_hook.on_phase_error)
    hooks.register('on_complete', state_hook.on_complete)

    # 메트릭 수집 Hook 등록
    hooks.register('before_phase', metrics_hook.before_phase)
    hooks.register('after_phase', metrics_hook.after_phase)
    hooks.register('on_phase_error', metrics_hook.on_phase_error)
    hooks.register('on_complete', metrics_hook.on_complete)

    # 알림 Hook 등록
    hooks.register('on_phase_error', alert_hook.on_phase_error)
    hooks.register('on_fallback', alert_hook.on_fallback)

    try:
        # Hook: 시작
        hooks.trigger('on_start')

        # 에이전트 팀 설정 확인
        if os.path.exists(".agent_team_config.json"):
            logger.info("Found existing agent team configuration")
            with open(".agent_team_config.json", "r", encoding="utf-8") as f:
                agent_config = json.load(f)
        else:
            logger.info("Setting up new agent team...")
            agent_config = setup_agent_team()

        # 메인 작업 정의
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

        # Phases 정의
        phases = [
            ('briefing_generation', 'BriefingGenerator'),
            ('briefing_validation', 'BriefingValidator'),
            ('issue_processing', 'IssueProcessor'),
            ('document_optimization', 'DocumentOptimizer'),
        ]

        results = {}
        failed_phases = []

        # Phase 루프
        for phase_name, phase_label in phases:
            try:
                # Hook: Phase 시작 전
                hooks.trigger('before_phase', phase_label)

                # Phase 실행
                logger.info(f"Executing phase: {phase_name}")
                result = run_agent_team(task, agent_config)
                results[phase_name] = result

                # Hook: Phase 완료
                hooks.trigger('after_phase', phase_label, result)

            except Exception as e:
                logger.error(f"Phase '{phase_name}' failed: {e}")

                # Hook: Phase 에러
                hooks.trigger('on_phase_error', phase_label, e, attempt=1)
                failed_phases.append((phase_name, e))

                # 재시도 로직 (최대 3회)
                for attempt in range(2, 4):
                    try:
                        delay = 2 ** attempt  # 지수 백오프: 4s, 8s

                        # Hook: 재시도
                        hooks.trigger('on_retry', phase_label, attempt, delay)

                        time.sleep(delay)
                        result = run_agent_team(task, agent_config)
                        results[phase_name] = result
                        failed_phases.remove((phase_name, e))

                        # Hook: 재시도 성공
                        hooks.trigger('after_phase', phase_label, result)
                        logger.info(f"Phase '{phase_name}' succeeded on attempt {attempt}")
                        break

                    except Exception as retry_error:
                        logger.error(f"Phase '{phase_name}' retry {attempt} failed: {retry_error}")
                        if attempt == 3:
                            failed_phases.append((phase_name, retry_error))

        # 최종 상태 확인
        success = len(failed_phases) == 0

        # 최종 결과 저장
        result_file = f"logs/agent_team_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(result_file, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(f"Agent Team Execution Result - {datetime.now().isoformat()}\n")
            f.write("=" * 70 + "\n\n")

            for phase_name, result in results.items():
                f.write(f"\n{phase_name.upper()}\n")
                f.write("-" * 70 + "\n")
                f.write(result + "\n")

            if failed_phases:
                f.write(f"\n\nFAILED PHASES: {len(failed_phases)}\n")
                for phase_name, error in failed_phases:
                    f.write(f"  - {phase_name}: {error}\n")

        logger.info(f"Result saved to: {result_file}")

        # Hook: 완료
        summary = {
            'total_phases': len(phases),
            'successful_phases': len(phases) - len(failed_phases),
            'failed_phases': len(failed_phases),
            'result_file': result_file,
        }
        hooks.trigger('on_complete', success, summary)

        # Hook 로그 저장
        hooks.save_log()

    except Exception as e:
        logger.critical(f"Critical error in orchestrator: {e}")
        hooks.trigger('on_complete', False, {'error': str(e)})
        raise


if __name__ == "__main__":
    main()
