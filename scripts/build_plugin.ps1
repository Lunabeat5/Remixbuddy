$cmakePath = "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"

if (-Not (Test-Path $cmakePath)) {
    Write-Error "CMake wurde nicht unter dem erwarteten Pfad gefunden: $cmakePath"
    exit 1
}

$pluginDir = "D:\ASDZ-Projekte-2026\FL-Plugin\plugin"
$buildDir = Join-Path $pluginDir "build"

if (-Not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir -Force
}

Set-Location $pluginDir

Write-Host "--- Konfiguriere RemixBuddy Plugin ---" -ForegroundColor Cyan
& $cmakePath -B build -G "Visual Studio 17 2022" -A x64

if ($LASTEXITCODE -ne 0) {
    Write-Error "CMake-Konfiguration fehlgeschlagen."
    exit 1
}

Write-Host "--- Baue RemixBuddy Plugin (Release) ---" -ForegroundColor Cyan
& $cmakePath --build build --config Release

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build fehlgeschlagen."
    exit 1
}

Write-Host "--- Build erfolgreich abgeschlossen! ---" -ForegroundColor Green
Write-Host "Das VST3-Plugin sollte nun unter 'C:\Program Files\Common Files\VST3' oder im Build-Ordner liegen."
