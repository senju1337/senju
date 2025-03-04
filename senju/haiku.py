from __future__ import annotations

import json
from dataclasses import dataclass

import requests

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
Put every line of the poem on a new line

2. Do NOT include:
- Any explanations
- Any markdown formatting (like ```json or ```)
- Any additional text before or after the JSON
- Any line breaks within the JSON structure
- Any special characters

IMPORTANT: The output will be consumed by a web application that requires
EXACT FORMAT compliance. Any deviation will cause the application to break.

USER INPUT FOR HAIKU CREATION:
"""


@dataclass
class Haiku:
    lines: list[str]

    def get_json(self):
        return json.dumps(self.lines)

    @staticmethod
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
                ai_response = str(r.json()["response"])
                lines = ai_response.split("\n")
                haiku = Haiku(
                    [
                        lines[0],
                        lines[1],
                        lines[2]
                    ])
                break
            except json.JSONDecodeError:
                continue

        return haiku
