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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack11111ll1l1_opy_,
)
from bstack_utils.helper import  bstack11ll111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11ll111_opy_, bstack1llll1llll1_opy_, bstack1lll11lll11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll111ll_opy_ import bstack11ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lllll11ll1_opy_
from bstack_utils.percy import bstack1ll1111l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll11llll_opy_(bstack1lll11ll1l1_opy_):
    def __init__(self, bstack1ll1111111l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1ll1111111l_opy_ = bstack1ll1111111l_opy_
        self.percy = bstack1ll1111l1l_opy_()
        self.bstack11l1ll11l1_opy_ = bstack11ll11l1_opy_()
        self.bstack1ll11111111_opy_()
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.bstack1ll11111l1l_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l1ll1l_opy_(self, instance: bstack11111ll1l1_opy_, driver: object):
        bstack1ll11ll1lll_opy_ = TestFramework.bstack11111lllll_opy_(instance.context)
        for t in bstack1ll11ll1lll_opy_:
            bstack1ll11l11l11_opy_ = TestFramework.bstack1111l111l1_opy_(t, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
            if any(instance is d[1] for d in bstack1ll11l11l11_opy_) or instance == driver:
                return t
    def bstack1ll11111l1l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1111111l1l_opy_.bstack1ll1ll1l1l1_opy_(method_name):
                return
            platform_index = f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0)
            bstack1ll11l1l1l1_opy_ = self.bstack1ll11l1ll1l_opy_(instance, driver)
            bstack1l1lllll1ll_opy_ = TestFramework.bstack1111l111l1_opy_(bstack1ll11l1l1l1_opy_, TestFramework.bstack1l1llllllll_opy_, None)
            if not bstack1l1lllll1ll_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦᇑ"))
                return
            driver_command = f.bstack1ll1lll1lll_opy_(*args)
            for command in bstack11ll1l1111_opy_:
                if command == driver_command:
                    self.bstack1l1111l1_opy_(driver, platform_index)
            bstack11ll1lll1_opy_ = self.percy.bstack11ll1l1ll_opy_()
            if driver_command in bstack1l1lll1l11_opy_[bstack11ll1lll1_opy_]:
                self.bstack11l1ll11l1_opy_.bstack1l1l1l1111_opy_(bstack1l1lllll1ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨᇒ"), e)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
        bstack1ll11l11l11_opy_ = f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᇓ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠢࠣᇔ"))
            return
        if len(bstack1ll11l11l11_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᇕ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥᇖ"))
        bstack1l1lllllll1_opy_, bstack1ll11111ll1_opy_ = bstack1ll11l11l11_opy_[0]
        driver = bstack1l1lllllll1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᇗ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧᇘ"))
            return
        bstack1l1llllll11_opy_ = {
            TestFramework.bstack1lll111l11l_opy_: bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᇙ"),
            TestFramework.bstack1ll1ll1l1ll_opy_: bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᇚ"),
            TestFramework.bstack1l1llllllll_opy_: bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤᇛ")
        }
        bstack1ll11111l11_opy_ = { key: f.bstack1111l111l1_opy_(instance, key) for key in bstack1l1llllll11_opy_ }
        bstack1l1lllll1l1_opy_ = [key for key, value in bstack1ll11111l11_opy_.items() if not value]
        if bstack1l1lllll1l1_opy_:
            for key in bstack1l1lllll1l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦᇜ") + str(key) + bstack1l1l1l1_opy_ (u"ࠤࠥᇝ"))
            return
        platform_index = f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0)
        if self.bstack1ll1111111l_opy_.percy_capture_mode == bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᇞ"):
            bstack111ll1111_opy_ = bstack1ll11111l11_opy_.get(TestFramework.bstack1l1llllllll_opy_) + bstack1l1l1l1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᇟ")
            bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1ll111111ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111ll1111_opy_,
                bstack1lllll11l_opy_=bstack1ll11111l11_opy_[TestFramework.bstack1lll111l11l_opy_],
                bstack111ll111_opy_=bstack1ll11111l11_opy_[TestFramework.bstack1ll1ll1l1ll_opy_],
                bstack11lll11l1_opy_=platform_index
            )
            bstack1lll1l1ll11_opy_.end(EVENTS.bstack1ll111111ll_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᇠ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᇡ"), True, None, None, None, None, test_name=bstack111ll1111_opy_)
    def bstack1l1111l1_opy_(self, driver, platform_index):
        if self.bstack11l1ll11l1_opy_.bstack111111l1_opy_() is True or self.bstack11l1ll11l1_opy_.capturing() is True:
            return
        self.bstack11l1ll11l1_opy_.bstack11ll1l1ll1_opy_()
        while not self.bstack11l1ll11l1_opy_.bstack111111l1_opy_():
            bstack1l1lllll1ll_opy_ = self.bstack11l1ll11l1_opy_.bstack1l1l1ll11l_opy_()
            self.bstack1l1l11l1l1_opy_(driver, bstack1l1lllll1ll_opy_, platform_index)
        self.bstack11l1ll11l1_opy_.bstack1ll1l1ll11_opy_()
    def bstack1l1l11l1l1_opy_(self, driver, bstack11l1ll111l_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
        bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1l1l1lll_opy_.value)
        if test != None:
            bstack1lllll11l_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᇢ"), None)
            bstack111ll111_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇣ"), None)
            PercySDK.screenshot(driver, bstack11l1ll111l_opy_, bstack1lllll11l_opy_=bstack1lllll11l_opy_, bstack111ll111_opy_=bstack111ll111_opy_, bstack11lll11l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1ll111l_opy_)
        bstack1lll1l1ll11_opy_.end(EVENTS.bstack1l1l1lll_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᇤ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᇥ"), True, None, None, None, None, test_name=bstack11l1ll111l_opy_)
    def bstack1ll11111111_opy_(self):
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᇦ")] = str(self.bstack1ll1111111l_opy_.success)
        os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᇧ")] = str(self.bstack1ll1111111l_opy_.percy_capture_mode)
        self.percy.bstack1ll111111l1_opy_(self.bstack1ll1111111l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1llllll1l_opy_(self.bstack1ll1111111l_opy_.percy_build_id)