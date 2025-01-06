from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from router import (blog_get, blog_post, user,
                    article, product, file, dependencies)
from templates import templates
from auth import authentication
from db import models
from db.database import engine
from tools.exceptions import StoryException
from tools.client import html
from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os, time

app = FastAPI(
    title="Practice API",
    description="This is a practice API with FastAPI",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc"
)
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

if not os.getenv('PRODUCTION'):
    @app.get("/chat/", include_in_schema=False)
    async def chat():
        return HTMLResponse(html)
    
    clients = []
    messages = []

    @app.websocket("/chat/")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        clients.append(websocket)
        for message in messages:
            await websocket.send_text(message)
        try:
            while True:
                data = await websocket.receive_text()
                messages.append(data)
                for client in clients:
                    await client.send_text(data)
        except WebSocketDisconnect:
            clients.remove(websocket)

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})

models.Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def add_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response

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
app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")
