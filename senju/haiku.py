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
    def request_haiku(seed: str, url=AI_BASE_URL + AI_GEN_ENDPOINT) -> Haiku:
        """This function prompts the ai to generate
        the hauku based on the user input"""

        ai_gen_request = {
            "model": "haiku",
            "prompt": f"{seed}",
            "stream": False,
            "eval_count": 20
        }

        tries = 0
        while True:
            tries += 1
            try:
                r = requests.post(url=url,
                                  json=ai_gen_request)
                ai_response = str(r.json()["response"])

                logging.debug(f"ai response: {ai_response}")

                lines = ai_response.split("\n")

                while len(lines) != 3:
                    lines.pop()

                logging.info(f"lines for haiku: {lines}")

                if len(lines) < 3:
                    if tries < 20:
                        logging.warning("too few lines, trying again")
                        logging.debug(lines)
                        continue
                    else:
                        logging.warning("too many tries, aborting")
                        raise Exception(
                            "Generating the haiku took too many tries")

                haiku = Haiku(
                    [
                        lines[0],
                        lines[1],
                        lines[2]
                    ])

                break
            except json.JSONDecodeError as e:
                logging.error(f"error while reading json from LLM: {e}")
                raise e

        return haiku


DEFAULT_HAIKU: Haiku = Haiku(["Purple petals rise", "Defying fragile beauty",
                              "Fiercely breathing life"])
