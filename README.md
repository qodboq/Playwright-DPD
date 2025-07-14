# ✅ Ako rozbehať Playwright s Pytestom

## 🧰 Čo budeš potrebovať

### 1. Python (verzia aspoň 3.8)

- Stiahni a nainštaluj z: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Dôležité:** Zaškrtni možnosť `Add Python to PATH` počas inštalácie

### 2. PyCharm (Community Edition stačí)

- Stiahni a nainštaluj z: [https://www.jetbrains.com/pycharm/download/](https://www.jetbrains.com/pycharm/download/)

---

## ⚙️ Nastavenie projektu

### Možnosť A: Vytvorenie nového projektu

- Spusti PyCharm → `File > New Project`

### Možnosť B: Klonovanie existujúceho projektu

```bash
git clone https://gitlab.bootiq.io/automatizovane-testy/dpd-mk.git
```

- Otvor projekt v PyCharme cez `File > Open`

---

## 📦 Príprava virtuálneho prostredia

V koreňovom priečinku projektu spusti:

```bash
python -m venv .venv           # Vytvorenie virtuálneho prostredia
.venv\Scripts\activate         # Aktivácia prostredia (Windows)
```

---

## 📄 Vytvorenie requirements.txt

Ak ešte nemáš, vytvor súbor `requirements.txt` s týmto obsahom:

```
pytest
pytest-playwright
python-dotenv
playwright
```

---

## 📥 Inštalácia balíkov a prehliadačov

```bash
pip install -r requirements.txt
playwright install
```

Týmto nainštaluješ všetky potrebné balíky a prehliadače (Chromium, Firefox, WebKit).

---

### Nastavenie interpretera v PyCharme

- `File > Settings > Project: <tvoj-projekt> > Python Interpreter`
- Klikni na ⚙️ → `Add` → `Existing environment`
- Vyber `.venv/Scripts/python.exe`

---

## 🔐 Príprava `.env` súboru

- V koreňovom priečinku vytvor kópiu súboru `.env.example`
- Premenuj ho na `.env`
- Doplň potrebné hodnoty ako prihlasovacie údaje alebo API kľúče

---

## 🐞 Debugovanie testov

Pre krokovanie testov pomocou Playwright debug módu:

```powershell
$Env:PWDEBUG=1; pytest -s .\nazov_testu.py
```

---

## ✍️ Generovanie testov pomocou codegen

Na rýchle vytvorenie testov pomocou GUI nahrávania:

```bash
playwright codegen https://www.priklad.sk
```

---

## 🧪 Spúšťanie testov

Spusti všetky testy v projekte príkazom:

```bash
pytest
```

Alebo ak chceš spustiť testy viditeľne (headed mód):

```bash
pytest --headed
```

---

## 🧾 Príklad súboru `pytest.ini`

```ini
[pytest]
addopts = -v
testpaths = Tests
```

---

## 📁 Štruktúra projektu (príklad)

```
projekt/
├── .venv/
├── .env
├── requirements.txt
├── pytest.ini
├── Tests/
│   └── test_nazov.py
└── README.md
```

---

## 📚 Užitočné odkazy

- Oficiálna dokumentácia Playwrightu (Python):  👉 [https://playwright.dev/python/docs/intro](https://playwright.dev/python/docs/intro)

---

## 🧠 Tipy a rady

- **Nikdy nezdieľaj `.env` súbor s citlivými údajmi verejne.**
- Namiesto `page.wait_for_timeout(...)` používaj radšej `page.wait_for_selector(...)`.
- Ak sa testy nespúšťajú (`Empty suite`), skontroluj:
  - Máš testy vo foldri `Tests`?
  - Sú testy pomenované `test_*.py`?
  - Máš správne nastavený `pytest.ini`?
- Môžeš si vytvoriť `conftest.py` pre vlastné fixture alebo konfiguráciu Playwrightu.