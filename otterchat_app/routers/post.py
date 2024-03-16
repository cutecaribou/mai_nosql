from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi     import APIRouter, Depends, HTTPException
from mongos.post import PostStorage
from models.post import PostModel
from models.post import IncomingPostModel
from typing      import Annotated
from fastapi     import Cookie


# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/post",
    tags=["posts"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


post_storage = PostStorage('mongodb://localhost:27017')

@router.get("/", tags=["posts"])
async def read_posts():
    return await post_storage.get_all_posts()

@router.get("/self", tags=["posts"])
async def read_posts(username: Annotated[str | None, Cookie()]):
    if username:
        return await post_storage.get_posts_by_user(username)
    else:
        return Response(status_code=401)

@router.get("/{username}", tags=["posts"])
async def read_posts(username: str):
    return await post_storage.get_posts_by_user(username)

@router.post("/", tags=["posts"])
async def new_post(data: IncomingPostModel, username: Annotated[str | None, Cookie()] = None):
    # return [{"username": "Rick"}, {"username": "Morty"}]
    if username:
        res = await post_storage.send_post(username, data.text)
        return {'status': res}
    else:
        return Response(status_code=401)
#
# @router.post("/{username}", tags=["users"])
# async def create_message(username: str, user: MessageModel):
#     # return [{"username": "Rick"}, {"username": "Morty"}]
#     # return await user_storage.get_all_users()
#     try:
#         inserted = await user_storage.create_new_user(
#             username,
#             user
#         )
#         return JSONResponse(
#             content={'message': 'Created new user'},
#             status_code=201
#         )
#     except UserAlreadyExistsException as e:
#         return JSONResponse(
#             content={'message': str(e)},
#             status_code=400
#         )
#
# @router.delete("/{username}", tags=["users"])
# async def del_user(username: str):
#     await user_storage.delete_user(username)
#     return Response(
#         status_code=200
#     )
#
# @router.get("/{username}", tags=["users"])
# async def read_user(username: str):
#     result = await user_storage.get_user(username)
#     if result:
#         return JSONResponse(
#             content=result,
#             status_code=200
#         )
#     else:
#         return Response(
#             status_code=404
#         )
#
#
# @router.get("/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}
