import re
import json
from playwright.sync_api import Playwright, APIRequestContext, expect, Page
from dotenv import load_dotenv; load_dotenv()
from os import getenv


# Karta a DB a API
cisloKarty, platnost, cvv, dbPassword, API_key = getenv("CISLO_KARTY"), getenv("PLATNOST_KARTY"), getenv("CVV_KARTY"), getenv("dbPassword"), getenv("API_key")


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


def get_order_id(page) -> str | None:
    try:
        order_locator = page.get_by_text(re.compile(r'Vaša objednávka číslo \d+'))
        if order_locator.count() > 0:
            order_text = order_locator.text_content()
            match = re.search(r'\d+', order_text)
            if match:
                order_id = match.group()
                print(f"✅ Číslo objednávky: {order_id}")
                return order_id
            else:
                print("❌ Číslo objednávky nebolo nájdené.")
        else:
            print("❌ Žiadny element s objednávkou nebol nájdený.")
    finally:
        print("✅ Funkcia get_order_id skoncila")


def update_order_state_api(request_context: APIRequestContext, order_id: str, api_key: str, data: dict) -> int | None:
    url = f"https://twww.dpdmojkurier.sk/integration-api/order/{order_id}/state"
    print("Request data:", json.dumps(data, indent=2))

    try:
        response = request_context.put(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-API-KEY": api_key
            },
            data=json.dumps(data)
        )

        if response.status == 200:
            response_data = response.json()
            print("✅ Úspešne prevzatý balík do Lockera:", response_data)
        else:
            print(f"❌ Chyba: {response.status}, {response.text()}")
        return response.status

    except Exception as e:
        print(f"❌ Výnimka: {e}")
        return None

# Objednávka na Locker
def test_l2h_cod_dpl(page: Page, playwright: Playwright) -> None:
        page.goto("https://twww.dpdmojkurier.sk/")
        page.get_by_role("button", name="Prijať všetko").click()
        page.get_by_role("link", name="Poslať zásielku").first.click()
        page.get_by_role("button", name="Pokračovať").first.click()
        page.wait_for_timeout(timeout=2000)

        #Sender
        #Sender
        page.get_by_role("textbox", name="Meno").fill(sMeno)
        page.get_by_role("textbox", name="Priezvisko").fill(sPriezvisko)
        page.get_by_role("textbox", name="Email").fill(sEmail)
        page.get_by_role("textbox", name="Telefón").fill(sTel)
        page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(sMesto)
        page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(sPSC)
        page.get_by_role("textbox", name="Ulica").fill(sUlica)
        page.get_by_role("textbox", name="Popisné číslo").fill(sPopisneCislo)
        page.get_by_text("Pobočka DPD BRATISLAVA").click()
        page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
        page.get_by_role("button", name="Pokračovať").click()
        page.wait_for_timeout(timeout=2000)

        #Reciever
        page.get_by_role("textbox", name="Meno").clear()
        page.get_by_role("textbox", name="Meno").fill(rMeno)
        page.get_by_role("textbox", name="Priezvisko").clear()
        page.get_by_role("textbox", name="Priezvisko").fill(rPriezvisko)
        page.get_by_role("textbox", name="Email").fill(rEmail)
        page.get_by_role("textbox", name="Telefón").fill(rTel)

        #poslat na domacu adresu
        page.get_by_role("checkbox", name="Poslať na adresu Poslať do").uncheck()
        page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(rMesto)
        page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(rPSC)
        page.get_by_role("textbox", name="Ulica").fill(rUlica)
        page.get_by_role("textbox", name="Popisné číslo").fill(rPopisneCislo)
        page.get_by_role("textbox", name="Popisné číslo").click()
        page.wait_for_timeout(timeout=2000)
        page.get_by_role("button", name="Pokračovať").click()

        # Package
        page.get_by_role("img", name="add-parcel-icon").click()
        page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
        page.get_by_role("img", name="add-parcel-icon").click()
        page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
        page.get_by_role("button", name="Pokračovať").click()
        page.wait_for_timeout(timeout=2000)

        # Zhrnutie objednavky
        # page.get_by_role("checkbox", name="Prepravný štítok Digitálny").uncheck()
        page.get_by_role("button", name="Pokračovať na výber platby").click()

        # Potvrdenie objednavky
        page.get_by_role("button", name="Potvrdiť objednávku").click()

        # Platba kartou
        assert cisloKarty and platnost and cvv, "Chýbajú hodnoty z .env súboru!"
        page.wait_for_url("https://moja.tatrabanka.sk/cgi-bin/e-commerce/start/cardpay")
        page.get_by_role("textbox", name="Číslo karty").fill(cisloKarty)
        page.get_by_role("textbox", name="Platnosť").fill(platnost)
        page.get_by_role("textbox", name="CVV").fill(cvv)
        page.get_by_role("button", name="ZAPLATIŤ").click()
        page.wait_for_timeout(timeout=2000)

        page.get_by_role("button", name="Pokračovať").click()
        expect(page.get_by_role("heading", name="Hotovo")).to_be_visible()

        # --- ORDER ID získanie ---
        order_id = get_order_id(page)
        assert order_id is not None, "Objednávka nebola nájdená"

        # --- API volanie cez Playwright ---
        request_context = playwright.request.new_context()
        api_key = API_key
        data = {
            "state": "RECEIVED",
            "pudoCode": "SK20271"
        }

        status = update_order_state_api(request_context, order_id, api_key, data)
        assert status == 200, f"API nevrátilo 200, ale {status}"

        # Čistenie
        request_context.dispose()

