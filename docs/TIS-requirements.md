# 1. Introduction

## 1.1 Purpose of requirements document
Tento dokument slúži ako katalóg požiadaviek projektu "Športový pretek". Je určený pre riešiteľov projektu, zadávateľa a vyučujúceho predmetu Tvorba Informačných Systémov.
## 1.2 Scope of the product
Produkt má za úlohu predovšetkým zabezpečiť komunikáciu existujúcej webovej aplikácie "Športový klub" s oficiálnym aplikačným rozhraním [SZOS](https://is.orienteering.sk/). Dalej je potrebné umožniť zobrazenie štatistík pre zúčastnených športovcov.
## 1.3 Definitions, acronyms and abbreviations
- API - Application programming interface
- SZOS
- REST
- JSON
- TODO
## 1.4 References
TODO: doplniť
## 1.5 Overview of the remainder of the document
TODO: zosumarizovať nasledujúce kapitoly

# 2. General description
## 2.1 Product perspective
Športový klub Sandberg používa na prihlasovanie svojich členov na preteky svoju vlastnú webovú aplikáciu. Táto aplikácia však nie je nijakým spôsobom prepojená s oficiálnym API SZOS. Tým pádom sa vyžaduje ručné prihlasovanie účastníkov, ktorí sa prihlásili do klubovej aplikácie do oficiálneho systému SZOS. Klubová aplikácia naposkytuje žiadne bližšie informácie o pretekároch a ich dlhodobej výkonnosti.
## 2.2 Product functions
Aplikácia musí zabezpečiť obojstrannú komunikáciu klubovej aplikácie s API SZOS, najmä stiahnutie aktuálnych pretekov z API do databázy klubovej aplikácie ako aj prihlásenie pretekárov, ktorí sa prihlásili na preteky v klubovej aplikácii do systému SZOS.
Taktiež zabezpečí vygenerovanie štatistík pre vybraných pretekárov na základe dát z API SZOS.  
## 2.3 User characteristics
S aplikáciou bude interagovať a pracovať vylučne administrátor klubovej aplikácie.
## 2.4 General constraints
Existujúci klubový systém je webová aplikácia v jazyku PHP využívajúca databázu SQLite, bežiaca na Ubuntu Linux serveri.
## 2.5 Assumptions and dependencies
Rozhraním klubového systému je predovšetkým databáza SQLite. Rozhraním systému SZOS je REST API rozhranie využívajúce API kľúče na overenie identity používateľa. Formát výmeny dát je JSON.

# 3 Specific requirements
Požiadavky sú zoradené od najvyššej priority zostupne.
## 3.1 Komunikácia z API SZOS do klubovej aplikácie
### 3.1.1 Práca s databázou klubovej aplikácie
Schopnosť aplikácie pridať do databázy klubovej aplikácie nové vekové kategórie a ďalšie informácie o pretekoch. 
### 3.1.2 Stiahnutie požadovaných pretekov z API
Závislosti: [práca s databázou](#praca-s-databazou-klubovej-aplikacie)

Používateľ si zvolí budúce preteky, napr. podľa mesiaca konania. Údaje o týchto prerekoch sa stiahnu z API a uložia do databázy klubovej aplikácie.

## 3.2 Komunikácia z klubovej aplikácie do API SZOS
### 3.2.1 Prihlásenie pretekárov
Pretekári, ktorí sa prihlásili na preteky (z 3.1) v klubovej aplikácii sú automaticky, alebo ručne na základe výberu používateľa prihlásení na príslušné preteky v systéme SZOS.

## 3.3 Štatistiky

## 3.4 Voliteľné
Požiadavky v tejto stati nie sú potrebné pre úspešnosť projektu a majú najnižšiu prioritu.
### 3.4.1 Predvolená kategória
Pri prihlasovaní používateľa na pretek v klubovej aplikácii bude v zozname vekových kategórii predvolene vybraná jeho posledná kategória, na základe dát z API alebo z databázy.
### 3.4.2 Obmedzenie kategórii
Pri prihlasovaní používateľa na pretek v klubovej aplikácii nebudú v zozname vekových kategórii také kategórie, na ktoré by sa používateľ na základe pravidiel nemal mať možnosť prihlásiť.

