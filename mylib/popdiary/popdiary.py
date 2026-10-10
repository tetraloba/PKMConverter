import json
import logging

logger = logging.getLogger(__name__)

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)

class Diary:
    # WIP #TODO
    PHOTOGRAPH_MAX_NUM = 11
    DEFAULT_CATEGORY = '未分類'
    DEFAULT_EMOTION = 'ちっぽけ'
    DEFAULT_STAR = '0'
    DEFAULT_BGCOLOR = 'white'
    def __init__(self, id: int, year: str, month: str, day: str, time: str, weather: str, category: str, emotion: str, title: str, note_01: str, note_02 = '', note_03 = '', note_04 = '', photograph_01 = '', photograph_02 = '', photograph_03 = '', photograph_04 = '', star = '0', bgcolor = 'white', note_05 = '', note_06 = '', photograph_05 = '', photograph_06 = '', primary_photo = '', text_color = None, text_align = None, note_07 = None, note_08 = None, photograph_07 = None, photograph_08 = None, note__00 = None, video_path = None, video_title = None, note_09 = None, photograph_09 = None, location = None, map_path = None, timestamp_color = None, weather_condition = None, notes = None, note_10 = None, note_11 = None, photograph_10 = None, photograph_11 = None, audio_name = None, font = None):
        self.id: int = id
        self.year: str = year
        self.month: str = month
        self.day: str = day
        self.time: str = time
        self.weather: str = weather
        self.category: str = category
        self.emotion: str = emotion
        self.title: str = title
        self.note_01: str = note_01
        self.note_02: str = note_02
        self.note_03: str = note_03
        self.note_04: str = note_04
        self.note_05: str = note_05
        self.note_06: str = note_06
        self.note_07: str = note_07
        self.note_08: str = note_08
        self.note_09: str = note_09
        self.note_10: str = note_10
        self.note_11: str = note_11
        self.photograph_01: str = photograph_01
        self.photograph_02: str = photograph_02
        self.photograph_03: str = photograph_03
        self.photograph_04: str = photograph_04
        self.photograph_05: str = photograph_05
        self.photograph_06: str = photograph_06
        self.photograph_07: str = photograph_07
        self.photograph_08: str = photograph_08
        self.photograph_09: str = photograph_09
        self.photograph_10: str = photograph_10
        self.photograph_11: str = photograph_11
        self.star: str = star
        self.bgcolor: str = bgcolor
        self.notes: str = notes
    def from_json(diary_json: json, diary_category: dict, diary_emotion: dict):
        if (
            # diary_json['note_02'] or diary_json['note_03'] or diary_json['note_04'] or
            # diary_json['photograph_01'] or diary_json['photograph_02'] or diary_json['photograph_03'] or diary_json['photograph_04'] or
            # int(diary_json['star']) or
            # diary_json['bgcolor'] != 'white' or
            # diary_json['note_05'] or diary_json['note_06'] or
            # diary_json['photograph_05'] or diary_json['photograph_06'] or diary_json['primary_photo'] or 
            diary_json['text_color'] and diary_json['text_color'] != 'black' or
            diary_json['text_align'] and diary_json['text_align'] != 'left' or
            # diary_json['note_07'] or diary_json['note_08'] or
            # diary_json['photograph_07'] or diary_json['photograph_08'] or
            diary_json['note__00'] or diary_json['video_path'] or diary_json['video_title'] or
            # diary_json['note_09'] or
            # diary_json['photograph_09'] or
            diary_json['location'] or diary_json['map_path'] or
            diary_json['timestamp_color'] and diary_json['timestamp_color'] != 'timestamp_01' or
            diary_json['weather_condition'] or
            # diary_json['notes'] or
            # diary_json['note_10'] or diary_json['note_11'] or
            # diary_json['photograph_10'] or diary_json['photograph_11'] or
            diary_json['audio_name'] or
            diary_json['font'] and diary_json['font'] != 'Default'
        ):
            logger.error(f"not implemented attribute detected! {diary_json}")
            raise NotImplementedError
        if (
            diary_json['note_02'] or diary_json['note_03'] or diary_json['note_04'] or
            diary_json['note_05'] or diary_json['note_06'] or
            diary_json['note_07'] or diary_json['note_08'] or
            diary_json['note_09'] or
            diary_json['note_10'] or diary_json['note_11']
        ):
            logger.info(f"note > 1 on {diary_json['id']}, {diary_json['title']}")
        if (
            diary_json['photograph_01'] or diary_json['photograph_02'] or diary_json['photograph_03'] or diary_json['photograph_04'] or
            diary_json['photograph_05'] or diary_json['photograph_06'] or diary_json['primary_photo'] or
            diary_json['photograph_07'] or diary_json['photograph_08'] or
            diary_json['photograph_09'] or
            diary_json['photograph_10'] or diary_json['photograph_11']
        ):
            logger.info(f"photograph on {diary_json['id']}, {diary_json['title']}")
        if int(diary_json['star']):
            logger.info(f"star: {diary_json['star']} on {diary_json['id']}, {diary_json['title']}")
        if diary_json['bgcolor'] != 'white':
            logger.info(f"bgcolor: {diary_json['bgcolor']} on {diary_json['id']}, {diary_json['title']}")
        if diary_json['notes']:
            logger.debug(f"notes detected on {diary_json['id']}, {diary_json['title']}")
        return Diary(
            id = diary_json['id'],
            year = diary_json['year'],
            month = diary_json['month'],
            day = diary_json['day'],
            time = diary_json['time'],
            weather = diary_json['weather'],
            category = diary_category.get(diary_json['id'], Diary.DEFAULT_CATEGORY),
            emotion = diary_emotion.get(diary_json['id'], Diary.DEFAULT_EMOTION),
            title = diary_json['title'],
            note_01 = diary_json['note_01'],
            note_02 = diary_json['note_02'],
            note_03 = diary_json['note_03'],
            note_04 = diary_json['note_04'],
            note_05 = diary_json['note_05'],
            note_06 = diary_json['note_06'],
            note_07 = diary_json['note_07'],
            note_08 = diary_json['note_08'],
            note_09 = diary_json['note_09'],
            note_10 = diary_json['note_10'],
            note_11 = diary_json['note_11'],
            photograph_01 = diary_json['photograph_01'],
            photograph_02 = diary_json['photograph_02'],
            photograph_03 = diary_json['photograph_03'],
            photograph_04 = diary_json['photograph_04'],
            photograph_05 = diary_json['photograph_05'],
            photograph_06 = diary_json['photograph_06'],
            photograph_07 = diary_json['photograph_07'],
            photograph_08 = diary_json['photograph_08'],
            photograph_09 = diary_json['photograph_09'],
            photograph_10 = diary_json['photograph_10'],
            photograph_11 = diary_json['photograph_11'],
            star = diary_json['star'],
            bgcolor = diary_json['bgcolor'],
            notes = diary_json['notes'],
        )
    def get_note_list(self):
        return [
            self.note_01,
            self.note_02,
            self.note_03,
            self.note_04,
            self.note_05,
            self.note_06,
            self.note_07,
            self.note_08,
            self.note_09,
            self.note_10,
            self.note_11,
        ]
    def get_photograph_list(self):
        return [
            self.photograph_01,
            self.photograph_02,
            self.photograph_03,
            self.photograph_04,
            self.photograph_05,
            self.photograph_06,
            self.photograph_07,
            self.photograph_08,
            self.photograph_09,
            self.photograph_10,
            self.photograph_11,
        ]
    def dump_json(self):
        #TODO
        pass

class Diaries:
    def __init__(self, diary_list: list[Diary] = []):
        self.diaries = diary_list
    def from_jsons(jsons_dir: str):
        with open(jsons_dir + '/diary.json', 'r') as f:
            diaries_json = json.load(f)

        category_id2name = dict()
        with open(jsons_dir + '/category.json', 'r') as f:
            category_json = json.load(f)
        for category in category_json:
            category_id2name[category['key_id']] = category['category_name']
        diary_category = dict()
        with open(jsons_dir + '/diary_category.json', 'r') as f:
            diary_category_json = json.load(f)
        for diary in diary_category_json:
            diary_category[diary['diary_id']] = category_id2name[diary['category_id']]

        emotion_id2name = dict()
        with open(jsons_dir + '/emotion.json', 'r') as f:
            emotion_json = json.load(f)
        for emotion in emotion_json:
            emotion_id2name[emotion['emotion_id']] = emotion['emotion_name']
        diary_emotion = dict()
        with open(jsons_dir + '/diary_emotion.json', 'r') as f:
            diary_emotion_json = json.load(f)
        for diary in diary_emotion_json:
            diary_emotion[diary['diary_id2']] = emotion_id2name[diary['emotion_id']]

        return Diaries([Diary.from_json(diary_json, diary_category, diary_emotion) for diary_json in diaries_json])
    def dump_json(self, file_path):
        diaries_json = {'diaries': self.diaries}
        with open(file_path, 'w') as f:
            json.dump(diaries_json, f, indent=2, ensure_ascii=False, cls=CustomEncoder)
