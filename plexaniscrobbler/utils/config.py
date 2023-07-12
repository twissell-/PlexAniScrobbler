class Config:
    __conf = {
        "anilist_username": "",
        "anilist_access_token": "",
        "plex_username": "",
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
    anilist_username: str,
    anilist_access_token: str,
    plex_username: str,
):

    Config.set("anilist_username", anilist_username)
    Config.set("anilist_access_token", anilist_access_token)
    Config.set("plex_username", plex_username)
