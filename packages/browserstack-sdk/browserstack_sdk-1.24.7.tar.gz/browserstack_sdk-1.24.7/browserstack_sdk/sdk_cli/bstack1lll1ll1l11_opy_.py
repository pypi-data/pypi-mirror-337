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
import json
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack1111l11l1l_opy_,
    bstack11111ll1l1_opy_,
    bstack1111lllll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_, bstack1lll11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l1l1_opy_ import bstack1ll1l11ll11_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll1111ll11_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lllll11ll1_opy_(bstack1ll1l11ll11_opy_):
    bstack1l1ll1ll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦካ")
    bstack1ll11ll1111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧኬ")
    bstack1l1lll11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤክ")
    bstack1l1ll1lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣኮ")
    bstack1l1ll1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨኯ")
    bstack1ll111l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤኰ")
    bstack1l1ll1llll1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢ኱")
    bstack1l1ll1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥኲ")
    def __init__(self):
        super().__init__(bstack1ll1l111l1l_opy_=self.bstack1l1ll1ll11l_opy_, frameworks=[bstack1111111l1l_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll1llll1_opy_.POST), self.bstack1l1l1ll1ll1_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.PRE), self.bstack1ll1ll11l11_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11l11l11_opy_ = self.bstack1l1l1ll11l1_opy_(instance.context)
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤኳ") + str(bstack1111l1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣኴ"))
        f.bstack1111lll1l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, bstack1ll11l11l11_opy_)
        bstack1l1l1ll11ll_opy_ = self.bstack1l1l1ll11l1_opy_(instance.context, bstack1l1l1ll1lll_opy_=False)
        f.bstack1111lll1l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1lll11l1l_opy_, bstack1l1l1ll11ll_opy_)
    def bstack1ll1ll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
        if not f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1llll1_opy_, False):
            self.__1l1l1l1lll1_opy_(f,instance,bstack1111l1llll_opy_)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
        if not f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1llll1_opy_, False):
            self.__1l1l1l1lll1_opy_(f, instance, bstack1111l1llll_opy_)
        if not f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1l1ll1_opy_, False):
            self.__1l1l1ll111l_opy_(f, instance, bstack1111l1llll_opy_)
    def bstack1l1l1ll1111_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1llll1_opy_(instance):
            return
        if f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1l1ll1_opy_, False):
            return
        driver.execute_script(
            bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨኵ").format(
                json.dumps(
                    {
                        bstack1l1l1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤ኶"): bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨ኷"),
                        bstack1l1l1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢኸ"): {bstack1l1l1l1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧኹ"): result},
                    }
                )
            )
        )
        f.bstack1111lll1l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1l1ll1_opy_, True)
    def bstack1l1l1ll11l1_opy_(self, context: bstack1111lllll1_opy_, bstack1l1l1ll1lll_opy_= True):
        if bstack1l1l1ll1lll_opy_:
            bstack1ll11l11l11_opy_ = self.bstack1ll1l1111ll_opy_(context, reverse=True)
        else:
            bstack1ll11l11l11_opy_ = self.bstack1ll1l11l1ll_opy_(context, reverse=True)
        return [f for f in bstack1ll11l11l11_opy_ if f[1].state != bstack1111l1l11l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1111l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1l1l1ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
    ):
        bstack1ll11l11l11_opy_ = f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤኺ") + str(bstack1111l1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣኻ"))
            return
        driver = bstack1ll11l11l11_opy_[0][0]()
        status = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1ll1lllll_opy_, None)
        if not status:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥኼ") + str(bstack1111l1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠤࠥኽ"))
            return
        bstack1l1lll1111l_opy_ = {bstack1l1l1l1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥኾ"): status.lower()}
        bstack1l1lll11ll1_opy_ = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_, None)
        if status.lower() == bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ኿") and bstack1l1lll11ll1_opy_ is not None:
            bstack1l1lll1111l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬዀ")] = bstack1l1lll11ll1_opy_[0][bstack1l1l1l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ዁")][0] if isinstance(bstack1l1lll11ll1_opy_, list) else str(bstack1l1lll11ll1_opy_)
        driver.execute_script(
            bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧዂ").format(
                json.dumps(
                    {
                        bstack1l1l1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣዃ"): bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧዄ"),
                        bstack1l1l1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨዅ"): bstack1l1lll1111l_opy_,
                    }
                )
            )
        )
        f.bstack1111lll1l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1l1ll1_opy_, True)
    @measure(event_name=EVENTS.bstack11l1ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_]
    ):
        test_name = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1l1l1ll1l1l_opy_, None)
        if not test_name:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥ዆"))
            return
        bstack1ll11l11l11_opy_ = f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢ዇") + str(bstack1111l1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢወ"))
            return
        for bstack1l1lllllll1_opy_, bstack1l1l1ll1l11_opy_ in bstack1ll11l11l11_opy_:
            if not bstack1111111l1l_opy_.bstack1ll1l1llll1_opy_(bstack1l1l1ll1l11_opy_):
                continue
            driver = bstack1l1lllllll1_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠧዉ").format(
                    json.dumps(
                        {
                            bstack1l1l1l1_opy_ (u"ࠣࡣࡦࡸ࡮ࡵ࡮ࠣዊ"): bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥዋ"),
                            bstack1l1l1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨዌ"): {bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤው"): test_name},
                        }
                    )
                )
            )
        f.bstack1111lll1l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1ll1llll1_opy_, True)
    def bstack1ll111l1111_opy_(
        self,
        instance: bstack1lll11ll111_opy_,
        f: TestFramework,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
        bstack1ll11l11l11_opy_ = [d for d, _ in f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])]
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧዎ"))
            return
        if not bstack1ll1111ll11_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦዏ"))
            return
        for bstack1l1l1l1llll_opy_ in bstack1ll11l11l11_opy_:
            driver = bstack1l1l1l1llll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1l1l1_opy_ (u"ࠢࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࡓࡺࡰࡦ࠾ࠧዐ") + str(timestamp)
            driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨዑ").format(
                    json.dumps(
                        {
                            bstack1l1l1l1_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤዒ"): bstack1l1l1l1_opy_ (u"ࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧዓ"),
                            bstack1l1l1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢዔ"): {
                                bstack1l1l1l1_opy_ (u"ࠧࡺࡹࡱࡧࠥዕ"): bstack1l1l1l1_opy_ (u"ࠨࡁ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠥዖ"),
                                bstack1l1l1l1_opy_ (u"ࠢࡥࡣࡷࡥࠧ዗"): data,
                                bstack1l1l1l1_opy_ (u"ࠣ࡮ࡨࡺࡪࡲࠢዘ"): bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡧࡻࡧࠣዙ")
                            }
                        }
                    )
                )
            )
    def bstack1ll111ll111_opy_(
        self,
        instance: bstack1lll11ll111_opy_,
        f: TestFramework,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
        bstack1ll11l11l11_opy_ = [d for _, d in f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])] + [d for _, d in f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1l1lll11l1l_opy_, [])]
        keys = [
            bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_,
            bstack1lllll11ll1_opy_.bstack1l1lll11l1l_opy_,
        ]
        bstack1ll11l11l11_opy_ = [
            d for key in keys for _, d in f.bstack1111l111l1_opy_(instance, key, [])
        ]
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧ࡮ࡺࠢࡶࡩࡸࡹࡩࡰࡰࡶࠤࡹࡵࠠ࡭࡫ࡱ࡯ࠧዚ"))
            return
        if f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll111l11ll_opy_, False):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡉࡂࡕࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡧࡷ࡫ࡡࡵࡧࡧࠦዛ"))
            return
        self.bstack1lll111l1l1_opy_()
        bstack11ll11ll11_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1lll1ll1_opy_)
        req.test_framework_name = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)
        req.test_framework_version = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
        req.test_framework_state = bstack1111l1llll_opy_[0].name
        req.test_hook_state = bstack1111l1llll_opy_[1].name
        req.test_uuid = TestFramework.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        for driver in bstack1ll11l11l11_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠦዜ")
                if bstack1111111l1l_opy_.bstack1111l111l1_opy_(driver, bstack1111111l1l_opy_.bstack1l1l1lll111_opy_, False)
                else bstack1l1l1l1_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠧዝ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1111111l1l_opy_.bstack1111l111l1_opy_(driver, bstack1111111l1l_opy_.bstack1l1lll1l11l_opy_, bstack1l1l1l1_opy_ (u"ࠢࠣዞ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1111111l1l_opy_.bstack1111l111l1_opy_(driver, bstack1111111l1l_opy_.bstack1l1llll1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠣࠤዟ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1llllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll11l11l11_opy_ = f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዠ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠥࠦዡ"))
            return {}
        if len(bstack1ll11l11l11_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዢ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠧࠨዣ"))
            return {}
        bstack1l1lllllll1_opy_, bstack1ll11111ll1_opy_ = bstack1ll11l11l11_opy_[0]
        driver = bstack1l1lllllll1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዤ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠢࠣዥ"))
            return {}
        capabilities = f.bstack1111l111l1_opy_(bstack1ll11111ll1_opy_, bstack1111111l1l_opy_.bstack1l1llll11ll_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዦ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥዧ"))
            return {}
        return capabilities.get(bstack1l1l1l1_opy_ (u"ࠥࡥࡱࡽࡡࡺࡵࡐࡥࡹࡩࡨࠣየ"), {})
    def bstack1ll1ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll11l11l11_opy_ = f.bstack1111l111l1_opy_(instance, bstack1lllll11ll1_opy_.bstack1ll11ll1111_opy_, [])
        if not bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዩ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠧࠨዪ"))
            return
        if len(bstack1ll11l11l11_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤያ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠢࠣዬ"))
        bstack1l1lllllll1_opy_, bstack1ll11111ll1_opy_ = bstack1ll11l11l11_opy_[0]
        driver = bstack1l1lllllll1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥይ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥዮ"))
            return
        return driver