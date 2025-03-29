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
from uuid import uuid4
from bstack_utils.helper import bstack1lll11llll_opy_, bstack11lll11l1ll_opy_
from bstack_utils.bstack1l1ll1lll1_opy_ import bstack11l111l1111_opy_
class bstack111lll1lll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111llll111l_opy_=None, bstack111lll11lll_opy_=True, bstack1l1l11111l1_opy_=None, bstack1l1ll11111_opy_=None, result=None, duration=None, bstack11l111l11l_opy_=None, meta={}):
        self.bstack11l111l11l_opy_ = bstack11l111l11l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111lll11lll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111llll111l_opy_ = bstack111llll111l_opy_
        self.bstack1l1l11111l1_opy_ = bstack1l1l11111l1_opy_
        self.bstack1l1ll11111_opy_ = bstack1l1ll11111_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111ll11l1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1l11111_opy_(self, meta):
        self.meta = meta
    def bstack11l1l11lll_opy_(self, hooks):
        self.hooks = hooks
    def bstack111lll1lll1_opy_(self):
        bstack111lll1ll1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭᲏"): bstack111lll1ll1l_opy_,
            bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭Ა"): bstack111lll1ll1l_opy_,
            bstack1l1l1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᲑ"): bstack111lll1ll1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᲒ") + key)
            setattr(self, key, val)
    def bstack111llll11l1_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᲓ"): self.name,
            bstack1l1l1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭Ე"): {
                bstack1l1l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᲕ"): bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᲖ"),
                bstack1l1l1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩᲗ"): self.code
            },
            bstack1l1l1l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᲘ"): self.scope,
            bstack1l1l1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫᲙ"): self.tags,
            bstack1l1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᲚ"): self.framework,
            bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᲛ"): self.started_at
        }
    def bstack111lll1llll_opy_(self):
        return {
         bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡹࡧࠧᲜ"): self.meta
        }
    def bstack111lll111ll_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭Ო"): {
                bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᲞ"): self.bstack111llll111l_opy_
            }
        }
    def bstack111lll1l1l1_opy_(self, bstack111lll11l11_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࠨᲟ")] == bstack111lll11l11_opy_, self.meta[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᲠ")]), None)
        step.update(details)
    def bstack1lll1l1111_opy_(self, bstack111lll11l11_opy_):
        step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠧࡪࡦࠪᲡ")] == bstack111lll11l11_opy_, self.meta[bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᲢ")]), None)
        step.update({
            bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Უ"): bstack1lll11llll_opy_()
        })
    def bstack11l11l11ll_opy_(self, bstack111lll11l11_opy_, result, duration=None):
        bstack1l1l11111l1_opy_ = bstack1lll11llll_opy_()
        if bstack111lll11l11_opy_ is not None and self.meta.get(bstack1l1l1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᲤ")):
            step = next(filter(lambda st: st[bstack1l1l1l1_opy_ (u"ࠫ࡮ࡪࠧᲥ")] == bstack111lll11l11_opy_, self.meta[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᲦ")]), None)
            step.update({
                bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᲧ"): bstack1l1l11111l1_opy_,
                bstack1l1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᲨ"): duration if duration else bstack11lll11l1ll_opy_(step[bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᲩ")], bstack1l1l11111l1_opy_),
                bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᲪ"): result.result,
                bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᲫ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111lll11l1l_opy_):
        if self.meta.get(bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᲬ")):
            self.meta[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᲭ")].append(bstack111lll11l1l_opy_)
        else:
            self.meta[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᲮ")] = [ bstack111lll11l1l_opy_ ]
    def bstack111llll11ll_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᲯ"): self.bstack111ll11l1l_opy_(),
            **self.bstack111llll11l1_opy_(),
            **self.bstack111lll1lll1_opy_(),
            **self.bstack111lll1llll_opy_()
        }
    def bstack111lll111l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭Ჰ"): self.bstack1l1l11111l1_opy_,
            bstack1l1l1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᲱ"): self.duration,
            bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᲲ"): self.result.result
        }
        if data[bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᲳ")] == bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᲴ"):
            data[bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᲵ")] = self.result.bstack111l11l1ll_opy_()
            data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᲶ")] = [{bstack1l1l1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᲷ"): self.result.bstack11lll1ll11l_opy_()}]
        return data
    def bstack111llll1111_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᲸ"): self.bstack111ll11l1l_opy_(),
            **self.bstack111llll11l1_opy_(),
            **self.bstack111lll1lll1_opy_(),
            **self.bstack111lll111l1_opy_(),
            **self.bstack111lll1llll_opy_()
        }
    def bstack11l111lll1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l1l1_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᲹ") in event:
            return self.bstack111llll11ll_opy_()
        elif bstack1l1l1l1_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ჺ") in event:
            return self.bstack111llll1111_opy_()
    def bstack11l111l1ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l1l11111l1_opy_ = time if time else bstack1lll11llll_opy_()
        self.duration = duration if duration else bstack11lll11l1ll_opy_(self.started_at, self.bstack1l1l11111l1_opy_)
        if result:
            self.result = result
class bstack11l11l1ll1_opy_(bstack111lll1lll_opy_):
    def __init__(self, hooks=[], bstack11l11l1l11_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l11l1l11_opy_ = bstack11l11l1l11_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11111_opy_=bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ᲻"))
    @classmethod
    def bstack111lll1ll11_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩ᲼"): id(step),
                bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡻࡸࠬᲽ"): step.name,
                bstack1l1l1l1_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᲾ"): step.keyword,
            })
        return bstack11l11l1ll1_opy_(
            **kwargs,
            meta={
                bstack1l1l1l1_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᲿ"): {
                    bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ᳀"): feature.name,
                    bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡴࡩࠩ᳁"): feature.filename,
                    bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᳂"): feature.description
                },
                bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨ᳃"): {
                    bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᳄"): scenario.name
                },
                bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧ᳅"): steps,
                bstack1l1l1l1_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫ᳆"): bstack11l111l1111_opy_(test)
            }
        )
    def bstack111lll1l111_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᳇"): self.hooks
        }
    def bstack111lll1l11l_opy_(self):
        if self.bstack11l11l1l11_opy_:
            return {
                bstack1l1l1l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ᳈"): self.bstack11l11l1l11_opy_
            }
        return {}
    def bstack111llll1111_opy_(self):
        return {
            **super().bstack111llll1111_opy_(),
            **self.bstack111lll1l111_opy_()
        }
    def bstack111llll11ll_opy_(self):
        return {
            **super().bstack111llll11ll_opy_(),
            **self.bstack111lll1l11l_opy_()
        }
    def bstack11l111l1ll_opy_(self):
        return bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ᳉")
class bstack11l11llll1_opy_(bstack111lll1lll_opy_):
    def __init__(self, hook_type, *args,bstack11l11l1l11_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack111lll1l1ll_opy_ = None
        self.bstack11l11l1l11_opy_ = bstack11l11l1l11_opy_
        super().__init__(*args, **kwargs, bstack1l1ll11111_opy_=bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ᳊"))
    def bstack111ll11ll1_opy_(self):
        return self.hook_type
    def bstack111lll11ll1_opy_(self):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ᳋"): self.hook_type
        }
    def bstack111llll1111_opy_(self):
        return {
            **super().bstack111llll1111_opy_(),
            **self.bstack111lll11ll1_opy_()
        }
    def bstack111llll11ll_opy_(self):
        return {
            **super().bstack111llll11ll_opy_(),
            bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭᳌"): self.bstack111lll1l1ll_opy_,
            **self.bstack111lll11ll1_opy_()
        }
    def bstack11l111l1ll_opy_(self):
        return bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫ᳍")
    def bstack11l1l111ll_opy_(self, bstack111lll1l1ll_opy_):
        self.bstack111lll1l1ll_opy_ = bstack111lll1l1ll_opy_