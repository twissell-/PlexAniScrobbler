import json
import logging

import requests

from plexaniscrobbler.anilist import query
from plexaniscrobbler.anilist.model import ListEntry
from plexaniscrobbler.utils import Config, Singleton

logger = logging.getLogger(__name__)


class Anilist(metaclass=Singleton):

    BASE_URL = "https://anilist.co/api/v2"
    GQL_URL = "https://graphql.anilist.co"

    def __init__(self):
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "",
        }

        if not Config.get("anilist_access_token"):
            raise ValueError("anilist_access_token is not configured.")

        self._access_token = Config.get("anilist_access_token")
        self._headers["Authorization"] = "Bearer  " + self._access_token

    def _request(
        self,
        endpoint=None,
        params="",
        method="GET",
        headers=None,
        body={},
    ):
        if not endpoint:
            url = Anilist.GQL_URL
        else:
            url = Anilist.BASE_URL + endpoint

        headers = headers or self._headers

        if method == "POST":
            rtn = requests.post(
                url,
                headers=headers,
                json=body,
                params=params,
            )
        elif method == "GET":
            rtn = requests.get(url, headers=headers, params=params)
        elif method == "PATCH":
            rtn = requests.patch(url, headers=headers, params=params)

        if rtn.status_code != 200:
            raise Exception(
                "Anilist respose was: [{status}] {text}".format(
                    status=rtn.status_code, text=rtn.text
                )
            )

        return rtn.json()

    def get_list(self, username, status):

        response = self._request(
            method="POST",
            body={
                "query": query.LIST_BY_USERNAME_AND_STATUS,
                "variables": {"username": username, "status": status},
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        entries = (
            response.get("data")
            .get("MediaListCollection")
            .get("lists")[0]
            .get("entries")
        )
        logger.debug("Raw response: " + json.dumps(entries, indent=2))

        rtn = []
        for entry in entries:
            rtn.append(ListEntry(entry))

        logger.debug("Mapped respose: " + str(rtn))
        return rtn

    def get_watching_list(self, username):
        return self.get_list(username, "CURRENT")

    def update_progress(self, entry_id: int, progress: int):

        response = self._request(
            method="POST",
            body={
                "query": query.UPDATE_PROGRESS,
                "variables": {"id": entry_id, "progress": progress},
            },
        )

        return response
