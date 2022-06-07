"""Main file for development and testing."""
import os

from src.osmsqlite.downloader import GeofabrikDownloader

download_url = (
    "https://download.geofabrik.de/europe/great-britain"
    "/england/isle-of-wight-latest.osm.bz2"
)
path_to_file = os.path.join(
    os.getcwd(),
    os.path.join("downloads", download_url.split("/")[-1]),
)

downloader = GeofabrikDownloader()
downloader.download_osm_data(download_url, path_to_file)
