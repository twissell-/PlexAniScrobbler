class ListEntry(object):
    def __init__(self, raw_entry):
        self._id = raw_entry.get("id")
        self._media_id = raw_entry.get("media").get("id")
        self._title = raw_entry.get("media").get("title").get("userPreferred")
        self._progress = raw_entry.get("progress")
        self._notes = raw_entry.get("notes")
        self._episodes = raw_entry.get("media").get("episodes") or 98
        self._startYear = raw_entry.get("media").get("startDate").get("year")

    @property
    def id(self):
        return self._id

    @property
    def media_id(self):
        return self._media_id

    @property
    def title(self):
        return self._title

    @property
    def progress(self):
        return self._progress

    @property
    def notes(self):
        return self._notes

    @property
    def episodes(self):
        return self._episodes

    @property
    def startYear(self):
        return self._startYear

    def __repr__(self):
        return "[%d] %s (%d/%d)" % (
            self.media_id,
            self.title,
            self.progress or 0,
            self.episodes or 0,
        )
