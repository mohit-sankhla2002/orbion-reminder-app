from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from bcrypt import gensalt, hashpw, checkpw

# JWT configuration
SECRET_KEY = "WupNFdl4VNWgRR6kg6QBx2SI1en18q0H9MWD9fmiIqo="  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

users_db = {}

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Pydantic models
class User_login(BaseModel):
    username: str
    password: str

class User_register(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    contactNo: int

class ChangePassword(BaseModel):
    username: str
    email: str
    previouspassword: str  # Fixed typo from 'perviouspassword'
    newpassword : str   

class ForgotPassword(BaseModel):
    username: str
    email: str
    otp: int
    newpassword: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password):
    return hashpw(password.encode('utf-8'), gensalt())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# Endpoints
@auth_router.post("/login", response_model=Token)
async def login_user(user: User_login):
    db_user = users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register")
async def registration(user: User_register):
    print(user)
    if user.email in [u["email"] for u in users_db.values()]:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    users_db[user.email] = {
        "username": user.email,  # Using email as username for simplicity
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "password": hashed_password,
        "contactNo": user.contactNo
    }
    return user.model_dump()

@auth_router.put("/change-password")
async def update_password(
    changepassword: ChangePassword,
    current_user: dict = Depends(get_current_user)
):
    if current_user["username"] != changepassword.username or current_user["email"] != changepassword.email:
        raise HTTPException(status_code=403, detail="Not authorized to change this user's password")
    if not verify_password(changepassword.previouspassword, current_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect previous password")
    hashed_password = get_password_hash(changepassword.newpassword)  # In real app, use new password
    users_db[current_user["username"]]["password"] = hashed_password
    return {"changepassword": changepassword.model_dump()}

@auth_router.post("/forgot-password")
async def forgot_password(password: ForgotPassword):
    user = users_db.get(password.email)
    if not user or user["username"] != password.email:
        raise HTTPException(status_code=404, detail="User not found")
    # Simulate OTP verification (in production, validate OTP)
    hashed_password = get_password_hash(password.newpassword)
    users_db[password.email]["password"] = hashed_password
    return password.model_dump()

@auth_router.put("/reset-password")  # Fixed typo from 'reset-paasword'
async def reset_password(
    resetpassword: ChangePassword,
    current_user: dict = Depends(get_current_user)
):
    if current_user["username"] != resetpassword.username or current_user["email"] != resetpassword.email:
        raise HTTPException(status_code=403, detail="Not authorized to reset this user's password")
    hashed_password = get_password_hash(resetpassword.previouspassword)  # In real app, use new password
    users_db[current_user["username"]]["password"] = hashed_password
    return {"changepassword": resetpassword.model_dump()}