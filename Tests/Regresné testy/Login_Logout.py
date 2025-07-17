from playwright.sync_api import Playwright, expect

# Test na prihlasenie a odhlasenie Kurier, Sukromna osoba, Firma

def test_login_logout(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    # Login/Logout kurier
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("erik.valigursky+ku@bootiq.io")
    page.locator("#password").click()
    page.locator("#password").fill("123123")
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Erik Valigursky+Kurier|")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()

    # Login/Logout sukromna osoba
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("erik.valigursky+test5@bootiq.io")
    page.locator("#password").click()
    page.locator("#password").fill("123123")
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Súkromný zákazník Erik erik.")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()

    # Login/Logout firemny zakaznik
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("erik.valigursky+b11@bootiq.io")
    page.locator("#password").click()
    page.locator("#password").fill("123123")
    page.get_by_role("button", name="Prihlásenie").click()
    expect(page.get_by_text("Firemný zákazník Erik")).to_be_visible()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Odhlásenie").click()
    expect(page.get_by_role("link", name="Prihlásenie")).to_be_visible()
    print("✅ Testy Login/Logout prebehli úspešne.")

    # ---------------------
    context.close()
    browser.close()
