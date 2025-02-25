from typing import Optional
from tinydb import TinyDB, Query
from uuid import UUID, uuid1
from pathlib import Path
import time

from tinydb.queries import QueryImpl

DEFAULT_DB_PATH: Path = Path("/var/lib/senju.json")


class StoreManager:
    __slots__ = "_db"
    _db: TinyDB

    def __init__(self, path_to_db: Path = DEFAULT_DB_PATH) -> None:
        self._db = TinyDB(path_to_db)

    def new_id(self) -> UUID:
        _guard: int = 0
        while True:
            unix_timestamp: int = int(time.time())
            id = uuid1(node=None, clock_seq=unix_timestamp)
            if len(self._query(Query().id == id)) < 1:
                break
            _guard += 1
            if _guard > 100:
                raise Exception(
                    "tried 100 random UUIDs but found no unused one")
        return id

    def _query(self, query: QueryImpl) -> list[dict]:
        return self._db.search(query)

    def load(self, key: UUID) -> Optional[dict]:
        results = self._query(Query().id == str(key))
        if len(results) < 1:
            raise Exception("foobar")
        elif len(results) > 2:
            raise KeyError("The requested item did not exist in our database")
        else:
            return results[0]["data"]

    def save(self, data: dict) -> UUID:
        id = self.new_id()
        self._db.insert({
            "id": str(id),
            "data": data
        })
        return id
