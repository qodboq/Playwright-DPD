import json
import requests

def update_order_state(order_id: str, api_key: str, data: dict) -> int | None:
    url = f"https://twww.dpdmojkurier.sk/integration-api/order/{order_id}/state"
    print("Request data:", json.dumps(data, indent=2))

    try:
        response = requests.put(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-API-KEY": api_key
            },
            json=data
        )

        if response.status_code == 200:
            response_data = response.json()
            print("Úspešne Prevzatý balík do Lockera:", response_data)
            return response.status_code
        else:
            print(f"Chyba: {response.status_code}, {response.text}")
            return response.status_code
    except Exception as e:
        print(f"Nastala chyba: {e}")
        return None
