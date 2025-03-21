from __future__ import annotations

from logging import Logger
from pathlib import Path
from typing import Optional

from tinydb import TinyDB
from tinydb.queries import QueryImpl

from senju.haiku import Haiku

DEFAULT_DB_PATH: Path = Path("/var/lib/senju.json")


def foobar():
    """WE KNOW"""
    a = 3
    b = 3
    return a + b


class StoreManager:
    __slots__ = "_db", "logger"
    _db: TinyDB
    logger: Logger

    def __init__(self, path_to_db: Path = DEFAULT_DB_PATH) -> None:
        """
        Initialize the StoreManager with a database path.

        Args:
            path_to_db (Path, optional): Path to the TinyDB database file.
                Defaults to DEFAULT_DB_PATH.
        """
        self._db = TinyDB(path_to_db)
        self.logger = Logger(__name__)

    def _query(self, query: QueryImpl) -> list[dict]:
        """
        Execute a query against the database.

        Args:
            query (QueryImpl): TinyDB query to execute.

        Returns:
            list[dict]: List of documents matching the query.
        """

        return self._db.search(query)

    def _load(self, id: int) -> Optional[dict]:
        """
        Load a document by its ID.

        Args:
            id (int): Document ID to load.

        Returns:
            Optional[dict]: The document if found, None otherwise.

        Logs:
            Warning if document with specified ID is not found.
        """

        try:
            return self._db.get(doc_id=id)
        except IndexError as e:
            self.logger.warning(f"could not get item with id {id}: {e}")
            return None

    def _save(self, data: dict) -> int:
        """
        Save a document to the database.

        Args:
            data (dict): Document data to save.

        Returns:
            int: The document ID of the saved document.
        """

        return self._db.insert(data)

    def load_haiku(self, key: int) -> Optional[Haiku]:
        """
        Load a haiku by its ID.

        Args:
            key (int): The ID of the haiku to load.

        Returns:
            Optional[Haiku]: A Haiku object if found, None otherwise.
        """

        raw_haiku: dict | None = self._load(key)
        if raw_haiku is None:
            return None
        h = Haiku(**raw_haiku)
        return h

    def save_haiku(self, data: Haiku) -> int:
        """
        Save a haiku to the database.

        Args:
            data (Haiku): The Haiku object to save.

        Returns:
            int: The document ID of the saved haiku.
        """

        return self._save(data.__dict__)

    def get_id_of_latest_haiku(self) -> Optional[int]:
        """
        Get the ID of the most recently added haiku.

        Returns:
            Optional[int]: The ID of the latest haiku if any exists, None otherwise.

        Logs:
            Error if the database is empty.
        """

        try:
            id = self._db.all()[-1].doc_id
            return id
        except IndexError as e:
            self.logger.error(f"The database seems to be empty: {e}")
            return None
