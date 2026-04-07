@echo off
REM AI Traffic Control System - GitHub Push Script
REM This script pushes the committed code to GitHub

echo ============================================
echo AI Traffic Control - GitHub Push Script
echo ============================================
echo.

REM Change to project directory
cd /d "%~dp0"

echo Checking git status...
git status
echo.

echo Pushing to GitHub (https://github.com/archisha-b30/ai-project-)...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Push successful!
    echo Repository: https://github.com/archisha-b30/ai-project-
    pause
) else (
    echo.
    echo ✗ Push failed. Please check:
    echo - Internet connection
    echo - GitHub credentials
    echo - Repository access
    echo.
    pause
)
