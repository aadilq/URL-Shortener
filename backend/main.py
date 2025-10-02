from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import string
import random

app = FastAPI()

## Request Model - Defines what type of data we expect from the user
class URL_Request(BaseModel):
    url: HttpUrl ## pydantic HttpUrl allows us to validate if the url is a proper url

## Response Model - Defines what we want to send back to the user
class URL_Response(BaseModel):
    original_url: str
    short_code: str
    shorten_url: str

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))




@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}





