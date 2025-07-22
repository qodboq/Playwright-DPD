import re
from playwright.sync_api import expect

def test_kalkulacka1kg(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("1")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

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
    print(f"✅ Cena pri odoslaní 1kg zásielky má hodnotu: {match.group(0)}")



def test_kalkulacka10kg(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("10")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

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
    print(f"✅ Cena pri odoslaní 10kg zásielky má hodnotu: {match.group(0)}")


def test_kalkulacka31_5kg(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

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
    print(f"✅ Cena pri odoslaní 31,5kg zásielky má hodnotu: {match.group(0)}")



def test_kalkulacka_hranicna_hodnota_min(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("1")
    page.get_by_role("textbox", name="Šírka (cm)").fill("1")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("1")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("0,1")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí zásielky s minimálnou hraničnou hodnotou je: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní zásielky s minimálnou hraničnou hodnotou je: {match.group(0)}")



def test_kalkulacka_hranicna_hodnota_max(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("60")
    page.get_by_role("textbox", name="Šírka (cm)").fill("60")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("60")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí zásielky s maximálnou hraničnou hodnotou je: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní zásielky s maximálnou hraničnou hodnotou je: {match.group(0)}")



def test_kalkulacka_cz_zona1(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("combobox").select_option("CZ")
    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí CZ zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní CZ zásielky má hodnotu: {match.group(0)}")



def test_kalkulacka_at_zona2(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("combobox").select_option("AT")
    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí AT zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní AT zásielky má hodnotu: {match.group(0)}")




def test_kalkulacka_fr_zona3(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("combobox").select_option("FR")
    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí FR zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní FR zásielky má hodnotu: {match.group(0)}")




def test_kalkulacka_fi_zona4(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("combobox").select_option("FI")
    page.get_by_role("textbox", name="Výška (cm)").fill("10")
    page.get_by_role("textbox", name="Šírka (cm)").fill("10")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("10")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("31,5")
    page.get_by_role("button", name="Vypočítať").click()

    pattern = r"\d+(?:[.,]\d{1,2})? EUR"

    locator_vyzdvihnutie = page.get_by_text("Cena pri vyzdvihnutí zásielky")
    expect(locator_vyzdvihnutie).to_be_visible(timeout=5000)
    text_vyzdvihnutie = locator_vyzdvihnutie.inner_text()
    match = re.search(pattern, text_vyzdvihnutie)
    assert match is not None, f"Cena pri vyzdvihnutí zásielky nemá očakávaný formát: {text_vyzdvihnutie}"
    print(f"✅ Cena pri vyzdvihnutí AT zásielky má správny formát: {match.group(0)}")

    locator_odoslanie = page.get_by_text("Cena pri odoslaní zásielky z")
    expect(locator_odoslanie).to_be_visible(timeout=5000)
    text_odoslanie = locator_odoslanie.inner_text()
    match = re.search(pattern, text_odoslanie)
    assert match is not None, f"Cena pri odoslaní zásielky nemá očakávaný formát: {text_odoslanie}"
    print(f"✅ Cena pri odoslaní AT zásielky má hodnotu: {match.group(0)}")



# tento negativny scenar nefunguje
def test_kalkulacka_negativny_scenar(page) -> None:

    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()

    page.get_by_role("textbox", name="Výška (cm)").fill("+20")
    page.get_by_role("textbox", name="Šírka (cm)").fill("")
    page.get_by_role("textbox", name="Dĺžka (cm)").fill("d")
    page.get_by_role("textbox", name="Hmotnosť (kg)").fill("$")
    page.get_by_role("button", name="Vypočítať").click()


    expect(page.locator("#height-helper-text")).to_have_text("Musí byť zadaná celočíselná hodnota")
    expect(page.locator("#width-helper-text")).to_have_text("Musí byť zadaná celočíselná hodnota Pole musí byť vyplnené")
    expect(page.locator("#length-helper-text")).to_have_text("Musí byť zadaná celočíselná hodnota")
    expect(page.locator("#weight-helper-text")).to_have_text("Hodnota musí byť reálne číslo")
    print(f"✅ Negativny scenar dopadol v dobre")

#------------------------END