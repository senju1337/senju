# do not remove this import. This is needed for
# pytest fixtures to work
from pathlib import Path
import pytest  # noqa: F401

from senju.haiku import Haiku
from senju.store_manager import StoreManager  # noqa: F401


def test_save_and_load_any(store_manager: StoreManager):
    thing = {
        "color": "blue",
        "number": 19,
        "inner": {
            "no": "yes"
        }
    }
    thing_id = store_manager._save(thing)
    thing_loaded = store_manager._load(thing_id)

    if thing_loaded is None:
        assert False, "store manager load did not return anything but \
            should have"
    for key in thing.keys():
        assert thing[key] == thing_loaded[key]


def test_save_and_load_haiku(store_manager: StoreManager):
    h = Haiku(text="foobar")
    hid = store_manager.save_haiku(h)
    h_loaded = store_manager.load_haiku(hid)

    if h_loaded is None:
        assert False, "store manager load_haiku did not return anything \
            but should have"

    assert h == h_loaded


def test_load_latest_with_empty_store(temp_data_dir):
    store = StoreManager(temp_data_dir / "empty_store.json")
    h = store.get_id_of_latest_haiku()
    assert h is None
