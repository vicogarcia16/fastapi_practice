from fastapi import FastAPI
from router import (blog_get, blog_post, user,
                    article, product, file)
from auth import authentication
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get("/")
def index():
    return {"message": "Hello World"}

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
