from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api  import ServerApi

from models.user import UserModel

class UserStorage:
    def __init__(self, connection_url: str):
        self._url_ = connection_url

    async def get_all_users(self):
        return {'hmmm': 'olololo'}

    async def create_new_user(self, username: str, user_data: UserModel):
        client = AsyncIOMotorClient(self._url_, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            await client.admin.command('ping')

            db = client.otter_database
            collection = db.user_collection
            document = {
                "username": username,
            }

            document.update(user_data)
            # result = await db.test_collection.insert_one(document)
            result = await collection.insert_one(document)

            # print(result)
            #
            # document = await collection.find_one({"Olenya": "wuv!"})
            # print(document)

            # print('----')

            # cursor = collection.find({"Olenya": "wuv!"}).sort('Olenya')
            # for document in await cursor.to_list(length=100):
            #     print(document)

            # print("Pinged your deployment. You successfully connected to MongoDB!")

            print(result)
            return str(result)
        except Exception as e:
            print(e)
            raise e
