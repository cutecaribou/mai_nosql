from fastapi        import APIRouter, Depends, HTTPException
from mongos.post import PostStorage
from models.post import PostModel

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/post",
    tags=["posts"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


msg_storage = PostStorage('mongodb://localhost:27017')

@router.get("/", tags=["posts"])
async def read_messages():
    return await msg_storage.get_all_posts()

# async def read_users():
#     # return [{"username": "Rick"}, {"username": "Morty"}]
#     return await user_storage.get_all_users()
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
