from fastapi import APIRouter,HTTPException,Depends
from src.core.security import create_access_token
from src.core.dependencies import get_current_user
from src.services.auth_services import hash_password, verify_password
from src.app.schemas.auth_schema import AuthRequest,UserRegisterRequest

router = APIRouter()


USERS_DB = {}

@router.post("/register")
async def register(request: UserRegisterRequest):

    if request.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash,email = hash_password(request.password),request.email

    USERS_DB[email] = {
        "email": email,
        "password_hash": password_hash
    }
    return {"user": USERS_DB[email], "message": "User registered successfully"}

@router.post("/login")
async def login(request: AuthRequest):
    user = USERS_DB.get(request.username)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
