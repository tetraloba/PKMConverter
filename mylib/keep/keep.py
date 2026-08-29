import json

class Memo:
    class Label:
        def __init__(self, name):
            self.name: str = name
    def __init__(self, title: str, color: str, isTrashed: bool, isPinned: bool, isArchived: bool, labels: list[Label], createdTimestampUsec: int, userEditedTimestampUsec: int, textContent: str):
        self.title: str = title
        self.color: str = color
        self.isTrashed: bool = isTrashed
        self.isPinned: bool = isPinned
        self.isArchived: bool = isArchived
        self.labels: list[Memo.Label] = [Memo.Label(('' if label['name'][0] == '#' else '#') + label['name']) for label in labels]
        # self.color:str = memo_json['color']
        self.createdTimestampUsec: int = createdTimestampUsec # [microseconds]
        self.userEditedTimestampUsec: int = userEditedTimestampUsec # [microseconds]
        self.textContent: str = textContent # sepalated with \n
    def from_json(memo_json: json):
        return Memo(
            title = memo_json['title'],
            color = memo_json['color'],
            isTrashed = memo_json['isTrashed'],
            isPinned = memo_json['isPinned'],
            isArchived = memo_json['isArchived'],
            labels = memo_json.get('labels', []),
            createdTimestampUsec = memo_json['createdTimestampUsec'],
            userEditedTimestampUsec = memo_json['userEditedTimestampUsec'],
            textContent = memo_json.get('textContent', '')
        )        
    def dump_json(self):
        #TODO
        pass
