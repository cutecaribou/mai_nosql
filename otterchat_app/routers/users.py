from fastapi     import APIRouter
from mongos.user import UserStorage
from models.user import UserModel

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
    inserted = await user_storage.create_new_user(
        username,
        user
    )
    return {
        'result': str(inserted)
    }


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
