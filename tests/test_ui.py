from playwright.sync_api import expect
from src.ui import StartPage, ApiReferencePage


def test_get_started_link(page):
    start_page = StartPage(page)
    start_page.open()
    start_page.get_started_link.click()
    api_reference_page = ApiReferencePage(page)
    expect(api_reference_page.heading_label).to_be_visible()
