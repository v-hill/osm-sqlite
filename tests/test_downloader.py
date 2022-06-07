"""Test downloader.py module."""

from src.osmsqlite.downloader import GeofabrikDownloader


def test_headers():
    downloader = GeofabrikDownloader()
    header = downloader._fake_requests_headers()
    assert isinstance(header, dict)
    assert len(header["User-Agent"]) > 0
