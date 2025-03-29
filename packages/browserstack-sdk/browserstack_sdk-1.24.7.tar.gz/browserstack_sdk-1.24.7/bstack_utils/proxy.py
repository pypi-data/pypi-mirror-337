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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1lll1l1l_opy_
bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
def bstack11l111ll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11l111ll11l_opy_(bstack11l111l1ll1_opy_, bstack11l111ll1ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11l111l1ll1_opy_):
        with open(bstack11l111l1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11l111ll111_opy_(bstack11l111l1ll1_opy_):
        pac = get_pac(url=bstack11l111l1ll1_opy_)
    else:
        raise Exception(bstack1l1l1l1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩ᯻").format(bstack11l111l1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l1l1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ᯼"), 80))
        bstack11l111l1lll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11l111l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬ᯽")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11l111ll1ll_opy_, bstack11l111l1lll_opy_)
    return proxy_url
def bstack1ll11l1l_opy_(config):
    return bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᯾") in config or bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᯿") in config
def bstack11ll1111ll_opy_(config):
    if not bstack1ll11l1l_opy_(config):
        return
    if config.get(bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᰀ")):
        return config.get(bstack1l1l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᰁ"))
    if config.get(bstack1l1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᰂ")):
        return config.get(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᰃ"))
def bstack1l1lll1111_opy_(config, bstack11l111ll1ll_opy_):
    proxy = bstack11ll1111ll_opy_(config)
    proxies = {}
    if config.get(bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᰄ")) or config.get(bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᰅ")):
        if proxy.endswith(bstack1l1l1l1_opy_ (u"࠭࠮ࡱࡣࡦࠫᰆ")):
            proxies = bstack1l111lll1_opy_(proxy, bstack11l111ll1ll_opy_)
        else:
            proxies = {
                bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᰇ"): proxy
            }
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᰈ"), proxies)
    return proxies
def bstack1l111lll1_opy_(bstack11l111l1ll1_opy_, bstack11l111ll1ll_opy_):
    proxies = {}
    global bstack11l111ll1l1_opy_
    if bstack1l1l1l1_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᰉ") in globals():
        return bstack11l111ll1l1_opy_
    try:
        proxy = bstack11l111ll11l_opy_(bstack11l111l1ll1_opy_, bstack11l111ll1ll_opy_)
        if bstack1l1l1l1_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᰊ") in proxy:
            proxies = {}
        elif bstack1l1l1l1_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᰋ") in proxy or bstack1l1l1l1_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᰌ") in proxy or bstack1l1l1l1_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᰍ") in proxy:
            bstack11l111l1l1l_opy_ = proxy.split(bstack1l1l1l1_opy_ (u"ࠢࠡࠤᰎ"))
            if bstack1l1l1l1_opy_ (u"ࠣ࠼࠲࠳ࠧᰏ") in bstack1l1l1l1_opy_ (u"ࠤࠥᰐ").join(bstack11l111l1l1l_opy_[1:]):
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᰑ"): bstack1l1l1l1_opy_ (u"ࠦࠧᰒ").join(bstack11l111l1l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᰓ"): str(bstack11l111l1l1l_opy_[0]).lower() + bstack1l1l1l1_opy_ (u"ࠨ࠺࠰࠱ࠥᰔ") + bstack1l1l1l1_opy_ (u"ࠢࠣᰕ").join(bstack11l111l1l1l_opy_[1:])
                }
        elif bstack1l1l1l1_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᰖ") in proxy:
            bstack11l111l1l1l_opy_ = proxy.split(bstack1l1l1l1_opy_ (u"ࠤࠣࠦᰗ"))
            if bstack1l1l1l1_opy_ (u"ࠥ࠾࠴࠵ࠢᰘ") in bstack1l1l1l1_opy_ (u"ࠦࠧᰙ").join(bstack11l111l1l1l_opy_[1:]):
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᰚ"): bstack1l1l1l1_opy_ (u"ࠨࠢᰛ").join(bstack11l111l1l1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᰜ"): bstack1l1l1l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᰝ") + bstack1l1l1l1_opy_ (u"ࠤࠥᰞ").join(bstack11l111l1l1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᰟ"): proxy
            }
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᰠ"), bstack11l1lll1l1l_opy_.format(bstack11l111l1ll1_opy_, str(e)))
    bstack11l111ll1l1_opy_ = proxies
    return proxies