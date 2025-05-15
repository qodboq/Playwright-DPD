import re
from playwright.sync_api import APIRequestContext, expect, Page, Playwright
from dotenv import load_dotenv
import json
import os

# Načítanie údajov z .env
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


def test_vo2_bbx_dpl_cod(page: Page, playwright: Playwright) -> None:


        # --- UI FLOW ---
        page.goto("https://twww.dpdmojkurier.sk/")
        page.get_by_role("button", name="Prijať všetko").click()
        page.get_by_role("link", name="Poslať zásielku").first.click()
        page.get_by_role("button", name="Pokračovať").first.click()
        page.wait_for_timeout(timeout=2000)
        page.get_by_role("textbox", name="Meno").fill("Erik")
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
        page.wait_for_timeout(timeout=2000)

        page.get_by_role("textbox", name="Meno").clear()
        page.get_by_role("textbox", name="Meno").fill("Test")
        page.get_by_role("textbox", name="Priezvisko").clear()
        page.get_by_role("textbox", name="Priezvisko").fill("Test")
        page.get_by_role("textbox", name="Email").fill("email@email.com")
        page.get_by_role("textbox", name="Telefón").fill("+421948328484")
        page.get_by_text("AlzaBox (N-CENTRO)").click()
        page.get_by_role("button", name="Pokračovať").click()

        page.get_by_role("img", name="add-parcel-icon").click()
        page.locator("div").filter(has_text=re.compile(r"^váha:do 1 kgdĺžka:45 cmšírka:35 cmvýška:20 cmPridať$")).get_by_role("button").click()
        page.get_by_role("checkbox", name="Poslať dobierkový balík").check()
        page.wait_for_timeout(timeout=2000)
        page.get_by_role("textbox", name="Dobierková suma").fill("1")
        page.get_by_role("textbox", name="IBAN").fill("SK4075000000007777777777")
        page.get_by_role("textbox", name="Variabilný symbol").fill("2221178")
        page.get_by_role("button", name="Pokračovať").click()
        page.get_by_role("button", name="Pokračovať na výber platby").click()
        page.get_by_role("button", name="Potvrdiť objednávku").click()
        page.wait_for_timeout(timeout=2000)

        assert cisloKarty and platnost and cvv, "Chýbajú hodnoty z .env súboru!"
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
        api_key = "21c24472-ivua-2590-jluw-6b4dee64ddaa"
        data = {
            "state": "RECEIVED",
            "pudoCode": "SK20271"
        }

        status = update_order_state_api(request_context, order_id, api_key, data)
        assert status == 200, f"API nevrátilo 200, ale {status}"

        # Čistenie
        request_context.dispose()

