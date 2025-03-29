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
from datetime import datetime, timezone
import os
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack11111ll1l1_opy_, bstack1111l1l11l_opy_, bstack1111l1111l_opy_
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lllll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11ll111_opy_, bstack1llll1llll1_opy_, bstack1lll11lll11_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll1111ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll11ll111l_opy_ = [bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᅬ"), bstack1l1l1l1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᅭ"), bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᅮ"), bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧᅯ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡵࡪࠥᅰ")]
bstack1ll11l111ll_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦᅱ"): bstack1ll11ll111l_opy_,
    bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣᅲ"): bstack1ll11ll111l_opy_,
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣᅳ"): bstack1ll11ll111l_opy_,
    bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣᅴ"): bstack1ll11ll111l_opy_,
    bstack1l1l1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧᅵ"): bstack1ll11ll111l_opy_
    + [
        bstack1l1l1l1_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥᅶ"),
        bstack1l1l1l1_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢᅷ"),
        bstack1l1l1l1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦᅸ"),
        bstack1l1l1l1_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᅹ"),
        bstack1l1l1l1_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥᅺ"),
        bstack1l1l1l1_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥᅻ"),
        bstack1l1l1l1_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤᅼ"),
        bstack1l1l1l1_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᅽ"),
        bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢᅾ"),
        bstack1l1l1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᅿ"),
    ],
    bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨᆀ"): [bstack1l1l1l1_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦᆁ"), bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢᆂ"), bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦᆃ"), bstack1l1l1l1_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥᆄ")],
    bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧᆅ"): [bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥᆆ"), bstack1l1l1l1_opy_ (u"ࠢࡢࡴࡪࡷࠧᆇ")],
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢᆈ"): [bstack1l1l1l1_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᆉ"), bstack1l1l1l1_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᆊ"), bstack1l1l1l1_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤᆋ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧᆌ"), bstack1l1l1l1_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᆍ"), bstack1l1l1l1_opy_ (u"ࠢࡪࡦࡶࠦᆎ")],
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢᆏ"): [bstack1l1l1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᆐ"), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤᆑ"), bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤᆒ")],
    bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢᆓ"): [bstack1l1l1l1_opy_ (u"ࠨࡷࡩࡧࡱࠦᆔ"), bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢᆕ")],
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤᆖ"): [bstack1l1l1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᆗ"), bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᆘ")],
    bstack1l1l1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦᆙ"): [bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆚ"), bstack1l1l1l1_opy_ (u"ࠨࡡࡳࡩࡶࠦᆛ"), bstack1l1l1l1_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢᆜ")],
}
class bstack1lll1l1ll1l_opy_(bstack1lll11ll1l1_opy_):
    bstack1ll11l11111_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣᆝ")
    bstack1ll1111ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡌࡒࡋࡕࠢᆞ")
    bstack1ll11l111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤᆟ")
    bstack1ll1l111111_opy_: Callable
    bstack1ll11ll1l1l_opy_: Callable
    def __init__(self, bstack111111111l_opy_, bstack1lllll11111_opy_):
        super().__init__()
        self.bstack1ll1llll11l_opy_ = bstack1lllll11111_opy_
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣᆠ"), bstack1l1l1l1_opy_ (u"ࠧ࠷ࠢᆡ")) != bstack1l1l1l1_opy_ (u"ࠨ࠱ࠣᆢ") or not self.is_enabled():
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࠣᆣ") + str(self.__class__.__name__) + bstack1l1l1l1_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦᆤ"))
            return
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.PRE), self.bstack1ll1ll11l11_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST), self.bstack1ll1ll11111_opy_)
        for event in bstack1lll1l1lll1_opy_:
            for state in bstack1llll1llll1_opy_:
                TestFramework.bstack1lll1111l11_opy_((event, state), self.bstack1ll111l1l11_opy_)
        bstack111111111l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.POST), self.bstack1ll11ll1l11_opy_)
        self.bstack1ll1l111111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll11l1l1ll_opy_(bstack1lll1l1ll1l_opy_.bstack1ll1111ll1l_opy_, self.bstack1ll1l111111_opy_)
        self.bstack1ll11ll1l1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll11l1l1ll_opy_(bstack1lll1l1ll1l_opy_.bstack1ll11l111l1_opy_, self.bstack1ll11ll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1ll11lll111_opy_() and instance:
            bstack1ll11l1l111_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1111l1llll_opy_
            if test_framework_state == bstack1lll1l1lll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                bstack11ll11ll11_opy_ = datetime.now()
                entries = f.bstack1ll11lll1l1_opy_(instance, bstack1111l1llll_opy_)
                if entries:
                    self.bstack1ll111l1ll1_opy_(instance, entries)
                    instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤᆥ"), datetime.now() - bstack11ll11ll11_opy_)
                    f.bstack1ll11llll11_opy_(instance, bstack1111l1llll_opy_)
                instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᆦ"), datetime.now() - bstack1ll11l1l111_opy_)
                return # bstack1ll11l1ll11_opy_ not send this event with the bstack1ll11lllll1_opy_ bstack1ll11l1111l_opy_
            elif (
                test_framework_state == bstack1lll1l1lll1_opy_.TEST
                and test_hook_state == bstack1llll1llll1_opy_.POST
                and not f.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
            ):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤᆧ") + str(TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠧࠨᆨ"))
                f.bstack1111lll1l1_opy_(instance, bstack1lll1l1ll1l_opy_.bstack1ll11l11111_opy_, True)
                return # bstack1ll11l1ll11_opy_ not send this event bstack1ll111l11l1_opy_ bstack1ll11ll11l1_opy_
            elif (
                f.bstack1111l111l1_opy_(instance, bstack1lll1l1ll1l_opy_.bstack1ll11l11111_opy_, False)
                and test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT
                and test_hook_state == bstack1llll1llll1_opy_.POST
                and f.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
            ):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧᆩ") + str(TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠢࠣᆪ"))
                self.bstack1ll111l1l11_opy_(f, instance, (bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST), *args, **kwargs)
            bstack11ll11ll11_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll11111lll_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1l1l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᆫ"), None), data.pop(bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᆬ"), {}).values()),
                key=lambda x: x[bstack1l1l1l1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᆭ")],
            )
            if bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_ in data:
                data.pop(bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_)
            data.update({bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᆮ"): bstack1ll11111lll_opy_})
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᆯ"), datetime.now() - bstack11ll11ll11_opy_)
            bstack11ll11ll11_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll111l1lll_opy_)
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᆰ"), datetime.now() - bstack11ll11ll11_opy_)
            self.bstack1ll11l1111l_opy_(instance, bstack1111l1llll_opy_, event_json=event_json)
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᆱ"), datetime.now() - bstack1ll11l1l111_opy_)
    def bstack1ll1ll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
        bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1l111lllll_opy_.value)
        self.bstack1ll1llll11l_opy_.bstack1ll111l1111_opy_(instance, f, bstack1111l1llll_opy_, *args, **kwargs)
        bstack1lll1l1ll11_opy_.end(EVENTS.bstack1l111lllll_opy_.value, bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᆲ"), bstack1lll11111ll_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᆳ"), status=True, failure=None, test_name=None)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1llll11l_opy_.bstack1ll111ll111_opy_(instance, f, bstack1111l1llll_opy_, *args, **kwargs)
        self.bstack1ll111ll1ll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1ll11lll1ll_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1ll111ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨᆴ"))
            return
        bstack11ll11ll11_opy_ = datetime.now()
        try:
            r = self.bstack1llll111l11_opy_.TestSessionEvent(req)
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧᆵ"), datetime.now() - bstack11ll11ll11_opy_)
            f.bstack1111lll1l1_opy_(instance, self.bstack1ll1llll11l_opy_.bstack1ll111l11ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆶ") + str(r) + bstack1l1l1l1_opy_ (u"ࠨࠢᆷ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆸ") + str(e) + bstack1l1l1l1_opy_ (u"ࠣࠤᆹ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1l11_opy_(
        self,
        f: bstack1111111l1l_opy_,
        _driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        _1ll1111l1l1_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1111111l1l_opy_.bstack1ll1ll1l1l1_opy_(method_name):
            return
        if f.bstack1ll1lll1lll_opy_(*args) != bstack1111111l1l_opy_.bstack1ll111ll11l_opy_:
            return
        bstack1ll11l1l111_opy_ = datetime.now()
        screenshot = result.get(bstack1l1l1l1_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᆺ"), None) if isinstance(result, dict) else None
        if not isinstance(screenshot, str) or len(screenshot) <= 0:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦᆻ"))
            return
        bstack1ll11l1l1l1_opy_ = self.bstack1ll11l1ll1l_opy_(instance)
        if bstack1ll11l1l1l1_opy_:
            entry = bstack1lll11lll11_opy_(TestFramework.bstack1ll11llll1l_opy_, screenshot)
            self.bstack1ll111l1ll1_opy_(bstack1ll11l1l1l1_opy_, [entry])
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧᆼ"), datetime.now() - bstack1ll11l1l111_opy_)
        else:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠢᆽ") + str(instance.ref()) + bstack1l1l1l1_opy_ (u"ࠨࠢᆾ"))
    @measure(event_name=EVENTS.bstack1ll111llll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1ll111l1ll1_opy_(
        self,
        bstack1ll11l1l1l1_opy_: bstack1lll11ll111_opy_,
        entries: List[bstack1lll11lll11_opy_],
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l111l1_opy_(bstack1ll11l1l1l1_opy_, TestFramework.bstack1ll1lll1ll1_opy_)
        req.execution_context.hash = str(bstack1ll11l1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll11l1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll11l1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111l111l1_opy_(bstack1ll11l1l1l1_opy_, TestFramework.bstack1ll1llll1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111l111l1_opy_(bstack1ll11l1l1l1_opy_, TestFramework.bstack1ll11l1lll1_opy_)
            log_entry.uuid = TestFramework.bstack1111l111l1_opy_(bstack1ll11l1l1l1_opy_, TestFramework.bstack1ll1ll1l1ll_opy_)
            log_entry.test_framework_state = bstack1ll11l1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᆿ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
        def bstack1ll1111l1ll_opy_():
            bstack11ll11ll11_opy_ = datetime.now()
            try:
                self.bstack1llll111l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1ll11llll1l_opy_:
                    bstack1ll11l1l1l1_opy_.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᇀ"), datetime.now() - bstack11ll11ll11_opy_)
                else:
                    bstack1ll11l1l1l1_opy_.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨᇁ"), datetime.now() - bstack11ll11ll11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇂ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111l111l11_opy_.enqueue(bstack1ll1111l1ll_opy_)
    @measure(event_name=EVENTS.bstack1ll111lllll_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1ll11l1111l_opy_(
        self,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        event_json=None,
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1lll1ll1_opy_)
        req.test_framework_name = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)
        req.test_framework_version = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
        req.test_framework_state = bstack1111l1llll_opy_[0].name
        req.test_hook_state = bstack1111l1llll_opy_[1].name
        started_at = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1111llll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll111l1lll_opy_)).encode(bstack1l1l1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᇃ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll1111l1ll_opy_():
            bstack11ll11ll11_opy_ = datetime.now()
            try:
                self.bstack1llll111l11_opy_.TestFrameworkEvent(req)
                instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᇄ"), datetime.now() - bstack11ll11ll11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇅ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111l111l11_opy_.enqueue(bstack1ll1111l1ll_opy_)
    def bstack1ll111ll1l1_opy_(self, event_url: str, bstack111ll1l1l1_opy_: dict) -> bool:
        return True # always return True so that old bstack1ll111l1l1l_opy_ bstack1ll111l111l_opy_'t bstack1ll11ll1ll1_opy_
    def bstack1ll11l1ll1l_opy_(self, instance: bstack11111ll1l1_opy_):
        bstack1ll11ll1lll_opy_ = TestFramework.bstack11111lllll_opy_(instance.context)
        for t in bstack1ll11ll1lll_opy_:
            bstack1ll11l11l11_opy_ = TestFramework.bstack1111l111l1_opy_(t, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
            if any(instance is d[1] for d in bstack1ll11l11l11_opy_):
                return t
    def bstack1ll1111lll1_opy_(self, message):
        self.bstack1ll1l111111_opy_(message + bstack1l1l1l1_opy_ (u"ࠢ࡝ࡰࠥᇆ"))
    def log_error(self, message):
        self.bstack1ll11ll1l1l_opy_(message + bstack1l1l1l1_opy_ (u"ࠣ࡞ࡱࠦᇇ"))
    def bstack1ll11l1l1ll_opy_(self, level, original_func):
        def bstack1ll1111l111_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll11ll1lll_opy_ = TestFramework.bstack1ll111lll11_opy_()
            if not bstack1ll11ll1lll_opy_:
                return return_value
            bstack1ll11l1l1l1_opy_ = next(
                (
                    instance
                    for instance in bstack1ll11ll1lll_opy_
                    if TestFramework.bstack1111lll1ll_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
                ),
                None,
            )
            if not bstack1ll11l1l1l1_opy_:
                return
            entry = bstack1lll11lll11_opy_(TestFramework.bstack1ll11l1llll_opy_, message, level)
            self.bstack1ll111l1ll1_opy_(bstack1ll11l1l1l1_opy_, [entry])
            return return_value
        return bstack1ll1111l111_opy_
class bstack1ll111l1lll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1ll11l11l1l_opy_ = set()
        kwargs[bstack1l1l1l1_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦᇈ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll11l11lll_opy_(obj, self.bstack1ll11l11l1l_opy_)
def bstack1ll11llllll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll11l11lll_opy_(obj, bstack1ll11l11l1l_opy_=None, max_depth=3):
    if bstack1ll11l11l1l_opy_ is None:
        bstack1ll11l11l1l_opy_ = set()
    if id(obj) in bstack1ll11l11l1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1ll11l11l1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1ll11ll11ll_opy_ = TestFramework.bstack1ll111lll1l_opy_(obj)
    bstack1ll11l1l11l_opy_ = next((k.lower() in bstack1ll11ll11ll_opy_.lower() for k in bstack1ll11l111ll_opy_.keys()), None)
    if bstack1ll11l1l11l_opy_:
        obj = TestFramework.bstack1ll1111l11l_opy_(obj, bstack1ll11l111ll_opy_[bstack1ll11l1l11l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1l1l1_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᇉ")):
            keys = getattr(obj, bstack1l1l1l1_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢᇊ"), [])
        elif hasattr(obj, bstack1l1l1l1_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᇋ")):
            keys = getattr(obj, bstack1l1l1l1_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᇌ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1l1l1_opy_ (u"ࠢࡠࠤᇍ"))}
        if not obj and bstack1ll11ll11ll_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧᇎ"):
            obj = {bstack1l1l1l1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᇏ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll11llllll_opy_(key) or str(key).startswith(bstack1l1l1l1_opy_ (u"ࠥࡣࠧᇐ")):
            continue
        if value is not None and bstack1ll11llllll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll11l11lll_opy_(value, bstack1ll11l11l1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll11l11lll_opy_(o, bstack1ll11l11l1l_opy_, max_depth) for o in value]))
    return result or None