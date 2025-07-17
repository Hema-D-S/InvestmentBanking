from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..models import UserCreate, UserOut, Token
from ..auth import get_password_hash, verify_password, create_access_token, get_user_by_username
from ..database import db
from jose import JWTError, jwt
from datetime import timedelta
import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    user_dict["is_active"] = True
    db.users.insert_one(user_dict)
    return UserOut(username=user.username, email=user.email, is_active=True)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=UserOut)
def read_users_me(current_user=Depends(get_current_user)):
    return UserOut(username=current_user.username, email=current_user.email, is_active=current_user.is_active) 