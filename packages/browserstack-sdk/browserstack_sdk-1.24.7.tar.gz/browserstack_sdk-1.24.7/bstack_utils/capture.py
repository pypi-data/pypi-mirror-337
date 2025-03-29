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
import builtins
import logging
class bstack11l11lllll_opy_:
    def __init__(self, handler):
        self._1l111l1lll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1l111l1ll11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᕙ"), bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᕚ"), bstack1l1l1l1_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᕛ"), bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᕜ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1l111l1l1ll_opy_
        self._1l111l1llll_opy_()
    def _1l111l1l1ll_opy_(self, *args, **kwargs):
        self._1l111l1lll1_opy_(*args, **kwargs)
        message = bstack1l1l1l1_opy_ (u"ࠩࠣࠫᕝ").join(map(str, args)) + bstack1l1l1l1_opy_ (u"ࠪࡠࡳ࠭ᕞ")
        self._log_message(bstack1l1l1l1_opy_ (u"ࠫࡎࡔࡆࡐࠩᕟ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᕠ"): level, bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕡ"): msg})
    def _1l111l1llll_opy_(self):
        for level, bstack1l111l1ll1l_opy_ in self._1l111l1ll11_opy_.items():
            setattr(logging, level, self._1l111l1l1l1_opy_(level, bstack1l111l1ll1l_opy_))
    def _1l111l1l1l1_opy_(self, level, bstack1l111l1ll1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1l111l1ll1l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1l111l1lll1_opy_
        for level, bstack1l111l1ll1l_opy_ in self._1l111l1ll11_opy_.items():
            setattr(logging, level, bstack1l111l1ll1l_opy_)