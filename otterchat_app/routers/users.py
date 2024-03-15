from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi     import APIRouter
from mongos.user import UserStorage
from models.user import UserModel

from mongos.user import UserAlreadyExistsException

router = APIRouter(
    prefix="/user",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

user_storage = UserStorage('mongodb://localhost:27017')

@router.get("/", tags=["users"])
async def read_users():
    # return [{"username": "Rick"}, {"username": "Morty"}]
    return await user_storage.get_all_users()

@router.post("/{username}", tags=["users"])
async def create_user(username: str, user: UserModel):
    # return [{"username": "Rick"}, {"username": "Morty"}]
    # return await user_storage.get_all_users()
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


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
