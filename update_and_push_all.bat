@echo off
cd /d %~dp0
echo ===============================
echo 正在将所有更改添加到 Git 暂存区...
git add .

echo ===============================
echo 输入本次提交说明：
set /p msg=说明: 
git commit -m "%msg%"

echo ===============================
echo 正在推送到 GitHub（main 分支）...
git push origin main

echo ===============================
echo ✅ 推送完成，请检查 GitHub 和 Railway 状态。
pause