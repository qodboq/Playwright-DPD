import re
from playwright.sync_api import Page, expect
from dotenv import load_dotenv; load_dotenv()
from os import getenv


# Sender
sMeno, sPriezvisko, sEmail, sTel, sMesto, sPSC, sUlica, sPopisneCislo = (
    getenv("sMeno"), getenv("sPriezvisko"), getenv("sEmail"), getenv("sTel"),
    getenv("sMesto"), getenv("sPSC"), getenv("sUlica"), getenv("sPopisneCislo")
)

# Receiver
rMeno, rPriezvisko, rEmail, rTel, rMesto, rPSC, rUlica, rPopisneCislo = (
    getenv("rMeno"), getenv("rPriezvisko"), getenv("rEmail"), getenv("rTel"),
    getenv("rMesto"), getenv("rPSC"), getenv("rUlica"), getenv("rPopisneCislo")
)

# Tento test odosle objednavku z OM na OM - OM2_home_ppl_prevzatie_do_OM_CASH_cez_DMK_test.py (Platba pri prevzati)

def test_om2om_multi(page: Page) -> None:

    # Open page DPDmojkurier.sk
    page.goto("https://twww.dpdmojkurier.sk/")

    # Prijatie cookies
    page.get_by_role("button", name="Prijať všetko").click()


    # Vytvorenie bjednavky na OM DPD Bratislava (Sender)
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").first.click()
    page.get_by_role("textbox", name="Meno").fill(sMeno)
    page.get_by_role("textbox", name="Priezvisko").fill(sPriezvisko)
    page.get_by_role("textbox", name="Email").fill(sEmail)
    page.get_by_role("textbox", name="Telefón").fill(sTel)
    page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(sMesto)
    page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(sPSC)
    page.get_by_role("textbox", name="Ulica").fill(sUlica)
    page.get_by_role("textbox", name="Popisné číslo").fill(sPopisneCislo)
    page.get_by_text("Pobočka DPD BRATISLAVA").click()
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Reciever
    page.get_by_role("textbox", name="Meno").clear()
    page.get_by_role("textbox", name="Meno").fill(rMeno)
    page.get_by_role("textbox", name="Priezvisko").clear()
    page.get_by_role("textbox", name="Priezvisko").fill(rPriezvisko)
    page.get_by_role("textbox", name="Email").fill(rEmail)
    page.get_by_role("textbox", name="Telefón").fill(rTel)

    # poslat na domacu adresu
    page.get_by_role("checkbox", name="Poslať na adresu Poslať do").uncheck()
    page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(rMesto)
    page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(rPSC)
    page.get_by_role("textbox", name="Ulica").fill(rUlica)
    page.get_by_role("textbox", name="Popisné číslo").fill(rPopisneCislo)
    page.get_by_role("textbox", name="Popisné číslo").click()
    page.click("body")
    page.wait_for_timeout(timeout=2000)
    page.get_by_role("button", name="Pokračovať").click()

    # Package
    page.get_by_role("img", name="add-parcel-icon").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("button", name="Pokračovať").click()

    # PPL zasielka
    page.get_by_role("checkbox", name="Prepravný štítok Digitálny").uncheck()

    # Package2
    page.get_by_role("button", name="Ďalšia zásielka").click()
    # Reciever2
    page.get_by_role("textbox", name="Meno").clear()
    page.get_by_role("textbox", name="Meno").fill(rMeno)
    page.get_by_role("textbox", name="Priezvisko").clear()
    page.get_by_role("textbox", name="Priezvisko").fill(rPriezvisko)
    page.get_by_role("textbox", name="Email").fill(rEmail)
    page.get_by_role("textbox", name="Telefón").fill(rTel)

    # poslat na domacu adresu
    page.get_by_role("checkbox", name="Poslať na adresu Poslať do").uncheck()
    page.locator("xpath=//label[normalize-space()='Mesto']/following::input[1]").fill(rMesto)
    page.locator("xpath=//label[normalize-space()='PSČ']/following::input[1]").fill(rPSC)
    page.get_by_role("textbox", name="Ulica").fill(rUlica)
    page.get_by_role("textbox", name="Popisné číslo").fill(rPopisneCislo)
    page.click("body")
    page.wait_for_timeout(timeout=2000)
    page.get_by_role("button", name="Pokračovať").click()
    # Package2
    page.get_by_role("img", name="add-parcel-icon").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("button", name="Pokračovať").click()
    page.get_by_role("button", name="Pokračovať na výber platby").click()
    page.get_by_text("Platba na odbernom mieste DPD").click()
    page.get_by_role("radio", name="Platba na odbernom mieste DPD").check()
    page.get_by_role("button", name="Potvrdiť objednávku").click()




# Prijatie balika cez OM v CashApp
def test_login_prijatie_balika(page: Page) -> None:
    page.goto("https://twww.dpdmojkurier.sk")  # Prejdite na URL
    # Prijat cookies
    page.get_by_role("button", name="Prijať všetko").click()
    # Prihlas sa ako admin userov
    page.get_by_role("link", name="Prihlásenie").click()
    # Username
    page.get_by_role("textbox", name="Login").fill("ADMIN_UM@bootiq.io")
    # Password
    page.locator("#password").fill("1")
    # Login
    page.get_by_role("button", name="Prihlásenie").click()
    # Expect a title "to contain" a substring.
    expect(page.get_by_role("heading", name="Správa používateľov")).to_be_visible()

    # Prihlasenie do OM uctu
    page.get_by_role("checkbox", name="Klient", exact=True).uncheck()
    page.get_by_role("checkbox", name="Admin používateľov").uncheck()
    page.get_by_role("checkbox", name="Admin všetkých odberných miest").uncheck()
    page.get_by_role("checkbox", name="Admin firemných klientov").uncheck()
    page.get_by_role("checkbox", name="Firemný klient so zľavou").uncheck()
    page.get_by_role("checkbox", name="Firma").uncheck()
    page.get_by_role("checkbox", name="Admin bannerov").uncheck()
    page.get_by_role("checkbox", name="Admin odberných miest").uncheck()
    page.get_by_role("checkbox", name="Kuriér").uncheck()
    page.get_by_role("checkbox", name="Admin", exact=True).uncheck()
    page.get_by_role("button", name="Hľadať").click()
    page.get_by_role("row", name="5818 Interne OM OM lucia.").get_by_role("button").nth(2).click()
    page.get_by_role("button", name="Customer_blackred_pos_rgb").click()
    page.get_by_role("menuitem", name="Môj profil").click()
    # Tu musis ocakavat kym nacita zasielky a az potom mozes prejst na cakajuce zasielky
    expect(page.get_by_role("button", name="Dátum")).to_be_visible(timeout=60000)
    page.get_by_role("button", name="Čakajúce zásielky").click()

    # funkcia na najdene prveho parcel number
    # Caka na elementy s danou triedou
    page.wait_for_selector("td.jss222.jss224.jss221.jss238")
    # Získame prvý element
    td = page.locator("td.jss222.jss224.jss221.jss238").first
    # Získame textový obsah
    text = td.text_content()
    # Vypíšeme textový obsah
    print(f"Číslo zásielky je{text}")

    page.get_by_role("button", name="Príjem zásielky").click()
    page.locator("#parcelNumber").fill(text)
    page.locator("#serviceCode").fill("650")
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Hotovosť").check()
    page.get_by_role("button", name="Zásielka uhradená").click()

    # Očakáva nadpis "Úspešne odoslané"
    expect(page.get_by_role("heading", name="Úspešne odoslané")).to_be_visible()

