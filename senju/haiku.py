from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class Haiku:
    lines: list[str]

    def get_json(self):
        return json.dumps(self.lines)
