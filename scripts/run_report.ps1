# AI 일일 리포트 실행 스크립트
Set-Location $PSScriptRoot\..

Write-Host "AI 일일 리포트 생성 중..." -ForegroundColor Cyan

python src/main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "완료!" -ForegroundColor Green
    $today = Get-Date -Format "yyyy-MM-dd"
    $reportPath = "reports\${today}_ai_report.html"
    if (Test-Path $reportPath) {
        Start-Process $reportPath
    }
} else {
    Write-Host "오류가 발생했습니다." -ForegroundColor Red
}
