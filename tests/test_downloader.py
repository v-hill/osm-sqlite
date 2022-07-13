"""Test downloader.py module."""

import pytest

from osmsqlite.downloader import GeofabrikDownloader


def test_headers():
    downloader = GeofabrikDownloader()
    header = downloader._fake_requests_headers()
    assert isinstance(header, dict)
    assert len(header["User-Agent"]) > 0


@pytest.mark.xfail
def test_divide_by_zero():
    assert 1 / 0 == 1
