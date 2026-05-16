from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class NotificationPage(BasePage):
    PATH: str = "/notification_message_rendered"

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Notification Message")).to_be_visible()