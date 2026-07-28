# 自动同步 .claude/skills 仓库的 git 变更
$repoPath = "C:\Users\admin\.claude\skills"
$logFile = "$repoPath\auto-git-sync.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Set-Location $repoPath

    $status = git status --porcelain
    if (-not $status) {
        "$timestamp --- 无变更，跳过提交" | Out-File $logFile -Append
        exit 0
    }

    $null = git add -A
    $null = git commit -m "auto-sync: daily commit $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

    $pushResult = git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        "$timestamp --- 同步成功" | Out-File $logFile -Append
    } else {
        "$timestamp --- push 失败: $pushResult" | Out-File $logFile -Append
    }
} catch {
    "$timestamp --- 错误: $_" | Out-File $logFile -Append
}
