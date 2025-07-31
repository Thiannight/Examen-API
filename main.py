from fastapi import FastAPI, Request, HTTPException, status, Body
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from datetime import datetime
import base64

app = FastAPI()

posts_storage = []

#Q1
@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return PlainTextResponse(content="pong", status_code=200)

#Q2
@app.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="<h1>Welcome home!</h1>", status_code=200)

#Q3
@app.exception_handler(404)
def not_found_handler(request: Request, exc):
    return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)

# Q4
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

@app.post("/posts", response_model=List[Post], status_code=status.HTTP_201_CREATED)
def create_posts(new_posts: List[Post]):
    posts_storage.extend(new_posts)
    return posts_storage

#Q5
@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts_storage

#Q6
@app.put("/posts", response_model=List[Post])
def update_or_add_posts(updated_posts: List[Post]):
    for new_post in updated_posts:
        for i, existing_post in enumerate(posts_storage):
            if existing_post.title == new_post.title:
                posts_storage[i] = new_post
                break
        else:
            posts_storage.append(new_post)
    return posts_storage

#Bonus
VALID_USERNAME = "admin"
VALID_PASSWORD = "123456"

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        encoded_credentials = auth.encode("utf-8")
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode("utf-8")
        username, password = decoded_str

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return PlainTextResponse(content="pong", status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Invalid credentials")

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid authentication header format")
