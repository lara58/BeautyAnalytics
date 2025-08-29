@echo off
setlocal enabledelayedexpansion

REM Stop on error
set ERRORLEVEL=0

REM Variables connexion DB
set DB_NAME=beautyanalytics
set DB_USER=postgres
set DB_PASSWORD=postgres
set DB_HOST=localhost
set DB_PORT=5432

echo ===== [1/3] Téléchargement des datasets =====
C:\Users\kheli\AppData\Local\Microsoft\WindowsApps\python3.12.exe scripts\dataset\dataset_download.py
if errorlevel 1 exit /b %errorlevel%
C:\Users\kheli\AppData\Local\Microsoft\WindowsApps\python3.12.exe scripts\dataset\dataset_ingestion.py
if errorlevel 1 exit /b %errorlevel%

echo ===== [2/3] Exécution des scripts SQL supplémentaires =====
REM PostgreSQL password for psql
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f scripts\dataset\persist_data.sql
if errorlevel 1 exit /b %errorlevel%

echo ===== [3/3] Transformation + Insertion dans PostgreSQL =====
C:\Users\kheli\AppData\Local\Microsoft\WindowsApps\python3.12.exe scripts\dataset\dataset_persist.py
if errorlevel 1 exit /b %errorlevel%

echo ===== ✅ ETL terminé avec succès =====
endlocal
