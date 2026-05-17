"""Pytest fixtures for UI tests.

Page-object fixtures live here rather than in the root conftest so they only
load for UI tests. The home_page fixture auto-navigates to the home page;
other page-object fixtures only construct, because reaching them is part of
each test's scenario (per the assignment's UI-navigation requirement).
"""
import pytest
from playwright.sync_api import Page

from framework.pages.home_page import HomePage
from framework.pages.notification_page import NotificationPage
from framework.pages.challenging_dom_page import ChallengingDomPage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    home = HomePage(page)
    home.navigate()
    return home

@pytest.fixture
def notification_page(page: Page) -> NotificationPage:
    return NotificationPage(page)


@pytest.fixture
def challenging_dom_page(page: Page) -> ChallengingDomPage:
    return ChallengingDomPage(page)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on test failure for UI tests."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            screenshot_path = f"output/reports/{item.name}_failure.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n[screenshot saved] {screenshot_path}")
            except Exception:
                pass