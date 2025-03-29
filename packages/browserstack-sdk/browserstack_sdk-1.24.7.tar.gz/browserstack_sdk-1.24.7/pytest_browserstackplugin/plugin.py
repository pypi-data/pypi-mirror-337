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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll11lll_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lllll1lll_opy_, bstack1ll1l1ll_opy_, update, bstack1111llll_opy_,
                                       bstack11l1l1l1l_opy_, bstack1l11llllll_opy_, bstack1l111l1ll_opy_, bstack11l1l11l1_opy_,
                                       bstack1l11lll11l_opy_, bstack111111l11_opy_, bstack1l111l1111_opy_, bstack11lll1l11_opy_,
                                       bstack11llll1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111lll1ll_opy_)
from browserstack_sdk.bstack1ll11111l1_opy_ import bstack1l111l1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1llllll_opy_
from bstack_utils.capture import bstack11l11lllll_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1l1lll11_opy_, bstack11l11ll1l_opy_, bstack1llll11111_opy_, \
    bstack1lll1ll1l1_opy_
from bstack_utils.helper import bstack11ll111l_opy_, bstack11lll1111ll_opy_, bstack111ll1l111_opy_, bstack1ll1l11ll_opy_, bstack1ll1111ll11_opy_, bstack1lll11llll_opy_, \
    bstack11ll1ll1l1l_opy_, \
    bstack11lllll1l11_opy_, bstack1l11l1lll_opy_, bstack111l1l1ll_opy_, bstack11lll1ll111_opy_, bstack1l111l11l_opy_, Notset, \
    bstack111111lll_opy_, bstack11lll11l1ll_opy_, bstack11lllllll1l_opy_, Result, bstack11ll1ll1l11_opy_, bstack11llll1ll1l_opy_, bstack111ll1llll_opy_, \
    bstack1l1l1ll111_opy_, bstack1ll1l111l_opy_, bstack11ll11l1l_opy_, bstack11lll1lllll_opy_
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11ll1l1_opy_
from bstack_utils.messages import bstack11l1ll11ll_opy_, bstack1l1l1ll1l1_opy_, bstack11lll11l11_opy_, bstack1lll111ll_opy_, bstack1l1lll1l_opy_, \
    bstack1ll11l1l1l_opy_, bstack1ll11ll11l_opy_, bstack11l1l11ll_opy_, bstack1l1l11l111_opy_, bstack1111ll1l1_opy_, \
    bstack11ll11llll_opy_, bstack1l111l1l1_opy_
from bstack_utils.proxy import bstack11ll1111ll_opy_, bstack1l111lll1_opy_
from bstack_utils.bstack1l1ll1lll1_opy_ import bstack11l1111ll11_opy_, bstack11l111l11ll_opy_, bstack11l1111l11l_opy_, bstack11l111l11l1_opy_, \
    bstack11l111l111l_opy_, bstack11l1111l1ll_opy_, bstack11l111l1l11_opy_, bstack1ll1l1llll_opy_, bstack11l1111lll1_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1l111lll11_opy_
from bstack_utils.bstack1l11l1ll1_opy_ import bstack1lll1ll1ll_opy_, bstack1111l1l1l_opy_, bstack11llllll1l_opy_, \
    bstack1ll1lllll1_opy_, bstack1l1ll1l11l_opy_
from bstack_utils.bstack11l11ll1l1_opy_ import bstack11l11l1ll1_opy_
from bstack_utils.bstack11l11ll1ll_opy_ import bstack1l11l1lll1_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack11l1l1111l_opy_ import bstack111111ll1_opy_
from bstack_utils.bstack1l111lll1l_opy_ import bstack1l111lll1l_opy_
from browserstack_sdk.__init__ import bstack11ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11111l1_opy_ import bstack1l11111l1_opy_, bstack1l1l1111ll_opy_, bstack1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11llll111_opy_, bstack1lll1l1lll1_opy_, bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1l11111l1_opy_ import bstack1l11111l1_opy_, bstack1l1l1111ll_opy_, bstack1ll1lll1_opy_
bstack1ll11l11ll_opy_ = None
bstack1ll1lll11_opy_ = None
bstack1l1l1llll1_opy_ = None
bstack1ll11lll11_opy_ = None
bstack11ll11ll_opy_ = None
bstack1ll1lll11l_opy_ = None
bstack11111111l_opy_ = None
bstack11l1l1ll_opy_ = None
bstack1l111llll_opy_ = None
bstack1l1111lll1_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l1lllll11_opy_ = None
bstack1l1lll1l1l_opy_ = None
bstack1l11111ll1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧḨ")
CONFIG = {}
bstack1l1ll11ll_opy_ = False
bstack1l1llll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨḩ")
bstack1l1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠩḪ")
bstack11l11l11l_opy_ = False
bstack1ll11ll11_opy_ = []
bstack11ll11111l_opy_ = bstack1l1l1lll11_opy_
bstack111l11l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩḫ")
bstack11ll1l111_opy_ = {}
bstack1ll1l1111l_opy_ = None
bstack1lll1ll11l_opy_ = False
logger = bstack1l1llllll_opy_.get_logger(__name__, bstack11ll11111l_opy_)
store = {
    bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧḬ"): []
}
bstack111l1l1llll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111lll1111_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11llll111_opy_(
    test_framework_name=bstack1111111l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗ࠱ࡇࡊࡄࠨḭ")] if bstack1l111l11l_opy_() else bstack1111111l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࠬḮ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack11l1lllll_opy_(page, bstack1l1ll1llll_opy_):
    try:
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢḯ"),
                      bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫḰ") + json.dumps(
                          bstack1l1ll1llll_opy_) + bstack1l1l1l1_opy_ (u"ࠣࡿࢀࠦḱ"))
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢḲ"), e)
def bstack11lll1l1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦḳ"), bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩḴ") + json.dumps(
            message) + bstack1l1l1l1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨḵ") + json.dumps(level) + bstack1l1l1l1_opy_ (u"࠭ࡽࡾࠩḶ"))
    except Exception as e:
        print(bstack1l1l1l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥḷ"), e)
def pytest_configure(config):
    global bstack1l1llll1ll_opy_
    global CONFIG
    bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
    config.args = bstack1l11l1lll1_opy_.bstack111l1lll11l_opy_(config.args)
    bstack1l1l1111l_opy_.bstack1ll1ll111l_opy_(bstack11ll11l1l_opy_(config.getoption(bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬḸ"))))
    try:
        bstack1l1llllll_opy_.bstack11ll11111ll_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.CONNECT, bstack1ll1lll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩḹ"), bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬḺ")))
        config = json.loads(os.environ.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥḻ"), bstack1l1l1l1_opy_ (u"ࠧࢁࡽࠣḼ")))
        cli.bstack1lll1ll1lll_opy_(bstack111l1l1ll_opy_(bstack1l1llll1ll_opy_, CONFIG), cli_context.platform_index, bstack1111llll_opy_)
    if cli.bstack1llll1ll11l_opy_(bstack1lll1l1ll1l_opy_):
        cli.bstack1llllll1l11_opy_()
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡃࡍࡋࠣ࡭ࡸࠦࡡࡤࡶ࡬ࡺࡪࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧḽ") + str(cli_context.platform_index) + bstack1l1l1l1_opy_ (u"ࠢࠣḾ"))
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_ALL, bstack1llll1llll1_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1l1l1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨḿ"), None)
    if cli.is_running() and when == bstack1l1l1l1_opy_ (u"ࠤࡦࡥࡱࡲࠢṀ"):
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG_REPORT, bstack1llll1llll1_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤṁ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll1llll1_opy_.POST, item, call, outcome)
        elif when == bstack1l1l1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࠤṂ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG_REPORT, bstack1llll1llll1_opy_.POST, item, call, outcome)
        elif when == bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢṃ"):
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.AFTER_EACH, bstack1llll1llll1_opy_.POST, item, call, outcome)
        return # skip all existing bstack111l1l1l1ll_opy_
    bstack111l11ll1ll_opy_ = item.config.getoption(bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨṄ"))
    plugins = item.config.getoption(bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡸ࡫࡮ࡴࡳࠣṅ"))
    report = outcome.get_result()
    bstack111l11lllll_opy_(item, call, report)
    if bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳࠨṆ") not in plugins or bstack1l111l11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠤࡢࡨࡷ࡯ࡶࡦࡴࠥṇ"), None)
    page = getattr(item, bstack1l1l1l1_opy_ (u"ࠥࡣࡵࡧࡧࡦࠤṈ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack111l1l1ll1l_opy_(item, report, summary, bstack111l11ll1ll_opy_)
    if (page is not None):
        bstack111l1l11l11_opy_(item, report, summary, bstack111l11ll1ll_opy_)
def bstack111l1l1ll1l_opy_(item, report, summary, bstack111l11ll1ll_opy_):
    if report.when == bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪṉ") and report.skipped:
        bstack11l1111lll1_opy_(report)
    if report.when in [bstack1l1l1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦṊ"), bstack1l1l1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣṋ")]:
        return
    if not bstack1ll1111ll11_opy_():
        return
    try:
        if (str(bstack111l11ll1ll_opy_).lower() != bstack1l1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬṌ") and not cli.is_running()):
            item._driver.execute_script(
                bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭ṍ") + json.dumps(
                    report.nodeid) + bstack1l1l1l1_opy_ (u"ࠩࢀࢁࠬṎ"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ṏ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࡀࠠࡼ࠲ࢀࠦṐ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢṑ")))
    bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࠢṒ")
    bstack11l1111lll1_opy_(report)
    if not passed:
        try:
            bstack1l1l11l11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢṓ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l11l11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥṔ")))
        bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠤࠥṕ")
        if not passed:
            try:
                bstack1l1l11l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥṖ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l11l11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨṗ")
                    + json.dumps(bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨṘ"))
                    + bstack1l1l1l1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤṙ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬṚ")
                    + json.dumps(str(bstack1l1l11l11l_opy_))
                    + bstack1l1l1l1_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦṛ")
                )
        except Exception as e:
            summary.append(bstack1l1l1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢṜ").format(e))
def bstack111l11llll1_opy_(test_name, error_message):
    try:
        bstack111l1l11lll_opy_ = []
        bstack1l1ll111ll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪṝ"), bstack1l1l1l1_opy_ (u"ࠫ࠵࠭Ṟ"))
        bstack11llllllll_opy_ = {bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪṟ"): test_name, bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬṠ"): error_message, bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ṡ"): bstack1l1ll111ll_opy_}
        bstack111l11ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠨࡲࡺࡣࡵࡿࡴࡦࡵࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭Ṣ"))
        if os.path.exists(bstack111l11ll11l_opy_):
            with open(bstack111l11ll11l_opy_) as f:
                bstack111l1l11lll_opy_ = json.load(f)
        bstack111l1l11lll_opy_.append(bstack11llllllll_opy_)
        with open(bstack111l11ll11l_opy_, bstack1l1l1l1_opy_ (u"ࠩࡺࠫṣ")) as f:
            json.dump(bstack111l1l11lll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡥࡳࡵ࡬ࡷࡹ࡯࡮ࡨࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡰࡺࡶࡨࡷࡹࠦࡥࡳࡴࡲࡶࡸࡀࠠࠨṤ") + str(e))
def bstack111l1l11l11_opy_(item, report, summary, bstack111l11ll1ll_opy_):
    if report.when in [bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥṥ"), bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢṦ")]:
        return
    if (str(bstack111l11ll1ll_opy_).lower() != bstack1l1l1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫṧ")):
        bstack11l1lllll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1l1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤṨ")))
    bstack1l1l11l11l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࠤṩ")
    bstack11l1111lll1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l11l11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤṪ").format(e)
                )
        try:
            if passed:
                bstack1l1ll1l11l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩṫ"), None), bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦṬ"))
            else:
                error_message = bstack1l1l1l1_opy_ (u"ࠬ࠭ṭ")
                if bstack1l1l11l11l_opy_:
                    bstack11lll1l1ll_opy_(item._page, str(bstack1l1l11l11l_opy_), bstack1l1l1l1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧṮ"))
                    bstack1l1ll1l11l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ṯ"), None), bstack1l1l1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣṰ"), str(bstack1l1l11l11l_opy_))
                    error_message = str(bstack1l1l11l11l_opy_)
                else:
                    bstack1l1ll1l11l_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨṱ"), None), bstack1l1l1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥṲ"))
                bstack111l11llll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀ࠶ࡽࠣṳ").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1l1l1_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤṴ"), default=bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧṵ"), help=bstack1l1l1l1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨṶ"))
    parser.addoption(bstack1l1l1l1_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢṷ"), default=bstack1l1l1l1_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣṸ"), help=bstack1l1l1l1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤṹ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l1l1_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨṺ"), action=bstack1l1l1l1_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦṻ"), default=bstack1l1l1l1_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨṼ"),
                         help=bstack1l1l1l1_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨṽ"))
def bstack11l11lll1l_opy_(log):
    if not (log[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩṾ")] and log[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪṿ")].strip()):
        return
    active = bstack11l11l1lll_opy_()
    log = {
        bstack1l1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩẀ"): log[bstack1l1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẁ")],
        bstack1l1l1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨẂ"): bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"࡚࠭ࠨẃ"),
        bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẄ"): log[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẅ")],
    }
    if active:
        if active[bstack1l1l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧẆ")] == bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨẇ"):
            log[bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẈ")] = active[bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẉ")]
        elif active[bstack1l1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫẊ")] == bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࠬẋ"):
            log[bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẌ")] = active[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẍ")]
    bstack111111ll1_opy_.bstack1l11l1l1_opy_([log])
def bstack11l11l1lll_opy_():
    if len(store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧẎ")]) > 0 and store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨẏ")][-1]:
        return {
            bstack1l1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪẐ"): bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫẑ"),
            bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẒ"): store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬẓ")][-1]
        }
    if store.get(bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ẕ"), None):
        return {
            bstack1l1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨẕ"): bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩẖ"),
            bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẗ"): store[bstack1l1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪẘ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.INIT_TEST, bstack1llll1llll1_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.INIT_TEST, bstack1llll1llll1_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._111l1l11l1l_opy_ = True
        bstack1l111ll1ll_opy_ = bstack11111l11l_opy_.bstack1l111l111l_opy_(bstack11lllll1l11_opy_(item.own_markers))
        if not cli.bstack1llll1ll11l_opy_(bstack1lll1l1ll1l_opy_):
            item._a11y_test_case = bstack1l111ll1ll_opy_
            if bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ẙ"), None):
                driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩẚ"), None)
                item._a11y_started = bstack11111l11l_opy_.bstack1l111ll11_opy_(driver, bstack1l111ll1ll_opy_)
        if not bstack111111ll1_opy_.on() or bstack111l11l1lll_opy_ != bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩẛ"):
            return
        global current_test_uuid #, bstack11l11l111l_opy_
        bstack111ll1ll11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨẜ"): uuid4().__str__(),
            bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨẝ"): bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠬࡠࠧẞ")
        }
        current_test_uuid = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫẟ")]
        store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫẠ")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ạ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111lll1111_opy_[item.nodeid] = {**_111lll1111_opy_[item.nodeid], **bstack111ll1ll11_opy_}
        bstack111l1l1l1l1_opy_(item, _111lll1111_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪẢ"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬả"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨẤ")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll1llll1_opy_.PRE, item, bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫấ"))
        return # skip all existing bstack111l1l1l1ll_opy_
    global bstack111l1l1llll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11lll1ll111_opy_():
        atexit.register(bstack1ll1l1l1_opy_)
        if not bstack111l1l1llll_opy_:
            try:
                bstack111l1l1l111_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11lll1lllll_opy_():
                    bstack111l1l1l111_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack111l1l1l111_opy_:
                    signal.signal(s, bstack111l11ll111_opy_)
                bstack111l1l1llll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢẦ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l1111ll11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧầ")
    try:
        if not bstack111111ll1_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111ll1ll11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ẩ"): uuid,
            bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ẩ"): bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬẪ"),
            bstack1l1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩẫ"): bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪẬ"),
            bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩậ"): bstack1l1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬẮ"),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫắ"): bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨẰ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧằ")] = item
        store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨẲ")] = [uuid]
        if not _111lll1111_opy_.get(item.nodeid, None):
            _111lll1111_opy_[item.nodeid] = {bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫẳ"): [], bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨẴ"): []}
        _111lll1111_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ẵ")].append(bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ặ")])
        _111lll1111_opy_[item.nodeid + bstack1l1l1l1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩặ")] = bstack111ll1ll11_opy_
        bstack111l1l11ll1_opy_(item, bstack111ll1ll11_opy_, bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫẸ"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧẹ"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.AFTER_EACH, bstack1llll1llll1_opy_.PRE, item, bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧẺ"))
        return # skip all existing bstack111l1l1l1ll_opy_
    try:
        global bstack11ll1l111_opy_
        bstack1l1ll111ll_opy_ = 0
        if bstack11l11l11l_opy_ is True:
            bstack1l1ll111ll_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ẻ")))
        if bstack1ll1111l1l_opy_.bstack1lllll1l1_opy_() == bstack1l1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧẼ"):
            if bstack1ll1111l1l_opy_.bstack11ll1l1ll_opy_() == bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥẽ"):
                bstack111l11lll11_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬẾ"), None)
                bstack111ll1111_opy_ = bstack111l11lll11_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨế")
                driver = getattr(item, bstack1l1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬỀ"), None)
                bstack1lllll11l_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪề"), None)
                bstack111ll111_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫỂ"), None)
                PercySDK.screenshot(driver, bstack111ll1111_opy_, bstack1lllll11l_opy_=bstack1lllll11l_opy_, bstack111ll111_opy_=bstack111ll111_opy_, bstack11lll11l1_opy_=bstack1l1ll111ll_opy_)
        if not cli.bstack1llll1ll11l_opy_(bstack1lll1l1ll1l_opy_):
            if getattr(item, bstack1l1l1l1_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧể"), False):
                bstack1l111l1lll_opy_.bstack1l1111l1ll_opy_(getattr(item, bstack1l1l1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩỄ"), None), bstack11ll1l111_opy_, logger, item)
        if not bstack111111ll1_opy_.on():
            return
        bstack111ll1ll11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧễ"): uuid4().__str__(),
            bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧỆ"): bstack111ll1l111_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠫ࡟࠭ệ"),
            bstack1l1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪỈ"): bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫỉ"),
            bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪỊ"): bstack1l1l1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬị"),
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬỌ"): bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬọ")
        }
        _111lll1111_opy_[item.nodeid + bstack1l1l1l1_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧỎ")] = bstack111ll1ll11_opy_
        bstack111l1l11ll1_opy_(item, bstack111ll1ll11_opy_, bstack1l1l1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ỏ"))
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬỐ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack11l111l11l1_opy_(fixturedef.argname):
        store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ố")] = request.node
    elif bstack11l111l111l_opy_(fixturedef.argname):
        store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭Ồ")] = request.node
    if not bstack111111ll1_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll1llll1_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll1llll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l1l1l1ll_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll1llll1_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.SETUP_FIXTURE, bstack1llll1llll1_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack111l1l1l1ll_opy_
    try:
        fixture = {
            bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧồ"): fixturedef.argname,
            bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪỔ"): bstack11ll1ll1l1l_opy_(outcome),
            bstack1l1l1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ổ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩỖ")]
        if not _111lll1111_opy_.get(current_test_item.nodeid, None):
            _111lll1111_opy_[current_test_item.nodeid] = {bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨỗ"): []}
        _111lll1111_opy_[current_test_item.nodeid][bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩỘ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫộ"), str(err))
if bstack1l111l11l_opy_() and bstack111111ll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll1llll1_opy_.PRE, request, step)
            return
        try:
            _111lll1111_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬỚ")].bstack1lll1l1111_opy_(id(step))
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨớ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll1llll1_opy_.POST, request, step, exception)
            return
        try:
            _111lll1111_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧỜ")].bstack11l11l11ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩờ"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.STEP, bstack1llll1llll1_opy_.POST, request, step)
            return
        try:
            bstack11l11ll1l1_opy_: bstack11l11l1ll1_opy_ = _111lll1111_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩỞ")]
            bstack11l11ll1l1_opy_.bstack11l11l11ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫở"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111l11l1lll_opy_
        try:
            if not bstack111111ll1_opy_.on() or bstack111l11l1lll_opy_ != bstack1l1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬỠ"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.TEST, bstack1llll1llll1_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨỡ"), None)
            if not _111lll1111_opy_.get(request.node.nodeid, None):
                _111lll1111_opy_[request.node.nodeid] = {}
            bstack11l11ll1l1_opy_ = bstack11l11l1ll1_opy_.bstack111lll1ll11_opy_(
                scenario, feature, request.node,
                name=bstack11l1111l1ll_opy_(request.node, scenario),
                started_at=bstack1lll11llll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬỢ"),
                tags=bstack11l111l1l11_opy_(feature, scenario),
                bstack11l11l1l11_opy_=bstack111111ll1_opy_.bstack11l1l11l11_opy_(driver) if driver and driver.session_id else {}
            )
            _111lll1111_opy_[request.node.nodeid][bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧợ")] = bstack11l11ll1l1_opy_
            bstack111l1ll1l1l_opy_(bstack11l11ll1l1_opy_.uuid)
            bstack111111ll1_opy_.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ụ"), bstack11l11ll1l1_opy_)
        except Exception as err:
            print(bstack1l1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨụ"), str(err))
def bstack111l1l111l1_opy_(bstack11l11l11l1_opy_):
    if bstack11l11l11l1_opy_ in store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫỦ")]:
        store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬủ")].remove(bstack11l11l11l1_opy_)
def bstack111l1ll1l1l_opy_(test_uuid):
    store[bstack1l1l1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ứ")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack111111ll1_opy_.bstack111ll1l11l1_opy_
def bstack111l11lllll_opy_(item, call, report):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡵࡸࠬứ"))
    global bstack111l11l1lll_opy_
    bstack11ll11ll1_opy_ = bstack1lll11llll_opy_()
    if hasattr(report, bstack1l1l1l1_opy_ (u"ࠫࡸࡺ࡯ࡱࠩỪ")):
        bstack11ll11ll1_opy_ = bstack11ll1ll1l11_opy_(report.stop)
    elif hasattr(report, bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫừ")):
        bstack11ll11ll1_opy_ = bstack11ll1ll1l11_opy_(report.start)
    try:
        if getattr(report, bstack1l1l1l1_opy_ (u"࠭ࡷࡩࡧࡱࠫỬ"), bstack1l1l1l1_opy_ (u"ࠧࠨử")) == bstack1l1l1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭Ữ"):
            logger.debug(bstack1l1l1l1_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫữ").format(getattr(report, bstack1l1l1l1_opy_ (u"ࠪࡻ࡭࡫࡮ࠨỰ"), bstack1l1l1l1_opy_ (u"ࠫࠬự")).__str__(), bstack111l11l1lll_opy_))
            if bstack111l11l1lll_opy_ == bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬỲ"):
                _111lll1111_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫỳ")] = bstack11ll11ll1_opy_
                bstack111l1l1l1l1_opy_(item, _111lll1111_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩỴ"), report, call)
                store[bstack1l1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬỵ")] = None
            elif bstack111l11l1lll_opy_ == bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨỶ"):
                bstack11l11ll1l1_opy_ = _111lll1111_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ỷ")]
                bstack11l11ll1l1_opy_.set(hooks=_111lll1111_opy_[item.nodeid].get(bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪỸ"), []))
                exception, bstack11l111llll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11l111llll_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l1l1_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫỹ"), bstack1l1l1l1_opy_ (u"࠭ࠧỺ"))]
                bstack11l11ll1l1_opy_.stop(time=bstack11ll11ll1_opy_, result=Result(result=getattr(report, bstack1l1l1l1_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨỻ"), bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨỼ")), exception=exception, bstack11l111llll_opy_=bstack11l111llll_opy_))
                bstack111111ll1_opy_.bstack11l11ll111_opy_(bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫỽ"), _111lll1111_opy_[item.nodeid][bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ỿ")])
        elif getattr(report, bstack1l1l1l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩỿ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ἀ")) in [bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬἁ"), bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩἂ")]:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡸࡺࡡࡵࡧࠣ࠱ࠥࢁࡽ࠭ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡼࡿࠪἃ").format(getattr(report, bstack1l1l1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧἄ"), bstack1l1l1l1_opy_ (u"ࠪࠫἅ")).__str__(), bstack111l11l1lll_opy_))
            bstack11l11ll11l_opy_ = item.nodeid + bstack1l1l1l1_opy_ (u"ࠫ࠲࠭ἆ") + getattr(report, bstack1l1l1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪἇ"), bstack1l1l1l1_opy_ (u"࠭ࠧἈ"))
            if getattr(report, bstack1l1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨἉ"), False):
                hook_type = bstack1l1l1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ἂ") if getattr(report, bstack1l1l1l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧἋ"), bstack1l1l1l1_opy_ (u"ࠪࠫἌ")) == bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪἍ") else bstack1l1l1l1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩἎ")
                _111lll1111_opy_[bstack11l11ll11l_opy_] = {
                    bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫἏ"): uuid4().__str__(),
                    bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫἐ"): bstack11ll11ll1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫἑ"): hook_type
                }
            _111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧἒ")] = bstack11ll11ll1_opy_
            bstack111l1l111l1_opy_(_111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨἓ")])
            bstack111l1l11ll1_opy_(item, _111lll1111_opy_[bstack11l11ll11l_opy_], bstack1l1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ἔ"), report, call)
            if getattr(report, bstack1l1l1l1_opy_ (u"ࠬࡽࡨࡦࡰࠪἕ"), bstack1l1l1l1_opy_ (u"࠭ࠧ἖")) == bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭἗"):
                if getattr(report, bstack1l1l1l1_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩἘ"), bstack1l1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩἙ")) == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪἚ"):
                    bstack111ll1ll11_opy_ = {
                        bstack1l1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩἛ"): uuid4().__str__(),
                        bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩἜ"): bstack1lll11llll_opy_(),
                        bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫἝ"): bstack1lll11llll_opy_()
                    }
                    _111lll1111_opy_[item.nodeid] = {**_111lll1111_opy_[item.nodeid], **bstack111ll1ll11_opy_}
                    bstack111l1l1l1l1_opy_(item, _111lll1111_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ἞"))
                    bstack111l1l1l1l1_opy_(item, _111lll1111_opy_[item.nodeid], bstack1l1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ἟"), report, call)
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧἠ"), str(err))
def bstack111l1ll11l1_opy_(test, bstack111ll1ll11_opy_, result=None, call=None, bstack1l1ll11111_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11l11ll1l1_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨἡ"): bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩἢ")],
        bstack1l1l1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪἣ"): bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫἤ"),
        bstack1l1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬἥ"): test.name,
        bstack1l1l1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭ἦ"): {
            bstack1l1l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧἧ"): bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪἨ"),
            bstack1l1l1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩἩ"): inspect.getsource(test.obj)
        },
        bstack1l1l1l1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩἪ"): test.name,
        bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬἫ"): test.name,
        bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧἬ"): bstack1l11l1lll1_opy_.bstack11l1111ll1_opy_(test),
        bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫἭ"): file_path,
        bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫἮ"): file_path,
        bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪἯ"): bstack1l1l1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬἰ"),
        bstack1l1l1l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪἱ"): file_path,
        bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪἲ"): bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫἳ")],
        bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫἴ"): bstack1l1l1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩἵ"),
        bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ἶ"): {
            bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨἷ"): test.nodeid
        },
        bstack1l1l1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪἸ"): bstack11lllll1l11_opy_(test.own_markers)
    }
    if bstack1l1ll11111_opy_ in [bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧἹ"), bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩἺ")]:
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭Ἳ")] = {
            bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫἼ"): bstack111ll1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬἽ"), [])
        }
    if bstack1l1ll11111_opy_ == bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬἾ"):
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬἿ")] = bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧὀ")
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ὁ")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧὂ")]
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧὃ")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨὄ")]
    if result:
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫὅ")] = result.outcome
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭὆")] = result.duration * 1000
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ὇")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬὈ")]
        if result.failed:
            bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧὉ")] = bstack111111ll1_opy_.bstack111l11l1ll_opy_(call.excinfo.typename)
            bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪὊ")] = bstack111111ll1_opy_.bstack111ll1lll1l_opy_(call.excinfo, result)
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩὋ")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪὌ")]
    if outcome:
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬὍ")] = bstack11ll1ll1l1l_opy_(outcome)
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ὎")] = 0
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ὏")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ὐ")]
        if bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩὑ")] == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪὒ"):
            bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪὓ")] = bstack1l1l1l1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ὔ")  # bstack111l1l11111_opy_
            bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧὕ")] = [{bstack1l1l1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪὖ"): [bstack1l1l1l1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬὗ")]}]
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ὘")] = bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩὙ")]
    return bstack11l11ll1l1_opy_
def bstack111l1l1111l_opy_(test, bstack111ll11l11_opy_, bstack1l1ll11111_opy_, result, call, outcome, bstack111l1ll1111_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ὚")]
    hook_name = bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨὛ")]
    hook_data = {
        bstack1l1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ὜"): bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬὝ")],
        bstack1l1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭὞"): bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧὟ"),
        bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨὠ"): bstack1l1l1l1_opy_ (u"ࠫࢀࢃࠧὡ").format(bstack11l111l11ll_opy_(hook_name)),
        bstack1l1l1l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪὢ"): {
            bstack1l1l1l1_opy_ (u"࠭࡬ࡢࡰࡪࠫὣ"): bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧὤ"),
            bstack1l1l1l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭ὥ"): None
        },
        bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨὦ"): test.name,
        bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪὧ"): bstack1l11l1lll1_opy_.bstack11l1111ll1_opy_(test, hook_name),
        bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧὨ"): file_path,
        bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧὩ"): file_path,
        bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭Ὢ"): bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨὫ"),
        bstack1l1l1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭Ὤ"): file_path,
        bstack1l1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭Ὥ"): bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧὮ")],
        bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧὯ"): bstack1l1l1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧὰ") if bstack111l11l1lll_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪά") else bstack1l1l1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧὲ"),
        bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫέ"): hook_type
    }
    bstack111lll1l1ll_opy_ = bstack111llll11l_opy_(_111lll1111_opy_.get(test.nodeid, None))
    if bstack111lll1l1ll_opy_:
        hook_data[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧὴ")] = bstack111lll1l1ll_opy_
    if result:
        hook_data[bstack1l1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪή")] = result.outcome
        hook_data[bstack1l1l1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬὶ")] = result.duration * 1000
        hook_data[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪί")] = bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫὸ")]
        if result.failed:
            hook_data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ό")] = bstack111111ll1_opy_.bstack111l11l1ll_opy_(call.excinfo.typename)
            hook_data[bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩὺ")] = bstack111111ll1_opy_.bstack111ll1lll1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩύ")] = bstack11ll1ll1l1l_opy_(outcome)
        hook_data[bstack1l1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫὼ")] = 100
        hook_data[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩώ")] = bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ὾")]
        if hook_data[bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭὿")] == bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᾀ"):
            hook_data[bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᾁ")] = bstack1l1l1l1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᾂ")  # bstack111l1l11111_opy_
            hook_data[bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᾃ")] = [{bstack1l1l1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᾄ"): [bstack1l1l1l1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᾅ")]}]
    if bstack111l1ll1111_opy_:
        hook_data[bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᾆ")] = bstack111l1ll1111_opy_.result
        hook_data[bstack1l1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᾇ")] = bstack11lll11l1ll_opy_(bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᾈ")], bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᾉ")])
        hook_data[bstack1l1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᾊ")] = bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᾋ")]
        if hook_data[bstack1l1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᾌ")] == bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᾍ"):
            hook_data[bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᾎ")] = bstack111111ll1_opy_.bstack111l11l1ll_opy_(bstack111l1ll1111_opy_.exception_type)
            hook_data[bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᾏ")] = [{bstack1l1l1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᾐ"): bstack11lllllll1l_opy_(bstack111l1ll1111_opy_.exception)}]
    return hook_data
def bstack111l1l1l1l1_opy_(test, bstack111ll1ll11_opy_, bstack1l1ll11111_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡲࡶࡰࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠢ࠰ࠤࢀࢃࠧᾑ").format(bstack1l1ll11111_opy_))
    bstack11l11ll1l1_opy_ = bstack111l1ll11l1_opy_(test, bstack111ll1ll11_opy_, result, call, bstack1l1ll11111_opy_, outcome)
    driver = getattr(test, bstack1l1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᾒ"), None)
    if bstack1l1ll11111_opy_ == bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᾓ") and driver:
        bstack11l11ll1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᾔ")] = bstack111111ll1_opy_.bstack11l1l11l11_opy_(driver)
    if bstack1l1ll11111_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᾕ"):
        bstack1l1ll11111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᾖ")
    bstack11l111l1l1_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᾗ"): bstack1l1ll11111_opy_,
        bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᾘ"): bstack11l11ll1l1_opy_
    }
    bstack111111ll1_opy_.bstack11ll1ll111_opy_(bstack11l111l1l1_opy_)
    if bstack1l1ll11111_opy_ == bstack1l1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᾙ"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᾚ"): bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᾛ")}
    elif bstack1l1ll11111_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᾜ"):
        threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᾝ"): getattr(result, bstack1l1l1l1_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᾞ"), bstack1l1l1l1_opy_ (u"ࠪࠫᾟ"))}
def bstack111l1l11ll1_opy_(test, bstack111ll1ll11_opy_, bstack1l1ll11111_opy_, result=None, call=None, outcome=None, bstack111l1ll1111_opy_=None):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡸ࡫࡮ࡥࡡ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡨࡰࡱ࡮ࠤࡩࡧࡴࡢ࠮ࠣࡩࡻ࡫࡮ࡵࡖࡼࡴࡪࠦ࠭ࠡࡽࢀࠫᾠ").format(bstack1l1ll11111_opy_))
    hook_data = bstack111l1l1111l_opy_(test, bstack111ll1ll11_opy_, bstack1l1ll11111_opy_, result, call, outcome, bstack111l1ll1111_opy_)
    bstack11l111l1l1_opy_ = {
        bstack1l1l1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᾡ"): bstack1l1ll11111_opy_,
        bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨᾢ"): hook_data
    }
    bstack111111ll1_opy_.bstack11ll1ll111_opy_(bstack11l111l1l1_opy_)
def bstack111llll11l_opy_(bstack111ll1ll11_opy_):
    if not bstack111ll1ll11_opy_:
        return None
    if bstack111ll1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᾣ"), None):
        return getattr(bstack111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᾤ")], bstack1l1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᾥ"), None)
    return bstack111ll1ll11_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᾦ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG, bstack1llll1llll1_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_.LOG, bstack1llll1llll1_opy_.POST, request, caplog)
        return # skip all existing bstack111l1l1l1ll_opy_
    try:
        if not bstack111111ll1_opy_.on():
            return
        places = [bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᾧ"), bstack1l1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᾨ"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᾩ")]
        logs = []
        for bstack111l1l111ll_opy_ in places:
            records = caplog.get_records(bstack111l1l111ll_opy_)
            bstack111l11lll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾪ") if bstack111l1l111ll_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᾫ") else bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾬ")
            bstack111l1l1ll11_opy_ = request.node.nodeid + (bstack1l1l1l1_opy_ (u"ࠪࠫᾭ") if bstack111l1l111ll_opy_ == bstack1l1l1l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᾮ") else bstack1l1l1l1_opy_ (u"ࠬ࠳ࠧᾯ") + bstack111l1l111ll_opy_)
            test_uuid = bstack111llll11l_opy_(_111lll1111_opy_.get(bstack111l1l1ll11_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11llll1ll1l_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᾰ"): bstack11lll1111ll_opy_(record.created).isoformat() + bstack1l1l1l1_opy_ (u"࡛ࠧࠩᾱ"),
                    bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᾲ"): record.levelname,
                    bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾳ"): record.message,
                    bstack111l11lll1l_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack111111ll1_opy_.bstack1l11l1l1_opy_(logs)
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᾴ"), str(err))
def bstack111l1ll1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1lll1ll11l_opy_
    bstack1lll1111l1_opy_ = bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ᾵"), None) and bstack11ll111l_opy_(
            threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᾶ"), None)
    bstack11111111_opy_ = getattr(driver, bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᾷ"), None) != None and getattr(driver, bstack1l1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᾸ"), None) == True
    if sequence == bstack1l1l1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᾹ") and driver != None:
      if not bstack1lll1ll11l_opy_ and bstack1ll1111ll11_opy_() and bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᾺ") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪΆ")] == True and bstack1l111lll1l_opy_.bstack11lllll11_opy_(driver_command) and (bstack11111111_opy_ or bstack1lll1111l1_opy_) and not bstack111lll1ll_opy_(args):
        try:
          bstack1lll1ll11l_opy_ = True
          logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ᾼ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪ᾽").format(str(err)))
        bstack1lll1ll11l_opy_ = False
    if sequence == bstack1l1l1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬι"):
        if driver_command == bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫ᾿"):
            bstack111111ll1_opy_.bstack11llll111_opy_({
                bstack1l1l1l1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ῀"): response[bstack1l1l1l1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ῁")],
                bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῂ"): store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨῃ")]
            })
def bstack1ll1l1l1_opy_():
    global bstack1ll11ll11_opy_
    bstack1l1llllll_opy_.bstack1llll11l_opy_()
    logging.shutdown()
    bstack111111ll1_opy_.bstack111llllll1_opy_()
    for driver in bstack1ll11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111l11ll111_opy_(*args):
    global bstack1ll11ll11_opy_
    bstack111111ll1_opy_.bstack111llllll1_opy_()
    for driver in bstack1ll11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l111l1ll1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1llllll1ll_opy_(self, *args, **kwargs):
    bstack11l111ll_opy_ = bstack1ll11l11ll_opy_(self, *args, **kwargs)
    bstack1llllll1l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࡙࡫ࡳࡵࡏࡨࡸࡦ࠭ῄ"), None)
    if bstack1llllll1l_opy_ and bstack1llllll1l_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭῅"), bstack1l1l1l1_opy_ (u"ࠧࠨῆ")) == bstack1l1l1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩῇ"):
        bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
    return bstack11l111ll_opy_
@measure(event_name=EVENTS.bstack11l1ll111_opy_, stage=STAGE.bstack1l11111lll_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1lll1lll1l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
    if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭Ὲ")):
        return
    bstack1l1l1111l_opy_.bstack1l11l11l11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧΈ"), True)
    global bstack1l11111ll1_opy_
    global bstack1llllll1l1_opy_
    bstack1l11111ll1_opy_ = framework_name
    logger.info(bstack1l111l1l1_opy_.format(bstack1l11111ll1_opy_.split(bstack1l1l1l1_opy_ (u"ࠫ࠲࠭Ὴ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111ll11_opy_():
            Service.start = bstack1l111l1ll_opy_
            Service.stop = bstack11l1l11l1_opy_
            webdriver.Remote.get = bstack1l1lll1ll1_opy_
            webdriver.Remote.__init__ = bstack1lll11l1l_opy_
            if not isinstance(os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭Ή")), str):
                return
            WebDriver.close = bstack1l11lll11l_opy_
            WebDriver.quit = bstack1l1lll11l1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack111111ll1_opy_.on():
            webdriver.Remote.__init__ = bstack1llllll1ll_opy_
        bstack1llllll1l1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫῌ")):
        bstack1llllll1l1_opy_ = eval(os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ῍")))
    if not bstack1llllll1l1_opy_:
        bstack1l111l1111_opy_(bstack1l1l1l1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ῎"), bstack11ll11llll_opy_)
    if bstack1ll1ll1l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1l1l11111l_opy_ = bstack11l1llll11_opy_
        except Exception as e:
            logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
    if bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ῏") in str(framework_name).lower():
        if not bstack1ll1111ll11_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l1l1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l11llllll_opy_
            Config.getoption = bstack1llllll111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1ll11lll1l_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1l1ll1l_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1lll11l1_opy_(self):
    global bstack1l11111ll1_opy_
    global bstack1ll111l11l_opy_
    global bstack1ll1lll11_opy_
    try:
        if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪῐ") in bstack1l11111ll1_opy_ and self.session_id != None and bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨῑ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ῒ")) != bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧΐ"):
            bstack1lllllll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ῔") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ῕")
            bstack1ll1l111l_opy_(logger, True)
            if self != None:
                bstack1ll1lllll1_opy_(self, bstack1lllllll1l_opy_, bstack1l1l1l1_opy_ (u"ࠩ࠯ࠤࠬῖ").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll1ll11l_opy_(bstack1lll1l1ll1l_opy_):
            item = store.get(bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧῗ"), None)
            if item is not None and bstack11ll111l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪῘ"), None):
                bstack1l111l1lll_opy_.bstack1l1111l1ll_opy_(self, bstack11ll1l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l1l1_opy_ (u"ࠬ࠭Ῑ")
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢῚ") + str(e))
    bstack1ll1lll11_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11ll1111l1_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1lll11l1l_opy_(self, command_executor,
             desired_capabilities=None, bstack1ll1ll1l1l_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll111l11l_opy_
    global bstack1ll1l1111l_opy_
    global bstack11l11l11l_opy_
    global bstack1l11111ll1_opy_
    global bstack1ll11l11ll_opy_
    global bstack1ll11ll11_opy_
    global bstack1l1llll1ll_opy_
    global bstack1l1l1ll1_opy_
    global bstack11ll1l111_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩΊ")] = str(bstack1l11111ll1_opy_) + str(__version__)
    command_executor = bstack111l1l1ll_opy_(bstack1l1llll1ll_opy_, CONFIG)
    logger.debug(bstack1lll111ll_opy_.format(command_executor))
    proxy = bstack11llll1l_opy_(CONFIG, proxy)
    bstack1l1ll111ll_opy_ = 0
    try:
        if bstack11l11l11l_opy_ is True:
            bstack1l1ll111ll_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ῜")))
    except:
        bstack1l1ll111ll_opy_ = 0
    bstack111111l1l_opy_ = bstack1lllll1lll_opy_(CONFIG, bstack1l1ll111ll_opy_)
    logger.debug(bstack11l1l11ll_opy_.format(str(bstack111111l1l_opy_)))
    bstack11ll1l111_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ῝"))[bstack1l1ll111ll_opy_]
    if bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ῞") in CONFIG and CONFIG[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ῟")]:
        bstack11llllll1l_opy_(bstack111111l1l_opy_, bstack1l1l1ll1_opy_)
    if bstack11111l11l_opy_.bstack1111111l1_opy_(CONFIG, bstack1l1ll111ll_opy_) and bstack11111l11l_opy_.bstack11ll11ll1l_opy_(bstack111111l1l_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll1ll11l_opy_(bstack1lll1l1ll1l_opy_):
            bstack11111l11l_opy_.set_capabilities(bstack111111l1l_opy_, CONFIG)
    if desired_capabilities:
        bstack11l111lll_opy_ = bstack1ll1l1ll_opy_(desired_capabilities)
        bstack11l111lll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬῠ")] = bstack111111lll_opy_(CONFIG)
        bstack111lllll_opy_ = bstack1lllll1lll_opy_(bstack11l111lll_opy_)
        if bstack111lllll_opy_:
            bstack111111l1l_opy_ = update(bstack111lllll_opy_, bstack111111l1l_opy_)
        desired_capabilities = None
    if options:
        bstack111111l11_opy_(options, bstack111111l1l_opy_)
    if not options:
        options = bstack1111llll_opy_(bstack111111l1l_opy_)
    if proxy and bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ῡ")):
        options.proxy(proxy)
    if options and bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ῢ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l11l1lll_opy_() < version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧΰ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111111l1l_opy_)
    logger.info(bstack11lll11l11_opy_)
    bstack1lll11lll_opy_.end(EVENTS.bstack11l1ll111_opy_.value, EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤῤ"),
                               EVENTS.bstack11l1ll111_opy_.value + bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣῥ"), True, None)
    if bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫῦ")):
        bstack1ll11l11ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫῧ")):
        bstack1ll11l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭Ῠ")):
        bstack1ll11l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1ll11l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack1ll1ll1l1l_opy_=bstack1ll1ll1l1l_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll1l11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠧࠨῩ")
        if bstack1l11l1lll_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩῪ")):
            bstack1ll1l11lll_opy_ = self.caps.get(bstack1l1l1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤΎ"))
        else:
            bstack1ll1l11lll_opy_ = self.capabilities.get(bstack1l1l1l1_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥῬ"))
        if bstack1ll1l11lll_opy_:
            bstack1l1l1ll111_opy_(bstack1ll1l11lll_opy_)
            if bstack1l11l1lll_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ῭")):
                self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ΅") + bstack1l1llll1ll_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ`")
            else:
                self.command_executor._url = bstack1l1l1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ῰") + bstack1ll1l11lll_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ῱")
            logger.debug(bstack1l1l1ll1l1_opy_.format(bstack1ll1l11lll_opy_))
        else:
            logger.debug(bstack11l1ll11ll_opy_.format(bstack1l1l1l1_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥῲ")))
    except Exception as e:
        logger.debug(bstack11l1ll11ll_opy_.format(e))
    bstack1ll111l11l_opy_ = self.session_id
    if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪῳ") in bstack1l11111ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨῴ"), None)
        if item:
            bstack111l1ll111l_opy_ = getattr(item, bstack1l1l1l1_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ῵"), False)
            if not getattr(item, bstack1l1l1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧῶ"), None) and bstack111l1ll111l_opy_:
                setattr(store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫῷ")], bstack1l1l1l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩῸ"), self)
        bstack1llllll1l_opy_ = getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡖࡨࡷࡹࡓࡥࡵࡣࠪΌ"), None)
        if bstack1llllll1l_opy_ and bstack1llllll1l_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪῺ"), bstack1l1l1l1_opy_ (u"ࠫࠬΏ")) == bstack1l1l1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ῼ"):
            bstack111111ll1_opy_.bstack1l111111l1_opy_(self)
    bstack1ll11ll11_opy_.append(self)
    if bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ´") in CONFIG and bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ῾") in CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ῿")][bstack1l1ll111ll_opy_]:
        bstack1ll1l1111l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ ")][bstack1l1ll111ll_opy_][bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ ")]
    logger.debug(bstack1111ll1l1_opy_.format(bstack1ll111l11l_opy_))
@measure(event_name=EVENTS.bstack11ll1ll11_opy_, stage=STAGE.bstack1llll1ll11_opy_, bstack1lllll1ll_opy_=bstack1ll1l1111l_opy_)
def bstack1l1lll1ll1_opy_(self, url):
    global bstack1l111llll_opy_
    global CONFIG
    try:
        bstack1111l1l1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l11l111_opy_.format(str(err)))
    try:
        bstack1l111llll_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1111111l_opy_ = str(e)
            if any(err_msg in bstack1l1111111l_opy_ for err_msg in bstack1llll11111_opy_):
                bstack1111l1l1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l11l111_opy_.format(str(err)))
        raise e
def bstack1ll11l11_opy_(item, when):
    global bstack1l1lllll11_opy_
    try:
        bstack1l1lllll11_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11lll1l_opy_(item, call, rep):
    global bstack1l1lll1l1l_opy_
    global bstack1ll11ll11_opy_
    name = bstack1l1l1l1_opy_ (u"ࠫࠬ ")
    try:
        if rep.when == bstack1l1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ "):
            bstack1ll111l11l_opy_ = threading.current_thread().bstackSessionId
            bstack111l11ll1ll_opy_ = item.config.getoption(bstack1l1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ "))
            try:
                if (str(bstack111l11ll1ll_opy_).lower() != bstack1l1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ ")):
                    name = str(rep.nodeid)
                    bstack111lll1l_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ "), name, bstack1l1l1l1_opy_ (u"ࠩࠪ "), bstack1l1l1l1_opy_ (u"ࠪࠫ "), bstack1l1l1l1_opy_ (u"ࠫࠬ "), bstack1l1l1l1_opy_ (u"ࠬ࠭ "))
                    os.environ[bstack1l1l1l1_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ​")] = name
                    for driver in bstack1ll11ll11_opy_:
                        if bstack1ll111l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack111lll1l_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ‌").format(str(e)))
            try:
                bstack1ll1l1llll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ‍"):
                    status = bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ‎") if rep.outcome.lower() == bstack1l1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ‏") else bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ‐")
                    reason = bstack1l1l1l1_opy_ (u"ࠬ࠭‑")
                    if status == bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭‒"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬ–") if status == bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ—") else bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ―")
                    data = name + bstack1l1l1l1_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ‖") if status == bstack1l1l1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ‗") else name + bstack1l1l1l1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨ‘") + reason
                    bstack1ll1l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack1l1l1l1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ’"), bstack1l1l1l1_opy_ (u"ࠧࠨ‚"), bstack1l1l1l1_opy_ (u"ࠨࠩ‛"), bstack1l1l1l1_opy_ (u"ࠩࠪ“"), level, data)
                    for driver in bstack1ll11ll11_opy_:
                        if bstack1ll111l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll1l11l11_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧ”").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨ„").format(str(e)))
    bstack1l1lll1l1l_opy_(item, call, rep)
notset = Notset()
def bstack1llllll111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll111l1_opy_
    if str(name).lower() == bstack1l1l1l1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ‟"):
        return bstack1l1l1l1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧ†")
    else:
        return bstack1lll111l1_opy_(self, name, default, skip)
def bstack11l1llll11_opy_(self):
    global CONFIG
    global bstack11111111l_opy_
    try:
        proxy = bstack11ll1111ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ‡")):
                proxies = bstack1l111lll1_opy_(proxy, bstack111l1l1ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l11l1111l_opy_ = proxies.popitem()
                    if bstack1l1l1l1_opy_ (u"ࠣ࠼࠲࠳ࠧ•") in bstack1l11l1111l_opy_:
                        return bstack1l11l1111l_opy_
                    else:
                        return bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ‣") + bstack1l11l1111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢ․").format(str(e)))
    return bstack11111111l_opy_(self)
def bstack1ll1ll1l1_opy_():
    return (bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ‥") in CONFIG or bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ…") in CONFIG) and bstack1ll1l11ll_opy_() and bstack1l11l1lll_opy_() >= version.parse(
        bstack11l11ll1l_opy_)
def bstack11lll1111l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1l1111l_opy_
    global bstack11l11l11l_opy_
    global bstack1l11111ll1_opy_
    CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ‧")] = str(bstack1l11111ll1_opy_) + str(__version__)
    bstack1l1ll111ll_opy_ = 0
    try:
        if bstack11l11l11l_opy_ is True:
            bstack1l1ll111ll_opy_ = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ ")))
    except:
        bstack1l1ll111ll_opy_ = 0
    CONFIG[bstack1l1l1l1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ ")] = True
    bstack111111l1l_opy_ = bstack1lllll1lll_opy_(CONFIG, bstack1l1ll111ll_opy_)
    logger.debug(bstack11l1l11ll_opy_.format(str(bstack111111l1l_opy_)))
    if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭‪")):
        bstack11llllll1l_opy_(bstack111111l1l_opy_, bstack1l1l1ll1_opy_)
    if bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭‫") in CONFIG and bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ‬") in CONFIG[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ‭")][bstack1l1ll111ll_opy_]:
        bstack1ll1l1111l_opy_ = CONFIG[bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ‮")][bstack1l1ll111ll_opy_][bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ ")]
    import urllib
    import json
    if bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ‰") in CONFIG and str(CONFIG[bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭‱")]).lower() != bstack1l1l1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ′"):
        bstack11ll111l11_opy_ = bstack11ll1111_opy_()
        bstack111l11lll_opy_ = bstack11ll111l11_opy_ + urllib.parse.quote(json.dumps(bstack111111l1l_opy_))
    else:
        bstack111l11lll_opy_ = bstack1l1l1l1_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭″") + urllib.parse.quote(json.dumps(bstack111111l1l_opy_))
    browser = self.connect(bstack111l11lll_opy_)
    return browser
def bstack1l11ll11l_opy_():
    global bstack1llllll1l1_opy_
    global bstack1l11111ll1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1ll1llll11_opy_
        if not bstack1ll1111ll11_opy_():
            global bstack111l11l1_opy_
            if not bstack111l11l1_opy_:
                from bstack_utils.helper import bstack111lllll1_opy_, bstack1l1l1l111l_opy_
                bstack111l11l1_opy_ = bstack111lllll1_opy_()
                bstack1l1l1l111l_opy_(bstack1l11111ll1_opy_)
            BrowserType.connect = bstack1ll1llll11_opy_
            return
        BrowserType.launch = bstack11lll1111l_opy_
        bstack1llllll1l1_opy_ = True
    except Exception as e:
        pass
def bstack111l1l1lll1_opy_():
    global CONFIG
    global bstack1l1ll11ll_opy_
    global bstack1l1llll1ll_opy_
    global bstack1l1l1ll1_opy_
    global bstack11l11l11l_opy_
    global bstack11ll11111l_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ‴")))
    bstack1l1ll11ll_opy_ = eval(os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ‵")))
    bstack1l1llll1ll_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ‶"))
    bstack11lll1l11_opy_(CONFIG, bstack1l1ll11ll_opy_)
    bstack11ll11111l_opy_ = bstack1l1llllll_opy_.bstack1l1ll1l1l_opy_(CONFIG, bstack11ll11111l_opy_)
    if cli.bstack1lll11l1l1_opy_():
        bstack1l11111l1_opy_.invoke(bstack1l1l1111ll_opy_.CONNECT, bstack1ll1lll1_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ‷"), bstack1l1l1l1_opy_ (u"ࠩ࠳ࠫ‸")))
        cli.bstack1lll1l11l1l_opy_(cli_context.platform_index)
        cli.bstack1lll1ll1lll_opy_(bstack111l1l1ll_opy_(bstack1l1llll1ll_opy_, CONFIG), cli_context.platform_index, bstack1111llll_opy_)
        cli.bstack1llllll1l11_opy_()
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡇࡑࡏࠠࡪࡵࠣࡥࡨࡺࡩࡷࡧࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤ‹") + str(cli_context.platform_index) + bstack1l1l1l1_opy_ (u"ࠦࠧ›"))
        return # skip all existing bstack111l1l1l1ll_opy_
    global bstack1ll11l11ll_opy_
    global bstack1ll1lll11_opy_
    global bstack1l1l1llll1_opy_
    global bstack1ll11lll11_opy_
    global bstack11ll11ll_opy_
    global bstack1ll1lll11l_opy_
    global bstack11l1l1ll_opy_
    global bstack1l111llll_opy_
    global bstack11111111l_opy_
    global bstack1lll111l1_opy_
    global bstack1l1lllll11_opy_
    global bstack1l1lll1l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1ll11l11ll_opy_ = webdriver.Remote.__init__
        bstack1ll1lll11_opy_ = WebDriver.quit
        bstack11l1l1ll_opy_ = WebDriver.close
        bstack1l111llll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ※") in CONFIG or bstack1l1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ‼") in CONFIG) and bstack1ll1l11ll_opy_():
        if bstack1l11l1lll_opy_() < version.parse(bstack11l11ll1l_opy_):
            logger.error(bstack1ll11ll11l_opy_.format(bstack1l11l1lll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11111111l_opy_ = RemoteConnection._1l1l11111l_opy_
            except Exception as e:
                logger.error(bstack1ll11l1l1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll111l1_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1lllll11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1lll1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1lll1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ‽"))
    bstack1l1l1ll1_opy_ = CONFIG.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ‾"), {}).get(bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ‿"))
    bstack11l11l11l_opy_ = True
    bstack1lll1lll1l_opy_(bstack1lll1ll1l1_opy_)
if (bstack11lll1ll111_opy_()):
    bstack111l1l1lll1_opy_()
@bstack111ll1llll_opy_(class_method=False)
def bstack111l1l1l11l_opy_(hook_name, event, bstack1l11ll11l1l_opy_=None):
    if hook_name not in [bstack1l1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ⁀"), bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ⁁"), bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⁂"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⁃"), bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ⁄"), bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ⁅"), bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⁆"), bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⁇")]:
        return
    node = store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⁈")]
    if hook_name in [bstack1l1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫ⁉"), bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ⁊")]:
        node = store[bstack1l1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭⁋")]
    elif hook_name in [bstack1l1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭⁌"), bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ⁍")]:
        node = store[bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨ⁎")]
    hook_type = bstack11l1111l11l_opy_(hook_name)
    if event == bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⁏"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_[hook_type], bstack1llll1llll1_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111ll11l11_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁐"): uuid,
            bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⁑"): bstack1lll11llll_opy_(),
            bstack1l1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ⁒"): bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭⁓"),
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⁔"): hook_type,
            bstack1l1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⁕"): hook_name
        }
        store[bstack1l1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⁖")].append(uuid)
        bstack111l1ll1l11_opy_ = node.nodeid
        if hook_type == bstack1l1l1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ⁗"):
            if not _111lll1111_opy_.get(bstack111l1ll1l11_opy_, None):
                _111lll1111_opy_[bstack111l1ll1l11_opy_] = {bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⁘"): []}
            _111lll1111_opy_[bstack111l1ll1l11_opy_][bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭⁙")].append(bstack111ll11l11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⁚")])
        _111lll1111_opy_[bstack111l1ll1l11_opy_ + bstack1l1l1l1_opy_ (u"ࠩ࠰ࠫ⁛") + hook_name] = bstack111ll11l11_opy_
        bstack111l1l11ll1_opy_(node, bstack111ll11l11_opy_, bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⁜"))
    elif event == bstack1l1l1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ⁝"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1l1lll1_opy_[hook_type], bstack1llll1llll1_opy_.POST, node, None, bstack1l11ll11l1l_opy_)
            return
        bstack11l11ll11l_opy_ = node.nodeid + bstack1l1l1l1_opy_ (u"ࠬ࠳ࠧ⁞") + hook_name
        _111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ ")] = bstack1lll11llll_opy_()
        bstack111l1l111l1_opy_(_111lll1111_opy_[bstack11l11ll11l_opy_][bstack1l1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁠")])
        bstack111l1l11ll1_opy_(node, _111lll1111_opy_[bstack11l11ll11l_opy_], bstack1l1l1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁡"), bstack111l1ll1111_opy_=bstack1l11ll11l1l_opy_)
def bstack111l1ll11ll_opy_():
    global bstack111l11l1lll_opy_
    if bstack1l111l11l_opy_():
        bstack111l11l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⁢")
    else:
        bstack111l11l1lll_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ⁣")
@bstack111111ll1_opy_.bstack111ll1l11l1_opy_
def bstack111l11ll1l1_opy_():
    bstack111l1ll11ll_opy_()
    if cli.is_running():
        try:
            bstack11ll11ll1l1_opy_(bstack111l1l1l11l_opy_)
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡴࠢࡳࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⁤").format(e))
        return
    if bstack1ll1l11ll_opy_():
        bstack1l1l1111l_opy_ = Config.bstack1l111l1l1l_opy_()
        bstack1l1l1l1_opy_ (u"ࠬ࠭ࠧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠾ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣ࡫ࡪࡺࡳࠡࡷࡶࡩࡩࠦࡦࡰࡴࠣࡥ࠶࠷ࡹࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠰ࡻࡷࡧࡰࡱ࡫ࡱ࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡱࡲࡳࠤࡃࠦ࠱࠭ࠢࡰࡳࡩࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡵࡹࡳࠦࡢࡦࡥࡤࡹࡸ࡫ࠠࡪࡶࠣ࡭ࡸࠦࡰࡢࡶࡦ࡬ࡪࡪࠠࡪࡰࠣࡥࠥࡪࡩࡧࡨࡨࡶࡪࡴࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࠢ࡬ࡨࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭ࡻࡳࠡࡹࡨࠤࡳ࡫ࡥࡥࠢࡷࡳࠥࡻࡳࡦࠢࡖࡩࡱ࡫࡮ࡪࡷࡰࡔࡦࡺࡣࡩࠪࡶࡩࡱ࡫࡮ࡪࡷࡰࡣ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠮ࠦࡦࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠭ࠧࠨ⁥")
        if bstack1l1l1111l_opy_.get_property(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪ⁦")):
            if CONFIG.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⁧")) is not None and int(CONFIG[bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⁨")]) > 1:
                bstack1l111lll11_opy_(bstack111l1ll1_opy_)
            return
        bstack1l111lll11_opy_(bstack111l1ll1_opy_)
    try:
        bstack11ll11ll1l1_opy_(bstack111l1l1l11l_opy_)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥ⁩").format(e))
bstack111l11ll1l1_opy_()