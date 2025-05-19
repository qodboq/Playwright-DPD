import re
from playwright.sync_api import Page


# TOTO JE LEN UPLNE NA HRUBO, A NIE JE TAM PREBRATIE KURIEROM Z DOVODU NEFUNKCNOSTI CASHAPP V DANOM MOMENTE.
# Vytvorenie objednavjy by malo fungovat, ale treba to precistit.

def test_kurier2home_cod(page: Page) -> None:


    page.goto("https://twww.dpdmojkurier.sk/")
    page.get_by_role("button", name="Prijať všetko").click()
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").nth(1).click()
    page.get_by_role("textbox", name="Meno").click()
    page.get_by_role("textbox", name="Meno").fill("Erik")
    page.get_by_role("textbox", name="Meno").press("Tab")
    page.get_by_role("textbox", name="Priezvisko").fill("Valigurský")
    page.get_by_role("textbox", name="Priezvisko").press("Tab")
    page.get_by_role("textbox", name="Email").fill("erik.valigursky@bootiq.sk")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Telefón").fill("+421948328484")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.click()
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Opoj")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.press("Tab")
    page.get_by_role("menuitem", name="Opoj -").click()
    page.get_by_role("textbox", name="Ulica").click()
    page.get_by_role("textbox", name="Ulica").fill("Opoj")
    page.get_by_role("textbox", name="Ulica").press("Tab")
    page.get_by_role("textbox", name="Popisné číslo").fill("108")
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("textbox", name="Meno").click()
    page.get_by_role("textbox", name="Meno").fill("Test")
    page.get_by_role("textbox", name="Meno").press("Tab")
    page.get_by_role("textbox", name="Priezvisko").fill("Test")
    page.get_by_role("textbox", name="Priezvisko").press("Tab")
    page.get_by_role("textbox", name="Email").fill("email@email.com")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Telefón").fill("+421123123123")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.click()
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Poprad")
    page.get_by_role("menuitem", name="Poprad -").click()
    page.get_by_role("textbox", name="Ulica").click()
    page.get_by_role("textbox", name="Ulica").fill("Ulica")
    page.get_by_role("textbox", name="Ulica").press("Tab")
    page.get_by_role("textbox", name="Popisné číslo").fill("1")
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_text("Pridať balík").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("checkbox", name="Poslať dobierkový balík").check()

    page.get_by_role("textbox", name="Dobierková suma").click()
    page.get_by_role("textbox", name="Dobierková suma").fill("1")
    page.get_by_role("textbox", name="IBAN").click()
    page.get_by_role("textbox", name="IBAN").fill("SK4075000000007777777777")
    page.get_by_role("textbox", name="IBAN").click(modifiers=["ControlOrMeta"])
    page.get_by_role("textbox", name="Variabilný symbol").click()
    page.get_by_role("textbox", name="Variabilný symbol").fill("2221178")
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Pokračovať na výber platby").click()
    page.get_by_role("button", name="Potvrdiť objednávku").click()
    page.goto("https://twww.dpdmojkurier.sk/order/confirm")

# Prebratie Zásielky kurierom v DPD Moj kurier / API