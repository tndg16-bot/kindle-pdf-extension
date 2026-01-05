$envMap = @{
    "NEXT_PUBLIC_GOOGLE_FORMS_URL" = "https://docs.google.com/forms/d/e/1FAIpQLSden_oZDjoTd82_laPSbt3Sjj-wWsH8rHzw8T2hd9qSQ1hQSw/formResponse"
    "NEXT_PUBLIC_ENTRY_NAME" = "entry.748946296"
    "NEXT_PUBLIC_ENTRY_EMAIL" = "entry.927838379"
    "NEXT_PUBLIC_ENTRY_OCCUPATION" = "entry.1878828453"
    "NEXT_PUBLIC_ENTRY_GOAL" = "entry.2144465245"
    "NEXT_PUBLIC_ENTRY_MOTIVATION" = "entry.1384709182"
    "NEXT_PUBLIC_ENTRY_DATE1" = "entry.1374991460"
    "NEXT_PUBLIC_ENTRY_DATE2" = "entry.1283089140"
    "NEXT_PUBLIC_ENTRY_MESSAGE" = "entry.1655835053"
}

foreach ($key in $envMap.Keys) {
    Write-Host "Setting $key..."
    # vercel env add prompts: 1. value? 2. encrypt? (y/N)
    # We send: Value + Newline + "n" + Newline
    $val = $envMap[$key]
    $inputStr = "$val`nn`n"
    
    $inputStr | npx vercel env add $key production
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to set $key"
    } else {
        Write-Host "Successfully set $key" -ForegroundColor Green
    }
    Start-Sleep -Seconds 2
}
