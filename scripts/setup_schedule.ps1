# 매일 오전 8시 자동 실행 스케줄 등록
$scriptPath = (Resolve-Path "$PSScriptRoot\run_report.ps1").Path
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NonInteractive -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00AM"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask -TaskName "AI-Daily-Report" -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "스케줄 등록 완료: 매일 오전 8시 자동 실행" -ForegroundColor Green
