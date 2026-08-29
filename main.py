import json
import glob # ファイルリストを取得

from mylib.converter.converter import GKMemo2SBPage
from mylib.converter.converter import GKMemo
from mylib.converter.converter import SBPages

keep_dir = './data_keep'
sb_file_path = './out_scrapbox/scrapbox.json'

# keep.json の一覧を取得
json_files = glob.glob(keep_dir+'/*.json')
# print(json_files) # debug

sb_pages = SBPages()

attribute_counter = dict()

for keep_file_path in json_files:
    # print(keep_file_path) # debug
    with open(keep_file_path, 'r') as f_keep:
        gk_json = json.load(f_keep)
    for attr in gk_json.keys():
        attribute_counter[attr] = attribute_counter.get(attr, 0) + 1
    gk_memo = GKMemo.from_json(gk_json)
    sb_pages.pages.append(GKMemo2SBPage(gk_memo))

print(attribute_counter)
# scrapbox.json を書き出す
sb_pages.dump_json(sb_file_path)
