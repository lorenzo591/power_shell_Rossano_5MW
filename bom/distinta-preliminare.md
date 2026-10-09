# Distinta preliminare dei componenti principali (configurazione A · K2 · E2)

- Revisione: A (2026-10-09). Nessun costo in questa fase.
- Marche e modelli sono **esempi di classe** per dare dimensioni e masse realistiche: nessuno è selezionato o verificato sul datasheet. Dove possibile si sono ripresi i prodotti già individuati nei repo `powered_shell_container` e `powered_shell_schneider-vertiv`.
- Stato: **Da scegliere** (solo classe), **Da selezionare** (serve una selezione del fornitore sul punto di lavoro).

| # | Sistema | Componente | Q.tà | Taglia | Esempi | Stato |
|---|---|---|---|---|---|---|
| M1 | Struttura | Container ISO 40' HC adattato offshore (CX, isolamento, pavimento rinforzato, porte laterali stagne) | 10 | Lordo ≤ 30,48 t | – | Da scegliere |
| M2 | Struttura | Telaio con guide cellulari, passerelle su 2 livelli, scale, tettoia | 1 | circa 19 × 15 m, circa 28 t | – | Da progettare |
| E1 | Elettrico | Cavo sottomarino MT 12/20 kV, 3 × 120 mm² Cu, fibra integrata | 2 | circa 350 m ciascuno, 2 × 100 % | Prysmian, Nexans, NKT | Da selezionare |
| E2 | Elettrico | Quadro MT a 2 semisbarre, senza SF6 | 1 | 24 kV, 630 A, circa 12 scomparti | Schneider SM AirSeT | Da selezionare |
| E3 | Elettrico | Trasformatore a secco in resina 20/0,415 kV | 8 | 1600 kVA, uk 6 %, AF, E2-C2-F1 | Schneider Trihal | Da selezionare |
| E4 | Elettrico | Trasformatore ausiliari | 2 | 250 kVA | Schneider Trihal | Da selezionare |
| E5 | Elettrico | Quadro generale BT | 8 | 2500 A, ≥ 50 kA | Schneider PrismaSeT P + MasterPacT MTZ2 | Da selezionare |
| E6 | Elettrico | Blindosbarra ai rack con derivazioni | 8 linee, 72 derivazioni | 2500 A, derivazioni circa 200 A | Schneider Canalis KTA | Da selezionare |
| E7 | Elettrico | UPS ausiliari con Li-ion | 2 | 300 kW, circa 10 min | Schneider Galaxy VL + Galaxy Lithium-ion | Da selezionare |
| E8 | Elettrico | Misure di energia e qualità | circa 20 | – | PowerLogic PM5560 / ION9000 | Da selezionare |
| E9 | Elettrico | Scaricatori MT, SPD BT, captatori, rete equipotenziale | 1 set | – | – | Da progettare |
| I1 | IT | Rack DLC 140 kW con power shelf A/B e BBU | 36 | 140 kW, circa 1,55 t | Classe NVIDIA GB300 NVL72 | Dal cliente / tenant |
| I2 | IT | Rack rete, storage, gestione | 4–8 | 10–20 kW | – | Dal cliente |
| C1 | Raffreddamento | CDU liquido-liquido a pavimento | 8 | circa 1,2–1,4 MW | Vertiv CoolChip CDU, Motivair MCDU, CoolIT CHx | Da selezionare |
| C2 | Raffreddamento | Collettori di rack, raccordi rapidi, tubazioni TCS inox 316L | 4 pod | – | – | Da progettare |
| C3 | Raffreddamento | Porte posteriori raffreddate (RDHx) | 36 | circa 17–20 kW | Motivair ChilledDoor | Da selezionare |
| C4 | Raffreddamento | Unità aria/acqua per i container inferiori e servizi | circa 6 | circa 15 kW | Uniflair InRow CW o ventilconvettori | Da selezionare |
| C5 | Raffreddamento | Chiller di rifinitura condensato ad acqua | 2 | circa 700 kW frigoriferi | Chiller a vite / centrifughi oil-free | Da selezionare |
| C6 | Raffreddamento | Scambiatore a piastre in titanio | 3 | circa 2,8 MW, avvicinamento 2 K | Alfa Laval, Kelvion | Da selezionare |
| C7 | Raffreddamento | Pompe FWS a velocità variabile | 3 | circa 300 m³/h a 25 m | Grundfos, Wilo | Da selezionare |
| C8 | Raffreddamento | Pompe sommerse acqua di mare, 904L o super duplex | 3 | circa 350 m³/h a 25 m | Grundfos SP R, KSB | Da selezionare |
| C9 | Raffreddamento | Filtro autopulente acqua di mare | 2 | circa 700 m³/h, super duplex | Amiad, Filtersafe | Da selezionare |
| C10 | Raffreddamento | Antivegetativo | 1 | – | Cathelco MGPS, De Nora SANILEC | Da selezionare |
| C11 | Raffreddamento | Tubazioni di presa e scarico, diffusore | 1 + 1 | DN350 | Super duplex o vetroresina | Da progettare |
| C12 | Raffreddamento | Vaso di espansione a membrana, trattamento acqua | 1 set | – | Reflex | Da selezionare |
| C13 | Raffreddamento | Deumidificatori e filtri chimici | circa 10 | ISA-71.04 G1 | Munters, Purafil | Da selezionare |
| S1 | Sicurezza | Spegnimento automatico a gas | 10 compartimenti + locale Li-ion | – | IG-541 o FK-5-1-12 | Da scegliere (ADR) |
| S2 | Sicurezza | Rivelazione ad aspirazione | 10 | – | Xtralis VESDA-E | Da selezionare |
| S3 | Sicurezza | Rilevazione perdite, monitoraggio, DCIM | 1 set | – | NetBotz, EcoStruxure IT | Da selezionare |
| S4 | Sicurezza | Vasche di contenimento con bordi per 15° | circa 10 | – | – | Da progettare |
