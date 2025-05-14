import re
from playwright.sync_api import expect, sync_playwright
from dotenv import load_dotenv
from prevzatie_balika_API_sync import update_order_state
import os
# DPD Shop2Shop - Tento test vytvori objednavku na Locker 2 Locker s Dobierkou, zaplati za dopravu a nasledne ju prevezme do prepravy do Lockera

load_dotenv()

cisloKarty = os.getenv("CISLO_KARTY")
platnost = os.getenv("PLATNOST_KARTY")
cvv = os.getenv("CVV_KARTY")


def get_order_id(page) -> str | None:
    try:
        order_locator = page.get_by_text(re.compile(r'Vaša objednávka číslo \d+'))
        if order_locator.count() > 0:
            order_text = order_locator.text_content()
            match = re.search(r'\d+', order_text)
            if match:
                order_id = match.group()
                print(f"Číslo objednávky: {order_id}")
                return order_id
            else:
                print("Číslo objednávky nebolo nájdené.")
        else:
            print("Žiadny element s objednávkou nebol nájdený.")
    finally:
        print("funkcia get_order_id skoncila")


def test_vo2_bbx_dpl_cod():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://twww.dpdmojkurier.sk/")
        page.get_by_role("button", name="Prijať všetko").click()
        page.get_by_role("link", name="Poslať zásielku").first.click()
        page.get_by_role("button", name="Pokračovať").first.click()
        page.get_by_role("textbox", name="Meno").wait_for(state="visible")
        page.get_by_role("textbox", name="Meno").fill("Erik")
        page.get_by_role("textbox", name="Priezvisko").wait_for(state="visible")
        page.get_by_role("textbox", name="Priezvisko").fill("Valigurský")
        page.get_by_role("textbox", name="Email").fill("erik.valigursky@bootiq.io")
        page.get_by_role("textbox", name="Telefón").fill("+421948328484")
        page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Bratislava")
        page.get_by_role("menuitem", name="Bratislava Devín -").click()
        page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").nth(1).click()
        page.get_by_role("textbox", name="Ulica").fill("Ulica")
        page.get_by_role("textbox", name="Popisné číslo").fill("1")
        page.get_by_text("DPDBox (Avion)").click()
        page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
        page.get_by_role("button", name="Pokračovať").click()

        expect(page.get_by_role("textbox", name="Meno")).to_be_visible()
        page.get_by_role("textbox", name="Meno").clear(timeout=5000)
        page.get_by_role("textbox", name="Meno").fill("Test")
        page.get_by_role("textbox", name="Priezvisko").clear(timeout=5000)
        page.get_by_role("textbox", name="Priezvisko").fill("Test")
        page.get_by_role("textbox", name="Email").fill("email@email.com")
        page.get_by_role("textbox", name="Telefón").fill("+421948328484")

        expect(page.get_by_text("AlzaBox (N-CENTRO)")).to_be_visible()
        page.get_by_text("AlzaBox (N-CENTRO)").click()
        expect(page.get_by_role("button", name="Pokračovať")).to_be_enabled()
        page.get_by_role("button", name="Pokračovať").click()

        page.get_by_role("img", name="add-parcel-icon").click()
        page.locator("div").filter(has_text=re.compile(r"^váha:do 1 kgdĺžka:45 cmšírka:35 cmvýška:20 cmPridať$")).get_by_role("button").click()
        page.get_by_role("checkbox", name="Poslať dobierkový balík").check()

        page.get_by_role("textbox", name="Dobierková suma").clear(timeout=5000)
        page.get_by_role("textbox", name="Dobierková suma").fill("1")
        page.get_by_role("textbox", name="IBAN").fill("SK4075000000007777777777")
        page.get_by_role("textbox", name="Variabilný symbol").fill("2221178")
        page.get_by_role("button", name="Pokračovať").click()
        page.get_by_role("button", name="Pokračovať na výber platby").click()
        page.get_by_role("button", name="Potvrdiť objednávku").click()

        assert cisloKarty and platnost and cvv, "Chýbajú hodnoty z .env súboru!"
        page.get_by_role("textbox", name="Číslo karty").fill(cisloKarty)
        page.get_by_role("textbox", name="Platnosť").fill(platnost)
        page.get_by_role("textbox", name="CVV").fill(cvv)
        page.get_by_role("button", name="ZAPLATIŤ 2,85 EUR").click()

        page.get_by_role("button", name="Pokračovať").click()
        expect(page.get_by_role("heading", name="Hotovo")).to_be_visible()

        order_id2 = get_order_id(page)
        assert order_id2 is not None, "Objednávka nebola nájdená, nemožno pokračovať."

        api_key = "21c24472-ivua-2590-jluw-6b4dee64ddaa"
        data = {
            "state": "RECEIVED",
            "pudoCode": "SK20271"
        }

        response_status_api = update_order_state(order_id2, api_key, data)
        assert response_status_api == 200
        #page.screenshot(path="screenshot.png")

        context.close()
        browser.close()
