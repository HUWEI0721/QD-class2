from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Activity
from ..schemas import Activity as ActivitySchema, ActivityCreate, ActivityUpdate
from ..auth import get_current_active_user

router = APIRouter(prefix="/activities", tags=["活动管理"])


@router.get("/", response_model=List[ActivitySchema], summary="获取活动列表")
async def get_activities(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取活动列表
    - 支持分页查询
    - 支持状态筛选
    """
    query = db.query(Activity)
    
    # 这里可以添加状态筛选逻辑
    # if status_filter:
    #     query = query.filter(Activity.status == status_filter)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.post("/", response_model=ActivitySchema, summary="创建活动")
async def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新的活动
    """
    db_activity = Activity(
        **activity.model_dump(),
        creator_id=current_user.id
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/{activity_id}", response_model=ActivitySchema, summary="获取活动详情")
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定活动的详细信息
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="活动不存在"
        )
    return activity


@router.put("/{activity_id}", response_model=ActivitySchema, summary="更新活动")
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新活动信息
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="活动不存在"
        )
    
    # 检查权限：只有创建者或管理员可以修改
    if activity.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此活动"
        )
    
    # 更新活动信息
    update_data = activity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}", summary="删除活动")
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除指定活动
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="活动不存在"
        )
    
    # 检查权限：只有创建者或管理员可以删除
    if activity.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此活动"
        )
    
    db.delete(activity)
    db.commit()
    
    return {"message": "活动删除成功"}


@router.get("/stats/summary", summary="获取活动统计信息")
async def get_activity_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取活动相关的统计信息
    """
    from datetime import datetime
    
    total_activities = db.query(Activity).count()
    
    # 统计即将开始的活动（活动时间在未来）
    now = datetime.utcnow()
    upcoming_activities = db.query(Activity).filter(Activity.activity_date > now).count()
    
    # 统计已完成的活动（活动时间在过去）
    completed_activities = db.query(Activity).filter(Activity.activity_date <= now).count()
    
    return {
        "total_activities": total_activities,
        "upcoming_activities": upcoming_activities,
        "completed_activities": completed_activities,
        "ongoing_activities": 0  # 可以根据具体业务逻辑计算
    }
