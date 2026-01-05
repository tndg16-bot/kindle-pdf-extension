$envMap = @{
    "GITHUB_OWNER" = "tndg16-bot"
    "GITHUB_REPO" = "papa"
    "GITHUB_FILE_PATH" = "本山貴裕/やりたいことリスト.md"
}

$token = Read-Host "Please enter your GitHub Personal Access Token"

if (-not $token) {
    Write-Error "Token is required."
    exit 1
}

# Set Token
Write-Host "Setting GITHUB_TOKEN..."
"$token`nn`n" | npx vercel env add GITHUB_TOKEN production

# Set other vars
foreach ($key in $envMap.Keys) {
    Write-Host "Setting $key..."
    $val = $envMap[$key]
    "$val`nn`n" | npx vercel env add $key production
}

Write-Host "All GitHub environment variables set!" -ForegroundColor Green
