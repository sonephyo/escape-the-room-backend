from models import Recipe
from prompts import puzzle_prompt
from dotenv import load_dotenv

from google.genai import types
from google import genai
import asyncio 
import os
from pydantic import BaseModel

load_dotenv() 
gemini_api_key = os.getenv("GEMINI_API_KEY")

data = [{
    "id":1,"name":"Ronaldo", "description":"Best football player"
}
,{
    "id":2,"name":"Mr Beast", "description":"Youtuber"
}
]


async def generate_for_item(client, puzzle_prompt):
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=puzzle_prompt,
        config={
        "response_mime_type": "application/json",
        "response_schema": Recipe,
    },
        
    )
    return response.parsed

    

async def get_puzzle(data):
    client = genai.Client()
    tasks = []
    for x in data:
    #     print("starting==")
        tasks.append(generate_for_item(client, puzzle_prompt))
    #     print('----finish------')
    res = await asyncio.gather(*tasks)


    for idx, x in enumerate(data):
        x['puzzle'] = res[idx].Puzzle

    return data

# # To run
# ans = asyncio.run(get_puzzle(data))
# print(ans)