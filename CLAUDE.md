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

## 커밋 규칙

```
feat: 새 기능 추가
fix: 이슈 수정 (closes #N)
```
