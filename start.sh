#!/bin/bash

# 班级建设网站启动脚本

echo "🎓 班级建设网站启动脚本"
echo "=========================="

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查是否安装了 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

# 检查是否安装了 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm，请先安装 npm"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动后端服务
echo ""
echo "🚀 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装 Python 依赖..."
pip install -r requirements.txt

# 初始化数据库（如果需要）
if [ ! -f "class_website.db" ]; then
    echo "🗄️ 初始化数据库..."
    python init_db.py
fi

# 启动后端（后台运行）
echo "⚡ 启动后端服务 (http://localhost:8000)..."
python run.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务
echo ""
echo "🚀 启动前端服务..."
cd ../frontend

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📥 安装前端依赖..."
    npm install
fi

# 启动前端
echo "⚡ 启动前端服务 (http://localhost:5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 启动完成！"
echo "=========================="
echo "📖 后端 API 文档: http://localhost:8000/docs"
echo "🌐 前端应用: http://localhost:5173"
echo "🛑 按 Ctrl+C 停止服务"
echo ""

# 等待用户中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 保持脚本运行
wait
