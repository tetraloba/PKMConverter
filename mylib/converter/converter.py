from datetime import datetime
import re
import logging

from mylib.keep.keep import Memo as GKMemo
from mylib.scrapbox.scrapbox import Page as SBPage
from mylib.scrapbox.scrapbox import Pages as SBPages
from mylib.notediscovery.notediscovery import Page as NDPage

logger = logging.getLogger(__name__)

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
        lines = [memo.title] + memo.textContent.split('\n') + [importation_tag, tags, state_tags],
        # id and views in Scrapbox are not in Google Keep. so skipped.
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

def SBPage2NDPage(sbPage: SBPage):
    def _replace_codeblock(sbPage: SBPage):
        """
        replace codeblock on Scrapbox (code:) style to Markdown (```) style
        Args:
            sbPage (SBPage)
        Returns:
            lines (list[str])
        #TODO match the type of Args to Returns
        #TODO support indented codeblock on Scrapbox
        """
        cbs = _get_codeblock_linenums_from_SBPage(sbPage)
        lines = sbPage.lines
        for cb in reversed(cbs): # descendding order for insertion
            logger.debug(f"codeblock range: [{cb[0]},{cb[1]})")
            if len(lines) < cb[1]:
                raise IndexError(f"the codeblock [{cb[0]},{cb[1]}) of '{sbPage.title}' is out of range!")
            if len(lines[cb[0]]) < 5 or lines[cb[0]][0:5] != 'code:':
                raise RuntimeError(f"the codeblock range [{cb[0]},{cb[1]}) of '{sbPage.title}' is not codeblock!")
            # replace header
            lines[cb[0]] = lines[cb[0]].replace('code:', '```')
            # unindent body
            for i in range(cb[0] + 1, cb[1]):
                if len(lines[i]) == 0 or lines[i][0] != ' ' and lines[i][0] != '\t':
                    raise RuntimeError(f"the line ({i}) of '{sbPage.title}' is not codeblock!")
                lines[i] = lines[i][1:]
            # insert footer
            lines.insert(cb[1], '```')
        return lines
    def _get_tags_from_SBPage(sbPage: SBPage):
        tags = []
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
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{sbPage.title}: tags: {tags}")
            # for tag in tags:
            #     logger.debug(tag)
        tags = [tag[1:] for tag in tags] # remove '#'
        return tags
    tags = _get_tags_from_SBPage(sbPage) + ['importedFromScrapbox']
    content = "\n".join(_replace_codeblock(sbPage)[1:]) + '\n#importedFromScrapbox\n'
    return NDPage(
        title = sbPage.title,
        created = sbPage.created,
        updated = sbPage.updated,
        tags = tags,
        content = content,
    )
