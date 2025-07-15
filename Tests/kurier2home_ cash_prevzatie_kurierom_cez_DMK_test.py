import re
import mysql.connector
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv
import os

# Načítanie údajov z .env
load_dotenv()
cisloKarty = os.getenv("CISLO_KARTY")
platnost = os.getenv("PLATNOST_KARTY")
cvv = os.getenv("CVV_KARTY")
dbPassword = os.getenv("dbPassword")


# Objednávka na zvoz kuriérom
@pytest.fixture
def test_vytvor_objednavku(page: Page):
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").nth(1).click()
    page.wait_for_timeout(timeout=2000)

    # Odosielateľ
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

    # Príjemca
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

    # Balík
    page.get_by_text("Pridať balík").click()
    page.locator("div").filter(
        has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")
    ).get_by_role("button").click()
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Pokračovať na výber platby").click()
    page.get_by_role("button", name="Potvrdiť objednávku").click()

    # Platobná brána
    assert cisloKarty and platnost and cvv, "Chýbajú hodnoty z .env súboru!"
    page.wait_for_url("https://moja.tatrabanka.sk/cgi-bin/e-commerce/start/cardpay")
    page.get_by_role("textbox", name="Číslo karty").fill(cisloKarty)
    page.get_by_role("textbox", name="Platnosť").fill(platnost)
    page.get_by_role("textbox", name="CVV").fill(cvv)
    page.get_by_role("button", name="ZAPLATIŤ").click()
    page.wait_for_timeout(timeout=5000)

    # Získanie čísla balíka z DB
    conn = mysql.connector.connect(
        host="10.57.50.168",
        port=3306,
        database="cashapp_test",
        user="cashapp",
        password=dbPassword
    )
    cursor = conn.cursor()
    cursor.execute("SELECT o10_parcel_number FROM o10_parcel ORDER BY o01_order_id DESC LIMIT 1;")
    parcel_number = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(f"(✅) Zásielka {parcel_number} na zvoz kuriérom bola vytvorená")
    return parcel_number


def test_prijatie_zasielky_kurierom(page: Page, test_vytvor_objednavku: str) -> None:
    parcel_number = test_vytvor_objednavku
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").fill("erik.valigursky+ku@bootiq.io")
    page.locator("#password").fill("123123")
    page.locator("#password").press("Enter")

    # Príjem zásielky
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Nastavenie").click()
    page.get_by_role("button", name="Príjem zásielky").click()
    page.get_by_label("").fill(parcel_number)
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Hotovosť").check()
    page.get_by_role("button", name="Zásielka uhradená").click()
    assert page.get_by_role("heading", name="Úspešne odoslané")
    print(f"(✅) Zásielka {parcel_number} bola prijatá do prepravy kuriérom")
