
from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the-internet.herokuapp.com home page.

    The home page is the entry point for every test in the framework - every test
    must navigate through the UI rather than deep-linking, so each navigable
    destination is exposed here as a method.
    """
    PATH: str = "/"

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Welcome to the-internet")).to_be_visible()
    
    def click_notification_messages_link(self) -> None:
        self.page.get_by_role("link", name="Notification Messages").click()

    def click_challenging_dom_link(self) -> None:   
        self.page.get_by_role("link", name="Challenging DOM").click()