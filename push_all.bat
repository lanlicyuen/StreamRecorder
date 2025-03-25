@echo off
chcp 65001 > nul

echo 处理 chromedriver.exe 的删除...
git rm chromedriver.exe
git commit -m "删除 chromedriver.exe 文件"

REM 确保我们有 .gitignore 文件
echo dist/app.log > .gitignore
echo dist/config.json >> .gitignore
echo dist/*.log >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore

echo 添加 .gitignore 文件...
git add .gitignore
git commit -m "Add .gitignore file"

echo 添加 README 文件到 Git...
git add README_github.md README_gitee.md push_all.bat -f
git commit -m "Add README files for different platforms"

echo 推送到 GitHub...
copy README_github.md README.md
git add README.md -f
git commit -m "Update README for GitHub"
git push origin master

echo 推送到 Gitee...
copy README_gitee.md README.md
git add README.md -f
git commit -m "Update README for Gitee"
git push gitee master

echo 拉取并合并 Gitee 的变更...
git pull gitee master --allow-unrelated-histories

echo 恢复 GitHub README...
copy README_github.md README.md
git add README.md -f
git commit -m "恢复 GitHub README"
git push origin master

echo 推送完成！
pause