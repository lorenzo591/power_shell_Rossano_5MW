# Requisiti

- Stato: **TBD** (da definire), **Ipotesi** (valore provvisorio), **Confermato** (con fonte), **Ereditato** (dai repo `powered_shell_container` e `powered_shell_schneider-vertiv`, riferito alla TLP del pilota: da riconfermare per la TLP da 5 MW).
- Un ID non si riusa. I calcoli citano questi ID.

## Carico IT

| ID | Requisito | Valore | Unità | Stato | Fonte / Note |
|---|---|---|---|---|---|
| REQ-IT-001 | Potenza IT nominale | 5000 | kW | Confermato | Cliente, 2026-10-09: solo potenza IT, ausiliari esclusi |
| REQ-IT-002 | Tipo di raffreddamento IT | Liquido diretto a cold plate (DLC), quota residua ad aria | – | Confermato | Cliente, 2026-10-09: niente raffreddamento ad aria come soluzione principale |
| REQ-IT-003 | Rack di riferimento | Classe GB200/GB300 NVL72: 140 kW, circa 1,55 t, 600 × 1068–1200 × 2236–2258 mm, circa 88 % al liquido | – | Ipotesi | ADR 0005. Ricerca DLC del repo container |
| REQ-IT-004 | Numero di rack | 36 (+ 1–2 rack rete per pod) | – | Ipotesi | 5000 / 140 |
| REQ-IT-005 | Ingresso liquido ai server | ≤ 45 °C (classe W45) | °C | Ereditato | Ricerca DLC, repo container |
| REQ-IT-006 | Aria ai rack | 18–27 °C raccomandato, ≤ 32 °C ammesso (ASHRAE A1) | °C | Ipotesi | Determina il chiller di rifinitura (ADR 0002) |
| REQ-IT-007 | Ridondanza alimentazione | 2N fino al rack (A/B); BBU nel rack | – | Ipotesi | ADR 0004 |
| REQ-IT-008 | Ridondanza raffreddamento | CDU 2N per pod; scambiatori e pompe di mare 3 × 50 %; chiller 2 × 100 % | – | Ipotesi | |
| REQ-IT-009 | Continuità | Server: BBU, 1,5–5 min. Pompe e controlli: UPS 2N circa 10 min | min | Ipotesi | Nessun generatore a bordo |
| REQ-IT-010 | Esercizio non presidiato, riavvio automatico | Sì | – | Ereditato | REQ-ENV-023 del pilota |

## Alimentazione

| ID | Requisito | Valore | Unità | Stato | Fonte / Note |
|---|---|---|---|---|---|
| REQ-PWR-001 | Tensione di alimentazione alla TLP | 20 kV MT (da confermare col distributore) | kV | Ipotesi | ADR 0001. In BT servirebbero circa 9600 A |
| REQ-PWR-002 | Frequenza | 50 | Hz | Ipotesi | |
| REQ-PWR-003 | Potenza al punto di consegna | circa 5500 kW, 5800 kVA; di progetto 6700 kVA (margine 15 %) | kVA | Ipotesi | `calcs/risultati.md` §4 |
| REQ-PWR-004 | Numero di alimentazioni da terra | 2 cavi MT, 2 × 100 %, da cabine o semisbarre diverse | – | Ipotesi | ADR 0004 |
| REQ-PWR-005 | Corrente di cortocircuito MT al punto di consegna | TBD (ipotesi 16 kA) | kA | TBD | Serve per quadro MT e cavo |
| REQ-PWR-006 | Livello di connessione alla rete (MT o AT) | TBD | – | TBD | Vicino alla soglia MT/AT (circa 6 MW, da verificare) |
| REQ-PWR-007 | Trasformatori sulla TLP | A secco in resina, ammessi | – | **TBD** | Il proprietario della TLP del pilota li aveva esclusi (ADR 0001 dei repo precedenti): da rinegoziare |
| REQ-PWR-008 | Sistema di distribuzione BT | TN-S | – | Ipotesi | |
| REQ-PWR-009 | Generazione di emergenza a bordo | No | – | Ipotesi | Gasolio su piattaforma non presidiata |

## Ambiente

| ID | Requisito | Valore | Unità | Stato | Fonte / Note |
|---|---|---|---|---|---|
| REQ-ENV-001 | Sito | Mar Ionio al largo di Corigliano-Rossano, fondale circa 450 m | – | Ipotesi | Cliente, 2026-10-15. Punto esatto, distanza dalla costa, batimetria e geohazard da rilevare. I dati della TLP pilota di Napoli non valgono più |
| REQ-ENV-002 | Area utile del ponte | 24 × 24 (TLP minima, soluzione B); massimo 30 × 30 | m | Ipotesi | Cliente, 2026-10-09 ("non più di 30 × 30"); [`mechanical/tlp-5mw-rossano.md`](../mechanical/tlp-5mw-rossano.md) |
| REQ-ENV-003 | Aria esterna | 0–38 °C, UR fino a 100 % | °C | Ereditato | |
| REQ-ENV-004 | Corrosività esterna | CX (ISO 12944-2) | – | Ereditato | |
| REQ-ENV-005 | Mare alla presa a 25 m | massimo 24,7 °C, 99° percentile 23,4 °C, minimo circa 12,7 °C | °C | Ereditato | Dataset Napoli 1987–2023 (da qualificare) |
| REQ-ENV-006 | Mare alla presa a 50 m | massimo 21,7 °C, 99° percentile 20,2 °C | °C | Ereditato | Stesso dataset |
| REQ-ENV-007 | Profondità della presa | 25 m (50 m se il fondale lo permette) | m | Ipotesi | |
| REQ-ENV-008 | Scarico a mare | ≤ 35 °C; ≤ +3 °C a 1000 m | °C | Ereditato | D.Lgs. 152/2006 All. 5 Tab. 3, da verificare con l'autorità |
| REQ-ENV-009 | Quota del fondo del ponte sul medio mare | 15 | m | Ipotesi | Onda centenaria Hs 8,2 m (boa di Crotone): cresta circa 9,7 m + margini. Sostituisce i 5 m della TLP pilota |
| REQ-ENV-010 | Moti e accelerazioni in esercizio e rimorchio | Rollio 20°, beccheggio 12,5°, Ay 3,36 m/s², Az 11,54 m/s² (rimorchio) | – | Ereditato | SIZ0PLT001 rev 0, TLP pilota: **da rifare per la TLP da 5 MW** |
| REQ-ENV-011 | Frequenze proprie della piattaforma | 6,4–17,2 | Hz | Ereditato | Idem |
| REQ-ENV-012 | Area pericolosa | No (area sicura) | – | Ereditato | |

## Meccanica

| ID | Requisito | Valore | Unità | Stato | Fonte / Note |
|---|---|---|---|---|---|
| REQ-MEC-001 | Formato dei moduli | Container ISO 40' High Cube, impilati su 2 piani | – | Ipotesi | Cliente, 2026-10-09; ADR 0003 |
| REQ-MEC-002 | Massa massima per container | 30,48 (ISO); obiettivo ≤ 26 | t | Ipotesi | Margine per il sollevamento |
| REQ-MEC-003 | Massa totale ammessa sul ponte | TBD (stima di progetto circa 270 t) | t | TBD | Da chiedere al progettista della TLP |
| REQ-MEC-004 | Baricentro ammesso | TBD (stima circa 2,6 m sopra il ponte) | m | TBD | Idem |
| REQ-MEC-005 | Carico ammissibile sul ponte e punti di appoggio | TBD | kN/m² | TBD | |
| REQ-MEC-006 | Ritenuta delle apparecchiature | Meccanica positiva, non per attrito | – | Ereditato | |
| REQ-MEC-007 | Prima frequenza di telaio e armadi | > 1,2 × frequenza massima della piattaforma | Hz | Ereditato | Criterio dei repo precedenti |
| REQ-MEC-008 | Antincendio | Spegnimento automatico a gas in ogni container | – | Ereditato | |
| REQ-MEC-009 | Installazione | **Da decidere**: (A) topside montato in banchina e rimorchio integrato, scafo 5.900 t; (B) scafo e tendini prima, ponte e container sollevati in mare, scafo 3.400 t | – | TBD | [`mechanical/tlp-5mw-rossano.md`](../mechanical/tlp-5mw-rossano.md) §5 |
