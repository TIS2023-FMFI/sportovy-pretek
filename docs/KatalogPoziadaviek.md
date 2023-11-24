# 1 Úvod
## 1.1 Účel katalógu požiadaviek
Tento dokument opisuje všetku požadovanú funkcionalitu vyvíjaného projektu "Športový pretek". Je určený pre riešiteľov projektu, zadávateľa a vyučujúceho predmetu Tvorba Informačných Systémov. Ide o záväznú dohodu na finálnom znení požiadaviek medzi zadávateľom a riešiteľmi.

## 1.2 Rozsah produktu
Vyvinutý informačný systém bude slúžiť správcovi klubovej aplikácie Športového klubu Sandberg.

Produkt má za úlohu predovšetkým zabezpečiť komunikáciu existujúcej webovej aplikácie ["Športový klub"][KA] s oficiálnym [aplikačným rozhraním SZOS][API SZOS]. Ďalej je potrebné umožniť správcovi zobrazenie a export štatistík pre zúčastnených športovcov buď priamo z príkazového riadku alebo cez modikovaný webový interfejs existujúcej aplikácie Športový klub. 

## 1.3 Definície s skratky
- produkt - výsledný informačný systém, ktorý bude riešením týchto požiadaviek
- klubová aplikácia - webová aplikácia, ktorú používajú členovia Športového klubu Sandberg ako aj správca
- SZOS - Slovenský zväz orientačných bežcov
- preteky - kompetitívna udalosť organizovaná SZOS
- disciplína pretekov - druh pretekov, napríklad šprint, štafeta
- API - Application programming interface
- REST - Representational state transfer
- JSON - JavaScript Object Notation
- API SZOS - API pre komunikáciu s oficiálnym systémom SZOS
- pretekár - účastník pretekov za Športový klub Sandberg
- poradie pretekára v klube - poradie pretekára v porovnaní s ostatými členmi Športového klubu Sandberg
- správca - človek, ktorý má zodpovednosť za administráciu klubovej aplikácie 
- kategória, veková kategória - rozdelenie pretekárov do spádových skupín podľa ich veku, príp. pohlavia
- disciplína - druh pretekov
- aktívne preteky - preteky, na ktoré je otvorené prihlasovanie
 
## 1.4 Referencie
[KA]: https://github.com/TIS2017/SportovyKlub "Klubová aplikácia"
[API SZOS]: https://is.orienteering.sk/api "API SZOS"
- [Klubová aplikácia][KA]
- [API SZOS][API SZOS]

## 1.5 Prehľad zvyšnej časti dokumentu
[Kapitola 2](#2) slovne popisuje plánovaný produkt a jeho perspektívu. [Kapitola 3](#3) detailne opisuje požiadavky, ktoré musí spĺňať produkt.

# 2 Všeobecný popis {#2}
## 2.1 Perspektíva produktu
Športový klub Sandberg používa na prihlasovanie svojich členov na preteky svoju vlastnú klubovú aplikáciu. Táto aplikácia však nie je nijakým spôsobom prepojená s oficiálnym API SZOS. Tým pádom sa vyžaduje ručné prihlasovanie účastníkov, ktorí sa prihlásili do klubovej aplikácie do oficiálneho systému SZOS, taktiež preteky v klubovej aplikácii je potrebné vytvárať ručne. Klubová aplikácia neposkytuje žiadne bližšie informácie o pretekároch a ich dlhodobej výkonnosti.

## 2.2 Funkcie produktu {#funkcie}
Produkt musí zabezpečiť obojstrannú komunikáciu klubovej aplikácie so systémom SZOS prostredníctvom API, najmä stiahnutie aktuálnych pretekov zo systému SZOS do databázy klubovej aplikácie ako aj prihlásenie pretekárov, ktorí sa prihlásili na preteky v klubovej aplikácii do systému SZOS. Produkt umožní správcovi plynulo pridať želané preteky do databázy klubovej aplikácie, ako aj jednoducho prihlásiť želaných pretekárov do systému SZOS.

Želanými pretekmi sa rozumejú preteky, ktoré si správca zvolí spomedzi vyfiltrovaných pretekov na základe preddefinovaných filtrov, akými budú predovšetkým kalendárny mesiac začiatku konania, prípadne disciplína pretekov. Želanými pretekármi sa rozumejú takí pretekári, ktorých si správca zvolí spomedzi pretekárov, ktorí sa prihlásili na preteky v klubovej aplikácii.

Taktiež treba zabezpečiť vygenerovanie štatistík pre želaných pretekárov na základe dát zo systému SZOS. To budú pre zvolené obdobie grafy poradia na pretekoch, kĺzavého mediánu poradia na pretekoch z aktuálneho roka, počet účastí na pretekoch, počet víťazstiev na pretekoch. Ďalej zobrazí poradie pretekára v klube, celkový počet účastí na pretekoch a víťazstiev na pretekoch. Okrem toho systém získa automatickým procesom ďalšie údaje priamo z webu SZOS, pomocou ktorých zobrazí rozšírené štatistiky, teda 1) vývoj percentuálneho odklonu dĺžky trate jedného alebo viacerých zvolených pretekárov oproti ideálnej trase v jednotlivých pretekoch, 2) penalizácia jedného alebo viacerých pretekárov klubu prirážkou - stĺpcový graf cez jednotlivé preteky, 3) graf priemernej rýchlosti jedného alebo viacerých pretekárov klubu cez jednotlivé preteky, 4) graf vývoja percentilu jedného alebo viacerých pretekárov klubu v pretekoch, 5) relatívne porovnanie časov pretekárov klubu v zvolenom preteku. 

Štatistiky sa generujú v grafickej podobe vo forme HTML súborov (a vložených obrázkov), ich generovanie sa bude štartovať z webovej aplikácie pre športový klub, ktorá ich aj zobrazí vo webovom prehliadači, takže na generovanie/prezeranie štatistík sa používateľ nemusí prihlasovať na Linuxový server.

Produkt bude mať charakter konzolovej aplikácie, ktorú bude používateľ ovládať cez konzolu. V každej fáze používania produktu budú používateľovi vypísané jeho aktuálne možnosti a bude od neho očakávaná odpoveď, ktorá buď zvolí ďalšiu akciu alebo poskytne produktu dáta na ďalšie spracovanie. Napríklad po spustení produktu sa používateľovi vypíše hlavné menu, v ktorom si zvolí činnosť, ktorú si želá spraviť. Po vykonaní voľby budú od používateľa vyžiadané dáta, ktorými vykoná dopyt.

## 2.3 Charakteristiky používateľov
S produktom bude interagovať a pracovať výlučne administrátor klubovej aplikácie. Keďže pôjde o konzolovú aplikáciu, správca bude interagovať s produktom cez konzolu. Overenie identity správcu sa nevyžaduje, nakoľko sa očakáva ostrá prevádzka na serveri zabezpečenom prihlásením.

## 2.4 Všeobecné obmedzenia
Existujúci klubový systém je webová aplikácia v jazyku PHP využívajúca databázu SQLite, bežiaca na Ubuntu Linux serveri.

## 2.5 Predpoklady a závislosti
Rozhraním klubového systému je predovšetkým databáza SQLite. Rozhraním systému SZOS je REST API rozhranie využívajúce API kľúče na overenie identity používateľa. Formát výmeny dát je JSON.

# 3 Špecifické požiadavky {#3}
- **3.1 Stiahnutie požadovaných pretekov z API**
	+ 3.1.1 Správca si v produkte zvolí mesiac konania pretekov, údaje o týchto sa získajú z API SZOS
	+ 3.1.2 Z pretekov obdržaných od API SZOS vyhovujúcich nastaveným parametrom si správca vyberie jeden alebo viacero z nich. 
	+ 3.1.3 Údaje vybraných pretekoch sa stiahnu z API SZOS a uložia do databázy klubovej aplikácie.
      + 3.1.3.1 Pridané preteky nebudú označené ako aktívne
	+ 3.1.4 V prípade, že obsahuje pretek nejakú vekovú kategóriu, ktorá ešte nie je v databáze, pridá ju do nej.
	+ 3.1.5 V prípade, ak už je nejaký zvolený pretek v databáze, nevloží ho druhý krát.

- **3.2 Prihlásenie pretekárov na preteky**
	+ 3.2.1 Produkt správcovi umožní prečítať z databázy pretekárov, ktorí sa prihlásili na zvolené preteky a prihlási ich na príslušné preteky v systéme SZOS.
	+ 3.2.2 V prípade, ak už je nejaký z pretekárov prihlásený na tieto preteky, neprihlási ho druhý krát.

- **3.3 Jednoduché štatistiky** - Pre vybraného pretekára spomedzi členov klubu vypočíta a zobrazí na základe údajov z databázy a API SZOS jeho celkový počet účastí na pretekoch, celkový počet víťazstiev na pretekoch, poradie pretekára spomedzi pretekárov v klube.

- **3.4 Export do súboru** - Produkt vygeneruje zo štatistík súbor HTML, v ktorom budú prehľadne zobrazené.

- **3.5 Grafy** - Pre vybraného pretekára spomedzi členov klubu vypočíta a zobrazí grafy jeho poradia na posledných pretekoch, kĺzavého mediánu poradia na posledných pretekoch, počet účastí na pretekoch za uplynulý čas a počet víťazstiev na pretekoch za uplynulý čas.

- **3.6 Predvolená kategória** - Pri prihlasovaní používateľa na pretek v klubovej aplikácii bude v zozname vekových kategórii predvolene vybraná jeho posledná kategória, na základe dát z API alebo z databázy.

- **3.7 Obmedzenie kategórii** - Pri prihlasovaní používateľa na pretek v klubovej aplikácii nebudú v zozname vekových kategórii také kategórie, na ktoré by sa používateľ na základe pravidiel pretekov nemal mať možnosť prihlásiť.

- **3.8 Integrovanie s klubovou aplikáciou** - Všetky funkcie produktu budú dostupné aj prostredníctvom klubovej aplikácie.

