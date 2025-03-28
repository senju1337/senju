# do not remove this import. This is needed for
# pytest fixtures to work
from __future__ import annotations

import pytest  # noqa: F401
import os

from senju.haiku import DEFAULT_HAIKU, Haiku
from senju.store_manager import StoreManager  # noqa: F401


def test_temp_data_dir(temp_data_dir):
    print(temp_data_dir)
    testpath = temp_data_dir / "__test"
    with open(testpath, "w") as f:
        f.write("that dir actually works")
    os.remove(testpath)
    assert not os.path.exists(testpath)


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
    h = Haiku(lines=["foobar", "qux"])
    hid = store_manager.save_haiku(h)
    h_loaded = store_manager.load_haiku(hid)

    if h_loaded is None:
        assert False, "store manager load_haiku did not return anything \
            but should have"

    assert h == h_loaded
    assert h != DEFAULT_HAIKU


def test_load_latest_with_empty_store(temp_data_dir):
    store = StoreManager(temp_data_dir / "empty_store.json")
    h = store.get_id_of_latest_haiku()
    assert h is None


def test_load_latest_or_default_with_empty(temp_data_dir):
    store = StoreManager(temp_data_dir / "load_or_default_empty.json")
    haiku = store.load_haiku(store.get_id_of_latest_haiku())
    assert haiku == DEFAULT_HAIKU


def test_load_latest_or_default_with_non_empty(temp_data_dir):
    store = StoreManager(temp_data_dir / "load_or_default_not_empty.json")
    nonsense_test_haiku = Haiku(["nonsense", "test", "haiku"])
    store.save_haiku(nonsense_test_haiku)
    haiku = store.load_haiku(store.get_id_of_latest_haiku())
    assert haiku != DEFAULT_HAIKU
    assert haiku == nonsense_test_haiku


def test_load_latest_with_non_empty_store(temp_data_dir):
    store = StoreManager(temp_data_dir / "empty_store.json")
    store.save_haiku(Haiku(["hello", "world", "bananenkrokodil"]))
    h = store.get_id_of_latest_haiku()
    assert h is not None
    assert h > 0


def test_create_store_with_bad_file(temp_data_dir):
    with pytest.raises(Exception):
        testpath = temp_data_dir / "non_empty.json"
        with open(testpath, "w") as f:
            f.write("BUT IT DOES NOT ACTUALLY HAVE JSON")
        store = StoreManager(testpath)
        store._save({"hello": 19})


def test_create_store_with_non_empty(temp_data_dir):
    testpath = temp_data_dir / "non_empty.json"
    with open(testpath, "w") as f:
        f.write('{"this": ["is","valid","json"]}')
    store = StoreManager(testpath)
    store._save({"hello": 19})
