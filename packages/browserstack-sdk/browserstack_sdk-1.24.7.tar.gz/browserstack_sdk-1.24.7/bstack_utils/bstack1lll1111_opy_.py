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
class bstack1l111lll11_opy_:
    def __init__(self, handler):
        self._111lllll1l1_opy_ = None
        self.handler = handler
        self._111lllll1ll_opy_ = self.bstack111lllll111_opy_()
        self.patch()
    def patch(self):
        self._111lllll1l1_opy_ = self._111lllll1ll_opy_.execute
        self._111lllll1ll_opy_.execute = self.bstack111lllll11l_opy_()
    def bstack111lllll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧ᱙"), driver_command, None, this, args)
            response = self._111lllll1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1l1_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᱚ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._111lllll1ll_opy_.execute = self._111lllll1l1_opy_
    @staticmethod
    def bstack111lllll111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver