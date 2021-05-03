import logging
import os
import pathlib
import pickle
from datetime import datetime, timedelta
from typing import Optional

from dateutil.tz import UTC

import requests
import sys

from requests import Response

from overcast_stats_extractor.model.exceptions import (
    AuthenticationFailed,
    OpmlFetchError,
)

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache_path: str) -> None:
        self.cache_dir = cache_path
        self._cache_path = pathlib.Path(self.cache_dir).joinpath("./overcast.opml")
        super().__init__()

    @property
    def cache_path(self) -> pathlib.Path:
        return self._cache_path

    def read_cached_data(self) -> Optional[str]:
        cache_exists = self.cache_path.exists()
        cache_stale = True
        if cache_exists:
            now = datetime.utcnow().astimezone(UTC)
            cache_modified = datetime.fromtimestamp(
                self.cache_path.stat().st_mtime
            ).astimezone(UTC)
            cache_modified_day_later = cache_modified + timedelta(days=1)
            if now < cache_modified_day_later:
                cache_stale = False

        if not cache_exists or cache_stale:
            logging.info("Cached data stale")
            return None
        else:
            logging.info("Using data from cache")
            with self.cache_path.open("r") as f:
                return f.read()

    def write_cached_data(self, data: str):
        with self.cache_path.open("w") as f:
            f.write(data)


def fetch_fresh_data(settings) -> Response:
    logging.info("Authenticating")
    session = requests.Session()
    response = session.post(
        "https://overcast.fm/login",
        data={"email": settings.email, "password": settings.password},
    )

    if response.status_code != 200:
        logging.error("Authentication failed")
        raise AuthenticationFailed(
            status_code=response.status_code,
            response_text=response.text,
            response_headers=response.headers,
        )

    logging.info("Authenticated successfully.")

    # fetch the latest detailed OPML export from Overcast
    logging.info("Fetching latest OPML export from Overcast")
    response = session.get("https://overcast.fm/account/export_opml/extended")
    if response.status_code != 200:
        logging.error("Failed to fetch OPML")
        raise OpmlFetchError(
            status_code=response.status_code,
            response_text=response.text,
            response_headers=response.headers,
        )
    return response
