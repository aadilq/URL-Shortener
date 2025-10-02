from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

## Request Model - Defines what type of data we expect from the user
class URL_Request(BaseModel):
    url: HttpUrl ## pydantic HttpUrl allows us to validate if the url is a proper url

## Response Model - Defines what we want to send back to the user
class URL_Reponse(BaseModel):
    original_url: str
    short_code: str
    shorten_url: str


@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}


