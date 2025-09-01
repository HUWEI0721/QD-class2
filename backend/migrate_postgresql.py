#!/usr/bin/env python3
"""
PostgreSQL数据库迁移脚本 - Railway生产环境
"""

import sys
import os
from sqlalchemy import text, inspect, create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings

def get_database_engine():
    """获取数据库引擎"""
    database_url = os.environ.get('DATABASE_URL') or settings.database_url
    
    # 修复Railway PostgreSQL URL格式
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return create_engine(database_url)

def check_column_exists(engine, table_name, column_name):
    """检查表中是否存在指定列"""
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        return any(col['name'] == column_name for col in columns)
    except Exception as e:
        print(f"检查列时出错: {e}")
        return False

def migrate_postgresql():
    """执行PostgreSQL数据库迁移"""
    print("🔄 开始PostgreSQL数据库迁移...")
    
    try:
        engine = get_database_engine()
        print(f"数据库连接: {engine.url}")
        
        # 创建会话
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 要添加的新字段
        new_fields = [
            ('gender', 'VARCHAR(10)'),
            ('birthday', 'TIMESTAMP'),
            ('interests', 'TEXT'),
            ('address', 'VARCHAR(200)'),
            ('emergency_contact', 'VARCHAR(100)'),
            ('emergency_phone', 'VARCHAR(20)')
        ]
        
        for field_name, field_type in new_fields:
            try:
                if not check_column_exists(engine, 'users', field_name):
                    print(f"添加字段: {field_name} ({field_type})")
                    sql = f"ALTER TABLE users ADD COLUMN {field_name} {field_type}"
                    db.execute(text(sql))
                    db.commit()
                    print(f"✅ 字段 {field_name} 添加成功")
                else:
                    print(f"⏭️ 字段 {field_name} 已存在，跳过")
            except Exception as e:
                print(f"❌ 添加字段 {field_name} 失败: {e}")
                db.rollback()
                # 继续尝试其他字段
                continue
        
        print("✅ PostgreSQL数据库迁移完成！")
        db.close()
        
    except Exception as e:
        print(f"❌ PostgreSQL数据库迁移失败: {e}")
        print("请检查数据库连接和权限")
        raise

def test_connection():
    """测试数据库连接"""
    try:
        engine = get_database_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 数据库连接成功!")
            print(f"PostgreSQL版本: {version}")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PostgreSQL数据库迁移工具")
    parser.add_argument("--test", action="store_true", help="测试数据库连接")
    args = parser.parse_args()
    
    if args.test:
        test_connection()
    else:
        if test_connection():
            migrate_postgresql()
        else:
            print("❌ 数据库连接失败，无法执行迁移")
