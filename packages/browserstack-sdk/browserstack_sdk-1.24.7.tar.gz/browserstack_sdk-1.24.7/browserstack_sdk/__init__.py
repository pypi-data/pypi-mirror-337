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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.measure import bstack1lll11lll_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from browserstack_sdk.bstack1lllll1l1l_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll111ll_opy_ import bstack11ll11l1_opy_
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11l111l11_opy_():
  global CONFIG
  headers = {
        bstack1l1l1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l1lll1111_opy_(CONFIG, bstack1l11l11l1_opy_)
  try:
    response = requests.get(bstack1l11l11l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1lll1lll_opy_ = response.json()[bstack1l1l1l1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111l11ll_opy_.format(response.json()))
      return bstack1lll1lll_opy_
    else:
      logger.debug(bstack11l1l1ll1_opy_.format(bstack1l1l1l1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l1l1ll1_opy_.format(e))
def bstack1ll1ll11_opy_(hub_url):
  global CONFIG
  url = bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1l1l1l1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1l1l1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l1lll1111_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11lll111l1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll1l1l_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11l1ll1l1l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack1111l1lll_opy_():
  try:
    global bstack1l1llll1ll_opy_
    bstack1lll1lll_opy_ = bstack11l111l11_opy_()
    bstack1lll1lllll_opy_ = []
    results = []
    for bstack1ll1lllll_opy_ in bstack1lll1lll_opy_:
      bstack1lll1lllll_opy_.append(bstack11ll11l11_opy_(target=bstack1ll1ll11_opy_,args=(bstack1ll1lllll_opy_,)))
    for t in bstack1lll1lllll_opy_:
      t.start()
    for t in bstack1lll1lllll_opy_:
      results.append(t.join())
    bstack1l11l1ll11_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1l1l1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1l1l1l1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l11l1ll11_opy_[hub_url] = latency
    bstack11l1lll1_opy_ = min(bstack1l11l1ll11_opy_, key= lambda x: bstack1l11l1ll11_opy_[x])
    bstack1l1llll1ll_opy_ = bstack11l1lll1_opy_
    logger.debug(bstack11l11lll_opy_.format(bstack11l1lll1_opy_))
  except Exception as e:
    logger.debug(bstack1lll1lll1_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1llllll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1ll1lll_opy_, bstack1111l1ll1_opy_, bstack11ll1llll_opy_, bstack11ll111l_opy_, \
  bstack11lllll1_opy_, \
  Notset, bstack111111lll_opy_, \
  bstack1l111l11_opy_, bstack1ll1111ll1_opy_, bstack1ll1l111l1_opy_, bstack1llll1ll_opy_, bstack1l111l11l_opy_, bstack1ll1l11ll_opy_, \
  bstack1l11ll1l_opy_, \
  bstack1l1l1lllll_opy_, bstack1111ll111_opy_, bstack1l1l1ll111_opy_, bstack1lll1l1lll_opy_, \
  bstack1ll1l111l_opy_, bstack11l1l1lll_opy_, bstack11ll11l1l_opy_, bstack11ll11l1ll_opy_
from bstack_utils.bstack1lll111lll_opy_ import bstack1ll11ll1_opy_, bstack11lll1lll1_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1l111lll11_opy_
from bstack_utils.bstack1l11l1ll1_opy_ import bstack1ll1lllll1_opy_, bstack1l1ll1l11l_opy_
from bstack_utils.bstack1l111lll1l_opy_ import bstack1l111lll1l_opy_
from bstack_utils.proxy import bstack1l111lll1_opy_, bstack1l1lll1111_opy_, bstack11ll1111ll_opy_, bstack1ll11l1l_opy_
from browserstack_sdk.bstack1ll11111l1_opy_ import *
from browserstack_sdk.bstack1111ll11l_opy_ import *
from bstack_utils.bstack1l1ll1lll1_opy_ import bstack1ll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111l1_opy_ import bstack1l11111l1_opy_, bstack1l1l1111ll_opy_, bstack1ll111lll1_opy_, bstack1ll1lll1_opy_
from browserstack_sdk.bstack11l11111_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack1l1llllll_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack1lll1lll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack1lll1llll1_opy_():
    global bstack1l1llll1ll_opy_
    try:
        bstack1l1lll1ll_opy_ = bstack1l11l1ll_opy_()
        bstack1ll1111lll_opy_(bstack1l1lll1ll_opy_)
        hub_url = bstack1l1lll1ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack1l1l1l1_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack1l1l1l1_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack1l1l1l1_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l1llll1ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1l11l1ll_opy_():
    global CONFIG
    bstack1l11l11ll_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack1l1l1l1_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack1l1l1l1_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l11l11ll_opy_, str):
        raise ValueError(bstack1l1l1l1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l1lll1ll_opy_ = bstack111l1111l_opy_(bstack1l11l11ll_opy_)
        return bstack1l1lll1ll_opy_
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack111l1111l_opy_(bstack1l11l11ll_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1ll1111l1_opy_ + bstack1l11l11ll_opy_
        auth = (CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11lll1l1_opy_ = json.loads(response.text)
            return bstack11lll1l1_opy_
    except ValueError as ve:
        logger.error(bstack1l1l1l1_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll1111lll_opy_(bstack1lll1ll111_opy_):
    global CONFIG
    if bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1lll1ll111_opy_:
        bstack1l111l111_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1l111l111_opy_)
        bstack11l1l111_opy_ = bstack1lll1ll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack11111l111_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack11l1l111_opy_)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack11111l111_opy_)
        bstack11lll1l1l_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack1l1l1l1_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack1l1l1l1_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack1l1l1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack11111l111_opy_
        }
        bstack1l111l111_opy_.update(bstack11lll1l1l_opy_)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1l111l111_opy_)
        CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1l111l111_opy_
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack11ll1111_opy_():
    bstack1l1lll1ll_opy_ = bstack1l11l1ll_opy_()
    if not bstack1l1lll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l1lll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack1l1l1l1_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack1ll1ll11l1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack1ll1l1111_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack11lllll1l_opy_
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack1l1l1l1_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack1l1l1l1_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack1l1l1l1ll_opy_ = json.loads(response.text)
                bstack1l11l111l_opy_ = bstack1l1l1l1ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack1l11l111l_opy_:
                    bstack11l1ll1ll1_opy_ = bstack1l11l111l_opy_[0]
                    build_hashed_id = bstack11l1ll1ll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11l1l1l1ll_opy_ = bstack1l11l1l11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11l1l1l1ll_opy_])
                    logger.info(bstack1ll1l11l1l_opy_.format(bstack11l1l1l1ll_opy_))
                    bstack1l11ll1l1_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1l11ll1l1_opy_ += bstack1l1l1l1_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1l11ll1l1_opy_ != bstack11l1ll1ll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack1l1l1l1l1l_opy_.format(bstack11l1ll1ll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1l11ll1l1_opy_))
                    return result
                else:
                    logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
import bstack_utils.bstack11l1l1ll1l_opy_ as bstack1ll11llll_opy_
import bstack_utils.bstack1l1ll1l111_opy_ as bstack111111111_opy_
from browserstack_sdk.sdk_cli.cli import cli
if os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack1111l11l1_opy_()
else:
  os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack1l1l1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack1l1l1111_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack11lll111l_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1111l1111_opy_ = None
CONFIG = {}
bstack11lll1ll_opy_ = {}
bstack11lllll1ll_opy_ = {}
bstack1ll111l11l_opy_ = None
bstack11l11l111_opy_ = None
bstack1ll1l1111l_opy_ = None
bstack11l1l1l11_opy_ = -1
bstack1ll11l1ll_opy_ = 0
bstack11ll11111l_opy_ = bstack1l1l1lll11_opy_
bstack1l1ll11lll_opy_ = 1
bstack11l11l11l_opy_ = False
bstack1l11llll1_opy_ = False
bstack1l11111ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ࢾ")
bstack1l1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧࢿ")
bstack1l1ll11ll_opy_ = False
bstack1lllll11ll_opy_ = True
bstack1ll11111l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨࣀ")
bstack1ll11ll11_opy_ = []
bstack1l1llll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠩࣁ")
bstack1llllll1l1_opy_ = False
bstack1111llll1_opy_ = None
bstack1llllll11l_opy_ = None
bstack1llll1llll_opy_ = None
bstack1llll1ll1_opy_ = -1
bstack1ll111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠩࢁࠫࣂ")), bstack1l1l1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack1ll11l111_opy_ = 0
bstack111l111l1_opy_ = 0
bstack1l111l1l11_opy_ = []
bstack1ll1ll11ll_opy_ = []
bstack1l1l1ll1ll_opy_ = []
bstack11l1lll111_opy_ = []
bstack111l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ࣅ")
bstack1llll11l1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧࣆ")
bstack1ll11l1lll_opy_ = False
bstack1llll1l1ll_opy_ = False
bstack11ll1l111_opy_ = {}
bstack1ll11l11ll_opy_ = None
bstack1ll1lll11_opy_ = None
bstack11lll11ll1_opy_ = None
bstack1llll111l1_opy_ = None
bstack11ll1ll1l_opy_ = None
bstack1ll1llll1_opy_ = None
bstack1l1l1llll1_opy_ = None
bstack1ll11lll11_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll1lll11l_opy_ = None
bstack11111111l_opy_ = None
bstack11l1l1ll_opy_ = None
bstack1l111llll_opy_ = None
bstack1l1111lll1_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l1lllll11_opy_ = None
bstack1ll11l11l1_opy_ = None
bstack1l1lll1l1l_opy_ = None
bstack11111ll11_opy_ = None
bstack11lll1l111_opy_ = None
bstack111l11l1_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack1lll1ll11l_opy_ = False
bstack1l1llll1_opy_ = bstack1l1l1l1_opy_ (u"ࠢࠣࣇ")
logger = bstack1l1llllll_opy_.get_logger(__name__, bstack11ll11111l_opy_)
bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
percy = bstack1ll1111l1l_opy_()
bstack11l1ll11l1_opy_ = bstack11ll11l1_opy_()
bstack11l11lll1_opy_ = bstack11l11111_opy_()
def bstack1l11l1111_opy_():
  global CONFIG
  global bstack1ll11l1lll_opy_
  global bstack1l1l1111l_opy_
  bstack11llll1l1l_opy_ = bstack111l1llll_opy_(CONFIG)
  if bstack11lllll1_opy_(CONFIG):
    if (bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in bstack11llll1l1l_opy_ and str(bstack11llll1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack1l1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1ll11l1lll_opy_ = True
    bstack1l1l1111l_opy_.bstack1ll1ll111l_opy_(bstack11llll1l1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1ll11l1lll_opy_ = True
    bstack1l1l1111l_opy_.bstack1ll1ll111l_opy_(True)
def bstack1ll11lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11l1lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1lll1l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1l1l1_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack1l1l1l1_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll11111l_opy_
      bstack1ll11111l_opy_ += bstack1l1l1l1_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1l1l111l_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack11ll111lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l1l111l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1l1l1l1_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack1l1l1l1_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack111l1lll1_opy_():
  global bstack1l1l1l1l1_opy_
  if bstack1l1l1l1l1_opy_ is None:
        bstack1l1l1l1l1_opy_ = bstack11l1lll1l1_opy_()
  bstack1l1l1l11_opy_ = bstack1l1l1l1l1_opy_
  if bstack1l1l1l11_opy_ and os.path.exists(os.path.abspath(bstack1l1l1l11_opy_)):
    fileName = bstack1l1l1l11_opy_
  if bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack1l1l1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack11ll1ll_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠩࠪࣗ")
  bstack1llll1l1l1_opy_ = os.getcwd()
  bstack11lll111_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack11l1lllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack11ll1ll_opy_)) and bstack1llll1l1l1_opy_ != bstack1l1l1l1_opy_ (u"ࠧࠨࣚ"):
    bstack11ll1ll_opy_ = os.path.join(bstack1llll1l1l1_opy_, bstack11lll111_opy_)
    if not os.path.exists(bstack11ll1ll_opy_):
      bstack11ll1ll_opy_ = os.path.join(bstack1llll1l1l1_opy_, bstack11l1lllll1_opy_)
    if bstack1llll1l1l1_opy_ != os.path.dirname(bstack1llll1l1l1_opy_):
      bstack1llll1l1l1_opy_ = os.path.dirname(bstack1llll1l1l1_opy_)
    else:
      bstack1llll1l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠢࣛ")
  bstack1l1l1l1l1_opy_ = bstack11ll1ll_opy_ if os.path.exists(bstack11ll1ll_opy_) else None
  return bstack1l1l1l1l1_opy_
def bstack1ll11111ll_opy_():
  bstack11ll1ll_opy_ = bstack111l1lll1_opy_()
  if not os.path.exists(bstack11ll1ll_opy_):
    bstack1ll11l1ll1_opy_(
      bstack11111l1ll_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll1ll_opy_, bstack1l1l1l1_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack1l1l1l1_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1l1l111l_opy_)
      yaml.add_constructor(bstack1l1l1l1_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack11ll111lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11ll1ll_opy_, bstack1l1l1l1_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1ll11l1ll1_opy_(bstack1llll1l11l_opy_.format(str(exc)))
def bstack11llllll_opy_(config):
  bstack1llllllll_opy_ = bstack11llll11l1_opy_(config)
  for option in list(bstack1llllllll_opy_):
    if option.lower() in bstack11ll1l11l1_opy_ and option != bstack11ll1l11l1_opy_[option.lower()]:
      bstack1llllllll_opy_[bstack11ll1l11l1_opy_[option.lower()]] = bstack1llllllll_opy_[option]
      del bstack1llllllll_opy_[option]
  return config
def bstack1l1111l11l_opy_():
  global bstack11lllll1ll_opy_
  for key, bstack1l11ll111l_opy_ in bstack1ll111111_opy_.items():
    if isinstance(bstack1l11ll111l_opy_, list):
      for var in bstack1l11ll111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack11lllll1ll_opy_[key] = os.environ[var]
          break
    elif bstack1l11ll111l_opy_ in os.environ and os.environ[bstack1l11ll111l_opy_] and str(os.environ[bstack1l11ll111l_opy_]).strip():
      bstack11lllll1ll_opy_[key] = os.environ[bstack1l11ll111l_opy_]
  if bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack11lllll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack11lllll1ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1lll1111ll_opy_():
  global bstack11lll1ll_opy_
  global bstack1ll11111l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1l1l1l1_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack11lll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack11lll1ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11l1llll1_opy_ in bstack1l1ll111_opy_.items():
    if isinstance(bstack11l1llll1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11l1llll1_opy_:
          if idx < len(sys.argv) and bstack1l1l1l1_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack11lll1ll_opy_:
            bstack11lll1ll_opy_[key] = sys.argv[idx + 1]
            bstack1ll11111l_opy_ += bstack1l1l1l1_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack1l1l1l1_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1l1l1l1_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11l1llll1_opy_.lower() == val.lower() and not key in bstack11lll1ll_opy_:
          bstack11lll1ll_opy_[key] = sys.argv[idx + 1]
          bstack1ll11111l_opy_ += bstack1l1l1l1_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11l1llll1_opy_ + bstack1l1l1l1_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll1l1ll_opy_(config):
  bstack1l1lllllll_opy_ = config.keys()
  for bstack1l1l1l111_opy_, bstack111ll1l1l_opy_ in bstack11l1111l_opy_.items():
    if bstack111ll1l1l_opy_ in bstack1l1lllllll_opy_:
      config[bstack1l1l1l111_opy_] = config[bstack111ll1l1l_opy_]
      del config[bstack111ll1l1l_opy_]
  for bstack1l1l1l111_opy_, bstack111ll1l1l_opy_ in bstack1ll111l1ll_opy_.items():
    if isinstance(bstack111ll1l1l_opy_, list):
      for bstack11llll11l_opy_ in bstack111ll1l1l_opy_:
        if bstack11llll11l_opy_ in bstack1l1lllllll_opy_:
          config[bstack1l1l1l111_opy_] = config[bstack11llll11l_opy_]
          del config[bstack11llll11l_opy_]
          break
    elif bstack111ll1l1l_opy_ in bstack1l1lllllll_opy_:
      config[bstack1l1l1l111_opy_] = config[bstack111ll1l1l_opy_]
      del config[bstack111ll1l1l_opy_]
  for bstack11llll11l_opy_ in list(config):
    for bstack1lllllll1_opy_ in bstack111l1l111_opy_:
      if bstack11llll11l_opy_.lower() == bstack1lllllll1_opy_.lower() and bstack11llll11l_opy_ != bstack1lllllll1_opy_:
        config[bstack1lllllll1_opy_] = config[bstack11llll11l_opy_]
        del config[bstack11llll11l_opy_]
  bstack11l1llllll_opy_ = [{}]
  if not config.get(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack11l1llllll_opy_ = config[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack11l1llllll_opy_:
    for bstack11llll11l_opy_ in list(platform):
      for bstack1lllllll1_opy_ in bstack111l1l111_opy_:
        if bstack11llll11l_opy_.lower() == bstack1lllllll1_opy_.lower() and bstack11llll11l_opy_ != bstack1lllllll1_opy_:
          platform[bstack1lllllll1_opy_] = platform[bstack11llll11l_opy_]
          del platform[bstack11llll11l_opy_]
  for bstack1l1l1l111_opy_, bstack111ll1l1l_opy_ in bstack1ll111l1ll_opy_.items():
    for platform in bstack11l1llllll_opy_:
      if isinstance(bstack111ll1l1l_opy_, list):
        for bstack11llll11l_opy_ in bstack111ll1l1l_opy_:
          if bstack11llll11l_opy_ in platform:
            platform[bstack1l1l1l111_opy_] = platform[bstack11llll11l_opy_]
            del platform[bstack11llll11l_opy_]
            break
      elif bstack111ll1l1l_opy_ in platform:
        platform[bstack1l1l1l111_opy_] = platform[bstack111ll1l1l_opy_]
        del platform[bstack111ll1l1l_opy_]
  for bstack1l1ll11l11_opy_ in bstack1l1l111l1_opy_:
    if bstack1l1ll11l11_opy_ in config:
      if not bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_] in config:
        config[bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_]] = {}
      config[bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_]].update(config[bstack1l1ll11l11_opy_])
      del config[bstack1l1ll11l11_opy_]
  for platform in bstack11l1llllll_opy_:
    for bstack1l1ll11l11_opy_ in bstack1l1l111l1_opy_:
      if bstack1l1ll11l11_opy_ in list(platform):
        if not bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_] in platform:
          platform[bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_]] = {}
        platform[bstack1l1l111l1_opy_[bstack1l1ll11l11_opy_]].update(platform[bstack1l1ll11l11_opy_])
        del platform[bstack1l1ll11l11_opy_]
  config = bstack11llllll_opy_(config)
  return config
def bstack111ll1l11_opy_(config):
  global bstack1l1l1ll1_opy_
  bstack11ll11lll1_opy_ = False
  if bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack1l1l1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack1l1lll1ll_opy_ = bstack1l11l1ll_opy_()
      if bstack1l1l1l1_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack1l1lll1ll_opy_:
        if not bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack1l1l1l1_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack11ll11lll1_opy_ = True
        bstack1l1l1ll1_opy_ = config[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack11lllll1_opy_(config) and bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack11ll11lll1_opy_:
    if not bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1lll11llll_opy_ = datetime.datetime.now()
      bstack11ll1ll1ll_opy_ = bstack1lll11llll_opy_.strftime(bstack1l1l1l1_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack1llll11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1l1l1_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack11ll1ll1ll_opy_, hostname, bstack1llll11l11_opy_)
      config[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack1l1l1ll1_opy_ = config[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack1l1l1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l1l11lll_opy_():
  bstack11llllll11_opy_ =  bstack1llll1ll_opy_()[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack11llllll11_opy_ if bstack11llllll11_opy_ else -1
def bstack1ll1llll1l_opy_(bstack11llllll11_opy_):
  global CONFIG
  if not bstack1l1l1l1_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack1l1l1l1_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack11llllll11_opy_)
  )
def bstack1l11111l11_opy_():
  global CONFIG
  if not bstack1l1l1l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1lll11llll_opy_ = datetime.datetime.now()
  bstack11ll1ll1ll_opy_ = bstack1lll11llll_opy_.strftime(bstack1l1l1l1_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack1l1l1l1_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack11ll1ll1ll_opy_
  )
def bstack111ll1ll1_opy_():
  global CONFIG
  if bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack1l1l1l1_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack1l1l1l1_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1l11111l11_opy_()
    os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack1l1l1l1_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack11llllll11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨऩ")
  bstack111l1l11l_opy_ = bstack1l1l11lll_opy_()
  if bstack111l1l11l_opy_ != -1:
    bstack11llllll11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack111l1l11l_opy_)
  if bstack11llllll11_opy_ == bstack1l1l1l1_opy_ (u"ࠩࠪफ"):
    bstack1l11llll_opy_ = bstack11lll1ll1l_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1l11llll_opy_ != -1:
      bstack11llllll11_opy_ = str(bstack1l11llll_opy_)
  if bstack11llllll11_opy_:
    bstack1ll1llll1l_opy_(bstack11llllll11_opy_)
    os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack11l1llll1l_opy_(bstack11l1l1l1_opy_, bstack1lll1l1l11_opy_, path):
  bstack1l1ll1l11_opy_ = {
    bstack1l1l1l1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1lll1l1l11_opy_
  }
  if os.path.exists(path):
    bstack1l1lll111l_opy_ = json.load(open(path, bstack1l1l1l1_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack1l1lll111l_opy_ = {}
  bstack1l1lll111l_opy_[bstack11l1l1l1_opy_] = bstack1l1ll1l11_opy_
  with open(path, bstack1l1l1l1_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack1l1lll111l_opy_, outfile)
def bstack11lll1ll1l_opy_(bstack11l1l1l1_opy_):
  bstack11l1l1l1_opy_ = str(bstack11l1l1l1_opy_)
  bstack1l11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠩࢁࠫल")), bstack1l1l1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack1l11lll1ll_opy_):
      os.makedirs(bstack1l11lll1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠫࢃ࠭ऴ")), bstack1l1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack1l1l1l1_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1l1l1_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack1l1l1l1_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1l1l1_opy_ (u"ࠩࡵࠫह")) as bstack1l111ll1l_opy_:
      bstack1l11ll111_opy_ = json.load(bstack1l111ll1l_opy_)
    if bstack11l1l1l1_opy_ in bstack1l11ll111_opy_:
      bstack11l1ll1l11_opy_ = bstack1l11ll111_opy_[bstack11l1l1l1_opy_][bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1ll1ll1ll_opy_ = int(bstack11l1ll1l11_opy_) + 1
      bstack11l1llll1l_opy_(bstack11l1l1l1_opy_, bstack1ll1ll1ll_opy_, file_path)
      return bstack1ll1ll1ll_opy_
    else:
      bstack11l1llll1l_opy_(bstack11l1l1l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll1l11l_opy_.format(str(e)))
    return -1
def bstack1ll11llll1_opy_(config):
  if not config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1lll1ll1l_opy_(config, index=0):
  global bstack1l1ll11ll_opy_
  bstack11l1llll_opy_ = {}
  caps = bstack1l1l1l11ll_opy_ + bstack1l1llllll1_opy_
  if config.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1l1ll11ll_opy_:
    caps += bstack11lll11l1l_opy_
  for key in config:
    if key in caps + [bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack11l1llll_opy_[key] = config[key]
  if bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack1l1l11ll11_opy_ in config[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack1l1l11ll11_opy_ in caps:
        continue
      bstack11l1llll_opy_[bstack1l1l11ll11_opy_] = config[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack1l1l11ll11_opy_]
  bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack1l1l1l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack11l1llll_opy_:
    del (bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack11l1llll_opy_
def bstack11ll1l1l1_opy_(config):
  global bstack1l1ll11ll_opy_
  bstack11llll1ll1_opy_ = {}
  caps = bstack1l1llllll1_opy_
  if bstack1l1ll11ll_opy_:
    caps += bstack11lll11l1l_opy_
  for key in caps:
    if key in config:
      bstack11llll1ll1_opy_[key] = config[key]
  return bstack11llll1ll1_opy_
def bstack11ll111ll1_opy_(bstack11l1llll_opy_, bstack11llll1ll1_opy_):
  bstack1111lllll_opy_ = {}
  for key in bstack11l1llll_opy_.keys():
    if key in bstack11l1111l_opy_:
      bstack1111lllll_opy_[bstack11l1111l_opy_[key]] = bstack11l1llll_opy_[key]
    else:
      bstack1111lllll_opy_[key] = bstack11l1llll_opy_[key]
  for key in bstack11llll1ll1_opy_:
    if key in bstack11l1111l_opy_:
      bstack1111lllll_opy_[bstack11l1111l_opy_[key]] = bstack11llll1ll1_opy_[key]
    else:
      bstack1111lllll_opy_[key] = bstack11llll1ll1_opy_[key]
  return bstack1111lllll_opy_
def bstack1lllll1lll_opy_(config, index=0):
  global bstack1l1ll11ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11l1l1lll1_opy_ = bstack11l1ll1lll_opy_(bstack1l1l11ll1_opy_, config, logger)
  bstack11llll1ll1_opy_ = bstack11ll1l1l1_opy_(config)
  bstack1l111l1l_opy_ = bstack1l1llllll1_opy_
  bstack1l111l1l_opy_ += bstack11l1l111l_opy_
  bstack11llll1ll1_opy_ = update(bstack11llll1ll1_opy_, bstack11l1l1lll1_opy_)
  if bstack1l1ll11ll_opy_:
    bstack1l111l1l_opy_ += bstack11lll11l1l_opy_
  if bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1lll1ll11_opy_ = bstack11l1ll1lll_opy_(bstack1l1l11ll1_opy_, config[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l111l1l_opy_ += list(bstack1lll1ll11_opy_.keys())
    for bstack1lll1111l_opy_ in bstack1l111l1l_opy_:
      if bstack1lll1111l_opy_ in config[bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack1lll1111l_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1lll1ll11_opy_[bstack1lll1111l_opy_] = str(config[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack1lll1111l_opy_] * 1.0)
          except:
            bstack1lll1ll11_opy_[bstack1lll1111l_opy_] = str(config[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack1lll1111l_opy_])
        else:
          bstack1lll1ll11_opy_[bstack1lll1111l_opy_] = config[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack1lll1111l_opy_]
        del (config[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack1lll1111l_opy_])
    bstack11llll1ll1_opy_ = update(bstack11llll1ll1_opy_, bstack1lll1ll11_opy_)
  bstack11l1llll_opy_ = bstack1lll1ll1l_opy_(config, index)
  for bstack11llll11l_opy_ in bstack1l1llllll1_opy_ + list(bstack11l1l1lll1_opy_.keys()):
    if bstack11llll11l_opy_ in bstack11l1llll_opy_:
      bstack11llll1ll1_opy_[bstack11llll11l_opy_] = bstack11l1llll_opy_[bstack11llll11l_opy_]
      del (bstack11l1llll_opy_[bstack11llll11l_opy_])
  if bstack111111lll_opy_(config):
    bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack11llll1ll1_opy_)
    caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack11l1llll_opy_
  else:
    bstack11l1llll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11ll111ll1_opy_(bstack11l1llll_opy_, bstack11llll1ll1_opy_))
    if bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack111l1l1ll_opy_():
  global bstack1l1llll1ll_opy_
  global CONFIG
  if bstack1l11l1lll_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1l1llll1ll_opy_ != bstack1l1l1l1_opy_ (u"ࠬ࠭०"):
      return bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1l1llll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack1l11111111_opy_
  if bstack1l1llll1ll_opy_ != bstack1l1l1l1_opy_ (u"ࠨࠩ३"):
    return bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1l1llll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack1ll1111ll_opy_
def bstack1ll111l11_opy_(options):
  return hasattr(options, bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11ll1l1l11_opy_(options, bstack1l1l11111_opy_):
  for bstack1ll1ll1ll1_opy_ in bstack1l1l11111_opy_:
    if bstack1ll1ll1ll1_opy_ in [bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack1l1l1l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1ll1ll1ll1_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1ll1ll1_opy_] = update(options._experimental_options[bstack1ll1ll1ll1_opy_],
                                                         bstack1l1l11111_opy_[bstack1ll1ll1ll1_opy_])
    else:
      options.add_experimental_option(bstack1ll1ll1ll1_opy_, bstack1l1l11111_opy_[bstack1ll1ll1ll1_opy_])
  if bstack1l1l1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1l1l11111_opy_:
    for arg in bstack1l1l11111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1l1l11111_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack1l1l1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1l1l11111_opy_:
    for ext in bstack1l1l11111_opy_[bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1l1l11111_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack1lll1l1l1l_opy_(options, bstack1ll11ll1l_opy_):
  if bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack1ll11ll1l_opy_:
    for bstack1l1111ll1l_opy_ in bstack1ll11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack1l1111ll1l_opy_ in options._preferences:
        options._preferences[bstack1l1111ll1l_opy_] = update(options._preferences[bstack1l1111ll1l_opy_], bstack1ll11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack1l1111ll1l_opy_])
      else:
        options.set_preference(bstack1l1111ll1l_opy_, bstack1ll11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack1l1111ll1l_opy_])
  if bstack1l1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack1ll11ll1l_opy_:
    for arg in bstack1ll11ll1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack111l1lll_opy_(options, bstack1lll111l_opy_):
  if bstack1l1l1l1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1lll111l_opy_:
    options.use_webview(bool(bstack1lll111l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack11ll1l1l11_opy_(options, bstack1lll111l_opy_)
def bstack1111ll1l_opy_(options, bstack1l11l1l1ll_opy_):
  for bstack111ll11l_opy_ in bstack1l11l1l1ll_opy_:
    if bstack111ll11l_opy_ in [bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack111ll11l_opy_, bstack1l11l1l1ll_opy_[bstack111ll11l_opy_])
  if bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack1l11l1l1ll_opy_:
    for arg in bstack1l11l1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack1l11l1l1ll_opy_:
    options.bstack1lllll1111_opy_(bool(bstack1l11l1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1l11l111_opy_(options, bstack1ll1l11l_opy_):
  for bstack1111ll11_opy_ in bstack1ll1l11l_opy_:
    if bstack1111ll11_opy_ in [bstack1l1l1l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack1l1l1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack1111ll11_opy_] = bstack1ll1l11l_opy_[bstack1111ll11_opy_]
  if bstack1l1l1l1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack1ll1l11l_opy_:
    for bstack1ll111l111_opy_ in bstack1ll1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l1l1111l1_opy_(
        bstack1ll111l111_opy_, bstack1ll1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack1ll111l111_opy_])
  if bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack1ll1l11l_opy_:
    for arg in bstack1ll1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack11l11l1l1_opy_(options, caps):
  if not hasattr(options, bstack1l1l1l1_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack1l1l1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ") and options.KEY in caps:
    bstack11ll1l1l11_opy_(options, caps[bstack1l1l1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ")])
  elif options.KEY == bstack1l1l1l1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack1lll1l1l1l_opy_(options, caps[bstack1l1l1l1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack1l1l1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬএ") and options.KEY in caps:
    bstack1111ll1l_opy_(options, caps[bstack1l1l1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ")])
  elif options.KEY == bstack1l1l1l1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack111l1lll_opy_(options, caps[bstack1l1l1l1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack1l1l1l1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧও") and options.KEY in caps:
    bstack1l11l111_opy_(options, caps[bstack1l1l1l1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ")])
def bstack1111llll_opy_(caps):
  global bstack1l1ll11ll_opy_
  if isinstance(os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫক")), str):
    bstack1l1ll11ll_opy_ = eval(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")))
  if bstack1l1ll11ll_opy_:
    if bstack1ll11lll_opy_() < version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫগ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1l1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঘ")
    if bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঙ") in caps:
      browser = caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ")]
    elif bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪছ") in caps:
      browser = caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ")]
    browser = str(browser).lower()
    if browser == bstack1l1l1l1_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঝ") or browser == bstack1l1l1l1_opy_ (u"ࠬ࡯ࡰࡢࡦࠪঞ"):
      browser = bstack1l1l1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ট")
    if browser == bstack1l1l1l1_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঠ"):
      browser = bstack1l1l1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨড")
    if browser not in [bstack1l1l1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ"), bstack1l1l1l1_opy_ (u"ࠪࡩࡩ࡭ࡥࠨণ"), bstack1l1l1l1_opy_ (u"ࠫ࡮࡫ࠧত"), bstack1l1l1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬথ"), bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧদ")]:
      return None
    try:
      package = bstack1l1l1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩধ").format(browser)
      name = bstack1l1l1l1_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩন")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll111l11_opy_(options):
        return None
      for bstack11llll11l_opy_ in caps.keys():
        options.set_capability(bstack11llll11l_opy_, caps[bstack11llll11l_opy_])
      bstack11l11l1l1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111111l11_opy_(options, bstack111111l1l_opy_):
  if not bstack1ll111l11_opy_(options):
    return
  for bstack11llll11l_opy_ in bstack111111l1l_opy_.keys():
    if bstack11llll11l_opy_ in bstack11l1l111l_opy_:
      continue
    if bstack11llll11l_opy_ in options._caps and type(options._caps[bstack11llll11l_opy_]) in [dict, list]:
      options._caps[bstack11llll11l_opy_] = update(options._caps[bstack11llll11l_opy_], bstack111111l1l_opy_[bstack11llll11l_opy_])
    else:
      options.set_capability(bstack11llll11l_opy_, bstack111111l1l_opy_[bstack11llll11l_opy_])
  bstack11l11l1l1_opy_(options, bstack111111l1l_opy_)
  if bstack1l1l1l1_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ঩") in options._caps:
    if options._caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨপ")] and options._caps[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")].lower() != bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ব"):
      del options._caps[bstack1l1l1l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬভ")]
def bstack11l11ll1_opy_(proxy_config):
  if bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম") in proxy_config:
    proxy_config[bstack1l1l1l1_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪয")] = proxy_config[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র")]
    del (proxy_config[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")])
  if bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল") in proxy_config and proxy_config[bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳")].lower() != bstack1l1l1l1_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঴"):
    proxy_config[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack1l1l1l1_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨশ")
  if bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧষ") in proxy_config:
    proxy_config[bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭স")] = bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡣࠨহ")
  return proxy_config
def bstack11llll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺") in config:
    return proxy
  config[bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻")] = bstack11l11ll1_opy_(config[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  return proxy
def bstack11l1llll11_opy_(self):
  global CONFIG
  global bstack11111111l_opy_
  try:
    proxy = bstack11ll1111ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧা")):
        proxies = bstack1l111lll1_opy_(proxy, bstack111l1l1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11l1111l_opy_ = proxies.popitem()
          if bstack1l1l1l1_opy_ (u"ࠥ࠾࠴࠵ࠢি") in bstack1l11l1111l_opy_:
            return bstack1l11l1111l_opy_
          else:
            return bstack1l1l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧী") + bstack1l11l1111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤু").format(str(e)))
  return bstack11111111l_opy_(self)
def bstack1ll1ll1l1_opy_():
  global CONFIG
  return bstack1ll11l1l_opy_(CONFIG) and bstack1ll1l11ll_opy_() and bstack1l11l1lll_opy_() >= version.parse(bstack11l11ll1l_opy_)
def bstack1l1llll1l_opy_():
  global CONFIG
  return (bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩূ") in CONFIG or bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ") in CONFIG) and bstack1l11ll1l_opy_()
def bstack11llll11l1_opy_(config):
  bstack1llllllll_opy_ = {}
  if bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬৄ") in config:
    bstack1llllllll_opy_ = config[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅")]
  if bstack1l1l1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৆") in config:
    bstack1llllllll_opy_ = config[bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে")]
  proxy = bstack11ll1111ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪৈ")) and os.path.isfile(proxy):
      bstack1llllllll_opy_[bstack1l1l1l1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৉")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")):
        proxies = bstack1l1lll1111_opy_(config, bstack111l1l1ll_opy_())
        if len(proxies) > 0:
          protocol, bstack1l11l1111l_opy_ = proxies.popitem()
          if bstack1l1l1l1_opy_ (u"ࠣ࠼࠲࠳ࠧো") in bstack1l11l1111l_opy_:
            parsed_url = urlparse(bstack1l11l1111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1l1l1_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") + bstack1l11l1111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llllllll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ্࠭")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llllllll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৎ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llllllll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৏")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llllllll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ৐")] = str(parsed_url.password)
  return bstack1llllllll_opy_
def bstack111l1llll_opy_(config):
  if bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৑") in config:
    return config[bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒")]
  return {}
def bstack11llllll1l_opy_(caps):
  global bstack1l1l1ll1_opy_
  if bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓") in caps:
    caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔")][bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ৕")] = True
    if bstack1l1l1ll1_opy_:
      caps[bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")] = bstack1l1l1ll1_opy_
  else:
    caps[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ৘")] = True
    if bstack1l1l1ll1_opy_:
      caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৙")] = bstack1l1l1ll1_opy_
@measure(event_name=EVENTS.bstack11111ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack11l1ll1ll_opy_():
  global CONFIG
  if not bstack11lllll1_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭৚") in CONFIG and bstack11ll11l1l_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛")]):
    if (
      bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨড়") in CONFIG
      and bstack11ll11l1l_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়")].get(bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৞")))
    ):
      logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣয়"))
      return
    bstack1llllllll_opy_ = bstack11llll11l1_opy_(CONFIG)
    bstack11l1ll1l1_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫৠ")], bstack1llllllll_opy_)
def bstack11l1ll1l1_opy_(key, bstack1llllllll_opy_):
  global bstack1111l1111_opy_
  logger.info(bstack1lll1l1l1_opy_)
  try:
    bstack1111l1111_opy_ = Local()
    bstack111l1ll11_opy_ = {bstack1l1l1l1_opy_ (u"ࠩ࡮ࡩࡾ࠭ৡ"): key}
    bstack111l1ll11_opy_.update(bstack1llllllll_opy_)
    logger.debug(bstack1l11ll1lll_opy_.format(str(bstack111l1ll11_opy_)).replace(key, bstack1l1l1l1_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧৢ")))
    bstack1111l1111_opy_.start(**bstack111l1ll11_opy_)
    if bstack1111l1111_opy_.isRunning():
      logger.info(bstack11lll1ll11_opy_)
  except Exception as e:
    bstack1ll11l1ll1_opy_(bstack1l1l11ll_opy_.format(str(e)))
def bstack1ll111ll11_opy_():
  global bstack1111l1111_opy_
  if bstack1111l1111_opy_.isRunning():
    logger.info(bstack11l11llll_opy_)
    bstack1111l1111_opy_.stop()
  bstack1111l1111_opy_ = None
def bstack11111l11_opy_(bstack1111l111_opy_=[]):
  global CONFIG
  bstack1ll1l1ll1l_opy_ = []
  bstack1llll111ll_opy_ = [bstack1l1l1l1_opy_ (u"ࠫࡴࡹࠧৣ"), bstack1l1l1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৤"), bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৥"), bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ০"), bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭১"), bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ২")]
  try:
    for err in bstack1111l111_opy_:
      bstack111l1l1l_opy_ = {}
      for k in bstack1llll111ll_opy_:
        val = CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৩")][int(err[bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ৪")])].get(k)
        if val:
          bstack111l1l1l_opy_[k] = val
      if(err[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")] != bstack1l1l1l1_opy_ (u"࠭ࠧ৬")):
        bstack111l1l1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৭")] = {
          err[bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭৮")]: err[bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৯")]
        }
        bstack1ll1l1ll1l_opy_.append(bstack111l1l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬৰ") + str(e))
  finally:
    return bstack1ll1l1ll1l_opy_
def bstack1l1ll1l1_opy_(file_name):
  bstack1ll1lll1l1_opy_ = []
  try:
    bstack1ll1l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1l1l1ll_opy_):
      with open(bstack1ll1l1l1ll_opy_) as f:
        bstack1l1l11ll1l_opy_ = json.load(f)
        bstack1ll1lll1l1_opy_ = bstack1l1l11ll1l_opy_
      os.remove(bstack1ll1l1l1ll_opy_)
    return bstack1ll1lll1l1_opy_
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ৱ") + str(e))
    return bstack1ll1lll1l1_opy_
def bstack1l1l111l11_opy_():
  try:
      from bstack_utils.constants import bstack1ll1ll11l_opy_, EVENTS
      from bstack_utils.helper import bstack1111l1ll1_opy_, get_host_info, bstack1l1l1111l_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack111lll11_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡨࠩ৲"), bstack1l1l1l1_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৳"))
      lock = FileLock(bstack111lll11_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৴"))
      def bstack11ll1ll111_opy_():
          try:
              with lock:
                  with open(bstack111lll11_opy_, bstack1l1l1l1_opy_ (u"ࠣࡴࠥ৵"), encoding=bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৶")) as file:
                      data = json.load(file)
                      config = {
                          bstack1l1l1l1_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৷"): {
                              bstack1l1l1l1_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৸"): bstack1l1l1l1_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ৹"),
                          }
                      }
                      bstack1l1ll1111l_opy_ = datetime.utcnow()
                      bstack1lll11llll_opy_ = bstack1l1ll1111l_opy_.strftime(bstack1l1l1l1_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥ৺"))
                      bstack11llll1ll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ৻")) if os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) else bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ৽"))
                      payload = {
                          bstack1l1l1l1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢ৾"): bstack1l1l1l1_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣ৿"),
                          bstack1l1l1l1_opy_ (u"ࠧࡪࡡࡵࡣࠥ਀"): {
                              bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਁ"): bstack11llll1ll_opy_,
                              bstack1l1l1l1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਂ"): bstack1lll11llll_opy_,
                              bstack1l1l1l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਃ"): bstack1l1l1l1_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਄"),
                              bstack1l1l1l1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢਅ"): {
                                  bstack1l1l1l1_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨਆ"): data,
                                  bstack1l1l1l1_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਇ"): bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                              },
                              bstack1l1l1l1_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਉ"): bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਊ")),
                              bstack1l1l1l1_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਋"): get_host_info()
                          }
                      }
                      response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠥࡔࡔ࡙ࡔࠣ਌"), bstack1ll1ll11l_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦ਍").format(bstack1ll1ll11l_opy_, payload))
                      else:
                          logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack1ll1ll11l_opy_, payload))
          except Exception as e:
              logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਏ").format(e))
      bstack11ll1ll111_opy_()
      bstack1ll1111ll1_opy_(bstack111lll11_opy_, logger)
  except:
    pass
def bstack1ll1l1l1_opy_():
  global bstack1l1llll1_opy_
  global bstack1ll11ll11_opy_
  global bstack1l111l1l11_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1llll11l1_opy_
  global CONFIG
  bstack11111l1l1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਐ"))
  if bstack11111l1l1_opy_ in [bstack1l1l1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ਑"), bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ਒")]:
    bstack1l1ll1ll11_opy_()
  percy.shutdown()
  if bstack1l1llll1_opy_:
    logger.warning(bstack11ll1ll1_opy_.format(str(bstack1l1llll1_opy_)))
  else:
    try:
      bstack1l1lll111l_opy_ = bstack1l111l11_opy_(bstack1l1l1l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਓ"), logger)
      if bstack1l1lll111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਔ")) and bstack1l1lll111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")).get(bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਖ")):
        logger.warning(bstack11ll1ll1_opy_.format(str(bstack1l1lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਗ")][bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਘ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.bstack111ll11ll_opy_)
  logger.info(bstack11lll111ll_opy_)
  global bstack1111l1111_opy_
  if bstack1111l1111_opy_:
    bstack1ll111ll11_opy_()
  try:
    for driver in bstack1ll11ll11_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11lllll111_opy_)
  if bstack1llll11l1_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ"):
    bstack1l1l1ll1ll_opy_ = bstack1l1ll1l1_opy_(bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਚ"))
  if bstack1llll11l1_opy_ == bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਛ") and len(bstack1ll1ll11ll_opy_) == 0:
    bstack1ll1ll11ll_opy_ = bstack1l1ll1l1_opy_(bstack1l1l1l1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਜ"))
    if len(bstack1ll1ll11ll_opy_) == 0:
      bstack1ll1ll11ll_opy_ = bstack1l1ll1l1_opy_(bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਝ"))
  bstack11lllllll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨਞ")
  if len(bstack1l111l1l11_opy_) > 0:
    bstack11lllllll_opy_ = bstack11111l11_opy_(bstack1l111l1l11_opy_)
  elif len(bstack1ll1ll11ll_opy_) > 0:
    bstack11lllllll_opy_ = bstack11111l11_opy_(bstack1ll1ll11ll_opy_)
  elif len(bstack1l1l1ll1ll_opy_) > 0:
    bstack11lllllll_opy_ = bstack11111l11_opy_(bstack1l1l1ll1ll_opy_)
  elif len(bstack11l1lll111_opy_) > 0:
    bstack11lllllll_opy_ = bstack11111l11_opy_(bstack11l1lll111_opy_)
  if bool(bstack11lllllll_opy_):
    bstack1l11lllll_opy_(bstack11lllllll_opy_)
  else:
    bstack1l11lllll_opy_()
  bstack1ll1111ll1_opy_(bstack1l1lll11ll_opy_, logger)
  if bstack11111l1l1_opy_ not in [bstack1l1l1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਟ")]:
    bstack1l1l111l11_opy_()
  bstack1l1llllll_opy_.bstack1l11l1l1_opy_(CONFIG)
  if len(bstack1l1l1ll1ll_opy_) > 0:
    sys.exit(len(bstack1l1l1ll1ll_opy_))
def bstack11ll111l1_opy_(bstack1ll11l111l_opy_, frame):
  global bstack1l1l1111l_opy_
  logger.error(bstack1ll1l11l1_opy_)
  bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਠ"), bstack1ll11l111l_opy_)
  if hasattr(signal, bstack1l1l1l1_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਡ")):
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਢ"), signal.Signals(bstack1ll11l111l_opy_).name)
  else:
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), bstack1l1l1l1_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਤ"))
  if cli.is_running():
    bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.bstack111ll11ll_opy_)
  bstack11111l1l1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਥ"))
  if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and not cli.is_enabled(CONFIG):
    bstack111111ll1_opy_.stop(bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ")))
  bstack1ll1l1l1_opy_()
  sys.exit(1)
def bstack1ll11l1ll1_opy_(err):
  logger.critical(bstack1ll111l1_opy_.format(str(err)))
  bstack1l11lllll_opy_(bstack1ll111l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1ll1l1l1_opy_)
  bstack1l1ll1ll11_opy_()
  sys.exit(1)
def bstack1l111l1111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11lllll_opy_(message, True)
  atexit.unregister(bstack1ll1l1l1_opy_)
  bstack1l1ll1ll11_opy_()
  sys.exit(1)
def bstack1ll1llll_opy_():
  global CONFIG
  global bstack11lll1ll_opy_
  global bstack11lllll1ll_opy_
  global bstack1lllll11ll_opy_
  CONFIG = bstack1ll11111ll_opy_()
  load_dotenv(CONFIG.get(bstack1l1l1l1_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਨ")))
  bstack1l1111l11l_opy_()
  bstack1lll1111ll_opy_()
  CONFIG = bstack1ll1l1ll_opy_(CONFIG)
  update(CONFIG, bstack11lllll1ll_opy_)
  update(CONFIG, bstack11lll1ll_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack111ll1l11_opy_(CONFIG)
  bstack1lllll11ll_opy_ = bstack11lllll1_opy_(CONFIG)
  os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਩")] = bstack1lllll11ll_opy_.__str__().lower()
  bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਪ"), bstack1lllll11ll_opy_)
  if (bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਫ") in CONFIG and bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in bstack11lll1ll_opy_) or (
          bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in CONFIG and bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in bstack11lllll1ll_opy_):
    if os.getenv(bstack1l1l1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਯ")):
      CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")] = os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਱"))
    else:
      if not CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤਲ"), bstack1l1l1l1_opy_ (u"ࠢࠣਲ਼")) in bstack1ll1l1lll1_opy_:
        bstack111ll1ll1_opy_()
  elif (bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਴") not in CONFIG and bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ") in CONFIG) or (
          bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack11lllll1ll_opy_ and bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") not in bstack11lll1ll_opy_):
    del (CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")])
  if bstack1ll11llll1_opy_(CONFIG):
    bstack1ll11l1ll1_opy_(bstack1ll11ll111_opy_)
  Config.bstack1l111l1l1l_opy_().bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਹ"), CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ਺")])
  bstack111llll11_opy_()
  bstack1ll1l11111_opy_()
  if bstack1l1ll11ll_opy_ and not CONFIG.get(bstack1l1l1l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ਻"), bstack1l1l1l1_opy_ (u"ࠤ਼ࠥ")) in bstack1ll1l1lll1_opy_:
    CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶࠧ਽")] = bstack11lllll11l_opy_(CONFIG)
    logger.info(bstack1l1llll111_opy_.format(CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰࠨਾ")]))
  if not bstack1lllll11ll_opy_:
    CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")] = [{}]
def bstack11lll1l11_opy_(config, bstack11ll1lll1l_opy_):
  global CONFIG
  global bstack1l1ll11ll_opy_
  CONFIG = config
  bstack1l1ll11ll_opy_ = bstack11ll1lll1l_opy_
def bstack1ll1l11111_opy_():
  global CONFIG
  global bstack1l1ll11ll_opy_
  if bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࠪੀ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1l11l1ll1l_opy_)
    bstack1l1ll11ll_opy_ = True
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ੁ"), True)
def bstack11lllll11l_opy_(config):
  bstack11llll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠩੂ")
  app = config[bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵ࠭੃")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll1l1l1l1_opy_:
      if os.path.exists(app):
        bstack11llll1lll_opy_ = bstack111l1l1l1_opy_(config, app)
      elif bstack11lll1ll1_opy_(app):
        bstack11llll1lll_opy_ = app
      else:
        bstack1ll11l1ll1_opy_(bstack11ll1ll1l1_opy_.format(app))
    else:
      if bstack11lll1ll1_opy_(app):
        bstack11llll1lll_opy_ = app
      elif os.path.exists(app):
        bstack11llll1lll_opy_ = bstack111l1l1l1_opy_(app)
      else:
        bstack1ll11l1ll1_opy_(bstack1111ll1ll_opy_)
  else:
    if len(app) > 2:
      bstack1ll11l1ll1_opy_(bstack1l1l1l1l11_opy_)
    elif len(app) == 2:
      if bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ੄") in app and bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੅") in app:
        if os.path.exists(app[bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ੆")]):
          bstack11llll1lll_opy_ = bstack111l1l1l1_opy_(config, app[bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")], app[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪੈ")])
        else:
          bstack1ll11l1ll1_opy_(bstack11ll1ll1l1_opy_.format(app))
      else:
        bstack1ll11l1ll1_opy_(bstack1l1l1l1l11_opy_)
    else:
      for key in app:
        if key in bstack1l111llll1_opy_:
          if key == bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉"):
            if os.path.exists(app[key]):
              bstack11llll1lll_opy_ = bstack111l1l1l1_opy_(config, app[key])
            else:
              bstack1ll11l1ll1_opy_(bstack11ll1ll1l1_opy_.format(app))
          else:
            bstack11llll1lll_opy_ = app[key]
        else:
          bstack1ll11l1ll1_opy_(bstack1111lll11_opy_)
  return bstack11llll1lll_opy_
def bstack11lll1ll1_opy_(bstack11llll1lll_opy_):
  import re
  bstack1l1l1llll_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੊"))
  bstack1llll11lll_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢੋ"))
  if bstack1l1l1l1_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪੌ") in bstack11llll1lll_opy_ or re.fullmatch(bstack1l1l1llll_opy_, bstack11llll1lll_opy_) or re.fullmatch(bstack1llll11lll_opy_, bstack11llll1lll_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack11ll1lll_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack111l1l1l1_opy_(config, path, bstack1ll1ll1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1l1l1_opy_ (u"ࠬࡸࡢࠨ੍")).read()).hexdigest()
  bstack111l11111_opy_ = bstack1lllll1ll1_opy_(md5_hash)
  bstack11llll1lll_opy_ = None
  if bstack111l11111_opy_:
    logger.info(bstack1ll1l1lll_opy_.format(bstack111l11111_opy_, md5_hash))
    return bstack111l11111_opy_
  bstack11ll11ll11_opy_ = datetime.datetime.now()
  bstack1ll1l1l111_opy_ = MultipartEncoder(
    fields={
      bstack1l1l1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੎"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1l1l1_opy_ (u"ࠧࡳࡤࠪ੏")), bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੐")),
      bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੑ"): bstack1ll1ll1lll_opy_
    }
  )
  response = requests.post(bstack1111l1ll_opy_, data=bstack1ll1l1l111_opy_,
                           headers={bstack1l1l1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੒"): bstack1ll1l1l111_opy_.content_type},
                           auth=(config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੓")], config[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੔")]))
  try:
    res = json.loads(response.text)
    bstack11llll1lll_opy_ = res[bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੕")]
    logger.info(bstack1l11111l_opy_.format(bstack11llll1lll_opy_))
    bstack1l1ll1lll_opy_(md5_hash, bstack11llll1lll_opy_)
    cli.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੖"), datetime.datetime.now() - bstack11ll11ll11_opy_)
  except ValueError as err:
    bstack1ll11l1ll1_opy_(bstack1l1111111_opy_.format(str(err)))
  return bstack11llll1lll_opy_
def bstack111llll11_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l1ll11lll_opy_
  bstack1llll1l1_opy_ = 1
  bstack1lllllll11_opy_ = 1
  if bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੗") in CONFIG:
    bstack1lllllll11_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘")]
  else:
    bstack1lllllll11_opy_ = bstack1lll111111_opy_(framework_name, args) or 1
  if bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼") in CONFIG:
    bstack1llll1l1_opy_ = len(CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")])
  bstack1l1ll11lll_opy_ = int(bstack1lllllll11_opy_) * int(bstack1llll1l1_opy_)
def bstack1lll111111_opy_(framework_name, args):
  if framework_name == bstack11111lll_opy_ and args and bstack1l1l1l1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪਜ਼") in args:
      bstack1l11llll1l_opy_ = args.index(bstack1l1l1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ"))
      return int(args[bstack1l11llll1l_opy_ + 1]) or 1
  return 1
def bstack1lllll1ll1_opy_(md5_hash):
  bstack11l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠧࡿࠩ੝")), bstack1l1l1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੟"))
  if os.path.exists(bstack11l111l1l_opy_):
    bstack111ll11l1_opy_ = json.load(open(bstack11l111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠪࡶࡧ࠭੠")))
    if md5_hash in bstack111ll11l1_opy_:
      bstack11ll1l1lll_opy_ = bstack111ll11l1_opy_[md5_hash]
      bstack11ll11ll1_opy_ = datetime.datetime.now()
      bstack1l111111l_opy_ = datetime.datetime.strptime(bstack11ll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੡")], bstack1l1l1l1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੢"))
      if (bstack11ll11ll1_opy_ - bstack1l111111l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11ll1l1lll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੣")]):
        return None
      return bstack11ll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪ੤")]
  else:
    return None
def bstack1l1ll1lll_opy_(md5_hash, bstack11llll1lll_opy_):
  bstack1l11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠨࢀࠪ੥")), bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੦"))
  if not os.path.exists(bstack1l11lll1ll_opy_):
    os.makedirs(bstack1l11lll1ll_opy_)
  bstack11l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠪࢂࠬ੧")), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੨"), bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੩"))
  bstack1l1lll111_opy_ = {
    bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩ੪"): bstack11llll1lll_opy_,
    bstack1l1l1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੫"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1l1l1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੬")),
    bstack1l1l1l1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੭"): str(__version__)
  }
  if os.path.exists(bstack11l111l1l_opy_):
    bstack111ll11l1_opy_ = json.load(open(bstack11l111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠪࡶࡧ࠭੮")))
  else:
    bstack111ll11l1_opy_ = {}
  bstack111ll11l1_opy_[md5_hash] = bstack1l1lll111_opy_
  with open(bstack11l111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
    json.dump(bstack111ll11l1_opy_, outfile)
def bstack1l111l1ll_opy_(self):
  return
def bstack11l1l11l1_opy_(self):
  return
def bstack1l11lll11l_opy_(self):
  global bstack11l1l1ll_opy_
  bstack11l1l1ll_opy_(self)
def bstack111ll1ll_opy_():
  global bstack1llll1llll_opy_
  bstack1llll1llll_opy_ = True
@measure(event_name=EVENTS.bstack1l1l1ll1l_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1lll11l1_opy_(self):
  global bstack1l11111ll1_opy_
  global bstack1ll111l11l_opy_
  global bstack1ll1lll11_opy_
  try:
    if bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack1l11111ll1_opy_ and self.session_id != None and bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੱ"), bstack1l1l1l1_opy_ (u"ࠧࠨੲ")) != bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩੳ"):
      bstack1lllllll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੵ")
      if bstack1lllllll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶"):
        bstack1ll1l111l_opy_(logger)
      if self != None:
        bstack1ll1lllll1_opy_(self, bstack1lllllll1l_opy_, bstack1l1l1l1_opy_ (u"ࠬ࠲ࠠࠨ੷").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1l1l1l1_opy_ (u"࠭ࠧ੸")
    if bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੹") in bstack1l11111ll1_opy_ and getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੺"), None):
      bstack1l111l1lll_opy_.bstack1l1111l1ll_opy_(self, bstack11ll1l111_opy_, logger, wait=True)
    if bstack1l1l1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ੻") in bstack1l11111ll1_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1ll1lllll1_opy_(self, bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੼"))
      bstack111111111_opy_.bstack11111ll1l_opy_(self)
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੽") + str(e))
  bstack1ll1lll11_opy_(self)
  self.session_id = None
def bstack1llllll11_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1lll1ll1_opy_
    global bstack1l11111ll1_opy_
    command_executor = kwargs.get(bstack1l1l1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੾"), bstack1l1l1l1_opy_ (u"࠭ࠧ੿"))
    bstack1lll111ll1_opy_ = False
    if type(command_executor) == str and bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઀") in command_executor:
      bstack1lll111ll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in str(getattr(command_executor, bstack1l1l1l1_opy_ (u"ࠩࡢࡹࡷࡲࠧં"), bstack1l1l1l1_opy_ (u"ࠪࠫઃ"))):
      bstack1lll111ll1_opy_ = True
    else:
      return bstack1ll11l11ll_opy_(self, *args, **kwargs)
    if bstack1lll111ll1_opy_:
      bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(CONFIG, bstack1l11111ll1_opy_)
      if kwargs.get(bstack1l1l1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ઄")):
        kwargs[bstack1l1l1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")] = bstack1lll1ll1_opy_(kwargs[bstack1l1l1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")], bstack1l11111ll1_opy_, bstack11ll11l1l1_opy_)
      elif kwargs.get(bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧઇ")):
        kwargs[bstack1l1l1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")] = bstack1lll1ll1_opy_(kwargs[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")], bstack1l11111ll1_opy_, bstack11ll11l1l1_opy_)
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥઊ").format(str(e)))
  return bstack1ll11l11ll_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l111l1ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1llllll1ll_opy_(self, command_executor=bstack1l1l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧઋ"), *args, **kwargs):
  bstack11l111ll_opy_ = bstack1llllll11_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l11l1lll1_opy_.on():
    return bstack11l111ll_opy_
  try:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩઌ").format(str(command_executor)))
    logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨઍ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઎") in command_executor._url:
      bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩએ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬઐ") in command_executor):
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫઑ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1llllll1l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ઒"), None)
  if bstack1l1l1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬઓ") in bstack1l11111ll1_opy_ or bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ") in bstack1l11111ll1_opy_:
    bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
  if bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack1l11111ll1_opy_ and bstack1llllll1l_opy_ and bstack1llllll1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ"), bstack1l1l1l1_opy_ (u"ࠩࠪગ")) == bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫઘ"):
    bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
  return bstack11l111ll_opy_
def bstack111lll1ll_opy_(args):
  return bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઙ") in str(args)
def bstack1llll11ll_opy_(self, driver_command, *args, **kwargs):
  global bstack11111ll11_opy_
  global bstack1lll1ll11l_opy_
  bstack1lll1111l1_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩચ"), None) and bstack11ll111l_opy_(
          threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬછ"), None)
  bstack11111111_opy_ = getattr(self, bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧજ"), None) != None and getattr(self, bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨઝ"), None) == True
  if not bstack1lll1ll11l_opy_ and bstack1lllll11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩઞ") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪટ")] == True and bstack1l111lll1l_opy_.bstack11lllll11_opy_(driver_command) and (bstack11111111_opy_ or bstack1lll1111l1_opy_) and not bstack111lll1ll_opy_(args):
    try:
      bstack1lll1ll11l_opy_ = True
      logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ઠ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪડ").format(str(err)))
    bstack1lll1ll11l_opy_ = False
  response = bstack11111ll11_opy_(self, driver_command, *args, **kwargs)
  if (bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઢ") in str(bstack1l11111ll1_opy_).lower() or bstack1l1l1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧણ") in str(bstack1l11111ll1_opy_).lower()) and bstack1l11l1lll1_opy_.on():
    try:
      if driver_command == bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬત"):
        bstack111111ll1_opy_.bstack11llll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨથ"): response[bstack1l1l1l1_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩદ")],
            bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫધ"): bstack111111ll1_opy_.current_test_uuid() if bstack111111ll1_opy_.current_test_uuid() else bstack1l11l1lll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack11ll1111l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1lll11l1l_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll1ll1l1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack1ll111l11l_opy_
  global bstack11l1l1l11_opy_
  global bstack1ll1l1111l_opy_
  global bstack11l11l11l_opy_
  global bstack1l11llll1_opy_
  global bstack1l11111ll1_opy_
  global bstack1ll11l11ll_opy_
  global bstack1ll11ll11_opy_
  global bstack1llll1ll1_opy_
  global bstack11ll1l111_opy_
  CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧન")] = str(bstack1l11111ll1_opy_) + str(__version__)
  bstack1l111111ll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ઩")]
  bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(CONFIG, bstack1l11111ll1_opy_)
  CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪપ")] = bstack1l111111ll_opy_
  CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪફ")] = bstack11ll11l1l1_opy_
  command_executor = bstack111l1l1ll_opy_()
  logger.debug(bstack1lll111ll_opy_.format(command_executor))
  proxy = bstack11llll1l_opy_(CONFIG, proxy)
  bstack1l1ll111ll_opy_ = 0 if bstack11l1l1l11_opy_ < 0 else bstack11l1l1l11_opy_
  try:
    if bstack11l11l11l_opy_ is True:
      bstack1l1ll111ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l11llll1_opy_ is True:
      bstack1l1ll111ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1l1ll111ll_opy_ = 0
  bstack111111l1l_opy_ = bstack1lllll1lll_opy_(CONFIG, bstack1l1ll111ll_opy_)
  logger.debug(bstack11l1l11ll_opy_.format(str(bstack111111l1l_opy_)))
  if bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭બ") in CONFIG and bstack11ll11l1l_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧભ")]):
    bstack11llllll1l_opy_(bstack111111l1l_opy_)
  if bstack11111l11l_opy_.bstack1111111l1_opy_(CONFIG, bstack1l1ll111ll_opy_) and bstack11111l11l_opy_.bstack11ll11ll1l_opy_(bstack111111l1l_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if cli.accessibility is None or not cli.accessibility.is_enabled():
      bstack11111l11l_opy_.set_capabilities(bstack111111l1l_opy_, CONFIG)
  if desired_capabilities:
    bstack11l111lll_opy_ = bstack1ll1l1ll_opy_(desired_capabilities)
    bstack11l111lll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫમ")] = bstack111111lll_opy_(CONFIG)
    bstack111lllll_opy_ = bstack1lllll1lll_opy_(bstack11l111lll_opy_)
    if bstack111lllll_opy_:
      bstack111111l1l_opy_ = update(bstack111lllll_opy_, bstack111111l1l_opy_)
    desired_capabilities = None
  if options:
    bstack111111l11_opy_(options, bstack111111l1l_opy_)
  if not options:
    options = bstack1111llll_opy_(bstack111111l1l_opy_)
  bstack11ll1l111_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨય"))[bstack1l1ll111ll_opy_]
  if proxy and bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ર")):
    options.proxy(proxy)
  if options and bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭઱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l11l1lll_opy_() < version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧલ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack111111l1l_opy_)
  logger.info(bstack11lll11l11_opy_)
  bstack1lll11lll_opy_.end(EVENTS.bstack11l1ll111_opy_.value, EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤળ"), EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઴"), status=True, failure=None, test_name=bstack1ll1l1111l_opy_)
  if bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫવ")):
    bstack1ll11l11ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫશ")):
    bstack1ll11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ષ")):
    bstack1ll11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1ll11l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1ll1l11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨસ")
    if bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩહ")):
      bstack1ll1l11lll_opy_ = self.caps.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ઺"))
    else:
      bstack1ll1l11lll_opy_ = self.capabilities.get(bstack1l1l1l1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ઻"))
    if bstack1ll1l11lll_opy_:
      bstack1l1l1ll111_opy_(bstack1ll1l11lll_opy_)
      if bstack1l11l1lll_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳઼ࠫ")):
        self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨઽ") + bstack1l1llll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥા")
      else:
        self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤિ") + bstack1ll1l11lll_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤી")
      logger.debug(bstack1l1l1ll1l1_opy_.format(bstack1ll1l11lll_opy_))
    else:
      logger.debug(bstack11l1ll11ll_opy_.format(bstack1l1l1l1_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥુ")))
  except Exception as e:
    logger.debug(bstack11l1ll11ll_opy_.format(e))
  if bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૂ") in bstack1l11111ll1_opy_:
    bstack1llll11ll1_opy_(bstack11l1l1l11_opy_, bstack1llll1ll1_opy_)
  bstack1ll111l11l_opy_ = self.session_id
  if bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫૃ") in bstack1l11111ll1_opy_ or bstack1l1l1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬૄ") in bstack1l11111ll1_opy_ or bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬૅ") in bstack1l11111ll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1llllll1l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡔࡦࡵࡷࡑࡪࡺࡡࠨ૆"), None)
  if bstack1l1l1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨે") in bstack1l11111ll1_opy_ or bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨૈ") in bstack1l11111ll1_opy_:
    bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
  if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪૉ") in bstack1l11111ll1_opy_ and bstack1llllll1l_opy_ and bstack1llllll1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ૊"), bstack1l1l1l1_opy_ (u"ࠬ࠭ો")) == bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧૌ"):
    bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
  bstack1ll11ll11_opy_.append(self)
  if bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵ્ࠪ") in CONFIG and bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૎") in CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૏")][bstack1l1ll111ll_opy_]:
    bstack1ll1l1111l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૐ")][bstack1l1ll111ll_opy_][bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૑")]
  logger.debug(bstack1111ll1l1_opy_.format(bstack1ll111l11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack11ll1111_opy_
    def bstack111ll1lll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1llllll1l1_opy_
      if(bstack1l1l1l1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ૒") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"࠭ࡾࠨ૓")), bstack1l1l1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ૔"), bstack1l1l1l1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ૕")), bstack1l1l1l1_opy_ (u"ࠩࡺࠫ૖")) as fp:
          fp.write(bstack1l1l1l1_opy_ (u"ࠥࠦ૗"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૘")))):
          with open(args[1], bstack1l1l1l1_opy_ (u"ࠬࡸࠧ૙")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1l1l1_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬ૚") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l1l1111_opy_)
            if bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ૛") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ૜")]).lower() != bstack1l1l1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ૝"):
                bstack111l11lll_opy_ = bstack11ll1111_opy_()
                bstack11lll111l_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠫࠬࠐ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࠻ࠋࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡁࠊࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡁࠊࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻ࠋ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࡲࡥࡵࠢࡦࡥࡵࡹ࠻ࠋࠢࠣࡸࡷࡿࠠࡼࡽࠍࠤࠥࠦࠠࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࠾ࠎࠥࠦࡽࡾࠢࡦࡥࡹࡩࡨࠡࠪࡨࡼ࠮ࠦࡻࡼࠌࠣࠤࠥࠦࡣࡰࡰࡶࡳࡱ࡫࠮ࡦࡴࡵࡳࡷ࠮ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠻ࠤ࠯ࠤࡪࡾࠩ࠼ࠌࠣࠤࢂࢃࠊࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡿࠏࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࠨࡽࡦࡨࡵ࡛ࡲ࡭ࡿࠪࠤ࠰ࠦࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭࠱ࠐࠠࠡࠢࠣ࠲࠳࠴࡬ࡢࡷࡱࡧ࡭ࡕࡰࡵ࡫ࡲࡲࡸࠐࠠࠡࡿࢀ࠭ࡀࠐࡽࡾ࠽ࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࠧࠨࠩ૞").format(bstack111l11lll_opy_=bstack111l11lll_opy_)
            lines.insert(1, bstack11lll111l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨ૟")), bstack1l1l1l1_opy_ (u"ࠬࡽࠧૠ")) as bstack1l1llll1l1_opy_:
              bstack1l1llll1l1_opy_.writelines(lines)
        CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨૡ")] = str(bstack1l11111ll1_opy_) + str(__version__)
        bstack1l111111ll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬૢ")]
        bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(CONFIG, bstack1l11111ll1_opy_)
        CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫૣ")] = bstack1l111111ll_opy_
        CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ૤")] = bstack11ll11l1l1_opy_
        bstack1l1ll111ll_opy_ = 0 if bstack11l1l1l11_opy_ < 0 else bstack11l1l1l11_opy_
        try:
          if bstack11l11l11l_opy_ is True:
            bstack1l1ll111ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l11llll1_opy_ is True:
            bstack1l1ll111ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1l1ll111ll_opy_ = 0
        CONFIG[bstack1l1l1l1_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ૥")] = False
        CONFIG[bstack1l1l1l1_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ૦")] = True
        bstack111111l1l_opy_ = bstack1lllll1lll_opy_(CONFIG, bstack1l1ll111ll_opy_)
        logger.debug(bstack11l1l11ll_opy_.format(str(bstack111111l1l_opy_)))
        if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ૧")):
          bstack11llllll1l_opy_(bstack111111l1l_opy_)
        if bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૨") in CONFIG and bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૩") in CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૪")][bstack1l1ll111ll_opy_]:
          bstack1ll1l1111l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ૫")][bstack1l1ll111ll_opy_][bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ૬")]
        args.append(os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠫࢃ࠭૭")), bstack1l1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ૮"), bstack1l1l1l1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ૯")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack111111l1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1l1l1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ૰"))
      bstack1llllll1l1_opy_ = True
      return bstack1l1111lll1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11lll1111l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1l1l11_opy_
    global bstack1ll1l1111l_opy_
    global bstack11l11l11l_opy_
    global bstack1l11llll1_opy_
    global bstack1l11111ll1_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ૱")] = str(bstack1l11111ll1_opy_) + str(__version__)
    bstack1l111111ll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ૲")]
    bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(CONFIG, bstack1l11111ll1_opy_)
    CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭૳")] = bstack1l111111ll_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭૴")] = bstack11ll11l1l1_opy_
    bstack1l1ll111ll_opy_ = 0 if bstack11l1l1l11_opy_ < 0 else bstack11l1l1l11_opy_
    try:
      if bstack11l11l11l_opy_ is True:
        bstack1l1ll111ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l11llll1_opy_ is True:
        bstack1l1ll111ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1l1ll111ll_opy_ = 0
    CONFIG[bstack1l1l1l1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ૵")] = True
    bstack111111l1l_opy_ = bstack1lllll1lll_opy_(CONFIG, bstack1l1ll111ll_opy_)
    logger.debug(bstack11l1l11ll_opy_.format(str(bstack111111l1l_opy_)))
    if CONFIG.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ૶")):
      bstack11llllll1l_opy_(bstack111111l1l_opy_)
    if bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷") in CONFIG and bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૸") in CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬૹ")][bstack1l1ll111ll_opy_]:
      bstack1ll1l1111l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૺ")][bstack1l1ll111ll_opy_][bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩૻ")]
    import urllib
    import json
    if bstack1l1l1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩૼ") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ૽")]).lower() != bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭૾"):
        bstack11ll111l11_opy_ = bstack11ll1111_opy_()
        bstack111l11lll_opy_ = bstack11ll111l11_opy_ + urllib.parse.quote(json.dumps(bstack111111l1l_opy_))
    else:
        bstack111l11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ૿") + urllib.parse.quote(json.dumps(bstack111111l1l_opy_))
    browser = self.connect(bstack111l11lll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l11ll11l_opy_():
    global bstack1llllll1l1_opy_
    global bstack1l11111ll1_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1llll11_opy_
        global bstack1l1l1111l_opy_
        if not bstack1lllll11ll_opy_:
          global bstack111l11l1_opy_
          if not bstack111l11l1_opy_:
            from bstack_utils.helper import bstack111lllll1_opy_, bstack1l1l1l111l_opy_, bstack11ll1lllll_opy_
            bstack111l11l1_opy_ = bstack111lllll1_opy_()
            bstack1l1l1l111l_opy_(bstack1l11111ll1_opy_)
            bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(CONFIG, bstack1l11111ll1_opy_)
            bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦ଀"), bstack11ll11l1l1_opy_)
          BrowserType.connect = bstack1ll1llll11_opy_
          return
        BrowserType.launch = bstack11lll1111l_opy_
        bstack1llllll1l1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111ll1lll_opy_
      bstack1llllll1l1_opy_ = True
    except Exception as e:
      pass
def bstack11l1lllll_opy_(context, bstack1l1ll1llll_opy_):
  try:
    context.page.evaluate(bstack1l1l1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦଁ"), bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨଂ")+ json.dumps(bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠧࢃࡽࠣଃ"))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀ࠾ࠥࢁࡽࠣ଄").format(str(e), traceback.format_exc()))
def bstack11lll1l1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1l1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଅ"), bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଆ") + json.dumps(message) + bstack1l1l1l1_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬଇ") + json.dumps(level) + bstack1l1l1l1_opy_ (u"ࠪࢁࢂ࠭ଈ"))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃ࠺ࠡࡽࢀࠦଉ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11ll1ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1lll1ll1_opy_(self, url):
  global bstack1l111llll_opy_
  try:
    bstack1111l1l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1l11l111_opy_.format(str(err)))
  try:
    bstack1l111llll_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1111111l_opy_ = str(e)
      if any(err_msg in bstack1l1111111l_opy_ for err_msg in bstack1llll11111_opy_):
        bstack1111l1l1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1l11l111_opy_.format(str(err)))
    raise e
def bstack1l111111_opy_(self):
  global bstack1llllll11l_opy_
  bstack1llllll11l_opy_ = self
  return
def bstack1l111ll11l_opy_(self):
  global bstack1111llll1_opy_
  bstack1111llll1_opy_ = self
  return
def bstack1ll111ll_opy_(test_name, bstack1ll11l1111_opy_):
  global CONFIG
  if percy.bstack1lllll1l1_opy_() == bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥଊ"):
    bstack1l1l111ll_opy_ = os.path.relpath(bstack1ll11l1111_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1l111ll_opy_)
    bstack1lllll1ll_opy_ = suite_name + bstack1l1l1l1_opy_ (u"ࠨ࠭ࠣଋ") + test_name
    threading.current_thread().percySessionName = bstack1lllll1ll_opy_
def bstack1l111l11l1_opy_(self, test, *args, **kwargs):
  global bstack11lll11ll1_opy_
  test_name = None
  bstack1ll11l1111_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll11l1111_opy_ = str(test.source)
  bstack1ll111ll_opy_(test_name, bstack1ll11l1111_opy_)
  bstack11lll11ll1_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l111lllll_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack111l1l11_opy_(driver, bstack1lllll1ll_opy_):
  if not bstack1ll11l1lll_opy_ and bstack1lllll1ll_opy_:
      bstack1lll1l1ll1_opy_ = {
          bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଌ"): bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ଍"),
          bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ଎"): {
              bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨଏ"): bstack1lllll1ll_opy_
          }
      }
      bstack11ll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩଐ").format(json.dumps(bstack1lll1l1ll1_opy_))
      driver.execute_script(bstack11ll1l11_opy_)
  if bstack11l11l111_opy_:
      bstack11111lll1_opy_ = {
          bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ଑"): bstack1l1l1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ଒"),
          bstack1l1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଓ"): {
              bstack1l1l1l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଔ"): bstack1lllll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫକ"),
              bstack1l1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଖ"): bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩଗ")
          }
      }
      if bstack11l11l111_opy_.status == bstack1l1l1l1_opy_ (u"ࠬࡖࡁࡔࡕࠪଘ"):
          bstack11lllllll1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫଙ").format(json.dumps(bstack11111lll1_opy_))
          driver.execute_script(bstack11lllllll1_opy_)
          bstack1ll1lllll1_opy_(driver, bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧଚ"))
      elif bstack11l11l111_opy_.status == bstack1l1l1l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ଛ"):
          reason = bstack1l1l1l1_opy_ (u"ࠤࠥଜ")
          bstack1l1lllll1l_opy_ = bstack1lllll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫଝ")
          if bstack11l11l111_opy_.message:
              reason = str(bstack11l11l111_opy_.message)
              bstack1l1lllll1l_opy_ = bstack1l1lllll1l_opy_ + bstack1l1l1l1_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫଞ") + reason
          bstack11111lll1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଟ")] = {
              bstack1l1l1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬଠ"): bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ଡ"),
              bstack1l1l1l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ଢ"): bstack1l1lllll1l_opy_
          }
          bstack11lllllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧଣ").format(json.dumps(bstack11111lll1_opy_))
          driver.execute_script(bstack11lllllll1_opy_)
          bstack1ll1lllll1_opy_(driver, bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪତ"), reason)
          bstack11l1l1lll_opy_(reason, str(bstack11l11l111_opy_), str(bstack11l1l1l11_opy_), logger)
@measure(event_name=EVENTS.bstack111l11ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack11ll1lll11_opy_(driver, test):
  if percy.bstack1lllll1l1_opy_() == bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤଥ") and percy.bstack11ll1l1ll_opy_() == bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢଦ"):
      bstack111ll1111_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଧ"), None)
      bstack1l1l11l1l1_opy_(driver, bstack111ll1111_opy_, test)
  if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫନ"), None) and bstack11ll111l_opy_(
          threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ଩"), None):
      logger.info(bstack1l1l1l1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠡࠤପ"))
      bstack11111l11l_opy_.bstack1l1l111lll_opy_(driver, name=test.name, path=test.source)
def bstack1ll1lll1l_opy_(test, bstack1lllll1ll_opy_):
    try:
      bstack11ll11ll11_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨଫ")] = bstack1lllll1ll_opy_
      if bstack11l11l111_opy_:
        if bstack11l11l111_opy_.status == bstack1l1l1l1_opy_ (u"ࠫࡕࡇࡓࡔࠩବ"):
          data[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬଭ")] = bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ମ")
        elif bstack11l11l111_opy_.status == bstack1l1l1l1_opy_ (u"ࠧࡇࡃࡌࡐࠬଯ"):
          data[bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨର")] = bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଱")
          if bstack11l11l111_opy_.message:
            data[bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪଲ")] = str(bstack11l11l111_opy_.message)
      user = CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ଳ")]
      key = CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ଴")]
      url = bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫଵ").format(user, key, bstack1ll111l11l_opy_)
      headers = {
        bstack1l1l1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ଶ"): bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫଷ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡶࡲࡧࡥࡹ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸࠨସ"), datetime.datetime.now() - bstack11ll11ll11_opy_)
    except Exception as e:
      logger.error(bstack1l1111l1l1_opy_.format(str(e)))
def bstack1l11l111ll_opy_(test, bstack1lllll1ll_opy_):
  global CONFIG
  global bstack1111llll1_opy_
  global bstack1llllll11l_opy_
  global bstack1ll111l11l_opy_
  global bstack11l11l111_opy_
  global bstack1ll1l1111l_opy_
  global bstack1llll111l1_opy_
  global bstack11ll1ll1l_opy_
  global bstack1ll1llll1_opy_
  global bstack11lll1l111_opy_
  global bstack1ll11ll11_opy_
  global bstack11ll1l111_opy_
  try:
    if not bstack1ll111l11l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠪࢂࠬହ")), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ଺"), bstack1l1l1l1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ଻"))) as f:
        bstack1lllll11_opy_ = json.loads(bstack1l1l1l1_opy_ (u"ࠨࡻ଼ࠣ") + f.read().strip() + bstack1l1l1l1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩଽ") + bstack1l1l1l1_opy_ (u"ࠣࡿࠥା"))
        bstack1ll111l11l_opy_ = bstack1lllll11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll11ll11_opy_:
    for driver in bstack1ll11ll11_opy_:
      if bstack1ll111l11l_opy_ == driver.session_id:
        if test:
          bstack11ll1lll11_opy_(driver, test)
        bstack111l1l11_opy_(driver, bstack1lllll1ll_opy_)
  elif bstack1ll111l11l_opy_:
    bstack1ll1lll1l_opy_(test, bstack1lllll1ll_opy_)
  if bstack1111llll1_opy_:
    bstack11ll1ll1l_opy_(bstack1111llll1_opy_)
  if bstack1llllll11l_opy_:
    bstack1ll1llll1_opy_(bstack1llllll11l_opy_)
  if bstack1llll1llll_opy_:
    bstack11lll1l111_opy_()
def bstack111l1111_opy_(self, test, *args, **kwargs):
  bstack1lllll1ll_opy_ = None
  if test:
    bstack1lllll1ll_opy_ = str(test.name)
  bstack1l11l111ll_opy_(test, bstack1lllll1ll_opy_)
  bstack1llll111l1_opy_(self, test, *args, **kwargs)
def bstack1l11ll11l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1llll1_opy_
  global CONFIG
  global bstack1ll11ll11_opy_
  global bstack1ll111l11l_opy_
  bstack1l1ll1l1l1_opy_ = None
  try:
    if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨି"), None):
      try:
        if not bstack1ll111l11l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠪࢂࠬୀ")), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫୁ"), bstack1l1l1l1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧୂ"))) as f:
            bstack1lllll11_opy_ = json.loads(bstack1l1l1l1_opy_ (u"ࠨࡻࠣୃ") + f.read().strip() + bstack1l1l1l1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩୄ") + bstack1l1l1l1_opy_ (u"ࠣࡿࠥ୅"))
            bstack1ll111l11l_opy_ = bstack1lllll11_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll11ll11_opy_:
        for driver in bstack1ll11ll11_opy_:
          if bstack1ll111l11l_opy_ == driver.session_id:
            bstack1l1ll1l1l1_opy_ = driver
    bstack1l111ll1ll_opy_ = bstack11111l11l_opy_.bstack1l111l111l_opy_(test.tags)
    if bstack1l1ll1l1l1_opy_:
      threading.current_thread().isA11yTest = bstack11111l11l_opy_.bstack1l111ll11_opy_(bstack1l1ll1l1l1_opy_, bstack1l111ll1ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l111ll1ll_opy_
  except:
    pass
  bstack1l1l1llll1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l11l111_opy_
  try:
    bstack11l11l111_opy_ = self._test
  except:
    bstack11l11l111_opy_ = self.test
def bstack1llll11l1l_opy_():
  global bstack1ll111l1l_opy_
  try:
    if os.path.exists(bstack1ll111l1l_opy_):
      os.remove(bstack1ll111l1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୆") + str(e))
def bstack11ll11l111_opy_():
  global bstack1ll111l1l_opy_
  bstack1l1lll111l_opy_ = {}
  try:
    if not os.path.isfile(bstack1ll111l1l_opy_):
      with open(bstack1ll111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠪࡻࠬେ")):
        pass
      with open(bstack1ll111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠦࡼ࠱ࠢୈ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1ll111l1l_opy_):
      bstack1l1lll111l_opy_ = json.load(open(bstack1ll111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠬࡸࡢࠨ୉")))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୊") + str(e))
  finally:
    return bstack1l1lll111l_opy_
def bstack1llll11ll1_opy_(platform_index, item_index):
  global bstack1ll111l1l_opy_
  try:
    bstack1l1lll111l_opy_ = bstack11ll11l111_opy_()
    bstack1l1lll111l_opy_[item_index] = platform_index
    with open(bstack1ll111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠢࡸ࠭ࠥୋ")) as outfile:
      json.dump(bstack1l1lll111l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ୌ") + str(e))
def bstack1l1111lll_opy_(bstack1l1111ll1_opy_):
  global CONFIG
  bstack111l11l1l_opy_ = bstack1l1l1l1_opy_ (u"୍ࠩࠪ")
  if not bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୎") in CONFIG:
    logger.info(bstack1l1l1l1_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ୏"))
  try:
    platform = CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୐")][bstack1l1111ll1_opy_]
    if bstack1l1l1l1_opy_ (u"࠭࡯ࡴࠩ୑") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"ࠧࡰࡵࠪ୒")]) + bstack1l1l1l1_opy_ (u"ࠨ࠮ࠣࠫ୓")
    if bstack1l1l1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ୔") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭୕")]) + bstack1l1l1l1_opy_ (u"ࠫ࠱ࠦࠧୖ")
    if bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩୗ") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ୘")]) + bstack1l1l1l1_opy_ (u"ࠧ࠭ࠢࠪ୙")
    if bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ୚") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ୛")]) + bstack1l1l1l1_opy_ (u"ࠪ࠰ࠥ࠭ଡ଼")
    if bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଢ଼") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୞")]) + bstack1l1l1l1_opy_ (u"࠭ࠬࠡࠩୟ")
    if bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨୠ") in platform:
      bstack111l11l1l_opy_ += str(platform[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩୡ")]) + bstack1l1l1l1_opy_ (u"ࠩ࠯ࠤࠬୢ")
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪୣ") + str(e))
  finally:
    if bstack111l11l1l_opy_[len(bstack111l11l1l_opy_) - 2:] == bstack1l1l1l1_opy_ (u"ࠫ࠱ࠦࠧ୤"):
      bstack111l11l1l_opy_ = bstack111l11l1l_opy_[:-2]
    return bstack111l11l1l_opy_
def bstack1l1ll1l1ll_opy_(path, bstack111l11l1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll11ll11_opy_ = ET.parse(path)
    bstack1ll1l111ll_opy_ = bstack1lll11ll11_opy_.getroot()
    bstack11ll11lll_opy_ = None
    for suite in bstack1ll1l111ll_opy_.iter(bstack1l1l1l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୥")):
      if bstack1l1l1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୦") in suite.attrib:
        suite.attrib[bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ୧")] += bstack1l1l1l1_opy_ (u"ࠨࠢࠪ୨") + bstack111l11l1l_opy_
        bstack11ll11lll_opy_ = suite
    bstack1ll1111111_opy_ = None
    for robot in bstack1ll1l111ll_opy_.iter(bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୩")):
      bstack1ll1111111_opy_ = robot
    bstack11l11111l_opy_ = len(bstack1ll1111111_opy_.findall(bstack1l1l1l1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୪")))
    if bstack11l11111l_opy_ == 1:
      bstack1ll1111111_opy_.remove(bstack1ll1111111_opy_.findall(bstack1l1l1l1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ୫"))[0])
      bstack11ll111l1l_opy_ = ET.Element(bstack1l1l1l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୬"), attrib={bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ୭"): bstack1l1l1l1_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ୮"), bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫ୯"): bstack1l1l1l1_opy_ (u"ࠩࡶ࠴ࠬ୰")})
      bstack1ll1111111_opy_.insert(1, bstack11ll111l1l_opy_)
      bstack111lll111_opy_ = None
      for suite in bstack1ll1111111_opy_.iter(bstack1l1l1l1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩୱ")):
        bstack111lll111_opy_ = suite
      bstack111lll111_opy_.append(bstack11ll11lll_opy_)
      bstack11ll1l1l1l_opy_ = None
      for status in bstack11ll11lll_opy_.iter(bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ୲")):
        bstack11ll1l1l1l_opy_ = status
      bstack111lll111_opy_.append(bstack11ll1l1l1l_opy_)
    bstack1lll11ll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ୳") + str(e))
def bstack1lll1l11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll11l11l1_opy_
  global CONFIG
  if bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥ୴") in options:
    del options[bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦ୵")]
  bstack1l1ll1l11_opy_ = bstack11ll11l111_opy_()
  for bstack11l1lll11_opy_ in bstack1l1ll1l11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨ୶"), str(bstack11l1lll11_opy_), bstack1l1l1l1_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭୷"))
    bstack1l1ll1l1ll_opy_(path, bstack1l1111lll_opy_(bstack1l1ll1l11_opy_[bstack11l1lll11_opy_]))
  bstack1llll11l1l_opy_()
  return bstack1ll11l11l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1l1lll1l_opy_(self, ff_profile_dir):
  global bstack1ll11lll11_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll11lll11_opy_(self, ff_profile_dir)
def bstack1ll1ll111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l1l1ll1_opy_
  bstack11ll1ll11l_opy_ = []
  if bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୸") in CONFIG:
    bstack11ll1ll11l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1l1l1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ୺")],
      pabot_args[bstack1l1l1l1_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢ୻")],
      argfile,
      pabot_args.get(bstack1l1l1l1_opy_ (u"ࠢࡩ࡫ࡹࡩࠧ୼")),
      pabot_args[bstack1l1l1l1_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦ୽")],
      platform[0],
      bstack1l1l1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1l1l1_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ୾")] or [(bstack1l1l1l1_opy_ (u"ࠥࠦ୿"), None)]
    for platform in enumerate(bstack11ll1ll11l_opy_)
  ]
def bstack1ll1l1l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll11l1l1_opy_=bstack1l1l1l1_opy_ (u"ࠫࠬ஀")):
  global bstack11ll11ll_opy_
  self.platform_index = platform_index
  self.bstack11lll1lll_opy_ = bstack1ll11l1l1_opy_
  bstack11ll11ll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1lll111l1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lll11l_opy_
  global bstack1ll11111l_opy_
  bstack1llll1ll1l_opy_ = copy.deepcopy(item)
  if not bstack1l1l1l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ஁") in item.options:
    bstack1llll1ll1l_opy_.options[bstack1l1l1l1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨஂ")] = []
  bstack11l1l11l_opy_ = bstack1llll1ll1l_opy_.options[bstack1l1l1l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩஃ")].copy()
  for v in bstack1llll1ll1l_opy_.options[bstack1l1l1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஄")]:
    if bstack1l1l1l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨஅ") in v:
      bstack11l1l11l_opy_.remove(v)
    if bstack1l1l1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪஆ") in v:
      bstack11l1l11l_opy_.remove(v)
    if bstack1l1l1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨஇ") in v:
      bstack11l1l11l_opy_.remove(v)
  bstack11l1l11l_opy_.insert(0, bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧஈ").format(bstack1llll1ll1l_opy_.platform_index))
  bstack11l1l11l_opy_.insert(0, bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭உ").format(bstack1llll1ll1l_opy_.bstack11lll1lll_opy_))
  bstack1llll1ll1l_opy_.options[bstack1l1l1l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩஊ")] = bstack11l1l11l_opy_
  if bstack1ll11111l_opy_:
    bstack1llll1ll1l_opy_.options[bstack1l1l1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ஋")].insert(0, bstack1l1l1l1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬ஌").format(bstack1ll11111l_opy_))
  return bstack1ll1lll11l_opy_(caller_id, datasources, is_last, bstack1llll1ll1l_opy_, outs_dir)
def bstack1llll111_opy_(command, item_index):
  if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ஍")):
    os.environ[bstack1l1l1l1_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬஎ")] = json.dumps(CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨஏ")][item_index % bstack1ll11l1ll_opy_])
  global bstack1ll11111l_opy_
  if bstack1ll11111l_opy_:
    command[0] = command[0].replace(bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஐ"), bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫ஑") + str(
      item_index) + bstack1l1l1l1_opy_ (u"ࠨࠢࠪஒ") + bstack1ll11111l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨஓ"),
                                    bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧஔ") + str(item_index), 1)
def bstack11ll11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l1ll11l1_opy_
  bstack1llll111_opy_(command, item_index)
  return bstack1l1ll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l1l1ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l1ll11l1_opy_
  bstack1llll111_opy_(command, item_index)
  return bstack1l1ll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l11l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l1ll11l1_opy_
  bstack1llll111_opy_(command, item_index)
  return bstack1l1ll11l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack111lll1l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1ll11l1l_opy_
  bstack1llll111l_opy_ = bstack1l1ll11l1l_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫக")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩ஖")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1llll111l_opy_
def bstack1ll11l11l_opy_(runner, hook_name, context, element, bstack11lllll1l1_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack11l11lll1_opy_.bstack1ll11l1l11_opy_(hook_name, element)
    bstack11lllll1l1_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack11l11lll1_opy_.bstack1l11ll1ll1_opy_(element)
      if hook_name not in [bstack1l1l1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ஗"), bstack1l1l1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ஘")] and args and hasattr(args[0], bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨங")):
        args[0].error_message = bstack1l1l1l1_opy_ (u"ࠩࠪச")
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬ஛").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, hook_type=bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢஜ"), bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack11llllll1_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    if runner.hooks.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ஝")).__name__ != bstack1l1l1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤஞ"):
      bstack1ll11l11l_opy_(runner, name, context, runner, bstack11lllll1l1_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack11l11ll11_opy_(bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ட")) else context.browser
      runner.driver_initialised = bstack1l1l1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஠")
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭஡").format(str(e)))
def bstack1lll11111l_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    bstack1ll11l11l_opy_(runner, name, context, context.feature, bstack11lllll1l1_opy_, *args)
    try:
      if not bstack1ll11l1lll_opy_:
        bstack1l1ll1l1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ஢")) else context.browser
        if is_driver_active(bstack1l1ll1l1l1_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧண")
          bstack1l1ll1llll_opy_ = str(runner.feature.name)
          bstack11l1lllll_opy_(context, bstack1l1ll1llll_opy_)
          bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪத") + json.dumps(bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"࠭ࡽࡾࠩ஥"))
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ஦").format(str(e)))
def bstack1ll111ll1_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    if hasattr(context, bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪ஧")):
        bstack11l11lll1_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫந")) else context.feature
    bstack1ll11l11l_opy_(runner, name, context, target, bstack11lllll1l1_opy_, *args)
@measure(event_name=EVENTS.bstack1l1l1lll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack111ll1l1_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    if len(context.scenario.tags) == 0: bstack11l11lll1_opy_.start_test(context)
    bstack1ll11l11l_opy_(runner, name, context, context.scenario, bstack11lllll1l1_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack111111111_opy_.bstack1l11l1l111_opy_(context, *args)
    try:
      bstack1l1ll1l1l1_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩன"), context.browser)
      if is_driver_active(bstack1l1ll1l1l1_opy_):
        bstack111111ll1_opy_.bstack1l111111l1_opy_(bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪப"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ஫")
        if (not bstack1ll11l1lll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l1ll1llll_opy_ = str(runner.feature.name)
          bstack1l1ll1llll_opy_ = feature_name + bstack1l1l1l1_opy_ (u"࠭ࠠ࠮ࠢࠪ஬") + scenario_name
          if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ஭"):
            bstack11l1lllll_opy_(context, bstack1l1ll1llll_opy_)
            bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ம") + json.dumps(bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠩࢀࢁࠬய"))
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫர").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, hook_type=bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡗࡹ࡫ࡰࠣற"), bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1111lll1_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    bstack1ll11l11l_opy_(runner, name, context, args[0], bstack11lllll1l1_opy_, *args)
    try:
      bstack1l1ll1l1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll11_opy_(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫல")) else context.browser
      if is_driver_active(bstack1l1ll1l1l1_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1l1l1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦள")
        bstack11l11lll1_opy_.bstack1lll1l1111_opy_(args[0])
        if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧழ"):
          feature_name = bstack1l1ll1llll_opy_ = str(runner.feature.name)
          bstack1l1ll1llll_opy_ = feature_name + bstack1l1l1l1_opy_ (u"ࠨࠢ࠰ࠤࠬவ") + context.scenario.name
          bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧஶ") + json.dumps(bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠪࢁࢂ࠭ஷ"))
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨஸ").format(str(e)))
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, hook_type=bstack1l1l1l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡗࡹ࡫ࡰࠣஹ"), bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack111ll111l_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
  bstack11l11lll1_opy_.bstack1l1l11l11_opy_(args[0])
  try:
    bstack1l1111l111_opy_ = args[0].status.name
    bstack1l1ll1l1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ஺") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1ll1l1l1_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ஻")
        feature_name = bstack1l1ll1llll_opy_ = str(runner.feature.name)
        bstack1l1ll1llll_opy_ = feature_name + bstack1l1l1l1_opy_ (u"ࠨࠢ࠰ࠤࠬ஼") + context.scenario.name
        bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ஽") + json.dumps(bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠪࢁࢂ࠭ா"))
    if str(bstack1l1111l111_opy_).lower() == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫி"):
      bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ீ")
      bstack11l11l11_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧு")
      bstack1lll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨூ")
      try:
        import traceback
        bstack1l1l11l11l_opy_ = runner.exception.__class__.__name__
        bstack1l11111ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠢࠪ௃").join(bstack1l11111ll_opy_)
        bstack1lll1l11_opy_ = bstack1l11111ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1lllll_opy_.format(str(e)))
      bstack1l1l11l11l_opy_ += bstack1lll1l11_opy_
      bstack11lll1l1ll_opy_(context, json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௄") + str(bstack11l11l11_opy_)),
                          bstack1l1l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௅"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤெ"):
        bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡨࡧࠪே"), None), bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨை"), bstack1l1l11l11l_opy_)
        bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௉") + json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢொ") + str(bstack11l11l11_opy_)) + bstack1l1l1l1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩோ"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣௌ"):
        bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ்ࠫ"), bstack1l1l1l1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௎") + str(bstack1l1l11l11l_opy_))
    else:
      bstack11lll1l1ll_opy_(context, bstack1l1l1l1_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ௏"), bstack1l1l1l1_opy_ (u"ࠢࡪࡰࡩࡳࠧௐ"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௑"):
        bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௒"), None), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ௓"))
      bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௔") + json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ௕")) + bstack1l1l1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௖"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧௗ"):
        bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௘"))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ௙").format(str(e)))
  bstack1ll11l11l_opy_(runner, name, context, args[0], bstack11lllll1l1_opy_, *args)
@measure(event_name=EVENTS.bstack111l1ll1l_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1ll1ll1111_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
  bstack11l11lll1_opy_.end_test(args[0])
  try:
    bstack11lll1l1l1_opy_ = args[0].status.name
    bstack1l1ll1l1l1_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௚"), context.browser)
    bstack111111111_opy_.bstack11111ll1l_opy_(bstack1l1ll1l1l1_opy_)
    if str(bstack11lll1l1l1_opy_).lower() == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௛"):
      bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭௜")
      bstack11l11l11_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧ௝")
      bstack1lll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨ௞")
      try:
        import traceback
        bstack1l1l11l11l_opy_ = runner.exception.__class__.__name__
        bstack1l11111ll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack11l11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠢࠪ௟").join(bstack1l11111ll_opy_)
        bstack1lll1l11_opy_ = bstack1l11111ll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l1lllll_opy_.format(str(e)))
      bstack1l1l11l11l_opy_ += bstack1lll1l11_opy_
      bstack11lll1l1ll_opy_(context, json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௠") + str(bstack11l11l11_opy_)),
                          bstack1l1l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௡"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௢") or runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௣"):
        bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡩࡨࠫ௤"), None), bstack1l1l1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ௥"), bstack1l1l11l11l_opy_)
        bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௦") + json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௧") + str(bstack11l11l11_opy_)) + bstack1l1l1l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ௨"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௩") or runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௪"):
        bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௫"), bstack1l1l1l1_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ௬") + str(bstack1l1l11l11l_opy_))
    else:
      bstack11lll1l1ll_opy_(context, bstack1l1l1l1_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ௭"), bstack1l1l1l1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ௮"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௯") or runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௰"):
        bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡨࡧࠪ௱"), None), bstack1l1l1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ௲"))
      bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ௳") + json.dumps(str(args[0].name) + bstack1l1l1l1_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ௴")) + bstack1l1l1l1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ௵"))
      if runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௶") or runner.driver_initialised == bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௷"):
        bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ௸"))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ௹").format(str(e)))
  bstack1ll11l11l_opy_(runner, name, context, context.scenario, bstack11lllll1l1_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11l1ll1l_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    target = context.scenario if hasattr(context, bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ௺")) else context.feature
    bstack1ll11l11l_opy_(runner, name, context, target, bstack11lllll1l1_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1ll1ll1l_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    try:
      bstack1l1ll1l1l1_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧ௻"), context.browser)
      bstack11l1ll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠩࠪ௼")
      if context.failed is True:
        bstack1l1llll11_opy_ = []
        bstack1l1lll1l1_opy_ = []
        bstack111l111ll_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1llll11_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l11111ll_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll1111_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠤࠬ௽").join(bstack1l11111ll_opy_)
            bstack1l1lll1l1_opy_.append(bstack1l1ll1111_opy_)
            bstack111l111ll_opy_.append(bstack1l11111ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1lllll_opy_.format(str(e)))
        bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠫࠬ௾")
        for i in range(len(bstack1l1llll11_opy_)):
          bstack1l1l11l11l_opy_ += bstack1l1llll11_opy_[i] + bstack111l111ll_opy_[i] + bstack1l1l1l1_opy_ (u"ࠬࡢ࡮ࠨ௿")
        bstack11l1ll11l_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠠࠨఀ").join(bstack1l1lll1l1_opy_)
        if runner.driver_initialised in [bstack1l1l1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఁ"), bstack1l1l1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧం")]:
          bstack11lll1l1ll_opy_(context, bstack11l1ll11l_opy_, bstack1l1l1l1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣః"))
          bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఄ"), None), bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఅ"), bstack1l1l11l11l_opy_)
          bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఆ") + json.dumps(bstack11l1ll11l_opy_) + bstack1l1l1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ఇ"))
          bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఈ"), bstack1l1l1l1_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨఉ") + str(bstack1l1l11l11l_opy_))
          bstack11llllllll_opy_ = bstack1lll1l1lll_opy_(bstack11l1ll11l_opy_, runner.feature.name, logger)
          if (bstack11llllllll_opy_ != None):
            bstack11l1lll111_opy_.append(bstack11llllllll_opy_)
      else:
        if runner.driver_initialised in [bstack1l1l1l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥఊ"), bstack1l1l1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢఋ")]:
          bstack11lll1l1ll_opy_(context, bstack1l1l1l1_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢఌ") + str(runner.feature.name) + bstack1l1l1l1_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢ఍"), bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦఎ"))
          bstack1l1ll1l11l_opy_(getattr(context, bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡪࡩࠬఏ"), None), bstack1l1l1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఐ"))
          bstack1l1ll1l1l1_opy_.execute_script(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ఑") + json.dumps(bstack1l1l1l1_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨఒ") + str(runner.feature.name) + bstack1l1l1l1_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨఓ")) + bstack1l1l1l1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఔ"))
          bstack1ll1lllll1_opy_(bstack1l1ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭క"))
          bstack11llllllll_opy_ = bstack1lll1l1lll_opy_(bstack11l1ll11l_opy_, runner.feature.name, logger)
          if (bstack11llllllll_opy_ != None):
            bstack11l1lll111_opy_.append(bstack11llllllll_opy_)
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩఖ").format(str(e)))
    bstack1ll11l11l_opy_(runner, name, context, context.feature, bstack11lllll1l1_opy_, *args)
@measure(event_name=EVENTS.bstack1ll111l1l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, hook_type=bstack1l1l1l1_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥగ"), bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1lll11111_opy_(runner, name, context, bstack11lllll1l1_opy_, *args):
    bstack1ll11l11l_opy_(runner, name, context, runner, bstack11lllll1l1_opy_, *args)
def bstack1lll11ll1l_opy_(self, name, context, *args):
  if bstack1lllll11ll_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1ll11l1ll_opy_
    bstack1ll1l1l11l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఘ")][platform_index]
    os.environ[bstack1l1l1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫఙ")] = json.dumps(bstack1ll1l1l11l_opy_)
  global bstack11lllll1l1_opy_
  if not hasattr(self, bstack1l1l1l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩచ")):
    self.driver_initialised = None
  bstack1l1l1l1l_opy_ = {
      bstack1l1l1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩఛ"): bstack11llllll1_opy_,
      bstack1l1l1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧజ"): bstack1lll11111l_opy_,
      bstack1l1l1l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫఝ"): bstack1ll111ll1_opy_,
      bstack1l1l1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪఞ"): bstack111ll1l1_opy_,
      bstack1l1l1l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧట"): bstack1111lll1_opy_,
      bstack1l1l1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧఠ"): bstack111ll111l_opy_,
      bstack1l1l1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬడ"): bstack1ll1ll1111_opy_,
      bstack1l1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨఢ"): bstack11l1ll1l_opy_,
      bstack1l1l1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ణ"): bstack1ll1ll1l_opy_,
      bstack1l1l1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪత"): bstack1lll11111_opy_
  }
  handler = bstack1l1l1l1l_opy_.get(name, bstack11lllll1l1_opy_)
  handler(self, name, context, bstack11lllll1l1_opy_, *args)
  if name in [bstack1l1l1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨథ"), bstack1l1l1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪద"), bstack1l1l1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭ధ")]:
    try:
      bstack1l1ll1l1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll11_opy_(bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪన")) else context.browser
      bstack1ll11lllll_opy_ = (
        (name == bstack1l1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ఩") and self.driver_initialised == bstack1l1l1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥప")) or
        (name == bstack1l1l1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧఫ") and self.driver_initialised == bstack1l1l1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤబ")) or
        (name == bstack1l1l1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪభ") and self.driver_initialised in [bstack1l1l1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧమ"), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦయ")]) or
        (name == bstack1l1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩర") and self.driver_initialised == bstack1l1l1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦఱ"))
      )
      if bstack1ll11lllll_opy_:
        self.driver_initialised = None
        bstack1l1ll1l1l1_opy_.quit()
    except Exception:
      pass
def bstack11l1l1l1l_opy_(config, startdir):
  return bstack1l1l1l1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧల").format(bstack1l1l1l1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢళ"))
notset = Notset()
def bstack1llllll111_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lll111l1_opy_
  if str(name).lower() == bstack1l1l1l1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩఴ"):
    return bstack1l1l1l1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤవ")
  else:
    return bstack1lll111l1_opy_(self, name, default, skip)
def bstack1ll11l11_opy_(item, when):
  global bstack1l1lllll11_opy_
  try:
    bstack1l1lllll11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11llllll_opy_():
  return
def bstack1lll1ll1ll_opy_(type, name, status, reason, bstack11lll1111_opy_, bstack1l11lllll1_opy_):
  bstack1lll1l1ll1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫశ"): type,
    bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨష"): {}
  }
  if type == bstack1l1l1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨస"):
    bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪహ")][bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ఺")] = bstack11lll1111_opy_
    bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ఻")][bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨ఼")] = json.dumps(str(bstack1l11lllll1_opy_))
  if type == bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬఽ"):
    bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨా")][bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫి")] = name
  if type == bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪీ"):
    bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫు")][bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩూ")] = status
    if status == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪృ"):
      bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧౄ")][bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౅")] = json.dumps(str(reason))
  bstack11ll1l11_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫె").format(json.dumps(bstack1lll1l1ll1_opy_))
  return bstack11ll1l11_opy_
def bstack111l1ll1_opy_(driver_command, response):
    if driver_command == bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫే"):
        bstack111111ll1_opy_.bstack11llll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧై"): response[bstack1l1l1l1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ౉")],
            bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪొ"): bstack111111ll1_opy_.current_test_uuid()
        })
def bstack1ll11lll1l_opy_(item, call, rep):
  global bstack1l1lll1l1l_opy_
  global bstack1ll11ll11_opy_
  global bstack1ll11l1lll_opy_
  name = bstack1l1l1l1_opy_ (u"ࠫࠬో")
  try:
    if rep.when == bstack1l1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪౌ"):
      bstack1ll111l11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll11l1lll_opy_:
          name = str(rep.nodeid)
          bstack111lll1l_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫్ࠧ"), name, bstack1l1l1l1_opy_ (u"ࠧࠨ౎"), bstack1l1l1l1_opy_ (u"ࠨࠩ౏"), bstack1l1l1l1_opy_ (u"ࠩࠪ౐"), bstack1l1l1l1_opy_ (u"ࠪࠫ౑"))
          threading.current_thread().bstack11l1111ll_opy_ = name
          for driver in bstack1ll11ll11_opy_:
            if bstack1ll111l11l_opy_ == driver.session_id:
              driver.execute_script(bstack111lll1l_opy_)
      except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ౒").format(str(e)))
      try:
        bstack1ll1l1llll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1l1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭౓"):
          status = bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭౔") if rep.outcome.lower() == bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪౕࠧ") else bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨౖ")
          reason = bstack1l1l1l1_opy_ (u"ࠩࠪ౗")
          if status == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪౘ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩౙ") if status == bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬౚ") else bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౛")
          data = name + bstack1l1l1l1_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ౜") if status == bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨౝ") else name + bstack1l1l1l1_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ౞") + reason
          bstack1ll1l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ౟"), bstack1l1l1l1_opy_ (u"ࠫࠬౠ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ౡ"), bstack1l1l1l1_opy_ (u"࠭ࠧౢ"), level, data)
          for driver in bstack1ll11ll11_opy_:
            if bstack1ll111l11l_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1l11l11_opy_)
      except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫౣ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ౤").format(str(e)))
  bstack1l1lll1l1l_opy_(item, call, rep)
def bstack1l1l11l1l1_opy_(driver, bstack11l1ll111l_opy_, test=None):
  global bstack11l1l1l11_opy_
  if test != None:
    bstack1lllll11l_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౥"), None)
    bstack111ll111_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ౦"), None)
    PercySDK.screenshot(driver, bstack11l1ll111l_opy_, bstack1lllll11l_opy_=bstack1lllll11l_opy_, bstack111ll111_opy_=bstack111ll111_opy_, bstack11lll11l1_opy_=bstack11l1l1l11_opy_)
  else:
    PercySDK.screenshot(driver, bstack11l1ll111l_opy_)
@measure(event_name=EVENTS.bstack1l1l1lll_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1111l1_opy_(driver):
  if bstack11l1ll11l1_opy_.bstack111111l1_opy_() is True or bstack11l1ll11l1_opy_.capturing() is True:
    return
  bstack11l1ll11l1_opy_.bstack11ll1l1ll1_opy_()
  while not bstack11l1ll11l1_opy_.bstack111111l1_opy_():
    bstack11lll11ll_opy_ = bstack11l1ll11l1_opy_.bstack1l1l1ll11l_opy_()
    bstack1l1l11l1l1_opy_(driver, bstack11lll11ll_opy_)
  bstack11l1ll11l1_opy_.bstack1ll1l1ll11_opy_()
def bstack1l11l11ll1_opy_(sequence, driver_command, response = None, bstack1l11l1l11l_opy_ = None, args = None):
    try:
      if sequence != bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ౧"):
        return
      if percy.bstack1lllll1l1_opy_() == bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ౨"):
        return
      bstack11lll11ll_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౩"), None)
      for command in bstack11ll1l1111_opy_:
        if command == driver_command:
          for driver in bstack1ll11ll11_opy_:
            bstack1l1111l1_opy_(driver)
      bstack11ll1lll1_opy_ = percy.bstack11ll1l1ll_opy_()
      if driver_command in bstack1l1lll1l11_opy_[bstack11ll1lll1_opy_]:
        bstack11l1ll11l1_opy_.bstack1l1l1l1111_opy_(bstack11lll11ll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1lll1lll1l_opy_(framework_name):
  if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ౪")):
      return
  bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ౫"), True)
  global bstack1l11111ll1_opy_
  global bstack1llllll1l1_opy_
  global bstack1llll1l1ll_opy_
  bstack1l11111ll1_opy_ = framework_name
  logger.info(bstack1l111l1l1_opy_.format(bstack1l11111ll1_opy_.split(bstack1l1l1l1_opy_ (u"ࠩ࠰ࠫ౬"))[0]))
  bstack1l11l1111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1lllll11ll_opy_:
      Service.start = bstack1l111l1ll_opy_
      Service.stop = bstack11l1l11l1_opy_
      webdriver.Remote.get = bstack1l1lll1ll1_opy_
      WebDriver.close = bstack1l11lll11l_opy_
      WebDriver.quit = bstack1l1lll11l1_opy_
      webdriver.Remote.__init__ = bstack1lll11l1l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1lllll11ll_opy_:
        webdriver.Remote.__init__ = bstack1llllll1ll_opy_
    WebDriver.execute = bstack1llll11ll_opy_
    bstack1llllll1l1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1lllll11ll_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack111ll1ll_opy_
  except Exception as e:
    pass
  bstack1l11ll11l_opy_()
  if not bstack1llllll1l1_opy_:
    bstack1l111l1111_opy_(bstack1l1l1l1_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ౭"), bstack11ll11llll_opy_)
  if bstack1ll1ll1l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1l1l11111l_opy_ = bstack11l1llll11_opy_
    except Exception as e:
      logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
  if bstack1l1llll1l_opy_():
    bstack1l1l1lllll_opy_(CONFIG, logger)
  if (bstack1l1l1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౮") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1lllll1l1_opy_() == bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ౯"):
          bstack1l111lll11_opy_(bstack1l11l11ll1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1l1lll1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l111ll11l_opy_
      except Exception as e:
        logger.warn(bstack1lll11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l111111_opy_
      except Exception as e:
        logger.debug(bstack11l1ll1111_opy_ + str(e))
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1lll11l11_opy_)
    Output.start_test = bstack1l111l11l1_opy_
    Output.end_test = bstack111l1111_opy_
    TestStatus.__init__ = bstack1l11ll11l1_opy_
    QueueItem.__init__ = bstack1ll1l1l11_opy_
    pabot._create_items = bstack1ll1ll111_opy_
    try:
      from pabot import __version__ as bstack1l1111l1l_opy_
      if version.parse(bstack1l1111l1l_opy_) >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭౰")):
        pabot._run = bstack1l1l11l1ll_opy_
      elif version.parse(bstack1l1111l1l_opy_) >= version.parse(bstack1l1l1l1_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧ౱")):
        pabot._run = bstack11l1l1ll11_opy_
      else:
        pabot._run = bstack11ll11l11l_opy_
    except Exception as e:
      pabot._run = bstack11ll11l11l_opy_
    pabot._create_command_for_execution = bstack1lll111l1l_opy_
    pabot._report_results = bstack1lll1l11l1_opy_
  if bstack1l1l1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ౲") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1ll11ll1ll_opy_)
    Runner.run_hook = bstack1lll11ll1l_opy_
    Step.run = bstack111lll1l1_opy_
  if bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ౳") in str(framework_name).lower():
    if not bstack1lllll11ll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l1l1l1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11llllll_opy_
      Config.getoption = bstack1llllll111_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll11lll1l_opy_
    except Exception as e:
      pass
def bstack1l11lll1_opy_():
  global CONFIG
  if bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ౴") in CONFIG and int(CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ౵")]) > 1:
    logger.warn(bstack1llll1111_opy_)
def bstack1llll1l111_opy_(arg, bstack1llll1lll_opy_, bstack1ll1lll1l1_opy_=None):
  global CONFIG
  global bstack1l1llll1ll_opy_
  global bstack1l1ll11ll_opy_
  global bstack1lllll11ll_opy_
  global bstack1l1l1111l_opy_
  bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ౶")
  if bstack1llll1lll_opy_ and isinstance(bstack1llll1lll_opy_, str):
    bstack1llll1lll_opy_ = eval(bstack1llll1lll_opy_)
  CONFIG = bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭౷")]
  bstack1l1llll1ll_opy_ = bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ౸")]
  bstack1l1ll11ll_opy_ = bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ౹")]
  bstack1lllll11ll_opy_ = bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ౺")]
  bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ౻"), bstack1lllll11ll_opy_)
  os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭౼")] = bstack11111l1l1_opy_
  os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ౽")] = json.dumps(CONFIG)
  os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭౾")] = bstack1l1llll1ll_opy_
  os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ౿")] = str(bstack1l1ll11ll_opy_)
  os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧಀ")] = str(True)
  if bstack1ll1l111l1_opy_(arg, [bstack1l1l1l1_opy_ (u"ࠩ࠰ࡲࠬಁ"), bstack1l1l1l1_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಂ")]) != -1:
    os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬಃ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l11llll11_opy_)
    return
  bstack1llll1lll1_opy_()
  global bstack1l1ll11lll_opy_
  global bstack11l1l1l11_opy_
  global bstack1l1l1ll1_opy_
  global bstack1ll11111l_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1llll1l1ll_opy_
  global bstack11l11l11l_opy_
  arg.append(bstack1l1l1l1_opy_ (u"ࠧ࠳ࡗࠣ಄"))
  arg.append(bstack1l1l1l1_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤಅ"))
  arg.append(bstack1l1l1l1_opy_ (u"ࠢ࠮࡙ࠥಆ"))
  arg.append(bstack1l1l1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢಇ"))
  global bstack1ll11l11ll_opy_
  global bstack1ll1lll11_opy_
  global bstack11111ll11_opy_
  global bstack1l1l1llll1_opy_
  global bstack1ll11lll11_opy_
  global bstack11ll11ll_opy_
  global bstack1ll1lll11l_opy_
  global bstack11l1l1ll_opy_
  global bstack1l111llll_opy_
  global bstack11111111l_opy_
  global bstack1lll111l1_opy_
  global bstack1l1lllll11_opy_
  global bstack1l1lll1l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll11l11ll_opy_ = webdriver.Remote.__init__
    bstack1ll1lll11_opy_ = WebDriver.quit
    bstack11l1l1ll_opy_ = WebDriver.close
    bstack1l111llll_opy_ = WebDriver.get
    bstack11111ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll11l1l_opy_(CONFIG) and bstack1ll1l11ll_opy_():
    if bstack1l11l1lll_opy_() < version.parse(bstack11l11ll1l_opy_):
      logger.error(bstack1ll11ll11l_opy_.format(bstack1l11l1lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11111111l_opy_ = RemoteConnection._1l1l11111l_opy_
      except Exception as e:
        logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lll111l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1lllll11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1lll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪಈ"))
  bstack1l1l1ll1_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧಉ"), {}).get(bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಊ"))
  bstack11l11l11l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1lll11l1l1_opy_():
      bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.CONNECT, bstack1ll1lll1_opy_())
    platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಋ"), bstack1l1l1l1_opy_ (u"࠭࠰ࠨಌ")))
  else:
    bstack1lll1lll1l_opy_(bstack1lll1ll1l1_opy_)
  os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ಍")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಎ")]
  os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬಏ")] = CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಐ")]
  os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ಑")] = bstack1lllll11ll_opy_.__str__()
  from _pytest.config import main as bstack1ll111llll_opy_
  bstack1l1l11l1_opy_ = []
  try:
    bstack1111l1l11_opy_ = bstack1ll111llll_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1ll1111l_opy_()
    if bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩಒ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l11l1_opy_.append(bstack1l11l1l1l1_opy_)
    try:
      bstack1l1ll1ll1l_opy_ = (bstack1l1l11l1_opy_, int(bstack1111l1l11_opy_))
      bstack1ll1lll1l1_opy_.append(bstack1l1ll1ll1l_opy_)
    except:
      bstack1ll1lll1l1_opy_.append((bstack1l1l11l1_opy_, bstack1111l1l11_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l1l11l1_opy_.append({bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಓ"): bstack1l1l1l1_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩಔ") + os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨಕ")), bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨಖ"): traceback.format_exc(), bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩಗ"): int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫಘ")))})
    bstack1ll1lll1l1_opy_.append((bstack1l1l11l1_opy_, 1))
def bstack11l1111l1_opy_(arg):
  global bstack111l111l1_opy_
  bstack1lll1lll1l_opy_(bstack1l1ll111l_opy_)
  os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಙ")] = str(bstack1l1ll11ll_opy_)
  from behave.__main__ import main as bstack11l11l1l_opy_
  status_code = bstack11l11l1l_opy_(arg)
  if status_code != 0:
    bstack111l111l1_opy_ = status_code
def bstack1lll111l11_opy_():
  logger.info(bstack1l11ll11ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬಚ"), help=bstack1l1l1l1_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨಛ"))
  parser.add_argument(bstack1l1l1l1_opy_ (u"ࠨ࠯ࡸࠫಜ"), bstack1l1l1l1_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ಝ"), help=bstack1l1l1l1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩಞ"))
  parser.add_argument(bstack1l1l1l1_opy_ (u"ࠫ࠲ࡱࠧಟ"), bstack1l1l1l1_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫಠ"), help=bstack1l1l1l1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧಡ"))
  parser.add_argument(bstack1l1l1l1_opy_ (u"ࠧ࠮ࡨࠪಢ"), bstack1l1l1l1_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಣ"), help=bstack1l1l1l1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨತ"))
  bstack1l1ll1ll_opy_ = parser.parse_args()
  try:
    bstack1ll1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧಥ")
    if bstack1l1ll1ll_opy_.framework and bstack1l1ll1ll_opy_.framework not in (bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫದ"), bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ಧ")):
      bstack1ll1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬನ")
    bstack1ll1ll1l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll1l1ll1_opy_)
    bstack11llll1111_opy_ = open(bstack1ll1ll1l11_opy_, bstack1l1l1l1_opy_ (u"ࠧࡳࠩ಩"))
    bstack11llll111l_opy_ = bstack11llll1111_opy_.read()
    bstack11llll1111_opy_.close()
    if bstack1l1ll1ll_opy_.username:
      bstack11llll111l_opy_ = bstack11llll111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨಪ"), bstack1l1ll1ll_opy_.username)
    if bstack1l1ll1ll_opy_.key:
      bstack11llll111l_opy_ = bstack11llll111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫಫ"), bstack1l1ll1ll_opy_.key)
    if bstack1l1ll1ll_opy_.framework:
      bstack11llll111l_opy_ = bstack11llll111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫಬ"), bstack1l1ll1ll_opy_.framework)
    file_name = bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧಭ")
    file_path = os.path.abspath(file_name)
    bstack1l1ll111l1_opy_ = open(file_path, bstack1l1l1l1_opy_ (u"ࠬࡽࠧಮ"))
    bstack1l1ll111l1_opy_.write(bstack11llll111l_opy_)
    bstack1l1ll111l1_opy_.close()
    logger.info(bstack1l1111l11_opy_)
    try:
      os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಯ")] = bstack1l1ll1ll_opy_.framework if bstack1l1ll1ll_opy_.framework != None else bstack1l1l1l1_opy_ (u"ࠢࠣರ")
      config = yaml.safe_load(bstack11llll111l_opy_)
      config[bstack1l1l1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨಱ")] = bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨಲ")
      bstack1l1lll1lll_opy_(bstack1l1lllll1_opy_, config)
    except Exception as e:
      logger.debug(bstack11ll1l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11lll1l11l_opy_.format(str(e)))
def bstack1l1lll1lll_opy_(bstack1l1ll11111_opy_, config, bstack1ll111ll1l_opy_={}):
  global bstack1lllll11ll_opy_
  global bstack1llll11l1_opy_
  global bstack1l1l1111l_opy_
  if not config:
    return
  bstack1lllllllll_opy_ = bstack1111l11l_opy_ if not bstack1lllll11ll_opy_ else (
    bstack11l1l1111_opy_ if bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶࠧಳ") in config else (
        bstack1ll1l1l1l_opy_ if config.get(bstack1l1l1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ಴")) else bstack1l1l1l11l1_opy_
    )
)
  bstack111llllll_opy_ = False
  bstack1l1l11lll1_opy_ = False
  if bstack1lllll11ll_opy_ is True:
      if bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱࠩವ") in config:
          bstack111llllll_opy_ = True
      else:
          bstack1l1l11lll1_opy_ = True
  bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack1ll1l111_opy_(config, bstack1llll11l1_opy_)
  bstack1l1l1l1lll_opy_ = bstack11lll1lll1_opy_()
  data = {
    bstack1l1l1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಶ"): config[bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩಷ")],
    bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಸ"): config[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಹ")],
    bstack1l1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ಺"): bstack1l1ll11111_opy_,
    bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ಻"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ಼ࠧ"), bstack1llll11l1_opy_),
    bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨಽ"): bstack111l111l_opy_,
    bstack1l1l1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩಾ"): bstack1111ll111_opy_(),
    bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫಿ"): {
      bstack1l1l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧೀ"): str(config[bstack1l1l1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪು")]) if bstack1l1l1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫೂ") in config else bstack1l1l1l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨೃ"),
      bstack1l1l1l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡗࡧࡵࡷ࡮ࡵ࡮ࠨೄ"): sys.version,
      bstack1l1l1l1_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩ೅"): bstack111lll11l_opy_(os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪೆ"), bstack1llll11l1_opy_)),
      bstack1l1l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫೇ"): bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪೈ"),
      bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ೉"): bstack1lllllllll_opy_,
      bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪೊ"): bstack11ll11l1l1_opy_,
      bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠬೋ"): os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬೌ")],
      bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮್ࠫ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ೎"), bstack1llll11l1_opy_),
      bstack1l1l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೏"): bstack1ll11ll1_opy_(os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭೐"), bstack1llll11l1_opy_)),
      bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ೑"): bstack1l1l1l1lll_opy_.get(bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೒")),
      bstack1l1l1l1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೓"): bstack1l1l1l1lll_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ೔")),
      bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬೕ"): config[bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೖ")] if config[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೗")] else bstack1l1l1l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ೘"),
      bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೙"): str(config[bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೚")]) if bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೛") in config else bstack1l1l1l1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ೜"),
      bstack1l1l1l1_opy_ (u"ࠪࡳࡸ࠭ೝ"): sys.platform,
      bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ೞ"): socket.gethostname(),
      bstack1l1l1l1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧ೟"): bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨೠ"))
    }
  }
  if not bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧೡ")) is None:
    data[bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫೢ")][bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡑࡪࡺࡡࡥࡣࡷࡥࠬೣ")] = {
      bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ೤"): bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ೥"),
      bstack1l1l1l1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ೦"): bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭೧")),
      bstack1l1l1l1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࡎࡶ࡯ࡥࡩࡷ࠭೨"): bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡐࡲࠫ೩"))
    }
  if bstack1l1ll11111_opy_ == bstack1l1l111111_opy_:
    data[bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೪")][bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࠨ೫")] = bstack11ll11l1ll_opy_(config)
    data[bstack1l1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧ೬")][bstack1l1l1l1_opy_ (u"ࠬ࡯ࡳࡑࡧࡵࡧࡾࡇࡵࡵࡱࡈࡲࡦࡨ࡬ࡦࡦࠪ೭")] = percy.bstack11ll111111_opy_
    data[bstack1l1l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ೮")][bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡈࡵࡪ࡮ࡧࡍࡩ࠭೯")] = percy.percy_build_id
  update(data[bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ೰")], bstack1ll111ll1l_opy_)
  try:
    response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧೱ"), bstack11ll1llll_opy_(bstack1lll11l1ll_opy_), data, {
      bstack1l1l1l1_opy_ (u"ࠪࡥࡺࡺࡨࠨೲ"): (config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ೳ")], config[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೴")])
    })
    if response:
      logger.debug(bstack1l1lll11l_opy_.format(bstack1l1ll11111_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11111llll_opy_.format(str(e)))
def bstack111lll11l_opy_(framework):
  return bstack1l1l1l1_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ೵").format(str(framework), __version__) if framework else bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣ೶").format(
    __version__)
def bstack1llll1lll1_opy_():
  global CONFIG
  global bstack11ll11111l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1ll1llll_opy_()
    logger.debug(bstack1lll11l1_opy_.format(str(CONFIG)))
    bstack11ll11111l_opy_ = bstack1l1llllll_opy_.bstack1l1ll1l1l_opy_(CONFIG, bstack11ll11111l_opy_)
    bstack1l11l1111_opy_()
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧ೷") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11ll1l11ll_opy_
  atexit.register(bstack1ll1l1l1_opy_)
  signal.signal(signal.SIGINT, bstack11ll111l1_opy_)
  signal.signal(signal.SIGTERM, bstack11ll111l1_opy_)
def bstack11ll1l11ll_opy_(exctype, value, traceback):
  global bstack1ll11ll11_opy_
  try:
    for driver in bstack1ll11ll11_opy_:
      bstack1ll1lllll1_opy_(driver, bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ೸"), bstack1l1l1l1_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ೹") + str(value))
  except Exception:
    pass
  logger.info(bstack11ll1l11l_opy_)
  bstack1l11lllll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11lllll_opy_(message=bstack1l1l1l1_opy_ (u"ࠫࠬ೺"), bstack111l11l11_opy_ = False):
  global CONFIG
  bstack1l11lll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠧ೻") if bstack111l11l11_opy_ else bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ೼")
  try:
    if message:
      bstack1ll111ll1l_opy_ = {
        bstack1l11lll1l1_opy_ : str(message)
      }
      bstack1l1lll1lll_opy_(bstack1l1l111111_opy_, CONFIG, bstack1ll111ll1l_opy_)
    else:
      bstack1l1lll1lll_opy_(bstack1l1l111111_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1111ll_opy_.format(str(e)))
def bstack11llll11_opy_(bstack1ll1lll1ll_opy_, size):
  bstack1l1ll11ll1_opy_ = []
  while len(bstack1ll1lll1ll_opy_) > size:
    bstack1lll11ll_opy_ = bstack1ll1lll1ll_opy_[:size]
    bstack1l1ll11ll1_opy_.append(bstack1lll11ll_opy_)
    bstack1ll1lll1ll_opy_ = bstack1ll1lll1ll_opy_[size:]
  bstack1l1ll11ll1_opy_.append(bstack1ll1lll1ll_opy_)
  return bstack1l1ll11ll1_opy_
def bstack11llll1l1_opy_(args):
  if bstack1l1l1l1_opy_ (u"ࠧ࠮࡯ࠪ೽") in args and bstack1l1l1l1_opy_ (u"ࠨࡲࡧࡦࠬ೾") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack11l1ll111_opy_, stage=STAGE.bstack1l11111lll_opy_)
def run_on_browserstack(bstack111llll1l_opy_=None, bstack1ll1lll1l1_opy_=None, bstack1lll11lll1_opy_=False):
  global CONFIG
  global bstack1l1llll1ll_opy_
  global bstack1l1ll11ll_opy_
  global bstack1llll11l1_opy_
  global bstack1l1l1111l_opy_
  bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠩࠪ೿")
  bstack1ll1111ll1_opy_(bstack1l1lll11ll_opy_, logger)
  if bstack111llll1l_opy_ and isinstance(bstack111llll1l_opy_, str):
    bstack111llll1l_opy_ = eval(bstack111llll1l_opy_)
  if bstack111llll1l_opy_:
    CONFIG = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪഀ")]
    bstack1l1llll1ll_opy_ = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬഁ")]
    bstack1l1ll11ll_opy_ = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧം")]
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨഃ"), bstack1l1ll11ll_opy_)
    bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഄ")
  bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪഅ"), uuid4().__str__())
  logger.info(bstack1l1l1l1_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧആ") + bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬഇ")));
  logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧഈ") + bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧഉ")))
  if not bstack1lll11lll1_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l11llll11_opy_)
      return
    if sys.argv[1] == bstack1l1l1l1_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩഊ") or sys.argv[1] == bstack1l1l1l1_opy_ (u"ࠧ࠮ࡸࠪഋ"):
      logger.info(bstack1l1l1l1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨഌ").format(__version__))
      return
    if sys.argv[1] == bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ഍"):
      bstack1lll111l11_opy_()
      return
  args = sys.argv
  bstack1llll1lll1_opy_()
  global bstack1l1ll11lll_opy_
  global bstack1ll11l1ll_opy_
  global bstack11l11l11l_opy_
  global bstack1l11llll1_opy_
  global bstack11l1l1l11_opy_
  global bstack1l1l1ll1_opy_
  global bstack1ll11111l_opy_
  global bstack1l111l1l11_opy_
  global bstack1ll1ll11ll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll11l111_opy_
  bstack1ll11l1ll_opy_ = len(CONFIG.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭എ"), []))
  if not bstack11111l1l1_opy_:
    if args[1] == bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫഏ") or args[1] == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ഐ"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭഑")
      args = args[2:]
    elif args[1] == bstack1l1l1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ഒ"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഓ")
      args = args[2:]
    elif args[1] == bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨഔ"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩക")
      args = args[2:]
    elif args[1] == bstack1l1l1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬഖ"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഗ")
      args = args[2:]
    elif args[1] == bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ഘ"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧങ")
      args = args[2:]
    elif args[1] == bstack1l1l1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨച"):
      bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഛ")
      args = args[2:]
    else:
      if not bstack1l1l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ജ") in CONFIG or str(CONFIG[bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഝ")]).lower() in [bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഞ"), bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧട")]:
        bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫഡ")]).lower() == bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഢ"):
        bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩണ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧത")]).lower() == bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫഥ"):
        bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬദ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪധ")]).lower() == bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨന"):
        bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഩ")
        args = args[1:]
      elif str(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭പ")]).lower() == bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഫ"):
        bstack11111l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬബ")
        args = args[1:]
      else:
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨഭ")] = bstack11111l1l1_opy_
        bstack1ll11l1ll1_opy_(bstack1ll11lll1_opy_)
  os.environ[bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨമ")] = bstack11111l1l1_opy_
  bstack1llll11l1_opy_ = bstack11111l1l1_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack111llll1_opy_ = bstack1111111l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔ࠮ࡄࡇࡈࠬയ")] if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩര") and bstack1l111l11l_opy_() else bstack11111l1l1_opy_
      bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.bstack1l11l1l1l_opy_, bstack1ll111lll1_opy_(
        sdk_version=__version__,
        path_config=bstack111l1lll1_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack111llll1_opy_,
        frameworks=[bstack111llll1_opy_],
        framework_versions={
          bstack111llll1_opy_: bstack1ll11ll1_opy_(bstack1l1l1l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩറ") if bstack11111l1l1_opy_ in [bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪല"), bstack1l1l1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫള"), bstack1l1l1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧഴ")] else bstack11111l1l1_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤവ"), None):
        CONFIG[bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥശ")] = cli.config.get(bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦഷ"), None)
    except Exception as e:
      bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.bstack1l11l11lll_opy_, e.__traceback__, 1)
    if bstack1l1ll11ll_opy_:
      CONFIG[bstack1l1l1l1_opy_ (u"ࠥࡥࡵࡶࠢസ")] = cli.config[bstack1l1l1l1_opy_ (u"ࠦࡦࡶࡰࠣഹ")]
      logger.info(bstack1l1llll111_opy_.format(CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱࠩഺ")]))
  else:
    bstack1l11111l1_opy_.clear()
  global bstack1l1111lll1_opy_
  global bstack111l11l1_opy_
  if bstack111llll1l_opy_:
    try:
      bstack11ll11ll11_opy_ = datetime.datetime.now()
      os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ഻")] = bstack11111l1l1_opy_
      bstack1l1lll1lll_opy_(bstack1l1l1ll11_opy_, CONFIG)
      cli.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡹࡤ࡬ࡡࡷࡩࡸࡺ࡟ࡢࡶࡷࡩࡲࡶࡴࡦࡦ഼ࠥ"), datetime.datetime.now() - bstack11ll11ll11_opy_)
    except Exception as e:
      logger.debug(bstack1lllll1l11_opy_.format(str(e)))
  global bstack1ll11l11ll_opy_
  global bstack1ll1lll11_opy_
  global bstack11lll11ll1_opy_
  global bstack1llll111l1_opy_
  global bstack1ll1llll1_opy_
  global bstack11ll1ll1l_opy_
  global bstack1l1l1llll1_opy_
  global bstack1ll11lll11_opy_
  global bstack1l1ll11l1_opy_
  global bstack11ll11ll_opy_
  global bstack1ll1lll11l_opy_
  global bstack11l1l1ll_opy_
  global bstack11lllll1l1_opy_
  global bstack1l1ll11l1l_opy_
  global bstack1l111llll_opy_
  global bstack11111111l_opy_
  global bstack1lll111l1_opy_
  global bstack1l1lllll11_opy_
  global bstack1ll11l11l1_opy_
  global bstack1l1lll1l1l_opy_
  global bstack11111ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll11l11ll_opy_ = webdriver.Remote.__init__
    bstack1ll1lll11_opy_ = WebDriver.quit
    bstack11l1l1ll_opy_ = WebDriver.close
    bstack1l111llll_opy_ = WebDriver.get
    bstack11111ll11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1111lll1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack111lllll1_opy_
    bstack111l11l1_opy_ = bstack111lllll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack11lll1l111_opy_
    from QWeb.keywords import browser
    bstack11lll1l111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11l1l_opy_(CONFIG) and bstack1ll1l11ll_opy_():
    if bstack1l11l1lll_opy_() < version.parse(bstack11l11ll1l_opy_):
      logger.error(bstack1ll11ll11l_opy_.format(bstack1l11l1lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11111111l_opy_ = RemoteConnection._1l1l11111l_opy_
      except Exception as e:
        logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
  if not CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪഽ"), False) and not bstack111llll1l_opy_:
    logger.info(bstack11l1lll1ll_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ാ") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧി")]).lower() != bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪീ"):
      bstack1lll1llll1_opy_()
    elif bstack11111l1l1_opy_ != bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬു") or (bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ൂ") and not bstack111llll1l_opy_):
      bstack1111l1lll_opy_()
  if (bstack11111l1l1_opy_ in [bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ൃ"), bstack1l1l1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧൄ"), bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൅")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1l1lll1l_opy_
        bstack11ll1ll1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lll11l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1ll1llll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1ll1111_opy_ + str(e))
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1lll11l11_opy_)
    if bstack11111l1l1_opy_ != bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫെ"):
      bstack1llll11l1l_opy_()
    bstack11lll11ll1_opy_ = Output.start_test
    bstack1llll111l1_opy_ = Output.end_test
    bstack1l1l1llll1_opy_ = TestStatus.__init__
    bstack1l1ll11l1_opy_ = pabot._run
    bstack11ll11ll_opy_ = QueueItem.__init__
    bstack1ll1lll11l_opy_ = pabot._create_command_for_execution
    bstack1ll11l11l1_opy_ = pabot._report_results
  if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫേ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1ll11ll1ll_opy_)
    bstack11lllll1l1_opy_ = Runner.run_hook
    bstack1l1ll11l1l_opy_ = Step.run
  if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬൈ"):
    try:
      from _pytest.config import Config
      bstack1lll111l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1lllll11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1lll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧ൉"))
  try:
    framework_name = bstack1l1l1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൊ") if bstack11111l1l1_opy_ in [bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧോ"), bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨൌ"), bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯്ࠫ")] else bstack1l11l111l1_opy_(bstack11111l1l1_opy_)
    bstack1l11ll1ll_opy_ = {
      bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬൎ"): bstack1l1l1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧ൏") if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൐") and bstack1l111l11l_opy_() else framework_name,
      bstack1l1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ൑"): bstack1ll11ll1_opy_(framework_name),
      bstack1l1l1l1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭൒"): __version__,
      bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ൓"): bstack11111l1l1_opy_
    }
    if bstack11111l1l1_opy_ in bstack1l111lll_opy_:
      if bstack1lllll11ll_opy_ and bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪൔ") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫൕ")] == True:
        if bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬൖ") in CONFIG:
          os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧൗ")] = os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ൘"), json.dumps(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൙")]))
          CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൚")].pop(bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ൛"), None)
          CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ൜")].pop(bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ൝"), None)
        bstack1l11ll1ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൞")] = {
          bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬൟ"): bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪൠ"),
          bstack1l1l1l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪൡ"): str(bstack1l11l1lll_opy_())
        }
    if bstack11111l1l1_opy_ not in [bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ")] and not cli.is_running():
      bstack11ll1llll1_opy_ = bstack111111ll1_opy_.launch(CONFIG, bstack1l11ll1ll_opy_)
  except Exception as e:
    logger.debug(bstack11lll11l_opy_.format(bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡊࡸࡦࠬൣ"), str(e)))
  if bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൤"):
    bstack11l11l11l_opy_ = True
    if bstack111llll1l_opy_ and bstack1lll11lll1_opy_:
      bstack1l1l1ll1_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ൥"), {}).get(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ൦"))
      bstack1lll1lll1l_opy_(bstack1l11ll1l11_opy_)
    elif bstack111llll1l_opy_:
      bstack1l1l1ll1_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ൧"), {}).get(bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൨"))
      global bstack1ll11ll11_opy_
      try:
        if bstack11llll1l1_opy_(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൩")]) and multiprocessing.current_process().name == bstack1l1l1l1_opy_ (u"ࠫ࠵࠭൪"):
          bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൫")].remove(bstack1l1l1l1_opy_ (u"࠭࠭࡮ࠩ൬"))
          bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൭")].remove(bstack1l1l1l1_opy_ (u"ࠨࡲࡧࡦࠬ൮"))
          bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ൯")] = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭൰")][0]
          with open(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ൱")], bstack1l1l1l1_opy_ (u"ࠬࡸࠧ൲")) as f:
            bstack1lllll11l1_opy_ = f.read()
          bstack1lllll111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡡࡳࡩࠣࡁࠥࡹࡴࡳࠪ࡬ࡲࡹ࠮ࡡࡳࡩࠬ࠯࠶࠶ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤ൳").format(str(bstack111llll1l_opy_))
          bstack1l1llll11l_opy_ = bstack1lllll111_opy_ + bstack1lllll11l1_opy_
          bstack1l111ll1l1_opy_ = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ൴")] + bstack1l1l1l1_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪ൵")
          with open(bstack1l111ll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠩࡺࠫ൶")):
            pass
          with open(bstack1l111ll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠥࡻ࠰ࠨ൷")) as f:
            f.write(bstack1l1llll11l_opy_)
          import subprocess
          bstack1lll11ll1_opy_ = subprocess.run([bstack1l1l1l1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦ൸"), bstack1l111ll1l1_opy_])
          if os.path.exists(bstack1l111ll1l1_opy_):
            os.unlink(bstack1l111ll1l1_opy_)
          os._exit(bstack1lll11ll1_opy_.returncode)
        else:
          if bstack11llll1l1_opy_(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ൹")]):
            bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩൺ")].remove(bstack1l1l1l1_opy_ (u"ࠧ࠮࡯ࠪൻ"))
            bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫർ")].remove(bstack1l1l1l1_opy_ (u"ࠩࡳࡨࡧ࠭ൽ"))
            bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ൾ")] = bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൿ")][0]
          bstack1lll1lll1l_opy_(bstack1l11ll1l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ඀")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1l1l1_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨඁ")] = bstack1l1l1l1_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩං")
          mod_globals[bstack1l1l1l1_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪඃ")] = os.path.abspath(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඄")])
          exec(open(bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭අ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1l1l1_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫආ").format(str(e)))
          for driver in bstack1ll11ll11_opy_:
            bstack1ll1lll1l1_opy_.append({
              bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪඇ"): bstack111llll1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඈ")],
              bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ඉ"): str(e),
              bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧඊ"): multiprocessing.current_process().name
            })
            bstack1ll1lllll1_opy_(driver, bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩඋ"), bstack1l1l1l1_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨඌ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll11ll11_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l1ll11ll_opy_, CONFIG, logger)
      bstack11l1ll1ll_opy_()
      bstack1l11lll1_opy_()
      bstack1llll1lll_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඍ"): args[0],
        bstack1l1l1l1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬඎ"): CONFIG,
        bstack1l1l1l1_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧඏ"): bstack1l1llll1ll_opy_,
        bstack1l1l1l1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩඐ"): bstack1l1ll11ll_opy_
      }
      percy.bstack1lll1l1ll_opy_()
      if bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫඑ") in CONFIG:
        bstack11l111l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1ll11l_opy_ = manager.list()
        if bstack11llll1l1_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬඒ")]):
            if index == 0:
              bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඓ")] = args
            bstack11l111l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1lll_opy_, bstack1l1ll11l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧඔ")]):
            bstack11l111l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1llll1lll_opy_, bstack1l1ll11l_opy_)))
        for t in bstack11l111l1_opy_:
          t.start()
        for t in bstack11l111l1_opy_:
          t.join()
        bstack1l111l1l11_opy_ = list(bstack1l1ll11l_opy_)
      else:
        if bstack11llll1l1_opy_(args):
          bstack1llll1lll_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඕ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1llll1lll_opy_,))
          test.start()
          test.join()
        else:
          bstack1lll1lll1l_opy_(bstack1l11ll1l11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1l1l1_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨඖ")] = bstack1l1l1l1_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩ඗")
          mod_globals[bstack1l1l1l1_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪ඘")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ඙") or bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩක"):
    percy.init(bstack1l1ll11ll_opy_, CONFIG, logger)
    percy.bstack1lll1l1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1lll11l11_opy_)
    bstack11l1ll1ll_opy_()
    bstack1lll1lll1l_opy_(bstack11111lll_opy_)
    if bstack1lllll11ll_opy_:
      bstack111llll11_opy_(bstack11111lll_opy_, args)
      if bstack1l1l1l1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩඛ") in args:
        i = args.index(bstack1l1l1l1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪග"))
        args.pop(i)
        args.pop(i)
      if bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩඝ") not in CONFIG:
        CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඞ")] = [{}]
        bstack1ll11l1ll_opy_ = 1
      if bstack1l1ll11lll_opy_ == 0:
        bstack1l1ll11lll_opy_ = 1
      args.insert(0, str(bstack1l1ll11lll_opy_))
      args.insert(0, str(bstack1l1l1l1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ඟ")))
    if bstack111111ll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l1l11llll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1l11ll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1l1l1l1_opy_ (u"ࠤࡕࡓࡇࡕࡔࡠࡑࡓࡘࡎࡕࡎࡔࠤච"),
        ).parse_args(bstack1l1l11llll_opy_)
        bstack111111ll_opy_ = args.index(bstack1l1l11llll_opy_[0]) if len(bstack1l1l11llll_opy_) > 0 else len(args)
        args.insert(bstack111111ll_opy_, str(bstack1l1l1l1_opy_ (u"ࠪ࠱࠲ࡲࡩࡴࡶࡨࡲࡪࡸࠧඡ")))
        args.insert(bstack111111ll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶ࠳ࡶࡹࠨජ"))))
        if bstack11ll11l1l_opy_(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪඣ"))) and str(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪඤ"), bstack1l1l1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬඥ"))) != bstack1l1l1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ඦ"):
          for bstack1l1l1l1ll1_opy_ in bstack1ll1l11ll1_opy_:
            args.remove(bstack1l1l1l1ll1_opy_)
          bstack1l11ll11_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭ට")).split(bstack1l1l1l1_opy_ (u"ࠪ࠰ࠬඨ"))
          for bstack1111111ll_opy_ in bstack1l11ll11_opy_:
            args.append(bstack1111111ll_opy_)
      except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡸࡹࡧࡣࡩ࡫ࡱ࡫ࠥࡲࡩࡴࡶࡨࡲࡪࡸࠠࡧࡱࡵࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࠢඩ").format(e))
    pabot.main(args)
  elif bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ඪ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1lll11l11_opy_)
    for a in args:
      if bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬණ") in a:
        bstack11l1l1l11_opy_ = int(a.split(bstack1l1l1l1_opy_ (u"ࠧ࠻ࠩඬ"))[1])
      if bstack1l1l1l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬත") in a:
        bstack1l1l1ll1_opy_ = str(a.split(bstack1l1l1l1_opy_ (u"ࠩ࠽ࠫථ"))[1])
      if bstack1l1l1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪද") in a:
        bstack1ll11111l_opy_ = str(a.split(bstack1l1l1l1_opy_ (u"ࠫ࠿࠭ධ"))[1])
    bstack11l1l1llll_opy_ = None
    if bstack1l1l1l1_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫන") in args:
      i = args.index(bstack1l1l1l1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ඲"))
      args.pop(i)
      bstack11l1l1llll_opy_ = args.pop(i)
    if bstack11l1l1llll_opy_ is not None:
      global bstack1llll1ll1_opy_
      bstack1llll1ll1_opy_ = bstack11l1l1llll_opy_
    bstack1lll1lll1l_opy_(bstack11111lll_opy_)
    run_cli(args)
    if bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫඳ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l11l1l1l1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll1lll1l1_opy_.append(bstack1l11l1l1l1_opy_)
  elif bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨප"):
    bstack1ll1llllll_opy_ = bstack1l111l1lll_opy_(args, logger, CONFIG, bstack1lllll11ll_opy_)
    bstack1ll1llllll_opy_.bstack1l11l11l_opy_()
    bstack11l1ll1ll_opy_()
    bstack1l11llll1_opy_ = True
    bstack1llll1l1ll_opy_ = bstack1ll1llllll_opy_.bstack1111l11ll_opy_()
    bstack1ll1llllll_opy_.bstack1llll1lll_opy_(bstack1ll11l1lll_opy_)
    bstack11111l1l_opy_ = bstack1ll1llllll_opy_.bstack1llll1l11_opy_(bstack1llll1l111_opy_, {
      bstack1l1l1l1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪඵ"): bstack1l1llll1ll_opy_,
      bstack1l1l1l1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬබ"): bstack1l1ll11ll_opy_,
      bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧභ"): bstack1lllll11ll_opy_
    })
    try:
      bstack1l1l11l1_opy_, bstack11ll11111_opy_ = map(list, zip(*bstack11111l1l_opy_))
      bstack1ll1ll11ll_opy_ = bstack1l1l11l1_opy_[0]
      for status_code in bstack11ll11111_opy_:
        if status_code != 0:
          bstack1ll11l111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡤࡺࡪࠦࡥࡳࡴࡲࡶࡸࠦࡡ࡯ࡦࠣࡷࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠯ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡀࠠࡼࡿࠥම").format(str(e)))
  elif bstack11111l1l1_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ඹ"):
    try:
      from behave.__main__ import main as bstack11l11l1l_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l111l1111_opy_(e, bstack1ll11ll1ll_opy_)
    bstack11l1ll1ll_opy_()
    bstack1l11llll1_opy_ = True
    bstack1l111ll1_opy_ = 1
    if bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧය") in CONFIG:
      bstack1l111ll1_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨර")]
    if bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ඼") in CONFIG:
      bstack1ll11ll1l1_opy_ = int(bstack1l111ll1_opy_) * int(len(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ල")]))
    else:
      bstack1ll11ll1l1_opy_ = int(bstack1l111ll1_opy_)
    config = Configuration(args)
    bstack1ll1lll111_opy_ = config.paths
    if len(bstack1ll1lll111_opy_) == 0:
      import glob
      pattern = bstack1l1l1l1_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪ඾")
      bstack1ll111111l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll111111l_opy_)
      config = Configuration(args)
      bstack1ll1lll111_opy_ = config.paths
    bstack11ll1111l_opy_ = [os.path.normpath(item) for item in bstack1ll1lll111_opy_]
    bstack1llll1l1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1111llll_opy_ = [item for item in bstack1llll1l1l_opy_ if item not in bstack11ll1111l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1l1l1_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭඿"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1111l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l1l11l_opy_)))
                    for bstack1l1l1l11l_opy_ in bstack11ll1111l_opy_]
    bstack11llll1l11_opy_ = []
    for spec in bstack11ll1111l_opy_:
      bstack1l11lll111_opy_ = []
      bstack1l11lll111_opy_ += bstack1l1111llll_opy_
      bstack1l11lll111_opy_.append(spec)
      bstack11llll1l11_opy_.append(bstack1l11lll111_opy_)
    execution_items = []
    for bstack1l11lll111_opy_ in bstack11llll1l11_opy_:
      if bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩව") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪශ")]):
          item = {}
          item[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࠬෂ")] = bstack1l1l1l1_opy_ (u"ࠩࠣࠫස").join(bstack1l11lll111_opy_)
          item[bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩහ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࠨළ")] = bstack1l1l1l1_opy_ (u"ࠬࠦࠧෆ").join(bstack1l11lll111_opy_)
        item[bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ෇")] = 0
        execution_items.append(item)
    bstack1l11lll11_opy_ = bstack11llll11_opy_(execution_items, bstack1ll11ll1l1_opy_)
    for execution_item in bstack1l11lll11_opy_:
      bstack11l111l1_opy_ = []
      for item in execution_item:
        bstack11l111l1_opy_.append(bstack11ll11l11_opy_(name=str(item[bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭෈")]),
                                             target=bstack11l1111l1_opy_,
                                             args=(item[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࠬ෉")],)))
      for t in bstack11l111l1_opy_:
        t.start()
      for t in bstack11l111l1_opy_:
        t.join()
  else:
    bstack1ll11l1ll1_opy_(bstack1ll11lll1_opy_)
  if not bstack111llll1l_opy_:
    bstack1l1ll1ll11_opy_()
    if(bstack11111l1l1_opy_ in [bstack1l1l1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ්ࠩ"), bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ෋")]):
      bstack1l1l111l11_opy_()
  bstack1l1llllll_opy_.bstack1llll11l_opy_()
def browserstack_initialize(bstack11lll11111_opy_=None):
  logger.info(bstack1l1l1l1_opy_ (u"ࠫࡗࡻ࡮࡯࡫ࡱ࡫࡙ࠥࡄࡌࠢࡺ࡭ࡹ࡮ࠠࡢࡴࡪࡷ࠿ࠦࠧ෌") + str(bstack11lll11111_opy_))
  run_on_browserstack(bstack11lll11111_opy_, None, True)
@measure(event_name=EVENTS.bstack1l11l11l1l_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1ll1ll11_opy_():
  global CONFIG
  global bstack1llll11l1_opy_
  global bstack1ll11l111_opy_
  global bstack111l111l1_opy_
  global bstack1l1l1111l_opy_
  if cli.is_running():
    bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.bstack111ll11ll_opy_)
  if bstack1llll11l1_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෍"):
    if not cli.is_enabled(CONFIG):
      bstack111111ll1_opy_.stop()
  else:
    bstack111111ll1_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1l11l1lll1_opy_.bstack1lll11l111_opy_()
  if bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ෎") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫා")]).lower() != bstack1l1l1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧැ"):
    bstack11l111111_opy_, bstack11l1l1l1ll_opy_ = bstack1ll1l1111_opy_()
  else:
    bstack11l111111_opy_, bstack11l1l1l1ll_opy_ = get_build_link()
  bstack11l11l1ll_opy_(bstack11l111111_opy_)
  logger.info(bstack1l1l1l1_opy_ (u"ࠩࡖࡈࡐࠦࡲࡶࡰࠣࡩࡳࡪࡥࡥࠢࡩࡳࡷࠦࡩࡥ࠼ࠪෑ") + bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬි"), bstack1l1l1l1_opy_ (u"ࠫࠬී")) + bstack1l1l1l1_opy_ (u"ࠬ࠲ࠠࡵࡧࡶࡸ࡭ࡻࡢࠡ࡫ࡧ࠾ࠥ࠭ු") + os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ෕"), bstack1l1l1l1_opy_ (u"ࠧࠨූ")))
  if bstack11l111111_opy_ is not None and bstack1l1l11lll_opy_() != -1:
    sessions = bstack1l1l111l1l_opy_(bstack11l111111_opy_)
    bstack1111l111l_opy_(sessions, bstack11l1l1l1ll_opy_)
  if bstack1llll11l1_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෗") and bstack1ll11l111_opy_ != 0:
    sys.exit(bstack1ll11l111_opy_)
  if bstack1llll11l1_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ") and bstack111l111l1_opy_ != 0:
    sys.exit(bstack111l111l1_opy_)
def bstack11l11l1ll_opy_(new_id):
    global bstack111l111l_opy_
    bstack111l111l_opy_ = new_id
def bstack1l11l111l1_opy_(bstack1l11l11111_opy_):
  if bstack1l11l11111_opy_:
    return bstack1l11l11111_opy_.capitalize()
  else:
    return bstack1l1l1l1_opy_ (u"ࠪࠫෙ")
@measure(event_name=EVENTS.bstack11l1ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l11ll1111_opy_(bstack11llll11ll_opy_):
  if bstack1l1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩේ") in bstack11llll11ll_opy_ and bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪෛ")] != bstack1l1l1l1_opy_ (u"࠭ࠧො"):
    return bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬෝ")]
  else:
    bstack1lllll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠣࠤෞ")
    if bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩෟ") in bstack11llll11ll_opy_ and bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ෠")] != None:
      bstack1lllll1ll_opy_ += bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ෡")] + bstack1l1l1l1_opy_ (u"ࠧ࠲ࠠࠣ෢")
      if bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡴࠩ෣")] == bstack1l1l1l1_opy_ (u"ࠢࡪࡱࡶࠦ෤"):
        bstack1lllll1ll_opy_ += bstack1l1l1l1_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ෥")
      bstack1lllll1ll_opy_ += (bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭෦")] or bstack1l1l1l1_opy_ (u"ࠪࠫ෧"))
      return bstack1lllll1ll_opy_
    else:
      bstack1lllll1ll_opy_ += bstack1l11l111l1_opy_(bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ෨")]) + bstack1l1l1l1_opy_ (u"ࠧࠦࠢ෩") + (
              bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ෪")] or bstack1l1l1l1_opy_ (u"ࠧࠨ෫")) + bstack1l1l1l1_opy_ (u"ࠣ࠮ࠣࠦ෬")
      if bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡷࠬ෭")] == bstack1l1l1l1_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ෮"):
        bstack1lllll1ll_opy_ += bstack1l1l1l1_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ෯")
      bstack1lllll1ll_opy_ += bstack11llll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෰")] or bstack1l1l1l1_opy_ (u"࠭ࠧ෱")
      return bstack1lllll1ll_opy_
@measure(event_name=EVENTS.bstack1ll1111l11_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1lllll111l_opy_(bstack1l1l11l1l_opy_):
  if bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠢࡥࡱࡱࡩࠧෲ"):
    return bstack1l1l1l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫෳ")
  elif bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ෴"):
    return bstack1l1l1l1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭෵")
  elif bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ෶"):
    return bstack1l1l1l1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෷")
  elif bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ෸"):
    return bstack1l1l1l1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ෹")
  elif bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ෺"):
    return bstack1l1l1l1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ෻")
  elif bstack1l1l11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ෼"):
    return bstack1l1l1l1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෽")
  else:
    return bstack1l1l1l1_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ෾") + bstack1l11l111l1_opy_(
      bstack1l1l11l1l_opy_) + bstack1l1l1l1_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ෿")
def bstack1l11ll1l1l_opy_(session):
  return bstack1l1l1l1_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ฀").format(
    session[bstack1l1l1l1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬก")], bstack1l11ll1111_opy_(session), bstack1lllll111l_opy_(session[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨข")]),
    bstack1lllll111l_opy_(session[bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪฃ")]),
    bstack1l11l111l1_opy_(session[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬค")] or session[bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬฅ")] or bstack1l1l1l1_opy_ (u"࠭ࠧฆ")) + bstack1l1l1l1_opy_ (u"ࠢࠡࠤง") + (session[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪจ")] or bstack1l1l1l1_opy_ (u"ࠩࠪฉ")),
    session[bstack1l1l1l1_opy_ (u"ࠪࡳࡸ࠭ช")] + bstack1l1l1l1_opy_ (u"ࠦࠥࠨซ") + session[bstack1l1l1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩฌ")], session[bstack1l1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨญ")] or bstack1l1l1l1_opy_ (u"ࠧࠨฎ"),
    session[bstack1l1l1l1_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬฏ")] if session[bstack1l1l1l1_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ฐ")] else bstack1l1l1l1_opy_ (u"ࠪࠫฑ"))
@measure(event_name=EVENTS.bstack1l1111ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1111l111l_opy_(sessions, bstack11l1l1l1ll_opy_):
  try:
    bstack1llll1111l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࠧฒ")
    if not os.path.exists(bstack1l11111l1l_opy_):
      os.mkdir(bstack1l11111l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1l1l1_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪณ")), bstack1l1l1l1_opy_ (u"࠭ࡲࠨด")) as f:
      bstack1llll1111l_opy_ = f.read()
    bstack1llll1111l_opy_ = bstack1llll1111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫต"), str(len(sessions)))
    bstack1llll1111l_opy_ = bstack1llll1111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨถ"), bstack11l1l1l1ll_opy_)
    bstack1llll1111l_opy_ = bstack1llll1111l_opy_.replace(bstack1l1l1l1_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪท"),
                                              sessions[0].get(bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧธ")) if sessions[0] else bstack1l1l1l1_opy_ (u"ࠫࠬน"))
    with open(os.path.join(bstack1l11111l1l_opy_, bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩบ")), bstack1l1l1l1_opy_ (u"࠭ࡷࠨป")) as stream:
      stream.write(bstack1llll1111l_opy_.split(bstack1l1l1l1_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫผ"))[0])
      for session in sessions:
        stream.write(bstack1l11ll1l1l_opy_(session))
      stream.write(bstack1llll1111l_opy_.split(bstack1l1l1l1_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬฝ"))[1])
    logger.info(bstack1l1l1l1_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬพ").format(bstack1l11111l1l_opy_));
  except Exception as e:
    logger.debug(bstack1lll1l111_opy_.format(str(e)))
def bstack1l1l111l1l_opy_(bstack11l111111_opy_):
  global CONFIG
  try:
    bstack11ll11ll11_opy_ = datetime.datetime.now()
    host = bstack1l1l1l1_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ฟ") if bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰࠨภ") in CONFIG else bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡪࠩม")
    user = CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨย")]
    key = CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪร")]
    bstack11lll1llll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧฤ") if bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵ࠭ล") in CONFIG else (bstack1l1l1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧฦ") if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨว")) else bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧศ"))
    url = bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫษ").format(user, key, host, bstack11lll1llll_opy_,
                                                                                bstack11l111111_opy_)
    headers = {
      bstack1l1l1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ส"): bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫห"),
    }
    proxies = bstack1l1lll1111_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺ࡨࡧࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࡥ࡬ࡪࡵࡷࠦฬ"), datetime.datetime.now() - bstack11ll11ll11_opy_)
      return list(map(lambda session: session[bstack1l1l1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨอ")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1lll11_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack11lll11lll_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def get_build_link():
  global CONFIG
  global bstack111l111l_opy_
  try:
    if bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧฮ") in CONFIG:
      bstack11ll11ll11_opy_ = datetime.datetime.now()
      host = bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨฯ") if bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࠪะ") in CONFIG else bstack1l1l1l1_opy_ (u"ࠧࡢࡲ࡬ࠫั")
      user = CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪา")]
      key = CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬำ")]
      bstack11lll1llll_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩิ") if bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰࠨี") in CONFIG else bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧึ")
      url = bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ื").format(user, key, host, bstack11lll1llll_opy_)
      headers = {
        bstack1l1l1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪุ࠭"): bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱูࠫ"),
      }
      if bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵฺࠫ") in CONFIG:
        params = {bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ฻"): CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ฼")], bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฽"): CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ฾")]}
      else:
        params = {bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ฿"): CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫเ")]}
      proxies = bstack1l1lll1111_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l11lll1l_opy_ = response.json()[0][bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬแ")]
        if bstack1l11lll1l_opy_:
          bstack11l1l1l1ll_opy_ = bstack1l11lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧโ")].split(bstack1l1l1l1_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪใ"))[0] + bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭ไ") + bstack1l11lll1l_opy_[
            bstack1l1l1l1_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩๅ")]
          logger.info(bstack1ll1l11l1l_opy_.format(bstack11l1l1l1ll_opy_))
          bstack111l111l_opy_ = bstack1l11lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪๆ")]
          bstack1l11ll1l1_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ็")]
          if bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ่ࠫ") in CONFIG:
            bstack1l11ll1l1_opy_ += bstack1l1l1l1_opy_ (u"ࠪࠤ้ࠬ") + CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ๊࠭")]
          if bstack1l11ll1l1_opy_ != bstack1l11lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧ๋ࠪ")]:
            logger.debug(bstack1l1l1l1l1l_opy_.format(bstack1l11lll1l_opy_[bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ์")], bstack1l11ll1l1_opy_))
          cli.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࡭ࡥࡵࡡࡥࡹ࡮ࡲࡤࡠ࡮࡬ࡲࡰࠨํ"), datetime.datetime.now() - bstack11ll11ll11_opy_)
          return [bstack1l11lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๎")], bstack11l1l1l1ll_opy_]
    else:
      logger.warn(bstack1lll11l11l_opy_)
  except Exception as e:
    logger.debug(bstack11ll1l111l_opy_.format(str(e)))
  return [None, None]
def bstack1111l1l1l_opy_(url, bstack1ll11111_opy_=False):
  global CONFIG
  global bstack1l1llll1_opy_
  if not bstack1l1llll1_opy_:
    hostname = bstack1111lll1l_opy_(url)
    is_private = bstack1l1l111ll1_opy_(hostname)
    if (bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭๏") in CONFIG and not bstack11ll11l1l_opy_(CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๐")])) and (is_private or bstack1ll11111_opy_):
      bstack1l1llll1_opy_ = hostname
def bstack1111lll1l_opy_(url):
  return urlparse(url).hostname
def bstack1l1l111ll1_opy_(hostname):
  for bstack11l1lll1l_opy_ in bstack11l1lll11l_opy_:
    regex = re.compile(bstack11l1lll1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l11ll11_opy_(bstack1l111ll111_opy_):
  return True if bstack1l111ll111_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1l1ll1ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1l1l11_opy_
  bstack1lll1llll_opy_ = not (bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๑"), None) and bstack11ll111l_opy_(
          threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๒"), None))
  bstack11l111ll1_opy_ = getattr(driver, bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭๓"), None) != True
  if not bstack11111l11l_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l1l11_opy_) or (bstack11l111ll1_opy_ and bstack1lll1llll_opy_):
    logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴ࠰ࠥ๔"))
    return {}
  try:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ๕"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l111lll1l_opy_.bstack1l11l1llll_opy_)
    return results
  except Exception:
    logger.error(bstack1l1l1l1_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ๖"))
    return {}
@measure(event_name=EVENTS.bstack1llllllll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1l1l11_opy_
  bstack1lll1llll_opy_ = not (bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ๗"), None) and bstack11ll111l_opy_(
          threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๘"), None))
  bstack11l111ll1_opy_ = getattr(driver, bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ๙"), None) != True
  if not bstack11111l11l_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l1l11_opy_) or (bstack11l111ll1_opy_ and bstack1lll1llll_opy_):
    logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡵࡸࡱࡲࡧࡲࡺ࠰ࠥ๚"))
    return {}
  try:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽࠬ๛"))
    logger.debug(perform_scan(driver))
    bstack1111l1l1_opy_ = driver.execute_async_script(bstack1l111lll1l_opy_.bstack1l111l11ll_opy_)
    return bstack1111l1l1_opy_
  except Exception:
    logger.error(bstack1l1l1l1_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡻ࡭࡮ࡣࡵࡽࠥࡽࡡࡴࠢࡩࡳࡺࡴࡤ࠯ࠤ๜"))
    return {}
@measure(event_name=EVENTS.bstack1lll1l11ll_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l1l1l11_opy_
  bstack1lll1llll_opy_ = not (bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭๝"), None) and bstack11ll111l_opy_(
          threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๞"), None))
  bstack11l111ll1_opy_ = getattr(driver, bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ๟"), None) != True
  if not bstack11111l11l_opy_.bstack1111111l1_opy_(CONFIG, bstack11l1l1l11_opy_) or (bstack11l111ll1_opy_ and bstack1lll1llll_opy_):
    logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷࡻ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢ๠"))
    return {}
  try:
    bstack1lll1l111l_opy_ = driver.execute_async_script(bstack1l111lll1l_opy_.perform_scan, {bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭๡"): kwargs.get(bstack1l1l1l1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡱࡰࡱࡦࡴࡤࠨ๢"), None) or bstack1l1l1l1_opy_ (u"ࠨࠩ๣")})
    return bstack1lll1l111l_opy_
  except Exception:
    logger.error(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣ๤"))
    return {}