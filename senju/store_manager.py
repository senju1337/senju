"""
Senju Database Management Module
================================

A database interaction layer for the Senju haiku management system.

This module implements a lightweight document database
abstraction using TinyDB
for persistent storage of haiku poems. It provides a
clean interface for storing,
retrieving, updating, and managing haiku entries in the system.

Classes
-------
StoreManager
    The primary class responsible for all database operations.
    Handles connection
    management, CRUD operations, and query capabilities for haiku data.

Functions
---------
utility_function
    Provides simple arithmetic operations to support
    database functionalities.

Constants
---------
DEFAULT_DB_PATH
    The default filesystem location for the TinyDB database file
    (/var/lib/senju.json).

Dependencies
------------
* future.annotations: Enhanced type hint support
* logging.Logger: Diagnostic and error logging capabilities
* pathlib.Path: Cross-platform filesystem path handling
* typing.Optional: Type annotations for nullable values
* tinydb.TinyDB: Lightweight document database implementation
* tinydb.QueryImpl: Query builder for database searches
* senju.haiku.Haiku: Data model for haiku representation

Implementation Details
----------------------
The module uses TinyDB as its storage engine, providing a JSON-based document
storage solution that balances simplicity with functionality. The StoreManager
abstracts all database operations behind a clean API,
handling connection lifecycle
and providing methods for common operations on haiku data.
"""

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
    """
    Manages the storage and retrieval of haiku
    data using TinyDB.

    This class provides an interface for saving and
    loading haikus from
    a TinyDB database file.

    :ivar _db: Database instance for storing haiku data.
    :type _db: TinyDB
    :ivar logger: Logger for tracking operations and errors.
    :type logger: Logger
    """
    __slots__ = "_db", "logger"
    _db: TinyDB
    logger: Logger

    def __init__(self, path_to_db: Path = DEFAULT_DB_PATH) -> None:
        """
        Initialize the StoreManager with a database path.

        :param path_to_db: Path to the TinyDB database file.
            Defaults to DEFAULT_DB_PATH.
        :type path_to_db: Path, optional
        :return: None
        """
        self._db = TinyDB(path_to_db)

        try:
            self._db = TinyDB(path_to_db)
        except Exception as e:
            raise BadStoreManagerFileError(f"{e}")
        self.logger = Logger(__name__)

    def _query(self, query: QueryImpl) -> list[dict]:
        """
        Execute a query against the database.

        :param query: TinyDB query to execute.
        :type query: QueryImpl
        :return: List of documents matching the query.
        :rtype: list[dict]
        """
        return self._db.search(query)

    def _load(self, id: int) -> Optional[dict]:
        """
        Load a document by its ID.

        :param id: Document ID to load.
        :type id: int
        :return: The document if found, None otherwise.
        :rtype: Optional[dict]

        .. note::
           Logs a warning if document with specified
           ID is not found.
        """
        try:
            return self._db.get(doc_id=id)
        except IndexError as e:
            self.logger.warning(f"could not get item with id {id}: {e}")
            return None

    def _save(self, data: dict) -> int:
        """
        Save a document to the database.

        :param data: Document data to save.
        :type data: dict
        :return: The document ID of the saved document.
        :rtype: int
        """
        return self._db.insert(data)

    def load_haiku(self, key: Optional[int]) -> Haiku:
        """
        Load a haiku by its ID.

        :param key: The ID of the haiku to load.
        :type key: int
        :return: A Haiku object if found, None otherwise.
        :rtype: Optional[Haiku]
        """
        if key is None:
            return DEFAULT_HAIKU
        raw_haiku: dict | None = self._load(key)
        if raw_haiku is None:
            return DEFAULT_HAIKU
        h = Haiku(**raw_haiku)
        return h

    def save_haiku(self, data: Haiku) -> int:
        """
        Save a haiku to the database.

        :param data: The Haiku object to save.
        :type data: Haiku
        :return: The document ID of the saved haiku.
        :rtype: int
        """
        return self._save(data.__dict__)

    def get_id_of_latest_haiku(self) -> Optional[int]:
        """
        Get the ID of the most recently added haiku.

        :return: The ID of the latest haiku if any exists,
                 None otherwise.
        :rtype: Optional[int]

        .. note::
           Logs an error if the database is empty.
        """
        try:
            id = self._db.all()[-1].doc_id
            return id
        except IndexError as e:
            self.logger.error(f"The database seems to be empty: {e}")
            return None
