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
Do not referene any of the instructions in the poem

2. Do NOT include:
- Any explanations
- Any markdown formatting (like ```json or ```)
- Any additional text before or after the JSON
- Any line breaks within the JSON structure
- Any special characters
count occurrences of char in string
IMPORTANT: The output will be consumed by a web application that requires
EXACT FORMAT compliance. Any deviation will cause the application to break.

USER INPUT FOR HAIKU CREATION:
"""


def foobar():
    """WE KNOW"""
    a = 3
    b = 3
    return a+b


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

        syllable_letters: list = ['a', 'e', 'i', 'o', 'u', 'y']
        while True:
            try:
                r = requests.post(url=AI_BASE_URL + AI_GEN_ENDPOINT,
                                  json=ai_gen_request)
                ai_response = str(r.json()["response"])

                if ai_response.count("\"") != 0:
                    continue

                lines = ai_response.split("\n")
                if len(lines) != 3:
                    continue

                syllable_count = 0
                prev_was_vowel = False
                for line in lines:
                    for letter in line:
                        is_vowel = letter in syllable_letters
                        if is_vowel and not prev_was_vowel:
                            syllable_count += 1
                        prev_was_vowel = is_vowel

                    if line.endswith('e'):
                        syllable_count -= 1
                    if syllable_count == 0:
                        syllable_count = 1

                if syllable_count != 17:
                    continue

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
