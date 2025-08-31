# 🚀 班级建设网站部署指南

本指南将帮助您将班级建设网站部署到线上，实现真正的在线访问。

## 📋 部署架构

- **前端**: GitHub Pages（静态托管，免费）
- **后端**: Railway（云平台，免费额度）
- **数据库**: Railway PostgreSQL（免费额度）

## 🎯 第一步：准备GitHub仓库

### 1.1 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 `+` → `New repository`
3. 仓库名设置为：`QD-class2`
4. 设置为 `Public`（GitHub Pages需要）
5. 点击 `Create repository`

### 1.2 上传代码到GitHub

```bash
# 在项目根目录执行
cd /Users/hjw/Desktop/QD-class2

# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: 班级建设网站"

# 连接到GitHub仓库（替换为您的用户名）
git remote add origin https://github.com/YOUR-USERNAME/QD-class2.git
git branch -M main
git push -u origin main
```

## 🌐 第二步：部署后端到Railway

### 2.1 注册Railway账号

1. 访问 [Railway](https://railway.app)
2. 点击 `Sign in with GitHub` 使用GitHub账号登录

### 2.2 部署后端

1. **创建新项目**
   - 点击 `New Project`
   - 选择 `Deploy from GitHub repo`
   - 选择 `QD-class2` 仓库

2. **配置部署**
   - 在项目设置中，设置 `Root Directory` 为 `backend`
   - Railway会自动检测到Python项目

3. **添加环境变量**
   在Railway项目的 `Variables` 标签页中添加：
   ```
   DATABASE_URL=postgresql://...（Railway会自动提供）
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ENVIRONMENT=production
   ALLOWED_ORIGINS=["https://your-username.github.io"]
   ```

4. **添加PostgreSQL数据库**
   - 在项目中点击 `+ Add Service`
   - 选择 `PostgreSQL`
   - Railway会自动设置 `DATABASE_URL`

### 2.3 获取后端URL

部署完成后，您会得到一个后端URL，类似：
```
https://your-backend-name.railway.app
```

## 📱 第三步：配置前端并部署到GitHub Pages

### 3.1 配置GitHub Secrets

1. 进入GitHub仓库页面
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加以下密钥：
   - **Name**: `API_BASE_URL`
   - **Value**: `https://your-backend-name.railway.app/api`

### 3.2 启用GitHub Pages

1. 在仓库页面，点击 `Settings`
2. 滚动到 `Pages` 部分
3. **Source** 选择 `GitHub Actions`
4. 保存设置

### 3.3 触发部署

推送任何更改到 `main` 分支都会触发自动部署：

```bash
git add .
git commit -m "Deploy: Configure for production"
git push origin main
```

## 🔧 第四步：初始化生产数据库

### 4.1 连接到Railway后端

部署完成后，访问您的后端URL：
```
https://your-backend-name.railway.app/docs
```

### 4.2 初始化数据

由于生产环境是新的数据库，您需要：

1. **访问API文档页面**进行注册
2. **或者修改初始化脚本**在Railway中自动运行

可以在Railway的部署日志中查看初始化结果。

## 🎉 第五步：访问您的网站

### 前端地址
```
https://your-username.github.io/QD-class2
```

### 后端API
```
https://your-backend-name.railway.app
```

## 🔍 故障排除

### 常见问题

1. **GitHub Pages部署失败**
   - 检查 `API_BASE_URL` 密钥是否正确设置
   - 查看 Actions 页面的部署日志

2. **后端部署失败**
   - 检查 `backend/requirements.txt` 是否包含所有依赖
   - 查看Railway的部署日志

3. **CORS错误**
   - 确保后端的 `ALLOWED_ORIGINS` 包含前端域名
   - 检查前端的API调用地址是否正确

4. **数据库连接失败**
   - 确保Railway的PostgreSQL服务正在运行
   - 检查 `DATABASE_URL` 环境变量

### 调试技巧

1. **查看部署日志**
   - GitHub: Actions 页面
   - Railway: 项目的 Deployments 页面

2. **检查网络请求**
   - 打开浏览器开发者工具
   - 查看 Network 标签页的API请求

## 📊 监控和维护

### 定期维护

1. **监控Railway使用量**（免费额度有限）
2. **定期备份数据库**
3. **更新依赖包版本**

### 扩展选项

当项目增长时，可以考虑：

1. **升级Railway套餐**获得更多资源
2. **使用CDN**加速静态资源
3. **添加域名**使用自定义域名

## 💡 小贴士

1. **使用环境变量**管理不同环境的配置
2. **定期提交代码**保持版本控制
3. **写好提交信息**方便追踪变更
4. **测试后再部署**确保功能正常

---

🎊 **恭喜！您的班级建设网站现在已经在线运行了！**

记得与班级同学分享网站地址，开始使用这个数字化平台吧！
