from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi     import APIRouter, Depends, HTTPException
from mongos.post import PostStorage
from models.post import PostModel
from models.post import IncomingPostModel
from typing      import Annotated
from fastapi     import Cookie
import os


router = APIRouter(
    prefix="/post",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

mongo_user     = os.environ.get('MONGO_USER')
mongo_password = os.environ.get('MONGO_PASS')
mongo_host     = os.environ.get('MONGO_HOST'    , 'localhost')
mongo_port     = os.environ.get('MONGO_PORT'    , '27017')

if mongo_user and mongo_password:
    post_storage = PostStorage(f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}')
else:
    post_storage = PostStorage(f'mongodb://{mongo_host}:{mongo_port}')

@router.get("",  tags=["posts"])
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
