# Scenár 1

1. Používateľ vykoná kroky z README.md, konkrétne inštaláciu a konfiguráciu aplikácie
2. Používateľ spustí príkaz `make test` a počká na jeho skončenie
    - V prípade úspešného skončenia príkazu budú vygenerované súbory
      štatistík: `test_one_racer`, `test_multiple_racers.html`
        + tieto súbory si používateľ otvorí v ľubovoľnom HTML prehliadači, napr. vo webovom prehliadači
        + po ich otvorení používateľ skontroluje ich štruktúru a vzhľad

**V prípade úspešného skončenia boli pokryté požiadavky:**

+ 3.3 Generovanie štatistík - na 100%

**Poznámka:** Tento scenár pokrýva aj niektoré časti iných požiadaviek, aj keď nie úplne. Vzhľadom na jednoduchosť jeho
vykonania sa odporúča ho vykonať ako prvý, pred vykonaním ostatných, náročnejších scenárov.

# Scenár 2

1. Používateľ vykoná kroky z README.md, konkrétne inštaláciu a konfiguráciu aplikácie
2. Používateľ spustí aplikáciu a v hlavnom menu si vyberie prvú položku - `Pridanie nových pretekov`
    - výsledkom bude zobrazenie zoznamu mesiacov od Januára až po December
3. Používateľ si vyberie ľubovoľný z mesiacov
    - výsledkom bude vypísanie zoznamu pretekov, každý s dátumom konania v danom mesiaci
        - v prípade, že sa v zvolenom mesiaci nekonajú žiadne preteky, bude vypísaná
          správa `V zvolenom mesiaci sa nekonajú žiadne preteky.` a návrat do hlavného menu
4. Používateľ si vyberie ľubovolnú neprázdnu množinu z ponúknutých pretekov a výber potvrdí
    - výsledkom bude pre každé preteky zvolené v predošlom kroku vypísanie správy buď `Tieto preteky už existujú:` alebo
      správy `Preteky sa úspešne uložili.`
    - v oboch prípadoch je výsledným stavom, že v databáze sú vložené zvolené preteky

**V prípade úspešného skončenia boli pokryté požiadavky:**

+ 3.1 Stiahnutie požadovaných pretekov z API - na 100%

# Scenár 3

1. Používateľ vykoná kroky z README.md, konkrétne inštaláciu a konfiguráciu aplikácie
2. Používateľ spustí aplikáciu a v hlavnom menu si vyberie druhú položku - `Prihlasovanie účastníkov`
    - výsledkom bude zobrazenie zoznamu takých pretekov, ktoré sú v databáze označené ako aktívne
        - v prípade, že také preteky nie sú, bude vypísaná správa `"Nenašli sa žiadne aktívne preteky.` a návrat do
          hlavného menu
3. Používateľ si vyberie ľubovoľný z ponúknutých pretekov
    - výsledkom bude zobrazenie zoznamu pretekárov, ktorí sa prihlásili na vybrané preteky
        - v prípade, že takí pretekári nie sú, bude vypísaná
          správa `Nenašli sa žiadni pretekári prihlásení na tieto preteky.` a návrat do hlavného menu
4. Používateľ si vyberie ľubovolnú neprázdnu množinu z ponúknutých pretekárov a výber potvrdí
    - výsledkom bude pre každého zvoleného pretekára vypísanie potvrdzovacej správy, začínajúcej `OK - ` a údajmi o
      pretekárovi
    - výsledným stavom je, že v systéme SZOS bola pre každého vybraného pretekára vytvorená prihláška na skôr vybrané
      preteky

**V prípade úspešného skončenia boli pokryté požiadavky:**

+ 3.2 Prihlásenie pretekárov na preteky - na 100%