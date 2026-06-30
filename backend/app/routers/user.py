from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# ---------------- REGISTER ---------------- #

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# ---------------- LOGIN ---------------- #

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print("Username:", form_data.username)

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    print("User Found:", db_user)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    print("Stored Password:", db_user.password)

    result = verify_password(
        form_data.password,
        db_user.password
    )

    print("Password Match:", result)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"sub": str(db_user.id)}
    )

    print("Generated Token:", token)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------------- PROFILE ---------------- #

@router.get("/profile")
def profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


