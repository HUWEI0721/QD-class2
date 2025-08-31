from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Comment, MediaItem, Notification
from ..schemas import Comment as CommentSchema, CommentCreate
from ..auth import get_current_active_user

router = APIRouter(prefix="/comments", tags=["评论管理"])


@router.get("/media/{media_id}", response_model=List[CommentSchema], summary="获取媒体文件的评论")
async def get_media_comments(
    media_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定媒体文件的评论列表
    """
    # 验证媒体文件是否存在
    media_item = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    comments = db.query(Comment).filter(
        Comment.media_item_id == media_id,
        Comment.parent_id.is_(None)  # 只获取顶级评论
    ).offset(skip).limit(limit).all()
    
    return comments


@router.post("/", response_model=CommentSchema, summary="创建评论")
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新评论
    """
    # 验证媒体文件是否存在
    media_item = db.query(MediaItem).filter(MediaItem.id == comment.media_item_id).first()
    if not media_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 如果是回复评论，验证父评论是否存在
    if comment.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment.parent_id).first()
        if not parent_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )
    
    # 创建评论
    db_comment = Comment(
        content=comment.content,
        media_item_id=comment.media_item_id,
        author_id=current_user.id,
        parent_id=comment.parent_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # 创建通知
    await create_comment_notification(db, db_comment, media_item, current_user)
    
    return db_comment


@router.get("/{comment_id}", response_model=CommentSchema, summary="获取评论详情")
async def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取指定评论的详细信息
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    return comment


@router.delete("/{comment_id}", summary="删除评论")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除指定评论
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    
    # 检查权限：只有评论作者或管理员可以删除
    if comment.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此评论"
        )
    
    # 删除评论及其回复
    db.query(Comment).filter(Comment.parent_id == comment_id).delete()
    db.delete(comment)
    db.commit()
    
    return {"message": "评论删除成功"}


async def create_comment_notification(
    db: Session, 
    comment: Comment, 
    media_item: MediaItem, 
    author: User
):
    """
    创建评论通知
    """
    # 通知媒体文件的上传者（如果不是自己评论自己的文件）
    if media_item.uploader_id != author.id:
        notification = Notification(
            title="新评论",
            message=f"{author.full_name} 评论了您的 {media_item.title or media_item.original_filename}",
            user_id=media_item.uploader_id,
            related_comment_id=comment.id
        )
        db.add(notification)
    
    # 如果是回复评论，通知被回复的用户
    if comment.parent_id:
        parent_comment = db.query(Comment).filter(Comment.id == comment.parent_id).first()
        if parent_comment and parent_comment.author_id != author.id:
            notification = Notification(
                title="评论回复",
                message=f"{author.full_name} 回复了您的评论",
                user_id=parent_comment.author_id,
                related_comment_id=comment.id
            )
            db.add(notification)
    
    db.commit()
