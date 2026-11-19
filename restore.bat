@echo off
setlocal

set "BACKUP=D:\django_workspace\mysql_backup"

echo MySQL RESTORE

echo .
echo [1/3]Restore user
mysql -u root -p < "%BACKUP%\user_create.sql"

if errorlevel 1 (
    echo ERROR: usr restore failed.
    pause
    exit /b 1
)

echo .
echo [2/3]Restore database
mysql -u root -p < "%BACKUP%\psysdb3.sql"

if errorlevel 1 (
    echo ERROR: DB restore failed.
    pause
    exit /b 1
)

echo .
echo [2/3]Restore grants
mysql -u root -p < "%BACKUP%\user_grant.sql"

if errorlevel 1 (
    echo ERROR: grants restore failed.
    pause
    exit /b 1
)

echo .
echo MySQL RESTORE completed