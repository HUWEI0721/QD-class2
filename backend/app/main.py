from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text, inspect
import logging
from .config import settings
from .database import engine, SessionLocal
from .models import Base
from .routers import auth, users, activities, media, comments, notifications

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_database_schema():
    """确保数据库架构是最新的，包括新添加的字段"""
    try:
        logger.info("检查数据库架构...")
        
        # 首先创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 检查并添加新字段（如果不存在）
        inspector = inspect(engine)
        
        # 检查users表是否存在新字段
        if inspector.has_table('users'):
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            # 需要添加的新字段
            new_fields = {
                'gender': 'VARCHAR(10)',
                'birthday': 'TIMESTAMP',
                'interests': 'TEXT',
                'address': 'VARCHAR(200)',
                'emergency_contact': 'VARCHAR(100)',
                'emergency_phone': 'VARCHAR(20)'
            }
            
            db = SessionLocal()
            try:
                for field_name, field_type in new_fields.items():
                    if field_name not in existing_columns:
                        logger.info(f"添加新字段: {field_name}")
                        sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                        db.execute(text(sql))
                        db.commit()
                        logger.info(f"✅ 字段 {field_name} 添加成功")
            except Exception as e:
                logger.error(f"添加字段时出错: {e}")
                db.rollback()
            finally:
                db.close()
        
        logger.info("✅ 数据库架构检查完成")
        
    except Exception as e:
        logger.error(f"数据库架构检查失败: {e}")
        # 不要阻止应用启动，让基本功能可以工作

# 在应用启动时确保数据库架构
ensure_database_schema()

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

@app.post("/api/admin/migrate-database")
async def manual_migrate_database():
    """手动触发数据库迁移（紧急修复用）"""
    try:
        logger.info("手动触发数据库迁移...")
        
        inspector = inspect(engine)
        if not inspector.has_table('users'):
            return {"status": "error", "message": "users表不存在"}
        
        existing_columns = [col['name'] for col in inspector.get_columns('users')]
        
        new_fields = {
            'gender': 'VARCHAR(10)',
            'birthday': 'TIMESTAMP',
            'interests': 'TEXT',
            'address': 'VARCHAR(200)',
            'emergency_contact': 'VARCHAR(100)',
            'emergency_phone': 'VARCHAR(20)'
        }
        
        db = SessionLocal()
        added_fields = []
        
        try:
            for field_name, field_type in new_fields.items():
                if field_name not in existing_columns:
                    sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                    db.execute(text(sql))
                    db.commit()
                    added_fields.append(field_name)
                    logger.info(f"✅ 字段 {field_name} 添加成功")
            
            return {
                "status": "success",
                "message": "数据库迁移完成",
                "added_fields": added_fields,
                "existing_fields": [f for f in new_fields.keys() if f in existing_columns]
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"迁移失败: {e}")
            return {
                "status": "error",
                "message": f"迁移失败: {str(e)}",
                "added_fields": added_fields
            }
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"迁移过程出错: {e}")
        return {
            "status": "error",
            "message": f"迁移过程出错: {str(e)}"
        }

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
