@echo off
chcp 65001 > nul

echo 首先添加新文件到 Git...
git add README_github.md README_gitee.md push_all.bat
git commit -m "Add README files for different platforms"

echo 正在推送到 GitHub...
copy README_github.md README.md
git add README.md
git commit -m "Update README for GitHub"
git push origin master

echo 正在推送到 Gitee...
copy README_gitee.md README.md
git add README.md
git commit -m "Update README for Gitee"
git push gitee master

echo 恢复 GitHub README...
copy README_github.md README.md
git add README.md
git commit -m "恢复 GitHub README"
git push origin master

echo 忽略 dist 文件夹中的变化...
git status

echo 推送完成！
pause