@echo off
setlocal
if not defined FRET_HOME set "FRET_HOME=%~dp0..\vendor\fret\fret-electron"
cd /d "%FRET_HOME%"
set "NODE_ENV=production"
set "FRET_LEVEL_DB=%~dp0desktop-data\fret-db"
set "FRET_MODEL_DB=%~dp0desktop-data\model-db"
if not exist "%FRET_LEVEL_DB%\CURRENT" (
  echo Initialize the demo database first: node projects\seed-database.cjs
  pause
  exit /b 1
)
if not exist "%FRET_MODEL_DB%" mkdir "%FRET_MODEL_DB%"
start "" "node_modules\electron\dist\electron.exe" app --user-data-dir="%~dp0desktop-data\electron-profile"
endlocal
