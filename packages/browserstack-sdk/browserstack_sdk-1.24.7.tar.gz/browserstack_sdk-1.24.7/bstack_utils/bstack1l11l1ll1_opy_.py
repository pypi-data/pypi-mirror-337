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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll111111_opy_, bstack1111lll1l_opy_, bstack11ll111l_opy_, bstack1l1l111ll1_opy_, \
    bstack11ll1ll11ll_opy_
from bstack_utils.measure import measure
def bstack1ll1l1l1_opy_(bstack111llll1lll_opy_):
    for driver in bstack111llll1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1ll1111l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack1ll1lllll1_opy_(driver, status, reason=bstack1l1l1l1_opy_ (u"ࠧࠨᱛ")):
    bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
    if bstack1l1l1111l_opy_.bstack111l1ll1l1_opy_():
        return
    bstack111lll1l_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᱜ"), bstack1l1l1l1_opy_ (u"ࠩࠪᱝ"), status, reason, bstack1l1l1l1_opy_ (u"ࠪࠫᱞ"), bstack1l1l1l1_opy_ (u"ࠫࠬᱟ"))
    driver.execute_script(bstack111lll1l_opy_)
@measure(event_name=EVENTS.bstack1ll1111l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
def bstack1l1ll1l11l_opy_(page, status, reason=bstack1l1l1l1_opy_ (u"ࠬ࠭ᱠ")):
    try:
        if page is None:
            return
        bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
        if bstack1l1l1111l_opy_.bstack111l1ll1l1_opy_():
            return
        bstack111lll1l_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᱡ"), bstack1l1l1l1_opy_ (u"ࠧࠨᱢ"), status, reason, bstack1l1l1l1_opy_ (u"ࠨࠩᱣ"), bstack1l1l1l1_opy_ (u"ࠩࠪᱤ"))
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᱥ"), bstack111lll1l_opy_)
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᱦ"), e)
def bstack1lll1ll1ll_opy_(type, name, status, reason, bstack11lll1111_opy_, bstack1l11lllll1_opy_):
    bstack1lll1l1ll1_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᱧ"): type,
        bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᱨ"): {}
    }
    if type == bstack1l1l1l1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᱩ"):
        bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᱪ")][bstack1l1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᱫ")] = bstack11lll1111_opy_
        bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᱬ")][bstack1l1l1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᱭ")] = json.dumps(str(bstack1l11lllll1_opy_))
    if type == bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᱮ"):
        bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᱯ")][bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᱰ")] = name
    if type == bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᱱ"):
        bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᱲ")][bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᱳ")] = status
        if status == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᱴ") and str(reason) != bstack1l1l1l1_opy_ (u"ࠧࠨᱵ"):
            bstack1lll1l1ll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᱶ")][bstack1l1l1l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᱷ")] = json.dumps(str(reason))
    bstack11ll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᱸ").format(json.dumps(bstack1lll1l1ll1_opy_))
    return bstack11ll1l11_opy_
def bstack1111l1l1l_opy_(url, config, logger, bstack1ll11111_opy_=False):
    hostname = bstack1111lll1l_opy_(url)
    is_private = bstack1l1l111ll1_opy_(hostname)
    try:
        if is_private or bstack1ll11111_opy_:
            file_path = bstack11lll111111_opy_(bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᱹ"), bstack1l1l1l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᱺ"), logger)
            if os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᱻ")) and eval(
                    os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᱼ"))):
                return
            if (bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᱽ") in config and not config[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ᱾")]):
                os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭᱿")] = str(True)
                bstack111llll1l11_opy_ = {bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᲀ"): hostname}
                bstack11ll1ll11ll_opy_(bstack1l1l1l1_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᲁ"), bstack1l1l1l1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᲂ"), bstack111llll1l11_opy_, logger)
    except Exception as e:
        pass
def bstack11llllll1l_opy_(caps, bstack111llll1ll1_opy_):
    if bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᲃ") in caps:
        caps[bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᲄ")][bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᲅ")] = True
        if bstack111llll1ll1_opy_:
            caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲆ")][bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᲇ")] = bstack111llll1ll1_opy_
    else:
        caps[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᲈ")] = True
        if bstack111llll1ll1_opy_:
            caps[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᲉ")] = bstack111llll1ll1_opy_
def bstack11l11111lll_opy_(bstack111ll111l1_opy_):
    bstack111llll1l1l_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᲊ"), bstack1l1l1l1_opy_ (u"࠭ࠧ᲋"))
    if bstack111llll1l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠧࠨ᲌") or bstack111llll1l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᲍"):
        threading.current_thread().testStatus = bstack111ll111l1_opy_
    else:
        if bstack111ll111l1_opy_ == bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᲎"):
            threading.current_thread().testStatus = bstack111ll111l1_opy_