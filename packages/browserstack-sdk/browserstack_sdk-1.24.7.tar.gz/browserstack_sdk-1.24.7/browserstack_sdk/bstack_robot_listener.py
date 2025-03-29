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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111lll1l11_opy_ import RobotHandler
from bstack_utils.capture import bstack11l11lllll_opy_
from bstack_utils.bstack11l11ll1l1_opy_ import bstack111lll1lll_opy_, bstack11l11llll1_opy_, bstack11l11l1ll1_opy_
from bstack_utils.bstack11l11ll1ll_opy_ import bstack1l11l1lll1_opy_
from bstack_utils.bstack11l1l1111l_opy_ import bstack111111ll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11ll111l_opy_, bstack1lll11llll_opy_, Result, \
    bstack111ll1llll_opy_, bstack111ll1l111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ໙"): [],
        bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໚"): [],
        bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭໛"): []
    }
    bstack111lll1l1l_opy_ = []
    bstack111lll11ll_opy_ = []
    @staticmethod
    def bstack11l11lll1l_opy_(log):
        if not ((isinstance(log[bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫໜ")], list) or (isinstance(log[bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬໝ")], dict)) and len(log[bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ໞ")])>0) or (isinstance(log[bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧໟ")], str) and log[bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໠")].strip())):
            return
        active = bstack1l11l1lll1_opy_.bstack11l11l1lll_opy_()
        log = {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໡"): log[bstack1l1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໢")],
            bstack1l1l1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭໣"): bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠫ࡟࠭໤"),
            bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭໥"): log[bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໦")],
        }
        if active:
            if active[bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ໧")] == bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭໨"):
                log[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ໩")] = active[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ໪")]
            elif active[bstack1l1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ໫")] == bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ໬"):
                log[bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭໭")] = active[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໮")]
        bstack111111ll1_opy_.bstack1l11l1l1_opy_([log])
    def __init__(self):
        self.messages = bstack111ll11111_opy_()
        self._111lllllll_opy_ = None
        self._11l11111ll_opy_ = None
        self._111lll1111_opy_ = OrderedDict()
        self.bstack11l11l111l_opy_ = bstack11l11lllll_opy_(self.bstack11l11lll1l_opy_)
    @bstack111ll1llll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111ll1l1ll_opy_()
        if not self._111lll1111_opy_.get(attrs.get(bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫ໯")), None):
            self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬ໰"))] = {}
        bstack111ll11lll_opy_ = bstack11l11l1ll1_opy_(
                bstack11l111l11l_opy_=attrs.get(bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭໱")),
                name=name,
                started_at=bstack1lll11llll_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1l1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ໲")], start=os.getcwd()) if attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ໳")) != bstack1l1l1l1_opy_ (u"࠭ࠧ໴") else bstack1l1l1l1_opy_ (u"ࠧࠨ໵"),
                framework=bstack1l1l1l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ໶")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬ໷"), None)
        self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭໸"))][bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໹")] = bstack111ll11lll_opy_
    @bstack111ll1llll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1111l1l_opy_()
        self._11l111ll11_opy_(messages)
        for bstack11l1111l11_opy_ in self.bstack111lll1l1l_opy_:
            bstack11l1111l11_opy_[bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ໺")][bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ໻")].extend(self.store[bstack1l1l1l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭໼")])
            bstack111111ll1_opy_.bstack11ll1ll111_opy_(bstack11l1111l11_opy_)
        self.bstack111lll1l1l_opy_ = []
        self.store[bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧ໽")] = []
    @bstack111ll1llll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l11l111l_opy_.start()
        if not self._111lll1111_opy_.get(attrs.get(bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬ໾")), None):
            self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭໿"))] = {}
        driver = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪༀ"), None)
        bstack11l11ll1l1_opy_ = bstack11l11l1ll1_opy_(
            bstack11l111l11l_opy_=attrs.get(bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࠨ༁")),
            name=name,
            started_at=bstack1lll11llll_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1l1l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭༂")], start=os.getcwd()),
            scope=RobotHandler.bstack11l1111ll1_opy_(attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༃"), None)),
            framework=bstack1l1l1l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ༄"),
            tags=attrs[bstack1l1l1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ༅")],
            hooks=self.store[bstack1l1l1l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ༆")],
            bstack11l11l1l11_opy_=bstack111111ll1_opy_.bstack11l1l11l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1l1l1_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨ༇").format(bstack1l1l1l1_opy_ (u"ࠧࠦࠢ༈").join(attrs[bstack1l1l1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ༉")]), name) if attrs[bstack1l1l1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬ༊")] else name
        )
        self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠨ࡫ࡧࠫ་"))][bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༌")] = bstack11l11ll1l1_opy_
        threading.current_thread().current_test_uuid = bstack11l11ll1l1_opy_.bstack111ll11l1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭།"), None)
        self.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ༎"), bstack11l11ll1l1_opy_)
    @bstack111ll1llll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l11l111l_opy_.reset()
        bstack111ll111l1_opy_ = bstack111llll1l1_opy_.get(attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ༏")), bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ༐"))
        self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪ༑"))][bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༒")].stop(time=bstack1lll11llll_opy_(), duration=int(attrs.get(bstack1l1l1l1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧ༓"), bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬ༔"))), result=Result(result=bstack111ll111l1_opy_, exception=attrs.get(bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༕")), bstack11l111llll_opy_=[attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༖"))]))
        self.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ༗"), self._111lll1111_opy_[attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡪࡦ༘ࠪ"))][bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤ༙ࠫ")], True)
        self.store[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭༚")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111ll1llll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111ll1l1ll_opy_()
        current_test_id = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬ༛"), None)
        bstack111ll1111l_opy_ = current_test_id if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭༜"), None) else bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ༝"), None)
        if attrs.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ༞"), bstack1l1l1l1_opy_ (u"ࠧࠨ༟")).lower() in [bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ༠"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ༡")]:
            hook_type = bstack111llll1ll_opy_(attrs.get(bstack1l1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ༢")), bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ༣"), None))
            hook_name = bstack1l1l1l1_opy_ (u"ࠬࢁࡽࠨ༤").format(attrs.get(bstack1l1l1l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭༥"), bstack1l1l1l1_opy_ (u"ࠧࠨ༦")))
            if hook_type in [bstack1l1l1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ༧"), bstack1l1l1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ༨")]:
                hook_name = bstack1l1l1l1_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫ༩").format(bstack111l1lllll_opy_.get(hook_type), attrs.get(bstack1l1l1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ༪"), bstack1l1l1l1_opy_ (u"ࠬ࠭༫")))
            bstack111ll11l11_opy_ = bstack11l11llll1_opy_(
                bstack11l111l11l_opy_=bstack111ll1111l_opy_ + bstack1l1l1l1_opy_ (u"࠭࠭ࠨ༬") + attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ༭"), bstack1l1l1l1_opy_ (u"ࠨࠩ༮")).lower(),
                name=hook_name,
                started_at=bstack1lll11llll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1l1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༯")), start=os.getcwd()),
                framework=bstack1l1l1l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ༰"),
                tags=attrs[bstack1l1l1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ༱")],
                scope=RobotHandler.bstack11l1111ll1_opy_(attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ༲"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111ll11l11_opy_.bstack111ll11l1l_opy_()
            threading.current_thread().current_hook_id = bstack111ll1111l_opy_ + bstack1l1l1l1_opy_ (u"࠭࠭ࠨ༳") + attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ༴"), bstack1l1l1l1_opy_ (u"ࠨ༵ࠩ")).lower()
            self.store[bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༶")] = [bstack111ll11l11_opy_.bstack111ll11l1l_opy_()]
            if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ༷ࠧ"), None):
                self.store[bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ༸")].append(bstack111ll11l11_opy_.bstack111ll11l1l_opy_())
            else:
                self.store[bstack1l1l1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶ༹ࠫ")].append(bstack111ll11l11_opy_.bstack111ll11l1l_opy_())
            if bstack111ll1111l_opy_:
                self._111lll1111_opy_[bstack111ll1111l_opy_ + bstack1l1l1l1_opy_ (u"࠭࠭ࠨ༺") + attrs.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ༻"), bstack1l1l1l1_opy_ (u"ࠨࠩ༼")).lower()] = { bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༽"): bstack111ll11l11_opy_ }
            bstack111111ll1_opy_.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ༾"), bstack111ll11l11_opy_)
        else:
            bstack11l1l1l111_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠫ࡮ࡪࠧ༿"): uuid4().__str__(),
                bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡹࡶࠪཀ"): bstack1l1l1l1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬཁ").format(attrs.get(bstack1l1l1l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧག")), attrs.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭གྷ"), bstack1l1l1l1_opy_ (u"ࠩࠪང"))) if attrs.get(bstack1l1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨཅ"), []) else attrs.get(bstack1l1l1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫཆ")),
                bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬཇ"): attrs.get(bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ཈"), []),
                bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫཉ"): bstack1lll11llll_opy_(),
                bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨཊ"): bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪཋ"),
                bstack1l1l1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨཌ"): attrs.get(bstack1l1l1l1_opy_ (u"ࠫࡩࡵࡣࠨཌྷ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ཎ"))
            }
            if attrs.get(bstack1l1l1l1_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧཏ"), bstack1l1l1l1_opy_ (u"ࠧࠨཐ")) != bstack1l1l1l1_opy_ (u"ࠨࠩད"):
                bstack11l1l1l111_opy_[bstack1l1l1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪདྷ")] = attrs.get(bstack1l1l1l1_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫན"))
            if not self.bstack111lll11ll_opy_:
                self._111lll1111_opy_[self._111lll1ll1_opy_()][bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཔ")].add_step(bstack11l1l1l111_opy_)
                threading.current_thread().current_step_uuid = bstack11l1l1l111_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࠨཕ")]
            self.bstack111lll11ll_opy_.append(bstack11l1l1l111_opy_)
    @bstack111ll1llll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1111l1l_opy_()
        self._11l111ll11_opy_(messages)
        current_test_id = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨབ"), None)
        bstack111ll1111l_opy_ = current_test_id if current_test_id else bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪབྷ"), None)
        bstack111ll1ll1l_opy_ = bstack111llll1l1_opy_.get(attrs.get(bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨམ")), bstack1l1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪཙ"))
        bstack111ll1lll1_opy_ = attrs.get(bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཚ"))
        if bstack111ll1ll1l_opy_ != bstack1l1l1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཛ") and not attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཛྷ")) and self._111lllllll_opy_:
            bstack111ll1lll1_opy_ = self._111lllllll_opy_
        bstack11l1l11ll1_opy_ = Result(result=bstack111ll1ll1l_opy_, exception=bstack111ll1lll1_opy_, bstack11l111llll_opy_=[bstack111ll1lll1_opy_])
        if attrs.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫཝ"), bstack1l1l1l1_opy_ (u"ࠧࠨཞ")).lower() in [bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧཟ"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫའ")]:
            bstack111ll1111l_opy_ = current_test_id if current_test_id else bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ཡ"), None)
            if bstack111ll1111l_opy_:
                bstack11l11ll11l_opy_ = bstack111ll1111l_opy_ + bstack1l1l1l1_opy_ (u"ࠦ࠲ࠨར") + attrs.get(bstack1l1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪལ"), bstack1l1l1l1_opy_ (u"࠭ࠧཤ")).lower()
                self._111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཥ")].stop(time=bstack1lll11llll_opy_(), duration=int(attrs.get(bstack1l1l1l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ས"), bstack1l1l1l1_opy_ (u"ࠩ࠳ࠫཧ"))), result=bstack11l1l11ll1_opy_)
                bstack111111ll1_opy_.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬཨ"), self._111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཀྵ")])
        else:
            bstack111ll1111l_opy_ = current_test_id if current_test_id else bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧཪ"), None)
            if bstack111ll1111l_opy_ and len(self.bstack111lll11ll_opy_) == 1:
                current_step_uuid = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪཫ"), None)
                self._111lll1111_opy_[bstack111ll1111l_opy_][bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཬ")].bstack11l11l11ll_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1l1l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭཭"), bstack1l1l1l1_opy_ (u"ࠩ࠳ࠫ཮"))), result=bstack11l1l11ll1_opy_)
            else:
                self.bstack111ll111ll_opy_(attrs)
            self.bstack111lll11ll_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨ཯"), bstack1l1l1l1_opy_ (u"ࠫࡳࡵࠧ཰")) == bstack1l1l1l1_opy_ (u"ࠬࡿࡥࡴཱࠩ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l11l1lll1_opy_.bstack11l11l1lll_opy_():
                logs.append({
                    bstack1l1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱིࠩ"): bstack1lll11llll_opy_(),
                    bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཱི"): message.get(bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦུࠩ")),
                    bstack1l1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨཱུ"): message.get(bstack1l1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩྲྀ")),
                    **bstack1l11l1lll1_opy_.bstack11l11l1lll_opy_()
                })
                if len(logs) > 0:
                    bstack111111ll1_opy_.bstack1l11l1l1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack111111ll1_opy_.bstack111llllll1_opy_()
    def bstack111ll111ll_opy_(self, bstack111llll111_opy_):
        if not bstack1l11l1lll1_opy_.bstack11l11l1lll_opy_():
            return
        kwname = bstack1l1l1l1_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪཷ").format(bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬླྀ")), bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫཹ"), bstack1l1l1l1_opy_ (u"ࠧࠨེ"))) if bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸཻ࠭"), []) else bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦོࠩ"))
        error_message = bstack1l1l1l1_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤཽ").format(kwname, bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫཾ")), str(bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཿ"))))
        bstack11l111ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ྀࠦࠧ").format(kwname, bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹཱྀࠧ")))
        bstack111lll11l1_opy_ = error_message if bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྂ")) else bstack11l111ll1l_opy_
        bstack11l111l111_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྃ"): self.bstack111lll11ll_opy_[-1].get(bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ྄ࠧ"), bstack1lll11llll_opy_()),
            bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྅"): bstack111lll11l1_opy_,
            bstack1l1l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ྆"): bstack1l1l1l1_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ྇") if bstack111llll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྈ")) == bstack1l1l1l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ྉ") else bstack1l1l1l1_opy_ (u"ࠩࡌࡒࡋࡕࠧྊ"),
            **bstack1l11l1lll1_opy_.bstack11l11l1lll_opy_()
        }
        bstack111111ll1_opy_.bstack1l11l1l1_opy_([bstack11l111l111_opy_])
    def _111lll1ll1_opy_(self):
        for bstack11l111l11l_opy_ in reversed(self._111lll1111_opy_):
            bstack111lllll1l_opy_ = bstack11l111l11l_opy_
            data = self._111lll1111_opy_[bstack11l111l11l_opy_][bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྋ")]
            if isinstance(data, bstack11l11llll1_opy_):
                if not bstack1l1l1l1_opy_ (u"ࠫࡊࡇࡃࡉࠩྌ") in data.bstack111ll11ll1_opy_():
                    return bstack111lllll1l_opy_
            else:
                return bstack111lllll1l_opy_
    def _11l111ll11_opy_(self, messages):
        try:
            bstack11l111111l_opy_ = BuiltIn().get_variable_value(bstack1l1l1l1_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦྍ")) in (bstack111lllll11_opy_.DEBUG, bstack111lllll11_opy_.TRACE)
            for message, bstack11l11111l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྎ"))
                level = message.get(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྏ"))
                if level == bstack111lllll11_opy_.FAIL:
                    self._111lllllll_opy_ = name or self._111lllllll_opy_
                    self._11l11111ll_opy_ = bstack11l11111l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤྐ")) if bstack11l111111l_opy_ and bstack11l11111l1_opy_ else self._11l11111ll_opy_
        except:
            pass
    @classmethod
    def bstack11l11ll111_opy_(self, event: str, bstack111ll1l1l1_opy_: bstack111lll1lll_opy_, bstack11l1111lll_opy_=False):
        if event == bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫྑ"):
            bstack111ll1l1l1_opy_.set(hooks=self.store[bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧྒ")])
        if event == bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬྒྷ"):
            event = bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧྔ")
        if bstack11l1111lll_opy_:
            bstack11l111l1l1_opy_ = {
                bstack1l1l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪྕ"): event,
                bstack111ll1l1l1_opy_.bstack11l111l1ll_opy_(): bstack111ll1l1l1_opy_.bstack11l111lll1_opy_(event)
            }
            self.bstack111lll1l1l_opy_.append(bstack11l111l1l1_opy_)
        else:
            bstack111111ll1_opy_.bstack11l11ll111_opy_(event, bstack111ll1l1l1_opy_)
class bstack111ll11111_opy_:
    def __init__(self):
        self._111lll111l_opy_ = []
    def bstack111ll1l1ll_opy_(self):
        self._111lll111l_opy_.append([])
    def bstack11l1111l1l_opy_(self):
        return self._111lll111l_opy_.pop() if self._111lll111l_opy_ else list()
    def push(self, message):
        self._111lll111l_opy_[-1].append(message) if self._111lll111l_opy_ else self._111lll111l_opy_.append([message])
class bstack111lllll11_opy_:
    FAIL = bstack1l1l1l1_opy_ (u"ࠧࡇࡃࡌࡐࠬྖ")
    ERROR = bstack1l1l1l1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧྗ")
    WARNING = bstack1l1l1l1_opy_ (u"࡚ࠩࡅࡗࡔࠧ྘")
    bstack111ll1l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡍࡓࡌࡏࠨྙ")
    DEBUG = bstack1l1l1l1_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪྚ")
    TRACE = bstack1l1l1l1_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫྛ")
    bstack11l1111111_opy_ = [FAIL, ERROR]
def bstack111llll11l_opy_(bstack111ll1ll11_opy_):
    if not bstack111ll1ll11_opy_:
        return None
    if bstack111ll1ll11_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩྜ"), None):
        return getattr(bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྜྷ")], bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ྞ"), None)
    return bstack111ll1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧྟ"), None)
def bstack111llll1ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩྠ"), bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ྡ")]:
        return
    if hook_type.lower() == bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫྡྷ"):
        if current_test_uuid is None:
            return bstack1l1l1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪྣ")
        else:
            return bstack1l1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬྤ")
    elif hook_type.lower() == bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪྥ"):
        if current_test_uuid is None:
            return bstack1l1l1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬྦ")
        else:
            return bstack1l1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧྦྷ")