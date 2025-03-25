@echo off
chcp 65001 > nul

echo 准备同步到新的 GitHub 仓库...
git remote -v

echo 删除现有的 origin 远程仓库（如果存在）...
git remote remove origin

echo 添加新的 GitHub 远程仓库...
git remote add origin https://github.com/lanlicyuen/StreamRecorder.git

echo 确保使用 GitHub 版本的 README...
copy README_github.md README.md
echo README 已复制

echo 添加所有文件到 Git...
git add .
git status

echo 提交更改...
git commit -m "初始提交：同步完整项目到新的 GitHub 仓库"

echo 推送到 GitHub main 分支...
git push -u origin master:main --force

echo GitHub 同步完成！
pause