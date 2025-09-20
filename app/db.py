from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()


async def startup_db_client(app: FastAPI):
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONOGO_DB_NAME")

    app.mongodb_client = AsyncIOMotorClient(mongodb_uri)
    app.mongodb = app.mongodb_client.get_database(database_name)
    print(f"MongoDB connected to database: {database_name}")


async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()
    print("Database disconnected.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield
    await shutdown_db_client(app)
