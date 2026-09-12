import json

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)

class Page:
    def __init__(self, title: str, created: int, updated: int, lines: list[str], id_: str = "", views: int = 0):
        self.title: str = title
        self.created: int = created # [seconds]
        self.updated: int = updated # [seconds]
        self.lines: list[str] = lines
        self.id: str = id_
        self.views: int = views
    def from_json(page_json):
        return Page(
            title = page_json['title'],
            created = page_json['created'],
            updated = page_json['updated'],
            lines = page_json['lines'],
            id_ = page_json['id'],
            views = page_json['views'],
        )
class Pages:
    def __init__(self, page_list: list[Page] = []):
        self.pages = page_list
    def from_json(pages_json):
        return Pages([Page.from_json(page_json) for page_json in pages_json['pages']])
    def dump_json(self, file_path):
        pages_json = {'pages': self.pages}
        with open(file_path, 'w') as f:
            json.dump(pages_json, f, indent=2, ensure_ascii=False, cls=CustomEncoder)
