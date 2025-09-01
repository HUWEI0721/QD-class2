from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import User as UserSchema, UserUpdate, PasswordChange
from ..auth import get_current_active_user, get_password_hash, verify_password
import os
import uuid
from ..config import settings

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/", response_model=List[UserSchema], summary="获取所有用户")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取所有用户列表
    - 支持分页查询
    - 需要登录权限
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/me", response_model=UserSchema, summary="获取当前用户信息")
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前登录用户的详细信息
    """
    return current_user


@router.put("/me", response_model=UserSchema, summary="更新当前用户信息")
async def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新当前用户的个人信息
    """
    # 更新用户信息
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/{user_id}", response_model=UserSchema, summary="获取指定用户信息")
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定用户的详细信息
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user


@router.get("/stats/summary", summary="获取用户统计信息")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户相关的统计信息
    """
    total_users = db.query(User).count()
    
    # 按角色统计
    students_count = db.query(User).filter(User.role == "student").count()
    teachers_count = db.query(User).filter(User.role == "teacher").count()
    admins_count = db.query(User).filter(User.role == "admin").count()
    
    # 活跃用户统计
    active_users = db.query(User).filter(User.is_active == True).count()
    
    return {
        "total_users": total_users,
        "students_count": students_count,
        "teachers_count": teachers_count,
        "admins_count": admins_count,
        "active_users": active_users,
        "dormitories": []  # 可以后续扩展宿舍统计
    }


@router.post("/avatar", response_model=dict, summary="上传用户头像")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    上传用户头像
    """
    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能上传图片文件"
        )
    
    # 检查文件大小 (2MB)
    if file.size > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图片大小不能超过2MB"
        )
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"avatar_{current_user.id}_{uuid.uuid4()}{file_extension}"
    
    # 确保头像目录存在
    avatar_dir = f"{settings.upload_dir}/avatars"
    os.makedirs(avatar_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(avatar_dir, unique_filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 更新用户头像URL
    avatar_url = f"avatars/{unique_filename}"
    current_user.avatar_url = avatar_url
    db.commit()
    
    return {"avatar_url": avatar_url, "message": "头像上传成功"}


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    修改用户密码
    """
    # 验证当前密码
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 更新密码
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "密码修改成功"}
