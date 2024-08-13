from pydantic import BaseModel, ConfigDict

#Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool
    model_config = ConfigDict(from_attributes = True)

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: list[Article] = []
    model_config = ConfigDict(from_attributes = True)

# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes = True)
        
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
    
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    model_config = ConfigDict(from_attributes = True)