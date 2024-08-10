from fastapi import FastAPI
from router import (blog_get, blog_post, user,
                    article, product, file)
from auth import authentication
from db import models
from db.database import engine
from tools.exceptions import StoryException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Practice API",
    description="This is a practice API with FastAPI",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc"
)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})

models.Base.metadata.create_all(bind=engine)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if not os.path.exists("files"):
    os.makedirs("files")
    
app.mount("/files", StaticFiles(directory="files"), name="files")

