from dataclasses import dataclass
import json

@dataclass
class Haiku:
    lines: list[str]

    def get_json(self):
        return json.dumps(self.lines)

