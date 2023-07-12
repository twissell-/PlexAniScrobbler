import json
import logging
from functools import reduce

from flask import Blueprint, Response, request
from Levenshtein import distance
from werkzeug.exceptions import BadRequestKeyError

from plexaniscrobbler.anilist import Anilist
from plexaniscrobbler.utils.config import Config

_logger = logging.getLogger("PlexAniScrobbler")
webhook = Blueprint("PlexAniScrobbler", __name__)


@webhook.route("webhook", methods=["POST"])
def _webhook():
    plex_username = Config.get("plex_username")
    anilist_username = Config.get("anilist_username")
    anilist = Anilist()

    data = request.form.get("payload")
    if not data:
        _logger.debug("Request does not have a payload.")
        return Response(status=200)

    data = json.loads(data)

    # event filter
    if (
        data["Account"]["title"] != plex_username
        or "media.scrobble" not in data["event"]  # media.scrobble
        or data["Metadata"]["type"] not in ["episode", "movie"]
    ):
        _logger.debug("Request ignored by filters.")
        return Response(status=200)

    metadata = data["Metadata"]
    entries = anilist.get_watching_list(anilist_username)

    if metadata["type"] == "episode":
        title = metadata["grandparentTitle"]
    else:
        title = metadata["title"]

    # TODO: Make this comparison by distance and year.
    entry = reduce(
        lambda x, y: x if distance(x.title, title) < distance(y.title, title) else y,
        entries,
    )

    if distance(title, entry.title) > 2:
        _logger.info("Title '{}' not found in watchlist.".format(title))
        return Response(status=200)

    progress = (
        metadata["index"] if metadata["index"] < entry.episodes else entry.progress + 1
    )

    res = anilist.update_progress(entry.id, progress)

    _logger.info(
        "Updated {} to {}/{}.".format(
            entry.title,
            res["data"]["SaveMediaListEntry"]["progress"],
            entry.episodes,
        )
    )

    return Response(status=200)
