#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加新的用户字段
"""

import sys
import os
from sqlalchemy import text, inspect

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base

def check_column_exists(table_name, column_name):
    """检查表中是否存在指定列"""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)

def migrate_database():
    """执行数据库迁移"""
    print("🔄 开始数据库迁移...")
    
    db = SessionLocal()
    try:
        # 检查并添加新字段
        new_fields = [
            ('gender', 'VARCHAR(10)'),
            ('birthday', 'DATETIME'),
            ('interests', 'TEXT'),
            ('address', 'VARCHAR(200)'),
            ('emergency_contact', 'VARCHAR(100)'),
            ('emergency_phone', 'VARCHAR(20)')
        ]
        
        for field_name, field_type in new_fields:
            if not check_column_exists('users', field_name):
                print(f"添加字段: {field_name}")
                sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                db.execute(text(sql))
                db.commit()
                print(f"✅ 字段 {field_name} 添加成功")
            else:
                print(f"⏭️ 字段 {field_name} 已存在，跳过")
        
        print("✅ 数据库迁移完成！")
        
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def reset_database():
    """重置数据库（危险操作，仅用于开发环境）"""
    print("⚠️ 警告：这将删除所有数据！")
    response = input("确定要重置数据库吗？(输入 'YES' 确认): ")
    
    if response == 'YES':
        print("🔄 重置数据库...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库重置完成！")
        
        # 重新初始化数据
        from init_db import init_db
        init_db()
    else:
        print("❌ 操作已取消")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="数据库迁移工具")
    parser.add_argument("--reset", action="store_true", help="重置数据库（删除所有数据）")
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    else:
        migrate_database()
