"""
Harness Hooks Framework
Phase 전후 및 에러 처리 시점에 자동 실행되는 콜백 시스템
"""

import json
import logging
from datetime import datetime
from typing import Callable, Any, Dict, List

logger = logging.getLogger(__name__)


class HarnessHooks:
    """하네스 이벤트 후킹 시스템"""

    # 지원하는 이벤트
    EVENTS = [
        'on_start',           # 전체 시작
        'before_phase',       # Phase 시작 전
        'after_phase',        # Phase 완료 후
        'on_phase_error',     # Phase 에러 발생
        'on_retry',           # 재시도 시작
        'on_fallback',        # Fallback 실행
        'on_complete',        # 전체 완료
    ]

    def __init__(self):
        self.hooks: Dict[str, List[Callable]] = {event: [] for event in self.EVENTS}
        self.execution_log = []

    def register(self, event: str, callback: Callable) -> None:
        """
        Hook 콜백 등록

        Args:
            event: 이벤트 이름 (EVENTS 중 하나)
            callback: 실행할 함수
        """
        if event not in self.EVENTS:
            logger.warning(f"Unknown event: {event}")
            return

        self.hooks[event].append(callback)
        logger.debug(f"Registered hook: {event} -> {callback.__name__}")

    def trigger(self, event: str, *args, **kwargs) -> None:
        """
        Hook 실행

        Args:
            event: 이벤트 이름
            *args, **kwargs: 콜백에 전달할 인자
        """
        if event not in self.EVENTS:
            logger.warning(f"Unknown event: {event}")
            return

        logger.info(f"[Hook] Triggering '{event}'")

        for callback in self.hooks[event]:
            try:
                callback(*args, **kwargs)
                logger.debug(f"  ✓ {callback.__name__}")
            except Exception as e:
                logger.error(f"  ✗ {callback.__name__}: {e}")

        # 실행 로그 기록
        self.execution_log.append({
            'event': event,
            'timestamp': datetime.now().isoformat(),
            'callback_count': len(self.hooks[event]),
        })

    def save_log(self, filename: str = "logs/hooks_execution.json") -> None:
        """Hook 실행 로그 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.execution_log, f, indent=2, ensure_ascii=False)
        logger.info(f"Hook execution log saved: {filename}")


# 기본 Hook 콜백 함수들
class DefaultHooks:
    """기본 후킹 콜백 모음"""

    @staticmethod
    def on_start():
        """전체 시작"""
        print("\n" + "=" * 70)
        print(" " * 10 + "🚀 AI Daily Report - Harness Started")
        print("=" * 70 + "\n")
        logger.info("[Harness] Starting orchestration")

    @staticmethod
    def before_phase(phase_name: str):
        """Phase 시작 전"""
        print(f"\n📍 Phase: {phase_name}")
        print("-" * 70)
        logger.info(f"[Phase] Starting: {phase_name}")

    @staticmethod
    def after_phase(phase_name: str, result: Any):
        """Phase 완료 후"""
        print(f"✅ Phase '{phase_name}' completed")
        logger.info(f"[Phase] Completed: {phase_name}")

    @staticmethod
    def on_phase_error(phase_name: str, error: Exception, attempt: int = 1):
        """Phase 에러 발생"""
        print(f"\n❌ Phase '{phase_name}' failed (Attempt {attempt})")
        print(f"   Error: {str(error)}")
        logger.error(f"[Phase] Error in {phase_name}: {error}")

    @staticmethod
    def on_retry(phase_name: str, attempt: int, delay: int):
        """재시도 시작"""
        print(f"\n🔄 Retrying '{phase_name}' in {delay}s (Attempt {attempt})")
        logger.info(f"[Retry] {phase_name} - Attempt {attempt}, Wait {delay}s")

    @staticmethod
    def on_fallback(phase_name: str, fallback_method: str):
        """Fallback 실행"""
        print(f"\n⚡ Fallback: Using {fallback_method} for '{phase_name}'")
        logger.warning(f"[Fallback] {phase_name} -> {fallback_method}")

    @staticmethod
    def on_complete(success: bool, summary: Dict = None):
        """전체 완료"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print("\n" + "=" * 70)
        print(f" " * 15 + f"{status}")
        print("=" * 70)

        if summary:
            print("\n📊 Summary:")
            for key, value in summary.items():
                print(f"  • {key}: {value}")

        print()

        if success:
            logger.info("[Harness] Orchestration completed successfully")
        else:
            logger.error("[Harness] Orchestration failed")


class StateTrackingHook:
    """상태 추적 Hook"""

    def __init__(self, state_file: str = ".harness_state.json"):
        self.state_file = state_file
        self.state = {
            'phases': {},
            'start_time': None,
            'end_time': None,
            'status': 'running',
        }

    def on_start(self):
        """시작 시 상태 초기화"""
        self.state['start_time'] = datetime.now().isoformat()
        self.state['status'] = 'running'
        self._save()

    def before_phase(self, phase_name: str):
        """Phase 시작 시 상태 기록"""
        self.state['phases'][phase_name] = {
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'error': None,
        }
        self._save()

    def after_phase(self, phase_name: str, result: Any):
        """Phase 완료 시 상태 업데이트"""
        self.state['phases'][phase_name]['status'] = 'completed'
        self.state['phases'][phase_name]['end_time'] = datetime.now().isoformat()
        self._save()

    def on_phase_error(self, phase_name: str, error: Exception, attempt: int = 1):
        """에러 발생 시 상태 기록"""
        if phase_name not in self.state['phases']:
            self.state['phases'][phase_name] = {
                'status': 'error',
                'error': str(error),
                'attempt': attempt,
            }
        else:
            self.state['phases'][phase_name]['error'] = str(error)
            self.state['phases'][phase_name]['attempt'] = attempt
        self._save()

    def on_complete(self, success: bool, summary: Dict = None):
        """완료 시 최종 상태 저장"""
        self.state['end_time'] = datetime.now().isoformat()
        self.state['status'] = 'success' if success else 'failed'
        if summary:
            self.state['summary'] = summary
        self._save()

    def _save(self):
        """상태 파일로 저장"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)


class MetricsHook:
    """성능 메트릭 수집 Hook"""

    def __init__(self):
        self.metrics = {}
        self.phase_start_time = {}

    def before_phase(self, phase_name: str):
        """Phase 시작 시간 기록"""
        import time
        self.phase_start_time[phase_name] = time.time()

    def after_phase(self, phase_name: str, result: Any):
        """Phase 실행 시간 계산"""
        import time
        if phase_name in self.phase_start_time:
            duration = time.time() - self.phase_start_time[phase_name]
            self.metrics[phase_name] = {
                'status': 'success',
                'duration_seconds': round(duration, 2),
            }

    def on_phase_error(self, phase_name: str, error: Exception, attempt: int = 1):
        """에러 발생 시 메트릭 기록"""
        import time
        if phase_name in self.phase_start_time:
            duration = time.time() - self.phase_start_time[phase_name]
            self.metrics[phase_name] = {
                'status': 'error',
                'duration_seconds': round(duration, 2),
                'error': str(error),
                'attempt': attempt,
            }

    def on_complete(self, success: bool, summary: Dict = None):
        """완료 시 메트릭 저장"""
        metrics_file = "logs/harness_metrics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        logger.info(f"Metrics saved: {metrics_file}")


class AlertHook:
    """에러 발생 시 알림 Hook (선택)"""

    def __init__(self, enable_console: bool = True):
        self.enable_console = enable_console

    def on_phase_error(self, phase_name: str, error: Exception, attempt: int = 1):
        """Phase 에러 시 알림"""
        if self.enable_console:
            self._console_alert(phase_name, error, attempt)

    def on_fallback(self, phase_name: str, fallback_method: str):
        """Fallback 실행 시 알림"""
        if self.enable_console:
            self._console_alert(f"{phase_name} (Fallback)", fallback_method)

    @staticmethod
    def _console_alert(title: str, message: str, attempt: int = None):
        """콘솔 알림"""
        print(f"\n🚨 ALERT: {title}")
        if attempt:
            print(f"   Attempt: {attempt}")
        print(f"   Message: {message}\n")
