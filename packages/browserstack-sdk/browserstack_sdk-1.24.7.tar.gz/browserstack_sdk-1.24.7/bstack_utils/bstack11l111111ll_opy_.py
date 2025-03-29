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
import threading
import logging
logger = logging.getLogger(__name__)
bstack11l1111111l_opy_ = 1000
bstack111lllllll1_opy_ = 2
class bstack111llllll1l_opy_:
    def __init__(self, handler, bstack111llllllll_opy_=bstack11l1111111l_opy_, bstack11l11111ll1_opy_=bstack111lllllll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111llllllll_opy_ = bstack111llllllll_opy_
        self.bstack11l11111ll1_opy_ = bstack11l11111ll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111l111lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack11l11111l1l_opy_()
    def bstack11l11111l1l_opy_(self):
        self.bstack111l111lll_opy_ = threading.Event()
        def bstack11l11111l11_opy_():
            self.bstack111l111lll_opy_.wait(self.bstack11l11111ll1_opy_)
            if not self.bstack111l111lll_opy_.is_set():
                self.bstack11l11111111_opy_()
        self.timer = threading.Thread(target=bstack11l11111l11_opy_, daemon=True)
        self.timer.start()
    def bstack11l111111l1_opy_(self):
        try:
            if self.bstack111l111lll_opy_ and not self.bstack111l111lll_opy_.is_set():
                self.bstack111l111lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫ᱔") + (str(e) or bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤ᱕")))
        finally:
            self.timer = None
    def bstack111llllll11_opy_(self):
        if self.timer:
            self.bstack11l111111l1_opy_()
        self.bstack11l11111l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111llllllll_opy_:
                threading.Thread(target=self.bstack11l11111111_opy_).start()
    def bstack11l11111111_opy_(self, source = bstack1l1l1l1_opy_ (u"ࠩࠪ᱖")):
        with self.lock:
            if not self.queue:
                self.bstack111llllll11_opy_()
                return
            data = self.queue[:self.bstack111llllllll_opy_]
            del self.queue[:self.bstack111llllllll_opy_]
        self.handler(data)
        if source != bstack1l1l1l1_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ᱗"):
            self.bstack111llllll11_opy_()
    def shutdown(self):
        self.bstack11l111111l1_opy_()
        while self.queue:
            self.bstack11l11111111_opy_(source=bstack1l1l1l1_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭᱘"))