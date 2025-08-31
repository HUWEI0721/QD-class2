from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, MediaItem, Activity
from ..schemas import MediaItem as MediaItemSchema, MediaItemCreate
from ..auth import get_current_active_user
from ..config import settings
import os
import uuid
from PIL import Image

router = APIRouter(prefix="/media", tags=["媒体管理"])


@router.get("/", response_model=List[MediaItemSchema], summary="获取媒体文件列表")
async def get_media_items(
    skip: int = 0,
    limit: int = 100,
    activity_id: Optional[int] = None,
    media_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取媒体文件列表
    - 支持按活动筛选
    - 支持按媒体类型筛选
    """
    query = db.query(MediaItem)
    
    if activity_id:
        query = query.filter(MediaItem.activity_id == activity_id)
    
    if media_type:
        query = query.filter(MediaItem.media_type == media_type)
    
    media_items = query.offset(skip).limit(limit).all()
    return media_items


@router.post("/upload", response_model=MediaItemSchema, summary="上传媒体文件")
async def upload_media_file(
    activity_id: int = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    上传媒体文件
    """
    # 验证活动是否存在
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="活动不存在"
        )
    
    # 验证文件类型
    if not file.content_type.startswith(('image/', 'video/')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持图片和视频文件"
        )
    
    # 验证文件大小
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小超过限制"
        )
    
    # 确定媒体类型
    media_type = "photo" if file.content_type.startswith('image/') else "video"
    
    # 生成唯一文件名
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 确定文件保存路径
    if media_type == "photo":
        file_dir = f"{settings.upload_dir}/photos"
    else:
        file_dir = f"{settings.upload_dir}/videos"
    
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 创建数据库记录（保存相对于uploads目录的路径）
    relative_path = f"{media_type}s/{unique_filename}"  # photos/xxx.jpg 或 videos/xxx.mp4
    
    db_media = MediaItem(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=relative_path,  # 保存相对路径，前端可以拼接为 /uploads/photos/xxx.jpg
        file_size=file.size,
        media_type=media_type,
        title=title,
        description=description,
        activity_id=activity_id,
        uploader_id=current_user.id
    )
    
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    
    return db_media


@router.get("/{media_id}", response_model=MediaItemSchema, summary="获取媒体文件详情")
async def get_media_item(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定媒体文件的详细信息
    """
    media_item = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 增加浏览次数
    media_item.views_count += 1
    db.commit()
    
    return media_item


@router.delete("/{media_id}", summary="删除媒体文件")
async def delete_media_item(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除指定媒体文件
    """
    media_item = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 检查权限：只有上传者或管理员可以删除
    if media_item.uploader_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此文件"
        )
    
    # 删除文件
    full_file_path = os.path.join(settings.upload_dir, media_item.file_path)
    if os.path.exists(full_file_path):
        os.remove(full_file_path)
    
    # 删除数据库记录
    db.delete(media_item)
    db.commit()
    
    return {"message": "媒体文件删除成功"}


@router.get("/stats/summary", summary="获取媒体统计信息")
async def get_media_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取媒体相关的统计信息
    """
    total_media = db.query(MediaItem).count()
    total_photos = db.query(MediaItem).filter(MediaItem.media_type == "photo").count()
    total_videos = db.query(MediaItem).filter(MediaItem.media_type == "video").count()
    
    # 计算总浏览量
    from sqlalchemy import func
    total_views = db.query(func.sum(MediaItem.views_count)).scalar() or 0
    
    return {
        "total_media": total_media,
        "total_photos": total_photos,
        "total_videos": total_videos,
        "total_views": total_views
    }
