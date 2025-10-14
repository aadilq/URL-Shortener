from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
import string
import random

from database import database_engine, Base, Sessionlocal
import models

# Create all tables
Base.metadata.create_all(bind=database_engine)

app = FastAPI()

url_database = {}

## Request Model - Defines what type of data we expect from the user
class URL_Request(BaseModel):
    url: HttpUrl ## pydantic HttpUrl allows us to validate if the url is a proper url

## Response Model - Defines what we want to send back to the user
class URL_Response(BaseModel):
    short_code: str
    original_url: str
    shorten_url: str

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))




@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}


@app.post("/api/shorten_url", response_model=URL_Response)
def shorten_url(request: URL_Request):

    db = Sessionlocal()


    try:
        short_code = generate_short_code()

        while(db.query(models.URL).filter(models.URL.short_code == short_code)).first():
            short_code = generate_short_code()
    
        db_url = models.URL(
            short_code = short_code, 
            original_url = str(request.url),
            click_count = 0
    )

        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        return{
            "short_code": short_code, 
            "original_url": str(request.url),
            "shorten_url" : f"http://localhost:8000/{short_code}"
        }
    finally:
        db.close()

## Getting the short code and redirecting it the original URL
@app.get("/{short_code}") 
def redirect_to_url(short_code: str):

    db = Sessionlocal()

    try:
        url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()

        if not url_entry:
            raise HTTPException(status_code=404, detail="Short URL not found")
    
        url_entry.click_count += 1
        db.commit()
        return RedirectResponse(url=url_entry.original_url)
    finally:
        db.close()

@app.get("/api/stats/{short_code}")
def get_stats(short_code: str):
    db = Sessionlocal()

    try:
        url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()

        if not url_entry:
            raise HTTPException(status_code=404, detail="Short URL not found")
    
        return{
            "short_code": url_entry.short_code,
            "original_url": url_entry.original_url,
            "click_count": url_entry.click_count,
            "created_at": url_entry.created_at
        }
    finally:
        db.close()


## Activating the virtual environment 
# - source .venv/bin/activate


## Starting (or restarting) the FastAPI server 
# - uvicorn main:app --reload 

 





