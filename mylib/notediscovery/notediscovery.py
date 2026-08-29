from datetime import datetime
import re

class Page:
    def __init__(self, title: str, createdAt: int, updatedAt: int, tags: list[str], content: str):
        self._title: str = title
        self._createdAt: int = createdAt # [seconds]
        self._updatedAt: int = updatedAt # [seconds]
        self._tags: list[str] = tags # tag format is '#tagname'
        self._content: str = content
        self._set_filename(self._title, self._createdAt)
    def _set_filename(self, title: str, createdAt: int):
        created_dt = datetime.fromtimestamp(self._createdAt)
        created_dt_str = f"{created_dt.year:04}{created_dt.month:02}{created_dt.day:02}-{created_dt.hour:02}{created_dt.minute:02}{created_dt.second:02}"
        unsafe_filename = f"{created_dt_str}_{title}"
        INVALID_CHARS = r'[\\/:*?"<>|]' # characters can't be used as filename
        filename = re.sub(INVALID_CHARS, '_', unsafe_filename)
        self._filename: str = filename
    def from_file(filepath):
        with open(filepath, 'r') as f:
            #TODO
            pass
    def dump(self):
        with open(self._filename, 'w') as f:
            #TODO
            pass
