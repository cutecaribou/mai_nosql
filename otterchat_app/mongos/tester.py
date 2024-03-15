import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api  import ServerApi


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = "mongodb://localhost:27017"
    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')

        db = client.test_database
        collection = db.test_collection
        document = {
            "Olenya": "wuv!"
        }
        # result = await db.test_collection.insert_one(document)
        # result = await collection.insert_one(document)

        # print(result)
        #
        document = await collection.find_one({"Olenya": "wuv!"})
        print(document)

        print('----')

        cursor = collection.find({"Olenya": "wuv!"}).sort('Olenya')
        for document in await cursor.to_list(length=100):
            print(document)

        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


async def main():
    await ping_server()

if __name__ == '__main__':
    asyncio.run(main())
