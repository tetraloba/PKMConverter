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

def _get_tags_from_SBPage(sbPage: SBPage):
    tags = []
    # except code block #TODO
    for line in sbPage.lines:
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
