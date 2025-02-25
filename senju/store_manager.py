from typing import Optional
from tinydb import TinyDB
from pathlib import Path
from logging import Logger

from tinydb.queries import QueryImpl

DEFAULT_DB_PATH: Path = Path("/var/lib/senju.json")


class StoreManager:
    __slots__ = "_db", "logger"
    _db: TinyDB
    logger: Logger

    def __init__(self, path_to_db: Path = DEFAULT_DB_PATH) -> None:
        self._db = TinyDB(path_to_db)
        self.logger = Logger(__name__)

    def _query(self, query: QueryImpl) -> list[dict]:
        return self._db.search(query)

    def _load(self, id: int) -> Optional[dict]:
        try:
            return self._db.get(doc_id=id)
        except IndexError as e:
            self.logger.warning(f"could not get item with id {id}: {e}")
            return None

    def _save(self, data: dict) -> int:
        return self._db.insert(data)
