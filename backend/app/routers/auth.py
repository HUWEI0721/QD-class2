from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token, User as UserSchema
from ..auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user
)
from ..config import settings

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserSchema, summary="用户注册")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    - 检查用户名和邮箱是否已存在
    - 创建新用户账户
    """
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查学号是否已存在（如果提供了学号）
    if user.student_id:
        db_user = db.query(User).filter(User.student_id == user.student_id).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已存在"
            )
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        student_id=user.student_id,
        bio=user.bio,
        phone=user.phone,
        qq=user.qq,
        wechat=user.wechat,
        dormitory=user.dormitory,
        hometown=user.hometown
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token, summary="用户登录")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    - 验证用户名和密码
    - 返回JWT访问令牌
    """
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserSchema, summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户的详细信息
    """
    return current_user


@router.post("/logout", summary="用户登出")
async def logout():
    """
    用户登出（客户端需要删除本地存储的token）
    """
    return {"message": "登出成功"}
