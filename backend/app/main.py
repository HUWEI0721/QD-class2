from fastapi import FastAPI, Request, Response
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
# 生产环境使用更严格的CORS，开发环境允许所有来源
if settings.environment == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 开发环境允许所有来源
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

@app.get("/api/public/stats")
async def get_public_stats():
    """获取公开的基础统计信息，不需要认证"""
    from .database import SessionLocal
    from .models import User, Activity, MediaItem
    
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_activities = db.query(Activity).count()
        total_media = db.query(MediaItem).count()
        
        return {
            "total_users": total_users,
            "total_activities": total_activities,
            "total_media": total_media,
            "status": "success"
        }
    except Exception as e:
        return {
            "total_users": 0,
            "total_activities": 0,
            "total_media": 0,
            "status": "error",
            "message": str(e)
        }
    finally:
        db.close()

# 添加OPTIONS请求处理，解决预检请求问题
@app.options("/{path:path}")
async def options_handler(request: Request):
    """处理所有OPTIONS预检请求"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )
