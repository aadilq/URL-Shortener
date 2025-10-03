from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import string
import random

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
    short_code = generate_short_code()

    while short_code in url_database:
        short_code = generate_short_code
    

    url_database[short_code] = str(request.url)

    return{
        "short_code": short_code, 
        "original_url": str(request.url),
        "short_url" : f"http://localhost:8000/{short_code}"
    }

## Getting the short code and redirecting it the original URL
@app.get("/{short_code}") 
def redirect_to_url(short_code: str):
    if short_code not in url_database:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    original_url = url_database(short_code)

    return{
        "short_code" : short_code, 
        "original_url" : original_url, 
        "message": "Redirecting to this URL"
    }





