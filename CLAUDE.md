# CLAUDE.md

이 프로젝트에서 Claude가 따라야 할 행동 규칙.

## 저장소

GitHub: `kyoo111/wiremaint`
gh CLI 경로: `C:\Program Files\GitHub CLI\gh.exe`

## 파일 경로

| 파일 | 경로 |
|---|---|
| 스케줄 태스크 프롬프트 (실행) | `C:\Users\Admin\.claude\scheduled-tasks\ai-daily-report\SKILL.md` |
| 스케줄 태스크 프롬프트 (백업) | `C:\Users\Admin\Desktop\ai_daily_report\scheduled-task-prompt.md` |
| 브리핑 저장 경로 | `C:\Users\Admin\Desktop\ai_daily_report\reports\YYYY-MM-DD_ai_report.html` |
| 스킬 (로컬) | `C:\Users\Admin\.claude\skills\` |
| 스킬 (프로젝트) | `C:\Users\Admin\Desktop\ai_daily_report\.claude\skills\` |

## 스케줄 태스크 프롬프트 수정 시 규칙

두 파일을 항상 동일하게 유지한다.
수정 후 반드시 복사:
```powershell
Copy-Item "C:\Users\Admin\.claude\scheduled-tasks\ai-daily-report\SKILL.md" `
  -Destination "C:\Users\Admin\Desktop\ai_daily_report\scheduled-task-prompt.md" -Force
```

## 이슈 처리 규칙

- 이슈 수정 전 반드시 해당 이슈에 처리 계획 댓글을 먼저 남긴다.
- 커밋 메시지에 `closes #N` 포함 → 푸시 시 GitHub이 자동 Close.
- 여러 이슈 동시 처리: `closes #7, closes #8`

## Harness Architecture (하네스 구조)

공식 문서 기반으로 구축된 4계층 오케스트레이션 시스템.

### 📐 아키텍처 개요

```
Scheduled Task (매일 8시)
    ↓
🎛️ Orchestrator Harness (orchestrator.py - Manual Loop)
    ├─ 🪝 Hook Framework (hooks.py)
    ├─ 📊 State Management (.harness_state.json)
    ├─ 📈 Metrics Collection (logs/harness_metrics.json)
    │
    ├─ Phase 1: BriefingGenerator
    │  └─ Session + SSE Stream
    │
    ├─ Phase 2: BriefingValidator
    │  └─ Validation + Issue Creation
    │
    ├─ Phase 3: IssueProcessor
    │  └─ Issue Handling + Auto-close
    │
    └─ Phase 4: DocumentOptimizer
       └─ Doc Improvement + Commit
```

### 🪝 Hook System (후킹 시스템)

Phase 전후 및 에러 처리 시점에 자동 실행되는 콜백 메커니즘.

**지원 이벤트**:
- `on_start` - 전체 시작
- `before_phase` - Phase 시작 전
- `after_phase` - Phase 완료 후
- `on_phase_error` - Phase 에러 발생
- `on_retry` - 자동 재시도 시작
- `on_fallback` - Fallback 실행
- `on_complete` - 전체 완료

**등록된 Hook Callbacks**:
1. **DefaultHooks** - 콘솔 출력 & 진행상황 알림
2. **StateTrackingHook** - `.harness_state.json` 실시간 저장
3. **MetricsHook** - `logs/harness_metrics.json` 성능 지표 수집
4. **AlertHook** - 에러 발생 시 콘솔 알림

**사용 예시**:
```python
from hooks import HarnessHooks, DefaultHooks, StateTrackingHook

hooks = HarnessHooks()
hooks.register('on_phase_error', DefaultHooks.on_phase_error)
hooks.register('on_phase_error', StateTrackingHook.on_phase_error)

# Phase 실행 중
try:
    result = run_phase()
except Exception as e:
    hooks.trigger('on_phase_error', phase_name, e, attempt=1)  # 모든 콜백 자동 실행
```

### 📊 State & Metrics Files

실행 중 자동으로 생성되는 상태 및 메트릭 파일:

| 파일 | 용도 | 업데이트 시점 |
|------|------|-------------|
| `.harness_state.json` | Phase별 상태 추적 | 실시간 (Hook) |
| `logs/harness_metrics.json` | Phase별 실행 시간 & 토큰 | Phase 완료 시 |
| `logs/hooks_execution.json` | Hook 실행 이력 | 완료 시 |
| `logs/orchestrator.log` | 상세 로깅 | 실시간 |
| `logs/agent_team_result_*.txt` | Phase별 최종 결과 | Phase 완료 시 |

### ⚙️ Harness Components

| 파일 | 용도 | 역할 |
|------|------|------|
| `hooks.py` | Hook Framework | Phase 이벤트 처리 |
| `orchestrator.py` | Main Harness Loop | 4개 Phase 조율 + Hook 통합 |
| `agents.py` | Agent Management | 에이전트 생성 & 세션 관리 |
| `agents_config.yaml` | Agent Config | 5개 에이전트 설정 |

### 🔄 Error Handling & Auto-Retry

자동 재시도 로직 (지수 백오프):

```
Phase 실행 실패
├─ Attempt 1: 즉시 실행
├─ Attempt 2: 4초 후 재시도
├─ Attempt 3: 8초 후 재시도
└─ Attempt 4: 실패 → 다음 Phase로 진행
```

각 재시도 시점에 `on_retry` Hook 자동 실행.

## Managed Agents Multiagent 구조

```
🎯 Coordinator (조율자)
├── 📌 BriefingGenerator (브리핑 생성)
├── ✅ BriefingValidator (품질 검증)
├── 🔧 IssueProcessor (이슈 처리)
├── 📚 DocumentOptimizer (문서 최적화)
└── 🔄 Self (직접 작업)
```

### 에이전트 팀 실행

```bash
# 1단계: 패키지 설치
pip install -r requirements_agents.txt

# 2단계: 에이전트 팀 생성 (한 번만 실행)
python agents.py

# 3단계: 조율자를 통해 전체 프로세스 실행 (Hook Framework 포함)
python orchestrator.py
```

### 설정 파일

| 파일 | 용도 |
|------|------|
| `agents_config.yaml` | 모든 에이전트 설정 (이름, 모델, 시스템 프롬프트) |
| `agents.py` | 에이전트 생성 및 관리 |
| `hooks.py` | Hook Framework (Phase 이벤트 처리) |
| `orchestrator.py` | 전체 워크플로우 조율 + Hook 통합 |
| `.agent_team_config.json` | 생성된 에이전트 ID 및 환경 (자동 생성) |

### 에이전트별 역할

1. **Coordinator**: 전체 프로세스 감독 및 조율
2. **BriefingGenerator**: AI 동향 수집 및 HTML 리포트 생성
3. **BriefingValidator**: 품질 검증 (30일, 수치, 국내비율, 중복 제거)
4. **IssueProcessor**: GitHub 이슈 생성 및 처리
5. **DocumentOptimizer**: SOUL.md, README.md, CLAUDE.md 최적화

### 기존 Skills와의 관계

- **Skills** (`.claude/skills/`): 순차적 실행, 자연어 명령
- **Agents** (API): 병렬 처리, 에이전트 팀 조율, 상태 관리
- **Harness** (orchestrator.py): Manual Loop + Hook Framework + State Management

세 시스템은 상호 보완적으로 사용 가능합니다.

## 커밋 규칙

```
feat: 새 기능 추가
fix: 이슈 수정 (closes #N)
docs: 문서 업데이트
```
