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
import re
from bstack_utils.bstack1l11l1ll1_opy_ import bstack11l11111lll_opy_
def bstack11l1111l1l1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰡ")):
        return bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᰢ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰣ")):
        return bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᰤ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰥ")):
        return bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᰦ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᰧ")):
        return bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᰨ")
def bstack11l1111l111_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᰩ"), fixture_name))
def bstack11l111l11l1_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᰪ"), fixture_name))
def bstack11l111l111l_opy_(fixture_name):
    return bool(re.match(bstack1l1l1l1_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᰫ"), fixture_name))
def bstack11l1111llll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰬ")):
        return bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᰭ"), bstack1l1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᰮ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰯ")):
        return bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᰰ"), bstack1l1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᰱ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᰲ")):
        return bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᰳ"), bstack1l1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᰴ")
    elif fixture_name.startswith(bstack1l1l1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰵ")):
        return bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᰶ"), bstack1l1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍ᰷ࠩ")
    return None, None
def bstack11l111l11ll_opy_(hook_name):
    if hook_name in [bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᰸"), bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ᰹")]:
        return hook_name.capitalize()
    return hook_name
def bstack11l1111l11l_opy_(hook_name):
    if hook_name in [bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪ᰺"), bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᰻")]:
        return bstack1l1l1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ᰼")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ᰽"), bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫ᰾")]:
        return bstack1l1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ᰿")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ᱀"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ᱁")]:
        return bstack1l1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ᱂")
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᱃"), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭᱄")]:
        return bstack1l1l1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ᱅")
    return hook_name
def bstack11l1111l1ll_opy_(node, scenario):
    if hasattr(node, bstack1l1l1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩ᱆")):
        parts = node.nodeid.rsplit(bstack1l1l1l1_opy_ (u"ࠣ࡝ࠥ᱇"))
        params = parts[-1]
        return bstack1l1l1l1_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤ᱈").format(scenario.name, params)
    return scenario.name
def bstack11l111l1111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ᱉")):
            examples = list(node.callspec.params[bstack1l1l1l1_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪ᱊")].values())
        return examples
    except:
        return []
def bstack11l111l1l11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l1111lll1_opy_(report):
    try:
        status = bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᱋")
        if report.passed or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣ᱌"))):
            status = bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᱍ")
        elif report.skipped:
            status = bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᱎ")
        bstack11l11111lll_opy_(status)
    except:
        pass
def bstack1ll1l1llll_opy_(status):
    try:
        bstack11l1111ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᱏ")
        if status == bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᱐"):
            bstack11l1111ll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᱑")
        elif status == bstack1l1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᱒"):
            bstack11l1111ll1l_opy_ = bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᱓")
        bstack11l11111lll_opy_(bstack11l1111ll1l_opy_)
    except:
        pass
def bstack11l1111ll11_opy_(item=None, report=None, summary=None, extra=None):
    return