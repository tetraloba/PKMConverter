import json
import glob # ファイルリストを取得
import logging

from mylib.converter.converter import PDDiaries2NDPages
from mylib.converter.converter import PDDiaries
from mylib.converter.converter import GKMemo2SBPage
from mylib.converter.converter import GKMemo
from mylib.converter.converter import SBPages
from mylib.converter.converter import SBPages2NDPages

LOGFILE = '/dev/stdout'
LOGLEVEL = logging.DEBUG

logger = logging.getLogger(__name__)

def pd2nd():
    pd_data_dir = './data_popdiary'
    nd_out_dir = './out_notediscovery_from_popdiary'
    pddiaries = PDDiaries.from_jsons(pd_data_dir)
    PDDiaries2NDPages(pddiaries, nd_out_dir)

def gk2sb():
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

def sb2nd():
    sb_file_path = './data_scrapbox/tetraloba-private.json'
    nd_out_dir = './out_notediscovery_from_scrapbox'

    with open(sb_file_path, 'r') as f_sb:
        sb_json = json.load(f_sb)

    if logger.isEnabledFor(logging.DEBUG):
        attribute_counter = dict()
        for sbpage_json in sb_json['pages']:
            for attr in sbpage_json.keys():
                attribute_counter[attr] = attribute_counter.get(attr, 0) + 1
        logging.debug(attribute_counter)

    sbPages = SBPages.from_json(sb_json)
    SBPages2NDPages(sbPages, nd_out_dir)

def main():
    logging.basicConfig(
        filename=LOGFILE,
        level=LOGLEVEL
    )
    # gk2sb()
    # sb2nd()
    pd2nd()

if __name__ == '__main__':
    main()
