import asyncio

import motor.motor_asyncio

from BlynkBot.main import mongo_url

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
client.get_io_loop = asyncio.get_running_loop
db = client.BlynkBot
users = db['users']


async def get_user(user_id):
    return await users.find_one({"user_id": user_id})


async def check_user(user_id):
    return await users.find_one({"user_id": user_id, "email": {"$exists": True}})


async def add_email(user, email):
    await users.update_one(user, {'$set': {'email': email}})


async def add_user(user_id):
    if not await get_user(user_id):
        await users.insert_one({"user_id": user_id})
