# I do not trust python and it's tests, so I'm testing them. May not be worth
# much, but at least it shows me a few things.

from __future__ import annotations

import json
from pytest_httpserver import HTTPServer
import requests

# do not remove this import. This is needed for
# pytest fixtures to work
import pytest  # noqa: F401

from senju.haiku import Haiku  # noqa: F401

# Note: these weird arguments are an indicator of what should be dome
# before. For example, `temp_data_dir` is a function in `conftest.py`. If we
# put it in the arguments, it seems to run before our test, and the return
# value becomes a local. This is all very confusing for someone used to
# Rust's libtest


def test_create_haiku():
    haiku = Haiku(["line number 1", "line number 2", "line number 3"])
    assert haiku.lines[0] == "line number 1"
    assert haiku.lines[1] == "line number 2"
    assert haiku.lines[2] == "line number 3"
    assert len(haiku.lines) == 3


def test_get_haiku_json():
    haiku = Haiku(["line number 1", "line number 2", "line number 3"])
    data_raw: str = haiku.get_json()
    assert data_raw == '["line number 1", "line number 2", "line number 3"]'
    data = json.loads(data_raw)
    assert haiku.lines[0] == "line number 1"
    assert haiku.lines[1] == "line number 2"
    assert haiku.lines[2] == "line number 3"
    assert len(haiku.lines) == 3
    assert data == ['line number 1', 'line number 2', 'line number 3']


def test_request_haiku(httpserver: HTTPServer):

    httpserver.expect_request(
        "/testhaiku").respond_with_json({"response":
                                         "The apparition of these\n"
                                         "faces in a crowd; Petal\n"
                                         "on a wet, black bough."
                                         })

    haiku = Haiku.request_haiku(
        "apple banana papaya", url=httpserver.url_for("/testhaiku"))
    assert haiku.lines[0] == "The apparition of these"
    assert haiku.lines[1] == "faces in a crowd; Petal"
    assert haiku.lines[2] == "on a wet, black bough."
    assert len(haiku.lines) == 3


def test_request_haiku_respondse_bad(httpserver: HTTPServer):
    with pytest.raises(requests.exceptions.JSONDecodeError):

        httpserver.expect_request(
            "/testhaiku").respond_with_data(
            "this is completely wrong" + ("A" * 50 + "\n") * 20)

        Haiku.request_haiku(
            "apple banana papaya", url=httpserver.url_for("/testhaiku"))
