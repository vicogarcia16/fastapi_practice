from router.blog_post import required_functionality
from fastapi import APIRouter, status, Response, Depends
from typing import Optional
from enum import Enum

router = APIRouter(
    prefix="/blog",
    tags=["blog"],
    responses={404: {"description": "Not found"}},
)

# @router.get("/all")
# def get_all_blogs():
#     return {"message": "All blogs"}

@router.get("/all/",
         summary="Retrieve all blogs", 
         description="This api call simulates fetching all blogs",
         response_description="The list of available blogs")
def get_all_blogs(page=1, page_size: Optional[int] = None, 
                  req_parameter: dict = Depends(required_functionality)):
    return {"message": f"All {page_size} blogs on page {page}", "req": req_parameter}

@router.get("/{id}/comments/{comment_id}/", tags=["comment"])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retrieving a comment of a blog

    Args:
    - **id (int)**: _mandatory path parameter_
    - **comment_id (int)**: _mandatory path parameter_
    - **valid (bool)**: _optional query parameter_. Defaults to True.
    - **username (Optional[str])**: _optional query parameter_. Defaults to None.

    Returns:
    - **message (str)**: _response body_
    """
    return {"message": f"Blog {id} has comment {comment_id}, valid: {valid}, username: {username}"}

class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"

@router.get("/type/{blog_type}/")
def get_blog_type(blog_type: BlogType):
    return {"message": f"Blog type {blog_type}"}

@router.get("/{id}/", status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Blog id {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id {id}"}
