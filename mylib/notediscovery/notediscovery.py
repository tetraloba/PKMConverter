from datetime import datetime
import re
from os import path
import yaml

class QuotedStr(str):
    pass
class Title(QuotedStr):
    pass

# customize PyYAML dumper
class CustomDumper(yaml.Dumper):
    # enforce indent (avoid list indentless style)
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)
# force double quotes ("") for QuotedStr (include inheritance)
yaml.add_multi_representer(
    QuotedStr,
    lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"'),
    Dumper=CustomDumper
)
# force isoformat for datetime
yaml.add_representer(
    datetime,
    lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:timestamp', data.isoformat()),
    Dumper=CustomDumper
)

class Page:
    def generate_filename(title: str, created: int):
        created_dt = datetime.fromtimestamp(created)
        created_dt_str = f"{created_dt.year:04}{created_dt.month:02}{created_dt.day:02}-{created_dt.hour:02}{created_dt.minute:02}{created_dt.second:02}"
        unsafe_filename = f"{created_dt_str}_{title}"
        INVALID_CHARS = r'[\\/:*?"<>|]' # characters can't be used as filename
        filename = re.sub(INVALID_CHARS, '_', unsafe_filename)
        return filename
    def __init__(self, title: str, created: int, updated: int, tags: list[str], content: str):
        self._title: Title = Title(title)
        self._created: int = created # [seconds]
        self._updated: int = updated # [seconds]
        self._tags: list[str] = tags # tag format is 'tagname', no '#'
        self._content: str = content
        self._filename = Page.generate_filename(self._title, self._created)
    def from_file(filepath):
        with open(filepath, 'r') as f:
            #TODO
            pass
    def dump(self, targetDir: str):
        with open(path.join(targetDir, self._filename + '.md'), 'w') as f:
            f.write(f"---\n")
            yaml.dump({
                    "title": self._title,
                    "created": datetime.fromtimestamp(self._created),
                    "updated": datetime.fromtimestamp(self._updated),
                    "tags": self._tags
                }, f, Dumper=CustomDumper, allow_unicode=True, sort_keys=False,
            )
            f.write(f"---\n")
            f.write(self._content)
