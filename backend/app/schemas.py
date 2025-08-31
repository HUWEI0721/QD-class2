from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from .models import UserRole, MediaType


# 用户相关schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    student_id: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    qq: Optional[str] = None
    wechat: Optional[str] = None
    dormitory: Optional[str] = None
    hometown: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少为6位')
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    qq: Optional[str] = None
    wechat: Optional[str] = None
    dormitory: Optional[str] = None
    hometown: Optional[str] = None
    avatar_url: Optional[str] = None


class User(UserBase):
    id: int
    role: UserRole
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


# 活动相关schemas
class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_date: Optional[datetime] = None
    location: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    title: Optional[str] = None


class Activity(ActivityBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    creator: User

    class Config:
        from_attributes = True


# 媒体文件相关schemas
class MediaItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MediaItemCreate(MediaItemBase):
    activity_id: int


class MediaItem(MediaItemBase):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: Optional[int] = None
    media_type: MediaType
    activity_id: int
    uploader_id: int
    upload_time: datetime
    views_count: int = 0
    uploader: User
    activity: Activity

    class Config:
        from_attributes = True


# 评论相关schemas
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    media_item_id: int
    parent_id: Optional[int] = None


class Comment(CommentBase):
    id: int
    media_item_id: int
    author_id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: User
    replies: List['Comment'] = []

    class Config:
        from_attributes = True


# 通知相关schemas
class NotificationBase(BaseModel):
    title: str
    message: str


class NotificationCreate(NotificationBase):
    user_id: int
    related_comment_id: Optional[int] = None


class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool = False
    related_comment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# 更新Comment模型以解决前向引用
Comment.model_rebuild()
