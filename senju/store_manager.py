from __future__ import annotations

from logging import Logger
from pathlib import Path
from typing import Optional

from tinydb import TinyDB
from tinydb.queries import QueryImpl

from senju.haiku import DEFAULT_HAIKU, Haiku

DEFAULT_DB_PATH: Path = Path("/var/lib/senju.json")


class BadStoreManagerFileError(Exception):
    def __init__(self, msg: str, * args: object) -> None:
        self.msg = msg
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Store file is corrupted: {self.msg}"


class StoreManager:
    __slots__ = "_db", "logger"
    _db: TinyDB
    logger: Logger

    def __init__(self, path_to_db: Path = DEFAULT_DB_PATH) -> None:
        try:
            self._db = TinyDB(path_to_db)
        except Exception as e:
            raise BadStoreManagerFileError(f"{e}")
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

    def load_haiku(self, key: Optional[int]) -> Haiku:
        if key is None:
            return DEFAULT_HAIKU
        raw_haiku: dict | None = self._load(key)
        if raw_haiku is None:
            return DEFAULT_HAIKU
        h = Haiku(**raw_haiku)
        return h

    def save_haiku(self, data: Haiku) -> int:
        return self._save(data.__dict__)

    def get_id_of_latest_haiku(self) -> Optional[int]:
        try:
            id = self._db.all()[-1].doc_id
            return id
        except IndexError as e:
            self.logger.error(f"The database seems to be empty: {e}")
            return None
