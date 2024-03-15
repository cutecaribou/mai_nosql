from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api  import ServerApi

from models.user import UserModel

class UserAlreadyExistsException(Exception):
    pass

class UserStorage:
    def __init__(self, connection_url: str):
        self._url_ = connection_url

    async def get_all_users(self):
        client = AsyncIOMotorClient(self._url_, server_api=ServerApi('1'))

        db = client.otter_database
        collection = db.user_collection

        cursor = collection.find().sort('username')
        results = []
        for document in await cursor.to_list(length=100):
            del document['_id']
            print(document)
            results.append(document)
        return results

    async def create_new_user(self, username: str, user_data: UserModel):
        client = AsyncIOMotorClient(self._url_, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            await client.admin.command('ping')

            db = client.otter_database
            collection = db.user_collection

            old_document = await collection.find_one({'username': username})
            print(old_document)

            if not old_document:
                new_document = {
                    "username": username,
                }

                new_document.update(user_data)

                result = await collection.insert_one(new_document)

                print(result)
                return str(result)
            else:
                raise UserAlreadyExistsException(f'User with username {username} already exists')
        except Exception as e:
            print(e)
            raise e

    async def delete_user(self, username: str):
        client = AsyncIOMotorClient(self._url_, server_api=ServerApi('1'))

        db = client.otter_database
        collection = db.user_collection

        collection.delete_many({'username': username})
