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
    bstack11111ll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1llll11l1l1_opy_(bstack1lll11ll1l1_opy_):
    bstack1ll1l1ll1l1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.bstack1ll1l1l111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l1l111l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll1l11llll_opy_(hub_url):
            if not bstack1llll11l1l1_opy_.bstack1ll1l1ll1l1_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࠥࡹࡥ࡭ࡨ࠰࡬ࡪࡧ࡬ࠡࡨ࡯ࡳࡼࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡮ࡴࡦࡳࡣࠣࡷࡪࡹࡳࡪࡱࡱࡷࠥ࡮ࡵࡣࡡࡸࡶࡱࡃࠢᄹ") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠢࠣᄺ"))
                bstack1llll11l1l1_opy_.bstack1ll1l1ll1l1_opy_ = True
            return
        bstack1ll1ll1ll11_opy_ = f.bstack1ll1lll1lll_opy_(*args)
        bstack1ll1l1l1lll_opy_ = f.bstack1ll1l1l11ll_opy_(*args)
        if bstack1ll1ll1ll11_opy_ and bstack1ll1ll1ll11_opy_.lower() == bstack1l1l1l1_opy_ (u"ࠣࡨ࡬ࡲࡩ࡫࡬ࡦ࡯ࡨࡲࡹࠨᄻ") and bstack1ll1l1l1lll_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll1l1l1lll_opy_.get(bstack1l1l1l1_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᄼ"), None), bstack1ll1l1l1lll_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᄽ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦࢀࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠠࡰࡴࠣࡥࡷ࡭ࡳ࠯ࡷࡶ࡭ࡳ࡭࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡹࡥࡱࡻࡥ࠾ࠤᄾ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠧࠨᄿ"))
                return
            def bstack111l11111l_opy_(driver, bstack1ll1l1l11l1_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll1l1l11l1_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll1l1l1ll1_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࠤᅀ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠢࠣᅁ"))
                    else:
                        self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡱࡳ࠲ࡹࡣࡳ࡫ࡳࡸ࠿ࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࡂࢁ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡵࡻࡳࡩࢂࠦ࡬ࡰࡥࡤࡸࡴࡸ࡟ࡷࡣ࡯ࡹࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫ࡽࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࡀࠦᅂ") + str(response) + bstack1l1l1l1_opy_ (u"ࠤࠥᅃ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll1l1ll111_opy_(
                        driver, bstack1ll1l1l11l1_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack111l11111l_opy_.__name__ = bstack1ll1ll1ll11_opy_
            return bstack111l11111l_opy_
    def __1ll1l1ll111_opy_(
        self,
        driver,
        bstack1ll1l1l11l1_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll1l1l1ll1_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡺࡲࡪࡩࡪࡩࡷ࡫ࡤ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥᅄ") + str(locator_value) + bstack1l1l1l1_opy_ (u"ࠦࠧᅅ"))
                bstack1ll1l11lll1_opy_ = self.bstack1ll1l1l1l1l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣ࡬ࡪࡧ࡬ࡪࡰࡪࡣࡷ࡫ࡳࡶ࡮ࡷࡁࠧᅆ") + str(bstack1ll1l11lll1_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢᅇ"))
                if bstack1ll1l11lll1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1l1l1_opy_ (u"ࠢࡶࡵ࡬ࡲ࡬ࠨᅈ"): bstack1ll1l11lll1_opy_.locator_type,
                            bstack1l1l1l1_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᅉ"): bstack1ll1l11lll1_opy_.locator_value,
                        }
                    )
                    return bstack1ll1l1l11l1_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1l1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡌࡣࡉࡋࡂࡖࡉࠥᅊ"), False):
                    self.logger.info(bstack1llllllll1l_opy_ (u"ࠥࡪࡦ࡯࡬ࡶࡴࡨ࠱࡭࡫ࡡ࡭࡫ࡱ࡫࠲ࡸࡥࡴࡷ࡯ࡸ࠲ࡳࡩࡴࡵ࡬ࡲ࡬ࡀࠠࡴ࡮ࡨࡩࡵ࠮࠳࠱ࠫࠣࡰࡪࡺࡴࡪࡰࡪࠤࡾࡵࡵࠡ࡫ࡱࡷࡵ࡫ࡣࡵࠢࡷ࡬ࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡰࡴ࡭ࡳࠣᅋ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲ࡴ࡯࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡃࠢᅌ") + str(response) + bstack1l1l1l1_opy_ (u"ࠧࠨᅍ"))
        except Exception as err:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥᅎ") + str(err) + bstack1l1l1l1_opy_ (u"ࠢࠣᅏ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll1l1l1l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1ll1l1l1ll1_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1l1l1_opy_ (u"ࠣ࠲ࠥᅐ"),
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1l1l1_opy_ (u"ࠤࠥᅑ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll111l11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᅒ") + str(r) + bstack1l1l1l1_opy_ (u"ࠦࠧᅓ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᅔ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢᅕ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l1l1111_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1ll1l1l1l1l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1l1l1_opy_ (u"ࠢ࠱ࠤᅖ")):
        self.bstack1lll111l1l1_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll111l11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᅗ") + str(r) + bstack1l1l1l1_opy_ (u"ࠤࠥᅘ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᅙ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧᅚ"))
            traceback.print_exc()
            raise e