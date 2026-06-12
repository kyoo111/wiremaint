# Agent Team Setup Guide

## 개요

이 프로젝트는 **Managed Agents의 Multiagent 기능**을 사용하여 AI 일일 리포트 생성 프로세스를 자동화합니다.

### 에이전트 팀 구조

```
🎯 Coordinator (조율자)
├── 📌 BriefingGenerator (브리핑 생성)
├── ✅ BriefingValidator (품질 검증)
├── 🔧 IssueProcessor (이슈 처리)
├── 📚 DocumentOptimizer (문서 최적화)
└── 🔄 Self (자신도 직접 작업 가능)
```

## 설정 단계

### 1단계: 환경 준비

```bash
# 필수 패키지 설치
pip install -r requirements_agents.txt
```

### 2단계: API 키 설정

```bash
# .env 파일에 API 키 설정
ANTHROPIC_API_KEY=your_api_key_here
```

### 3단계: 에이전트 팀 생성

```bash
# agents.py 실행하여 에이전트 팀 설정
python agents.py
```

이 명령어는:
- ✅ 5개의 에이전트 생성 (Briefing Generator, Validator, Issue Processor, Document Optimizer, Coordinator)
- ✅ 클라우드 환경 설정
- ✅ 조율자 에이전트의 multiagent 구성 설정
- ✅ 설정 저장 (.agent_team_config.json)

## 실행

### 조율자를 통해 전체 프로세스 실행

```bash
python orchestrator.py
```

이 명령어는:
1. 브리핑 생성 (BriefingGenerator)
2. 품질 검증 (BriefingValidator)
3. GitHub 이슈 처리 (IssueProcessor)
4. 문서 최적화 (DocumentOptimizer)
를 순서대로 실행합니다.

### 특정 에이전트만 실행

```python
from agents import run_agent_team, load_agent_config

# 저장된 설정 로드
agent_config = json.load(open(".agent_team_config.json"))

# 특정 작업 실행
result = run_agent_team("브리핑을 생성해주세요", agent_config)
```

## 주요 파일

| 파일 | 용도 |
|------|------|
| `agents_config.yaml` | 모든 에이전트 설정 (이름, 모델, 시스템 프롬프트, 도구) |
| `agents.py` | 에이전트 생성 및 관리 로직 |
| `orchestrator.py` | 전체 워크플로우 조율 및 실행 |
| `.agent_team_config.json` | 생성된 에이전트 ID 및 환경 설정 (자동 생성) |

## 에이전트 역할

### 🎯 Coordinator (조율자)
- 전체 프로세스 감독
- 각 에이전트에 작업 위임
- 단계별 완료 확인

### 📌 BriefingGenerator (브리핑 생성)
- AI 동향 수집 (웹 검색)
- HTML 리포트 생성
- 카테고리별 정리

### ✅ BriefingValidator (품질 검증)
- 30일 초과 자료 검증
- 수치 오류 확인
- 국내/글로벌 비율 검증
- 중복 기사 제거

### 🔧 IssueProcessor (이슈 처리)
- GitHub 이슈 생성
- 이슈 처리 계획 댓글 작성
- 코드 수정 및 커밋
- 이슈 자동 닫기

### 📚 DocumentOptimizer (문서 최적화)
- SOUL.md, README.md, CLAUDE.md 검토
- 역할 분리 (왜/목표 | 무엇/어떻게 | 규칙)
- 중복 제거 및 링크화
- 낡은 내용 정리

## Multiagent 패턴의 장점

1. **병렬 처리**: 여러 에이전트가 독립적으로 작업
2. **책임 분리**: 각 에이전트는 명확한 역할 수행
3. **확장성**: 새로운 에이전트 쉽게 추가 가능
4. **상태 관리**: 각 에이전트는 자체 대화 이력 유지
5. **에러 격리**: 한 에이전트의 실패가 다른 에이전트에 영향 없음

## 기존 Skills 시스템과의 관계

| 항목 | Skills | Agents |
|------|--------|--------|
| 위치 | `.claude/skills/` | Anthropic API |
| 실행 방식 | 순차적 명령 | 병렬 + 조율 |
| 상태 추적 | GitHub Issues | API Events |
| 에이전트 관리 | 버전 관리 없음 | 버전 관리 내장 |

두 시스템은 상호 보완적이며, 필요에 따라 선택하거나 함께 사용할 수 있습니다.

## 로그 및 모니터링

모든 실행 결과는 `logs/` 디렉토리에 저장됩니다:

```
logs/
├── agent_team_result_20240101_120000.txt
├── agent_team_result_20240102_120000.txt
└── ...
```

## 문제 해결

### "Agent team not configured" 오류
```bash
python agents.py  # 에이전트 팀 재설정
```

### API 키 오류
```bash
echo ANTHROPIC_API_KEY=your_key > .env
```

### 에이전트 ID 재확인
```python
import json
config = json.load(open(".agent_team_config.json"))
print(config)
```

## 다음 단계

1. `agents_config.yaml`에서 에이전트 설정 커스터마이징
2. 각 에이전트의 시스템 프롬프트 튜닝
3. 새로운 도구 추가 (예: Slack 통지, 데이터베이스 연동)
4. 자동 스케줄 설정 (매일 실행)

## 참고 문서

- [Managed Agents 공식 문서](https://platform.claude.com/docs/en/managed-agents/overview)
- [Multiagent 패턴](https://platform.claude.com/docs/en/managed-agents/multi-agent)
- [Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
