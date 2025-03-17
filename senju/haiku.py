from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import requests

AI_BASE_URL: str = "http://ollama:11434/api"
AI_GEN_ENDPOINT: str = "/generate"


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
