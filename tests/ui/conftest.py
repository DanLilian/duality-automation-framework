# Pytest fixtures for UI tests

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