from flask import Blueprint, Response, request

from plexaniscrobbler.anilist import Anilist
from plexaniscrobbler.utils.config import Config

auth = Blueprint("ren_auth", __name__)

_endpoint = Config.get("auth_endpoint")


@auth.route(_endpoint, methods=["GET", "POST"])
def ren_auth():

    print(request.args)
    client_id = Config.get("anilist_client_id")
    redirect_uri = Config.get("anilist_redirect_url")

    if request.method == "GET":
        if not request.args.get("code"):
            return """
            <center>
                <a href='https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'>Login with AniList</a>
            </center>
            """.format(
                client_id=client_id, redirect_uri=redirect_uri
            )
        else:
            Anilist(request.args.get("code"))

    return Response("Authorization succesful", status=200)
