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
from datetime import datetime, timezone
from pyexpat import features
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import bstack1111ll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l1lll1_opy_,
    bstack1lll11ll111_opy_,
    bstack1llll1llll1_opy_,
    bstack1l11llll111_opy_,
    bstack1lll11lll11_opy_,
)
import traceback
from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
from bstack_utils.constants import EVENTS
class PytestBDDFramework(TestFramework):
    bstack1l11lll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣጉ")
    bstack1l1l11l1111_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢጊ")
    bstack1l11ll11ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤጋ")
    bstack1l1l11l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨጌ")
    bstack1l11ll1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣግ")
    bstack1l11lll1l1l_opy_: bool
    bstack1l11lllll11_opy_ = [
        bstack1lll1l1lll1_opy_.BEFORE_ALL,
        bstack1lll1l1lll1_opy_.AFTER_ALL,
        bstack1lll1l1lll1_opy_.BEFORE_EACH,
        bstack1lll1l1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l1111l1l_opy_: Dict[str, str],
        bstack1ll1ll1l11l_opy_: List[str]=[bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥጎ")],
    ):
        super().__init__(bstack1ll1ll1l11l_opy_, bstack1l1l1111l1l_opy_)
        self.bstack1l11lll1l1l_opy_ = any(bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦጏ") in item.lower() for item in bstack1ll1ll1l11l_opy_)
    def track_event(
        self,
        context: bstack1l11llll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll1llll1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l1lll1_opy_.NONE:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤጐ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥ጑"))
            return
        if not self.bstack1l11lll1l1l_opy_:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦጒ") + str(str(self.bstack1ll1ll1l11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠦࠧጓ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢጔ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢጕ"))
            return
        instance = self.__1l1l1111ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨ጖") + str(args) + bstack1l1l1l1_opy_ (u"ࠣࠤ጗"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11lllll11_opy_ and test_hook_state == bstack1llll1llll1_opy_.PRE:
                bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1ll111l1l1_opy_.value)
                name = str(EVENTS.bstack1ll111l1l1_opy_.name)+bstack1l1l1l1_opy_ (u"ࠤ࠽ࠦጘ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll11l11_opy_(instance, name, bstack1lll11111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢጙ").format(e))
        try:
            if test_framework_state == bstack1lll1l1lll1_opy_.TEST:
                if not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1l11ll1111l_opy_) and test_hook_state == bstack1llll1llll1_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l1l111l1l1_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦጚ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠧࠨጛ"))
                if test_hook_state == bstack1llll1llll1_opy_.PRE and not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_):
                    TestFramework.bstack1111lll1l1_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11llll11l_opy_(instance, args)
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦጜ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠢࠣጝ"))
                elif test_hook_state == bstack1llll1llll1_opy_.POST and not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll1111llll_opy_):
                    TestFramework.bstack1111lll1l1_opy_(instance, TestFramework.bstack1ll1111llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦጞ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠤࠥጟ"))
            elif test_framework_state == bstack1lll1l1lll1_opy_.STEP:
                if test_hook_state == bstack1llll1llll1_opy_.PRE:
                    PytestBDDFramework.__1l1l11l11l1_opy_(instance, args)
                elif test_hook_state == bstack1llll1llll1_opy_.POST:
                    PytestBDDFramework.__1l11ll111ll_opy_(instance, args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG and test_hook_state == bstack1llll1llll1_opy_.POST:
                PytestBDDFramework.__1l1l11ll11l_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT and test_hook_state == bstack1llll1llll1_opy_.POST:
                self.__1l1l11ll1l1_opy_(instance, *args)
            elif test_framework_state in PytestBDDFramework.bstack1l11lllll11_opy_:
                self.__1l1l11l111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦጠ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧጡ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l11lllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11lllll11_opy_ and test_hook_state == bstack1llll1llll1_opy_.POST:
                name = str(EVENTS.bstack1ll111l1l1_opy_.name)+bstack1l1l1l1_opy_ (u"ࠧࡀࠢጢ")+str(test_framework_state.name)
                bstack1lll11111ll_opy_ = TestFramework.bstack1l1l111ll1l_opy_(instance, name)
                bstack1lll1l1ll11_opy_.end(EVENTS.bstack1ll111l1l1_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨጣ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧጤ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣጥ").format(e))
    def bstack1ll11lll111_opy_(self):
        return self.bstack1l11lll1l1l_opy_
    def __1l1l11111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨጦ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l11l_opy_(rep, [bstack1l1l1l1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣጧ"), bstack1l1l1l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧጨ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧጩ"), bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨጪ"), bstack1l1l1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣጫ"), bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢጬ")])
        return None
    def __1l1l11ll1l1_opy_(self, instance: bstack1lll11ll111_opy_, *args):
        result = self.__1l1l11111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack111l11l1ll_opy_ = None
        if result.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥጭ"), None) == bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥጮ") and len(args) > 1 and getattr(args[1], bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧጯ"), None) is not None:
            failure = [{bstack1l1l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨጰ"): [args[1].excinfo.exconly(), result.get(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧጱ"), None)]}]
            bstack111l11l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣጲ") if bstack1l1l1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦጳ") in getattr(args[1].excinfo, bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦጴ"), bstack1l1l1l1_opy_ (u"ࠥࠦጵ")) else bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧጶ")
        bstack1l1l111l111_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨጷ"), TestFramework.bstack1l11llll1ll_opy_)
        if bstack1l1l111l111_opy_ != TestFramework.bstack1l11llll1ll_opy_:
            TestFramework.bstack1111lll1l1_opy_(instance, TestFramework.bstack1ll11lll11l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l1l11l11ll_opy_(instance, {
            TestFramework.bstack1l1ll1l1l1l_opy_: failure,
            TestFramework.bstack1l11llll1l1_opy_: bstack111l11l1ll_opy_,
            TestFramework.bstack1l1ll1lllll_opy_: bstack1l1l111l111_opy_,
        })
    def __1l1l1111ll1_opy_(
        self,
        context: bstack1l11llll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll1llll1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l1lll1_opy_.SETUP_FIXTURE:
            instance = self.__1l1l111llll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1ll1l_opy_ bstack1l11lllllll_opy_ this to be bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨጸ")
            if test_framework_state == bstack1lll1l1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1l11l1ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧጹ"), None), bstack1l1l1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣጺ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢጻ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥጼ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1111ll1ll1_opy_(target) if target else None
        return instance
    def __1l1l11l111l_opy_(
        self,
        instance: bstack1lll11ll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll1llll1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11llllll1_opy_ = TestFramework.bstack1111l111l1_opy_(instance, PytestBDDFramework.bstack1l1l11l1111_opy_, {})
        if not key in bstack1l11llllll1_opy_:
            bstack1l11llllll1_opy_[key] = []
        bstack1l1l1111l11_opy_ = TestFramework.bstack1111l111l1_opy_(instance, PytestBDDFramework.bstack1l11ll11ll1_opy_, {})
        if not key in bstack1l1l1111l11_opy_:
            bstack1l1l1111l11_opy_[key] = []
        bstack1l1l1111111_opy_ = {
            PytestBDDFramework.bstack1l1l11l1111_opy_: bstack1l11llllll1_opy_,
            PytestBDDFramework.bstack1l11ll11ll1_opy_: bstack1l1l1111l11_opy_,
        }
        if test_hook_state == bstack1llll1llll1_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1l1l1_opy_ (u"ࠦࡰ࡫ࡹࠣጽ"): key,
                TestFramework.bstack1l11ll1ll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1lllll_opy_: TestFramework.bstack1l1l11l1l11_opy_,
                TestFramework.bstack1l11lll1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll111l_opy_: [],
                TestFramework.bstack1l1l11lll11_opy_: hook_name
            }
            bstack1l11llllll1_opy_[key].append(hook)
            bstack1l1l1111111_opy_[PytestBDDFramework.bstack1l1l11l1lll_opy_] = key
        elif test_hook_state == bstack1llll1llll1_opy_.POST:
            bstack1l11ll1l1l1_opy_ = bstack1l11llllll1_opy_.get(key, [])
            hook = bstack1l11ll1l1l1_opy_.pop() if bstack1l11ll1l1l1_opy_ else None
            if hook:
                result = self.__1l1l11111ll_opy_(*args)
                if result:
                    bstack1l11ll11l1l_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨጾ"), TestFramework.bstack1l1l11l1l11_opy_)
                    if bstack1l11ll11l1l_opy_ != TestFramework.bstack1l1l11l1l11_opy_:
                        hook[TestFramework.bstack1l11l1lllll_opy_] = bstack1l11ll11l1l_opy_
                hook[TestFramework.bstack1l1l11llll1_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1l1111l11_opy_[key].append(hook)
                bstack1l1l1111111_opy_[PytestBDDFramework.bstack1l11ll1lll1_opy_] = key
        TestFramework.bstack1l1l11l11ll_opy_(instance, bstack1l1l1111111_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧጿ") + str(bstack1l1l1111l11_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣፀ"))
    def __1l1l111llll_opy_(
        self,
        context: bstack1l11llll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll1llll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l11l_opy_(args[0], [bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢፁ"), bstack1l1l1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥፂ"), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥፃ"), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡪࡳࠣፄ"), bstack1l1l1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢፅ"), bstack1l1l1l1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨፆ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨፇ")) else fixturedef.get(bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢፈ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1l1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢፉ")) else None
        node = request.node if hasattr(request, bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣፊ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1l1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦፋ")) else None
        baseid = fixturedef.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧፌ"), None) or bstack1l1l1l1_opy_ (u"ࠨࠢፍ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1l1l1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧፎ")):
            target = PytestBDDFramework.__1l11l1lll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥፏ")) else None
            if target and not TestFramework.bstack1111ll1ll1_opy_(target):
                self.__1l1l11l1ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦፐ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠥࠦፑ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤፒ") + str(target) + bstack1l1l1l1_opy_ (u"ࠧࠨፓ"))
            return None
        instance = TestFramework.bstack1111ll1ll1_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣፔ") + str(target) + bstack1l1l1l1_opy_ (u"ࠢࠣፕ"))
            return None
        bstack1l1l1l111ll_opy_ = TestFramework.bstack1111l111l1_opy_(instance, PytestBDDFramework.bstack1l11lll1lll_opy_, {})
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤፖ"), bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦፗ")) == bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧፘ"):
            bstack1l11lll1111_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࠿ࠨፙ").join((scope, fixturename))
            bstack1l1l111111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll1l1ll_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠧࡱࡥࡺࠤፚ"): bstack1l11lll1111_opy_,
                bstack1l1l1l1_opy_ (u"ࠨࡴࡢࡩࡶࠦ፛"): PytestBDDFramework.__1l1l1l1111l_opy_(request.node, scenario),
                bstack1l1l1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣ፜"): fixturedef,
                bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ፝"): scope,
                bstack1l1l1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ፞"): None,
            }
            try:
                if test_hook_state == bstack1llll1llll1_opy_.POST and callable(getattr(args[-1], bstack1l1l1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ፟"), None)):
                    bstack1l11ll1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤ፠")] = TestFramework.bstack1ll111lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1llll1_opy_.PRE:
                bstack1l11ll1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥ፡")] = uuid4().__str__()
                bstack1l11ll1l1ll_opy_[PytestBDDFramework.bstack1l11lll1ll1_opy_] = bstack1l1l111111l_opy_
            elif test_hook_state == bstack1llll1llll1_opy_.POST:
                bstack1l11ll1l1ll_opy_[PytestBDDFramework.bstack1l1l11llll1_opy_] = bstack1l1l111111l_opy_
            if bstack1l11lll1111_opy_ in bstack1l1l1l111ll_opy_:
                bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_].update(bstack1l11ll1l1ll_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢ።") + str(bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_]) + bstack1l1l1l1_opy_ (u"ࠢࠣ፣"))
            else:
                bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_] = bstack1l11ll1l1ll_opy_
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦ፤") + str(len(bstack1l1l1l111ll_opy_)) + bstack1l1l1l1_opy_ (u"ࠤࠥ፥"))
        TestFramework.bstack1111lll1l1_opy_(instance, PytestBDDFramework.bstack1l11lll1lll_opy_, bstack1l1l1l111ll_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ፦") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠦࠧ፧"))
        return instance
    def __1l1l11l1ll1_opy_(
        self,
        context: bstack1l11llll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111ll1111_opy_.create_context(target)
        ob = bstack1lll11ll111_opy_(ctx, self.bstack1ll1ll1l11l_opy_, self.bstack1l1l1111l1l_opy_, test_framework_state)
        TestFramework.bstack1l1l11l11ll_opy_(ob, {
            TestFramework.bstack1ll1llll1ll_opy_: context.test_framework_name,
            TestFramework.bstack1ll11l1lll1_opy_: context.test_framework_version,
            TestFramework.bstack1l1l111l11l_opy_: [],
            PytestBDDFramework.bstack1l11lll1lll_opy_: {},
            PytestBDDFramework.bstack1l11ll11ll1_opy_: {},
            PytestBDDFramework.bstack1l1l11l1111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111lll1l1_opy_(ob, TestFramework.bstack1l11lll11ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111lll1l1_opy_(ob, TestFramework.bstack1ll1lll1ll1_opy_, context.platform_index)
        TestFramework.bstack11111l1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧ፨") + str(TestFramework.bstack11111l1ll1_opy_.keys()) + bstack1l1l1l1_opy_ (u"ࠨࠢ፩"))
        return ob
    @staticmethod
    def __1l11llll11l_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪ፪"): id(step),
                bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡼࡹ࠭፫"): step.name,
                bstack1l1l1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ፬"): step.keyword,
            })
        meta = {
            bstack1l1l1l1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫ፭"): {
                bstack1l1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ፮"): feature.name,
                bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ፯"): feature.filename,
                bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ፰"): feature.description
            },
            bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩ፱"): {
                bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭፲"): scenario.name
            },
            bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ፳"): steps,
            bstack1l1l1l1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬ፴"): PytestBDDFramework.__1l11ll1llll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11lllll1l_opy_: meta
            }
        )
    @staticmethod
    def __1l1l11l11l1_opy_(instance, args):
        request, bstack1l1l11lll1l_opy_ = args
        bstack1l1l111l1ll_opy_ = id(bstack1l1l11lll1l_opy_)
        bstack1l11ll1l111_opy_ = instance.data[TestFramework.bstack1l11lllll1l_opy_]
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠫ࡮ࡪࠧ፵")] == bstack1l1l111l1ll_opy_, bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ፶")]), None)
        step.update({
            bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ፷"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭፸")]) if st[bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫ፹")] == step[bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬ፺")]), None)
        if index is not None:
            bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ፻")][index] = step
        instance.data[TestFramework.bstack1l11lllll1l_opy_] = bstack1l11ll1l111_opy_
    @staticmethod
    def __1l11ll111ll_opy_(instance, args):
        bstack1l1l1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ፼")
        bstack1l1l11111l1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l1l11lll1l_opy_ = args[1]
        bstack1l1l111l1ll_opy_ = id(bstack1l1l11lll1l_opy_)
        bstack1l11ll1l111_opy_ = instance.data[TestFramework.bstack1l11lllll1l_opy_]
        step = None
        if bstack1l1l111l1ll_opy_ is not None and bstack1l11ll1l111_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ፽")):
            step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩ፾")] == bstack1l1l111l1ll_opy_, bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭፿")]), None)
            step.update({
                bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᎀ"): bstack1l1l11111l1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᎁ"): bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᎂ"),
                bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᎃ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᎄ"): bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᎅ"),
                })
        index = next((i for i, st in enumerate(bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᎆ")]) if st[bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫᎇ")] == step[bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬᎈ")]), None)
        if index is not None:
            bstack1l11ll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᎉ")][index] = step
        instance.data[TestFramework.bstack1l11lllll1l_opy_] = bstack1l11ll1l111_opy_
    @staticmethod
    def __1l11ll1llll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᎊ")):
                examples = list(node.callspec.params[bstack1l1l1l1_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᎋ")].values())
            return examples
        except:
            return []
    def bstack1ll11lll1l1_opy_(self, instance: bstack1lll11ll111_opy_, bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_]):
        bstack1l1l1111lll_opy_ = (
            PytestBDDFramework.bstack1l1l11l1lll_opy_
            if bstack1111l1llll_opy_[1] == bstack1llll1llll1_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1lll1_opy_
        )
        hook = PytestBDDFramework.bstack1l11ll1l11l_opy_(instance, bstack1l1l1111lll_opy_)
        entries = hook.get(TestFramework.bstack1l11lll111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, []))
        return entries
    def bstack1ll11llll11_opy_(self, instance: bstack1lll11ll111_opy_, bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_]):
        bstack1l1l1111lll_opy_ = (
            PytestBDDFramework.bstack1l1l11l1lll_opy_
            if bstack1111l1llll_opy_[1] == bstack1llll1llll1_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1lll1_opy_
        )
        PytestBDDFramework.bstack1l11lll11l1_opy_(instance, bstack1l1l1111lll_opy_)
        TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, []).clear()
    @staticmethod
    def bstack1l11ll1l11l_opy_(instance: bstack1lll11ll111_opy_, bstack1l1l1111lll_opy_: str):
        bstack1l11ll11111_opy_ = (
            PytestBDDFramework.bstack1l11ll11ll1_opy_
            if bstack1l1l1111lll_opy_ == PytestBDDFramework.bstack1l11ll1lll1_opy_
            else PytestBDDFramework.bstack1l1l11l1111_opy_
        )
        bstack1l11l1llll1_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack1l1l1111lll_opy_, None)
        bstack1l1l1l11111_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack1l11ll11111_opy_, None) if bstack1l11l1llll1_opy_ else None
        return (
            bstack1l1l1l11111_opy_[bstack1l11l1llll1_opy_][-1]
            if isinstance(bstack1l1l1l11111_opy_, dict) and len(bstack1l1l1l11111_opy_.get(bstack1l11l1llll1_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11lll11l1_opy_(instance: bstack1lll11ll111_opy_, bstack1l1l1111lll_opy_: str):
        hook = PytestBDDFramework.bstack1l11ll1l11l_opy_(instance, bstack1l1l1111lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll111l_opy_, []).clear()
    @staticmethod
    def __1l1l11ll11l_opy_(instance: bstack1lll11ll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᎌ"), None)):
            return
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᎍ"), bstack1l1l1l1_opy_ (u"ࠣ࠳ࠥᎎ")) != bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦᎏ"):
            PytestBDDFramework.logger.warning(bstack1l1l1l1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧ᎐"))
            return
        bstack1l11lll1l11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥ᎑"): (PytestBDDFramework.bstack1l1l11l1lll_opy_, PytestBDDFramework.bstack1l1l11l1111_opy_),
            bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢ᎒"): (PytestBDDFramework.bstack1l11ll1lll1_opy_, PytestBDDFramework.bstack1l11ll11ll1_opy_),
        }
        for when in (bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧ᎓"), bstack1l1l1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࠧ᎔"), bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ᎕")):
            bstack1l1l111ll11_opy_ = args[1].get_records(when)
            if not bstack1l1l111ll11_opy_:
                continue
            records = [
                bstack1lll11lll11_opy_(
                    kind=TestFramework.bstack1ll11l1llll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1l1l1_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧ᎖")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1l1l1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦ᎗")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1l111ll11_opy_
                if isinstance(getattr(r, bstack1l1l1l1_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ᎘"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l1l111lll1_opy_, bstack1l11ll11111_opy_ = bstack1l11lll1l11_opy_.get(when, (None, None))
            bstack1l1l11l1l1l_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack1l1l111lll1_opy_, None) if bstack1l1l111lll1_opy_ else None
            bstack1l1l1l11111_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack1l11ll11111_opy_, None) if bstack1l1l11l1l1l_opy_ else None
            if isinstance(bstack1l1l1l11111_opy_, dict) and len(bstack1l1l1l11111_opy_.get(bstack1l1l11l1l1l_opy_, [])) > 0:
                hook = bstack1l1l1l11111_opy_[bstack1l1l11l1l1l_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11lll111l_opy_ in hook:
                    hook[TestFramework.bstack1l11lll111l_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l1l111l1l1_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11llll1ll_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l1l11ll1ll_opy_(request.node, scenario)
        bstack1l1l1l111l1_opy_ = feature.filename
        if not bstack11llll1ll_opy_ or not test_name or not bstack1l1l1l111l1_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1ll1l1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1111l_opy_: bstack11llll1ll_opy_,
            TestFramework.bstack1lll111l11l_opy_: test_name,
            TestFramework.bstack1l1llllllll_opy_: bstack11llll1ll_opy_,
            TestFramework.bstack1l11ll111l1_opy_: bstack1l1l1l111l1_opy_,
            TestFramework.bstack1l11ll11lll_opy_: PytestBDDFramework.__1l1l1l1111l_opy_(feature, scenario),
            TestFramework.bstack1l1l11ll111_opy_: code,
            TestFramework.bstack1l1ll1lllll_opy_: TestFramework.bstack1l11llll1ll_opy_,
            TestFramework.bstack1l1l1ll1l1l_opy_: test_name
        }
    @staticmethod
    def __1l1l11ll1ll_opy_(node, scenario):
        if hasattr(node, bstack1l1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧ᎙")):
            parts = node.nodeid.rsplit(bstack1l1l1l1_opy_ (u"ࠨ࡛ࠣ᎚"))
            params = parts[-1]
            return bstack1l1l1l1_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢ᎛").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l1l1l1111l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1l1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭᎜")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1l1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ᎝")) else [])
    @staticmethod
    def __1l11l1lll1l_opy_(location):
        return bstack1l1l1l1_opy_ (u"ࠥ࠾࠿ࠨ᎞").join(filter(lambda x: isinstance(x, str), location))