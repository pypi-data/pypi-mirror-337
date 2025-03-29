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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack1l1111l1111_opy_, bstack1l11111llll_opy_
import tempfile
import json
bstack11l1llll1ll_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡇࡠࡈࡌࡐࡊࠨ᫑"), None) or os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠣ᫒"))
bstack11ll111l1ll_opy_ = os.path.join(bstack1l1l1l1_opy_ (u"ࠢ࡭ࡱࡪࠦ᫓"), bstack1l1l1l1_opy_ (u"ࠨࡵࡧ࡯࠲ࡩ࡬ࡪ࠯ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠬ᫔"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1l1l1_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ᫕"),
      datefmt=bstack1l1l1l1_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨ᫖"),
      stream=sys.stdout
    )
  return logger
def bstack1llllll11l1_opy_():
  bstack11ll111l111_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤ᫗"), bstack1l1l1l1_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ᫘"))
  return logging.DEBUG if bstack11ll111l111_opy_.lower() == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ᫙") else logging.INFO
def bstack1ll11llll11_opy_():
  global bstack11l1llll1ll_opy_
  if os.path.exists(bstack11l1llll1ll_opy_):
    os.remove(bstack11l1llll1ll_opy_)
  if os.path.exists(bstack11ll111l1ll_opy_):
    os.remove(bstack11ll111l1ll_opy_)
def bstack1llll11l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1ll1l1l_opy_(config, log_level):
  bstack11ll111l1l1_opy_ = log_level
  if bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᫚") in config and config[bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᫛")] in bstack1l1111l1111_opy_:
    bstack11ll111l1l1_opy_ = bstack1l1111l1111_opy_[config[bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫ᫜")]]
  if config.get(bstack1l1l1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ᫝"), False):
    logging.getLogger().setLevel(bstack11ll111l1l1_opy_)
    return bstack11ll111l1l1_opy_
  global bstack11l1llll1ll_opy_
  bstack1llll11l_opy_()
  bstack11l1llllll1_opy_ = logging.Formatter(
    fmt=bstack1l1l1l1_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧ᫞"),
    datefmt=bstack1l1l1l1_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪ᫟"),
  )
  bstack11ll1111ll1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l1llll1ll_opy_)
  file_handler.setFormatter(bstack11l1llllll1_opy_)
  bstack11ll1111ll1_opy_.setFormatter(bstack11l1llllll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11ll1111ll1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1l1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨ᫠"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11ll1111ll1_opy_.setLevel(bstack11ll111l1l1_opy_)
  logging.getLogger().addHandler(bstack11ll1111ll1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11ll111l1l1_opy_
def bstack11ll111l11l_opy_(config):
  try:
    bstack11l1llll1l1_opy_ = set(bstack1l11111llll_opy_)
    bstack11ll1111111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨ᫡")
    with open(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ᫢")) as bstack11ll111ll11_opy_:
      bstack11l1lllllll_opy_ = bstack11ll111ll11_opy_.read()
      bstack11ll1111111_opy_ = re.sub(bstack1l1l1l1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪ᫣"), bstack1l1l1l1_opy_ (u"ࠪࠫ᫤"), bstack11l1lllllll_opy_, flags=re.M)
      bstack11ll1111111_opy_ = re.sub(
        bstack1l1l1l1_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧ᫥") + bstack1l1l1l1_opy_ (u"ࠬࢂࠧ᫦").join(bstack11l1llll1l1_opy_) + bstack1l1l1l1_opy_ (u"࠭ࠩ࠯ࠬࠧࠫ᫧"),
        bstack1l1l1l1_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩ᫨"),
        bstack11ll1111111_opy_, flags=re.M | re.I
      )
    def bstack11ll1111l11_opy_(dic):
      bstack11ll111ll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l1llll1l1_opy_:
          bstack11ll111ll1l_opy_[key] = bstack1l1l1l1_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬ᫩")
        else:
          if isinstance(value, dict):
            bstack11ll111ll1l_opy_[key] = bstack11ll1111l11_opy_(value)
          else:
            bstack11ll111ll1l_opy_[key] = value
      return bstack11ll111ll1l_opy_
    bstack11ll111ll1l_opy_ = bstack11ll1111l11_opy_(config)
    return {
      bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ᫪"): bstack11ll1111111_opy_,
      bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭᫫"): json.dumps(bstack11ll111ll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack11ll11111ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠫࡱࡵࡧࠨ᫬"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l1lllll11_opy_ = os.path.join(log_dir, bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭᫭"))
  if not os.path.exists(bstack11l1lllll11_opy_):
    bstack11l1llll11l_opy_ = {
      bstack1l1l1l1_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢ᫮"): str(inipath),
      bstack1l1l1l1_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤ᫯"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧ᫰")), bstack1l1l1l1_opy_ (u"ࠩࡺࠫ᫱")) as bstack11ll11111l1_opy_:
      bstack11ll11111l1_opy_.write(json.dumps(bstack11l1llll11l_opy_))
def bstack11l1lllll1l_opy_():
  try:
    bstack11l1lllll11_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠪࡰࡴ࡭ࠧ᫲"), bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ᫳"))
    if os.path.exists(bstack11l1lllll11_opy_):
      with open(bstack11l1lllll11_opy_, bstack1l1l1l1_opy_ (u"ࠬࡸࠧ᫴")) as bstack11ll11111l1_opy_:
        bstack11ll111lll1_opy_ = json.load(bstack11ll11111l1_opy_)
      return bstack11ll111lll1_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧ᫵"), bstack1l1l1l1_opy_ (u"ࠧࠨ᫶")), bstack11ll111lll1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪ᫷"), bstack1l1l1l1_opy_ (u"ࠩࠪ᫸"))
  except:
    pass
  return None, None
def bstack11l1llll111_opy_():
  try:
    bstack11l1lllll11_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠪࡰࡴ࡭ࠧ᫹"), bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪ᫺"))
    if os.path.exists(bstack11l1lllll11_opy_):
      os.remove(bstack11l1lllll11_opy_)
  except:
    pass
def bstack1l11l1l1_opy_(config):
  from bstack_utils.helper import bstack1l1l1111l_opy_
  global bstack11l1llll1ll_opy_
  try:
    if config.get(bstack1l1l1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧ᫻"), False):
      return
    uuid = os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᫼")) if os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᫽")) else bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥ᫾"))
    if not uuid or uuid == bstack1l1l1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ᫿"):
      return
    bstack11ll111111l_opy_ = [bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭ᬀ"), bstack1l1l1l1_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬᬁ"), bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭ᬂ"), bstack11l1llll1ll_opy_, bstack11ll111l1ll_opy_]
    bstack11ll1111l1l_opy_, root_path = bstack11l1lllll1l_opy_()
    if bstack11ll1111l1l_opy_ != None:
      bstack11ll111111l_opy_.append(bstack11ll1111l1l_opy_)
    if root_path != None:
      bstack11ll111111l_opy_.append(os.path.join(root_path, bstack1l1l1l1_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫᬃ")))
    bstack1llll11l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭ᬄ") + uuid + bstack1l1l1l1_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩᬅ"))
    with tarfile.open(output_file, bstack1l1l1l1_opy_ (u"ࠤࡺ࠾࡬ࢀࠢᬆ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11ll111111l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11ll111l11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11ll1111lll_opy_ = data.encode()
        tarinfo.size = len(bstack11ll1111lll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11ll1111lll_opy_))
    bstack1ll1l1l111_opy_ = MultipartEncoder(
      fields= {
        bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᬇ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1l1l1_opy_ (u"ࠫࡷࡨࠧᬈ")), bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪᬉ")),
        bstack1l1l1l1_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᬊ"): uuid
      }
    )
    response = requests.post(
      bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᬋ"),
      data=bstack1ll1l1l111_opy_,
      headers={bstack1l1l1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᬌ"): bstack1ll1l1l111_opy_.content_type},
      auth=(config[bstack1l1l1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᬍ")], config[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᬎ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᬏ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᬐ") + str(e))
  finally:
    try:
      bstack1ll11llll11_opy_()
      bstack11l1llll111_opy_()
    except:
      pass