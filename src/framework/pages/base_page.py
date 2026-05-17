from playwright.sync_api import Page

from framework.config.settings import BASE_URL


class BasePage:
    """Parent class for all page objects.

    Subclasses override PATH (their route on the base URL) and wait_for_loaded
    (a page-specific readiness check beyond the browser's load event).
    """
    PATH: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page
    
    def navigate(self) -> None:
        url = F"{BASE_URL}{self.PATH}"
        self.page.goto(url)
        self.wait_for_loaded()
    
    def wait_for_loaded(self) -> None:
        # this method is empty, each subclass will override differently
        pass

    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(path=f"output/reports/{name}.png")