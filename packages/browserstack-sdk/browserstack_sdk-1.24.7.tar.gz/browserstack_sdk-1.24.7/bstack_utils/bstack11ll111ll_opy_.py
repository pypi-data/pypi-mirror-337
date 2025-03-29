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
from collections import deque
from bstack_utils.constants import *
class bstack11ll11l1_opy_:
    def __init__(self):
        self._11l11ll111l_opy_ = deque()
        self._11l11ll1111_opy_ = {}
        self._11l11l11ll1_opy_ = False
    def bstack11l11ll11l1_opy_(self, test_name, bstack11l11l1llll_opy_):
        bstack11l11l1lll1_opy_ = self._11l11ll1111_opy_.get(test_name, {})
        return bstack11l11l1lll1_opy_.get(bstack11l11l1llll_opy_, 0)
    def bstack11l11l1l1ll_opy_(self, test_name, bstack11l11l1llll_opy_):
        bstack11l11l11lll_opy_ = self.bstack11l11ll11l1_opy_(test_name, bstack11l11l1llll_opy_)
        self.bstack11l11l1l111_opy_(test_name, bstack11l11l1llll_opy_)
        return bstack11l11l11lll_opy_
    def bstack11l11l1l111_opy_(self, test_name, bstack11l11l1llll_opy_):
        if test_name not in self._11l11ll1111_opy_:
            self._11l11ll1111_opy_[test_name] = {}
        bstack11l11l1lll1_opy_ = self._11l11ll1111_opy_[test_name]
        bstack11l11l11lll_opy_ = bstack11l11l1lll1_opy_.get(bstack11l11l1llll_opy_, 0)
        bstack11l11l1lll1_opy_[bstack11l11l1llll_opy_] = bstack11l11l11lll_opy_ + 1
    def bstack1l1l1l1111_opy_(self, bstack11l11l1ll11_opy_, bstack11l11l1ll1l_opy_):
        bstack11l11l1l1l1_opy_ = self.bstack11l11l1l1ll_opy_(bstack11l11l1ll11_opy_, bstack11l11l1ll1l_opy_)
        event_name = bstack1l1111lll11_opy_[bstack11l11l1ll1l_opy_]
        bstack1l1lllll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᯡ").format(bstack11l11l1ll11_opy_, event_name, bstack11l11l1l1l1_opy_)
        self._11l11ll111l_opy_.append(bstack1l1lllll1ll_opy_)
    def bstack111111l1_opy_(self):
        return len(self._11l11ll111l_opy_) == 0
    def bstack1l1l1ll11l_opy_(self):
        bstack11l11l1l11l_opy_ = self._11l11ll111l_opy_.popleft()
        return bstack11l11l1l11l_opy_
    def capturing(self):
        return self._11l11l11ll1_opy_
    def bstack11ll1l1ll1_opy_(self):
        self._11l11l11ll1_opy_ = True
    def bstack1ll1l1ll11_opy_(self):
        self._11l11l11ll1_opy_ = False