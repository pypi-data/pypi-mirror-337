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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11ll1llll_opy_, bstack1111l1ll1_opy_
from bstack_utils.measure import measure
class bstack1ll1111l1l_opy_:
  working_dir = os.getcwd()
  bstack11ll1lll1l_opy_ = False
  config = {}
  bstack11ll1l11111_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧ᭞")
  binary_path = bstack1l1l1l1_opy_ (u"ࠧࠨ᭟")
  bstack11l11lll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠩ᭠")
  bstack11l1ll11l1_opy_ = False
  bstack11l1l1llll1_opy_ = None
  bstack11l1ll1lll1_opy_ = {}
  bstack11l1l1ll1ll_opy_ = 300
  bstack11l1ll11lll_opy_ = False
  logger = None
  bstack11l1l111111_opy_ = False
  bstack11ll111111_opy_ = False
  percy_build_id = None
  bstack11l1l1l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠩࠪ᭡")
  bstack11l1l11llll_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ᭢") : 1,
    bstack1l1l1l1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ᭣") : 2,
    bstack1l1l1l1_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ᭤") : 3,
    bstack1l1l1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭᭥") : 4
  }
  def __init__(self) -> None: pass
  def bstack11l1ll1ll11_opy_(self):
    bstack11l1ll111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨ᭦")
    bstack11l11llllll_opy_ = sys.platform
    bstack11l1lll11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᭧")
    if re.match(bstack1l1l1l1_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤ᭨"), bstack11l11llllll_opy_) != None:
      bstack11l1ll111l1_opy_ = bstack1l11111ll1l_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦ᭩")
      self.bstack11l1l1l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡲࡧࡣࠨ᭪")
    elif re.match(bstack1l1l1l1_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥ᭫"), bstack11l11llllll_opy_) != None:
      bstack11l1ll111l1_opy_ = bstack1l11111ll1l_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶ᭬ࠢ")
      bstack11l1lll11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥ᭭")
      self.bstack11l1l1l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡹ࡬ࡲࠬ᭮")
    else:
      bstack11l1ll111l1_opy_ = bstack1l11111ll1l_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧ᭯")
      self.bstack11l1l1l11ll_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ᭰")
    return bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_
  def bstack11l11ll1l11_opy_(self):
    try:
      bstack11l11lll1l1_opy_ = [os.path.join(expanduser(bstack1l1l1l1_opy_ (u"ࠦࢃࠨ᭱")), bstack1l1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᭲")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l11lll1l1_opy_:
        if(self.bstack11l1ll111ll_opy_(path)):
          return path
      raise bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥ᭳")
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤ᭴").format(e))
  def bstack11l1ll111ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11l1ll11111_opy_(self, bstack11l1l111l11_opy_):
    return os.path.join(bstack11l1l111l11_opy_, self.bstack11ll1l11111_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢ᭵"))
  def bstack11l11lll11l_opy_(self, bstack11l1l111l11_opy_, bstack11l11ll1ll1_opy_):
    if not bstack11l11ll1ll1_opy_: return
    try:
      bstack11l1l11l1l1_opy_ = self.bstack11l1ll11111_opy_(bstack11l1l111l11_opy_)
      with open(bstack11l1l11l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠤࡺࠦ᭶")) as f:
        f.write(bstack11l11ll1ll1_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢ᭷"))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᭸").format(e))
  def bstack11l1l11ll11_opy_(self, bstack11l1l111l11_opy_):
    try:
      bstack11l1l11l1l1_opy_ = self.bstack11l1ll11111_opy_(bstack11l1l111l11_opy_)
      if os.path.exists(bstack11l1l11l1l1_opy_):
        with open(bstack11l1l11l1l1_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࠢ᭹")) as f:
          bstack11l11ll1ll1_opy_ = f.read().strip()
          return bstack11l11ll1ll1_opy_ if bstack11l11ll1ll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ᭺").format(e))
  def bstack11l1l1lll11_opy_(self, bstack11l1l111l11_opy_, bstack11l1ll111l1_opy_):
    bstack11l1l11lll1_opy_ = self.bstack11l1l11ll11_opy_(bstack11l1l111l11_opy_)
    if bstack11l1l11lll1_opy_:
      try:
        bstack11l1l1lllll_opy_ = self.bstack11l1lll111l_opy_(bstack11l1l11lll1_opy_, bstack11l1ll111l1_opy_)
        if not bstack11l1l1lllll_opy_:
          self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤ᭻"))
          return True
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢ᭼"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ᭽").format(e))
    return False
  def bstack11l1lll111l_opy_(self, bstack11l1l11lll1_opy_, bstack11l1ll111l1_opy_):
    try:
      headers = {
        bstack1l1l1l1_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥ᭾"): bstack11l1l11lll1_opy_
      }
      response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡌࡋࡔࠨ᭿"), bstack11l1ll111l1_opy_, {}, {bstack1l1l1l1_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨᮀ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣᮁ").format(e))
  @measure(event_name=EVENTS.bstack1l1111l111l_opy_, stage=STAGE.bstack1llll1ll11_opy_)
  def bstack11l11llll11_opy_(self, bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_):
    try:
      bstack11l1l11ll1l_opy_ = self.bstack11l11ll1l11_opy_()
      bstack11l11lll111_opy_ = os.path.join(bstack11l1l11ll1l_opy_, bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪᮂ"))
      bstack11l1ll1l1l1_opy_ = os.path.join(bstack11l1l11ll1l_opy_, bstack11l1lll11l1_opy_)
      if self.bstack11l1l1lll11_opy_(bstack11l1l11ll1l_opy_, bstack11l1ll111l1_opy_):
        if os.path.exists(bstack11l1ll1l1l1_opy_):
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᮃ").format(bstack11l1ll1l1l1_opy_))
          return bstack11l1ll1l1l1_opy_
        if os.path.exists(bstack11l11lll111_opy_):
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢᮄ").format(bstack11l11lll111_opy_))
          return self.bstack11l1ll1ll1l_opy_(bstack11l11lll111_opy_, bstack11l1lll11l1_opy_)
      self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣᮅ").format(bstack11l1ll111l1_opy_))
      response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡌࡋࡔࠨᮆ"), bstack11l1ll111l1_opy_, {}, {})
      if response.status_code == 200:
        bstack11l1ll1llll_opy_ = response.headers.get(bstack1l1l1l1_opy_ (u"ࠧࡋࡔࡢࡩࠥᮇ"), bstack1l1l1l1_opy_ (u"ࠨࠢᮈ"))
        if bstack11l1ll1llll_opy_:
          self.bstack11l11lll11l_opy_(bstack11l1l11ll1l_opy_, bstack11l1ll1llll_opy_)
        with open(bstack11l11lll111_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࡤࠪᮉ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᮊ").format(bstack11l11lll111_opy_))
        return self.bstack11l1ll1ll1l_opy_(bstack11l11lll111_opy_, bstack11l1lll11l1_opy_)
      else:
        raise(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᮋ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᮌ").format(e))
  def bstack11l1ll1l111_opy_(self, bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_):
    try:
      retry = 2
      bstack11l1ll1l1l1_opy_ = None
      bstack11l1ll1l11l_opy_ = False
      while retry > 0:
        bstack11l1ll1l1l1_opy_ = self.bstack11l11llll11_opy_(bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_)
        bstack11l1ll1l11l_opy_ = self.bstack11l1l1lll1l_opy_(bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_, bstack11l1ll1l1l1_opy_)
        if bstack11l1ll1l11l_opy_:
          break
        retry -= 1
      return bstack11l1ll1l1l1_opy_, bstack11l1ll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᮍ").format(e))
    return bstack11l1ll1l1l1_opy_, False
  def bstack11l1l1lll1l_opy_(self, bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_, bstack11l1ll1l1l1_opy_, bstack11l1ll1l1ll_opy_ = 0):
    if bstack11l1ll1l1ll_opy_ > 1:
      return False
    if bstack11l1ll1l1l1_opy_ == None or os.path.exists(bstack11l1ll1l1l1_opy_) == False:
      self.logger.warn(bstack1l1l1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᮎ"))
      return False
    bstack11l11ll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᮏ")
    command = bstack1l1l1l1_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᮐ").format(bstack11l1ll1l1l1_opy_)
    bstack11l1l1l11l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11l11ll1l1l_opy_, bstack11l1l1l11l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᮑ"))
      return False
  def bstack11l1ll1ll1l_opy_(self, bstack11l11lll111_opy_, bstack11l1lll11l1_opy_):
    try:
      working_dir = os.path.dirname(bstack11l11lll111_opy_)
      shutil.unpack_archive(bstack11l11lll111_opy_, working_dir)
      bstack11l1ll1l1l1_opy_ = os.path.join(working_dir, bstack11l1lll11l1_opy_)
      os.chmod(bstack11l1ll1l1l1_opy_, 0o755)
      return bstack11l1ll1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᮒ"))
  def bstack11l11ll11ll_opy_(self):
    try:
      bstack11l1ll11ll1_opy_ = self.config.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᮓ"))
      bstack11l11ll11ll_opy_ = bstack11l1ll11ll1_opy_ or (bstack11l1ll11ll1_opy_ is None and self.bstack11ll1lll1l_opy_)
      if not bstack11l11ll11ll_opy_ or self.config.get(bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᮔ"), None) not in bstack1l1111l1lll_opy_:
        return False
      self.bstack11l1ll11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᮕ").format(e))
  def bstack11l1ll11l11_opy_(self):
    try:
      bstack11l1ll11l11_opy_ = self.percy_capture_mode
      return bstack11l1ll11l11_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᮖ").format(e))
  def init(self, bstack11ll1lll1l_opy_, config, logger):
    self.bstack11ll1lll1l_opy_ = bstack11ll1lll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11l11ll11ll_opy_():
      return
    self.bstack11l1ll1lll1_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᮗ"), {})
    self.percy_capture_mode = config.get(bstack1l1l1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᮘ"))
    try:
      bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_ = self.bstack11l1ll1ll11_opy_()
      self.bstack11ll1l11111_opy_ = bstack11l1lll11l1_opy_
      bstack11l1ll1l1l1_opy_, bstack11l1ll1l11l_opy_ = self.bstack11l1ll1l111_opy_(bstack11l1ll111l1_opy_, bstack11l1lll11l1_opy_)
      if bstack11l1ll1l11l_opy_:
        self.binary_path = bstack11l1ll1l1l1_opy_
        thread = Thread(target=self.bstack11l1l1l1l1l_opy_)
        thread.start()
      else:
        self.bstack11l1l111111_opy_ = True
        self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᮙ").format(bstack11l1ll1l1l1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᮚ").format(e))
  def bstack11l1l11l1ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡧࠨᮛ"), bstack1l1l1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᮜ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᮝ").format(logfile))
      self.bstack11l11lll1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᮞ").format(e))
  @measure(event_name=EVENTS.bstack1l111111l11_opy_, stage=STAGE.bstack1llll1ll11_opy_)
  def bstack11l1l1l1l1l_opy_(self):
    bstack11l1l1ll111_opy_ = self.bstack11l1lll1111_opy_()
    if bstack11l1l1ll111_opy_ == None:
      self.bstack11l1l111111_opy_ = True
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᮟ"))
      return False
    command_args = [bstack1l1l1l1_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᮠ") if self.bstack11ll1lll1l_opy_ else bstack1l1l1l1_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᮡ")]
    bstack11l1lllll11_opy_ = self.bstack11l1ll11l1l_opy_()
    if bstack11l1lllll11_opy_ != None:
      command_args.append(bstack1l1l1l1_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᮢ").format(bstack11l1lllll11_opy_))
    env = os.environ.copy()
    env[bstack1l1l1l1_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᮣ")] = bstack11l1l1ll111_opy_
    env[bstack1l1l1l1_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᮤ")] = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᮥ"), bstack1l1l1l1_opy_ (u"ࠨࠩᮦ"))
    bstack11l1l11l111_opy_ = [self.binary_path]
    self.bstack11l1l11l1ll_opy_()
    self.bstack11l1l1llll1_opy_ = self.bstack11l1l1l1l11_opy_(bstack11l1l11l111_opy_ + command_args, env)
    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᮧ"))
    bstack11l1ll1l1ll_opy_ = 0
    while self.bstack11l1l1llll1_opy_.poll() == None:
      bstack11l1l1l111l_opy_ = self.bstack11l11llll1l_opy_()
      if bstack11l1l1l111l_opy_:
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᮨ"))
        self.bstack11l1ll11lll_opy_ = True
        return True
      bstack11l1ll1l1ll_opy_ += 1
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᮩ").format(bstack11l1ll1l1ll_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵ᮪ࠥ").format(bstack11l1ll1l1ll_opy_))
    self.bstack11l1l111111_opy_ = True
    return False
  def bstack11l11llll1l_opy_(self, bstack11l1ll1l1ll_opy_ = 0):
    if bstack11l1ll1l1ll_opy_ > 10:
      return False
    try:
      bstack11l1l1111l1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ᮫࠭"), bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᮬ"))
      bstack11l1l111lll_opy_ = bstack11l1l1111l1_opy_ + bstack1l111l1111l_opy_
      response = requests.get(bstack11l1l111lll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᮭ"), {}).get(bstack1l1l1l1_opy_ (u"ࠩ࡬ࡨࠬᮮ"), None)
      return True
    except:
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᮯ"))
      return False
  def bstack11l1lll1111_opy_(self):
    bstack11l11ll1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰࠨ᮰") if self.bstack11ll1lll1l_opy_ else bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ᮱")
    bstack11l1l1ll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤ᮲") if self.config.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭᮳")) is None else True
    bstack11ll1lllll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤ᮴").format(self.config[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᮵")], bstack11l11ll1lll_opy_, bstack11l1l1ll11l_opy_)
    if self.percy_capture_mode:
      bstack11ll1lllll1_opy_ += bstack1l1l1l1_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧ᮶").format(self.percy_capture_mode)
    uri = bstack11ll1llll_opy_(bstack11ll1lllll1_opy_)
    try:
      response = bstack1111l1ll1_opy_(bstack1l1l1l1_opy_ (u"ࠫࡌࡋࡔࠨ᮷"), uri, {}, {bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪ᮸"): (self.config[bstack1l1l1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ᮹")], self.config[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᮺ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l1ll11l1_opy_ = data.get(bstack1l1l1l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᮻ"))
        self.percy_capture_mode = data.get(bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᮼ"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᮽ")] = str(self.bstack11l1ll11l1_opy_)
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᮾ")] = str(self.percy_capture_mode)
        if bstack11l1l1ll11l_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᮿ") and str(self.bstack11l1ll11l1_opy_).lower() == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᯀ"):
          self.bstack11ll111111_opy_ = True
        if bstack1l1l1l1_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᯁ") in data:
          return data[bstack1l1l1l1_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᯂ")]
        else:
          raise bstack1l1l1l1_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᯃ").format(data)
      else:
        raise bstack1l1l1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᯄ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᯅ").format(e))
  def bstack11l1ll11l1l_opy_(self):
    bstack11l1l1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᯆ"))
    try:
      if bstack1l1l1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᯇ") not in self.bstack11l1ll1lll1_opy_:
        self.bstack11l1ll1lll1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᯈ")] = 2
      with open(bstack11l1l1ll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡹࠪᯉ")) as fp:
        json.dump(self.bstack11l1ll1lll1_opy_, fp)
      return bstack11l1l1ll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᯊ").format(e))
  def bstack11l1l1l1l11_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11l1l1l11ll_opy_ == bstack1l1l1l1_opy_ (u"ࠪࡻ࡮ࡴࠧᯋ"):
        bstack11l1l1l1lll_opy_ = [bstack1l1l1l1_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᯌ"), bstack1l1l1l1_opy_ (u"ࠬ࠵ࡣࠨᯍ")]
        cmd = bstack11l1l1l1lll_opy_ + cmd
      cmd = bstack1l1l1l1_opy_ (u"࠭ࠠࠨᯎ").join(cmd)
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᯏ").format(cmd))
      with open(self.bstack11l11lll1ll_opy_, bstack1l1l1l1_opy_ (u"ࠣࡣࠥᯐ")) as bstack11l1l1111ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11l1l1111ll_opy_, text=True, stderr=bstack11l1l1111ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11l1l111111_opy_ = True
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᯑ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11l1ll11lll_opy_:
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᯒ"))
        cmd = [self.binary_path, bstack1l1l1l1_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᯓ")]
        self.bstack11l1l1l1l11_opy_(cmd)
        self.bstack11l1ll11lll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᯔ").format(cmd, e))
  def bstack1lll1l1ll_opy_(self):
    if not self.bstack11l1ll11l1_opy_:
      return
    try:
      bstack11l1l1l1ll1_opy_ = 0
      while not self.bstack11l1ll11lll_opy_ and bstack11l1l1l1ll1_opy_ < self.bstack11l1l1ll1ll_opy_:
        if self.bstack11l1l111111_opy_:
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᯕ"))
          return
        time.sleep(1)
        bstack11l1l1l1ll1_opy_ += 1
      os.environ[bstack1l1l1l1_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᯖ")] = str(self.bstack11l11lllll1_opy_())
      self.logger.info(bstack1l1l1l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᯗ"))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᯘ").format(e))
  def bstack11l11lllll1_opy_(self):
    if self.bstack11ll1lll1l_opy_:
      return
    try:
      bstack11l1l1l1111_opy_ = [platform[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᯙ")].lower() for platform in self.config.get(bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᯚ"), [])]
      bstack11l1l111l1l_opy_ = sys.maxsize
      bstack11l1ll1111l_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ᯛ")
      for browser in bstack11l1l1l1111_opy_:
        if browser in self.bstack11l1l11llll_opy_:
          bstack11l1l111ll1_opy_ = self.bstack11l1l11llll_opy_[browser]
        if bstack11l1l111ll1_opy_ < bstack11l1l111l1l_opy_:
          bstack11l1l111l1l_opy_ = bstack11l1l111ll1_opy_
          bstack11l1ll1111l_opy_ = browser
      return bstack11l1ll1111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᯜ").format(e))
  @classmethod
  def bstack1lllll1l1_opy_(self):
    return os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᯝ"), bstack1l1l1l1_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᯞ")).lower()
  @classmethod
  def bstack11ll1l1ll_opy_(self):
    return os.getenv(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᯟ"), bstack1l1l1l1_opy_ (u"ࠪࠫᯠ"))
  @classmethod
  def bstack1ll111111l1_opy_(cls, value):
    cls.bstack11ll111111_opy_ = value
  @classmethod
  def bstack11l1l11l11l_opy_(cls):
    return cls.bstack11ll111111_opy_
  @classmethod
  def bstack1l1llllll1l_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack11l1l11111l_opy_(cls):
    return cls.percy_build_id