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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import (
    bstack1111l1l11l_opy_,
    bstack1111l1111l_opy_,
    bstack11111ll1l1_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1llll1l1l11_opy_ import bstack1lllllll1ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11lll11l11_opy_
from bstack_utils.helper import bstack1ll1111ll11_opy_
import threading
import os
import urllib.parse
class bstack1llll11lll1_opy_(bstack1lll11ll1l1_opy_):
    def __init__(self, bstack1lllll11111_opy_):
        super().__init__()
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l111ll_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1llll1lll_opy_)
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l111ll_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1lll1l1ll_opy_)
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack11111lll1l_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1lll1l111_opy_)
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l1l1l1_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1lllll11l_opy_)
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.bstack1111l111ll_opy_, bstack1111l1111l_opy_.PRE), self.bstack1l1lllll111_opy_)
        bstack1lllllll1ll_opy_.bstack1lll1111l11_opy_((bstack1111l1l11l_opy_.QUIT, bstack1111l1111l_opy_.PRE), self.on_close)
        self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll1lll_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        bstack1l1llll111l_opy_: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨᇨ"):
            return
        if not bstack1ll1111ll11_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇩ"))
            return
        def wrapped(bstack1l1llll111l_opy_, launch, *args, **kwargs):
            response = self.bstack1l1lll1lll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᇪ"): True}).encode(bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᇫ")))
            if response is not None and response.capabilities:
                if not bstack1ll1111ll11_opy_():
                    browser = launch(bstack1l1llll111l_opy_)
                    return browser
                bstack1l1llll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᇬ")))
                if not bstack1l1llll11l1_opy_: # empty caps bstack1l1lll1llll_opy_ bstack1l1lll1ll11_opy_ bstack1l1lll11lll_opy_ bstack1lllll1l1l1_opy_ or error in processing
                    return
                bstack1l1llll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1llll11l1_opy_))
                f.bstack1111lll1l1_opy_(instance, bstack1lllllll1ll_opy_.bstack1l1lll1l11l_opy_, bstack1l1llll1l11_opy_)
                f.bstack1111lll1l1_opy_(instance, bstack1lllllll1ll_opy_.bstack1l1llll11ll_opy_, bstack1l1llll11l1_opy_)
                browser = bstack1l1llll111l_opy_.connect(bstack1l1llll1l11_opy_)
                return browser
        return wrapped
    def bstack1l1lll1l111_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨᇭ"):
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇮ"))
            return
        if not bstack1ll1111ll11_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1l1l1_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ᇯ"), {}).get(bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩᇰ")):
                    bstack1l1lll1l1l1_opy_ = args[0][bstack1l1l1l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᇱ")][bstack1l1l1l1_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦᇲ")]
                    session_id = bstack1l1lll1l1l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨᇳ"))
                    f.bstack1111lll1l1_opy_(instance, bstack1lllllll1ll_opy_.bstack1l1llll1l1l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢᇴ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1lllll111_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        bstack1l1llll111l_opy_: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨᇵ"):
            return
        if not bstack1ll1111ll11_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇶ"))
            return
        def wrapped(bstack1l1llll111l_opy_, connect, *args, **kwargs):
            response = self.bstack1l1lll1lll1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᇷ"): True}).encode(bstack1l1l1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᇸ")))
            if response is not None and response.capabilities:
                bstack1l1llll11l1_opy_ = json.loads(response.capabilities.decode(bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᇹ")))
                if not bstack1l1llll11l1_opy_:
                    return
                bstack1l1llll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1llll11l1_opy_))
                if bstack1l1llll11l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᇺ")):
                    browser = bstack1l1llll111l_opy_.bstack1l1llll1111_opy_(bstack1l1llll1l11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1llll1l11_opy_
                    return connect(bstack1l1llll111l_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1lll1l1ll_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        bstack1ll1l111l11_opy_: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᇻ"):
            return
        if not bstack1ll1111ll11_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦᇼ"))
            return
        def wrapped(bstack1ll1l111l11_opy_, bstack1l1lll1ll1l_opy_, *args, **kwargs):
            contexts = bstack1ll1l111l11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1l1l1l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᇽ") in page.url:
                                    return page
                    else:
                        return bstack1l1lll1ll1l_opy_(bstack1ll1l111l11_opy_)
        return wrapped
    def bstack1l1lll1lll1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᇾ") + str(req) + bstack1l1l1l1_opy_ (u"ࠣࠤᇿ"))
        try:
            r = self.bstack1llll111l11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧሀ") + str(r.success) + bstack1l1l1l1_opy_ (u"ࠥࠦሁ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤሂ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨሃ"))
            traceback.print_exc()
            raise e
    def bstack1l1lllll11l_opy_(
        self,
        f: bstack1lllllll1ll_opy_,
        Connection: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤሄ"):
            return
        if not bstack1ll1111ll11_opy_():
            return
        def wrapped(Connection, bstack1l1llll1ll1_opy_, *args, **kwargs):
            return bstack1l1llll1ll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1lllllll1ll_opy_,
        bstack1l1llll111l_opy_: object,
        exec: Tuple[bstack11111ll1l1_opy_, str],
        bstack1111l1llll_opy_: Tuple[bstack1111l1l11l_opy_, bstack1111l1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l1l1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨህ"):
            return
        if not bstack1ll1111ll11_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦሆ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped