import hashlib
import os
from typing import List
from fastapi import Depends, FastAPI, HTTPException,Request,status
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from routers import files
import secrets

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

app.include_router(files.router)

origins = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_keys = [
    
]  # This is encrypted in the database


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def api_key_auth(api_key: str = Depends(oauth2_scheme)):

    db = SessionLocal()
    try:
        keys = db.query(models.Key).all()
        keys = [key.key for key in keys]
        if api_key not in keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden"
            )
    finally:
        db.close()


@app.post("/api/keys")
def create_key(db: SessionLocal = Depends(get_db)):
    key = models.Key()
    # Generate a random key 16 characters long
    key.key = secrets.token_urlsafe(16)
    print(key.key)
    db.add(key)
    db.commit()
    db.refresh(key)
    return key.key

@app.delete("/api/keys")
def delete_key(key:str,db: SessionLocal = Depends(get_db)):
    try:
        db.query(models.Key).filter(models.Key.key == key).delete()
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error deleting key"
        )
    return {"message": "Key succesfully deleted"}

@app.get("/protected", dependencies=[Depends(api_key_auth)])
def add_post() -> dict:
    return {
        "data": "You used a valid API key."
    }