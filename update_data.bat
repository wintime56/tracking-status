@echo off
cd /d "%~dp0"
echo Updating data.csv to GitHub...
git add data/data.csv
git commit -m "update data.csv"
git push origin main
pause