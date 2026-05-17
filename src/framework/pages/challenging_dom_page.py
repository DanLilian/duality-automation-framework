import re
from playwright.sync_api import expect
from framework.pages.base_page import BasePage


class ChallengingDomPage(BasePage):
    PATH: str = "/challenging_dom"

    BUTTON_VARIANTS = ("default", "alert", "success")

    def wait_for_loaded(self) -> None:
        expect(self.page.get_by_role("heading", name="Challenging DOM")).to_be_visible()

    def click_button(self, variant: str) -> None:
        if variant == "default":
            locator = self.page.locator("a.button:not(.alert):not(.success)")
        elif variant == "alert":
            locator = self.page.locator("a.button.alert")
        elif variant == "success":
            locator = self.page.locator("a.button.success")
        else:
            raise ValueError(f"Unknown button variant: {variant}")
        locator.first.click()

    def read_answer(self) -> int:
        # The answer is rendered onto a <canvas> via JavaScript - it's pixels, not DOM text.
        # However, the inline <script> tag that draws it contains the literal call:
        #   canvas.strokeText('Answer: 80118', 90, 112);
        # We read the script's text content and extract the number from there.
        scripts = self.page.locator("script").all()
        for script in scripts:
            content = script.inner_text()
            if "strokeText" in content and "Answer" in content:
                match = re.search(r"Answer:\s*(\d+)", content)
                if match:
                    return int(match.group(1))
        raise ValueError("Could not find Answer in any script tag on the page.")