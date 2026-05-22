import os
import psycopg2
import psycopg2.extras
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# --- Pydantic Models ---
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Configuration ---
SECRET_KEY = os.environ.get("SECRET_KEY", "b4a1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Router ---
router = APIRouter()

# --- Database Connection ---
def get_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "pingone"),
            user=os.environ.get("DB_USER", "ping"),
            password=os.environ.get("DB_PASSWORD", "ping"),
        )
        yield conn
    finally:
        if conn is not None:
            conn.close()

# --- Helper Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- API Endpoints ---
@router.post("/api/auth/login", response_model=Token)
async def login_for_access_token(form_data: User, db=Depends(get_db)):
    try:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (form_data.username,))
            user = cursor.fetchone()

            if not user or not verify_password(form_data.password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["username"], "last_login": user["last_login"].isoformat() if user["last_login"] else None},
                expires_delta=access_token_expires
            )

            # Update last login time
            cursor.execute("UPDATE tbl_users SET last_login = NOW() WHERE username = %s", (form_data.username,))
            db.commit()

            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"AN ERROR OCCURRED DURING LOGIN: {e}")
        raise HTTPException(status_code=500, detail=str(e))