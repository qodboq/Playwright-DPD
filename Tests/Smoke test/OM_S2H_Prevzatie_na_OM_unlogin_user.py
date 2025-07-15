# TC odoslanie balíka S2H OM a prevzatie balika cez DMK na OM.Unlogin user. Payment method cash.

import re
from playwright.sync_api import Playwright, expect, Page


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Open page DPDmojkurier.sk
    page.goto("https://twww.dpdmojkurier.sk/")

    # Prijatie cookies
    page.get_by_role("button", name="Prijať všetko").click()

    # Vyber prepravy
    page.get_by_role("link", name="Poslať zásielku").first.click()
    page.get_by_role("button", name="Pokračovať").first.click()

    # Vytvorenie bjednavky na OM DPD Bratislava (Sender)
    page.get_by_role("textbox", name="Meno").click()
    page.get_by_role("textbox", name="Meno").fill("Lucia")
    page.get_by_role("textbox", name="Priezvisko").click()
    page.get_by_role("textbox", name="Priezvisko").fill("Piesova")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("lucia.piesova@bootiq.io")
    page.get_by_role("textbox", name="Telefón").click()
    page.get_by_role("textbox", name="Telefón").fill("+421918304547")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.click()
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").first.fill("Svaty")
    page.get_by_role("menuitem", name="Svätý Jur -").click()
    page.get_by_role("textbox", name="Ulica").click()
    page.get_by_role("textbox", name="Ulica").fill("1.maja")
    page.get_by_role("textbox", name="Popisné číslo").click()
    page.get_by_role("textbox", name="Popisné číslo").fill("22")
    page.get_by_role("textbox", name="Zadajte mesto").click()
    page.get_by_role("textbox", name="Zadajte mesto").fill("82104")
    page.get_by_role("menuitem", name="Bratislava").click()
    page.get_by_role("cell", name="Pobočka DPD BRATISLAVA Pri").click()
    page.get_by_role("checkbox", name="Prosím, pre ďalší krok a").check()
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Vytvorenie bjednavky na OM DPD Bratislava (Reciever)
    page.get_by_role("checkbox", name="Poslať na adresu Poslať do").uncheck()
    page.get_by_role("textbox", name="Meno").click()
    page.get_by_role("textbox", name="Meno").fill("Peter")
    page.get_by_role("textbox", name="Priezvisko").click()
    page.get_by_role("textbox", name="Priezvisko").fill("Kocian")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("lucia.piesova+recipient@bootiq.io")
    page.get_by_role("textbox", name="Telefón").click()
    page.get_by_role("textbox", name="Telefón").fill("+421918304547")
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^MestoPSČ$")).get_by_role("textbox").nth(1).fill("83102")
    page.get_by_text("Bratislava Nové Mesto").click()
    page.get_by_role("textbox", name="Ulica").click()
    page.get_by_role("textbox", name="Ulica").fill("Racianska")
    page.get_by_role("textbox", name="Popisné číslo").click()
    page.get_by_role("textbox", name="Popisné číslo").fill("66")
    page.get_by_role("button", name="Pokračovať").click()
    page.wait_for_timeout(timeout=2000)

    # Package
    page.get_by_role("img", name="add-parcel-icon").click()
    page.locator("div").filter(has_text=re.compile(r"^váha:do 5 kgdĺžka:55 cmšírka:45 cmvýška:20 cmPridať$")).get_by_role("button").click()
    page.get_by_role("button", name="Pokračovať").click()

    # Kosik
    page.get_by_role("checkbox", name="Prepravný štítok Digitálny").uncheck()
    page.get_by_role("button", name="Pokračovať na výber platby").click()

    # Vyber sposobu platby
    page.get_by_role("radio", name="Platba na odbernom mieste DPD").check()
    page.get_by_role("button", name="Potvrdiť objednávku").click()

    # Vytvorenie objednavky / Thank you page
    page.goto("https://twww.dpdmojkurier.sk/order/confirm")

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
    print(text)

    page.get_by_role("button", name="Príjem zásielky").click()
    page.locator("#parcelNumber").fill(text)
    page.locator("#serviceCode").fill("650")
    page.get_by_role("button", name="Hľadať zásielku").click()
    page.get_by_role("radio", name="Platobná brána").check()
    page.get_by_role("button", name="Zásielka uhradená").click()

    # Očakáva nadpis "Úspešne odoslané"
    expect(page.get_by_role("heading", name="Úspešne odoslané")).to_be_visible()
