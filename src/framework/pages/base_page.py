from playwright.sync_api import Page

from framework.config.settings import BASE_URL

# TODO: comment needed here
class BasePage:
    PATH: str = ""

    # TODO: Comment needed here too
    def __init__(self, page: Page) -> None:
        self.page = page
    
    # TODO: Comment needed here
    def navigate(self) -> None:
        url = F"{BASE_URL}{self.PATH}"
        self.page.goto(url)
        self.wait_for_loaded()
    
    # TODO: Comment needed here
    def wait_for_loaded(self) -> None:
        # this method is empty, each subclass will override differently
        pass

    # TODO: Comment needed here
    def take_screenshot(self, name: str) -> None:
        self.page.screenshot(path=f"output/reports/{name}.png")