from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class NotificationPage(BasePage):
    PATH: str = "/notification_message_rendered"

    def wait_for_loaded(self) -> None:
        """Wait until the 'Click here" link test is loaded and visible"""
        expect(self.page.get_by_role("link", name="Click here")).to_be_visible()

    def click_link(self) -> None:
        """Click the 'Click here' link that triggers the notification banner."""
        self.page.get_by_role("link", name="Click here").click()

    def read_banner_text(self) -> str:
        """Return the current notification banner text."""
        return self.page.locator("#flash").inner_text()