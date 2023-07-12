import json
from functools import reduce

from flask import Blueprint, Response, request
from Levenshtein import distance

from plexaniscrobbler.anilist import Anilist
from plexaniscrobbler.utils.config import Config

webhook = Blueprint("PlexAniScrobbler_webhook", __name__)


@webhook.route("webhook", methods=["POST"])
def _webhook():
    plex_username = Config.get("plex_username")
    anilist_username = Config.get("anilist_username")
    anilist = Anilist()

    data = json.loads(request.form["payload"])

    # event filter
    if (
        data["Account"]["title"] != plex_username
        or "media.scrobble" not in data["event"]  # media.scrobble
        or data["Metadata"]["type"] not in ["episode", "movie"]
    ):
        return Response(status=200)

    metadata = data["Metadata"]
    entries = anilist.get_watching_list(anilist_username)

    if metadata["type"] == "episode":
        title = metadata["grandparentTitle"]
        episode = metadata["index"]
    else:
        title = metadata["title"]
        episode = 1

    # TODO: Make this comparison by distance and year.
    entry = reduce(
        lambda x, y: x if distance(x.title, title) < distance(y.title, title) else y,
        entries,
    )

    print(title, episode, distance(title, entry.title))
    print(entry)

    if distance(title, entry.title) > 2:
        print("Title '{}' not found in watchlist.".format(title))
        return Response(status=200)

    progress = (
        metadata["index"] if metadata["index"] < entry.episodes else entry.progress + 1
    )

    progress = entry.progress

    res = anilist.update_progress(entry.id, progress)

    print(
        "Updated {} to {}".format(
            entry.title, res["data"]["SaveMediaListEntry"]["progress"]
        )
    )

    return Response(status=200)
