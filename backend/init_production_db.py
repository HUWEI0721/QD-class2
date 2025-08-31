#!/usr/bin/env python3
"""
生产环境数据库初始化脚本
在Railway首次部署时运行
"""

import os
import sys
from sqlalchemy.orm import Session

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models import User
from app.schemas import UserCreate
from app.routers.auth import create_user

def init_production_db():
    """初始化生产环境数据库"""
    print("🔄 正在初始化生产环境数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成")
    
    db = SessionLocal()
    try:
        # 检查是否已有管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("ℹ️ 管理员用户已存在，跳过初始化")
            return
        
        print("👤 创建默认管理员用户...")
        
        # 创建管理员用户
        admin_data = UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            full_name="系统管理员",
            role="admin"
        )
        
        admin_user = create_user(db, admin_data)
        print(f"✅ 管理员用户创建成功: {admin_user.username}")
        
        print("🎉 生产环境数据库初始化完成！")
        print("📝 默认管理员账号: admin / admin123")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_production_db()
