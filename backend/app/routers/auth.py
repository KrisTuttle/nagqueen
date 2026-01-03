from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import OTPRequest, OTPVerify, Token, UserResponse
from ..auth import create_otp, verify_otp, get_or_create_user, create_access_token, get_current_user
from ..sms import send_otp
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/request-otp")
def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    code = create_otp(db, request.phone_number)
    success = send_otp(request.phone_number, code)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp", response_model=Token)
def verify_otp_endpoint(request: OTPVerify, db: Session = Depends(get_db)):
    if not verify_otp(db, request.phone_number, request.code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )

    user = get_or_create_user(db, request.phone_number)
    token = create_access_token(user.id)

    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
