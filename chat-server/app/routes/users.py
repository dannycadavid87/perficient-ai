from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user import create_user, get_user_by_username, verify_password, get_user_info
from app.db.session import SessionLocal
from app.auth.jwt_interpreter import create_access_token, oauth2_scheme
from app.services.redis_session import get_redis
from app.auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import datetime

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut, summary="Register a new User")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)

@router.post("/login", summary="Authenticates a User")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), redis=Depends(get_redis)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": str(user.id)})
    # Store token in Redis for session management
    await redis.set(access_token, str(user.id), ex=3600)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", summary="Revoke the session of the authenticated User")
async def logout(token: str = Depends(oauth2_scheme), redis=Depends(get_redis)):
    await redis.delete(token)
    return {"msg": "Logged out"}

@router.get("/me", response_model=UserOut, summary="Get the information of the authenticated User")
def me(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_info(db, int(current_user["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user.__dict__)
