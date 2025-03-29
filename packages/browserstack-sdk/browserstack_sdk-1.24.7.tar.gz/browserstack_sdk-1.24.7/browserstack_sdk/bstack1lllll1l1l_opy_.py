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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llll1l1_opy_ = {}
        bstack11l1l1l1l1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫ๥"), bstack1l1l1l1_opy_ (u"ࠫࠬ๦"))
        if not bstack11l1l1l1l1_opy_:
            return bstack1llll1l1_opy_
        try:
            bstack11l1l1l11l_opy_ = json.loads(bstack11l1l1l1l1_opy_)
            if bstack1l1l1l1_opy_ (u"ࠧࡵࡳࠣ๧") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡴࠤ๨")] = bstack11l1l1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠢࡰࡵࠥ๩")]
            if bstack1l1l1l1_opy_ (u"ࠣࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ๪") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧ๫") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๬")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ๭"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ๮")))
            if bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࠢ๯") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧ๰") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨ๱")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࠥ๲"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ๳")))
            if bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ๴") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ๵") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢ๶")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤ๷"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ๸")))
            if bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࠤ๹") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢ๺") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣ๻")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࠧ๼"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ๽")))
            if bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ๾") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ๿") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ຀")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧກ"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥຂ")))
            if bstack1l1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ຃") in bstack11l1l1l11l_opy_ or bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣຄ") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ຅")] = bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠦຆ"), bstack11l1l1l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦງ")))
            if bstack1l1l1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧຈ") in bstack11l1l1l11l_opy_:
                bstack1llll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨຉ")] = bstack11l1l1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢຊ")]
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡡࡵࡣ࠽ࠤࠧ຋") +  str(error))
        return bstack1llll1l1_opy_