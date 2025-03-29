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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack1l111llllll_opy_ as bstack1l11l11l1ll_opy_, EVENTS
from bstack_utils.bstack1l111lll1l_opy_ import bstack1l111lll1l_opy_
from bstack_utils.helper import bstack1lll11llll_opy_, bstack111ll1l111_opy_, bstack11lllll1_opy_, bstack1l111ll1l11_opy_, \
  bstack1l111lllll1_opy_, bstack1llll1ll_opy_, get_host_info, bstack1l11l111ll1_opy_, bstack1111l1ll1_opy_, bstack111ll1llll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1llllll_opy_ import get_logger
from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
logger = get_logger(__name__)
bstack1lll11lll_opy_ = bstack1lll1l1ll11_opy_()
@bstack111ll1llll_opy_(class_method=False)
def _1l11l1111l1_opy_(driver, bstack111l1ll111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1l1l1_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᒆ"): caps.get(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᒇ"), None),
        bstack1l1l1l1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᒈ"): bstack111l1ll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᒉ"), None),
        bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᒊ"): caps.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᒋ"), None),
        bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᒌ"): caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᒍ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᒎ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᒏ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᒐ")] == bstack1l1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᒑ"):
        return False
    return True
def bstack1l111lll11l_opy_(config):
  return config.get(bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒒ"), False) or any([p.get(bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᒓ"), False) == True for p in config.get(bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᒔ"), [])])
def bstack1111111l1_opy_(config, bstack1l1ll111ll_opy_):
  try:
    if not bstack11lllll1_opy_(config):
      return False
    bstack1l11l11111l_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᒕ"), False)
    if int(bstack1l1ll111ll_opy_) < len(config.get(bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᒖ"), [])) and config[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᒗ")][bstack1l1ll111ll_opy_]:
      bstack1l111lll111_opy_ = config[bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᒘ")][bstack1l1ll111ll_opy_].get(bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᒙ"), None)
    else:
      bstack1l111lll111_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᒚ"), None)
    if bstack1l111lll111_opy_ != None:
      bstack1l11l11111l_opy_ = bstack1l111lll111_opy_
    bstack1l11l111l11_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᒛ")) is not None and len(os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᒜ"))) > 0 and os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᒝ")) != bstack1l1l1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᒞ")
    return bstack1l11l11111l_opy_ and bstack1l11l111l11_opy_
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᒟ") + str(error))
  return False
def bstack1l111l111l_opy_(test_tags):
  bstack1lll1111l1l_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᒠ"))
  if bstack1lll1111l1l_opy_ is None:
    return True
  bstack1lll1111l1l_opy_ = json.loads(bstack1lll1111l1l_opy_)
  try:
    include_tags = bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᒡ")] if bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᒢ") in bstack1lll1111l1l_opy_ and isinstance(bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᒣ")], list) else []
    exclude_tags = bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᒤ")] if bstack1l1l1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᒥ") in bstack1lll1111l1l_opy_ and isinstance(bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᒦ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᒧ") + str(error))
  return False
def bstack1l111ll1ll1_opy_(config, bstack1l11l11l11l_opy_, bstack1l11l11l111_opy_, bstack1l111ll1lll_opy_):
  bstack1l11l11l1l1_opy_ = bstack1l111ll1l11_opy_(config)
  bstack1l111lll1l1_opy_ = bstack1l111lllll1_opy_(config)
  if bstack1l11l11l1l1_opy_ is None or bstack1l111lll1l1_opy_ is None:
    logger.error(bstack1l1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᒨ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᒩ"), bstack1l1l1l1_opy_ (u"ࠬࢁࡽࠨᒪ")))
    data = {
        bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᒫ"): config[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᒬ")],
        bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᒭ"): config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᒮ"), os.path.basename(os.getcwd())),
        bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᒯ"): bstack1lll11llll_opy_(),
        bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᒰ"): config.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᒱ"), bstack1l1l1l1_opy_ (u"࠭ࠧᒲ")),
        bstack1l1l1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᒳ"): {
            bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᒴ"): bstack1l11l11l11l_opy_,
            bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᒵ"): bstack1l11l11l111_opy_,
            bstack1l1l1l1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᒶ"): __version__,
            bstack1l1l1l1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᒷ"): bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒸ"),
            bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᒹ"): bstack1l1l1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᒺ"),
            bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᒻ"): bstack1l111ll1lll_opy_
        },
        bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᒼ"): settings,
        bstack1l1l1l1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᒽ"): bstack1l11l111ll1_opy_(),
        bstack1l1l1l1_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᒾ"): bstack1llll1ll_opy_(),
        bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᒿ"): get_host_info(),
        bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᓀ"): bstack11lllll1_opy_(config)
    }
    headers = {
        bstack1l1l1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᓁ"): bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᓂ"),
    }
    config = {
        bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᓃ"): (bstack1l11l11l1l1_opy_, bstack1l111lll1l1_opy_),
        bstack1l1l1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᓄ"): headers
    }
    response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩᓅ"), bstack1l11l11l1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᓆ"), data, config)
    bstack1l11l11ll1l_opy_ = response.json()
    if bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᓇ")]:
      parsed = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᓈ"), bstack1l1l1l1_opy_ (u"ࠨࡽࢀࠫᓉ")))
      parsed[bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᓊ")] = bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᓋ")][bstack1l1l1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᓌ")]
      os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᓍ")] = json.dumps(parsed)
      bstack1l111lll1l_opy_.bstack1l11l11ll11_opy_(bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᓎ")][bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᓏ")])
      bstack1l111lll1l_opy_.bstack1l11l1111ll_opy_(bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᓐ")][bstack1l1l1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᓑ")])
      bstack1l111lll1l_opy_.store()
      return bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᓒ")][bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᓓ")], bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪᓔ")][bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩᓕ")]
    else:
      logger.error(bstack1l1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᓖ") + bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᓗ")])
      if bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓘ")] == bstack1l1l1l1_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᓙ"):
        for bstack1l111lll1ll_opy_ in bstack1l11l11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᓚ")]:
          logger.error(bstack1l111lll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᓛ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᓜ") +  str(error))
    return None, None
def bstack1l111llll11_opy_():
  if os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᓝ")) is None:
    return {
        bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᓞ"): bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᓟ"),
        bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᓠ"): bstack1l1l1l1_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᓡ")
    }
  data = {bstack1l1l1l1_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᓢ"): bstack1lll11llll_opy_()}
  headers = {
      bstack1l1l1l1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᓣ"): bstack1l1l1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᓤ") + os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᓥ")),
      bstack1l1l1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᓦ"): bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᓧ")
  }
  response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡕ࡛ࡔࠨᓨ"), bstack1l11l11l1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᓩ"), data, { bstack1l1l1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᓪ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1l1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᓫ") + bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠨ࡜ࠪᓬ"))
      return {bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᓭ"): bstack1l1l1l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᓮ"), bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᓯ"): bstack1l1l1l1_opy_ (u"ࠬ࠭ᓰ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᓱ") + str(error))
    return {
        bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᓲ"): bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᓳ"),
        bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᓴ"): str(error)
    }
def bstack11ll11ll1l_opy_(caps, options, desired_capabilities={}):
  try:
    bstack1ll1l1ll1ll_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᓵ"), {}).get(bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᓶ"), caps.get(bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᓷ"), bstack1l1l1l1_opy_ (u"࠭ࠧᓸ")))
    if bstack1ll1l1ll1ll_opy_:
      logger.warn(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᓹ"))
      return False
    if options:
      bstack1l11l111l1l_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack1l11l111l1l_opy_ = desired_capabilities
    else:
      bstack1l11l111l1l_opy_ = {}
    browser = caps.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᓺ"), bstack1l1l1l1_opy_ (u"ࠩࠪᓻ")).lower() or bstack1l11l111l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᓼ"), bstack1l1l1l1_opy_ (u"ࠫࠬᓽ")).lower()
    if browser != bstack1l1l1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᓾ"):
      logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᓿ"))
      return False
    browser_version = caps.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔀ")) or caps.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᔁ")) or bstack1l11l111l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᔂ")) or bstack1l11l111l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᔃ"), {}).get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᔄ")) or bstack1l11l111l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᔅ"), {}).get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔆ"))
    if browser_version and browser_version != bstack1l1l1l1_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᔇ") and int(browser_version.split(bstack1l1l1l1_opy_ (u"ࠨ࠰ࠪᔈ"))[0]) <= 98:
      logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣ࠽࠽࠴ࠢᔉ"))
      return False
    if not options:
      bstack1ll1l1lll11_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᔊ")) or bstack1l11l111l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᔋ"), {})
      if bstack1l1l1l1_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᔌ") in bstack1ll1l1lll11_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫᔍ"), []):
        logger.warn(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᔎ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᔏ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack1lll1l11l11_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᔐ"), {})
    bstack1lll1l11l11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᔑ")] = os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᔒ"))
    bstack1l11l111111_opy_ = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᔓ"), bstack1l1l1l1_opy_ (u"࠭ࡻࡾࠩᔔ"))).get(bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔕ"))
    caps[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᔖ")] = True
    if bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᔗ") in caps:
      caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᔘ")][bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᔙ")] = bstack1lll1l11l11_opy_
      caps[bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᔚ")][bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᔛ")][bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔜ")] = bstack1l11l111111_opy_
    else:
      caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᔝ")] = bstack1lll1l11l11_opy_
      caps[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᔞ")][bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᔟ")] = bstack1l11l111111_opy_
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᔠ") +  str(error))
def bstack1l111ll11_opy_(driver, bstack1l111ll1l1l_opy_):
  try:
    setattr(driver, bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᔡ"), True)
    session = driver.session_id
    if session:
      bstack1l111llll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1l111llll1l_opy_ = False
      bstack1l111llll1l_opy_ = url.scheme in [bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡶࡳࠦᔢ"), bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᔣ")]
      if bstack1l111llll1l_opy_:
        if bstack1l111ll1l1l_opy_:
          logger.info(bstack1l1l1l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᔤ"))
      return bstack1l111ll1l1l_opy_
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᔥ") + str(e))
    return False
def bstack1l1l111lll_opy_(driver, name, path):
  try:
    bstack1ll1l1lll1l_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᔦ"): threading.current_thread().current_test_uuid,
        bstack1l1l1l1_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᔧ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᔨ"), bstack1l1l1l1_opy_ (u"࠭ࠧᔩ")),
        bstack1l1l1l1_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᔪ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᔫ"), bstack1l1l1l1_opy_ (u"ࠩࠪᔬ"))
    }
    bstack1lll11111ll_opy_ = bstack1lll11lll_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1lll1l11ll_opy_.value)
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᔭ"))
    try:
      logger.debug(driver.execute_async_script(bstack1l111lll1l_opy_.perform_scan, {bstack1l1l1l1_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᔮ"): name}))
      bstack1lll11lll_opy_.end(EVENTS.bstack1lll1l11ll_opy_.value, bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔯ"), bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔰ"), True, None)
    except Exception as error:
      bstack1lll11lll_opy_.end(EVENTS.bstack1lll1l11ll_opy_.value, bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᔱ"), bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᔲ"), False, str(error))
    bstack1lll11111ll_opy_ = bstack1lll11lll_opy_.bstack1l11l111lll_opy_(EVENTS.bstack1ll1lllll1l_opy_.value)
    bstack1lll11lll_opy_.mark(bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᔳ"))
    try:
      logger.debug(driver.execute_async_script(bstack1l111lll1l_opy_.bstack1l11l11lll1_opy_, bstack1ll1l1lll1l_opy_))
      bstack1lll11lll_opy_.end(bstack1lll11111ll_opy_, bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᔴ"), bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᔵ"),True, None)
    except Exception as error:
      bstack1lll11lll_opy_.end(bstack1lll11111ll_opy_, bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔶ"), bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔷ"),False, str(error))
    logger.info(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᔸ"))
  except Exception as bstack1ll1lll11ll_opy_:
    logger.error(bstack1l1l1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᔹ") + str(path) + bstack1l1l1l1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᔺ") + str(bstack1ll1lll11ll_opy_))