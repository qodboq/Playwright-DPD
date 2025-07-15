import re
from playwright.sync_api import Playwright, sync_playwright, expect, Page
from dotenv import load_dotenv
import os


# Načítanie údajov z .env
load_dotenv()
cisloKarty = os.getenv("CISLO_KARTY")
platnost = os.getenv("PLATNOST_KARTY")
cvv = os.getenv("CVV_KARTY")

# Login
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("lucia.piesova+user0402@bootiq.io")
    page.locator("#password").click()
    page.locator("#password").fill("17101989")
    page.get_by_role("button", name="Prihlásenie").click()

# Vyber prepravy
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").nth(1).click()

# Sender
    page.locator("span").filter(has_text="Meno").get_by_role("textbox").click()
    page.locator("span").filter(has_text="Meno").get_by_role("textbox").fill("Lucia")
    page.get_by_role("menuitem", name="Lucia Piešová, Prostredná 19").click()
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()

# Reciver
    page.get_by_role("button", name="Pridať príjemcu").click()
    page.get_by_role("row", name="Lucia Piešová Riazanská 5,").get_by_role("button").nth(1).click()
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

# Zásielka
    page.get_by_role("img", name="add-parcel-icon").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Pokračovať na výber platby").click()

# Vyber platby a platba na PB
    page.get_by_role("button", name="Potvrdiť objednávku").click()
    page.get_by_role("textbox", name="Číslo karty").click()
    page.get_by_role("textbox", name="Číslo karty").fill("4405778611779996")
    page.locator("#cp-manual-input-expiration div").filter(has_text="Platnosť").nth(2).click()
    page.get_by_text("Platnosť").click()
    page.get_by_role("textbox", name="Platnosť").fill("07 / 28")
    page.get_by_text("CVV").click()
    page.get_by_role("textbox", name="CVV").fill("798")
    page.get_by_role("button", name="ZAPLATIŤ 7,81 EUR").click()
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()


    page.get_by_role("menuitem", name="Odhlásenie").click()

    # Login do kurierskeho uctu
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("lucia.piesova+kurier262@bootiq.io")
    page.locator("#password").click()
    page.locator("#password").fill("17101989")
    page.get_by_role("button", name="Prihlásenie").click()

    # Prevzatie balika
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Môj profil").click()
    page.get_by_role("button", name="Príjem zásielky").click()
    page.get_by_label("").click()
    page.get_by_label("").fill("06705530008906")
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Platobná brána").check()
    page.get_by_role("button", name="Zásielka uhradená").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
