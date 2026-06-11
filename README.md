# wiremaint — AI 일일 리포트

매일 오전 8시 AI 동향을 자동 수집해 HTML 브리핑으로 저장하는 프로젝트.

→ 목적과 철학: [SOUL.md](SOUL.md)
→ Claude 행동 규칙: [CLAUDE.md](CLAUDE.md)

## 구조

```
.claude/skills/
  issue-writer/   브리핑 검증 후 GitHub 이슈 자동 등록
  issue-runner/   이슈 읽고 수정 → 커밋 → Close

scheduled-task-prompt.md   ai-daily-report 태스크 프롬프트 (GitHub 백업)
reports/                   생성된 HTML 브리핑 (gitignore)
templates/report.html      HTML 템플릿
```

## 실행

| 할 일 | 명령 |
|---|---|
| 브리핑 즉시 생성 | "오늘 AI 브리핑 만들어줘" |
| 브리핑 검증 + 이슈 등록 | "issue-writer 실행해줘" |
| 이슈 처리 | "issue-runner 실행해줘" |
| 자동 실행 | 매일 오전 8시 (Claude Code 앱이 열려 있을 때) |

## 수집 기준

- 카테고리 6개 (LLM 모델·기업전략·규제·기술트렌드·스타트업·빅테크)
- 글로벌:국내 = 7:3, 국내 최소 4개
- 30일 이내 자료만, 발행일 표시 필수
- 항목당 요약 + 시사점 + 출처 URL

## 개선 히스토리

`git log` 또는 [GitHub Issues](https://github.com/kyoo111/wiremaint/issues?q=is:issue+is:closed) 참고.
