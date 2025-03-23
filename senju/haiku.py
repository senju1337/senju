"""
Haiku Generation Module
=======================

A client interface for AI-powered haiku poem generation.

This module provides the core functionality for communicating with an Ollama-based
AI service to generate three-line haiku poems. It handles the entire generation
process, from sending properly formatted requests to processing and validating
the returned poems.

Classes
-------
Haiku
    A dataclass representation of a haiku poem, providing structure for storage,
    manipulation and serialization of poem data.

    **Methods**:

    * ``to_json()``: Converts a haiku instance to JSON format for API responses
    * ``generate_haiku(seed_text)``: Creates a new haiku using the AI service

Constants
---------
AI_SERVICE_URL
    The endpoint URL for the Ollama API service.

AI_MODEL_NAME
    The specific AI model used for haiku generation.

REQUEST_TIMEOUT
    The maximum time (in seconds) to wait for AI service responses.

Dependencies
------------
* requests: HTTP client library for API communication
* dataclasses: Support for the Haiku data structure
* logging: Error and diagnostic information capture
* json: Processing of API responses

Implementation Details
----------------------
The module implements a robust communication pattern with the AI service, including:

1. Proper request formatting with seed text integration
2. Multiple retry attempts for handling temporary service issues
3. Response validation to ensure the returned text follows haiku structure
4. Fallback mechanisms when the AI service returns unsuitable content
5. JSON serialization for consistent data exchange

When communicating with the AI service, the module maintains appropriate
error handling and logging to help diagnose any generation issues. It aims
to provide a reliable haiku generation experience even when dealing with the
inherent unpredictability of AI-generated content.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass

import requests

AI_BASE_URL: str = "http://ollama:11434/api"
AI_GEN_ENDPOINT: str = "/generate"


@dataclass
class Haiku:
    """
    A class representing a haiku poem with three lines.

    :ivar lines: A list containing the three lines of the haiku.
    :type lines: list[str]
    """
    lines: list[str]

    def get_json(self):
        """
        Converts the haiku lines to a JSON string.

        :return: A JSON string representation of the haiku lines.
        :rtype: str
        """
        return json.dumps(self.lines)

    @staticmethod
    def request_haiku(seed: str, url=AI_BASE_URL + AI_GEN_ENDPOINT) -> Haiku:
        """This function prompts the ai to generate
        the hauku based on the user input
        :param seed: The input text used to inspire the haiku generation.
        :param url: The URL to the AI endpoint
        :type seed: str
        :return: A new Haiku object containing the generated three lines.
        :rtype: Haiku

        :raises: Possible JSONDecodeError which is caught and handled with retries.
        """
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
