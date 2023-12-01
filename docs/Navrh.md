# Úvod
Tento dokument predstavuje návrh na implementáciu systému rozširujúceho aplikáciu pre administráciu činnosti športového klubu. Obsahuje špecifikáciu vonkajších interfejsov, analýzu databázy prostredníctvom dátového modelu, použité technológie, grafický návrh administrátorského aj používateľského rozhrania, diagramy na priblíženie funkcionalít a interakcií systému, spracovanie
požiadaviek v kóde, mimo neho a ďalšie úpravy.

# Špecifikácia vonkajších interfejsov
Medzi vonkajšie interfejsy aplikácie patria jej konzolové rozhranie a aj grafické rozhranie existujúcej aplikácie, ktorá bude rozšírená o nové prvky. ďalej k nim patria súbory exportu vo formáte HTML, súbor databázy SQLite a aj [API SZOS](https://sandberg.orienteering.sk/api/API-dokumentacia.html).

# Návrh dátového modelu
<u>_**Dátovy model je prevzatý z existujúcej aplikácie.**_</u>
![Dátový model](images/realita_db.png)
<u>_**Dátovy model je prevzatý z existujúcej aplikácie.**_</u>

# Analýza použitých technológii
- HTML, CSS, JavaScript - výstupné súbory štatistík
- PHP, SQLite - prevzaté z pôvodnej aplikácie
- Python 3.11 - primárny jazyk aplikácie
- [Chart.js](https://www.w3schools.com/js/js_graphics_chartjs.asp) - grafy v štatistikách
- pip - balíčkovanie aplikácie
- pip balíčky, na ktorých aplikácia závisí
	- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) - práca s databázou
	- [tabulate](https://pypi.org/project/tabulate/) - plaintextové tabuľky
	- [requests](https://pypi.org/project/requests/) - komunikácia s API
	- [tomli-w](https://pypi.org/project/tomli-w/) - export konfigurácie do súboru
	- [jinja](https://jinja.palletsprojects.com/en/3.0.x/) - exportovanie štatistík

# Návrh konzolového rozhrania
## Hlavné menu
```
Orienter v1.0.0 - Hlavné menu
1. Pridanie nových pretekov
2. Prihlasovanie účastníkov
3. Štatistiky
q - ukončiť

zvoľte akciu [1] >>>
```

## Pridať preteky
```
Pridanie nových pretekov > Voľba mesiaca konania
Zadajte mesiac konania pretekov.
q - návrat

mesiac konania pretekov [jun] >>>
```

## Voľba pretekov
```
Pridanie nových pretekov > Voľba mesiaca konania > Voľba pretekov
Vyberte preteky podľa ich čísel, oddelené čiarkou.
╔═══════╦════════════╦═════════════════════════════════════════════════════╦════════╦═════════════╗
║ Číslo ║ Dátum      ║ Názov                                               ║ Miesto ║ Organizátor ║
╠═══════╬════════════╬═════════════════════════════════════════════════════╬════════╬═════════════╣
║ 1.    ║ 25.05.2024 ║ Majstrovstvá Slovenska v OB v šprintových štafetách ║ Martin ║ ZMT         ║
╠═══════╬════════════╬═════════════════════════════════════════════════════╬════════╬═════════════╣
║ 2.    ║ 26.05.2024 ║ Majstrovstvá Slovenska v OB v šprintových štafetách ║ Martin ║ ZMT         ║
╚═══════╩════════════╩═════════════════════════════════════════════════════╩════════╩═════════════╝

q - návrat

preteky [vsetky] >>>
```

## Prihlasovanie
```
Prihlasovanie > Voľba pretekov
Tieto preteky sú aktívne. Vyberte tie, na ktoré chcete prihlásiť používateľov.
╔═══════╦════════════╦═════════════════════════════════════════════════════╦════════╦═════════════╗
║ Číslo ║ Dátum      ║ Názov                                               ║ Miesto ║ Organizátor ║
╠═══════╬════════════╬═════════════════════════════════════════════════════╬════════╬═════════════╣
║ 1.    ║ 25.05.2024 ║ Majstrovstvá Slovenska v OB v šprintových štafetách ║ Martin ║ ZMT         ║
╠═══════╬════════════╬═════════════════════════════════════════════════════╬════════╬═════════════╣
║ 2.    ║ 26.05.2024 ║ Majstrovstvá Slovenska v OB v šprintových štafetách ║ Martin ║ ZMT         ║
╚═══════╩════════════╩═════════════════════════════════════════════════════╩════════╩═════════════╝
q - návrat

preteky [1] >>>
```

## Voľba prihlásených pretekárov
```
Prihlasovanie > Voľba pretekov > Voľba pretekárov
Títo používatelia sa prihlásili na zvolené preteky. Vyberte tých ktorých neprihlásiť, oddeľte čiarkou.
╔═══════╦═══════════════════╦════════════╦══════════╗
║ Číslo ║ Meno a priezvisko ║ Klubové ID ║ Poznámka ║
╠═══════╬═══════════════════╬════════════╬══════════╣
║ 1.    ║ David Krchňavý    ║ id1        ║ chory    ║
╠═══════╬═══════════════════╬════════════╬══════════╣
║ 2.    ║ Ondrej Bublavý    ║ id2        ║ zdravy   ║
╚═══════╩═══════════════════╩════════════╩══════════╝

q - návrat
pretekári >>>
```

# Návrh grafického rozhrania
## Pridanie nových pretekov
![Pridanie nových pretekov](images/novy_pretek.png)

## Prihlasovanie účastníkov pretekov
![Prihlasovanie pretekárov](images/pridanie_pretekov.png)

## Generovanie štatistík
Používateľ vyznačením zaškrtávacích okienok zvolí pretekárov, pre ktorých aplikácia vygeneruje HTML súbor obsahujúci ich štatistiky. Pri zvolení len jedného pretekára, bude vygenerovaný sumár jeho individuálnych štatistík. Pri zvolení viacerych pretekárov, bude vygenerovaný tiež len jeden súbor, kde budú títo pretekári porovnaní na základe ich štatistík. Ak je funkcia spustená z webového rozhrania, časový interval, za ktorý sú štatistiky generované, je automaticky nastavený na jeden rok. V konzolovej aplikácii si však správca môže zvoliť ľubovoľný časový rozsah.

![Generovanie štatistík](images/generovanie_statistik.png)

# Návrh zobrazenia štatistík
Vygenerovaný HTML dokument obsahujúci štatistiky pretekára alebo pretekárov pozostáva z dvoch sekcii. Prvá je Prehľad - ten zobrazí akumulované informácie za celú zaznamenanú históriu pretekára v klube Sandberg. Druhá sú grafy na základe štatistík za zvolený alebo prednastavený časový interval. 

## Štatistiky jedného pretekára
![štatistiky jedného pretekára](images/statistics_mockup_one_racer.jpeg)

## Štatistiky viacerých pretekárov
Štatistiky porovnávajúce viacerých pretekárov obsahujú jeden graf navyše, a to porovnanie časov na pretekoch za dané čaosvé obdobie. Porovnávať časy medzi pretekmi jednoho pretekára by vzhľadom na odlišné dĺžky ich trás nemalo význam.

![štatistiky viacerých pretekárov](images/statistics_mockup_multiple_racers.jpeg)

# Diagramy
![Sekvenčný diagram](images/sekvencny_diagram.png)
![Use case diagram](images/use_case_diagram.png)
![Component diagram](images/komponent_diagram.png)
