from typing import Optional, List
from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from tools.custom_log import log
import time

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}}
)

products = ['watch', 'camera', 'phone']

async def time_consuming_operation():
    time.sleep(5)
    return "Done"


@router.post("/new/")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/all/")
async def get_all_products():
    await time_consuming_operation()
    log("MyAPI", "Call to get all products")
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response

@router.get("/withheader/")
def get_products(response: Response, 
                 custom_header: Optional[List[str]] = Header(None),
                 test_cookie: Optional[str] = Cookie(None)):
    if custom_header:
        response.headers['custom_response_header'] = ' , '.join(custom_header)
    return {"data": products, "custom_header": custom_header, 'my_cookie': test_cookie}

@router.get("/{id}/", responses={
    404: {
        "content": {
            "text/plain": {
                "example": "Product not available"
                }
            },
          "description": "A cleartext error message" 
        },
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
                }
            },
        "description": "Returns the HTML for an object" 
        }
    })
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(content=out, media_type="text/plain", status_code=404)
    else:
        product = products[id]
        out = f"""
            <head>
                <style>
                .product {{
                    width: 500px;
                    height: 30px;
                    border: 2px inset green;
                    background-color: lightblue;
                    text-align: center;
                }}
                </style>
            </head>
            <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type="text/html")