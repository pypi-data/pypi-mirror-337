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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack111l111l11_opy_ import bstack111l11l111_opy_
from browserstack_sdk.sdk_cli.bstack111111lll1_opy_ import bstack1lll11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1llll1l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import bstack1llll11l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1llll11llll_opy_
from browserstack_sdk.sdk_cli.bstack111111ll1l_opy_ import bstack1lll1l1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l11_opy_ import bstack1lllll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l11_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11111l1_opy_ import bstack1l11111l1_opy_, bstack1l1l1111ll_opy_, bstack1ll1lll1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll11l1l1l_opy_ import bstack111111llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll111_opy_ import bstack1111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack1111l11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1l11_opy_ import bstack1lllllll1ll_opy_
from bstack_utils.helper import Notset, bstack11111111ll_opy_, get_cli_dir, bstack1llll111lll_opy_, bstack1l111l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from bstack_utils.helper import Notset, bstack11111111ll_opy_, get_cli_dir, bstack1llll111lll_opy_, bstack1l111l11l_opy_, bstack1111l1ll1_opy_, bstack11ll1llll_opy_, bstack1l11ll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11ll111_opy_, bstack1llll1llll1_opy_, bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1111l11l11_opy_ import bstack11111ll1l1_opy_, bstack1111l1l11l_opy_, bstack1111l1111l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1llllll_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1lll11l_opy_, bstack11111llll_opy_
logger = bstack1l1llllll_opy_.get_logger(__name__, bstack1l1llllll_opy_.bstack1llllll11l1_opy_())
def bstack1lll1l1llll_opy_(bs_config):
    bstack1lllll1l11l_opy_ = None
    bstack1lllll11l11_opy_ = None
    try:
        bstack1lllll11l11_opy_ = get_cli_dir()
        bstack1lllll1l11l_opy_ = bstack1llll111lll_opy_(bstack1lllll11l11_opy_)
        bstack111111l11l_opy_ = bstack11111111ll_opy_(bstack1lllll1l11l_opy_, bstack1lllll11l11_opy_, bs_config)
        bstack1lllll1l11l_opy_ = bstack111111l11l_opy_ if bstack111111l11l_opy_ else bstack1lllll1l11l_opy_
        if not bstack1lllll1l11l_opy_:
            raise ValueError(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤ࿡"))
    except Exception as ex:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡬ࡢࡶࡨࡷࡹࠦࡢࡪࡰࡤࡶࡾࠦࡻࡾࠤ࿢").format(ex))
        bstack1lllll1l11l_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥ࿣"))
        if bstack1lllll1l11l_opy_:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡳࡱࡰࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࠦ࿤") + str(bstack1lllll1l11l_opy_) + bstack1l1l1l1_opy_ (u"ࠤࠥ࿥"))
        else:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡒࡴࠦࡶࡢ࡮࡬ࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠼ࠢࡶࡩࡹࡻࡰࠡ࡯ࡤࡽࠥࡨࡥࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨ࿦"))
    return bstack1lllll1l11l_opy_, bstack1lllll11l11_opy_
bstack1llll1ll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࠾࠿࠹࠺ࠤ࿧")
bstack1lll1ll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡸࡥࡢࡦࡼࠦ࿨")
bstack1llll1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥ࿩")
bstack11111l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡍࡋࡖࡘࡊࡔ࡟ࡂࡆࡇࡖࠧ࿪")
bstack1lllll11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦ࿫")
bstack1lll1lll1ll_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡴࠥࠬࡄ࡯ࠩ࠯ࠬࠫࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡾࡅࡗ࠮࠴ࠪࠣ࿬"))
bstack1lllllllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡨࡪࡼࡥ࡭ࡱࡳࡱࡪࡴࡴࠣ࿭")
bstack1lllll1ll11_opy_ = [
    bstack1l1l1111ll_opy_.bstack1l11l1l1l_opy_,
    bstack1l1l1111ll_opy_.CONNECT,
    bstack1l1l1111ll_opy_.bstack111ll11ll_opy_,
]
class SDKCLI:
    _11111l111l_opy_ = None
    process: Union[None, Any]
    bstack1111111l11_opy_: bool
    bstack1lllll111l1_opy_: bool
    bstack1lllllll1l1_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lllll1111l_opy_: Union[None, grpc.Channel]
    bstack1lll1ll11ll_opy_: str
    test_framework: TestFramework
    bstack1111l11l11_opy_: bstack1111l11l1l_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1llll111l1l_opy_: bstack1lll1l1ll1l_opy_
    accessibility: bstack1llll1l1lll_opy_
    ai: bstack1llll11l1l1_opy_
    bstack1lll11ll11l_opy_: bstack1llll11llll_opy_
    bstack1lllllll111_opy_: List[bstack1lll11ll1l1_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1l111l1_opy_: Any
    bstack1lll11lll1l_opy_: Dict[str, timedelta]
    bstack1lllll11l1l_opy_: str
    bstack111l111l11_opy_: bstack111l11l111_opy_
    def __new__(cls):
        if not cls._11111l111l_opy_:
            cls._11111l111l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._11111l111l_opy_
    def __init__(self):
        self.process = None
        self.bstack1111111l11_opy_ = False
        self.bstack1lllll1111l_opy_ = None
        self.bstack1llll111l11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack11111l11ll_opy_, None)
        self.bstack1llll1lll1l_opy_ = os.environ.get(bstack1llll1ll111_opy_, bstack1l1l1l1_opy_ (u"ࠦࠧ࿮")) == bstack1l1l1l1_opy_ (u"ࠧࠨ࿯")
        self.bstack1lllll111l1_opy_ = False
        self.bstack1lllllll1l1_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1l111l1_opy_ = None
        self.test_framework = None
        self.bstack1111l11l11_opy_ = None
        self.bstack1lll1ll11ll_opy_=bstack1l1l1l1_opy_ (u"ࠨࠢ࿰")
        self.session_framework = None
        self.logger = bstack1l1llllll_opy_.get_logger(self.__class__.__name__, bstack1l1llllll_opy_.bstack1llllll11l1_opy_())
        self.bstack1lll11lll1l_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack111l111l11_opy_ = bstack111l11l111_opy_()
        self.bstack111111111l_opy_ = None
        self.bstack1lllll11111_opy_ = None
        self.bstack1llll111l1l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lllllll111_opy_ = []
    def bstack11lllll1_opy_(self):
        return os.environ.get(bstack1lllll11ll_opy_).lower().__eq__(bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ࿱"))
    def is_enabled(self, config):
        if bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ࿲") in config and str(config[bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭࿳")]).lower() != bstack1l1l1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ࿴"):
            return False
        bstack1lll1l1l1l1_opy_ = [bstack1l1l1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦ࿵"), bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤ࿶")]
        bstack1llllll111l_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤ࿷")) in bstack1lll1l1l1l1_opy_ or os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨ࿸")) in bstack1lll1l1l1l1_opy_
        os.environ[bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡊࡕࡢࡖ࡚ࡔࡎࡊࡐࡊࠦ࿹")] = str(bstack1llllll111l_opy_) # bstack1lll11l1ll1_opy_ bstack1lll1llllll_opy_ VAR to bstack1lll1l11111_opy_ is binary running
        return bstack1llllll111l_opy_
    def bstack1111l11l1_opy_(self):
        for event in bstack1lllll1ll11_opy_:
            bstack1l11111l1_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack1l11111l1_opy_.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠡ࠿ࡁࠤࢀࡧࡲࡨࡵࢀࠤࠧ࿺") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠥࠦ࿻"))
            )
        bstack1l11111l1_opy_.register(bstack1l1l1111ll_opy_.bstack1l11l1l1l_opy_, self.__1lllll1llll_opy_)
        bstack1l11111l1_opy_.register(bstack1l1l1111ll_opy_.CONNECT, self.__1lll1ll11l1_opy_)
        bstack1l11111l1_opy_.register(bstack1l1l1111ll_opy_.bstack111ll11ll_opy_, self.__1lll1l111ll_opy_)
        bstack1l11111l1_opy_.register(bstack1l1l1111ll_opy_.bstack1l11l11lll_opy_, self.__1llll1ll1l1_opy_)
    def bstack1lll11l1l1_opy_(self):
        return not self.bstack1llll1lll1l_opy_ and os.environ.get(bstack1llll1ll111_opy_, bstack1l1l1l1_opy_ (u"ࠦࠧ࿼")) != bstack1l1l1l1_opy_ (u"ࠧࠨ࿽")
    def is_running(self):
        if self.bstack1llll1lll1l_opy_:
            return self.bstack1111111l11_opy_
        else:
            return bool(self.bstack1lllll1111l_opy_)
    def bstack1llll1ll11l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lllllll111_opy_) and cli.is_running()
    def __1lllllll11l_opy_(self, bstack1lll11l1lll_opy_=10):
        if self.bstack1llll111l11_opy_:
            return
        bstack11ll11ll11_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack11111l11ll_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࠣ࿾") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠢ࡞ࠢࡦࡳࡳࡴࡥࡤࡶ࡬ࡲ࡬ࠨ࿿"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l1l1l1_opy_ (u"ࠣࡩࡵࡴࡨ࠴ࡥ࡯ࡣࡥࡰࡪࡥࡨࡵࡶࡳࡣࡵࡸ࡯ࡹࡻࠥက"), 0), (bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡸࡥࡰࡳࡱࡻࡽࠧခ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll11l1lll_opy_)
        self.bstack1lllll1111l_opy_ = channel
        self.bstack1llll111l11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lllll1111l_opy_)
        self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡥࡲࡲࡳ࡫ࡣࡵࠤဂ"), datetime.now() - bstack11ll11ll11_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack11111l11ll_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷࡩࡩࡀࠠࡪࡵࡢࡧ࡭࡯࡬ࡥࡡࡳࡶࡴࡩࡥࡴࡵࡀࠦဃ") + str(self.bstack1lll11l1l1_opy_()) + bstack1l1l1l1_opy_ (u"ࠧࠨင"))
    def __1lll1l111ll_opy_(self, event_name):
        if self.bstack1lll11l1l1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡴࡶࡲࡴࡵ࡯࡮ࡨࠢࡆࡐࡎࠨစ"))
        self.__111111l111_opy_()
    def __1llll1ll1l1_opy_(self, event_name, bstack1lll1l1l11l_opy_ = None, bstack1111l1l11_opy_=1):
        if bstack1111l1l11_opy_ == 1:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠢဆ"))
        bstack111111l1ll_opy_ = Path(bstack1llllllll1l_opy_ (u"ࠣࡽࡶࡩࡱ࡬࠮ࡤ࡮࡬ࡣࡩ࡯ࡲࡾ࠱ࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࡶ࠲࡯ࡹ࡯࡯ࠤဇ"))
        if self.bstack1lllll11l11_opy_ and bstack111111l1ll_opy_.exists():
            with open(bstack111111l1ll_opy_, bstack1l1l1l1_opy_ (u"ࠩࡵࠫဈ"), encoding=bstack1l1l1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩဉ")) as fp:
                data = json.load(fp)
                try:
                    bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩည"), bstack11ll1llll_opy_(bstack1lll11l1ll_opy_), data, {
                        bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪဋ"): (self.config[bstack1l1l1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨဌ")], self.config[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪဍ")])
                    })
                except Exception as e:
                    logger.debug(bstack11111llll_opy_.format(str(e)))
            bstack111111l1ll_opy_.unlink()
        sys.exit(bstack1111l1l11_opy_)
    @measure(event_name=EVENTS.bstack1llll11ll1l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1lllll1llll_opy_(self, event_name: str, data):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1lll1l1ll11_opy_
        self.bstack1lll1ll11ll_opy_, self.bstack1lllll11l11_opy_ = bstack1lll1l1llll_opy_(data.bs_config)
        os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡘࡔࡌࡘࡆࡈࡌࡆࡡࡇࡍࡗ࠭ဎ")] = self.bstack1lllll11l11_opy_
        if not self.bstack1lll1ll11ll_opy_ or not self.bstack1lllll11l11_opy_:
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡸ࡭࡫ࠠࡔࡆࡎࠤࡈࡒࡉࠡࡤ࡬ࡲࡦࡸࡹࠣဏ"))
        if self.bstack1lll11l1l1_opy_():
            self.__1lll1ll11l1_opy_(event_name, bstack1ll1lll1_opy_())
            return
        try:
            bstack1lll1l1ll11_opy_.end(EVENTS.bstack11l1ll111_opy_.value, EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥတ"), EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤထ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࠠࡔࡆࡎࠤࡘ࡫ࡴࡶࡲ࠱ࠦဒ"))
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡼࡿࠥဓ").format(e))
        start = datetime.now()
        is_started = self.__1lll1lll11l_opy_()
        self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡴࡲࡤࡻࡳࡥࡴࡪ࡯ࡨࠦန"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lllllll11l_opy_()
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࡡࡷ࡭ࡲ࡫ࠢပ"), datetime.now() - start)
            start = datetime.now()
            self.__1llll1l1ll1_opy_(data)
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢဖ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack111111ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1lll1ll11l1_opy_(self, event_name: str, data: bstack1ll1lll1_opy_):
        if not self.bstack1lll11l1l1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰࡰࡱࡩࡨࡺ࠺ࠡࡰࡲࡸࠥࡧࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹࠢဗ"))
            return
        bin_session_id = os.environ.get(bstack1llll1ll111_opy_)
        start = datetime.now()
        self.__1lllllll11l_opy_()
        self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥဘ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠡࡶࡲࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡃࡍࡋࠣࠦမ") + str(bin_session_id) + bstack1l1l1l1_opy_ (u"ࠨࠢယ"))
        start = datetime.now()
        self.__1lll1ll111l_opy_()
        self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧရ"), datetime.now() - start)
    def __1lll1l1l1ll_opy_(self):
        if not self.bstack1llll111l11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡥࡤࡲࡳࡵࡴࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࠤࡲࡵࡤࡶ࡮ࡨࡷࠧလ"))
            return
        bstack1lllll111ll_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨဝ"): (bstack1llll11lll1_opy_, bstack1lll1lllll1_opy_, bstack1lllllll1ll_opy_),
            bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧသ"): (bstack1lll1l1l111_opy_, bstack1lllll11ll1_opy_, bstack1111111l1l_opy_),
        }
        if not self.bstack111111111l_opy_ and self.session_framework in bstack1lllll111ll_opy_:
            bstack1llll11l1ll_opy_, bstack1llll111ll1_opy_, bstack1llllll1ll1_opy_ = bstack1lllll111ll_opy_[self.session_framework]
            bstack11111111l1_opy_ = bstack1llll111ll1_opy_()
            self.bstack1lllll11111_opy_ = bstack11111111l1_opy_
            self.bstack111111111l_opy_ = bstack1llllll1ll1_opy_
            self.bstack1lllllll111_opy_.append(bstack11111111l1_opy_)
            self.bstack1lllllll111_opy_.append(bstack1llll11l1ll_opy_(self.bstack1lllll11111_opy_))
        if not self.bstack1llll111l1l_opy_ and self.config_observability and self.config_observability.success: # bstack1lllll1l1l1_opy_
            self.bstack1llll111l1l_opy_ = bstack1lll1l1ll1l_opy_(self.bstack111111111l_opy_, self.bstack1lllll11111_opy_) # bstack1lll1lll1l1_opy_
            self.bstack1lllllll111_opy_.append(self.bstack1llll111l1l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1llll1l1lll_opy_(self.bstack111111111l_opy_, self.bstack1lllll11111_opy_)
            self.bstack1lllllll111_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡬ࡧࡊࡨࡥࡱࠨဟ"), False) == True:
            self.ai = bstack1llll11l1l1_opy_()
            self.bstack1lllllll111_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1l111l1_opy_ and self.bstack1lll1l111l1_opy_.success:
            self.percy = bstack1llll11llll_opy_(self.bstack1lll1l111l1_opy_)
            self.bstack1lllllll111_opy_.append(self.percy)
        for mod in self.bstack1lllllll111_opy_:
            if not mod.bstack1llllllll11_opy_():
                mod.configure(self.bstack1llll111l11_opy_, self.config, self.cli_bin_session_id, self.bstack111l111l11_opy_)
    def __1111111ll1_opy_(self):
        for mod in self.bstack1lllllll111_opy_:
            if mod.bstack1llllllll11_opy_():
                mod.configure(self.bstack1llll111l11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll1l11ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1llll1l1ll1_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lllll111l1_opy_:
            return
        self.__1lllll11lll_opy_(data)
        bstack11ll11ll11_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࠧဠ")
        req.sdk_language = bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨအ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1lll1lll1ll_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡜ࠤဢ") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠣ࡟ࠣࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢဣ"))
            r = self.bstack1llll111l11_opy_.StartBinSession(req)
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡶࡤࡶࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦဤ"), datetime.now() - bstack11ll11ll11_opy_)
            os.environ[bstack1llll1ll111_opy_] = r.bin_session_id
            self.__1lll1llll1l_opy_(r)
            self.__1lll1l1l1ll_opy_()
            self.bstack111l111l11_opy_.start()
            self.bstack1lllll111l1_opy_ = True
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥ࡟ࠧဥ") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠤဦ"))
        except grpc.bstack11111l1111_opy_ as bstack1llll111111_opy_:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢဧ") + str(bstack1llll111111_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢဨ"))
            traceback.print_exc()
            raise bstack1llll111111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦဩ") + str(e) + bstack1l1l1l1_opy_ (u"ࠣࠤဪ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll11lllll_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1lll1ll111l_opy_(self):
        if not self.bstack1lll11l1l1_opy_() or not self.cli_bin_session_id or self.bstack1lllllll1l1_opy_:
            return
        bstack11ll11ll11_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩါ"), bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬာ")))
        try:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡠࠨိ") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠧࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢီ"))
            r = self.bstack1llll111l11_opy_.ConnectBinSession(req)
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥု"), datetime.now() - bstack11ll11ll11_opy_)
            self.__1lll1llll1l_opy_(r)
            self.__1lll1l1l1ll_opy_()
            self.bstack111l111l11_opy_.start()
            self.bstack1lllllll1l1_opy_ = True
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡜ࠤူ") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪࠢေ"))
        except grpc.bstack11111l1111_opy_ as bstack1llll111111_opy_:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡶ࡬ࡱࡪࡵࡥࡶࡶ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦဲ") + str(bstack1llll111111_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠦဳ"))
            traceback.print_exc()
            raise bstack1llll111111_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣဴ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨဵ"))
            traceback.print_exc()
            raise e
    def __1lll1llll1l_opy_(self, r):
        self.bstack1lll11ll1ll_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠨࡵ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧံ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l1l1l1_opy_ (u"ࠢࡦ࡯ࡳࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡷࡱࡨ့ࠧ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡥࡳࡥࡼࠤ࡮ࡹࠠࡴࡧࡱࡸࠥࡵ࡮࡭ࡻࠣࡥࡸࠦࡰࡢࡴࡷࠤࡴ࡬ࠠࡵࡪࡨࠤࠧࡉ࡯࡯ࡰࡨࡧࡹࡈࡩ࡯ࡕࡨࡷࡸ࡯࡯࡯࠮ࠥࠤࡦࡴࡤࠡࡶ࡫࡭ࡸࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࡦࡲࡳࡰࠢࡸࡷࡪࡪࠠࡣࡻࠣࡗࡹࡧࡲࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪࡨࡶࡪ࡬࡯ࡳࡧ࠯ࠤࡓࡵ࡮ࡦࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤ࡮ࡹࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥး")
        self.bstack1lll1l111l1_opy_ = getattr(r, bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ္"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜်࡚ࠧ")] = self.config_testhub.jwt
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩျ")] = self.config_testhub.build_hashed_id
    def bstack1lll1l1111l_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1111111l11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1llll1lllll_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1llll1lllll_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1l1111l_opy_(event_name=EVENTS.bstack1llll1l11l1_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __1lll1lll11l_opy_(self, bstack1lll11l1lll_opy_=10):
        if self.bstack1111111l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡹࡴࡢࡴࡷ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠢြ"))
            return True
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧွ"))
        if os.getenv(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡉࡓ࡜ࠢှ")) == bstack1lllllllll1_opy_:
            self.cli_bin_session_id = bstack1lllllllll1_opy_
            self.cli_listen_addr = bstack1l1l1l1_opy_ (u"ࠣࡷࡱ࡭ࡽࡀ࠯ࡵ࡯ࡳ࠳ࡸࡪ࡫࠮ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࠩࡸ࠴ࡳࡰࡥ࡮ࠦဿ") % (self.cli_bin_session_id)
            self.bstack1111111l11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1ll11ll_opy_, bstack1l1l1l1_opy_ (u"ࠤࡶࡨࡰࠨ၀")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1111111lll_opy_ compat for text=True in bstack1lllll1l1ll_opy_ python
            encoding=bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ၁"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1ll1ll1_opy_ = threading.Thread(target=self.__1llll1l1111_opy_, args=(bstack1lll11l1lll_opy_,))
        bstack1lll1ll1ll1_opy_.start()
        bstack1lll1ll1ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡷࡵࡧࡷ࡯࠼ࠣࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫࠽ࡼࡵࡨࡰ࡫࠴ࡰࡳࡱࡦࡩࡸࡹ࠮ࡳࡧࡷࡹࡷࡴࡣࡰࡦࡨࢁࠥࡵࡵࡵ࠿ࡾࡷࡪࡲࡦ࠯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡶࡸࡩࡵࡵࡵ࠰ࡵࡩࡦࡪࠨࠪࡿࠣࡩࡷࡸ࠽ࠣ၂") + str(self.process.stderr.read()) + bstack1l1l1l1_opy_ (u"ࠧࠨ၃"))
        if not self.bstack1111111l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࠣ၄") + str(id(self)) + bstack1l1l1l1_opy_ (u"ࠢ࡞ࠢࡦࡰࡪࡧ࡮ࡶࡲࠥ၅"))
            self.__111111l111_opy_()
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡱࡴࡲࡧࡪࡹࡳࡠࡴࡨࡥࡩࡿ࠺ࠡࠤ၆") + str(self.bstack1111111l11_opy_) + bstack1l1l1l1_opy_ (u"ࠤࠥ၇"))
        return self.bstack1111111l11_opy_
    def __1llll1l1111_opy_(self, bstack1llll1lll11_opy_=10):
        bstack1llll11111l_opy_ = time.time()
        while self.process and time.time() - bstack1llll11111l_opy_ < bstack1llll1lll11_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l1l1l1_opy_ (u"ࠥ࡭ࡩࡃࠢ၈") in line:
                    self.cli_bin_session_id = line.split(bstack1l1l1l1_opy_ (u"ࠦ࡮ࡪ࠽ࠣ၉"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡩ࡬ࡪࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦ࠽ࠦ၊") + str(self.cli_bin_session_id) + bstack1l1l1l1_opy_ (u"ࠨࠢ။"))
                    continue
                if bstack1l1l1l1_opy_ (u"ࠢ࡭࡫ࡶࡸࡪࡴ࠽ࠣ၌") in line:
                    self.cli_listen_addr = line.split(bstack1l1l1l1_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤ၍"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡦࡰ࡮ࡥ࡬ࡪࡵࡷࡩࡳࡥࡡࡥࡦࡵ࠾ࠧ၎") + str(self.cli_listen_addr) + bstack1l1l1l1_opy_ (u"ࠥࠦ၏"))
                    continue
                if bstack1l1l1l1_opy_ (u"ࠦࡵࡵࡲࡵ࠿ࠥၐ") in line:
                    port = line.split(bstack1l1l1l1_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦၑ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡰࡰࡴࡷ࠾ࠧၒ") + str(port) + bstack1l1l1l1_opy_ (u"ࠢࠣၓ"))
                    continue
                if line.strip() == bstack1lll1ll1l1l_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l1l1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡊࡑࡢࡗ࡙ࡘࡅࡂࡏࠥၔ"), bstack1l1l1l1_opy_ (u"ࠤ࠴ࠦၕ")) == bstack1l1l1l1_opy_ (u"ࠥ࠵ࠧၖ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1111111l11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡪࡸࡲࡰࡴ࠽ࠤࠧၗ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨၘ"))
        return False
    @measure(event_name=EVENTS.bstack1lll1llll11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def __111111l111_opy_(self):
        if self.bstack1lllll1111l_opy_:
            self.bstack111l111l11_opy_.stop()
            start = datetime.now()
            if self.bstack11111l11l1_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lllllll1l1_opy_:
                    self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡳࡵࡱࡳࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥၙ"), datetime.now() - start)
                else:
                    self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦၚ"), datetime.now() - start)
            self.__1111111ll1_opy_()
            start = datetime.now()
            self.bstack1lllll1111l_opy_.close()
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠣࡦ࡬ࡷࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥၛ"), datetime.now() - start)
            self.bstack1lllll1111l_opy_ = None
        if self.process:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡶࡸࡴࡶࠢၜ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡯࡮ࡲ࡬ࡠࡶ࡬ࡱࡪࠨၝ"), datetime.now() - start)
            self.process = None
            if self.bstack1llll1lll1l_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1ll1111l_opy_()
                self.logger.info(
                    bstack1l1l1l1_opy_ (u"࡛ࠦ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠢၞ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫၟ")] = self.config_testhub.build_hashed_id
        self.bstack1111111l11_opy_ = False
    def __1lllll11lll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l1l1l1_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣၠ")] = selenium.__version__
            data.frameworks.append(bstack1l1l1l1_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤၡ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧၢ")] = __version__
            data.frameworks.append(bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨၣ"))
        except:
            pass
    def bstack1lll1ll1lll_opy_(self, hub_url: str, platform_index: int, bstack1111llll_opy_: Any):
        if self.bstack1111l11l11_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡴࡧࡷࠤࡺࡶࠢၤ"))
            return
        try:
            bstack11ll11ll11_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨၥ")
            self.bstack1111l11l11_opy_ = bstack1111111l1l_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lllll1l111_opy_={bstack1l1l1l1_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡦࡳࡱࡰࡣࡨࡧࡰࡴࠤၦ"): bstack1111llll_opy_}
            )
            def bstack1lll11llll1_opy_(self):
                return
            if self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠣၧ"), True):
                Service.start = bstack1lll11llll1_opy_
                Service.stop = bstack1lll11llll1_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣၨ"), datetime.now() - bstack11ll11ll11_opy_)
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡷࡪࡲࡥ࡯࡫ࡸࡱ࠿ࠦࠢၩ") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥၪ"))
    def bstack1lll1l11l1l_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack1ll1llll11_opy_
            self.bstack1111l11l11_opy_ = bstack1lllllll1ll_opy_(
                platform_index,
                framework_name=bstack1l1l1l1_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢၫ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠽ࠤࠧၬ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨၭ"))
            pass
    def bstack1llllll1l11_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣၮ"))
            return
        if bstack1l111l11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢၯ"): pytest.__version__ }, [bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧၰ")])
            return
        try:
            import pytest
            self.test_framework = bstack111111llll_opy_({ bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤၱ"): pytest.__version__ }, [bstack1l1l1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥၲ")])
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡺࡶࡨࡷࡹࡀࠠࠣၳ") + str(e) + bstack1l1l1l1_opy_ (u"ࠧࠨၴ"))
        self.bstack1lll1ll1111_opy_()
    def bstack1lll1ll1111_opy_(self):
        if not self.bstack11lllll1_opy_():
            return
        bstack1lll111l1_opy_ = None
        def bstack11l1l1l1l_opy_(config, startdir):
            return bstack1l1l1l1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦၵ").format(bstack1l1l1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨၶ"))
        def bstack1l11llllll_opy_():
            return
        def bstack1llllll111_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l1l1l1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨၷ"):
                return bstack1l1l1l1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣၸ")
            else:
                return bstack1lll111l1_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack1lll111l1_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11l1l1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11llllll_opy_
            Config.getoption = bstack1llllll111_opy_
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡶࡦ࡬ࠥࡶࡹࡵࡧࡶࡸࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠽ࠤࠧၹ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧၺ"))
    def bstack1lllll1ll1l_opy_(self):
        bstack1llll1111ll_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1llll1111ll_opy_, dict):
            if cli.config_observability:
                bstack1llll1111ll_opy_.update(
                    {bstack1l1l1l1_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧၻ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤၼ") in accessibility.get(bstack1l1l1l1_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣၽ"), {}):
                    bstack1lll1l11l11_opy_ = accessibility.get(bstack1l1l1l1_opy_ (u"ࠣࡱࡳࡸ࡮ࡵ࡮ࡴࠤၾ"))
                    bstack1lll1l11l11_opy_.update({ bstack1l1l1l1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠥၿ"): bstack1lll1l11l11_opy_.pop(bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࡤࡺ࡯ࡠࡹࡵࡥࡵࠨႀ")) })
                bstack1llll1111ll_opy_.update({bstack1l1l1l1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦႁ"): accessibility })
        return bstack1llll1111ll_opy_
    @measure(event_name=EVENTS.bstack1llllll1l1l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
    def bstack11111l11l1_opy_(self, bstack1lllll1lll1_opy_: str = None, bstack1llllll11ll_opy_: str = None, bstack1111l1l11_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1llll111l11_opy_:
            return
        bstack11ll11ll11_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1111l1l11_opy_:
            req.bstack1111l1l11_opy_ = bstack1111l1l11_opy_
        if bstack1lllll1lll1_opy_:
            req.bstack1lllll1lll1_opy_ = bstack1lllll1lll1_opy_
        if bstack1llllll11ll_opy_:
            req.bstack1llllll11ll_opy_ = bstack1llllll11ll_opy_
        try:
            r = self.bstack1llll111l11_opy_.StopBinSession(req)
            self.bstack1ll111lll_opy_(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡵࡰࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨႂ"), datetime.now() - bstack11ll11ll11_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll111lll_opy_(self, key: str, value: timedelta):
        tag = bstack1l1l1l1_opy_ (u"ࠨࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࠨႃ") if self.bstack1lll11l1l1_opy_() else bstack1l1l1l1_opy_ (u"ࠢ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࠨႄ")
        self.bstack1lll11lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠣ࠼ࠥႅ").join([tag + bstack1l1l1l1_opy_ (u"ࠤ࠰ࠦႆ") + str(id(self)), key])] += value
    def bstack1ll1111l_opy_(self):
        if not os.getenv(bstack1l1l1l1_opy_ (u"ࠥࡈࡊࡈࡕࡈࡡࡓࡉࡗࡌࠢႇ"), bstack1l1l1l1_opy_ (u"ࠦ࠵ࠨႈ")) == bstack1l1l1l1_opy_ (u"ࠧ࠷ࠢႉ"):
            return
        bstack1llll11ll11_opy_ = dict()
        bstack11111l1ll1_opy_ = []
        if self.test_framework:
            bstack11111l1ll1_opy_.extend(list(self.test_framework.bstack11111l1ll1_opy_.values()))
        if self.bstack1111l11l11_opy_:
            bstack11111l1ll1_opy_.extend(list(self.bstack1111l11l11_opy_.bstack11111l1ll1_opy_.values()))
        for instance in bstack11111l1ll1_opy_:
            if not instance.platform_index in bstack1llll11ll11_opy_:
                bstack1llll11ll11_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1llll11ll11_opy_[instance.platform_index]
            for k, v in instance.bstack1llll11l111_opy_().items():
                report[k] += v
                report[k.split(bstack1l1l1l1_opy_ (u"ࠨ࠺ࠣႊ"))[0]] += v
        bstack1llll1l1l1l_opy_ = sorted([(k, v) for k, v in self.bstack1lll11lll1l_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll1l11lll_opy_ = 0
        for r in bstack1llll1l1l1l_opy_:
            bstack1llll11l11l_opy_ = r[1].total_seconds()
            bstack1lll1l11lll_opy_ += bstack1llll11l11l_opy_
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡜ࡲࡨࡶ࡫ࡣࠠࡤ࡮࡬࠾ࢀࡸ࡛࠱࡟ࢀࡁࠧႋ") + str(bstack1llll11l11l_opy_) + bstack1l1l1l1_opy_ (u"ࠣࠤႌ"))
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤ࠰࠱ႍࠧ"))
        bstack1llll1l111l_opy_ = []
        for platform_index, report in bstack1llll11ll11_opy_.items():
            bstack1llll1l111l_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1llll1l111l_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1llll1l1_opy_ = set()
        bstack1llllllllll_opy_ = 0
        for r in bstack1llll1l111l_opy_:
            bstack1llll11l11l_opy_ = r[2].total_seconds()
            bstack1llllllllll_opy_ += bstack1llll11l11l_opy_
            bstack1llll1l1_opy_.add(r[0])
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠰ࡿࡷࡡ࠰࡞ࡿ࠽ࡿࡷࡡ࠱࡞ࡿࡀࠦႎ") + str(bstack1llll11l11l_opy_) + bstack1l1l1l1_opy_ (u"ࠦࠧႏ"))
        if self.bstack1lll11l1l1_opy_():
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࠳࠭ࠣ႐"))
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡣ࡭࡫࠽ࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࡀࡿࡹࡵࡴࡢ࡮ࡢࡧࡱ࡯ࡽࠡࡶࡨࡷࡹࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ࠯ࡾࡷࡹࡸࠨࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠬࢁࡂࠨ႑") + str(bstack1llllllllll_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣ႒"))
        else:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡳࡡࡪࡰ࠰ࡴࡷࡵࡣࡦࡵࡶࡁࠧ႓") + str(bstack1lll1l11lll_opy_) + bstack1l1l1l1_opy_ (u"ࠤࠥ႔"))
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥ࠱࠲ࠨ႕"))
    def bstack1lll11ll1ll_opy_(self, r):
        if r is not None and getattr(r, bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࠬ႖"), None) and getattr(r.testhub, bstack1l1l1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ႗"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l1l1l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ႘")))
            for bstack1llll1111l1_opy_, err in errors.items():
                if err[bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ႙")] == bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ႚ"):
                    self.logger.info(err[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪႛ")])
                else:
                    self.logger.error(err[bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫႜ")])
cli = SDKCLI()