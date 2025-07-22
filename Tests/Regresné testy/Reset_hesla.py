from playwright.sync_api import expect

# Test na resetovanie hesla (skontroluj ci ti prisiel mail)

def test_reset_hesla(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Prihlásenie").click()
    page.get_by_role("link", name="Máte problém s prihlásením?").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("erik.valigursky+test1@bootiq.io")
    page.get_by_role("button", name="Odoslať").click()
    expect(page.get_by_text("Na email erik.valigursky+")).to_be_visible()
    print("✅ Email na resetovanie hesla sa uspesne odoslal.")
    # ---------------------




