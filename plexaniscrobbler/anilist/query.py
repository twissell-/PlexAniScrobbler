LIST_BY_USERNAME_AND_STATUS = """
query ($username: String, $status: MediaListStatus) {
  MediaListCollection(userName: $username, type: ANIME, status: $status) {
    lists {
      name
      status
      entries {
        id
        media {
          id
          title {
            userPreferred
          }
          episodes
          startDate {
            year
          }
        }
        progress
        notes
      }
    }
  }
}
"""

UPDATE_PROGRESS = """
  mutation ($id: Int, $progress: Int) {
    SaveMediaListEntry(id: $id, progress: $progress) {
      id
      progress
    }
  }
"""
