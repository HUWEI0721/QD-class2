#!/bin/bash

# 班级建设网站部署脚本

echo "🚀 开始部署班级建设网站"
echo "=============================="

# 检查是否在项目根目录
if [ ! -f "README.md" ] || [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查是否安装了 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查是否安装了 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未找到 Git，请先安装 Git"
    exit 1
fi

echo "✅ 环境检查通过"

# 初始化 Git 仓库（如果需要）
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit: Class website project"
    
    echo ""
    echo "🔗 请手动添加远程仓库:"
    echo "git remote add origin https://github.com/your-username/QD-class2.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
    read -p "添加完远程仓库后按 Enter 继续..."
fi

# 构建前端
echo ""
echo "🏗️ 构建前端项目..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "📥 安装前端依赖..."
    npm install
fi

# 构建项目
echo "⚡ 构建生产版本..."
NODE_ENV=production npm run build

if [ $? -eq 0 ]; then
    echo "✅ 前端构建成功"
else
    echo "❌ 前端构建失败"
    exit 1
fi

cd ..

# 提交更改
echo ""
echo "📤 提交更改到 Git..."
git add .
git commit -m "Deploy: Ready for GitHub Pages deployment"

echo ""
echo "🎉 部署准备完成！"
echo "=============================="
echo ""
echo "🌐 下一步操作:"
echo "1. 推送代码到 GitHub:"
echo "   git push origin main"
echo ""
echo "2. 在 GitHub 仓库中:"
echo "   - 进入 Settings → Pages"
echo "   - Source 选择 'GitHub Actions'"
echo ""
echo "3. 配置后端 (推荐使用 Railway):"
echo "   - 访问 https://railway.app"
echo "   - 连接您的 GitHub 仓库"
echo "   - 部署 backend 目录"
echo ""
echo "4. 配置环境变量:"
echo "   - 在 GitHub 仓库 Settings → Secrets"
echo "   - 添加 API_BASE_URL (后端地址)"
echo ""
echo "📖 详细部署指南请查看 README.md"
