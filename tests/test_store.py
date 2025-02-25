# do not remove this import. This is needed for
# pytest fixtures to work
import pytest

from senju.store_manager import StoreManager  # noqa: F401


def test_temp_data_dir(store_manager: StoreManager):
    thing = {
        "color": "blue",
        "number": 19,
        "inner": {
            "no": "yes"
        }
    }
    thing_id = store_manager.save(thing)
    thing_loaded = store_manager.load(thing_id)
    if thing_loaded is None:
        assert False, "the store manager load did not return anything"
    for key in thing.keys():
        assert thing[key] == thing_loaded[key]
