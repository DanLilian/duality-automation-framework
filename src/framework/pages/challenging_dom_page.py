import re
from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class ChallengingDomPage(BasePage):
    PATH: str = "/challenging_dom"

    # Button label → CSS class on the styled <a> element
    BUTTON_VARIANTS = ("default", "alert", "success")

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Challenging DOM")).to_be_visible()

    def click_button(self, variant: str) -> None:
        """Click the button of the given variant: 'default', 'alert', or 'success'."""
        self.page.locator(f"a.button.{variant}").first.click()

    def read_answer(self) -> int:
        """Return the current Answer numeric value."""
        text = self.page.locator("#content .large-2.columns canvas").get_attribute("data-answer") or ""
        if not text:
            text = self.page.locator(".large-2.columns").inner_text()
        match = re.search(r"\d+", text)
        if not match:
            raise ValueError(f"Could not parse answer from: {text!r}")
        return int(match.group())