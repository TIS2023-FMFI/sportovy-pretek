# sportovy-pretek

Projekt na Tvorbu informačných systémov 2023 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg

# Inštalácia

Aplikácia vyžaduje operačný systém Linux, prípadne WSL. Iný operačný systém nie je podporovaný.

```shell
git clone https://github.com/TIS2023-FMFI/sportovy-pretek.git
cd sportovy-pretek
make build
make install
python -m orienter configure
```

# Spustenie
- program možno spustiť pomocou príkazu `python -m orienter`
- konfiguráciu je možné upraviť pomocou príkazu `python -m orienter configure`

# Konfigurácia
- v prípade, že sa nenašiel konfiguračný súbor, vygeneruje sa prázdny
- pred používaním je potrebné konfiguráciu doplniť

## Položky konfigurácie
- `API_KEY` - API kľúč pre systém SZOS
- `API_ENDPOINT` - URL pre koncový bod API
- `API_CLUB_ID` - čislo klubu v systéme SZOS
- `WEB_APP_URL` - URL klubovej aplikácie pre prístup k databáze
