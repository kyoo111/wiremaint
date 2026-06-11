---
name: issue-runner
description: >
  GitHub 열린 이슈를 확인하고, 각 이슈에 처리 계획을 댓글로 남긴 뒤,
  스케줄 프롬프트를 수정하고 커밋·푸시·이슈 Close까지 자동으로 처리하는 스킬.
  "이슈 처리해줘", "열린 이슈 고쳐줘", "issue-runner 실행해줘",
  "이슈 #N 처리해줘" 등의 말이 나오면 반드시 이 스킬을 사용할 것.
---

# issue-runner: 이슈 확인 → 계획 댓글 → 수정 → Close

GitHub 열린 이슈를 순서대로 처리한다. 각 단계를 빠짐없이 실행할 것.

## 1단계 — 열린 이슈 목록 확인

```
gh issue list --repo kyoo111/wiremaint --state open
```

특정 이슈 번호가 지정된 경우:
```
gh issue view [번호] --repo kyoo111/wiremaint
```

## 2단계 — 각 이슈에 처리 계획 댓글 작성

이슈 내용을 읽고 무엇을 어떻게 고칠지 댓글로 먼저 남긴다.
계획을 먼저 공개하면 히스토리가 남아 나중에 왜 고쳤는지 추적할 수 있다.

```
gh issue comment [번호] --repo kyoo111/wiremaint --body "## 처리 계획\n[무엇을 어떻게 수정할지 구체적으로]"
```

## 3단계 — 스케줄 프롬프트 수정

수정 대상 파일 (두 곳 모두 동일하게 수정):
- `C:\Users\Admin\.claude\scheduled-tasks\ai-daily-report\SKILL.md` (실제 실행 파일)
- `C:\Users\Admin\Desktop\ai_daily_report\scheduled-task-prompt.md` (GitHub 백업 사본)

이슈 내용에 맞게 수집 기준, 출력 형식, 완료 조건 등 해당 부분을 수정한다.
수정 후 백업 사본도 반드시 동일하게 업데이트:
```
Copy-Item "C:\Users\Admin\.claude\scheduled-tasks\ai-daily-report\SKILL.md" `
  -Destination "C:\Users\Admin\Desktop\ai_daily_report\scheduled-task-prompt.md" -Force
```

## 4단계 — 커밋·푸시

커밋 메시지에 반드시 `closes #번호` 형식을 포함한다.
이 키워드가 있으면 GitHub이 푸시 시 이슈를 자동으로 Close한다.

```
cd C:\Users\Admin\Desktop\ai_daily_report
git add scheduled-task-prompt.md
git commit -m "fix: [한 줄 요약] (closes #[번호])"
git push origin main
```

이슈가 여러 개면 한 커밋에 모두 포함:
```
git commit -m "fix: [요약] (closes #7, closes #8)"
```

## 5단계 — 결과 보고

처리한 이슈 번호·제목·수정 내용을 표로 정리해서 보여준다.

| 이슈 | 처리 내용 |
|---|---|
| #N 제목 | 수정한 내용 한 줄 요약 |
