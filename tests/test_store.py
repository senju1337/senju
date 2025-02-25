# do not remove this import. This is needed for
# pytest fixtures to work
import pytest  # noqa: F401

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
