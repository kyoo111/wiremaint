---
name: issue-runner
description: >
  GitHub 이슈를 읽고 AI 일일 리포트 스케줄 프롬프트를 수정한 뒤 커밋하고 이슈를 Close하는 스킬.
  "이슈 #N 처리해줘", "열린 이슈 처리해줘", "이슈 고쳐줘", "이슈 기반으로 수정해줘" 등의
  말이 나오면 반드시 이 스킬을 사용할 것.
---

# issue-runner: 이슈 읽고 수정 후 Close

GitHub 이슈를 확인하고, 스케줄 프롬프트를 수정한 뒤, 커밋·푸시·이슈 Close까지 한 번에 처리한다.

## 1단계 — 이슈 읽기

특정 이슈 번호가 지정된 경우:
```
gh issue view [번호] --repo kyoo111/wiremaint
```

열린 이슈 전체를 처리하는 경우:
```
gh issue list --repo kyoo111/wiremaint --state open
```
목록을 보고 각 이슈를 순서대로 처리한다.

## 2단계 — 현재 상태 파악

수정 대상 파일:
- 스케줄 프롬프트: `C:\Users\Admin\.claude\scheduled-tasks\ai-daily-report\SKILL.md`
- 리포 사본: `C:\Users\Admin\Desktop\ai_daily_report\scheduled-task-prompt.md`

이슈 내용을 읽고 어떤 부분을 어떻게 고칠지 이슈에 댓글로 계획을 먼저 남긴다:
```
gh issue comment [번호] --repo kyoo111/wiremaint --body "## 처리 계획\n[무엇을 어떻게 수정할지]"
```

## 3단계 — 수정 적용

이슈 내용에 맞게 스케줄 프롬프트(`SKILL.md`)를 수정한다.
수정 후 리포 사본(`scheduled-task-prompt.md`)도 동일하게 업데이트한다.

## 4단계 — 커밋·푸시·이슈 Close

```
cd C:\Users\Admin\Desktop\ai_daily_report
git add scheduled-task-prompt.md
git commit -m "fix: [한 줄 요약] (closes #[번호])"
git push origin main
```

커밋 메시지에 `closes #번호`를 포함하면 푸시 시 GitHub이 자동으로 이슈를 닫는다.

## 5단계 — 결과 보고

처리한 이슈 번호·제목·수정 내용을 한 줄씩 요약해서 보여준다.
