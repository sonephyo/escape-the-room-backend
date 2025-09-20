from pydantic import BaseModel


class Character(BaseModel):
    name: str
    description: str


class CharacterResponse(BaseModel):
    id: str
    name: str
    description: str

class PuzzleResponse(BaseModel):
    name: str
    description: str
    puzzle: str

class Recipe(BaseModel):
    Puzzle: str
