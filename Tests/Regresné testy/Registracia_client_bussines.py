
import time
from playwright.sync_api import Playwright, expect

# Generovanie emailu
def generate_email() -> str:

    timestamp = int(time.time())  # kolko sekund uplynulo od 1. januára 1970, 00:00:00 UTC
    return f"erik.valigursky+{timestamp}@bootiq.sk"

# Registracia firemneho zakaznika
def test_registracia_client_bussines(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Firemný zákazník").nth(1).click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("link", name="Nemáte účet? Registrujte sa!").click()
    page.get_by_role("textbox", name="IČO").click()
    page.get_by_role("textbox", name="IČO").fill("47165367")
    page.get_by_role("textbox", name="Telefón").click()
    page.get_by_role("textbox", name="Telefón").fill("+421948328484")
    page.get_by_role("textbox", name="Meno").click()
    page.get_by_role("textbox", name="Meno").fill("Test")
    page.get_by_role("textbox", name="Priezvisko").fill("Test")
    page.get_by_role("textbox", name="Email").fill(generate_email())
    page.locator("#password").click()
    page.locator("#password").fill("123123")
    page.get_by_role("checkbox", name="Súhlasím so všeobecnými obchodnými podmienkami a prečítal som si vyhlásenie o").check()
    page.get_by_role("checkbox", name="Oboznámil/a som sa a súhlasím").check()
    page.get_by_role("checkbox", name="Udeľujem súhlas so spracúvaním svojich osobných údajov za účelom zasielania").check()
    page.get_by_role("button", name="Vytvoriť účet").click()
    expect(page.get_by_role("heading", name="Dokončenie registrácie")).to_be_visible()
    print("✅ Registrácia bola úspešne dokončená.")
    # ---------------------
    context.close()
    browser.close()

