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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack1111l11l1l_opy_,
    bstack11111ll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_, bstack1lll11ll111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lllll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l11_opy_ import bstack1lllllll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
import grpc
import traceback
import json
class bstack1llll1l1lll_opy_(bstack1lll11ll1l1_opy_):
    bstack1ll1l1ll1l1_opy_ = False
    bstack1ll1ll1ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧႵ")
    bstack1ll1ll11ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥ࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦႶ")
    bstack1ll1lllll11_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡲ࡮ࡺࠢႷ")
    bstack1lll111ll11_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡸࡥࡳࡤࡣࡱࡲ࡮ࡴࡧࠣႸ")
    bstack1ll1ll11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣ࡭ࡧࡳࡠࡷࡵࡰࠧႹ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack111111111l_opy_, bstack1lllll11111_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1llll11l_opy_ = bstack1lllll11111_opy_
        bstack111111111l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.bstack1lll111111l_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.PRE), self.bstack1ll1ll11l11_opy_)
        TestFramework.bstack1lll1111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1ll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1llll111_opy_(instance, args)
        test_framework = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1llll1ll_opy_)
        if bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩႺ") in instance.bstack1ll1ll1l11l_opy_:
            platform_index = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1lll1ll1_opy_)
            self.accessibility = self.bstack1l111l111l_opy_(tags) and self.bstack11ll11ll1l_opy_(self.config[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႻ")][platform_index])
        else:
            capabilities = self.bstack1ll1llll11l_opy_.bstack1ll1llllll1_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢႼ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠣࠤႽ"))
                return
            self.accessibility = self.bstack1l111l111l_opy_(tags) and self.bstack11ll11ll1l_opy_(capabilities)
        if self.bstack1ll1llll11l_opy_.pages and self.bstack1ll1llll11l_opy_.pages.values():
            bstack1ll1lll11l1_opy_ = list(self.bstack1ll1llll11l_opy_.pages.values())
            if bstack1ll1lll11l1_opy_ and isinstance(bstack1ll1lll11l1_opy_[0], (list, tuple)) and bstack1ll1lll11l1_opy_[0]:
                bstack1ll1lll111l_opy_ = bstack1ll1lll11l1_opy_[0][0]
                if callable(bstack1ll1lll111l_opy_):
                    page = bstack1ll1lll111l_opy_()
                    def bstack1l11l1llll_opy_():
                        self.get_accessibility_results(page, bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨႾ"))
                    def bstack1ll1llll1l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1l1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢႿ"))
                    setattr(page, bstack1l1l1l1_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹࡹࠢჀ"), bstack1l11l1llll_opy_)
                    setattr(page, bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢჁ"), bstack1ll1llll1l1_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡩࡱࡸࡰࡩࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡺࡦࡲࡵࡦ࠿ࠥჂ") + str(self.accessibility) + bstack1l1l1l1_opy_ (u"ࠢࠣჃ"))
    def bstack1lll111111l_opy_(
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
            bstack11ll11ll11_opy_ = datetime.now()
            self.bstack1ll1ll1111l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦჄ"), datetime.now() - bstack11ll11ll11_opy_)
            if (
                not f.bstack1ll1ll1l1l1_opy_(method_name)
                or f.bstack1ll1l1lllll_opy_(method_name, *args)
                or f.bstack1lll111l111_opy_(method_name, *args)
            ):
                return
            if not f.bstack1111l111l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1ll1lllll11_opy_, False):
                if not bstack1llll1l1lll_opy_.bstack1ll1l1ll1l1_opy_:
                    self.logger.warning(bstack1l1l1l1_opy_ (u"ࠤ࡞ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧჅ") + str(f.platform_index) + bstack1l1l1l1_opy_ (u"ࠥࡡࠥࡧ࠱࠲ࡻࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢ࡫ࡥࡻ࡫ࠠ࡯ࡱࡷࠤࡧ࡫ࡥ࡯ࠢࡶࡩࡹࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠤ჆"))
                    bstack1llll1l1lll_opy_.bstack1ll1l1ll1l1_opy_ = True
                return
            bstack1ll1lll1111_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1lll1111_opy_:
                platform_index = f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤჇ") + str(f.framework_name) + bstack1l1l1l1_opy_ (u"ࠧࠨ჈"))
                return
            bstack1ll1ll1ll11_opy_ = f.bstack1ll1lll1lll_opy_(*args)
            if not bstack1ll1ll1ll11_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࠣ჉") + str(method_name) + bstack1l1l1l1_opy_ (u"ࠢࠣ჊"))
                return
            bstack1ll1ll111l1_opy_ = f.bstack1111l111l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1ll1ll11lll_opy_, False)
            if bstack1ll1ll1ll11_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࠧ჋") and not bstack1ll1ll111l1_opy_:
                f.bstack1111lll1l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1ll1ll11lll_opy_, True)
            if not bstack1ll1ll111l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡱࡳ࡛ࠥࡒࡍࠢ࡯ࡳࡦࡪࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣ჌") + str(bstack1ll1ll1ll11_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠦჍ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1ll1ll11_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤ჎") + str(bstack1ll1ll1ll11_opy_) + bstack1l1l1l1_opy_ (u"ࠧࠨ჏"))
                return
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡹࡣࡳ࡫ࡳࡸࡸࡥࡴࡰࡡࡵࡹࡳ࠯ࡽࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣა") + str(bstack1ll1ll1ll11_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣბ"))
            scripts = [(s, bstack1ll1lll1111_opy_[s]) for s in scripts_to_run if s in bstack1ll1lll1111_opy_]
            for bstack1ll1l1ll11l_opy_, bstack1lll1111lll_opy_ in scripts:
                try:
                    bstack11ll11ll11_opy_ = datetime.now()
                    if bstack1ll1l1ll11l_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡥࡳࠨგ"):
                        result = self.perform_scan(driver, method=bstack1ll1ll1ll11_opy_, framework_name=f.framework_name)
                    instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࠣდ") + bstack1ll1l1ll11l_opy_, datetime.now() - bstack11ll11ll11_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1l1l1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦე"), True):
                        self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡸࡱࡩࡱࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡸࡥ࡮ࡣ࡬ࡲ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࠦვ") + str(result) + bstack1l1l1l1_opy_ (u"ࠧࠨზ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴ࠾ࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽࠡࡧࡵࡶࡴࡸ࠽ࠣთ") + str(e) + bstack1l1l1l1_opy_ (u"ࠢࠣი"))
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡫ࡲࡳࡱࡵࡁࠧკ") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥლ"))
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll111_opy_,
        bstack1111l1llll_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_],
        *args,
        **kwargs,
    ):
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢმ"))
            return
        driver = self.bstack1ll1llll11l_opy_.bstack1ll1ll1l111_opy_(f, instance, bstack1111l1llll_opy_, *args, **kwargs)
        test_name = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1lll111l11l_opy_)
        if not test_name:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤნ"))
            return
        test_uuid = f.bstack1111l111l1_opy_(instance, TestFramework.bstack1ll1ll1l1ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥო"))
            return
        if isinstance(self.bstack1ll1llll11l_opy_, bstack1lll1lllll1_opy_):
            framework_name = bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪპ")
        else:
            framework_name = bstack1l1l1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩჟ")
        self.bstack1l1l111lll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1lll1l11ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤრ"))
            return
        bstack11ll11ll11_opy_ = datetime.now()
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠤࡶࡧࡦࡴࠢს"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥტ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠦࠥࠨუ"))
            return
        instance = bstack1111l11l1l_opy_.bstack1111ll1ll1_opy_(driver)
        if instance:
            if not bstack1111l11l1l_opy_.bstack1111l111l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1lll111ll11_opy_, False):
                bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1lll111ll11_opy_, True)
            else:
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤფ") + str(method) + bstack1l1l1l1_opy_ (u"ࠨࠢქ"))
                return
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧღ") + str(method) + bstack1l1l1l1_opy_ (u"ࠣࠤყ"))
        if framework_name == bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭შ"):
            result = self.bstack1ll1llll11l_opy_.bstack1lll1111ll1_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_, {bstack1l1l1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥჩ"): method if method else bstack1l1l1l1_opy_ (u"ࠦࠧც")})
        bstack1lll1l1ll11_opy_.end(EVENTS.bstack1lll1l11ll_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧძ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦწ"), True, None, command=method)
        if instance:
            bstack1111l11l1l_opy_.bstack1111lll1l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1lll111ll11_opy_, False)
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱࠦჭ"), datetime.now() - bstack11ll11ll11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll1ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥხ"))
            return
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨჯ"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤჰ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠦࠧჱ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll11ll11_opy_ = datetime.now()
        if framework_name == bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩჲ"):
            result = self.bstack1ll1llll11l_opy_.bstack1lll1111ll1_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_)
        instance = bstack1111l11l1l_opy_.bstack1111ll1ll1_opy_(driver)
        if instance:
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࠤჳ"), datetime.now() - bstack11ll11ll11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1llllllll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥჴ"))
            return
        bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧჵ"), None)
        if not bstack1lll1111lll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣჶ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠥࠦჷ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll11ll11_opy_ = datetime.now()
        if framework_name == bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨჸ"):
            result = self.bstack1ll1llll11l_opy_.bstack1lll1111ll1_opy_(driver, bstack1lll1111lll_opy_)
        else:
            result = driver.execute_async_script(bstack1lll1111lll_opy_)
        instance = bstack1111l11l1l_opy_.bstack1111ll1ll1_opy_(driver)
        if instance:
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤჹ"), datetime.now() - bstack11ll11ll11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1ll1llll_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1lll1111l1l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llll111l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣჺ") + str(r) + bstack1l1l1l1_opy_ (u"ࠢࠣ჻"))
            else:
                self.bstack1lll1111111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨჼ") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥჽ"))
            traceback.print_exc()
            raise e
    def bstack1lll1111111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡰࡴࡧࡤࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥჾ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1lll11111l1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1ll1ll1l_opy_ and command.module == self.bstack1ll1ll11ll1_opy_:
                        if command.method and not command.method in bstack1lll11111l1_opy_:
                            bstack1lll11111l1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1lll11111l1_opy_[command.method]:
                            bstack1lll11111l1_opy_[command.method][command.name] = list()
                        bstack1lll11111l1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1lll11111l1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1ll1111l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1llll11l_opy_, bstack1lll1lllll1_opy_) and method_name != bstack1l1l1l1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬჿ"):
            return
        if bstack1111l11l1l_opy_.bstack1111lll1ll_opy_(instance, bstack1llll1l1lll_opy_.bstack1ll1lllll11_opy_):
            return
        if not f.bstack1ll1l1llll1_opy_(instance):
            if not bstack1llll1l1lll_opy_.bstack1ll1l1ll1l1_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡧ࠱࠲ࡻࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠ࡯ࡱࡱ࠱ࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࠤᄀ"))
                bstack1llll1l1lll_opy_.bstack1ll1l1ll1l1_opy_ = True
            return
        if f.bstack1ll1ll111ll_opy_(method_name, *args):
            bstack1ll1ll1lll1_opy_ = False
            desired_capabilities = f.bstack1ll1lllllll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1lll111l1ll_opy_(instance)
                platform_index = f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0)
                bstack1ll1ll11l1l_opy_ = datetime.now()
                r = self.bstack1lll1111l1l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᄁ"), datetime.now() - bstack1ll1ll11l1l_opy_)
                bstack1ll1ll1lll1_opy_ = r.success
            else:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤᄂ") + str(desired_capabilities) + bstack1l1l1l1_opy_ (u"ࠣࠤᄃ"))
            f.bstack1111lll1l1_opy_(instance, bstack1llll1l1lll_opy_.bstack1ll1lllll11_opy_, bstack1ll1ll1lll1_opy_)
    def bstack1l111l111l_opy_(self, test_tags):
        bstack1lll1111l1l_opy_ = self.config.get(bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᄄ"))
        if not bstack1lll1111l1l_opy_:
            return True
        try:
            include_tags = bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᄅ")] if bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᄆ") in bstack1lll1111l1l_opy_ and isinstance(bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᄇ")], list) else []
            exclude_tags = bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᄈ")] if bstack1l1l1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᄉ") in bstack1lll1111l1l_opy_ and isinstance(bstack1lll1111l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᄊ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᄋ") + str(error))
        return False
    def bstack11ll11ll1l_opy_(self, caps):
        try:
            bstack1ll1l1ll1ll_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᄌ"), {}).get(bstack1l1l1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᄍ"), caps.get(bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᄎ"), bstack1l1l1l1_opy_ (u"࠭ࠧᄏ")))
            if bstack1ll1l1ll1ll_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᄐ"))
                return False
            browser = caps.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᄑ"), bstack1l1l1l1_opy_ (u"ࠩࠪᄒ")).lower()
            if browser != bstack1l1l1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᄓ"):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᄔ"))
                return False
            browser_version = caps.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᄕ"))
            if browser_version and browser_version != bstack1l1l1l1_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᄖ") and int(browser_version.split(bstack1l1l1l1_opy_ (u"ࠧ࠯ࠩᄗ"))[0]) <= 98:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠼࠳ࠨᄘ"))
                return False
            bstack1ll1l1lll11_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᄙ"), {}).get(bstack1l1l1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᄚ"))
            if bstack1ll1l1lll11_opy_ and bstack1l1l1l1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᄛ") in bstack1ll1l1lll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᄜ"), []):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᄝ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᄞ") + str(error))
            return False
    def bstack1l1l111lll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1lll11111ll_opy_ = None
        try:
            bstack1ll1l1lll1l_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᄟ"): test_uuid,
                bstack1l1l1l1_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᄠ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᄡ"), bstack1l1l1l1_opy_ (u"ࠫࠬᄢ")),
                bstack1l1l1l1_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩᄣ"): os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᄤ"), bstack1l1l1l1_opy_ (u"ࠧࠨᄥ"))
            }
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᄦ") + str(bstack1ll1l1lll1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            bstack1lll1111lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᄧ"), None)
            if not bstack1lll1111lll_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᄨ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠦࠥࠨᄩ"))
                return
            bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1ll1lll1l11_opy_(EVENTS.bstack1ll1lllll1l_opy_.value)
            self.bstack1ll1lll1l1l_opy_(driver, bstack1lll1111lll_opy_, bstack1ll1l1lll1l_opy_, framework_name)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᄪ"))
            bstack1lll1l1ll11_opy_.end(EVENTS.bstack1ll1lllll1l_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᄫ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᄬ"), True, None, command=bstack1l1l1l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᄭ"),test_name=name)
        except Exception as bstack1ll1lll11ll_opy_:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᄮ") + bstack1l1l1l1_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᄯ") + bstack1l1l1l1_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᄰ") + str(bstack1ll1lll11ll_opy_))
            bstack1lll1l1ll11_opy_.end(EVENTS.bstack1ll1lllll1l_opy_.value, bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᄱ"), bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᄲ"), False, bstack1ll1lll11ll_opy_, command=bstack1l1l1l1_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᄳ"),test_name=name)
    def bstack1ll1lll1l1l_opy_(self, driver, bstack1lll1111lll_opy_, bstack1ll1l1lll1l_opy_, framework_name):
        if framework_name == bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᄴ"):
            self.bstack1ll1llll11l_opy_.bstack1lll1111ll1_opy_(driver, bstack1lll1111lll_opy_, bstack1ll1l1lll1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1lll1111lll_opy_, bstack1ll1l1lll1l_opy_))
    def _1ll1llll111_opy_(self, instance: bstack1lll11ll111_opy_, args: Tuple) -> list:
        bstack1l1l1l1_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᄵ")
        if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᄶ") in instance.bstack1ll1ll1l11l_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1l1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᄷ")) else []
        if hasattr(args[0], bstack1l1l1l1_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪᄸ")):
            return [marker.name for marker in args[0].own_markers]
        return []