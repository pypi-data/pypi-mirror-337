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
import threading
import logging
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.helper import bstack11ll111l_opy_
logger = logging.getLogger(__name__)
def bstack11l11ll11_opy_(bstack1l111ll111_opy_):
  return True if bstack1l111ll111_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11l1l111_opy_(context, *args):
    tags = getattr(args[0], bstack1l1l1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᕐ"), [])
    bstack1l111ll1ll_opy_ = bstack11111l11l_opy_.bstack1l111l111l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l111ll1ll_opy_
    try:
      bstack1l1ll1l1l1_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11ll11_opy_(bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪᕑ")) else context.browser
      if bstack1l1ll1l1l1_opy_ and bstack1l1ll1l1l1_opy_.session_id and bstack1l111ll1ll_opy_ and bstack11ll111l_opy_(
              threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᕒ"), None):
          threading.current_thread().isA11yTest = bstack11111l11l_opy_.bstack1l111ll11_opy_(bstack1l1ll1l1l1_opy_, bstack1l111ll1ll_opy_)
    except Exception as e:
       logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭ᕓ").format(str(e)))
def bstack11111ll1l_opy_(bstack1l1ll1l1l1_opy_):
    if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᕔ"), None) and bstack11ll111l_opy_(
      threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᕕ"), None) and not bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬᕖ"), False):
      threading.current_thread().a11y_stop = True
      bstack11111l11l_opy_.bstack1l1l111lll_opy_(bstack1l1ll1l1l1_opy_, name=bstack1l1l1l1_opy_ (u"ࠥࠦᕗ"), path=bstack1l1l1l1_opy_ (u"ࠦࠧᕘ"))