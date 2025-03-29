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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1llllll_opy_ import get_logger
logger = get_logger(__name__)
bstack11l11l11111_opy_: Dict[str, float] = {}
bstack11l11l11l11_opy_: List = []
bstack11l111lllll_opy_ = 5
bstack111lll11_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡨࠩᯢ"), bstack1l1l1l1_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩᯣ"))
logging.getLogger(bstack1l1l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠩᯤ")).setLevel(logging.WARNING)
lock = FileLock(bstack111lll11_opy_+bstack1l1l1l1_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᯥ"))
class bstack11l111lll1l_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack11l11l111l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack11l11l111l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1l1l1_opy_ (u"ࠤࡰࡩࡦࡹࡵࡳࡧ᯦ࠥ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1l1ll11_opy_:
    global bstack11l11l11111_opy_
    @staticmethod
    def bstack1ll1lll1l11_opy_(key: str):
        bstack1lll11111ll_opy_ = bstack1lll1l1ll11_opy_.bstack1l11l111lll_opy_(key)
        bstack1lll1l1ll11_opy_.mark(bstack1lll11111ll_opy_+bstack1l1l1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᯧ"))
        return bstack1lll11111ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack11l11l11111_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᯨ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1l1ll11_opy_.mark(end)
            bstack1lll1l1ll11_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷ࠿ࠦࡻࡾࠤᯩ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack11l11l11111_opy_ or end not in bstack11l11l11111_opy_:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠤࡴࡸࠠࡦࡰࡧࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠣᯪ").format(start,end))
                return
            duration: float = bstack11l11l11111_opy_[end] - bstack11l11l11111_opy_[start]
            bstack11l11l1111l_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᯫ"), bstack1l1l1l1_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᯬ")).lower() == bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᯭ")
            bstack11l11l111ll_opy_: bstack11l111lll1l_opy_ = bstack11l111lll1l_opy_(duration, label, bstack11l11l11111_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᯮ"), 0), command, test_name, hook_type, bstack11l11l1111l_opy_)
            del bstack11l11l11111_opy_[start]
            del bstack11l11l11111_opy_[end]
            bstack1lll1l1ll11_opy_.bstack11l111llll1_opy_(bstack11l11l111ll_opy_)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡩࡦࡹࡵࡳ࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵ࠽ࠤࢀࢃࠢᯯ").format(e))
    @staticmethod
    def bstack11l111llll1_opy_(bstack11l11l111ll_opy_):
        os.makedirs(os.path.dirname(bstack111lll11_opy_)) if not os.path.exists(os.path.dirname(bstack111lll11_opy_)) else None
        bstack1lll1l1ll11_opy_.bstack11l111lll11_opy_()
        try:
            with lock:
                with open(bstack111lll11_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࠫࠣᯰ"), encoding=bstack1l1l1l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᯱ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack11l11l111ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack11l11l11l1l_opy_:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠡࡽࢀ᯲ࠦ").format(bstack11l11l11l1l_opy_))
            with lock:
                with open(bstack111lll11_opy_, bstack1l1l1l1_opy_ (u"ࠣࡹ᯳ࠥ"), encoding=bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᯴")) as file:
                    data = [bstack11l11l111ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡥࡵࡶࡥ࡯ࡦࠣࡿࢂࠨ᯵").format(str(e)))
        finally:
            if os.path.exists(bstack111lll11_opy_+bstack1l1l1l1_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ᯶")):
                os.remove(bstack111lll11_opy_+bstack1l1l1l1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦ᯷"))
    @staticmethod
    def bstack11l111lll11_opy_():
        attempt = 0
        while (attempt < bstack11l111lllll_opy_):
            attempt += 1
            if os.path.exists(bstack111lll11_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠮࡭ࡱࡦ࡯ࠧ᯸")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack1l11l111lll_opy_(label: str) -> str:
        try:
            return bstack1l1l1l1_opy_ (u"ࠢࡼࡿ࠽ࡿࢂࠨ᯹").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᯺").format(e))