@echo off
chcp 65001 > nul

echo 推送到 GitHub...
copy README_github.md README.md
git add README.md
git commit -m "更新 GitHub README"
git push origin master

echo 推送到 Gitee...
copy README_gitee.md README.md
git add README.md
git commit -m "更新 Gitee README"
git push gitee master

echo 恢复 GitHub README...
copy README_github.md README.md
git add README.md
git commit -m "恢复 GitHub README"
git push origin master

echo 同步完成！
pause