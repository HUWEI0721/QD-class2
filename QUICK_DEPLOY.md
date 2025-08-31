# 🚀 快速部署指南

## ✅ 问题已修复！

npm依赖冲突问题已经解决，现在可以正常部署了。

## 📋 部署检查清单

### 1. 验证本地构建 ✅
```bash
cd frontend
npm install  # 重新安装依赖
npm run build  # 测试构建
```

### 2. 部署到GitHub Pages

#### 2.1 创建GitHub仓库
1. 登录GitHub，创建新仓库：`QD-class2`
2. 设置为Public（GitHub Pages需要）

#### 2.2 上传代码
```bash
# 在项目根目录执行
git init
git add .
git commit -m "feat: 班级建设网站完整版"
git remote add origin https://github.com/YOUR-USERNAME/QD-class2.git
git branch -M main
git push -u origin main
```

#### 2.3 配置GitHub Pages
1. 仓库设置 → Pages
2. Source 选择 "GitHub Actions"
3. 等待自动部署完成

#### 2.4 配置后端API
1. 注册 [Railway](https://railway.app)
2. 连接GitHub仓库
3. 部署 `backend` 目录
4. 添加PostgreSQL数据库
5. 配置环境变量：
   ```
   SECRET_KEY=your-secret-key
   ENVIRONMENT=production
   ```

#### 2.5 更新前端API地址
1. 获得Railway后端URL（如：`https://xxx.railway.app`）
2. GitHub仓库 → Settings → Secrets → Actions
3. 添加密钥：
   - Name: `API_BASE_URL`
   - Value: `https://your-backend.railway.app/api`

## 🎯 最终结果

- **前端网站**: `https://your-username.github.io/QD-class2`
- **后端API**: `https://your-backend.railway.app`
- **自动部署**: 每次git push自动更新

## 🔧 本地开发

```bash
# 后端
cd backend
source venv/bin/activate
python run.py

# 前端  
cd frontend
npm run dev
```

## 📝 测试账号

部署完成后，使用以下账号测试：

- **管理员**: `admin` / `123456`
- **教师**: `teacher` / `123456`  
- **学生**: `student1` / `123456`

## 🚨 故障排除

### 构建失败
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 部署失败
1. 检查GitHub Actions日志
2. 确认API_BASE_URL密钥正确
3. 验证后端服务正常运行

## ✨ 完成！

按照以上步骤，您的班级网站将在几分钟内上线运行！

---

💡 **提示**: 如有问题，查看 `DEPLOYMENT.md` 获取详细说明。
