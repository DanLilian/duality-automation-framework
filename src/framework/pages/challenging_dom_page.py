from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class ChallengingDomPage(BasePage):
    PATH: str = "/challenging_dom"

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Challenging DOM")).to_be_visible()