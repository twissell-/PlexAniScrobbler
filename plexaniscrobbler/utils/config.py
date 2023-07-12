class Config:
    __conf = {
        "anilist_client_id": 0,
        "anilist_client_secret": "",
        "anilist_redirect_url": "",
        "anilist_username": "",
        "anilist_access_token": "",
        "plex_username": "",
        "tmp_dir": "",
        "webhook_endpoint": "/webhook",
        "auth_endpoint": "/auth",
    }

    __setters = __conf.keys()

    @staticmethod
    def get(name):
        return Config.__conf[name]

    @staticmethod
    def set(name, value):
        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")


def configure(
    anilist_client_id: int,
    anilist_client_secret: str,
    anilist_redirect_url: str,
    anilist_username: str,
    anilist_access_token: str,
    plex_username: str,
    tmp_dir: str,
    webhook_endpoint: str = "/webhook",
    auth_endpoint: str = "/auth",
):

    Config.set("anilist_client_id", anilist_client_id)
    Config.set("anilist_client_secret", anilist_client_secret)
    Config.set("anilist_redirect_url", anilist_redirect_url)
    Config.set("anilist_username", anilist_username)
    Config.set("anilist_access_token", anilist_access_token)
    Config.set("plex_username", plex_username)
    Config.set("tmp_dir", tmp_dir)
    Config.set("webhook_endpoint", webhook_endpoint)
    Config.set("auth_endpoint", auth_endpoint)
