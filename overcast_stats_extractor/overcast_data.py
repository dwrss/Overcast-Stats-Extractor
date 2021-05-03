import os
import pathlib
import pickle
from datetime import datetime, timedelta
from typing import Optional

from dateutil.tz import UTC

import requests
import sys

from requests import Response


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
            print("Cache stale fetching new data")
            return None
        else:
            print("Using data from cache")
            with self.cache_path.open("r") as f:
                return f.read()

    def write_cached_data(self, data: str):
        with self, self.cache_path.open("w") as f:
            f.write(data)


def fetch_fresh_data(settings) -> Response:
    # load stored session, or re-authenticate
    if os.path.exists(settings.session_path):
        print("Found saved session. Restoring!")
        session = pickle.loads(open(settings.session_path, "rb").read())
    else:
        print("No saved session. Authenticating!")
        session = requests.Session()
        response = session.post(
            "https://overcast.fm/login",
            data={"email": settings.email, "password": settings.password},
        )

        if response.status_code != 200:
            print("Authentication failed")
            sys.exit(0)

        print("Authenticated successfully. Saving session.")

        with open(settings.session_path, "wb") as saved_session:
            saved_session.write(pickle.dumps(session))

    # fetch the latest detailed OPML export from Overcast
    print("Fetching latest OPML export from Overcast")
    response = session.get("https://overcast.fm/account/export_opml/extended")
    if response.status_code != 200:
        print("Failed to fetch OPML. Exiting.")
        print(response.text)
        print(response.headers)
        sys.exit(0)
    return response
