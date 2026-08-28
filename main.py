import json
import glob # ファイルリストを取得
import datetime
import re

keep_dir = './data_keep'
sb_file_path = './data_scrapbox/data.json'
pkm_dir = './data_pkm'

# keep.json を読み込む
json_files = glob.glob(keep_dir+'/*.json')
print(len(json_files), 'json files detected.') # debug

# for debug
cnt = {'trushed':0, 'archived':0, 'textContents':0, 'selected':0}

# keep.json から scrapbox.json に変換する
sb:json = dict()
sb['pages'] = list()

for keep_file_path in json_files:
    # print(keep_file_path) # debug
    f_keep = open(keep_file_path, 'r')
    keep:json = json.load(f_keep)
    if keep['isTrashed']:
        cnt['trushed'] += 1 # debug
        continue
    if keep['isArchived']:
        cnt['archived'] += 1 # debug
    if not 'textContent' in keep:
        print(f"empty page ditected. ({keep['title']})")
        continue
    cnt['textContents'] += 1

    sb['pages'].append(dict())
    sb_page_json = sb['pages'][-1]
    sb_page_json['title'] = keep['title']
    sb_page_json['created'] = keep['createdTimestampUsec'] // 1000 // 1000
    sb_page_json['updated'] = keep['userEditedTimestampUsec'] // 1000 // 1000
    sb_page_json['lines'] = list()
    sb_page_json['lines'].append(sb_page_json['title'])
    sb_page_json['lines'] += keep['textContent'].split('\n')

    # taglist:str = str()
    # taglist += '#' + keep['color'] # colorは要らんかなあ…
    # for label in keep.get('labels', []):
    #     taglist += ' #' + label['name']
    # sb_page_json['lines'].append(taglist)

    state_tag_list:str = str()
    if keep['isTrashed']:
        state_tag_list += '#trashed '
    if keep['isPinned']:
        state_tag_list += '#pinned '
    if keep['isArchived']:
        state_tag_list += '#archived '
    sb_page_json['lines'].append(state_tag_list)

    created_dt = datetime.datetime.fromtimestamp(keep['createdTimestampUsec'] // 1000 // 1000)
    created_dt_str = f"{created_dt.year:04}{created_dt.month:02}{created_dt.day:02}-{created_dt.hour:02}{created_dt.minute:02}{created_dt.second:02}"
    invalid_chars = r'[\\/:*?"<>|]'
    pkm_filename = f"{created_dt_str}_{re.sub(invalid_chars, '_', keep['title'])}"
    
    with open(pkm_dir + '/' + pkm_filename, 'w') as f_pkm:
        f_pkm.write(keep['textContent'])

    f_keep.close()
    


# for debug
print(json_files.__len__(), 'files')
for key in cnt.keys():
    print(cnt[key], key)
