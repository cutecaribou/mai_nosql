from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi     import APIRouter, Depends, HTTPException
from mongos.post import PostStorage
from models.post import PostModel
from models.post import IncomingPostModel
from typing      import Annotated
from fastapi     import Cookie


router = APIRouter(
    prefix="/post",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


post_storage = PostStorage('mongodb://localhost:27017')

@router.get("/", tags=["posts"])
async def read_all_posts():
    return await post_storage.get_all_posts()

@router.get("/self", tags=["posts"])
async def read_own_posts(username: Annotated[str | None, Cookie()]):
    if username:
        return await post_storage.get_posts_by_user(username)
    else:
        return Response(status_code=401)

@router.get("/{username}", tags=["posts"])
async def read_posts_of_a_user(username: str):
    return await post_storage.get_posts_by_user(username)

@router.post("/", tags=["posts"])
async def new_post(data: IncomingPostModel, username: Annotated[str | None, Cookie()] = None):
    if username:
        res = await post_storage.send_post(username, data.text)
        return {'status': res}
    else:
        return Response(status_code=401)
