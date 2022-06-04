"""Download OpenStreetMap data files provided by Geofabrik.

The download server at https://download.geofabrik.de has excerpts and derived
data from the OpenStreetMap dataset available for free download.
"""

import os
import time

import requests
from fake_useragent import UserAgent
from tqdm import tqdm


class GeofabrikDownloader:
    def __init__(self):
        self.x = "Hello"

    def _fake_requests_headers(self):
        """Make a fake HTTP headers for 'requests.get'."""
        fake_user_agent = UserAgent(verify_ssl=False)
        user_agent = fake_user_agent["google chrome"]
        fake_headers = {"User-Agent": user_agent}
        return fake_headers

    def _download_file_from_url(self, url, path_to_file, wait_to_retry=3600):
        """Download an object from a URL.

        Parameters
        ----------
        url : str
            Input URL.
        path_to_file : str
            A path where the downloaded object is saved as, or a filename.
        wait_to_retry : int or float, optional
            A wait time to retry downloading, by default 3600 (in second).
        """
        headers = self._fake_requests_headers()
        try:
            resp = requests.get(url, stream=True, headers=headers)
            resp.raise_for_status()
        except resp.status_code == 429:
            print(f"Too Many Requests, waiting for {wait_to_retry} seconds")
            time.sleep(wait_to_retry)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        self._stream_data_to_file(path_to_file, resp)
        resp.close()

    def _stream_data_to_file(self, path_to_file, resp):
        """Stream data into file.

        Parameters
        ----------
        path_to_file : str
            A path where the downloaded object is saved as, or a filename.
        resp : requests.models.Response
            Request response.
        """
        total_size = int(resp.headers.get("content-length"))
        block_size = 1024 * 1024
        downloaded = 0

        with open(path_to_file, mode="wb") as f:
            temp = resp.iter_content(block_size, decode_unicode=True)
            for data in tqdm(temp, total=total_size // block_size, unit="MB"):
                downloaded = downloaded + len(data)
                f.write(data)
            f.close()

        # verify download
        if total_size != 0 and downloaded != total_size:
            print(
                "Error downloading file\ntotal size remaining :"
                f" {total_size}\ntotal downloaded : {downloaded}"
            )

    def download_osm_data(self, download_url, path_to_file):
        """Download OSM data given a URL and a filepath.

        Parameters
        ----------
        download_url : str
            Link to file to be downloaded.
        path_to_file : str or
            Path to locally downloaded file.
        """
        path_to_dir = os.path.dirname(path_to_file)
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)

        relative_path = os.path.relpath(os.path.dirname(path_to_file))
        print(f"Downloading {path_to_file} to {relative_path}")
        try:
            self._download_file_from_url(download_url, path_to_file)
        except Exception as err:
            print(f"Download failed.\n{err}")
