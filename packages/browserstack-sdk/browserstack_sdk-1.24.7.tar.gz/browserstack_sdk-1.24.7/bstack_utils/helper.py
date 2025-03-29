# coding: UTF-8
import sys
bstack1l1lll_opy_ = sys.version_info [0] == 2
bstack1111l_opy_ = 2048
bstack1l1l1ll_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1ll11_opy_):
    global bstack1l1111l_opy_
    bstack1l11lll_opy_ = ord (bstack1ll11_opy_ [-1])
    bstack1111l11_opy_ = bstack1ll11_opy_ [:-1]
    bstack1ll111l_opy_ = bstack1l11lll_opy_ % len (bstack1111l11_opy_)
    bstack11111ll_opy_ = bstack1111l11_opy_ [:bstack1ll111l_opy_] + bstack1111l11_opy_ [bstack1ll111l_opy_:]
    if bstack1l1lll_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l_opy_ - (bstack11l11ll_opy_ + bstack1l11lll_opy_) % bstack1l1l1ll_opy_) for bstack11l11ll_opy_, char in enumerate (bstack11111ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1111l_opy_ - (bstack11l11ll_opy_ + bstack1l11lll_opy_) % bstack1l1l1ll_opy_) for bstack11l11ll_opy_, char in enumerate (bstack11111ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l111111ll1_opy_, bstack11l1lll11l_opy_, bstack1l11111111_opy_, bstack1ll1111ll_opy_,
                                    bstack1l111l111l1_opy_, bstack1l1111l11l1_opy_, bstack1l11111llll_opy_, bstack1l1111l11ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll1l11l_opy_, bstack1ll11l1l1l_opy_
from bstack_utils.proxy import bstack1l1lll1111_opy_, bstack11ll1111ll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1llllll_opy_
from browserstack_sdk._version import __version__
bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
logger = bstack1l1llllll_opy_.get_logger(__name__, bstack1l1llllll_opy_.bstack1llllll11l1_opy_())
def bstack1l111ll1l11_opy_(config):
    return config[bstack1l1l1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᢗ")]
def bstack1l111lllll1_opy_(config):
    return config[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᢘ")]
def bstack1l11ll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11llll1llll_opy_(obj):
    values = []
    bstack11lll11ll1l_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣᢙ"), re.I)
    for key in obj.keys():
        if bstack11lll11ll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll1lll1l1_opy_(config):
    tags = []
    tags.extend(bstack11llll1llll_opy_(os.environ))
    tags.extend(bstack11llll1llll_opy_(config))
    return tags
def bstack11lllll1l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11llll11ll1_opy_(bstack11ll1l1l1l1_opy_):
    if not bstack11ll1l1l1l1_opy_:
        return bstack1l1l1l1_opy_ (u"ࠬ࠭ᢚ")
    return bstack1l1l1l1_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢᢛ").format(bstack11ll1l1l1l1_opy_.name, bstack11ll1l1l1l1_opy_.email)
def bstack1l11l111ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11llll1ll11_opy_ = repo.common_dir
        info = {
            bstack1l1l1l1_opy_ (u"ࠢࡴࡪࡤࠦᢜ"): repo.head.commit.hexsha,
            bstack1l1l1l1_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦᢝ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤᢞ"): repo.active_branch.name,
            bstack1l1l1l1_opy_ (u"ࠥࡸࡦ࡭ࠢᢟ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢᢠ"): bstack11llll11ll1_opy_(repo.head.commit.committer),
            bstack1l1l1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨᢡ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1l1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨᢢ"): bstack11llll11ll1_opy_(repo.head.commit.author),
            bstack1l1l1l1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᢣ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᢤ"): repo.head.commit.message,
            bstack1l1l1l1_opy_ (u"ࠤࡵࡳࡴࡺࠢᢥ"): repo.git.rev_parse(bstack1l1l1l1_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧᢦ")),
            bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᢧ"): bstack11llll1ll11_opy_,
            bstack1l1l1l1_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᢨ"): subprocess.check_output([bstack1l1l1l1_opy_ (u"ࠨࡧࡪࡶᢩࠥ"), bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥᢪ"), bstack1l1l1l1_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ᢫")]).strip().decode(
                bstack1l1l1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᢬")),
            bstack1l1l1l1_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᢭"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᢮"): repo.git.rev_list(
                bstack1l1l1l1_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ᢯").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11llll11l11_opy_ = []
        for remote in remotes:
            bstack11lll11l1l1_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᢰ"): remote.name,
                bstack1l1l1l1_opy_ (u"ࠢࡶࡴ࡯ࠦᢱ"): remote.url,
            }
            bstack11llll11l11_opy_.append(bstack11lll11l1l1_opy_)
        bstack11lll111lll_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᢲ"): bstack1l1l1l1_opy_ (u"ࠤࡪ࡭ࡹࠨᢳ"),
            **info,
            bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᢴ"): bstack11llll11l11_opy_
        }
        bstack11lll111lll_opy_ = bstack11llll1lll1_opy_(bstack11lll111lll_opy_)
        return bstack11lll111lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᢵ").format(err))
        return {}
def bstack11llll1lll1_opy_(bstack11lll111lll_opy_):
    bstack11ll1llll1l_opy_ = bstack11ll1lll1ll_opy_(bstack11lll111lll_opy_)
    if bstack11ll1llll1l_opy_ and bstack11ll1llll1l_opy_ > bstack1l111l111l1_opy_:
        bstack11lll11ll11_opy_ = bstack11ll1llll1l_opy_ - bstack1l111l111l1_opy_
        bstack11ll1ll111l_opy_ = bstack11lll1l11l1_opy_(bstack11lll111lll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᢶ")], bstack11lll11ll11_opy_)
        bstack11lll111lll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᢷ")] = bstack11ll1ll111l_opy_
        logger.info(bstack1l1l1l1_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᢸ")
                    .format(bstack11ll1lll1ll_opy_(bstack11lll111lll_opy_) / 1024))
    return bstack11lll111lll_opy_
def bstack11ll1lll1ll_opy_(bstack1l1ll1l11_opy_):
    try:
        if bstack1l1ll1l11_opy_:
            bstack11llll1l11l_opy_ = json.dumps(bstack1l1ll1l11_opy_)
            bstack11llll111l1_opy_ = sys.getsizeof(bstack11llll1l11l_opy_)
            return bstack11llll111l1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᢹ").format(e))
    return -1
def bstack11lll1l11l1_opy_(field, bstack11lllll111l_opy_):
    try:
        bstack11ll1lll11l_opy_ = len(bytes(bstack1l1111l11l1_opy_, bstack1l1l1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᢺ")))
        bstack11lll1lll1l_opy_ = bytes(field, bstack1l1l1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᢻ"))
        bstack11ll1l1llll_opy_ = len(bstack11lll1lll1l_opy_)
        bstack11lll1ll1ll_opy_ = ceil(bstack11ll1l1llll_opy_ - bstack11lllll111l_opy_ - bstack11ll1lll11l_opy_)
        if bstack11lll1ll1ll_opy_ > 0:
            bstack11ll1l11ll1_opy_ = bstack11lll1lll1l_opy_[:bstack11lll1ll1ll_opy_].decode(bstack1l1l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᢼ"), errors=bstack1l1l1l1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᢽ")) + bstack1l1111l11l1_opy_
            return bstack11ll1l11ll1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᢾ").format(e))
    return field
def bstack1llll1ll_opy_():
    env = os.environ
    if (bstack1l1l1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᢿ") in env and len(env[bstack1l1l1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᣀ")]) > 0) or (
            bstack1l1l1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᣁ") in env and len(env[bstack1l1l1l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᣂ")]) > 0):
        return {
            bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᣃ"): bstack1l1l1l1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᣄ"),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᣅ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᣆ")),
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᣇ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᣈ")),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᣉ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᣊ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡉࠣᣋ")) == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᣌ") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᣍ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᣎ"): bstack1l1l1l1_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᣏ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᣐ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᣑ")),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᣒ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᣓ")),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᣔ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᣕ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡍࠧᣖ")) == bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᣗ") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᣘ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᣙ"): bstack1l1l1l1_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᣚ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᣛ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᣜ")),
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᣝ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᣞ")),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᣟ"): env.get(bstack1l1l1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᣠ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࠤᣡ")) == bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᣢ") and env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᣣ")) == bstack1l1l1l1_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᣤ"):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᣥ"): bstack1l1l1l1_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᣦ"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᣧ"): None,
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᣨ"): None,
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᣩ"): None
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᣪ")) and env.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᣫ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᣬ"): bstack1l1l1l1_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᣭ"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᣮ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᣯ")),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᣰ"): None,
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᣱ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᣲ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡎࠨᣳ")) == bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᣴ") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᣵ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᣶"): bstack1l1l1l1_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᣷"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᣸"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧ᣹")),
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᣺"): None,
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᣻"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᣼"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࠤ᣽")) == bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ᣾") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᣿"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤀ"): bstack1l1l1l1_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᤁ"),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᤂ"): env.get(bstack1l1l1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᤃ")),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᤄ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᤅ")),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᤆ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᤇ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡎࠨᤈ")) == bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᤉ") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᤊ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᤋ"): bstack1l1l1l1_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᤌ"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᤍ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᤎ")),
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᤏ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᤐ")),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᤑ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᤒ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡋࠥᤓ")) == bstack1l1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᤔ") and bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᤕ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᤖ"): bstack1l1l1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᤗ"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᤘ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᤙ")),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᤚ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᤛ")) or env.get(bstack1l1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᤜ")),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᤝ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᤞ"))
        }
    if bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢ᤟"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᤠ"): bstack1l1l1l1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢᤡ"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᤢ"): bstack1l1l1l1_opy_ (u"ࠤࡾࢁࢀࢃࠢᤣ").format(env.get(bstack1l1l1l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᤤ")), env.get(bstack1l1l1l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᤥ"))),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᤦ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᤧ")),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᤨ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᤩ"))
        }
    if bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᤪ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᤫ"): bstack1l1l1l1_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨ᤬"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᤭"): bstack1l1l1l1_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧ᤮").format(env.get(bstack1l1l1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭᤯")), env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᤰ")), env.get(bstack1l1l1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᤱ")), env.get(bstack1l1l1l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᤲ"))),
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᤳ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᤴ")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᤵ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᤶ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᤷ")) and env.get(bstack1l1l1l1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᤸ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥ᤹ࠣ"): bstack1l1l1l1_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨ᤺"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᤻ࠣ"): bstack1l1l1l1_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤ᤼").format(env.get(bstack1l1l1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ᤽")), env.get(bstack1l1l1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭᤾")), env.get(bstack1l1l1l1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩ᤿"))),
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᥀"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᥁")),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᥂"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨ᥃"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᥄")), env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢ᥅")), env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᥆"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᥇"): bstack1l1l1l1_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦ᥈"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᥉"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᥊")),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᥋"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᥌")),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᥍"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᥎"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ᥏")):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᥐ"): bstack1l1l1l1_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᥑ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᥒ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᥓ")),
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᥔ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᥕ")),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᥖ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᥗ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᥘ")) or env.get(bstack1l1l1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᥙ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᥚ"): bstack1l1l1l1_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᥛ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᥜ"): env.get(bstack1l1l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᥝ")),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᥞ"): bstack1l1l1l1_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᥟ") if env.get(bstack1l1l1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᥠ")) else None,
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᥡ"): env.get(bstack1l1l1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᥢ"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᥣ")), env.get(bstack1l1l1l1_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᥤ")), env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᥥ"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᥦ"): bstack1l1l1l1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᥧ"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᥨ"): None,
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᥩ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᥪ")),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᥫ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᥬ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᥭ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᥮"): bstack1l1l1l1_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦ᥯"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᥰ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᥱ")),
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᥲ"): bstack1l1l1l1_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᥳ").format(env.get(bstack1l1l1l1_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᥴ"))) if env.get(bstack1l1l1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᥵")) else None,
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᥶"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᥷"))
        }
    if bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ᥸"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᥹"): bstack1l1l1l1_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ᥺"),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᥻"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦ᥼")),
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᥽"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧ᥾")),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᥿"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᦀ"))
        }
    if bstack11ll11l1l_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᦁ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᦂ"): bstack1l1l1l1_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᦃ"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᦄ"): bstack1l1l1l1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᦅ").format(env.get(bstack1l1l1l1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᦆ")), env.get(bstack1l1l1l1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᦇ")), env.get(bstack1l1l1l1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᦈ"))),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᦉ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᦊ")),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᦋ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᦌ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡎࠨᦍ")) == bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᦎ") and env.get(bstack1l1l1l1_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᦏ")) == bstack1l1l1l1_opy_ (u"ࠨ࠱ࠣᦐ"):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦑ"): bstack1l1l1l1_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᦒ"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦓ"): bstack1l1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᦔ").format(env.get(bstack1l1l1l1_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᦕ"))),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᦖ"): None,
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦗ"): None,
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᦘ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᦙ"): bstack1l1l1l1_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᦚ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᦛ"): None,
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦜ"): env.get(bstack1l1l1l1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᦝ")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦞ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᦟ"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᦠ")), env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᦡ")), env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᦢ")), env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᦣ"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᦤ"): bstack1l1l1l1_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᦥ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᦦ"): None,
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᦧ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᦨ")) or None,
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᦩ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᦪ"), 0)
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᦫ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᦬"): bstack1l1l1l1_opy_ (u"ࠢࡈࡱࡆࡈࠧ᦭"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᦮"): None,
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᦯"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᦰ")),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᦱ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᦲ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᦳ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦴ"): bstack1l1l1l1_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᦵ"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦶ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᦷ")),
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦸ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᦹ")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦺ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᦻ"))
        }
    return {bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᦼ"): None}
def get_host_info():
    return {
        bstack1l1l1l1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᦽ"): platform.node(),
        bstack1l1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᦾ"): platform.system(),
        bstack1l1l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤᦿ"): platform.machine(),
        bstack1l1l1l1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᧀ"): platform.version(),
        bstack1l1l1l1_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᧁ"): platform.architecture()[0]
    }
def bstack1ll1l11ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll1llll11_opy_():
    if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᧂ")):
        return bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᧃ")
    return bstack1l1l1l1_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᧄ")
def bstack11ll1l111ll_opy_(driver):
    info = {
        bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᧅ"): driver.capabilities,
        bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᧆ"): driver.session_id,
        bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᧇ"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᧈ"), None),
        bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᧉ"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᧊"), None),
        bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫ᧋"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᧌"), None),
    }
    if bstack11ll1llll11_opy_() == bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᧍"):
        if bstack11ll1lll1l_opy_():
            info[bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᧎")] = bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᧏")
        elif driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᧐"), {}).get(bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ᧑"), False):
            info[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᧒")] = bstack1l1l1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ᧓")
        else:
            info[bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ᧔")] = bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᧕")
    return info
def bstack11ll1lll1l_opy_():
    if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᧖")):
        return True
    if bstack11ll11l1l_opy_(os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ᧗"), None)):
        return True
    return False
def bstack1111l1ll1_opy_(bstack11ll1l1ll1l_opy_, url, data, config):
    headers = config.get(bstack1l1l1l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᧘"), None)
    proxies = bstack1l1lll1111_opy_(config, url)
    auth = config.get(bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ᧙"), None)
    response = requests.request(
            bstack11ll1l1ll1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11llll11_opy_(bstack1ll1lll1ll_opy_, size):
    bstack1l1ll11ll1_opy_ = []
    while len(bstack1ll1lll1ll_opy_) > size:
        bstack1lll11ll_opy_ = bstack1ll1lll1ll_opy_[:size]
        bstack1l1ll11ll1_opy_.append(bstack1lll11ll_opy_)
        bstack1ll1lll1ll_opy_ = bstack1ll1lll1ll_opy_[size:]
    bstack1l1ll11ll1_opy_.append(bstack1ll1lll1ll_opy_)
    return bstack1l1ll11ll1_opy_
def bstack11ll1l11l1l_opy_(message, bstack11ll11lllll_opy_=False):
    os.write(1, bytes(message, bstack1l1l1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧚")))
    os.write(1, bytes(bstack1l1l1l1_opy_ (u"ࠫࡡࡴࠧ᧛"), bstack1l1l1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᧜")))
    if bstack11ll11lllll_opy_:
        with open(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ᧝") + os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭᧞")] + bstack1l1l1l1_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭᧟"), bstack1l1l1l1_opy_ (u"ࠩࡤࠫ᧠")) as f:
            f.write(message + bstack1l1l1l1_opy_ (u"ࠪࡠࡳ࠭᧡"))
def bstack1ll1111ll11_opy_():
    return os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᧢")].lower() == bstack1l1l1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ᧣")
def bstack11ll1llll_opy_(bstack11ll1lllll1_opy_):
    return bstack1l1l1l1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ᧤").format(bstack1l111111ll1_opy_, bstack11ll1lllll1_opy_)
def bstack1lll11llll_opy_():
    return bstack111ll1l111_opy_().replace(tzinfo=None).isoformat() + bstack1l1l1l1_opy_ (u"࡛ࠧࠩ᧥")
def bstack11lll11l1ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1l1_opy_ (u"ࠨ࡜ࠪ᧦"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1l1_opy_ (u"ࠩ࡝ࠫ᧧")))).total_seconds() * 1000
def bstack11ll1ll1l11_opy_(timestamp):
    return bstack11lll1111ll_opy_(timestamp).isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬ᧨")
def bstack11llll1l111_opy_(bstack11lll111l1l_opy_):
    date_format = bstack1l1l1l1_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ᧩")
    bstack11llllll1l1_opy_ = datetime.datetime.strptime(bstack11lll111l1l_opy_, date_format)
    return bstack11llllll1l1_opy_.isoformat() + bstack1l1l1l1_opy_ (u"ࠬࡠࠧ᧪")
def bstack11ll1ll1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᧫")
    else:
        return bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᧬")
def bstack11ll11l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᧭")
def bstack11lll1l1111_opy_(val):
    return val.__str__().lower() == bstack1l1l1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ᧮")
def bstack111ll1llll_opy_(bstack1l11111111l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l11111111l_opy_ as e:
                print(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ᧯").format(func.__name__, bstack1l11111111l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11lll1l1l11_opy_(bstack11llll1111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11llll1111l_opy_(cls, *args, **kwargs)
            except bstack1l11111111l_opy_ as e:
                print(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦ᧰").format(bstack11llll1111l_opy_.__name__, bstack1l11111111l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11lll1l1l11_opy_
    else:
        return decorator
def bstack11lllll1_opy_(bstack111l11lll1_opy_):
    if os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᧱")) is not None:
        return bstack11ll11l1l_opy_(os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ᧲")))
    if bstack1l1l1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧳") in bstack111l11lll1_opy_ and bstack11lll1l1111_opy_(bstack111l11lll1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᧴")]):
        return False
    if bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᧵") in bstack111l11lll1_opy_ and bstack11lll1l1111_opy_(bstack111l11lll1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᧶")]):
        return False
    return True
def bstack1l111l11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11ll1ll1lll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ᧷"), None)
        return bstack11ll1ll1lll_opy_ is None or bstack11ll1ll1lll_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ᧸")
    except Exception as e:
        return False
def bstack111l1l1ll_opy_(hub_url, CONFIG):
    if bstack1l11l1lll_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭᧹")):
        if hub_url:
            return bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᧺") + hub_url + bstack1l1l1l1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ᧻")
        return bstack1l11111111_opy_
    if hub_url:
        return bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᧼") + hub_url + bstack1l1l1l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ᧽")
    return bstack1ll1111ll_opy_
def bstack11lll1ll111_opy_():
    return isinstance(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ᧾")), str)
def bstack1111lll1l_opy_(url):
    return urlparse(url).hostname
def bstack1l1l111ll1_opy_(hostname):
    for bstack11l1lll1l_opy_ in bstack11l1lll11l_opy_:
        regex = re.compile(bstack11l1lll1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11lll111111_opy_(bstack11lll1l11ll_opy_, file_name, logger):
    bstack1l11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠬࢄࠧ᧿")), bstack11lll1l11ll_opy_)
    try:
        if not os.path.exists(bstack1l11lll1ll_opy_):
            os.makedirs(bstack1l11lll1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"࠭ࡾࠨᨀ")), bstack11lll1l11ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1l1_opy_ (u"ࠧࡸࠩᨁ")):
                pass
            with open(file_path, bstack1l1l1l1_opy_ (u"ࠣࡹ࠮ࠦᨂ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll1l11l_opy_.format(str(e)))
def bstack11ll1ll11ll_opy_(file_name, key, value, logger):
    file_path = bstack11lll111111_opy_(bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᨃ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lll111l_opy_ = json.load(open(file_path, bstack1l1l1l1_opy_ (u"ࠪࡶࡧ࠭ᨄ")))
        else:
            bstack1l1lll111l_opy_ = {}
        bstack1l1lll111l_opy_[key] = value
        with open(file_path, bstack1l1l1l1_opy_ (u"ࠦࡼ࠱ࠢᨅ")) as outfile:
            json.dump(bstack1l1lll111l_opy_, outfile)
def bstack1l111l11_opy_(file_name, logger):
    file_path = bstack11lll111111_opy_(bstack1l1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᨆ"), file_name, logger)
    bstack1l1lll111l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1l1_opy_ (u"࠭ࡲࠨᨇ")) as bstack1l111ll1l_opy_:
            bstack1l1lll111l_opy_ = json.load(bstack1l111ll1l_opy_)
    return bstack1l1lll111l_opy_
def bstack1ll1111ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᨈ") + file_path + bstack1l1l1l1_opy_ (u"ࠨࠢࠪᨉ") + str(e))
def bstack1l11l1lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1l1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᨊ")
def bstack111111lll_opy_(config):
    if bstack1l1l1l1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᨋ") in config:
        del (config[bstack1l1l1l1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᨌ")])
        return False
    if bstack1l11l1lll_opy_() < version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫᨍ")):
        return False
    if bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬᨎ")):
        return True
    if bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᨏ") in config and config[bstack1l1l1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨᨐ")] is False:
        return False
    else:
        return True
def bstack1ll1l111l1_opy_(args_list, bstack11ll1l111l1_opy_):
    index = -1
    for value in bstack11ll1l111l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l111llll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l111llll_opy_ = bstack11l111llll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᨑ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᨒ"), exception=exception)
    def bstack111l11l1ll_opy_(self):
        if self.result != bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᨓ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣᨔ") in self.exception_type:
            return bstack1l1l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢᨕ")
        return bstack1l1l1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᨖ")
    def bstack11lll1ll11l_opy_(self):
        if self.result != bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᨗ"):
            return None
        if self.bstack11l111llll_opy_:
            return self.bstack11l111llll_opy_
        return bstack11lllllll1l_opy_(self.exception)
def bstack11lllllll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11llll1ll1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll111l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1l1lllll_opy_(config, logger):
    try:
        import playwright
        bstack11ll1lll111_opy_ = playwright.__file__
        bstack11lll11l11l_opy_ = os.path.split(bstack11ll1lll111_opy_)
        bstack11lllllll11_opy_ = bstack11lll11l11l_opy_[0] + bstack1l1l1l1_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷᨘࠬ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ᨙ")] = bstack11ll1111ll_opy_(config)
        with open(bstack11lllllll11_opy_, bstack1l1l1l1_opy_ (u"ࠫࡷ࠭ᨚ")) as f:
            bstack1lllll11l1_opy_ = f.read()
            bstack11llll11111_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫᨛ")
            bstack11ll1ll1111_opy_ = bstack1lllll11l1_opy_.find(bstack11llll11111_opy_)
            if bstack11ll1ll1111_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1l1_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥ᨜"), shell=True, cwd=bstack11lll11l11l_opy_[0])
              process.wait()
              bstack11llll11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧ᨝")
              bstack1l1111111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧ᨞")
              bstack11lll1llll1_opy_ = bstack1lllll11l1_opy_.replace(bstack11llll11l1l_opy_, bstack1l1111111l1_opy_)
              with open(bstack11lllllll11_opy_, bstack1l1l1l1_opy_ (u"ࠩࡺࠫ᨟")) as f:
                f.write(bstack11lll1llll1_opy_)
    except Exception as e:
        logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
def bstack1111ll111_opy_():
  try:
    bstack11lll1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᨠ"))
    bstack11llll1l1ll_opy_ = []
    if os.path.exists(bstack11lll1l1lll_opy_):
      with open(bstack11lll1l1lll_opy_) as f:
        bstack11llll1l1ll_opy_ = json.load(f)
      os.remove(bstack11lll1l1lll_opy_)
    return bstack11llll1l1ll_opy_
  except:
    pass
  return []
def bstack1l1l1ll111_opy_(bstack1ll1l11lll_opy_):
  try:
    bstack11llll1l1ll_opy_ = []
    bstack11lll1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫᨡ"))
    if os.path.exists(bstack11lll1l1lll_opy_):
      with open(bstack11lll1l1lll_opy_) as f:
        bstack11llll1l1ll_opy_ = json.load(f)
    bstack11llll1l1ll_opy_.append(bstack1ll1l11lll_opy_)
    with open(bstack11lll1l1lll_opy_, bstack1l1l1l1_opy_ (u"ࠬࡽࠧᨢ")) as f:
        json.dump(bstack11llll1l1ll_opy_, f)
  except:
    pass
def bstack1ll1l111l_opy_(logger, bstack11lll1lll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᨣ"), bstack1l1l1l1_opy_ (u"ࠧࠨᨤ"))
    if test_name == bstack1l1l1l1_opy_ (u"ࠨࠩᨥ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨᨦ"), bstack1l1l1l1_opy_ (u"ࠪࠫᨧ"))
    bstack11ll1l1l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠫ࠱ࠦࠧᨨ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11lll1lll11_opy_:
        bstack1l1ll111ll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᨩ"), bstack1l1l1l1_opy_ (u"࠭࠰ࠨᨪ"))
        bstack11llllllll_opy_ = {bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᨫ"): test_name, bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᨬ"): bstack11ll1l1l1ll_opy_, bstack1l1l1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᨭ"): bstack1l1ll111ll_opy_}
        bstack11lllll11l1_opy_ = []
        bstack11llllllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᨮ"))
        if os.path.exists(bstack11llllllll1_opy_):
            with open(bstack11llllllll1_opy_) as f:
                bstack11lllll11l1_opy_ = json.load(f)
        bstack11lllll11l1_opy_.append(bstack11llllllll_opy_)
        with open(bstack11llllllll1_opy_, bstack1l1l1l1_opy_ (u"ࠫࡼ࠭ᨯ")) as f:
            json.dump(bstack11lllll11l1_opy_, f)
    else:
        bstack11llllllll_opy_ = {bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᨰ"): test_name, bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᨱ"): bstack11ll1l1l1ll_opy_, bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᨲ"): str(multiprocessing.current_process().name)}
        if bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬᨳ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11llllllll_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᨴ").format(e))
def bstack11l1l1lll_opy_(error_message, test_name, index, logger):
  try:
    bstack11lllll1l1l_opy_ = []
    bstack11llllllll_opy_ = {bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᨵ"): test_name, bstack1l1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᨶ"): error_message, bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᨷ"): index}
    bstack11lllll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᨸ"))
    if os.path.exists(bstack11lllll11ll_opy_):
        with open(bstack11lllll11ll_opy_) as f:
            bstack11lllll1l1l_opy_ = json.load(f)
    bstack11lllll1l1l_opy_.append(bstack11llllllll_opy_)
    with open(bstack11lllll11ll_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࠩᨹ")) as f:
        json.dump(bstack11lllll1l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᨺ").format(e))
def bstack1lll1l1lll_opy_(bstack11l1ll11l_opy_, name, logger):
  try:
    bstack11llllllll_opy_ = {bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᨻ"): name, bstack1l1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᨼ"): bstack11l1ll11l_opy_, bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᨽ"): str(threading.current_thread()._name)}
    return bstack11llllllll_opy_
  except Exception as e:
    logger.warn(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᨾ").format(e))
  return
def bstack11lll1lllll_opy_():
    return platform.system() == bstack1l1l1l1_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧᨿ")
def bstack11l1ll1lll_opy_(bstack11llllll111_opy_, config, logger):
    bstack11lllll1ll1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11llllll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨᩀ").format(e))
    return bstack11lllll1ll1_opy_
def bstack11lllllllll_opy_(bstack11llll11lll_opy_, bstack11lll11llll_opy_):
    bstack11lll1111l1_opy_ = version.parse(bstack11llll11lll_opy_)
    bstack11ll1ll1ll1_opy_ = version.parse(bstack11lll11llll_opy_)
    if bstack11lll1111l1_opy_ > bstack11ll1ll1ll1_opy_:
        return 1
    elif bstack11lll1111l1_opy_ < bstack11ll1ll1ll1_opy_:
        return -1
    else:
        return 0
def bstack111ll1l111_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11lll1111ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11lll11l111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1lll1ll1_opy_(options, framework, bstack11ll11l1l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1l1l1_opy_ (u"ࠨࡩࡨࡸࠬᩁ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l1llll_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᩂ"))
    bstack11ll1l11l11_opy_ = True
    bstack1l111111ll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᩃ")]
    if bstack11lll1l1111_opy_(caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡗ࠴ࡅࠪᩄ"))) or bstack11lll1l1111_opy_(caps.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬᩅ"))):
        bstack11ll1l11l11_opy_ = False
    if bstack111111lll_opy_({bstack1l1l1l1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨᩆ"): bstack11ll1l11l11_opy_}):
        bstack11l1llll_opy_ = bstack11l1llll_opy_ or {}
        bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩇ")] = bstack11lll11l111_opy_(framework)
        bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩈ")] = bstack1ll1111ll11_opy_()
        bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᩉ")] = bstack1l111111ll_opy_
        bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᩊ")] = bstack11ll11l1l1_opy_
        if getattr(options, bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬᩋ"), None):
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩌ"), bstack11l1llll_opy_)
        else:
            options[bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᩍ")] = bstack11l1llll_opy_
    else:
        if getattr(options, bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨᩎ"), None):
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩏ"), bstack11lll11l111_opy_(framework))
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩐ"), bstack1ll1111ll11_opy_())
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᩑ"), bstack1l111111ll_opy_)
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᩒ"), bstack11ll11l1l1_opy_)
        else:
            options[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᩓ")] = bstack11lll11l111_opy_(framework)
            options[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩔ")] = bstack1ll1111ll11_opy_()
            options[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦࡵࡷ࡬ࡺࡨࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᩕ")] = bstack1l111111ll_opy_
            options[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᩖ")] = bstack11ll11l1l1_opy_
    return options
def bstack11llllll11l_opy_(bstack11ll1l11lll_opy_, framework):
    bstack11ll11l1l1_opy_ = bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᩗ"))
    if bstack11ll1l11lll_opy_ and len(bstack11ll1l11lll_opy_.split(bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᩘ"))) > 1:
        ws_url = bstack11ll1l11lll_opy_.split(bstack1l1l1l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᩙ"))[0]
        if bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᩚ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11lll1l111l_opy_ = json.loads(urllib.parse.unquote(bstack11ll1l11lll_opy_.split(bstack1l1l1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᩛ"))[1]))
            bstack11lll1l111l_opy_ = bstack11lll1l111l_opy_ or {}
            bstack1l111111ll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᩜ")]
            bstack11lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᩝ")] = str(framework) + str(__version__)
            bstack11lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᩞ")] = bstack1ll1111ll11_opy_()
            bstack11lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᩟")] = bstack1l111111ll_opy_
            bstack11lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴ᩠ࠬ")] = bstack11ll11l1l1_opy_
            bstack11ll1l11lll_opy_ = bstack11ll1l11lll_opy_.split(bstack1l1l1l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᩡ"))[0] + bstack1l1l1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᩢ") + urllib.parse.quote(json.dumps(bstack11lll1l111l_opy_))
    return bstack11ll1l11lll_opy_
def bstack111lllll1_opy_():
    global bstack111l11l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack111l11l1_opy_ = BrowserType.connect
    return bstack111l11l1_opy_
def bstack1l1l1l111l_opy_(framework_name):
    global bstack1l11111ll1_opy_
    bstack1l11111ll1_opy_ = framework_name
    return framework_name
def bstack1ll1llll11_opy_(self, *args, **kwargs):
    global bstack111l11l1_opy_
    try:
        global bstack1l11111ll1_opy_
        if bstack1l1l1l1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᩣ") in kwargs:
            kwargs[bstack1l1l1l1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᩤ")] = bstack11llllll11l_opy_(
                kwargs.get(bstack1l1l1l1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᩥ"), None),
                bstack1l11111ll1_opy_
            )
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᩦ").format(str(e)))
    return bstack111l11l1_opy_(self, *args, **kwargs)
def bstack11lll1l1ll1_opy_(bstack11ll1llllll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l1lll1111_opy_(bstack11ll1llllll_opy_, bstack1l1l1l1_opy_ (u"ࠦࠧᩧ"))
        if proxies and proxies.get(bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᩨ")):
            parsed_url = urlparse(proxies.get(bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᩩ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᩪ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᩫ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᩬ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᩭ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll11l1ll_opy_(bstack11ll1llllll_opy_):
    bstack11lll11lll1_opy_ = {
        bstack1l1111l11ll_opy_[bstack11ll1l1l111_opy_]: bstack11ll1llllll_opy_[bstack11ll1l1l111_opy_]
        for bstack11ll1l1l111_opy_ in bstack11ll1llllll_opy_
        if bstack11ll1l1l111_opy_ in bstack1l1111l11ll_opy_
    }
    bstack11lll11lll1_opy_[bstack1l1l1l1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᩮ")] = bstack11lll1l1ll1_opy_(bstack11ll1llllll_opy_, bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᩯ")))
    bstack11llll1l1l1_opy_ = [element.lower() for element in bstack1l11111llll_opy_]
    bstack11ll1l1l11l_opy_(bstack11lll11lll1_opy_, bstack11llll1l1l1_opy_)
    return bstack11lll11lll1_opy_
def bstack11ll1l1l11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1l1l1_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᩰ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll1l1l11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll1l1l11l_opy_(item, keys)
def bstack11lllll1111_opy_():
    bstack11lllll1lll_opy_ = [os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤᩱ")), os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠣࢀࠥᩲ")), bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᩳ")), os.path.join(bstack1l1l1l1_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᩴ"), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᩵"))]
    for path in bstack11lllll1lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ᩶") + str(path) + bstack1l1l1l1_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤ᩷"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦ᩸") + str(path) + bstack1l1l1l1_opy_ (u"ࠣࠩࠥ᩹"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤ᩺") + str(path) + bstack1l1l1l1_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣ᩻"))
            else:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨ᩼") + str(path) + bstack1l1l1l1_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤ᩽"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ᩾") + str(path) + bstack1l1l1l1_opy_ (u"ࠢࠨ࠰᩿ࠥ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ᪀") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥ᪁"))
    logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ᪂"))
    return None
@measure(event_name=EVENTS.bstack1l111l11l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack11111111ll_opy_(binary_path, bstack1lllll11l11_opy_, bs_config):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥ᪃").format(binary_path))
    bstack11lll111l11_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭᪄")
    bstack11ll1ll11l1_opy_ = {
        bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᪅"): __version__,
        bstack1l1l1l1_opy_ (u"ࠢࡰࡵࠥ᪆"): platform.system(),
        bstack1l1l1l1_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤ᪇"): platform.machine(),
        bstack1l1l1l1_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ᪈"): bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬ᪉"),
        bstack1l1l1l1_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥ᪊"): bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᪋")
    }
    try:
        if binary_path:
            bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᪌")] = subprocess.check_output([binary_path, bstack1l1l1l1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᪍")]).strip().decode(bstack1l1l1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᪎"))
        response = requests.request(
            bstack1l1l1l1_opy_ (u"ࠩࡊࡉ࡙࠭᪏"),
            url=bstack11ll1llll_opy_(bstack1l1111ll1l1_opy_),
            headers=None,
            auth=(bs_config[bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᪐")], bs_config[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᪑")]),
            json=None,
            params=bstack11ll1ll11l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1l1l1_opy_ (u"ࠬࡻࡲ࡭ࠩ᪒") in data.keys() and bstack1l1l1l1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᪓") in data.keys():
            logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣ᪔").format(bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᪕")]))
            bstack11ll1l11111_opy_ = bstack11lll1l1l1l_opy_(data[bstack1l1l1l1_opy_ (u"ࠩࡸࡶࡱ࠭᪖")], bstack1lllll11l11_opy_)
            bstack11lll111l11_opy_ = os.path.join(bstack1lllll11l11_opy_, bstack11ll1l11111_opy_)
            os.chmod(bstack11lll111l11_opy_, 0o777) # bstack11llll111ll_opy_ permission
            return bstack11lll111l11_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡗࡉࡑࠠࡼࡿࠥ᪗").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack1l111111l1l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack11lll1l1l1l_opy_(bstack11lll111ll1_opy_, bstack11llllll1ll_opy_):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨ᪘") + str(bstack11lll111ll1_opy_) + bstack1l1l1l1_opy_ (u"ࠧࠨ᪙"))
    zip_path = os.path.join(bstack11llllll1ll_opy_, bstack1l1l1l1_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧ᪚"))
    bstack11ll1l11111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨ᪛")
    with requests.get(bstack11lll111ll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1l1l1_opy_ (u"ࠣࡹࡥࠦ᪜")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦ᪝"))
    with zipfile.ZipFile(zip_path, bstack1l1l1l1_opy_ (u"ࠪࡶࠬ᪞")) as zip_ref:
        bstack11ll1l1ll11_opy_ = zip_ref.namelist()
        if len(bstack11ll1l1ll11_opy_) > 0:
            bstack11ll1l11111_opy_ = bstack11ll1l1ll11_opy_[0] # bstack11lll1ll1l1_opy_ bstack1l1111l1l11_opy_ will be bstack11lll11111l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11llllll1ll_opy_)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥ᪟") + str(bstack11llllll1ll_opy_) + bstack1l1l1l1_opy_ (u"ࠧ࠭ࠢ᪠"))
    os.remove(zip_path)
    return bstack11ll1l11111_opy_
def get_cli_dir():
    bstack11ll1l1111l_opy_ = bstack11lllll1111_opy_()
    if bstack11ll1l1111l_opy_:
        bstack1lllll11l11_opy_ = os.path.join(bstack11ll1l1111l_opy_, bstack1l1l1l1_opy_ (u"ࠨࡣ࡭࡫ࠥ᪡"))
        if not os.path.exists(bstack1lllll11l11_opy_):
            os.makedirs(bstack1lllll11l11_opy_, mode=0o777, exist_ok=True)
        return bstack1lllll11l11_opy_
    else:
        raise FileNotFoundError(bstack1l1l1l1_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥ᪢"))
def bstack1llll111lll_opy_(bstack1lllll11l11_opy_):
    bstack1l1l1l1_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧ᪣")
    bstack11ll1l1lll1_opy_ = [
        os.path.join(bstack1lllll11l11_opy_, f)
        for f in os.listdir(bstack1lllll11l11_opy_)
        if os.path.isfile(os.path.join(bstack1lllll11l11_opy_, f)) and f.startswith(bstack1l1l1l1_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥ᪤"))
    ]
    if len(bstack11ll1l1lll1_opy_) > 0:
        return max(bstack11ll1l1lll1_opy_, key=os.path.getmtime) # get bstack1l111111111_opy_ binary
    return bstack1l1l1l1_opy_ (u"ࠥࠦ᪥")