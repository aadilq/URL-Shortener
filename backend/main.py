from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class URL_Request(BaseModel):
    url: HttpUrl

## Defines what we want to send back to the user

@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}


