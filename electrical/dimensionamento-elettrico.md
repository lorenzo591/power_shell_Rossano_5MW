# Dimensionamento elettrico (configurazione A · E2)

- Revisione: A (2026-10-09).
- Numeri: [`calcs/risultati.md`](../calcs/risultati.md) §2 e §4. Requisiti: `REQ-PWR-*`, `REQ-IT-*` in [`requirements/requisiti.md`](../requirements/requisiti.md). Decisioni: [ADR 0001](../decisions/0001-media-tensione-fino-alla-tlp.md), [ADR 0004](../decisions/0004-2n-mt-bt-senza-ups-centrale.md).
- Norme candidate: IEC 61892 (impianti elettrici su unità offshore), CEI 0-16 (connessione MT), IEC 62271-200 (quadri MT), IEC 60076-11 (trasformatori a secco), IEC 61439 (quadri BT), IEC 62040 (UPS), EN 50600-2-2.

## 1. Potenza al punto di consegna

| Voce | kW | Nota |
|---|---|---|
| Carico IT | 5040 | 36 rack × 140 kW |
| Raffreddamento (pompe, ventole, chiller di rifinitura, HVAC) | 360 | Giorno peggiore con chiller (K2). Senza chiller circa 240 |
| Perdite (trasformatori, BT, UPS ausiliari) | 72 | Trasformatori Tier 2 UE 548/2014 al 43 % del carico |
| Controlli, luci, telecomunicazioni, sicurezza | 25 | |
| **Totale** | **circa 5500** | PUE circa 1,09 |
| Potenza apparente (cos φ 0,95) | 5790 kVA | |
| **Di progetto, margine 15 %** | **circa 6700 kVA** | Copre i picchi dei rack (fino a circa 1,1–1,15 × TDP con il power smoothing) e la crescita |

**Livello di tensione.** In BT a 400 V servirebbero circa 9600 A: circa 25 cavi da 240 mm² per fase su 250–350 m. Non è praticabile. Si porta la **media tensione (20 kV, da confermare con il distributore) fino alla TLP** e si trasforma a bordo. Questo supera l'ADR 0001 dei repo precedenti ("nessun trasformatore sulla TLP"): il vincolo va rinegoziato con il proprietario della TLP. Si usano trasformatori **a secco in resina**, senza olio.

**Connessione alla rete.** circa 5,5 MW di prelievo e 6,7 MVA di progetto sono vicini alla soglia oltre la quale in Italia la connessione passa di norma all'alta tensione (circa 6 MW, da verificare sul Testo integrato connessioni ARERA e con e-distribuzione). Due casi:

- connessione **MT** con 2 linee da cabine primarie o semisbarre diverse: la più semplice;
- connessione **AT** (132/150 kV) con sottostazione AT/MT del cliente a terra: più costosa, ma senza limiti di crescita.

## 2. Schema unifilare (concept)

```
 TERRA                                 │ TLP
 Cabina A (MT 20 kV) ── cavo sottomarino A, 3×120 Cu + fibra ──┐
 Cabina B (MT 20 kV) ── cavo sottomarino B, 3×120 Cu + fibra ──┼──┐
                                                               │  │
          Container SERVIZI (sopra) ─ Quadro MT a 2 semisbarre (SM AirSeT, senza SF6)
                         semisbarra A ──┤ congiuntore NA ├── semisbarra B
                          │  │  │  │  │                     │  │  │  │  │
                          │  │  │  │  └ TR-AUX-A 250 kVA    │  │  │  │  └ TR-AUX-B 250 kVA
                          │  │  │  │      └ UPS-AUX-A ─┐    │  │  │  │      └ UPS-AUX-B ─┐
                          │  │  │  │   pompe, CDU, controlli (2N, doppia alimentazione) ─┘
                          ▼  ▼  ▼  ▼  cavi MT verso i 4 pod                  ▼  ▼  ▼  ▼
 POD n (sotto):   TR-nA 1600 kVA 20/0,415 kV            TR-nB 1600 kVA 20/0,415 kV
                     │                                     │
                  QGBT-nA 2500 A (MasterPacT)           QGBT-nB 2500 A
                     │                                     │
 POD n (sopra):   blindosbarra A 2500 A                 blindosbarra B 2500 A
                     └─ derivazioni ai 9 rack ──┐ ┌── derivazioni ai 9 rack ─┘
                                           rack 140 kW (power shelf A/B, BBU)
```

Il dettaglio delle protezioni e il coordinamento si fanno nello schema unifilare esecutivo (`electrical/single-line/`, da fare).

## 3. Componenti e taglie

| Livello | Componente | Quantità | Taglia | Verifica |
|---|---|---|---|---|
| Alimentazione | Cavo sottomarino MT 12/20 (24) kV, 3 anime XLPE, armatura, fibra ottica integrata | 2 (A e B), percorsi separati | 3 × 120 mm² Cu (o 3 × 185 mm² Al); circa 190 A di esercizio, portata circa 300 A da catalogo (n.v.); tratto dinamico con J-tube e limitatore di curvatura sulla TLP | Sezione minima per 16 kA × 1 s: 112 mm². Caduta di tensione circa 0,13 % su 350 m |
| MT | Quadro MT a 2 semisbarre, isolato in aria, senza SF6 (es. Schneider SM AirSeT) | 1, circa 12 scomparti | 24 kV, 630 A, 16–20 kA; 2 arrivi, congiuntore normalmente aperto, 8 partenze pod, 2 partenze ausiliari, misure | Da dimensionare con la corrente di cortocircuito del distributore (REQ-PWR-006) |
| MT/BT | Trasformatore a secco in resina (es. Schneider Trihal), Dyn11, classi E2-C2-F1 | 8 (2 per pod) | **1600 kVA**, 20/0,415 kV, uk 6 %, ventilazione forzata (AF) per i sovraccarichi; perdite Tier 2: Po 2,2 kW, Pk 14 kW | In 2N ognuno lavora al **43 %**, all'**85 %** con il gemello fuori servizio |
| MT/BT ausiliari | Trasformatore a secco | 2 | 250 kVA | Pompe, chiller, HVAC, controlli: circa 240 kW con il chiller |
| BT | Quadro generale BT per linea (es. PrismaSeT P, interruttore MasterPacT MTZ2 25) | 8 | 2500 A, Icw ≥ 50 kA (cortocircuito ai morsetti circa 37 kA) | |
| BT | Blindosbarra verso i rack (es. Canalis KTA) | 8 (A e B per pod) | 2500 A, circa 12 m nel container IT + risalita di circa 3 m dal container sotto | La risalita attraversa tetto e pavimento con passaggi stagni |
| Rack | Derivazioni (tap-off) | 2 per rack (A e B), 72 in totale | circa 200 A per lato a 415 V (140 kW su una sola linea); numero e tipo delle prese secondo il power shelf (es. più prese IEC 60309 da 63 A, n.v.) | Ogni linea regge da sola il rack |
| Continuità IT | BBU nel rack o power shelf con accumulo | 36 rack | circa 1,5–5 min a pieno carico (n.v.) | **Da confermare col costruttore** |
| Continuità ausiliari | UPS (es. Galaxy VL) con armadio Li-ion | 2 (2N) | **300 kW** ciascuno, circa 10 min (carichi critici circa 230 kW: pompe CDU, FWS, mare, controlli) | Il liquido deve circolare anche durante una mancanza rete: senza portata i server DLC vanno in protezione in pochi secondi |
| Misura | Analizzatori (es. PowerLogic PM5560 / ION9000 sul punto di consegna) | circa 20 | Arrivi MT, ogni trasformatore, ausiliari | Serve anche per il PUE (ISO/IEC 30134-2) |
| Rifasamento e armoniche | Filtro attivo (es. AccuSine) | 1 per quadro BT, se serve | Da dimensionare | Gli alimentatori dei server hanno PFC: cos φ alto, armoniche basse. Il distributore può chiedere limiti (CEI 0-16) |

## 4. Funzionamento e ridondanza

- **Esercizio normale**: entrambi i cavi MT in servizio, congiuntore aperto. Ogni rack prende metà potenza dalla linea A e metà dalla B.
- **Guasto di un cavo MT, di una semisbarra, di un trasformatore, di un quadro BT o di una blindosbarra**: i rack passano sull'altra linea senza interruzione (power shelf A/B). Nessuna azione in sito fino alla visita programmata.
- **Mancanza della rete da terra (entrambi i cavi)**: le BBU tengono i rack per pochi minuti, l'UPS degli ausiliari tiene le pompe. Se la rete non torna, arresto ordinato. Al ritorno, **riavvio automatico** (piattaforma non presidiata, REQ-ENV-023).
- **Generatore a bordo**: escluso (gasolio su piattaforma non presidiata). Se servisse disponibilità maggiore, la soluzione è una terza linea da terra, non un generatore.

Con un solo punto di connessione alla rete, il 2N interno non elimina il guasto di modo comune a monte. Per questo i due cavi devono arrivare da **due cabine o due semisbarre diverse**.

## 5. Messa a terra, fulmini, sovratensioni

- Sistema **TN-S** a valle di ogni trasformatore. Lato MT secondo il distributore.
- Tutti i container, il telaio e la struttura della TLP collegati in un'unica rete equipotenziale. La struttura in acciaio della TLP fa da dispersore (in mare).
- Captatori sulla tettoia e calate sul telaio (CEI EN 62305). Scaricatori MT ai terminali dei cavi, SPD di tipo 1 + 2 sui quadri BT.
- Protezione catodica della TLP: coordinare con la messa a terra per evitare correnti vaganti nei tubi dell'acqua di mare.

## 6. Configurazioni alternative (per il confronto)

| | E1 2N con UPS centrale | E2 (scelta) | E3 N |
|---|---|---|---|
| UPS | 2 × circa 5,5 MW (es. moduli da 1,25 MW) + Li-ion 5 min per lato (circa 460 kWh) | 2 × 300 kW per gli ausiliari | 1 × 300 kW |
| Trasformatori | 8 × 1600 kVA | 8 × 1600 kVA | 4 × 2000 kVA |
| Container in più | circa 2–4 (n.v.) | 0 | 0 |
| Massa in più | circa 40–60 t (n.v.) | 0 | circa −15 t |
| Perdite in più | circa 1–3 % del carico IT con UPS in doppia conversione (50–150 kW) | – | – |

Configurazione C (rack classe Rubin a 800 V c.c.): i quadri BT del container sotto diventano raddrizzatori (sidecar o, in futuro, trasformatori allo stato solido MT → 800 V c.c.). Trasformatori 6 × 2500 kVA, BT circa 3500 A per linea, cortocircuito circa 58 kA. Da approfondire quando la tecnologia sarà disponibile.

## 7. Da verificare

- Tensione, soglia di connessione e corrente di cortocircuito del distributore (REQ-PWR-004, 006).
- Disponibilità di BBU o power shelf con accumulo per il rack scelto; durata e vita delle celle a 25–30 °C.
- Ingressi di alimentazione del rack (numero di prese, corrente, connettori) e picchi di potenza.
- Accettazione dei trasformatori a secco sulla TLP da parte del proprietario e della società di classe.
- Portata del cavo sottomarino in posa reale (interrata, in J-tube, in aria sul ponte).
