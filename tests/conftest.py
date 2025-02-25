import tempfile
from pathlib import Path

import pytest

from senju.store_manager import StoreManager


@pytest.fixture(scope="session")
def temp_data_dir():
    """Create a temporary directory for test data"""
    return Path(tempfile.mkdtemp())


@pytest.fixture(scope="session")
def store_manager(temp_data_dir):
    return StoreManager(temp_data_dir / "store.db")
