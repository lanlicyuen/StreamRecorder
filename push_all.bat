@echo off
chcp 65001 > nul

echo 设置远程仓库...
git remote -v
echo 设置 Gitee 远程仓库...
git remote remove gitee 2>nul
git remote add gitee https://gitee.com/lanlicyuenlanlicyuen/stream-recorder.git
echo 设置 GitHub 远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/lanlicyuen/StreamRecorder.git
git remote -v

REM 确保我们有 .gitignore 文件
echo dist/app.log > .gitignore
echo dist/config.json >> .gitignore
echo dist/*.log >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore

echo 记录当前工作区状态（包括文件删除）...
git add -A
git status

echo 提交所有更改（包括删除的文件）...
git commit -m "更新项目文件，处理文件删除"

echo 推送到 GitHub...
copy README_github.md README.md
git add README.md -f
git commit -m "Update README for GitHub"
git push -u origin master:main --force

echo 推送到 Gitee...
copy README_gitee.md README.md
git add README.md -f
git commit -m "Update README for Gitee"
git push -u gitee master --force

echo 恢复 GitHub README...
copy README_github.md README.md
git add README.md -f
git commit -m "恢复 GitHub README"
git push origin master:main

echo 推送完成！
echo.
echo GitHub: https://github.com/lanlicyuen/StreamRecorder
echo Gitee: https://gitee.com/lanlicyuenlanlicyuen/stream-recorder
pause