@echo off
chcp 65001 > nul

echo 处理 chromedriver.exe 的删除...
git rm chromedriver.exe
git commit -m "删除 chromedriver.exe 文件"

echo 拉取并合并 Gitee 的变更...
git pull gitee master --allow-unrelated-histories

echo 更新 .gitignore 文件...
echo dist/app.log > .gitignore
echo dist/config.json >> .gitignore
echo dist/*.log >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
git add .gitignore
git commit -m "更新 .gitignore 文件"

echo 同步到 GitHub...
copy README_github.md README.md
git add README.md README_github.md README_gitee.md -f
git commit -m "更新 GitHub README"
git push origin master

echo 同步到 Gitee...
copy README_gitee.md README.md
git add README.md -f
git commit -m "更新 Gitee README"
git push gitee master -f

echo 恢复 GitHub README...
copy README_github.md README.md
git add README.md -f
git commit -m "恢复 GitHub README"
git push origin master

echo 修复完成！
pause