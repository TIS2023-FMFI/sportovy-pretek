# sportovy-pretek

Projekt na Tvorbu informačných systémov 2023 - aplikácia pre prácu so systémom SZOS a webovou aplikáciou ŠK Sandberg

# Inštalácia

Aplikácia vyžaduje operačný systém Linux, prípadne WSL. Iný operačný systém nie je podporovaný.

1. poskladanie balíčka príkazom `make build`
2. inštalácia balíčka je možná príkazom `pip install dist/orienter-0.0.1-py3-none-any.whl`

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
