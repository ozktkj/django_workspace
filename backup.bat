@echo off
setlocal

set "MYSQL=C:\Program Files\MySQL\MySQL Server 8.3\bin"
set "BACKUP=D:\django_workspace\mysql_backup"
set "DB=psysdb3"

if not exist "%BACKUP%" mkdir "%BACKUP%"

echo MySQL Backup Start....

"%MYSQL%\mysqldump.exe" -u root -p ^
    --databases %DB% ^
    --single-transaction ^
    --routines ^
    --triggers ^
    --events ^
    --hex-blob ^
    --result-file="%BACKUP%\psysdb3.tmp"

echo GET

if errorlevel 1 (
    echo ERROR: Backup failed.
    del "%BACKUP%\psysdb3.tmp"
    pause
    exit /b 1
)

move /Y "%BACKUP%\psysdb3.tmp" "%BACKUP%\psysdb3.sql"

echo Backup completed.
pause
