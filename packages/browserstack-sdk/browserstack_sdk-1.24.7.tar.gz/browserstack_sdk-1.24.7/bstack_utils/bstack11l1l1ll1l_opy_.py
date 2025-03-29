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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1l11l111ll1_opy_, bstack1llll1ll_opy_, get_host_info, bstack11ll1lll1l1_opy_, \
 bstack11lllll1_opy_, bstack11ll111l_opy_, bstack111ll1llll_opy_, bstack11ll1l11l1l_opy_, bstack1lll11llll_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack11l11ll1ll_opy_ import bstack1l11l1lll1_opy_
from bstack_utils.percy import bstack1ll1111l1l_opy_
from bstack_utils.config import Config
bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll1111l1l_opy_()
@bstack111ll1llll_opy_(class_method=False)
def bstack111ll1l1l11_opy_(bs_config, bstack1l11ll1ll_opy_):
  try:
    data = {
        bstack1l1l1l1_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ᷈"): bstack1l1l1l1_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ᷉"),
        bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦ᷊ࠩ"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ᷋"), bstack1l1l1l1_opy_ (u"ࠬ࠭᷌")),
        bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᷍"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ᷎ࠪ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ᷏ࠫ"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ᷐ࠫ")),
        bstack1l1l1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ᷑"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ᷒"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᷓ")),
        bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᷔ"): bstack1lll11llll_opy_(),
        bstack1l1l1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬᷕ"): bstack11ll1lll1l1_opy_(bs_config),
        bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫᷖ"): get_host_info(),
        bstack1l1l1l1_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪᷗ"): bstack1llll1ll_opy_(),
        bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᷘ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᷙ")),
        bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪᷚ"): os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫᷛ"), False),
        bstack1l1l1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩᷜ"): bstack1l11l111ll1_opy_(),
        bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᷝ"): bstack111l1llll11_opy_(),
        bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭ᷞ"): bstack111ll1111ll_opy_(bstack1l11ll1ll_opy_),
        bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨᷟ"): bstack1ll1l111_opy_(bs_config, bstack1l11ll1ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᷠ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᷡ"))),
        bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᷢ"): bstack11lllll1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣᷣ").format(str(error)))
    return None
def bstack111ll1111ll_opy_(framework):
  return {
    bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᷤ"): framework.get(bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪᷥ"), bstack1l1l1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᷦ")),
    bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᷧ"): framework.get(bstack1l1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᷨ")),
    bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᷩ"): framework.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᷪ")),
    bstack1l1l1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᷫ"): bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᷬ"),
    bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᷭ"): framework.get(bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᷮ"))
  }
def bstack1ll1l111_opy_(bs_config, framework):
  bstack111llllll_opy_ = False
  bstack1l1l11lll1_opy_ = False
  bstack111l1lllll1_opy_ = False
  if bstack1l1l1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᷯ") in bs_config:
    bstack111l1lllll1_opy_ = True
  elif bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࠪᷰ") in bs_config:
    bstack111llllll_opy_ = True
  else:
    bstack1l1l11lll1_opy_ = True
  bstack11ll11l1l1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᷱ"): bstack1l11l1lll1_opy_.bstack111ll111111_opy_(bs_config, framework),
    bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᷲ"): bstack11111l11l_opy_.bstack1l111lll11l_opy_(bs_config),
    bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᷳ"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᷴ"), False),
    bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭᷵"): bstack1l1l11lll1_opy_,
    bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᷶"): bstack111llllll_opy_,
    bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧ᷷ࠪ"): bstack111l1lllll1_opy_
  }
  return bstack11ll11l1l1_opy_
@bstack111ll1llll_opy_(class_method=False)
def bstack111l1llll11_opy_():
  try:
    bstack111l1llllll_opy_ = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᷸"), bstack1l1l1l1_opy_ (u"ࠨࡽࢀ᷹ࠫ")))
    return {
        bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶ᷺ࠫ"): bstack111l1llllll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ᷻").format(str(error)))
    return {}
def bstack111ll11ll1l_opy_(array, bstack111ll11111l_opy_, bstack111l1lll1ll_opy_):
  result = {}
  for o in array:
    key = o[bstack111ll11111l_opy_]
    result[key] = o[bstack111l1lll1ll_opy_]
  return result
def bstack111ll11llll_opy_(bstack1l1ll11111_opy_=bstack1l1l1l1_opy_ (u"ࠫࠬ᷼")):
  bstack111l1llll1l_opy_ = bstack11111l11l_opy_.on()
  bstack111ll1111l1_opy_ = bstack1l11l1lll1_opy_.on()
  bstack111ll111l11_opy_ = percy.bstack1lllll1l1_opy_()
  if bstack111ll111l11_opy_ and not bstack111ll1111l1_opy_ and not bstack111l1llll1l_opy_:
    return bstack1l1ll11111_opy_ not in [bstack1l1l1l1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥ᷽ࠩ"), bstack1l1l1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ᷾")]
  elif bstack111l1llll1l_opy_ and not bstack111ll1111l1_opy_:
    return bstack1l1ll11111_opy_ not in [bstack1l1l1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ᷿"), bstack1l1l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪḀ"), bstack1l1l1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ḁ")]
  return bstack111l1llll1l_opy_ or bstack111ll1111l1_opy_ or bstack111ll111l11_opy_
@bstack111ll1llll_opy_(class_method=False)
def bstack111ll1ll1ll_opy_(bstack1l1ll11111_opy_, test=None):
  bstack111ll111l1l_opy_ = bstack11111l11l_opy_.on()
  if not bstack111ll111l1l_opy_ or bstack1l1ll11111_opy_ not in [bstack1l1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬḂ")] or test == None:
    return None
  return {
    bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḃ"): bstack111ll111l1l_opy_ and bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫḄ"), None) == True and bstack11111l11l_opy_.bstack1l111l111l_opy_(test[bstack1l1l1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫḅ")])
  }