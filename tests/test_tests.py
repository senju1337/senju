# I do not trust python and it's tests, so I'm testing them. May not be worth much, but at least it shows me a few things.

import os
import pytest  # noqa: F401 do not remove this import. This is needed for pytest fixtures to work

import senju  # noqa: F401

# Note: these weird arguments are an indicator of what should be dome before. For example,
# `temp_data_dir` is a function in `conftest.py`. If we put it in the arguments, it seems
# to run before our test, and the return value becomes a local.
#
# This is all very confusing for someone used to Rust's libtest


def test_tests_are_loaded():
    assert True  # if we make it here, they are


def test_temp_data_dir(temp_data_dir):
    print(temp_data_dir)
    testpath = temp_data_dir / "__test"
    with open(testpath, "w") as f:
        f.write("that dir actually works")
    os.remove(testpath)

