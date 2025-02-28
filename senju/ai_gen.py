import json
import requests
from senju.haiku import Haiku

AI_BASE_URL: str = "http://ollama:11434/api" 
AI_GEN_ENDPOINT: str = "/generate"

AI_GEN_SYS_PROMPT = """
You are a helpful AI agent whos task it is to generate Haikus from user input.
Here is the definition of a Haiku:

Haiku (俳句) is a type of short form poetry that originated in Japan. Traditional Japanese haiku consist of three
phrases composed of 17 morae (called on in Japanese) in a 5, 7, 5 pattern that include a kireji, 
or "cutting word" and a kigo, or seasonal reference.

You must return only the poem and nothing else.
You must return the poem in a json format in the following format:
{
    line1: First line of the poem,
    line2: Second line of the poem,
    line3: Third line of the poem,
}

Your input is as follows:  
"""

def request_haiku(seed: str) -> Haiku:
    """This function prompts the ai to generate the hauku based on the user input"""
    
    ai_gen_request = {
        "model": "llama3.2:1b",
        "prompt": f"{AI_GEN_SYS_PROMPT}{seed}",
        "stream": False
    }

    r = requests.post(url=AI_BASE_URL+AI_GEN_ENDPOINT, json=ai_gen_request)

    ai_response = json.loads(r.json()["response"])
    print(ai_response)
    haiku = Haiku([ai_response["line1"], ai_response["line2"], ai_response["line3"]]) 
    return haiku
