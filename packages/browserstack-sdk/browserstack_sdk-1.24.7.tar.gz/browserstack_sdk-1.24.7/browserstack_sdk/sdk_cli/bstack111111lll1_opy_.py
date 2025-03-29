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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack111l111l11_opy_ import bstack111l11l111_opy_
class bstack1lll11ll1l1_opy_(abc.ABC):
    bin_session_id: str
    bstack111l111l11_opy_: bstack111l11l111_opy_
    def __init__(self):
        self.bstack1llll111l11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack111l111l11_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1llllllll11_opy_(self):
        return (self.bstack1llll111l11_opy_ != None and self.bin_session_id != None and self.bstack111l111l11_opy_ != None)
    def configure(self, bstack1llll111l11_opy_, config, bin_session_id: str, bstack111l111l11_opy_: bstack111l11l111_opy_):
        self.bstack1llll111l11_opy_ = bstack1llll111l11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack111l111l11_opy_ = bstack111l111l11_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࡤࠡ࡯ࡲࡨࡺࡲࡥࠡࡽࡶࡩࡱ࡬࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡ࠱ࡣࡤࡴࡡ࡮ࡧࡢࡣࢂࡀࠠࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤ࠾ࠤᅛ") + str(self.bin_session_id) + bstack1l1l1l1_opy_ (u"ࠨࠢᅜ"))
    def bstack1lll111l1l1_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠢࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡓࡵ࡮ࡦࠤᅝ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False