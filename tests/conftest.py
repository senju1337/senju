import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def temp_data_dir():
    """Create a temporary directory for test data"""
    return Path(tempfile.mkdtemp())
