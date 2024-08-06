from fastapi import FastAPI
from router import blog_get, blog_post, user, article
from db import models
from db.database import engine
from exceptions import StoryException
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})
    
        

models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("Server stopped by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
