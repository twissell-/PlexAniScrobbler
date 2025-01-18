import json
from functools import reduce

from flask import Blueprint, Response, current_app, request
from Levenshtein import distance

from plexaniscrobbler.anilist import Anilist
from plexaniscrobbler.utils.config import Config

webhook = Blueprint("PlexAniScrobbler", __name__)


@webhook.route("webhook", methods=["POST"])
def _webhook():
    plex_username = Config.get("plex_username")
    anilist_username = Config.get("anilist_username")
    anilist = Anilist()

    data = request.form.get("payload")
    if not data:
        current_app.logger.debug("Request does not have a payload.")
        return Response(status=200)

    data = json.loads(data)

    # event filter
    if (
        data["Account"]["title"] != plex_username
        or "media.scrobble" not in data["event"]  # media.scrobble
        or data["Metadata"]["type"] not in ["episode", "movie"]
    ):
        current_app.logger.debug("Request ignored by filters.")
        return Response(status=200)

    metadata = data["Metadata"]
    entries = anilist.get_watching_list(anilist_username)
    entries += anilist.get_rewatching_list(anilist_username)

    if metadata["type"] == "episode":
        title = metadata["grandparentTitle"].lower()
    else:
        title = metadata["title"].lower()

    # TODO: Make this comparison by distance and year.
    entry = reduce(
        lambda x, y: (
            x
            if distance(x.title.lower(), title) < distance(y.title.lower(), title)
            else y
        ),
        entries,
    )

    if distance(title, entry.title) > 2:
        current_app.logger.info("Title '{}' not found in watchlist.".format(title))
        return Response(status=200)

    progress = (
        metadata["index"] if metadata["index"] < entry.episodes else entry.progress + 1
    )

    res = anilist.update_progress(entry.id, progress)

    current_app.logger.info(
        "Updated {} to {}/{}.".format(
            entry.title,
            res["data"]["SaveMediaListEntry"]["progress"],
            entry.episodes,
        )
    )

    return Response(status=200)
