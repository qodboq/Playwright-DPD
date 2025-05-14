import json
import aiohttp

async def update_order_state(order_id: str, api_key: str, data: dict) -> int | None:
    """
    Aktualizuje stav objednávky cez DPD API.

    :param order_id: ID objednávky, ktoré sa má aktualizovať
    :param api_key: API kľúč na autorizáciu požiadavky
    :param data: Dict obsahujúci nový stav objednávky a prípadně kód pick-up pointu
    :return: HTTP status code ak je volanie úspešné, inak None
    """
    url = f"https://twww.dpdmojkurier.sk/integration-api/order/{order_id}/state"
    print("Request data:", json.dumps(data, indent=2))

    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-API-KEY": api_key
                },
                json=data
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    print("Úspešne Prevzatý balík do Lockera:", response_data)
                    return response.status
                else:
                    print(f"Chyba: {response.status}, {await response.text()}")
                    return response.status
        except Exception as e:
            print(f"Nastala chyba: {e}")
            return None
