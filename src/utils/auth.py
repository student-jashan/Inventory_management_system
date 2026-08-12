from fastapi import Header, HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.utils.settings import settings
from src.models.user import UserModel


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    # 1. Check whether Authorization header exists
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing"
        )

    # 2. Check Bearer format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format"
        )

    # 3. Extract token
    token = authorization.split(" ", 1)[1]

    # 4. Decode JWT
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY_VALUE,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # 5. Find user in database
    user = (
        db.query(UserModel)
        .filter(UserModel.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def require_authenticated_user(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user


def require_inventory_manager(
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role not in ["Admin", "Inventory Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Inventory Manager privileges required"
        )

    return current_user

def require_sales_user(
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role not in ["Admin", "Sales Executive"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Sales Executive privileges required"
        )

    return current_user