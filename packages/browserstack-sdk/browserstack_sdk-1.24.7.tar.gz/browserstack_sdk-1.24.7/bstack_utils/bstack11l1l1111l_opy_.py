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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1l111ll1l11_opy_, bstack1l111lllll1_opy_, bstack1111l1ll1_opy_, bstack111ll1llll_opy_, bstack11ll1llll11_opy_, bstack11ll1l111ll_opy_, bstack11ll1l11l1l_opy_, bstack1lll11llll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l111111ll_opy_ import bstack111llllll1l_opy_
import bstack_utils.bstack11l1l1ll1l_opy_ as bstack1ll11llll_opy_
from bstack_utils.bstack11l11ll1ll_opy_ import bstack1l11l1lll1_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack1l111lll1l_opy_ import bstack1l111lll1l_opy_
from bstack_utils.bstack11l11ll1l1_opy_ import bstack111lll1lll_opy_
bstack111ll11l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ᳎")
logger = logging.getLogger(__name__)
class bstack111111ll1_opy_:
    bstack11l111111ll_opy_ = None
    bs_config = None
    bstack1l11ll1ll_opy_ = None
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l111l11ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def launch(cls, bs_config, bstack1l11ll1ll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11ll1ll_opy_ = bstack1l11ll1ll_opy_
        try:
            cls.bstack111ll1lll11_opy_()
            bstack1l11l11l1l1_opy_ = bstack1l111ll1l11_opy_(bs_config)
            bstack1l111lll1l1_opy_ = bstack1l111lllll1_opy_(bs_config)
            data = bstack1ll11llll_opy_.bstack111ll1l1l11_opy_(bs_config, bstack1l11ll1ll_opy_)
            config = {
                bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡩࠩ᳏"): (bstack1l11l11l1l1_opy_, bstack1l111lll1l1_opy_),
                bstack1l1l1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᳐"): cls.default_headers()
            }
            response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫ᳑"), cls.request_url(bstack1l1l1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧ᳒")), data, config)
            if response.status_code != 200:
                bstack1llll1111ll_opy_ = response.json()
                if bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᳓")] == False:
                    cls.bstack111ll1llll1_opy_(bstack1llll1111ll_opy_)
                    return
                cls.bstack111ll11lll1_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ᳔ࠩ")])
                cls.bstack111lll11111_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ᳕ࠪ")])
                return None
            bstack111ll1l1111_opy_ = cls.bstack111ll1l11ll_opy_(response)
            return bstack111ll1l1111_opy_
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤ᳖").format(str(error)))
            return None
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def stop(cls, bstack111ll1l111l_opy_=None):
        if not bstack1l11l1lll1_opy_.on() and not bstack11111l11l_opy_.on():
            return
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕ᳗ࠩ")) == bstack1l1l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯᳘ࠦ") or os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᳙ࠬ")) == bstack1l1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨ᳚"):
            logger.error(bstack1l1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ᳛"))
            return {
                bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ᳜ࠪ"): bstack1l1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴ᳝ࠪ"),
                bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ᳞࠭"): bstack1l1l1l1_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧ᳟ࠫ")
            }
        try:
            cls.bstack11l111111ll_opy_.shutdown()
            data = {
                bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᳠"): bstack1lll11llll_opy_()
            }
            if not bstack111ll1l111l_opy_ is None:
                data[bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬ᳡")] = [{
                    bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯᳢ࠩ"): bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ᳣"),
                    bstack1l1l1l1_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯᳤ࠫ"): bstack111ll1l111l_opy_
                }]
            config = {
                bstack1l1l1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ᳥࠭"): cls.default_headers()
            }
            bstack11ll1lllll1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶ᳦ࠧ").format(os.environ[bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᳧ࠧ")])
            bstack111ll1l1l1l_opy_ = cls.request_url(bstack11ll1lllll1_opy_)
            response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠨࡒࡘࡘ᳨ࠬ"), bstack111ll1l1l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l1l1_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣᳩ"))
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢᳪ") + str(error))
            return {
                bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᳫ"): bstack1l1l1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᳬ"),
                bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫᳭ࠧ"): str(error)
            }
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def bstack111ll1l11ll_opy_(cls, response):
        bstack1llll1111ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack111ll1l1111_opy_ = {}
        if bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠧ࡫ࡹࡷࠫᳮ")) is None:
            os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᳯ")] = bstack1l1l1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧᳰ")
        else:
            os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᳱ")] = bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡯ࡽࡴࠨᳲ"), bstack1l1l1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᳳ"))
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᳴")] = bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᳵ"), bstack1l1l1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᳶ"))
        logger.info(bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧ᳷") + os.getenv(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᳸")));
        if bstack1l11l1lll1_opy_.bstack111ll1l1ll1_opy_(cls.bs_config, cls.bstack1l11ll1ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ᳹"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᳺ"))) is True:
            bstack111ll1l1lll_opy_, build_hashed_id, bstack111ll11l111_opy_ = cls.bstack111ll1ll111_opy_(bstack1llll1111ll_opy_)
            if bstack111ll1l1lll_opy_ != None and build_hashed_id != None:
                bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᳻")] = {
                    bstack1l1l1l1_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪ᳼"): bstack111ll1l1lll_opy_,
                    bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ᳽"): build_hashed_id,
                    bstack1l1l1l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭᳾"): bstack111ll11l111_opy_
                }
            else:
                bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ᳿")] = {}
        else:
            bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᴀ")] = {}
        if bstack11111l11l_opy_.bstack1l111lll11l_opy_(cls.bs_config) is True:
            bstack111ll11l1l1_opy_, build_hashed_id = cls.bstack111ll11ll11_opy_(bstack1llll1111ll_opy_)
            if bstack111ll11l1l1_opy_ != None and build_hashed_id != None:
                bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴁ")] = {
                    bstack1l1l1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪᴂ"): bstack111ll11l1l1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᴃ"): build_hashed_id,
                }
            else:
                bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴄ")] = {}
        else:
            bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴅ")] = {}
        if bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᴆ")].get(bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᴇ")) != None or bstack111ll1l1111_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴈ")].get(bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᴉ")) != None:
            cls.bstack111ll11l11l_opy_(bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠧ࡫ࡹࡷࠫᴊ")), bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᴋ")))
        return bstack111ll1l1111_opy_
    @classmethod
    def bstack111ll1ll111_opy_(cls, bstack1llll1111ll_opy_):
        if bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᴌ")) == None:
            cls.bstack111ll11lll1_opy_()
            return [None, None, None]
        if bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᴍ")][bstack1l1l1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᴎ")] != True:
            cls.bstack111ll11lll1_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᴏ")])
            return [None, None, None]
        logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᴐ"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᴑ")] = bstack1l1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᴒ")
        if bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭ᴓ")):
            os.environ[bstack1l1l1l1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧᴔ")] = json.dumps({
                bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ᴕ"): bstack1l111ll1l11_opy_(cls.bs_config),
                bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧᴖ"): bstack1l111lllll1_opy_(cls.bs_config)
            })
        if bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᴗ")):
            os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᴘ")] = bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᴙ")]
        if bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᴚ")].get(bstack1l1l1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᴛ"), {}).get(bstack1l1l1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᴜ")):
            os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᴝ")] = str(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᴞ")][bstack1l1l1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᴟ")][bstack1l1l1l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᴠ")])
        else:
            os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᴡ")] = bstack1l1l1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᴢ")
        return [bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡯ࡽࡴࠨᴣ")], bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᴤ")], os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᴥ")]]
    @classmethod
    def bstack111ll11ll11_opy_(cls, bstack1llll1111ll_opy_):
        if bstack1llll1111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴦ")) == None:
            cls.bstack111lll11111_opy_()
            return [None, None]
        if bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴧ")][bstack1l1l1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᴨ")] != True:
            cls.bstack111lll11111_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴩ")])
            return [None, None]
        if bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴪ")].get(bstack1l1l1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᴫ")):
            logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᴬ"))
            parsed = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᴭ"), bstack1l1l1l1_opy_ (u"ࠨࡽࢀࠫᴮ")))
            capabilities = bstack1ll11llll_opy_.bstack111ll11ll1l_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴯ")][bstack1l1l1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᴰ")][bstack1l1l1l1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴱ")], bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᴲ"), bstack1l1l1l1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᴳ"))
            bstack111ll11l1l1_opy_ = capabilities[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᴴ")]
            os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᴵ")] = bstack111ll11l1l1_opy_
            parsed[bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᴶ")] = capabilities[bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᴷ")]
            os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᴸ")] = json.dumps(parsed)
            scripts = bstack1ll11llll_opy_.bstack111ll11ll1l_opy_(bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴹ")][bstack1l1l1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᴺ")][bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᴻ")], bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᴼ"), bstack1l1l1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪᴽ"))
            bstack1l111lll1l_opy_.bstack1l11l11ll11_opy_(scripts)
            commands = bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴾ")][bstack1l1l1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᴿ")][bstack1l1l1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭ᵀ")].get(bstack1l1l1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᵁ"))
            bstack1l111lll1l_opy_.bstack1l11l1111ll_opy_(commands)
            bstack1l111lll1l_opy_.store()
        return [bstack111ll11l1l1_opy_, bstack1llll1111ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᵂ")]]
    @classmethod
    def bstack111ll11lll1_opy_(cls, response=None):
        os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᵃ")] = bstack1l1l1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧᵄ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᵅ")] = bstack1l1l1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᵆ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫᵇ")] = bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᵈ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᵉ")] = bstack1l1l1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᵊ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᵋ")] = bstack1l1l1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᵌ")
        cls.bstack111ll1llll1_opy_(response, bstack1l1l1l1_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᵍ"))
        return [None, None, None]
    @classmethod
    def bstack111lll11111_opy_(cls, response=None):
        os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᵎ")] = bstack1l1l1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᵏ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᵐ")] = bstack1l1l1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᵑ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᵒ")] = bstack1l1l1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᵓ")
        cls.bstack111ll1llll1_opy_(response, bstack1l1l1l1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᵔ"))
        return [None, None, None]
    @classmethod
    def bstack111ll11l11l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᵕ")] = jwt
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᵖ")] = build_hashed_id
    @classmethod
    def bstack111ll1llll1_opy_(cls, response=None, product=bstack1l1l1l1_opy_ (u"ࠢࠣᵗ")):
        if response == None:
            logger.error(product + bstack1l1l1l1_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥᵘ"))
        for error in response[bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᵙ")]:
            bstack1l11111111l_opy_ = error[bstack1l1l1l1_opy_ (u"ࠪ࡯ࡪࡿࠧᵚ")]
            error_message = error[bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᵛ")]
            if error_message:
                if bstack1l11111111l_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦᵜ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l1l1_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢᵝ") + product + bstack1l1l1l1_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᵞ"))
    @classmethod
    def bstack111ll1lll11_opy_(cls):
        if cls.bstack11l111111ll_opy_ is not None:
            return
        cls.bstack11l111111ll_opy_ = bstack111llllll1l_opy_(cls.bstack111ll1ll1l1_opy_)
        cls.bstack11l111111ll_opy_.start()
    @classmethod
    def bstack111llllll1_opy_(cls):
        if cls.bstack11l111111ll_opy_ is None:
            return
        cls.bstack11l111111ll_opy_.shutdown()
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def bstack111ll1ll1l1_opy_(cls, bstack111ll1l1l1_opy_, event_url=bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᵟ")):
        config = {
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᵠ"): cls.default_headers()
        }
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥᵡ").format(bstack1l1l1l1_opy_ (u"ࠫ࠱ࠦࠧᵢ").join([event[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᵣ")] for event in bstack111ll1l1l1_opy_])))
        response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫᵤ"), cls.request_url(event_url), bstack111ll1l1l1_opy_, config)
        bstack1l11l11ll1l_opy_ = response.json()
    @classmethod
    def bstack11ll1ll111_opy_(cls, bstack111ll1l1l1_opy_, event_url=bstack1l1l1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᵥ")):
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣᵦ").format(bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᵧ")]))
        if not bstack1ll11llll_opy_.bstack111ll11llll_opy_(bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᵨ")]):
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤᵩ").format(bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᵪ")]))
            return
        bstack11ll11l1l1_opy_ = bstack1ll11llll_opy_.bstack111ll1ll1ll_opy_(bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᵫ")], bstack111ll1l1l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᵬ")))
        if bstack11ll11l1l1_opy_ != None:
            if bstack111ll1l1l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᵭ")) != None:
                bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᵮ")][bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨᵯ")] = bstack11ll11l1l1_opy_
            else:
                bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩᵰ")] = bstack11ll11l1l1_opy_
        if event_url == bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᵱ"):
            cls.bstack111ll1lll11_opy_()
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤᵲ").format(bstack111ll1l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᵳ")]))
            cls.bstack11l111111ll_opy_.add(bstack111ll1l1l1_opy_)
        elif event_url == bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᵴ"):
            cls.bstack111ll1ll1l1_opy_([bstack111ll1l1l1_opy_], event_url)
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def bstack1l11l1l1_opy_(cls, logs):
        bstack111lll1111l_opy_ = []
        for log in logs:
            bstack111ll1lllll_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᵵ"): bstack1l1l1l1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬᵶ"),
                bstack1l1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᵷ"): log[bstack1l1l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᵸ")],
                bstack1l1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᵹ"): log[bstack1l1l1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᵺ")],
                bstack1l1l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨᵻ"): {},
                bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᵼ"): log[bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᵽ")],
            }
            if bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵾ") in log:
                bstack111ll1lllll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵿ")] = log[bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶀ")]
            elif bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶁ") in log:
                bstack111ll1lllll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᶂ")] = log[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶃ")]
            bstack111lll1111l_opy_.append(bstack111ll1lllll_opy_)
        cls.bstack11ll1ll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᶄ"): bstack1l1l1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᶅ"),
            bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᶆ"): bstack111lll1111l_opy_
        })
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def bstack111ll111lll_opy_(cls, steps):
        bstack111ll1ll11l_opy_ = []
        for step in steps:
            bstack111ll111ll1_opy_ = {
                bstack1l1l1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫᶇ"): bstack1l1l1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪᶈ"),
                bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᶉ"): step[bstack1l1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᶊ")],
                bstack1l1l1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᶋ"): step[bstack1l1l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᶌ")],
                bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᶍ"): step[bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᶎ")],
                bstack1l1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᶏ"): step[bstack1l1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᶐ")]
            }
            if bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶑ") in step:
                bstack111ll111ll1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶒ")] = step[bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶓ")]
            elif bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᶔ") in step:
                bstack111ll111ll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶕ")] = step[bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶖ")]
            bstack111ll1ll11l_opy_.append(bstack111ll111ll1_opy_)
        cls.bstack11ll1ll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᶗ"): bstack1l1l1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᶘ"),
            bstack1l1l1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᶙ"): bstack111ll1ll11l_opy_
        })
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack111l11ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack11llll111_opy_(cls, screenshot):
        cls.bstack11ll1ll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᶚ"): bstack1l1l1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᶛ"),
            bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡩࡶࠫᶜ"): [{
                bstack1l1l1l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᶝ"): bstack1l1l1l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪᶞ"),
                bstack1l1l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᶟ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬᶠ"),
                bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᶡ"): screenshot[bstack1l1l1l1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᶢ")],
                bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶣ"): screenshot[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶤ")]
            }]
        }, event_url=bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᶥ"))
    @classmethod
    @bstack111ll1llll_opy_(class_method=True)
    def bstack1l111111l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1ll111_opy_({
            bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᶦ"): bstack1l1l1l1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᶧ"),
            bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᶨ"): {
                bstack1l1l1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥᶩ"): cls.current_test_uuid(),
                bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧᶪ"): cls.bstack11l1l11l11_opy_(driver)
            }
        })
    @classmethod
    def bstack11l11ll111_opy_(cls, event: str, bstack111ll1l1l1_opy_: bstack111lll1lll_opy_):
        bstack11l111l1l1_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᶫ"): event,
            bstack111ll1l1l1_opy_.bstack11l111l1ll_opy_(): bstack111ll1l1l1_opy_.bstack11l111lll1_opy_(event)
        }
        cls.bstack11ll1ll111_opy_(bstack11l111l1l1_opy_)
        result = getattr(bstack111ll1l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᶬ"), None)
        if event == bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᶭ"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᶮ"): bstack1l1l1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᶯ")}
        elif event == bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᶰ"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᶱ"): getattr(result, bstack1l1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᶲ"), bstack1l1l1l1_opy_ (u"ࠨࠩᶳ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᶴ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᶵ")] == bstack1l1l1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᶶ")) and (os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᶷ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᶸ")] == bstack1l1l1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᶹ")):
            return False
        return True
    @staticmethod
    def bstack111ll1l11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111111ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᶺ"): bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᶻ"),
            bstack1l1l1l1_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ᶼ"): bstack1l1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩᶽ")
        }
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᶾ"), None):
            headers[bstack1l1l1l1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᶿ")] = bstack1l1l1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ᷀").format(os.environ[bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ᷁")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1l1l1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᷂").format(bstack111ll11l1ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ᷃"), None)
    @staticmethod
    def bstack11l1l11l11_opy_(driver):
        return {
            bstack11ll1llll11_opy_(): bstack11ll1l111ll_opy_(driver)
        }
    @staticmethod
    def bstack111ll1lll1l_opy_(exception_info, report):
        return [{bstack1l1l1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ᷄"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111l11l1ll_opy_(typename):
        if bstack1l1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ᷅") in typename:
            return bstack1l1l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᷆")
        return bstack1l1l1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ᷇")