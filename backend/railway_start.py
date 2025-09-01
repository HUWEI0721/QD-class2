#!/usr/bin/env python3
"""
Railway专用启动脚本 - 确保数据库迁移后再启动应用
"""

import os
import sys
import logging
import uvicorn
from sqlalchemy import text, inspect, create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """在启动前执行数据库迁移"""
    try:
        logger.info("🔄 Railway启动：执行数据库迁移...")
        
        # 获取数据库连接
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            logger.warning("未找到DATABASE_URL环境变量")
            return
        
        # 修复Railway PostgreSQL URL格式
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # 检查数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("✅ 数据库连接成功")
        
        # 检查并添加新字段
        inspector = inspect(engine)
        if inspector.has_table('users'):
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
            try:
                for field_name, field_type in new_fields.items():
                    if field_name not in existing_columns:
                        logger.info(f"添加新字段: {field_name}")
                        sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                        db.execute(text(sql))
                        db.commit()
                        logger.info(f"✅ 字段 {field_name} 添加成功")
                    else:
                        logger.info(f"⏭️ 字段 {field_name} 已存在")
                        
                logger.info("✅ 数据库迁移完成")
            except Exception as e:
                logger.error(f"❌ 数据库迁移失败: {e}")
                db.rollback()
                raise
            finally:
                db.close()
        else:
            logger.info("users表不存在，将由SQLAlchemy创建")
            
    except Exception as e:
        logger.error(f"数据库迁移过程中出错: {e}")
        # 不阻止应用启动，让SQLAlchemy处理基本表创建

if __name__ == "__main__":
    # 执行数据库迁移
    migrate_database()
    
    # 启动应用
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🚀 启动应用，端口: {port}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
