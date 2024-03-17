from fastapi import Depends, FastAPI

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
from routers import post, user
import uvicorn

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=8000,
        host='0.0.0.0',
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips='*'
    )
