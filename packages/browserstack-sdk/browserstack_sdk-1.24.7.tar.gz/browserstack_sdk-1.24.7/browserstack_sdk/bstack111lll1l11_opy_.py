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
class RobotHandler():
    def __init__(self, args, logger, bstack111l11lll1_opy_, bstack111l1lll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l11lll1_opy_ = bstack111l11lll1_opy_
        self.bstack111l1lll1l_opy_ = bstack111l1lll1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11l1111ll1_opy_(bstack111l11ll11_opy_):
        bstack111l11ll1l_opy_ = []
        if bstack111l11ll11_opy_:
            tokens = str(os.path.basename(bstack111l11ll11_opy_)).split(bstack1l1l1l1_opy_ (u"ࠣࡡࠥ࿈"))
            camelcase_name = bstack1l1l1l1_opy_ (u"ࠤࠣࠦ࿉").join(t.title() for t in tokens)
            suite_name, bstack111l11l1l1_opy_ = os.path.splitext(camelcase_name)
            bstack111l11ll1l_opy_.append(suite_name)
        return bstack111l11ll1l_opy_
    @staticmethod
    def bstack111l11l1ll_opy_(typename):
        if bstack1l1l1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ࿊") in typename:
            return bstack1l1l1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ࿋")
        return bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ࿌")