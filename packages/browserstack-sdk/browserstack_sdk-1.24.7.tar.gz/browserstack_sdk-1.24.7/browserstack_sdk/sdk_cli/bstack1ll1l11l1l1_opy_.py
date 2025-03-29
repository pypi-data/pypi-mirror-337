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
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack1111l11l1l_opy_,
    bstack11111ll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l11_opy_ import bstack1lllllll1ll_opy_
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import bstack1111lllll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
import weakref
class bstack1ll1l11ll11_opy_(bstack1lll11ll1l1_opy_):
    bstack1ll1l111l1l_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack11111ll1l1_opy_]]
    pages: Dict[str, Tuple[Callable, bstack11111ll1l1_opy_]]
    def __init__(self, bstack1ll1l111l1l_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1ll1l11l111_opy_ = dict()
        self.bstack1ll1l111l1l_opy_ = bstack1ll1l111l1l_opy_
        self.frameworks = frameworks
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l111ll_opy_, bstack1111l1111l_opy_.POST), self.__1ll1l111lll_opy_)
        if any(bstack1111111l1l_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1111111l1l_opy_.bstack1lll1111l11_opy_(
                (bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.__1ll1l11l11l_opy_
            )
            bstack1111111l1l_opy_.bstack1lll1111l11_opy_(
                (bstack1111l1l11l_opy_.QUIT, bstack1111l1111l_opy_.POST), self.__1ll1l11111l_opy_
            )
    def __1ll1l111lll_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        bstack1ll1l111l11_opy_: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1l1l1_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᅞ"):
                return
            contexts = bstack1ll1l111l11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1l1l1_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢᅟ") in page.url:
                                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᅠ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, self.bstack1ll1l111l1l_opy_, True)
                                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡳࡥ࡬࡫࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᅡ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠧࠨᅢ"))
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࠼ࠥᅣ"),e)
    def __1ll1l11l11l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1111l11l1l_opy_.bstack1111l111l1_opy_(instance, self.bstack1ll1l111l1l_opy_, False):
            return
        if not f.bstack1ll1l11llll_opy_(f.hub_url(driver)):
            self.bstack1ll1l11l111_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, self.bstack1ll1l111l1l_opy_, True)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᅤ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠣࠤᅥ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, self.bstack1ll1l111l1l_opy_, True)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡ࡬ࡲ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᅦ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠥࠦᅧ"))
    def __1ll1l11111l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1ll1l11ll1l_opy_(instance)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡤࡥ࡯࡯ࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡶࡻࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᅨ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠧࠨᅩ"))
    def bstack1ll1l1111ll_opy_(self, context: bstack1111lllll1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111ll1l1_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1ll1l111ll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1111111l1l_opy_.bstack1ll1l1llll1_opy_(data[1])
                    and data[1].bstack1ll1l111ll1_opy_(context)
                    and getattr(data[0](), bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᅪ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll11l_opy_, reverse=reverse)
    def bstack1ll1l11l1ll_opy_(self, context: bstack1111lllll1_opy_, reverse=True) -> List[Tuple[Callable, bstack11111ll1l1_opy_]]:
        matches = []
        for data in self.bstack1ll1l11l111_opy_.values():
            if (
                data[1].bstack1ll1l111ll1_opy_(context)
                and getattr(data[0](), bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᅫ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack11111ll11l_opy_, reverse=reverse)
    def bstack1ll1l1111l1_opy_(self, instance: bstack11111ll1l1_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1ll1l11ll1l_opy_(self, instance: bstack11111ll1l1_opy_) -> bool:
        if self.bstack1ll1l1111l1_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, self.bstack1ll1l111l1l_opy_, False)
            return True
        return False