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
from bstack_utils.bstack11l11ll1ll_opy_ import bstack1l11l1lll1_opy_
class bstack111111llll_opy_(TestFramework):
    bstack1l11lll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ᎟")
    bstack1l1l11l1111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᎠ")
    bstack1l11ll11ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᎡ")
    bstack1l1l11l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᎢ")
    bstack1l11ll1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᎣ")
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
        bstack1ll1ll1l11l_opy_: List[str]=[bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᎤ")],
    ):
        super().__init__(bstack1ll1ll1l11l_opy_, bstack1l1l1111l1l_opy_)
        self.bstack1l11lll1l1l_opy_ = any(bstack1l1l1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᎥ") in item.lower() for item in bstack1ll1ll1l11l_opy_)
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
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᎦ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠧࠨᎧ"))
            return
        if not self.bstack1l11lll1l1l_opy_:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᎨ") + str(str(self.bstack1ll1ll1l11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠢࠣᎩ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᎪ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥᎫ"))
            return
        instance = self.__1l1l1111ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᎬ") + str(args) + bstack1l1l1l1_opy_ (u"ࠦࠧᎭ"))
            return
        try:
            if instance!= None and test_framework_state in bstack111111llll_opy_.bstack1l11lllll11_opy_ and test_hook_state == bstack1llll1llll1_opy_.PRE:
                bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1ll111l1l1_opy_.value)
                name = str(EVENTS.bstack1ll111l1l1_opy_.name)+bstack1l1l1l1_opy_ (u"ࠧࡀࠢᎮ")+str(test_framework_state.name)
                TestFramework.bstack1l11ll11l11_opy_(instance, name, bstack1lll11111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᎯ").format(e))
        try:
            if not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1l11ll1111l_opy_) and test_hook_state == bstack1llll1llll1_opy_.PRE:
                test = bstack111111llll_opy_.__1l1l111l1l1_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎰ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠣࠤᎱ"))
            if test_framework_state == bstack1lll1l1lll1_opy_.TEST:
                if test_hook_state == bstack1llll1llll1_opy_.PRE and not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_):
                    TestFramework.bstack1111lll1l1_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎲ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠥࠦᎳ"))
                elif test_hook_state == bstack1llll1llll1_opy_.POST and not TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll1111llll_opy_):
                    TestFramework.bstack1111lll1l1_opy_(instance, TestFramework.bstack1ll1111llll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᎴ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠧࠨᎵ"))
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG and test_hook_state == bstack1llll1llll1_opy_.POST:
                bstack111111llll_opy_.__1l1l11ll11l_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT and test_hook_state == bstack1llll1llll1_opy_.POST:
                self.__1l1l11ll1l1_opy_(instance, *args)
            elif test_framework_state in bstack111111llll_opy_.bstack1l11lllll11_opy_:
                self.__1l1l11l111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᎶ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠢࠣᎷ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l1l11lllll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack111111llll_opy_.bstack1l11lllll11_opy_ and test_hook_state == bstack1llll1llll1_opy_.POST:
                name = str(EVENTS.bstack1ll111l1l1_opy_.name)+bstack1l1l1l1_opy_ (u"ࠣ࠼ࠥᎸ")+str(test_framework_state.name)
                bstack1lll11111ll_opy_ = TestFramework.bstack1l1l111ll1l_opy_(instance, name)
                bstack1lll1l1ll11_opy_.end(EVENTS.bstack1ll111l1l1_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᎹ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᎺ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᎻ").format(e))
    def bstack1ll11lll111_opy_(self):
        return self.bstack1l11lll1l1l_opy_
    def __1l1l11111ll_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᎼ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll1111l11l_opy_(rep, [bstack1l1l1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᎽ"), bstack1l1l1l1_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᎾ"), bstack1l1l1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᎿ"), bstack1l1l1l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᏀ"), bstack1l1l1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᏁ"), bstack1l1l1l1_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᏂ")])
        return None
    def __1l1l11ll1l1_opy_(self, instance: bstack1lll11ll111_opy_, *args):
        result = self.__1l1l11111ll_opy_(*args)
        if not result:
            return
        failure = None
        bstack111l11l1ll_opy_ = None
        if result.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᏃ"), None) == bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᏄ") and len(args) > 1 and getattr(args[1], bstack1l1l1l1_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᏅ"), None) is not None:
            failure = [{bstack1l1l1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᏆ"): [args[1].excinfo.exconly(), result.get(bstack1l1l1l1_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᏇ"), None)]}]
            bstack111l11l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᏈ") if bstack1l1l1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᏉ") in getattr(args[1].excinfo, bstack1l1l1l1_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᏊ"), bstack1l1l1l1_opy_ (u"ࠨࠢᏋ")) else bstack1l1l1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᏌ")
        bstack1l1l111l111_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᏍ"), TestFramework.bstack1l11llll1ll_opy_)
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
            target = None # bstack1l11ll1ll1l_opy_ bstack1l11lllllll_opy_ this to be bstack1l1l1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᏎ")
            if test_framework_state == bstack1lll1l1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1l11l1ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᏏ"), None), bstack1l1l1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᏐ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1l1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᏑ"), None):
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
        bstack1l11llllll1_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack111111llll_opy_.bstack1l1l11l1111_opy_, {})
        if not key in bstack1l11llllll1_opy_:
            bstack1l11llllll1_opy_[key] = []
        bstack1l1l1111l11_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack111111llll_opy_.bstack1l11ll11ll1_opy_, {})
        if not key in bstack1l1l1111l11_opy_:
            bstack1l1l1111l11_opy_[key] = []
        bstack1l1l1111111_opy_ = {
            bstack111111llll_opy_.bstack1l1l11l1111_opy_: bstack1l11llllll1_opy_,
            bstack111111llll_opy_.bstack1l11ll11ll1_opy_: bstack1l1l1111l11_opy_,
        }
        if test_hook_state == bstack1llll1llll1_opy_.PRE:
            hook = {
                bstack1l1l1l1_opy_ (u"ࠨ࡫ࡦࡻࠥᏒ"): key,
                TestFramework.bstack1l11ll1ll11_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1lllll_opy_: TestFramework.bstack1l1l11l1l11_opy_,
                TestFramework.bstack1l11lll1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11lll111l_opy_: [],
                TestFramework.bstack1l1l11lll11_opy_: args[1] if len(args) > 1 else bstack1l1l1l1_opy_ (u"ࠧࠨᏓ")
            }
            bstack1l11llllll1_opy_[key].append(hook)
            bstack1l1l1111111_opy_[bstack111111llll_opy_.bstack1l1l11l1lll_opy_] = key
        elif test_hook_state == bstack1llll1llll1_opy_.POST:
            bstack1l11ll1l1l1_opy_ = bstack1l11llllll1_opy_.get(key, [])
            hook = bstack1l11ll1l1l1_opy_.pop() if bstack1l11ll1l1l1_opy_ else None
            if hook:
                result = self.__1l1l11111ll_opy_(*args)
                if result:
                    bstack1l11ll11l1l_opy_ = result.get(bstack1l1l1l1_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᏔ"), TestFramework.bstack1l1l11l1l11_opy_)
                    if bstack1l11ll11l1l_opy_ != TestFramework.bstack1l1l11l1l11_opy_:
                        hook[TestFramework.bstack1l11l1lllll_opy_] = bstack1l11ll11l1l_opy_
                hook[TestFramework.bstack1l1l11llll1_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1l1111l11_opy_[key].append(hook)
                bstack1l1l1111111_opy_[bstack111111llll_opy_.bstack1l11ll1lll1_opy_] = key
        TestFramework.bstack1l1l11l11ll_opy_(instance, bstack1l1l1111111_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᏕ") + str(bstack1l1l1111l11_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠦᏖ"))
    def __1l1l111llll_opy_(
        self,
        context: bstack1l11llll111_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll1llll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll1111l11l_opy_(args[0], [bstack1l1l1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᏗ"), bstack1l1l1l1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᏘ"), bstack1l1l1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᏙ"), bstack1l1l1l1_opy_ (u"ࠢࡪࡦࡶࠦᏚ"), bstack1l1l1l1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᏛ"), bstack1l1l1l1_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᏜ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᏝ")) else fixturedef.get(bstack1l1l1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᏞ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1l1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᏟ")) else None
        node = request.node if hasattr(request, bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᏠ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᏡ")) else None
        baseid = fixturedef.get(bstack1l1l1l1_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᏢ"), None) or bstack1l1l1l1_opy_ (u"ࠤࠥᏣ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1l1l1_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᏤ")):
            target = bstack111111llll_opy_.__1l11l1lll1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1l1l1_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᏥ")) else None
            if target and not TestFramework.bstack1111ll1ll1_opy_(target):
                self.__1l1l11l1ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᏦ") + str(test_hook_state) + bstack1l1l1l1_opy_ (u"ࠨࠢᏧ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᏨ") + str(target) + bstack1l1l1l1_opy_ (u"ࠣࠤᏩ"))
            return None
        instance = TestFramework.bstack1111ll1ll1_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᏪ") + str(target) + bstack1l1l1l1_opy_ (u"ࠥࠦᏫ"))
            return None
        bstack1l1l1l111ll_opy_ = TestFramework.bstack1111l111l1_opy_(instance, bstack111111llll_opy_.bstack1l11lll1lll_opy_, {})
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᏬ"), bstack1l1l1l1_opy_ (u"ࠧ࠷ࠢᏭ")) == bstack1l1l1l1_opy_ (u"ࠨ࠱ࠣᏮ"):
            bstack1l11lll1111_opy_ = bstack1l1l1l1_opy_ (u"ࠢ࠻ࠤᏯ").join((scope, fixturename))
            bstack1l1l111111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11ll1l1ll_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠣ࡭ࡨࡽࠧᏰ"): bstack1l11lll1111_opy_,
                bstack1l1l1l1_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᏱ"): bstack111111llll_opy_.__1l1l1l1111l_opy_(request.node),
                bstack1l1l1l1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᏲ"): fixturedef,
                bstack1l1l1l1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᏳ"): scope,
                bstack1l1l1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥᏴ"): None,
            }
            try:
                if test_hook_state == bstack1llll1llll1_opy_.POST and callable(getattr(args[-1], bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᏵ"), None)):
                    bstack1l11ll1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠢࡵࡻࡳࡩࠧ᏶")] = TestFramework.bstack1ll111lll1l_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll1llll1_opy_.PRE:
                bstack1l11ll1l1ll_opy_[bstack1l1l1l1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ᏷")] = uuid4().__str__()
                bstack1l11ll1l1ll_opy_[bstack111111llll_opy_.bstack1l11lll1ll1_opy_] = bstack1l1l111111l_opy_
            elif test_hook_state == bstack1llll1llll1_opy_.POST:
                bstack1l11ll1l1ll_opy_[bstack111111llll_opy_.bstack1l1l11llll1_opy_] = bstack1l1l111111l_opy_
            if bstack1l11lll1111_opy_ in bstack1l1l1l111ll_opy_:
                bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_].update(bstack1l11ll1l1ll_opy_)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᏸ") + str(bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_]) + bstack1l1l1l1_opy_ (u"ࠥࠦᏹ"))
            else:
                bstack1l1l1l111ll_opy_[bstack1l11lll1111_opy_] = bstack1l11ll1l1ll_opy_
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᏺ") + str(len(bstack1l1l1l111ll_opy_)) + bstack1l1l1l1_opy_ (u"ࠧࠨᏻ"))
        TestFramework.bstack1111lll1l1_opy_(instance, bstack111111llll_opy_.bstack1l11lll1lll_opy_, bstack1l1l1l111ll_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᏼ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠢࠣᏽ"))
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
            bstack111111llll_opy_.bstack1l11lll1lll_opy_: {},
            bstack111111llll_opy_.bstack1l11ll11ll1_opy_: {},
            bstack111111llll_opy_.bstack1l1l11l1111_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1111lll1l1_opy_(ob, TestFramework.bstack1l11lll11ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1111lll1l1_opy_(ob, TestFramework.bstack1ll1lll1ll1_opy_, context.platform_index)
        TestFramework.bstack11111l1ll1_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣ᏾") + str(TestFramework.bstack11111l1ll1_opy_.keys()) + bstack1l1l1l1_opy_ (u"ࠤࠥ᏿"))
        return ob
    def bstack1ll11lll1l1_opy_(self, instance: bstack1lll11ll111_opy_, bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_]):
        bstack1l1l1111lll_opy_ = (
            bstack111111llll_opy_.bstack1l1l11l1lll_opy_
            if bstack1111l1llll_opy_[1] == bstack1llll1llll1_opy_.PRE
            else bstack111111llll_opy_.bstack1l11ll1lll1_opy_
        )
        hook = bstack111111llll_opy_.bstack1l11ll1l11l_opy_(instance, bstack1l1l1111lll_opy_)
        entries = hook.get(TestFramework.bstack1l11lll111l_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, []))
        return entries
    def bstack1ll11llll11_opy_(self, instance: bstack1lll11ll111_opy_, bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_]):
        bstack1l1l1111lll_opy_ = (
            bstack111111llll_opy_.bstack1l1l11l1lll_opy_
            if bstack1111l1llll_opy_[1] == bstack1llll1llll1_opy_.PRE
            else bstack111111llll_opy_.bstack1l11ll1lll1_opy_
        )
        bstack111111llll_opy_.bstack1l11lll11l1_opy_(instance, bstack1l1l1111lll_opy_)
        TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, []).clear()
    @staticmethod
    def bstack1l11ll1l11l_opy_(instance: bstack1lll11ll111_opy_, bstack1l1l1111lll_opy_: str):
        bstack1l11ll11111_opy_ = (
            bstack111111llll_opy_.bstack1l11ll11ll1_opy_
            if bstack1l1l1111lll_opy_ == bstack111111llll_opy_.bstack1l11ll1lll1_opy_
            else bstack111111llll_opy_.bstack1l1l11l1111_opy_
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
        hook = bstack111111llll_opy_.bstack1l11ll1l11l_opy_(instance, bstack1l1l1111lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11lll111l_opy_, []).clear()
    @staticmethod
    def __1l1l11ll11l_opy_(instance: bstack1lll11ll111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1l1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣ᐀"), None)):
            return
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᐁ"), bstack1l1l1l1_opy_ (u"ࠧ࠷ࠢᐂ")) != bstack1l1l1l1_opy_ (u"ࠨ࠱ࠣᐃ"):
            bstack111111llll_opy_.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᐄ"))
            return
        bstack1l11lll1l11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᐅ"): (bstack111111llll_opy_.bstack1l1l11l1lll_opy_, bstack111111llll_opy_.bstack1l1l11l1111_opy_),
            bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᐆ"): (bstack111111llll_opy_.bstack1l11ll1lll1_opy_, bstack111111llll_opy_.bstack1l11ll11ll1_opy_),
        }
        for when in (bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᐇ"), bstack1l1l1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᐈ"), bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᐉ")):
            bstack1l1l111ll11_opy_ = args[1].get_records(when)
            if not bstack1l1l111ll11_opy_:
                continue
            records = [
                bstack1lll11lll11_opy_(
                    kind=TestFramework.bstack1ll11l1llll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1l1l1_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᐊ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1l1l1_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᐋ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l1l111ll11_opy_
                if isinstance(getattr(r, bstack1l1l1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᐌ"), None), str) and r.message.strip()
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
    def __1l1l111l1l1_opy_(test) -> Dict[str, Any]:
        bstack11llll1ll_opy_ = bstack111111llll_opy_.__1l11l1lll1l_opy_(test.location) if hasattr(test, bstack1l1l1l1_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᐍ")) else getattr(test, bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᐎ"), None)
        test_name = test.name if hasattr(test, bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐏ")) else None
        bstack1l1l1l111l1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1l1l1_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᐐ")) and test.fspath else None
        if not bstack11llll1ll_opy_ or not test_name or not bstack1l1l1l111l1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1l1l1_opy_ (u"ࠨ࡯ࡣ࡬ࠥᐑ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l11l1lll11_opy_ = []
        try:
            bstack1l11l1lll11_opy_ = bstack1l11l1lll1_opy_.bstack11l1111ll1_opy_(test)
        except:
            bstack111111llll_opy_.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᐒ"))
        return {
            TestFramework.bstack1ll1ll1l1ll_opy_: uuid4().__str__(),
            TestFramework.bstack1l11ll1111l_opy_: bstack11llll1ll_opy_,
            TestFramework.bstack1lll111l11l_opy_: test_name,
            TestFramework.bstack1l1llllllll_opy_: getattr(test, bstack1l1l1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᐓ"), None),
            TestFramework.bstack1l11ll111l1_opy_: bstack1l1l1l111l1_opy_,
            TestFramework.bstack1l11ll11lll_opy_: bstack111111llll_opy_.__1l1l1l1111l_opy_(test),
            TestFramework.bstack1l1l11ll111_opy_: code,
            TestFramework.bstack1l1ll1lllll_opy_: TestFramework.bstack1l11llll1ll_opy_,
            TestFramework.bstack1l1l1ll1l1l_opy_: bstack11llll1ll_opy_,
            TestFramework.bstack1l11l1ll1ll_opy_: bstack1l11l1lll11_opy_
        }
    @staticmethod
    def __1l1l1l1111l_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack1l1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᐔ"), None) for f in test.own_markers if getattr(f, bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᐕ"), None)]
            if isinstance(getattr(test, bstack1l1l1l1_opy_ (u"ࠦࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠤᐖ"), None), list)
            else []
        )
    @staticmethod
    def __1l11l1lll1l_opy_(location):
        return bstack1l1l1l1_opy_ (u"ࠧࡀ࠺ࠣᐗ").join(filter(lambda x: isinstance(x, str), location))