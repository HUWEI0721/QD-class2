#!/bin/bash

# 🚀 手动部署到GitHub Pages脚本
# 如果GitHub Actions失败，可以使用此脚本手动部署

set -e

echo "🔍 检查环境..."

# 检查是否在正确目录
if [ ! -f "package.json" ]; then
    echo "❌ 请在frontend目录中运行此脚本"
    echo "使用方法: cd frontend && ../manual-deploy.sh"
    exit 1
fi

# 检查是否安装了gh-pages
if ! npm list gh-pages > /dev/null 2>&1; then
    echo "📦 安装 gh-pages..."
    npm install --save-dev gh-pages
fi

echo "🏗️ 构建项目..."
NODE_ENV=production npm run build

if [ ! -d "dist" ]; then
    echo "❌ 构建失败，dist目录不存在"
    exit 1
fi

echo "📤 部署到GitHub Pages..."
npx gh-pages -d dist -m "Deploy: $(date)"

echo "✅ 部署完成！"
echo "🌐 网站将在几分钟内在以下地址可用:"
echo "   https://$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1.github.io\/\2/')/"
