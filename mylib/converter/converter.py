from datetime import datetime
import re
import copy
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

def SBPage2NDPage(sbPage: SBPage, title2sbpageFilename: dict):
    def _replace_link(sbPage: SBPage, linkStyle: str = 'wiki') -> SBPage:
        """
        Args:
            sbPage (SBPage): immutable (Changes will be applyed to deep copied object.)
            linkStyle (str): 'wiki' (Wikilink, default. `[[filename]]`) or 'md' (Markdown Link. `[title](filepath)`)
        Returns:
            sbPage (SBPage): link replaced.
        #TODO support subdirectory in LinkStyle 'md'.
        """
        sbPage = copy.deepcopy(sbPage) # the Arg `sbPage` should be immutable.
        links = [] # for debug
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
            LINK = r'\[[^[\]]*\]' # link pettern (on Scrapbox)
            line_links = re.findall(LINK, line)
            for link in line_links:
                filename = title2sbpageFilename.get(link[1:-1], None)
                if filename == None:
                    logger.info(f"the link ({link[1:-1]}) destination not found.")
                    continue
                if linkStyle == 'wiki':
                    sbPage.lines[i] = line.replace(link, f"[[{filename}]]")
                elif linkStyle == 'md':
                    #TODO support filepath (subdirectory).
                    sbPage.lines[i] = line.replace(link, f"{link}(./{filename})")
                else:
                    raise ValueError(f"linkStyle ({linkStyle}) not found!")
            links += line_links # for debug
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"{sbPage.title}")
            for link in links:
                logger.info(link)
            logger.debug("")
        return sbPage
    def _replace_codeblock(sbPage: SBPage) -> SBPage:
        """
        replace codeblock on Scrapbox (code:) style to Markdown (```) style
        Args:
            sbPage (SBPage): immutable (Changes will be applyed to deep copied object.)
        Returns:
            sbPage (SBPage): code block replaced.
        #TODO support indented codeblock on Scrapbox
        """
        sbPage = copy.deepcopy(sbPage) # the Arg `sbPage` should be immutable.
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
        return sbPage
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
    content = "\n".join(_replace_codeblock(_replace_link(sbPage, 'wiki')).lines[1:]) + '\n#importedFromScrapbox\n'
    return NDPage(
        title = sbPage.title,
        created = sbPage.created,
        updated = sbPage.updated,
        tags = tags,
        content = content,
    )

def SBPages2NDPages(sbPages: SBPages, nd_out_dir: str):
    title2sbpageFilename = dict()
    for sbPage in sbPages.pages:
        title2sbpageFilename[sbPage.title] = NDPage.generate_filename(sbPage.title, sbPage.created)
    logger.debug(f"title2sbpageFilename: {title2sbpageFilename}")
    for sbPage in sbPages.pages:
        ndPage = SBPage2NDPage(sbPage, title2sbpageFilename)
        ndPage.dump(nd_out_dir)
