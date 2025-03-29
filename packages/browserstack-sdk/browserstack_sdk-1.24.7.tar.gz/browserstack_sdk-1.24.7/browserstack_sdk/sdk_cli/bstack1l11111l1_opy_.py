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
from collections import defaultdict
from threading import Lock
from dataclasses import dataclass
import logging
import traceback
from typing import List, Dict, Any
import os
@dataclass
class bstack1ll111lll1_opy_:
    sdk_version: str
    path_config: str
    path_project: str
    test_framework: str
    frameworks: List[str]
    framework_versions: Dict[str, str]
    bs_config: Dict[str, Any]
@dataclass
class bstack1ll1lll1_opy_:
    pass
class bstack1l1l1111ll_opy_:
    bstack1l11l1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠢႝ")
    CONNECT = bstack1l1l1l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨ႞")
    bstack111ll11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡳࡩࡷࡷࡨࡴࡽ࡮ࠣ႟")
    CONFIG = bstack1l1l1l1_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢႠ")
    bstack1lll111llll_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷࠧႡ")
    bstack1l11l11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡨࡼ࡮ࡺࠢႢ")
class bstack1lll11l11ll_opy_:
    bstack1lll11l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡶࡸࡦࡸࡴࡦࡦࠥႣ")
    FINISHED = bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧႤ")
class bstack1lll11l1111_opy_:
    bstack1lll11l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣႥ")
    FINISHED = bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥႦ")
class bstack1lll111lll1_opy_:
    bstack1lll11l111l_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡶࡸࡦࡸࡴࡦࡦࠥႧ")
    FINISHED = bstack1l1l1l1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡲࡶࡰࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧႨ")
class bstack1lll111ll1l_opy_:
    bstack1lll11l1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡤࡴࡨࡥࡹ࡫ࡤࠣႩ")
class bstack1lll11l11l1_opy_:
    _11111l111l_opy_ = None
    def __new__(cls):
        if not cls._11111l111l_opy_:
            cls._11111l111l_opy_ = super(bstack1lll11l11l1_opy_, cls).__new__(cls)
        return cls._11111l111l_opy_
    def __init__(self):
        self._hooks = defaultdict(lambda: defaultdict(list))
        self._lock = Lock()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def clear(self):
        with self._lock:
            self._hooks = defaultdict(list)
    def register(self, event_name, callback):
        with self._lock:
            if not callable(callback):
                raise ValueError(bstack1l1l1l1_opy_ (u"ࠥࡇࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡳࡵࡴࡶࠣࡦࡪࠦࡣࡢ࡮࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࠨႪ") + event_name)
            pid = os.getpid()
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡗ࡫ࡧࡪࡵࡷࡩࡷ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࠠࠨࡽࡨࡺࡪࡴࡴࡠࡰࡤࡱࡪࢃࠧࠡࡹ࡬ࡸ࡭ࠦࡰࡪࡦࠣࠦႫ") + str(pid) + bstack1l1l1l1_opy_ (u"ࠧࠨႬ"))
            self._hooks[event_name][pid].append(callback)
    def invoke(self, event_name, *args, **kwargs):
        with self._lock:
            pid = os.getpid()
            callbacks = self._hooks.get(event_name, {}).get(pid, [])
            if not callbacks:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡎࡰࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࠡࠩࡾࡩࡻ࡫࡮ࡵࡡࡱࡥࡲ࡫ࡽࠨࠢࡺ࡭ࡹ࡮ࠠࡱ࡫ࡧࠤࠧႭ") + str(pid) + bstack1l1l1l1_opy_ (u"ࠢࠣႮ"))
                return
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡋࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡥࡤࡰࡱࡨࡡࡤ࡭ࡶ࠭ࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࠥ࠭ࡻࡦࡸࡨࡲࡹࡥ࡮ࡢ࡯ࡨࢁࠬࠦࡷࡪࡶ࡫ࠤࡵ࡯ࡤࠡࠤႯ") + str(pid) + bstack1l1l1l1_opy_ (u"ࠤࠥႰ"))
            for callback in callbacks:
                try:
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡍࡳࡼ࡯࡬ࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࠢࠪࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠩࠣࡻ࡮ࡺࡨࠡࡲ࡬ࡨࠥࠨႱ") + str(pid) + bstack1l1l1l1_opy_ (u"ࠦࠧႲ"))
                    callback(event_name, *args, **kwargs)
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࠤࠬࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠫࠥࡽࡩࡵࡪࠣࡴ࡮ࡪࠠࡼࡲ࡬ࡨࢂࡀࠠࠣႳ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢႴ"))
                    traceback.print_exc()
bstack1l11111l1_opy_ = bstack1lll11l11l1_opy_()