import datetime
from playwright.sync_api import sync_playwright

def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")

def test_main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.python.org/")
        with open("python_org_{0}.html".format(current_timestamp()), "w", encoding='utf-8') as f:
            f.write(page.content())
        browser.close()

test_main()