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
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack11111ll1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
class bstack1lll1l1l111_opy_(bstack1lll11ll1l1_opy_):
    bstack1l1ll11lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥቜ")
    bstack1l1ll11l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧቝ")
    bstack1l1ll1111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧ቞")
    def __init__(self, bstack1llllll1111_opy_):
        super().__init__()
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l111ll_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1l1llllll_opy_)
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.bstack1ll1l1l111l_opy_)
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.POST), self.bstack1l1ll11111l_opy_)
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.POST), self.bstack1l1ll1l111l_opy_)
        bstack1111111l1l_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.QUIT, bstack1111l1111l_opy_.POST), self.bstack1l1ll11llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣ቟"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1ll111ll1_opy_(instance, f, kwargs)
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡩ࠲ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨበ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠣࠤቡ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1111l111l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll11lll1_opy_, False):
            return
        if not f.bstack1111lll1ll_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_):
            return
        platform_index = f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_)
        if f.bstack1ll1ll111ll_opy_(method_name, *args) and len(args) > 1:
            bstack11ll11ll11_opy_ = datetime.now()
            hub_url = bstack1111111l1l_opy_.hub_url(driver)
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦቢ") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠥࠦባ"))
            bstack1l1l1lll1ll_opy_ = args[1][bstack1l1l1l1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥቤ")] if isinstance(args[1], dict) and bstack1l1l1l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦብ") in args[1] else None
            bstack1l1ll1l11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦቦ")
            if isinstance(bstack1l1l1lll1ll_opy_, dict):
                bstack11ll11ll11_opy_ = datetime.now()
                r = self.bstack1l1ll11l11l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧቧ"), datetime.now() - bstack11ll11ll11_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥቨ") + str(r) + bstack1l1l1l1_opy_ (u"ࠤࠥቩ"))
                        return
                    if r.hub_url:
                        f.bstack1l1ll111lll_opy_(instance, driver, r.hub_url)
                        f.bstack1111lll1l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll11lll1_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤቪ"), e)
    def bstack1l1ll11111l_opy_(
        self,
        f: bstack1111111l1l_opy_,
        driver: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1111111l1l_opy_.session_id(driver)
            if session_id:
                bstack1l1ll111l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨቫ").format(session_id)
                bstack1lll1l1ll11_opy_.mark(bstack1l1ll111l1l_opy_)
    def bstack1l1ll1l111l_opy_(
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
        if f.bstack1111l111l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll11l1l1_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1111111l1l_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤቬ") + str(hub_url) + bstack1l1l1l1_opy_ (u"ࠨࠢቭ"))
            return
        framework_session_id = bstack1111111l1l_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥቮ") + str(framework_session_id) + bstack1l1l1l1_opy_ (u"ࠣࠤቯ"))
            return
        if bstack1111111l1l_opy_.bstack1l1l1llll11_opy_(*args) == bstack1111111l1l_opy_.bstack1l1ll1l1l11_opy_:
            bstack1l1ll111l11_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤተ").format(framework_session_id)
            bstack1l1ll111l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧቱ").format(framework_session_id)
            bstack1lll1l1ll11_opy_.end(
                label=bstack1l1l1l1_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢቲ"),
                start=bstack1l1ll111l1l_opy_,
                end=bstack1l1ll111l11_opy_,
                status=True,
                failure=None
            )
            bstack11ll11ll11_opy_ = datetime.now()
            r = self.bstack1l1l1llll1l_opy_(
                ref,
                f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦታ"), datetime.now() - bstack11ll11ll11_opy_)
            f.bstack1111lll1l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll11l1l1_opy_, r.success)
    def bstack1l1ll11llll_opy_(
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
        if f.bstack1111l111l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll1111l1_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1111111l1l_opy_.session_id(driver)
        hub_url = bstack1111111l1l_opy_.hub_url(driver)
        bstack11ll11ll11_opy_ = datetime.now()
        r = self.bstack1l1ll1l11ll_opy_(
            ref,
            f.bstack1111l111l1_opy_(instance, bstack1111111l1l_opy_.bstack1ll1lll1ll1_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦቴ"), datetime.now() - bstack11ll11ll11_opy_)
        f.bstack1111lll1l1_opy_(instance, bstack1lll1l1l111_opy_.bstack1l1ll1111l1_opy_, r.success)
    @measure(event_name=EVENTS.bstack11ll1ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1l1lll1lll1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧት") + str(req) + bstack1l1l1l1_opy_ (u"ࠣࠤቶ"))
        try:
            r = self.bstack1llll111l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧቷ") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠥࠦቸ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቹ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨቺ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1l1ll11l11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣቻ") + str(req) + bstack1l1l1l1_opy_ (u"ࠢࠣቼ"))
        try:
            r = self.bstack1llll111l11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦች") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠤࠥቾ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቿ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧኀ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11l111_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1l1l1llll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣኁ") + str(req) + bstack1l1l1l1_opy_ (u"ࠨࠢኂ"))
        try:
            r = self.bstack1llll111l11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤኃ") + str(r) + bstack1l1l1l1_opy_ (u"ࠣࠤኄ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢኅ") + str(e) + bstack1l1l1l1_opy_ (u"ࠥࠦኆ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1ll11ll1l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1l1ll1l11ll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1lll111l1l1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨኇ") + str(req) + bstack1l1l1l1_opy_ (u"ࠧࠨኈ"))
        try:
            r = self.bstack1llll111l11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ኉") + str(r) + bstack1l1l1l1_opy_ (u"ࠢࠣኊ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨኋ") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥኌ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11ll1111l1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack1l1ll111ll1_opy_(self, instance: bstack11111ll1l1_opy_, f: bstack1111111l1l_opy_, kwargs):
        bstack1l1ll11l1ll_opy_ = version.parse(f.framework_version)
        bstack1l1l1lll1l1_opy_ = kwargs.get(bstack1l1l1l1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦኍ"))
        bstack1l1l1lllll1_opy_ = kwargs.get(bstack1l1l1l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦ኎"))
        bstack1l1llll11l1_opy_ = {}
        bstack1l1ll1l1111_opy_ = {}
        bstack1l1ll111111_opy_ = None
        bstack1l1l1lll11l_opy_ = {}
        if bstack1l1l1lllll1_opy_ is not None or bstack1l1l1lll1l1_opy_ is not None: # check top level caps
            if bstack1l1l1lllll1_opy_ is not None:
                bstack1l1l1lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ኏")] = bstack1l1l1lllll1_opy_
            if bstack1l1l1lll1l1_opy_ is not None and callable(getattr(bstack1l1l1lll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣነ"))):
                bstack1l1l1lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪኑ")] = bstack1l1l1lll1l1_opy_.to_capabilities()
        response = self.bstack1l1lll1lll1_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l1lll11l_opy_).encode(bstack1l1l1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኒ")))
        if response is not None and response.capabilities:
            bstack1l1llll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣና")))
            if not bstack1l1llll11l1_opy_: # empty caps bstack1l1lll1llll_opy_ bstack1l1lll1ll11_opy_ bstack1l1lll11lll_opy_ bstack1lllll1l1l1_opy_ or error in processing
                return
            bstack1l1ll111111_opy_ = f.bstack1lllll1l111_opy_[bstack1l1l1l1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢኔ")](bstack1l1llll11l1_opy_)
        if bstack1l1l1lll1l1_opy_ is not None and bstack1l1ll11l1ll_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪን")):
            bstack1l1ll1l1111_opy_ = None
        if (
                not bstack1l1l1lll1l1_opy_ and not bstack1l1l1lllll1_opy_
        ) or (
                bstack1l1ll11l1ll_opy_ < version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫኖ"))
        ):
            bstack1l1ll1l1111_opy_ = {}
            bstack1l1ll1l1111_opy_.update(bstack1l1llll11l1_opy_)
        self.logger.info(bstack11lll11l11_opy_)
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤኗ")).lower().__eq__(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧኘ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦኙ"): f.bstack1l1ll1111ll_opy_,
                }
            )
        if bstack1l1ll11l1ll_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩኚ")):
            if bstack1l1l1lllll1_opy_ is not None:
                del kwargs[bstack1l1l1l1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥኛ")]
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧኜ"): bstack1l1ll111111_opy_,
                    bstack1l1l1l1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤኝ"): True,
                    bstack1l1l1l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨኞ"): None,
                }
            )
        elif bstack1l1ll11l1ll_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ኟ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣአ"): bstack1l1ll1l1111_opy_,
                    bstack1l1l1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥኡ"): bstack1l1ll111111_opy_,
                    bstack1l1l1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢኢ"): True,
                    bstack1l1l1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦኣ"): None,
                }
            )
        elif bstack1l1ll11l1ll_opy_ >= version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬኤ")):
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨእ"): bstack1l1ll1l1111_opy_,
                    bstack1l1l1l1_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦኦ"): True,
                    bstack1l1l1l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣኧ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1l1l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤከ"): bstack1l1ll1l1111_opy_,
                    bstack1l1l1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢኩ"): True,
                    bstack1l1l1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦኪ"): None,
                }
            )