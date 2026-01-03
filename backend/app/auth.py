import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .models import User, OTPCode

settings = get_settings()
security = HTTPBearer()


def generate_otp() -> str:
    return "".join([str(secrets.randbelow(10)) for _ in range(6)])


def create_otp(db: Session, phone_number: str) -> str:
    # Invalidate any existing OTPs for this phone
    db.query(OTPCode).filter(
        OTPCode.phone_number == phone_number,
        OTPCode.used == False
    ).update({"used": True})

    code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiration_minutes)

    otp = OTPCode(
        phone_number=phone_number,
        code=code,
        expires_at=expires_at
    )
    db.add(otp)
    db.commit()

    return code


def verify_otp(db: Session, phone_number: str, code: str) -> bool:
    otp = db.query(OTPCode).filter(
        OTPCode.phone_number == phone_number,
        OTPCode.code == code,
        OTPCode.used == False,
        OTPCode.expires_at > datetime.utcnow()
    ).first()

    if not otp:
        return False

    otp.used = True
    db.commit()
    return True


def get_or_create_user(db: Session, phone_number: str) -> User:
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        # First user becomes admin and is auto-approved
        is_first_user = db.query(User).count() == 0
        user = User(
            phone_number=phone_number,
            is_admin=is_first_user,
            is_approved=is_first_user
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_approved_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user, but require approval."""
    user = get_current_user(credentials, db)
    if not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account pending approval"
        )
    return user


def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user, but require admin."""
    user = get_approved_user(credentials, db)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


def create_access_token(user_id: str) -> str:
    expires = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    payload = {
        "sub": user_id,
        "exp": expires
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
