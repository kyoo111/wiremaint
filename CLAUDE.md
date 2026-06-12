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

## 에이전트 팀 설정

### Managed Agents Multiagent 구조

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

# 3단계: 조율자를 통해 전체 프로세스 실행
python orchestrator.py
```

### 설정 파일

| 파일 | 용도 |
|------|------|
| `agents_config.yaml` | 모든 에이전트 설정 (이름, 모델, 시스템 프롬프트) |
| `agents.py` | 에이전트 생성 및 관리 |
| `orchestrator.py` | 전체 워크플로우 조율 |
| `.agent_team_config.json` | 생성된 에이전트 ID 및 환경 (자동 생성) |

### 에이전트별 역할

1. **Coordinator**: 전체 프로세스 감독 및 조율
2. **BriefingGenerator**: AI 동향 수집 및 HTML 리포트 생성
3. **BriefingValidator**: 품질 검증 (30일, 수치, 국내비율, 중복 제거)
4. **IssueProcessor**: GitHub 이슈 생성 및 처리
5. **DocumentOptimizer**: SOUL.md, README.md, CLAUDE.md 최적화

### 기존 Skills와의 관계

- **Skills** (`@claude/skills/`): 순차적 실행, 자연어 명령
- **Agents** (API): 병렬 처리, 에이전트 팀 조율, 상태 관리

두 시스템은 상호 보완적으로 사용 가능합니다.

## 커밋 규칙

```
feat: 새 기능 추가
fix: 이슈 수정 (closes #N)
docs: 문서 업데이트
```
