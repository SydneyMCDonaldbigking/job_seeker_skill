$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetRoot = Join-Path $HOME ".codex\skills"

$skills = @(
    "filtering-jobs-multilingual",
    "tailoring-resume-to-jd",
    "managing-job-pipeline-marvis"
)

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null

foreach ($skill in $skills) {
    $source = Join-Path $scriptDir $skill
    $target = Join-Path $targetRoot $skill

    if (-not (Test-Path $source)) {
        throw "Missing skill source: $source"
    }

    if (Test-Path $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }

    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Write-Host "Installed $skill -> $target"
}

Write-Host ""
Write-Host "Codex skills installed."
Write-Host "Restart or refresh the agent session before first use if the skills do not appear immediately."
