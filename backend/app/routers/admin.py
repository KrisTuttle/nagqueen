from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import UserResponse
from ..auth import get_admin_user
from ..models import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def list_users(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """List all users (admin only)."""
    return db.query(User).order_by(User.created_at.desc()).all()


@router.get("/users/pending", response_model=List[UserResponse])
def list_pending_users(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """List users awaiting approval (admin only)."""
    return db.query(User).filter(User.is_approved == False).order_by(User.created_at.desc()).all()


@router.post("/users/{user_id}/approve", response_model=UserResponse)
def approve_user(
    user_id: str,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Approve a pending user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_approved = True
    db.commit()
    db.refresh(user)
    return user


@router.post("/users/{user_id}/reject", status_code=status.HTTP_204_NO_CONTENT)
def reject_user(
    user_id: str,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Reject and delete a pending user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete admin user")

    db.delete(user)
    db.commit()


@router.post("/users/{user_id}/make-admin", response_model=UserResponse)
def make_admin(
    user_id: str,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Make a user an admin (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_admin = True
    user.is_approved = True
    db.commit()
    db.refresh(user)
    return user
