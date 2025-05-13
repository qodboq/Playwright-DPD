import json
from playwright.sync_api import sync_playwright

import json
from playwright.sync_api import sync_playwright

def update_order_state(order_id, api_key, data):
    # Zmeňte hodnoty podľa vašich potrieb
    url = f"https://twww.dpdmojkurier.sk/integration-api/order/{order_id}/state"  # Použitie f-string

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Vykonanie PUT požiadavky
            response = page.request.put(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-API": "",  # Ak je potrebné, zadajte hodnotu
                    "X-API-KEY": api_key
                },
                data=json.dumps(data)  # Serializujeme dáta do JSON formátu
            )

            # Skontrolujte stavový kód odpovede
            if response.status == 200:
                response_data = response.json()  # Získajte JSON dáta z odpovede
                print("Úspešne aktualizované:", response_data)
            else:
                print(f"Chyba: {response.status}, {response.text}")  # Opravené na response.text

        except Exception as e:
            print(f"Nastala chyba: {e}")

        finally:
            browser.close()  # Zatvorenie prehliadača

# Príklad volania funkcie
order_id = 8604
api_key = "21c24472-ivua-2590-jluw-6b4dee64ddaa"  # Zadajte váš API kľúč
data = {
    "state": "RECEIVED",
    "variableSymbol": None,
    "pudoCode": "SK20271",
    "metadata": {
        "paymentType": "CARD",
        "paymentReference": "",
        "amount": "2",
        "currency": "EUR"
    }
}

update_order_state(order_id, api_key, data)