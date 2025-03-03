from __future__ import annotations

import json

import requests

from senju.haiku import Haiku

AI_BASE_URL: str = "http://ollama:11434/api"
AI_GEN_ENDPOINT: str = "/generate"

AI_GEN_SYS_PROMPT = """
You are a haiku generation AI. Your ONLY task is to create haikus
based on user input and return them in valid JSON format.

HAIKU DEFINITION:
- Traditional Japanese poetry with three lines
- 5 syllables in the first line
- 7 syllables in the second line
- 5 syllables in the third line
- Must incorporate the subject(s) from user input

OUTPUT RULES:
1. ONLY respond with a valid JSON object in this exact format:
{
  "line1": "First line of haiku",
  "line2": "Second line of haiku",
  "line3": "Third line of haiku"
}

2. Do NOT include:
   - Any explanations
   - Any markdown formatting (like ```json or ```)
   - Any additional text before or after the JSON
   - Any line breaks within the JSON structure

3. Before submitting, verify:
   - The JSON uses double quotes (not single quotes)
   - All property names are lowercase and exactly as shown above
   - There are no trailing commas
   - The JSON is properly formatted

IMPORTANT: The output will be consumed by a web application that requires
EXACT FORMAT compliance. Any deviation will cause the application to break.

USER INPUT FOR HAIKU CREATION:
"""


def request_haiku(seed: str) -> Haiku:
    """This function prompts the ai to generate
    the hauku based on the user input"""

    ai_gen_request = {
        "model": "llama3.2:1b",
        "prompt": f"{AI_GEN_SYS_PROMPT}{seed}",
        "stream": False
    }

    while True:
        try:
            r = requests.post(url=AI_BASE_URL + AI_GEN_ENDPOINT,
                              json=ai_gen_request)
            ai_response = json.loads(r.json()["response"])
            haiku = Haiku(
                [
                    ai_response["line1"],
                    ai_response["line2"],
                    ai_response["line3"]
                ])
            break
        except json.JSONDecodeError:
            continue

    return haiku
