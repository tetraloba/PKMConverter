from datetime import datetime
import re

from mylib.keep.keep import Memo as GKMemo
from mylib.scrapbox.scrapbox import Page as SBPage
from mylib.scrapbox.scrapbox import Pages as SBPages
from mylib.notediscovery.notediscovery import Page as NDPage

def GKMemo2SBPage(memo: GKMemo):
    created_dt = datetime.fromtimestamp(memo.createdTimestampUsec // 1000 // 1000)
    title_if_empty = created_dt.isoformat()

    importation_tag: str = '#importedFromGoogleKeep'
    tags: str = ' '.join(['#' + memo.color] + [label.name for label in memo.labels])
    state_tags: str = ' '.join([tag for state, tag in zip(['isTrashed', 'isPinned', 'isArchived'], ['#trashed', '#pinned', '#archived']) if memo.__dict__[state]])

    return SBPage(
        title = memo.title if len(memo.title) else title_if_empty,
        created = memo.createdTimestampUsec // 1000 // 1000,
        updated = memo.userEditedTimestampUsec // 1000 // 1000,
        lines = [memo.title] + memo.textContent.split('\n') + [importation_tag, tags, state_tags]
    )

def _get_codeblock_linenums_from_SBPage(sbPage: SBPage):
    """
    SBPageのlinesの内，コードブロック(code:)である行範囲(半開区間)のリストを返す。
    10~13行目と22~47行目がコードブロックなら戻り値は[(10,14),(22,48)]
    """
    cbs = []
    begin = -1
    for i, line in enumerate(sbPage.lines):
        if begin != -1:
            if len(line) and (line[0] == ' ' or line[0] == '\t'):
                continue
            else:
                end = i
                cbs.append((begin, end))
                begin = -1
        if line[0:5] == 'code:':
            begin = i
    if begin != -1:
        if len(sbPage.lines) != i + 1: raise Exception('assertion failed')
        end = i + 1
        cbs.append((begin, end))
    return cbs

def _get_tags_from_SBPage(sbPage: SBPage):
    tags = []
    # except code block #TODO
    cbs = _get_codeblock_linenums_from_SBPage(sbPage)
    cbs_i = 0
    for i, line in enumerate(sbPage.lines):
        if cbs_i < len(cbs) and cbs[cbs_i][1] <= i:
            cbs_i += 1
        if cbs_i < len(cbs) and cbs[cbs_i][1] <= i:
            raise RuntimeError("codeblock range with same 'end' detected!")
        if cbs_i < len(cbs) and cbs[cbs_i][0] <= i:
            # is codeblock
            continue
        TAG = r'(?:^|\s)(#[^\s]+)' # tag pettern
        tags += re.findall(TAG, line)

    # debug
    print(f"{sbPage.title}: tags: {tags}")
    # for tag in tags:
    #     print(tag)

    return tags

def SBPage2NDPage(sbPage: SBPage):
    # WIP
    # replace code block (code: -> ```) #TODO
    # 
    return NDPage(
        title = sbPage.title,
        createdAt = sbPage.created,
        updatedAt = sbPage.updated,
        tags = _get_tags_from_SBPage(sbPage),
        content = "\n".join(sbPage.lines[1:])
    )
