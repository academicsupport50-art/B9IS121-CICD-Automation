param(
    [Parameter(Mandatory=$true)]
    [string]$BaseUrl
)
$BaseUrl = $BaseUrl.TrimEnd("/")
Write-Host "[1/4] Health endpoint"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/healthz" | ConvertTo-Json
Write-Host "[2/4] Build metadata"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/info" | ConvertTo-Json
Write-Host "[3/4] Resource collection"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/resources" | ConvertTo-Json -Depth 5
Write-Host "[4/4] POST echo"
$Body = @{ message = "smoke test"; correlation_id = "powershell-001" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/echo" -ContentType "application/json" -Body $Body | ConvertTo-Json
