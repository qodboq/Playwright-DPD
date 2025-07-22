from playwright.sync_api import expect
from dotenv import load_dotenv; load_dotenv()
from os import getenv

# Login kuriér
kLogin, kPassword = getenv("kLogin"), getenv("kPassword")
# Login sukromna osoba
sLogin, sPassword = getenv("sLogin"), getenv("sPassword")
# Login firemny zakaznik
fLogin, fPassword = getenv("fLogin"), getenv("fPassword")

# Test na prihlasenie a odhlasenie Kurier, Sukromna osoba, Firma

def test_login_logout(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    # Login/Logout kurier
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill(kLogin)
    page.locator("#password").click()
    page.locator("#password").fill(kPassword)
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Erik Valigursky+Kurier|")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()

    # Login/Logout sukromna osoba
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill(sLogin)
    page.locator("#password").click()
    page.locator("#password").fill(sPassword)
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Súkromný zákazník Erik erik.")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()

    # Login/Logout firemny zakaznik
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill(fLogin)
    page.locator("#password").click()
    page.locator("#password").fill(fPassword)
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Firemný zákazník Erik")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()
    print("✅ Testy Login/Logout prebehli úspešne.")

    # ---------------------
