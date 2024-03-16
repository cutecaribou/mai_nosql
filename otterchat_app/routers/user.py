from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi     import APIRouter
from fastapi     import Cookie
from mongos.user import UserStorage
from models.user import UserModel
from typing      import Annotated

from mongos.user import UserAlreadyExistsException

router = APIRouter(
    prefix="/user",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

user_storage = UserStorage('mongodb://localhost:27017')

@router.get("/self", tags=["users"])
async def read_user_self(username: Annotated[str | None, Cookie()] = None):
    if username:
        print('Current username:', username)
        return await user_storage.get_user(username)
    else:
        return Response(status_code=401)

@router.post("/login/{username}")
def login(username: str):
    result = user_storage.get_user(username)
    if result:
        resp = Response()
        resp.set_cookie(key="username", value=username)
        return resp
    else:
        return Response(status_code=404)
    # return {"message": "Come to the dark side, we have cookies"}

@router.get("/", tags=["users"])
async def read_users():
    # return [{"username": "Rick"}, {"username": "Morty"}]
    return await user_storage.get_all_users()

@router.post("/{username}", tags=["users"])
async def create_user(username: str, user: UserModel):
    # return [{"username": "Rick"}, {"username": "Morty"}]
    # return await user_storage.get_all_users()
    if username in ['self', 'all', 'any']:
        return JSONResponse(
            content={'message': 'Forbidden username'},
            status_code=400
        )
    else:
        try:
            inserted = await user_storage.create_new_user(
                username,
                user
            )
            return JSONResponse(
                content={'message': 'Created new user'},
                status_code=201
            )
        except UserAlreadyExistsException as e:
            return JSONResponse(
                content={'message': str(e)},
                status_code=400
            )

@router.delete("/{username}", tags=["users"])
async def del_user(username: str):
    await user_storage.delete_user(username)
    return Response(
        status_code=200
    )

@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    result = await user_storage.get_user(username)
    if result:
        return JSONResponse(
            content=result,
            status_code=200
        )
    else:
        return Response(
            status_code=404
        )
