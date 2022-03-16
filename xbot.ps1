$Env:DOCKER_BUILDKIT = 1
$Env:COMPOSE_DOCKER_CLI_BUILD = 1

$ComposeFile = ".\docker-compose.dev.yml"

$Env:XKOM_URL = "http://localhost:5000"
$Env:XKOM_API_URL = "http://localhost:5000"
$Env:SMTP_HOST = "localhost"
$Env:SMTP_PORT = 1025

switch ($args[0]) {
    "build" { & docker-compose.exe -f $ComposeFile build }
    "down" { & docker-compose.exe -f $ComposeFile down }
    "e2e-test" { Set-Location xbot; & python -m pytest .\tests\e2e; Set-Location .. }
    "integration-test" { Set-Location xbot; & python -m pytest .\tests\integration; Set-Location .. }
    "test" { Set-Location xbot; & python -m pytest .\tests; Set-Location .. }
    "unit-test" { Set-Location xbot; & python -m pytest .\tests\unit; Set-Location .. }
    "up" { & docker-compose.exe -f $ComposeFile up }
    "upd" { & docker-compose.exe -f $ComposeFile up -d }
    Default { Write-Output "Invalid command"; exit 1 }
}
