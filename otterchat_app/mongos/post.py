from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api  import ServerApi

import pymongo

from models.post import PostModel

# class UserAlreadyExistsException(Exception):
#     pass

class PostStorage:
    def __init__(self, connection_url: str):
        self._url_ = connection_url
        self._client_ = AsyncIOMotorClient(self._url_, server_api=ServerApi('1'))

    async def get_all_posts(self):
        db = self._client_.otter_database
        collection = db.msg_collection

        cursor = collection.find().sort('sent_at', pymongo.DESCENDING)
        results = []
        for document in await cursor.to_list(length=100):
            del document['_id']
            print(document)
            results.append(document)
        return results

    async def get_posts_by_user(self, username: str):
        db = self._client_.otter_database
        collection = db.msg_collection

        cursor = collection.find({'author': username}).sort('sent_at', pymongo.DESCENDING)
        results = []
        for document in await cursor.to_list(length=100):
            del document['_id']
            print(document)
            results.append(document)
        return results

    async def send_post(self, username: str, text: str):
        db = self._client_.otter_database
        collection = db.msg_collection

        new_document = {
            'author' : username,
            'text'   : text,
            'sent_at': datetime.now()
        }

        result = await collection.insert_one(new_document)
        if result:
            return 'ok'
        else:
            return 'error'

    # async def create_new_user(self, username: str, user_data: UserModel):
    #     # Send a ping to confirm a successful connection
    #     try:
    #         await self._client_.admin.command('ping')
    #
    #         db = self._client_.otter_database
    #         collection = db.user_collection
    #
    #         old_document = await collection.find_one({'username': username})
    #         print(old_document)
    #
    #         if not old_document:
    #             new_document = {
    #                 "username": username,
    #             }
    #
    #             new_document.update(user_data)
    #
    #             result = await collection.insert_one(new_document)
    #
    #             print(result)
    #             return str(result)
    #         else:
    #             raise UserAlreadyExistsException(f'User with username {username} already exists')
    #     except Exception as e:
    #         print(e)
    #         raise e
    #
    # async def delete_user(self, username: str):
    #     db = self._client_.otter_database
    #     collection = db.user_collection
    #
    #     collection.delete_many({'username': username})
    #
    # async def get_user(self, username: str):
    #     db = self._client_.otter_database
    #     collection = db.user_collection
    #
    #     result = await collection.find_one({'username': username})
    #     if result:
    #         del result['_id']
    #
    #     return result
