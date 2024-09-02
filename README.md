# sportovy-pretek

Projekt na Tvorbu informačných systémov 2023 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg

# Inštalácia

Aplikácia vyžaduje operačný systém Linux, prípadne WSL. Iný operačný systém nie je podporovaný.
Taktiež sa vyžaduje mať nainštalované balíky python, pip. Voliteľné ale odporúčané je použiť je Python balík venv.

```shell
git clone https://github.com/TIS2023-FMFI/sportovy-pretek.git
cd sportovy-pretek
make build
make install
```

# Konfigurácia
- v prípade, že sa nenašiel konfiguračný súbor, vygeneruje sa prázdny
- pred používaním je potrebné konfiguráciu doplniť

# Spustenie
- program možno spustiť pomocou príkazu `python -m orienter`
- konfiguráciu je možné upraviť pomocou príkazu `python -m orienter configure`

## Položky konfigurácie
- `API_KEY` - API kľúč pre systém SZOS
- `API_ENDPOINT` - URL pre koncový bod API
- `API_CLUB_ID` - čislo klubu v systéme SZOS
- `WEB_APP_URL` - URL klubovej aplikácie pre prístup k databáze

## Inštalácia na python 3.12 si vyžaduje nejaké ďalšie kroky, toto zafungovalo:

```
$ mkdir p2
$ cd p2
$ mkdir pretek
$ git clone https://github.com/TIS2023-FMFI/sportovy-pretek.git
$ cd sportovy-pretek
$ sudo apt install python3-full
$ sudo apt install python3-build
$ sudo apt install python3-distutils-extra

$ nano Makefile

zmenil som vsetky vyskyty python na
  /home/user/p2/pretek/bin/python3
a rovnako aj pip na
  /home/user/p2/pretek/bin/pip

(ale namiesto toho je asi lepsie pouzivat generovany script activate pre venv)

$ nano requirements.txt

zmenil som v poslednom riadku

numpy==1.24.4

na

numpy==1.26.4

(kvoli tomu, ze inak to pada na deprecated volani, ktore uz z python 3.12 vyhodili)

$ python3 -m venv /home/user/p2/pretek
$ /home/user/p2/pretek/bin/pip install --upgrade setuptools
$ /home/user/p2/pretek/bin/python3 -m pip install build

a teraz uz

$ make build
...
Successfully built orienter-0.1.1.tar.gz and orienter-0.1.1-py3-none-any.whl

$ make install
...
Successfully installed ansiwrap-0.8.4 build-1.0.3 certifi-2023.11.17
charset-normalizer-3.3.2 click-8.1.7 greenlet-3.0.2 idna-3.6
jinja2-3.1.3 markupsafe-2.1.4 marshmallow-3.22.0
marshmallow-sqlalchemy-0.30.0 numpy-1.26.4 orienter-0.1.1
packaging-23.2 pbr-6.1.0 pyproject-hooks-1.0.0 requests-2.31.0
simple-term-menu-1.6.4 six-1.16.0 sqlalchemy-2.0.25
testresources-2.0.1 textwrap3-0.9.2 tomli-2.0.1 tomli-w-1.0.0
typing-extensions-4.9.0 urllib3-2.1.0 xdg-6.0.0
```
