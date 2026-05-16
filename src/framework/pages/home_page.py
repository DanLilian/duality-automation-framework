from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class HomePage(BasePage):
    PATH: str = "/"

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Welcome to the-internet")).to_be_visible()
    
    def click_notification_messages_link(self) -> None:
        self.page.get_by_role("link", name="Notification Messages").click()