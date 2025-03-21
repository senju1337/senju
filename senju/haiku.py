from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import requests

AI_BASE_URL: str = "http://ollama:11434/api"
AI_GEN_ENDPOINT: str = "/generate"


def foobar():
    """WE KNOW"""
    a = 3
    b = 3
    return a + b


@dataclass
class Haiku:
    lines: list[str]

    def get_json(self):
        """
        Converts the haiku lines to a JSON string.

        Returns:
            str: A JSON string representation of the haiku lines.
        """

        return json.dumps(self.lines)

    @staticmethod
    def request_haiku(seed: str) -> Haiku:
        """
        Generates a haiku using an AI model based on the provided seed text.

        This function prompts the AI to generate a haiku based on the user input.
        It validates that the response:
        - Contains exactly 3 lines

        The function will retry until a valid haiku is generated.

        Args:
            seed (str): The input text used to inspire the haiku generation.

        Returns:
            Haiku: A new Haiku object containing the generated three lines.

        Raises:
            Possible JSONDecodeError which is caught and handled with retries.
        """

        ai_gen_request = {
            "model": "haiku",
            "prompt": f"{seed}",
            "stream": False,
            "eval_count": 20
        }

        while True:
            try:
                r = requests.post(url=AI_BASE_URL + AI_GEN_ENDPOINT,
                                  json=ai_gen_request)
                ai_response = str(r.json()["response"])

                logging.warning(ai_response)

                lines = ai_response.split("\n")

                for _ in range(0, 2):
                    lines.pop()

                logging.warning(lines)

                if len(lines) != 3:
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
