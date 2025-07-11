**Ako rozbehať Playwright s pytestom.**
-

**Čo potrebujeme**


Python (aspoň 3.8)
- Prejdi na stránku https://www.python.org/downloads/ a stiahni inštalačku
- Nainstaluj si python (Nezabudni urobiť add Python to PATH)

Pycharm (PyCharm Community Edition)

- Prejdi na stránku https://www.jetbrains.com/pycharm/download/?section=windows a stiahni si správnu verziu
- Nainštaluj si Pycharm

V Pycharme si vytvor nový projekt (stiahni tento z GitLabu)
návody nájdeš na internete, alebo ti pomože Kolega/AI.
Tento link ti pomôže začať: https://playwright.dev/python/docs/intro

Pred začatím spúštania testov je potrebné lokálne skopírovať a premenovať súbor .env.

- Pridaj si repozitár do Pycharmu

git clone https://gitlab.bootiq.io/automatizovane-testy/dpd-mk.git

- cd.. cesta do Projektu
- python -m venv .venv (vytvori nove virtualne prostredie)
- .venv\Scripts\activate (aktivuje ho)
- playwright install (nainstaluj playwright)
- Prejdi do nastaveni Pycharmu>Project interpreter>add interpreter>Pridat existujúci>vyber .venv/Scripts/python.exe

**DEBUGING**

- $Env:PWDEBUG = 1; pytest -s .\nazov_testu.py

**VYTVÁRANIE TESTOV**

- playwright codegen https://www.priklad.sk


# Kompletný návod na nastavenie Playwright + pytest + dotenv v Pythone

---

## 1. Vytvor si nový projekt alebo použij existujúci

Urob si adresár pre projekt, napríklad `PlaywrightProject`.

---

## 2. Vytvor a aktivuj virtuálne prostredie (voliteľné, ale odporúčané)

```bash
python -m venv .venv
# Aktivácia Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# alebo Windows (cmd)
.\.venv\Scripts\activate.bat
# alebo Linux / macOS
source .venv/bin/activate
```

---

## 3. Vytvor súbor `requirements.txt` s týmto obsahom:

```
pytest
pytest-playwright
python-dotenv
playwright
```

---

## 4. Nainštaluj všetky potrebné balíky:

```
pip install -r requirements.txt
pip install pytest-playwright
```

---

## 5. Spusti inštaláciu Playwright prehliadačov:

```
playwright install
```

Tento príkaz stiahne potrebné prehliadače (Chromium, Firefox, WebKit).

---

## 6. Vytvor súbor `pytest.ini` v koreňovom adresári projektu (teda tam, kde je aj `requirements.txt`):

```ini
[pytest]
addopts = -v
testpaths = Tests
```

Týmto nastavíš, že pytest bude hľadať testy v priečinku `Tests`.

---

## 7. Priprav si `.env` súbor v koreňovom adresári (nepíš ho do repozitára, môže obsahovať citlivé údaje):

Príklad `.env`:

```
CISLO_KARTY=1234123412341234
PLATNOST_KARTY=12/25
CVV_KARTY=123
```

---

## 8. Vytvor adresár `Tests` a doň umiestni svoj test, napríklad `Tests/test_objednavka.py`:

```python
import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page

# Načítanie .env súboru raz na začiatku testov
load_dotenv()

cisloKarty = os.getenv("CISLO_KARTY")
platnost = os.getenv("PLATNOST_KARTY")
cvv = os.getenv("CVV_KARTY")

@pytest.fixture
def vytvor_objednavku(page: Page) -> str:
    # Tu ide tvoj testovací kód, kde používaš "page"
    page.goto("https://twww.dpdmojkurier.sk/")
    # ... (tvoj test)
    # na konci return parcel_number
    return "test_parcel_number"

def test_prijatie_zasielky_kurierom(page: Page, vytvor_objednavku: str):
    parcel_number = vytvor_objednavku
    page.goto("https://twww.dpdmojkurier.sk/")
    # ... ďalšie kroky testu
    assert parcel_number is not None
```

---

## 9. Spúšťaj testy z terminálu v koreňovom adresári projektu:

```
pytest Tests --headed
```

- Argument `--headed` znamená, že browser sa spustí **viditeľne** (nie v headless režime).
- Ak chceš testy spustiť v tichom (headless) režime, `--headed` vynechaj.

---

## 10. Používanie testov v PyCharm

- Nastav **Test runner** na `pytest` v nastaveniach PyCharm.
- V konfigurácii testu pridaj do argumentov `--headed` ak chceš vidieť browser.
- Uisti sa, že používaš správne virtuálne prostredie, kde máš nainštalované balíky.

---

## Doplnkové rady

- **Nikdy nezdieľaj `.env` súbor s citlivými údajmi verejne.**
- Namiesto `page.wait_for_timeout(...)` používaj radšej explicitné čakacie metódy ako `page.wait_for_selector(...)`, aby boli testy stabilnejšie.
- Ak chceš mať vlastné nastavenie browsera (napríklad headless/ headed), môžeš si vytvoriť `conftest.py` s vlastnou fixture.


