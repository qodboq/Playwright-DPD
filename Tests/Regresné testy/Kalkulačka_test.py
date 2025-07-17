import re
from playwright.sync_api import Playwright, expect

def test_kalkulacka1kg(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("1")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+[,\.]\d{1,2} EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí 1kg zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní 1kg zásielky má správny formát: {match.group(0)}")

    context.close()
    browser.close()


def test_kalkulacka10kg(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("10")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+[,\.]\d{1,2} EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí 10kg zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní 10kg zásielky má správny formát: {match.group(0)}")

    context.close()
    browser.close()

def test_kalkulacka31_5kg(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+[,\.]\d{1,2} EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí 31,5kg zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní 31,5kg zásielky má správny formát: {match.group(0)}")

    context.close()
    browser.close()

