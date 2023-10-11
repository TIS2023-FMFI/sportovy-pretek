# 1. Úvod
## 1.1 Účel katalógu požiadaviek
Tento dokument slúži ako katalóg požiadaviek projektu "Športový pretek". Je určený pre riešiteľov projektu, zadávateľa a vyučujúceho predmetu Tvorba Informačných Systémov.

## 1.2 Rozsah produktu
Produkt má za úlohu predovšetkým zabezpečiť komunikáciu existujúcej webovej aplikácie ["Športový klub"][KA] s oficiálnym [aplikačným rozhraním SZOS][API SZOS]. Ďalej je potrebné umožniť zobrazenie štatistík pre zúčastnených športovcov.

## 1.3 Definície s skratky
- API - Application programming interface
- SZOS - Slovenský zväz orientačných bežcov
- REST - Representational state transfer
- JSON - JavaScript Object Notation
- API SZOS - API pre komunikáciu s oficiálnym systémom SZOS
 
## 1.4 Referencie
[KA]: https://github.com/TIS2017/SportovyKlub "Klubová aplikácia"
[API SZOS]: https://is.orienteering.sk/api "API SZOS"
- [Klubová aplikácia][KA]
- [API SZOS][API SZOS]

## 1.5 Prehľad zvyšnej časti dokumentu
[Kapitola 2](#2) slovne popisuje plánovaný produkt a jeho perspektívu. [Kapitola 3](#3) detailne opisuje požiadavky, ktoré musí spĺňať produkt.

# 2. Všeobecný popis {#2}
## 2.1 Perspektíva produktu
Športový klub Sandberg používa na prihlasovanie svojich členov na preteky svoju vlastnú webovú aplikáciu (ďalej len klubová aplikácia). Táto aplikácia však nie je nijakým spôsobom prepojená s oficiálnym API SZOS. Tým pádom sa vyžaduje ručné prihlasovanie účastníkov, ktorí sa prihlásili do klubovej aplikácie do oficiálneho systému SZOS, taktiež preteky v klubovej aplikácii je potrebné vytvárať ručne. Klubová aplikácia naposkytuje žiadne bližšie informácie o pretekároch a ich dlhodobej výkonnosti.

## 2.2 Funkcie produktu
Produkt musí zabezpečiť obojstrannú komunikáciu klubovej aplikácie s API SZOS, najmä stiahnutie aktuálnych pretekov z API do databázy klubovej aplikácie ako aj prihlásenie pretekárov, ktorí sa prihlásili na preteky v klubovej aplikácii do systému SZOS.
Taktiež treba zabezpečíť vygenerovanie štatistík pre vybraných pretekárov na základe dát z API SZOS.  

## 2.3 Charakteristiky používateľov
S produktom bude interagovať a pracovať vylučne administrátor klubovej aplikácie.

## 2.4 Všeobecné obmedzenia
Existujúci klubový systém je webová aplikácia v jazyku PHP využívajúca databázu SQLite, bežiaca na Ubuntu Linux serveri.

## 2.5 Predpoklady a závislosti
Rozhraním klubového systému je predovšetkým databáza SQLite. Rozhraním systému SZOS je REST API rozhranie využívajúce API kľúče na overenie identity používateľa. Formát výmeny dát je JSON.

# 3 Špecifické požiadavky {#3}
Požiadavky sú zoradené od najvyššej priority zostupne.

## 3.1 Komunikácia smerom z API SZOS do klubovej aplikácie
### 3.1.1 Práca s databázou klubovej aplikácie {#db}
Schopnosť produktu pridať do databázy klubovej aplikácie nové vekové kategórie a ďalšie informácie o pretekoch.

### 3.1.2 Stiahnutie požadovaných pretekov z API
Závislosti: [práca s databázou](#db)

Používateľ si v produkte zvolí budúce preteky, napr. podľa mesiaca konania. Údaje o týchto prerekoch sa stiahnu z API SZOS a uložia do databázy klubovej aplikácie.

## 3.2 Komunikácia z klubovej aplikácie do API SZOS
### 3.2.1 Prihlásenie pretekárov
Závislosti: [práca s databázou](#db)

Pretekári, ktorí sa prihlásili na preteky v klubovej aplikácii sú automaticky, alebo ručne na základe výberu používateľa prihlásení na príslušné preteky v systéme SZOS.

## 3.3 Štatistiky

## 3.4 Voliteľné
Požiadavky v tejto stati nie sú potrebné pre úspešnosť projektu a majú najnižšiu prioritu.

### 3.4.1 Predvolená kategória
Pri prihlasovaní používateľa na pretek v klubovej aplikácii bude v zozname vekových kategórii predvolene vybraná jeho posledná kategória, na základe dát z API alebo z databázy.

### 3.4.2 Obmedzenie kategórii
Pri prihlasovaní používateľa na pretek v klubovej aplikácii nebudú v zozname vekových kategórii také kategórie, na ktoré by sa používateľ na základe pravidiel nemal mať možnosť prihlásiť.

