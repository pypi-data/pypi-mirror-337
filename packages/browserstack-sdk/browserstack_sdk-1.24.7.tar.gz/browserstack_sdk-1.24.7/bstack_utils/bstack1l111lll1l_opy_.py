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
import json
class bstack1l111ll11ll_opy_(object):
  bstack1l11lll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠪࢂࠬᔻ")), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᔼ"))
  bstack1l111ll111l_opy_ = os.path.join(bstack1l11lll1ll_opy_, bstack1l1l1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬᔽ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11l1llll_opy_ = None
  bstack1l111l11ll_opy_ = None
  bstack1l11l11lll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨᔾ")):
      cls.instance = super(bstack1l111ll11ll_opy_, cls).__new__(cls)
      cls.instance.bstack1l111ll11l1_opy_()
    return cls.instance
  def bstack1l111ll11l1_opy_(self):
    try:
      with open(self.bstack1l111ll111l_opy_, bstack1l1l1l1_opy_ (u"ࠧࡳࠩᔿ")) as bstack1l111ll1l_opy_:
        bstack1l111ll1111_opy_ = bstack1l111ll1l_opy_.read()
        data = json.loads(bstack1l111ll1111_opy_)
        if bstack1l1l1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᕀ") in data:
          self.bstack1l11l1111ll_opy_(data[bstack1l1l1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᕁ")])
        if bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᕂ") in data:
          self.bstack1l11l11ll11_opy_(data[bstack1l1l1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᕃ")])
    except:
      pass
  def bstack1l11l11ll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1l1l1l1_opy_ (u"ࠬࡹࡣࡢࡰࠪᕄ")]
      self.bstack1l11l1llll_opy_ = scripts[bstack1l1l1l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᕅ")]
      self.bstack1l111l11ll_opy_ = scripts[bstack1l1l1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᕆ")]
      self.bstack1l11l11lll1_opy_ = scripts[bstack1l1l1l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᕇ")]
  def bstack1l11l1111ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack1l111ll111l_opy_, bstack1l1l1l1_opy_ (u"ࠩࡺࠫᕈ")) as file:
        json.dump({
          bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᕉ"): self.commands_to_wrap,
          bstack1l1l1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᕊ"): {
            bstack1l1l1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᕋ"): self.perform_scan,
            bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᕌ"): self.bstack1l11l1llll_opy_,
            bstack1l1l1l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᕍ"): self.bstack1l111l11ll_opy_,
            bstack1l1l1l1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᕎ"): self.bstack1l11l11lll1_opy_
          }
        }, file)
    except:
      pass
  def bstack11lllll11_opy_(self, bstack1ll1ll1ll11_opy_):
    try:
      return any(command.get(bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᕏ")) == bstack1ll1ll1ll11_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l111lll1l_opy_ = bstack1l111ll11ll_opy_()