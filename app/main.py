# all the imports
from typing import List
from fastapi import FastAPI, HTTPException
import httpx

from app.models import Character, CharacterResponse, PuzzleResponse
from app.db import lifespan
from app.utils import get_puzzle

# creating a server with python FastAPI
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Escape the Room API is working!"}


@app.get("/get_all_characters", response_model=List[Character])
async def get_all_characters():
    try:
        characters = []
        cursor = app.mongodb["characters"].find({})
        async for document in cursor:
            characters.append(Character(**document))
        return characters
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching characters: {str(e)}"
        )


@app.post("/add_character", response_model=CharacterResponse)
async def add_character(character: Character):
    try:
        character_dict = character.model_dump()
        result = await app.mongodb["characters"].insert_one(character_dict)
        return CharacterResponse(
            id=str(result.inserted_id),
            name=character.name,
            description=character.description,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating character: {str(e)}"
        )


@app.get("/get_n_random_characters", response_model=List[PuzzleResponse])
async def get_n_random_characters(n: int):
    try:
        characters = []
        cursor = app.mongodb["characters"].aggregate([{"$sample": {"size": n}}])
        async for document in cursor:
            characters.append(Character(**document))

        characters = [character.model_dump() for character in characters]

        puzzle_response = await get_puzzle(characters)
        
        return puzzle_response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching random characters: {str(e)}"
        )
