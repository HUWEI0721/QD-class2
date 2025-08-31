#!/usr/bin/env python3
"""
数据库初始化脚本
创建一些基础的测试数据
"""

from datetime import datetime, timedelta
from app.database import SessionLocal, engine
from app.models import Base, User, Activity, MediaItem, Comment, Notification
from app.auth import get_password_hash

def init_database():
    """初始化数据库并添加测试数据"""
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 检查是否已经有数据
        if db.query(User).count() > 0:
            print("数据库已有数据，跳过初始化")
            return
        
        print("开始初始化数据库...")
        
        # 创建测试用户
        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("123456"),
                full_name="管理员",
                role="admin",
                is_active=True
            ),
            User(
                username="teacher",
                email="teacher@example.com",
                hashed_password=get_password_hash("123456"),
                full_name="张老师",
                role="teacher",
                phone="13800138000",
                hometown="北京市",
                bio="计算机科学与技术专业教师",
                is_active=True
            ),
            User(
                username="student1",
                email="student1@example.com",
                hashed_password=get_password_hash("123456"),
                full_name="李明",
                student_id="2021001",
                role="student",
                phone="13800138001",
                qq="123456789",
                wechat="liming_wx",
                dormitory="1号楼101",
                hometown="上海市",
                bio="热爱编程，喜欢篮球",
                is_active=True
            ),
            User(
                username="student2",
                email="student2@example.com",
                hashed_password=get_password_hash("123456"),
                full_name="王小红",
                student_id="2021002",
                role="student",
                phone="13800138002",
                qq="987654321",
                wechat="wangxh_wx",
                dormitory="1号楼102",
                hometown="广州市",
                bio="喜欢阅读和旅行",
                is_active=True
            ),
            User(
                username="student3",
                email="student3@example.com",
                hashed_password=get_password_hash("123456"),
                full_name="陈建国",
                student_id="2021003",
                role="student",
                phone="13800138003",
                qq="555666777",
                wechat="chenjianguo_wx",
                dormitory="1号楼103",
                hometown="深圳市",
                bio="喜欢音乐和电影",
                is_active=True
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print(f"创建了 {len(users)} 个用户")
        
        # 创建测试活动
        activities = [
            Activity(
                title="班级聚餐活动",
                description="大家一起聚餐，增进友谊，分享学习和生活中的趣事",
                activity_date=datetime.now() + timedelta(days=7),
                location="学校食堂三楼",
                creator_id=2  # 张老师创建
            ),
            Activity(
                title="期末复习动员会",
                description="为期末考试做准备，互相鼓励，分享复习方法和经验",
                activity_date=datetime.now() + timedelta(days=3),
                location="教学楼A101",
                creator_id=2  # 张老师创建
            ),
            Activity(
                title="春游踏青",
                description="春天来了，我们一起去公园踏青，欣赏美丽的春景",
                activity_date=datetime.now() + timedelta(days=30),
                location="市中心公园",
                creator_id=3  # 李明创建
            ),
            Activity(
                title="班级篮球比赛",
                description="举办班级内部篮球比赛，锻炼身体，增强团队合作精神",
                activity_date=datetime.now() - timedelta(days=5),
                location="学校篮球场",
                creator_id=4  # 王小红创建
            )
        ]
        
        for activity in activities:
            db.add(activity)
        
        db.commit()
        print(f"创建了 {len(activities)} 个活动")
        
        print("数据库初始化完成!")
        print("\n测试账号:")
        print("管理员: admin / 123456")
        print("教师: teacher / 123456") 
        print("学生1: student1 / 123456")
        print("学生2: student2 / 123456")
        print("学生3: student3 / 123456")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
