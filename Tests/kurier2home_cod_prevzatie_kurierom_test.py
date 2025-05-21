import re
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv
import os

# Načítanie údajov z .env
load_dotenv()
cisloKarty = os.getenv("CISLO_KARTY")
platnost = os.getenv("PLATNOST_KARTY")
cvv = os.getenv("CVV_KARTY")

# Objednavka na zvoz Kurierom
@pytest.fixture
def vytvor_objednavku(page: Page) -> str:
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").nth(1).click()
    page.wait_for_timeout(timeout=2000)

    # Sender
    page.get_by_role("textbox", name="Meno").fill("Erik")
    page.get_by_role("textbox", name="Priezvisko").fill("Valigurský")
    page.get_by_role("textbox", name="Email").fill("erik.valigursky@bootiq.sk")
    page.get_by_role("textbox", name="Telefón").fill("+421948328484")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Opoj")
    page.get_by_role("menuitem", name="Opoj -").click()
    page.get_by_role("textbox", name="Ulica").fill("Opoj")
    page.get_by_role("textbox", name="Popisné číslo").fill("108")
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Prijemca
    page.get_by_role("textbox", name="Meno").fill("Test")
    page.get_by_role("textbox", name="Priezvisko").fill("Test")
    page.get_by_role("textbox", name="Email").fill("email@email.com")
    page.get_by_role("textbox", name="Telefón").fill("+421123123123")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Poprad")
    page.get_by_role("menuitem", name="Poprad -").click()
    page.get_by_role("textbox", name="Ulica").fill("Ulica")
    page.get_by_role("textbox", name="Popisné číslo").fill("1")
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Balik
    page.get_by_text("Pridať balík").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("checkbox", name="Poslať dobierkový balík").check()
    page.wait_for_timeout(timeout=2000)

    # Dobierka
    page.get_by_role("textbox", name="Dobierková suma").fill("1")
    page.get_by_role("textbox", name="IBAN").fill("SK4075000000007777777777")
    page.get_by_role("textbox", name="Variabilný symbol").fill("2221178")
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Pokračovať na výber platby").click()
    page.get_by_role("radio", name="Platba pri vyzdvihnutí balíka").check()

    # Očakávaj odpoveď
    with page.expect_response(lambda res: "api/cart/createOrder" in res.url and res.status == 200) as response_info:
        page.get_by_role("button", name="Potvrdiť objednávku").click()

    response = response_info.value
    data = response.json()
    parcel_number = data["o10_parcel_number"]
    assert parcel_number is not None, "Chýba o10_parcel_number v odpovedi!"
    return parcel_number


def test_prijatie_zasielky_kurierom(page: Page, vytvor_objednavku: str) -> None:
    parcel_number = vytvor_objednavku
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").fill("erik.valigursky+ku@bootiq.io")
    page.locator("#password").fill("123123")
    page.locator("#password").press("Enter")

    # Príjem zásielky
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Nastavenie").click()
    page.get_by_role("button", name="Príjem zásielky").click()
    page.get_by_label("").fill(parcel_number)  # uprav na lepší selector ale asi lepsi nie je
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Hotovosť").check()
    page.get_by_role("button", name="Zásielka uhradená").click()
    assert page.get_by_role("heading", name="Úspešne odoslané")
