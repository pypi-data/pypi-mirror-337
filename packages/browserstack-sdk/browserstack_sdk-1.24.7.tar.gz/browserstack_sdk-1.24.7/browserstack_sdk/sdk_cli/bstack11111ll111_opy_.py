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
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111lllll1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1111ll1111_opy_:
    bstack1l11l11llll_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡤࡨࡲࡨ࡮࡭ࡢࡴ࡮ࠦᒃ")
    context: bstack1111lllll1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111lllll1_opy_):
        self.context = context
        self.data = dict({bstack1111ll1111_opy_.bstack1l11l11llll_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒄ"), bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬᒅ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111lll11_opy_(self, target: object):
        return bstack1111ll1111_opy_.create_context(target) == self.context
    def bstack1ll1l111ll1_opy_(self, context: bstack1111lllll1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll111lll_opy_(self, key: str, value: timedelta):
        self.data[bstack1111ll1111_opy_.bstack1l11l11llll_opy_][key] += value
    def bstack1llll11l111_opy_(self) -> dict:
        return self.data[bstack1111ll1111_opy_.bstack1l11l11llll_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111lllll1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )