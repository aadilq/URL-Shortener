from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "URL Shortener API is running!"}

