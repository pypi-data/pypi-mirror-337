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
import threading
from bstack_utils.helper import bstack11ll11l1l_opy_
from bstack_utils.constants import bstack1l1111l1l1l_opy_, EVENTS, STAGE
from bstack_utils.bstack1l1llllll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l11l1lll1_opy_:
    bstack11l111111ll_opy_ = None
    @classmethod
    def bstack1lll11l111_opy_(cls):
        if cls.on() and os.getenv(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧḆ")):
            logger.info(
                bstack1l1l1l1_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫḇ").format(os.getenv(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢḈ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḉ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨḊ")] == bstack1l1l1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥḋ"):
            return False
        return True
    @classmethod
    def bstack111ll111111_opy_(cls, bs_config, framework=bstack1l1l1l1_opy_ (u"ࠨࠢḌ")):
        bstack1l111l1l11l_opy_ = False
        for fw in bstack1l1111l1l1l_opy_:
            if fw in framework:
                bstack1l111l1l11l_opy_ = True
        return bstack11ll11l1l_opy_(bs_config.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḍ"), bstack1l111l1l11l_opy_))
    @classmethod
    def bstack111l1lll111_opy_(cls, framework):
        return framework in bstack1l1111l1l1l_opy_
    @classmethod
    def bstack111ll1l1ll1_opy_(cls, bs_config, framework):
        return cls.bstack111ll111111_opy_(bs_config, framework) is True and cls.bstack111l1lll111_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬḎ"), None)
    @staticmethod
    def bstack11l11l1lll_opy_():
        if getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ḏ"), None):
            return {
                bstack1l1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨḐ"): bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩḑ"),
                bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬḒ"): getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪḓ"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫḔ"), None):
            return {
                bstack1l1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ḕ"): bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧḖ"),
                bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪḗ"): getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨḘ"), None)
            }
        return None
    @staticmethod
    def bstack111l1lll1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11l1lll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1111ll1_opy_(test, hook_name=None):
        bstack111l1ll1lll_opy_ = test.parent
        if hook_name in [bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪḙ"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧḚ"), bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ḛ"), bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪḜ")]:
            bstack111l1ll1lll_opy_ = test
        scope = []
        while bstack111l1ll1lll_opy_ is not None:
            scope.append(bstack111l1ll1lll_opy_.name)
            bstack111l1ll1lll_opy_ = bstack111l1ll1lll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack111l1ll1ll1_opy_(hook_type):
        if hook_type == bstack1l1l1l1_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢḝ"):
            return bstack1l1l1l1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢḞ")
        elif hook_type == bstack1l1l1l1_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣḟ"):
            return bstack1l1l1l1_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧḠ")
    @staticmethod
    def bstack111l1lll11l_opy_(bstack11ll1111l_opy_):
        try:
            if not bstack1l11l1lll1_opy_.on():
                return bstack11ll1111l_opy_
            if os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦḡ"), None) == bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧḢ"):
                tests = os.environ.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧḣ"), None)
                if tests is None or tests == bstack1l1l1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢḤ"):
                    return bstack11ll1111l_opy_
                bstack11ll1111l_opy_ = tests.split(bstack1l1l1l1_opy_ (u"ࠪ࠰ࠬḥ"))
                return bstack11ll1111l_opy_
        except Exception as exc:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧḦ") + str(str(exc)) + bstack1l1l1l1_opy_ (u"ࠧࠨḧ"))
        return bstack11ll1111l_opy_