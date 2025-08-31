from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine
from .models import Base
from .routers import auth, users, activities, media, comments, notifications

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用实例
app = FastAPI(
    title="班级建设网站API",
    description="一个现代化的班级建设网站后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# 注册路由
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(media.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")

# 根路径
@app.get("/")
async def root():
    return {
        "message": "欢迎使用班级建设网站API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点，用于Railway部署监控"""
    try:
        # 简单的数据库连接测试
        from .database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "environment": settings.environment,
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "environment": settings.environment
        }

@app.get("/api/health")
async def api_health_check():
    """API健康检查端点，更详细的检查"""
    return {
        "status": "healthy",
        "message": "班级建设网站API运行正常",
        "version": "1.0.0",
        "environment": settings.environment,
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "auth": "/api/auth",
            "users": "/api/users",
            "activities": "/api/activities",
            "media": "/api/media"
        }
    }
