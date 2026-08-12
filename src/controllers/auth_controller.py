from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.user import UserModel
from src.dtos.auth_dto import UserRegister,UserLogin
from src.utils.security import hash_password,verify_password
from src.utils.jwt_handler import create_access_token

def register_user(user: UserRegister, db: Session):

    # 1. Check whether email already exists
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash the password
    hashed_password = hash_password(user.password)

    # 3. Create user
    new_user = UserModel(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    # 4. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Return user
    return new_user


def login_user(user: UserLogin, db: Session):

    # 1. Find user
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. Verify password
    password_valid = verify_password(
        user.password,
        existing_user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Create JWT
    access_token = create_access_token(
        data={
            "sub": str(existing_user.id),
            "email": existing_user.email,
            "role": existing_user.role,
            "name": existing_user.full_name
        }
    )

    # 4. Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }