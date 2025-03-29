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
from browserstack_sdk.bstack1ll11111l1_opy_ import bstack1l111l1lll_opy_
from browserstack_sdk.bstack111lll1l11_opy_ import RobotHandler
def bstack1ll11ll1_opy_(framework):
    if framework.lower() == bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᢋ"):
        return bstack1l111l1lll_opy_.version()
    elif framework.lower() == bstack1l1l1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫᢌ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ᢍ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1l1_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࠨᢎ")
def bstack11lll1lll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᢏ"))
        framework_version.append(importlib.metadata.version(bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦᢐ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᢑ"))
        framework_version.append(importlib.metadata.version(bstack1l1l1l1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᢒ")))
    except:
        pass
    return {
        bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢓ"): bstack1l1l1l1_opy_ (u"࠭࡟ࠨᢔ").join(framework_name),
        bstack1l1l1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᢕ"): bstack1l1l1l1_opy_ (u"ࠨࡡࠪᢖ").join(framework_version)
    }