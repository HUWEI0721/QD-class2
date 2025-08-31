# 班级建设网站

一个基于 Vue3 + Python FastAPI 构建的现代化班级建设网站，为班级成员提供信息交流、活动管理、照片分享等功能。

## ✨ 功能特色

### 🎨 精美的UI设计
- 现代化的界面设计，采用 Element Plus 组件库
- 响应式布局，支持桌面端和移动端
- 优雅的动画效果和交互体验
- 渐变色彩搭配，视觉效果佳

### 🔐 用户认证系统
- 用户注册和登录
- JWT 身份验证
- 角色权限管理（学生、教师、管理员）
- 个人资料管理

### 👥 班级同学管理
- 查看班级所有成员信息
- 搜索和筛选功能
- 详细的个人信息展示
- 联系方式管理

### 📅 活动管理
- 创建和管理班级活动
- 活动状态跟踪（即将开始、进行中、已完成）
- 活动筛选和搜索
- 活动详情查看

### 📸 照片视频分享
- 按活动分类管理照片和视频
- 文件上传和预览
- 媒体文件统计
- 支持多种格式（JPG、PNG、GIF、MP4、MOV）

### 💬 评论和通知
- 对照片视频进行评论
- 回复评论功能
- 实时通知系统
- 评论管理

## 🛠 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - Vue 3 组件库
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理
- **Axios** - HTTP 客户端
- **Day.js** - 日期处理库

### 后端
- **Python 3.8+** - 编程语言
- **FastAPI** - 现代 Python Web 框架
- **SQLAlchemy** - ORM 框架
- **Alembic** - 数据库迁移工具
- **JWT** - 身份验证
- **Uvicorn** - ASGI 服务器

### 数据库
- **SQLite** - 开发环境（默认，无需额外配置）
- **PostgreSQL** - 生产环境（Railway部署时自动配置）

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 一键启动（推荐）
```bash
# 克隆项目后，直接运行启动脚本
cd QD-class2
./start.sh
```

### 手动启动

#### 后端设置

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 初始化数据库（首次运行）
```bash
python init_db.py
```

5. 启动后端服务
```bash
python run.py
```

后端服务将运行在 http://localhost:8000

#### 前端设置

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

前端应用将运行在 http://localhost:5173

### 测试账号
系统已预置以下测试账号：

| 角色 | 用户名 | 密码 | 说明 |
|------|-------|------|------|
| 管理员 | admin | 123456 | 系统管理员账号 |
| 教师 | teacher | 123456 | 教师账号 |
| 学生 | student1 | 123456 | 学生账号1 |
| 学生 | student2 | 123456 | 学生账号2 |
| 学生 | student3 | 123456 | 学生账号3 |

## 📁 项目结构

```
QD-class2/
├── backend/                    # 后端代码
│   ├── app/                   # 应用核心
│   │   ├── routers/          # API 路由
│   │   ├── models.py         # 数据模型
│   │   ├── schemas.py        # Pydantic 模式
│   │   ├── auth.py           # 认证相关
│   │   ├── config.py         # 配置管理
│   │   ├── database.py       # 数据库连接
│   │   └── main.py           # 主应用
│   ├── uploads/              # 文件上传目录
│   ├── requirements.txt      # Python 依赖
│   └── run.py               # 启动脚本
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── components/       # 组件
│   │   ├── layouts/          # 布局组件
│   │   ├── views/            # 页面视图
│   │   ├── stores/           # 状态管理
│   │   ├── router/           # 路由配置
│   │   └── assets/           # 静态资源
│   ├── package.json          # 前端依赖
│   └── vite.config.js        # Vite 配置
└── README.md                 # 项目说明
```

## 🎯 功能展示

### 登录注册
- 简洁的登录界面
- 详细的注册表单
- 表单验证和错误提示

### 首页仪表板
- 欢迎信息和统计数据
- 快捷功能入口
- 最新活动展示
- 班级动态通知

### 班级同学
- 网格式同学展示
- 搜索和筛选功能
- 详细信息弹窗
- 在线状态显示

### 活动管理
- 活动创建和编辑
- 状态分类管理
- 时间线展示
- 关联照片查看

### 照片视频
- 瀑布流式展示
- 活动分类筛选
- 在线预览功能
- 评论互动系统

### 个人资料
- 个人信息编辑
- 头像上传
- 活动记录
- 数据统计

## 🔧 开发指南

### API 文档
启动后端服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 数据库迁移
```bash
# 创建迁移文件
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head
```

### 代码规范
- 前端使用 ESLint + Prettier
- 后端遵循 PEP 8 规范
- 提交信息使用约定式提交格式

## 🚀 部署

### 生产环境部署

**推荐方式：GitHub Pages + Railway**

1. **前端部署到GitHub Pages**
   - 自动从GitHub仓库部署
   - 免费托管静态网站
   - 详见 `DEPLOYMENT.md`

2. **后端部署到Railway**
   - 自动配置PostgreSQL数据库
   - 零配置部署
   - 免费额度足够使用

3. **本地开发使用SQLite**
   - 无需额外配置
   - 数据文件：`backend/class_website.db`

### Docker 部署（可选）
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。

## 🚀 在线演示

- **在线访问**: [https://your-username.github.io/QD-class2](https://your-username.github.io/QD-class2)
- **后端API**: [https://your-backend.railway.app](https://your-backend.railway.app)

## 🌐 部署指南

### GitHub Pages 部署（前端）

1. **Fork 此仓库**到您的 GitHub 账号

2. **启用 GitHub Pages**
   - 进入仓库设置 → Pages
   - Source 选择 "GitHub Actions"

3. **配置环境变量**
   - 进入仓库设置 → Secrets and variables → Actions
   - 添加 `API_BASE_URL` 密钥，值为您的后端API地址

4. **推送代码**触发自动部署
   ```bash
   git push origin main
   ```

### Railway 部署（后端）

1. **注册 [Railway](https://railway.app) 账号**

2. **连接 GitHub 仓库**
   - 新建项目 → Deploy from GitHub repo
   - 选择 QD-class2 仓库

3. **配置环境变量**
   ```
   # Railway会自动配置DATABASE_URL (PostgreSQL)
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=production
   ```

4. **部署完成后**更新前端的 API_BASE_URL

### 其他部署选项

#### Vercel（推荐用于前端）
```bash
npm install -g vercel
cd frontend
vercel --prod
```

#### Heroku（后端）
```bash
git subtree push --prefix backend heroku main
```

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 优秀的前端框架
- [Element Plus](https://element-plus.org/) - 精美的组件库
- [FastAPI](https://fastapi.tiangolo.com/) - 现代的 Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - 强大的 ORM 工具
- [GitHub Pages](https://pages.github.com/) - 免费的静态网站托管
- [Railway](https://railway.app/) - 现代化的云平台

## 📞 联系我们

如果您有任何问题或建议，请随时联系我们：

- 项目地址: [GitHub](https://github.com/your-username/QD-class2)
- 问题反馈: [Issues](https://github.com/your-username/QD-class2/issues)
- 在线演示: [Demo](https://your-username.github.io/QD-class2)

---

**让我们一起构建更好的班级数字化平台！** 🎉
