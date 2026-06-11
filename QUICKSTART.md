# 빠른 시작 가이드

## 1. 환경 설정

```bash
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY 입력
```

## 2. 의존성 설치

```bash
pip install -r requirements.txt
```

## 3. 리포트 즉시 생성

```bash
python src/main.py
```

## 4. 자동 스케줄 설정 (Windows)

```powershell
.\scripts\setup_schedule.ps1
```

매일 오전 8시에 자동으로 리포트가 `reports/` 폴더에 생성됩니다.

## 출력 예시

```
reports/
└── 2026-06-11_ai_report.html
```
