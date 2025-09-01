#!/usr/bin/env python3
"""
修复student_id唯一约束冲突的脚本
"""

import sys
import os
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_student_id_constraint():
    """修复student_id唯一约束问题"""
    try:
        # 获取数据库连接
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("未找到DATABASE_URL环境变量")
            return False
        
        # 修复Railway PostgreSQL URL格式
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        print("🔄 开始修复student_id唯一约束问题...")
        
        db = SessionLocal()
        try:
            # 1. 检查是否存在唯一约束
            print("1. 检查现有约束...")
            result = db.execute(text("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'users' 
                AND constraint_type = 'UNIQUE' 
                AND constraint_name LIKE '%student_id%'
            """))
            constraints = result.fetchall()
            
            # 2. 删除student_id的唯一约束和索引
            for constraint in constraints:
                constraint_name = constraint[0]
                print(f"删除唯一约束: {constraint_name}")
                try:
                    db.execute(text(f"ALTER TABLE users DROP CONSTRAINT {constraint_name}"))
                    db.commit()
                    print(f"✅ 约束 {constraint_name} 删除成功")
                except Exception as e:
                    print(f"⚠️ 删除约束失败: {e}")
                    db.rollback()
            
            # 3. 删除唯一索引（如果存在）
            print("3. 删除唯一索引...")
            try:
                db.execute(text("DROP INDEX IF EXISTS ix_users_student_id"))
                db.commit()
                print("✅ 索引 ix_users_student_id 删除成功")
            except Exception as e:
                print(f"⚠️ 删除索引失败: {e}")
                db.rollback()
            
            # 4. 重新创建普通索引
            print("4. 重新创建普通索引...")
            try:
                db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_student_id ON users(student_id)"))
                db.commit()
                print("✅ 普通索引创建成功")
            except Exception as e:
                print(f"⚠️ 创建索引失败: {e}")
                db.rollback()
            
            # 5. 清理重复的空值（保留一个）
            print("5. 清理重复的空student_id...")
            try:
                # 查找有多少个空的student_id
                result = db.execute(text("SELECT COUNT(*) FROM users WHERE student_id IS NULL OR student_id = ''"))
                null_count = result.fetchone()[0]
                print(f"发现 {null_count} 个空的student_id")
                
                if null_count > 1:
                    # 为重复的空值设置唯一的临时值
                    db.execute(text("""
                        UPDATE users 
                        SET student_id = 'temp_' || id::text 
                        WHERE (student_id IS NULL OR student_id = '') 
                        AND id NOT IN (
                            SELECT MIN(id) 
                            FROM users 
                            WHERE student_id IS NULL OR student_id = ''
                        )
                    """))
                    db.commit()
                    print("✅ 重复空值已处理")
                
            except Exception as e:
                print(f"⚠️ 清理重复值失败: {e}")
                db.rollback()
            
            print("✅ student_id约束修复完成！")
            return True
            
        except Exception as e:
            print(f"❌ 修复过程失败: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ 连接数据库失败: {e}")
        return False

if __name__ == "__main__":
    success = fix_student_id_constraint()
    if success:
        print("🎉 修复完成，可以重启应用了")
    else:
        print("❌ 修复失败，请检查错误信息")
