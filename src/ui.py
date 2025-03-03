from playwright.sync_api import Page, Locator


class BasePage:
    page: Page
    url: str

    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url

    def open(self):
        self.page.goto(url=self.url)


class StartPage(BasePage):
    get_started_link: Locator

    def __init__(self, page: Page):
        super().__init__(page, "/")
        self.get_started_link = page.get_by_role("link", name="Get started")


class ApiReferencePage(BasePage):
    heading_label: Locator

    def __init__(self, page: Page):
        super().__init__(page, "/docs/intro")
        self.heading_label = self.page.get_by_role("heading", name="Installation")
