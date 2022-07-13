"""Test downloader.py module."""

import pytest

from src.osmsqlite.downloader import GeofabrikDownloader


def test_headers():
    downloader = GeofabrikDownloader()
    header = downloader._fake_requests_headers()
    assert isinstance(header, dict)
    assert len(header["User-Agent"]) > 0


@pytest.mark.xfail
def test_divide_by_zero():
    assert 1 / 0 == 1


def test_print(capture_stdout):
    print("hello")
    assert capture_stdout["stdout"] == "hello\n"
