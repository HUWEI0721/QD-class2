from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class MediaType(str, enum.Enum):
    """媒体类型枚举"""
    PHOTO = "photo"
    VIDEO = "video"


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    student_id = Column(String(20), index=True, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    avatar_url = Column(String(255))
    bio = Column(Text)
    phone = Column(String(20))
    qq = Column(String(20))
    wechat = Column(String(50))
    dormitory = Column(String(50))
    hometown = Column(String(100))
    # 新增字段（可选，兼容旧数据库）
    gender = Column(String(10), nullable=True)  # male, female, other
    birthday = Column(DateTime, nullable=True)
    interests = Column(Text, nullable=True)  # 兴趣爱好
    address = Column(String(200), nullable=True)  # 地址
    emergency_contact = Column(String(100), nullable=True)  # 紧急联系人
    emergency_phone = Column(String(20), nullable=True)  # 紧急联系电话
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    activities = relationship("Activity", back_populates="creator")
    media_items = relationship("MediaItem", back_populates="uploader")
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="user")


class Activity(Base):
    """活动模型"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    activity_date = Column(DateTime(timezone=True))
    location = Column(String(200))
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    creator = relationship("User", back_populates="activities")
    media_items = relationship("MediaItem", back_populates="activity")


class MediaItem(Base):
    """媒体文件模型（照片和视频）"""
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    media_type = Column(Enum(MediaType), nullable=False)
    title = Column(String(200))
    description = Column(Text)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    uploader_id = Column(Integer, ForeignKey("users.id"))
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    views_count = Column(Integer, default=0)

    # 关系
    activity = relationship("Activity", back_populates="media_items")
    uploader = relationship("User", back_populates="media_items")
    comments = relationship("Comment", back_populates="media_item")


class Comment(Base):
    """评论模型"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    media_item_id = Column(Integer, ForeignKey("media_items.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"))  # 用于回复评论
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    media_item = relationship("MediaItem", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id])
    replies = relationship("Comment", overlaps="parent")


class Notification(Base):
    """通知模型"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_read = Column(Boolean, default=False)
    related_comment_id = Column(Integer, ForeignKey("comments.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    user = relationship("User", back_populates="notifications")
    related_comment = relationship("Comment")
