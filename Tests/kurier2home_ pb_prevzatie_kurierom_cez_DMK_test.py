import re
import mysql.connector
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv; load_dotenv()
from os import getenv

# Karta a DB
cisloKarty, platnost, cvv, dbPassword = getenv("CISLO_KARTY"), getenv("PLATNOST_KARTY"), getenv("CVV_KARTY"), getenv("dbPassword")

# Sender
sMeno, sPriezvisko, sEmail, sTel, sMesto, sPSC, sUlica, sPopisneCislo = (
    getenv("sMeno"), getenv("sPriezvisko"), getenv("sEmail"), getenv("sTel"),
    getenv("sMesto"), getenv("sPSC"), getenv("sUlica"), getenv("sPopisneCislo")
)

# Receiver
rMeno, rPriezvisko, rEmail, rTel, rMesto, rPSC, rUlica, rPopisneCislo = (
    getenv("rMeno"), getenv("rPriezvisko"), getenv("rEmail"), getenv("rTel"),
    getenv("rMesto"), getenv("rPSC"), getenv("rUlica"), getenv("rPopisneCislo")
)

# Login kuriér
kLogin, kPassword = getenv("kLogin"), getenv("kPassword")


# Objednávka na zvoz kuriérom
@pytest.fixture
def test_vytvor_objednavku(page: Page)->str:
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").nth(1).click()
    page.wait_for_timeout(timeout=2000)

    # Sender
    page.get_by_role("textbox", name="Meno").fill(sMeno)
    page.get_by_role("textbox", name="Priezvisko").fill(sPriezvisko)
    page.get_by_role("textbox", name="Email").fill(sEmail)
    page.get_by_role("textbox", name="Telefón").fill(sTel)
    page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(sMesto)
    page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(sPSC)
    page.get_by_role("textbox", name="Ulica").fill(sUlica)
    page.get_by_role("textbox", name="Popisné číslo").fill(sPopisneCislo)
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Receiver
    page.get_by_role("textbox", name="Meno").fill(rMeno)
    page.get_by_role("textbox", name="Priezvisko").fill(rPriezvisko)
    page.get_by_role("textbox", name="Email").fill(rEmail)
    page.get_by_role("textbox", name="Telefón").fill(rTel)
    page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(rMesto)
    page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(rPSC)
    page.get_by_role("textbox", name="Ulica").fill(rUlica)
    page.get_by_role("textbox", name="Popisné číslo").fill(rPopisneCislo)
    page.get_by_role("textbox", name="Popisné číslo").click()
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
    page.get_by_role("textbox", name="Login").fill(kLogin)
    page.locator("#password").fill(kPassword)
    page.locator("#password").press("Enter")

    # Príjem zásielky
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Nastavenie").click()
    page.get_by_role("button", name="Príjem zásielky").click()
    page.get_by_label("").fill(parcel_number)
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Karta").check()
    page.get_by_role("button", name="Zásielka uhradená").click()
    assert page.get_by_role("heading", name="Úspešne odoslané")
    print(f"(✅) Zásielka {parcel_number} bola prijatá do prepravy kuriérom")
