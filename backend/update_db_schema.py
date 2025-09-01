#!/usr/bin/env python3
"""
简单的数据库架构更新脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app.models import Base

def update_database_schema():
    """更新数据库架构"""
    print("🔄 更新数据库架构...")
    
    try:
        # 创建所有表和新字段
        # SQLAlchemy会智能地只创建不存在的表和字段
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库架构更新完成！")
        
    except Exception as e:
        print(f"❌ 数据库架构更新失败: {e}")
        print("💡 建议：如果是字段冲突，可能需要手动迁移数据库")
        raise

if __name__ == "__main__":
    update_database_schema()
