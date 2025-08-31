from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import User as UserSchema, UserUpdate
from ..auth import get_current_active_user

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
