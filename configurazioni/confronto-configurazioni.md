# Configurazioni della powered shell da 5 MW IT: confronto e scelta

- Revisione: A (2026-10-09). Prima versione.
- Numeri: [`calcs/risultati.md`](../calcs/risultati.md), generati da [`calcs/dimensionamento_5mw.py`](../calcs/dimensionamento_5mw.py).
- Dettagli: [elettrico](../electrical/dimensionamento-elettrico.md) · [raffreddamento](../cooling/dimensionamento-raffreddamento.md) · [layout e masse](../mechanical/layout-e-masse.md).
- Tutti i valori sono **ipotesi di concept**: ordini di grandezza per scegliere l'architettura, non un progetto esecutivo.

## 0. Il problema in una riga

5 MW IT con cold plate (DLC) sul ponte di una TLP di circa 30 × 30 m, nel minor ingombro possibile, con container ISO impilati, senza presidio, in ambiente marino CX, con il mare come pozzo termico.

## 1. Tre scelte indipendenti

Il dimensionamento si scompone in tre scelte. Le combinazioni danno le configurazioni.

| Scelta | Opzioni | Cosa decide |
|---|---|---|
| **Densità del rack** (IT) | A: 140 kW/rack (classe GB300 NVL72) · B: 56 kW/rack (HGX 8-GPU 4U, 4 per rack) · C: 200 kW/rack (classe Vera Rubin, 800 V c.c.) | Numero di container, quindi ingombro e massa |
| **Sorgente fredda** (raffreddamento) | K1: presa a 25 m senza chiller · K2: presa a 25 m + chiller di rifinitura per l'aria · K3: presa a 50 m senza chiller | Temperatura dell'aria ai rack, PUE, complessità |
| **Ridondanza elettrica** | E1: 2N con UPS centrale · E2: 2N MT/BT con batterie nel rack (BBU) · E3: N | Spazio, massa, disponibilità |

## 2. Densità del rack: quanti container

| | A (raccomandata) | B | C (evoluzione) |
|---|---|---|---|
| Rack di riferimento | Classe GB200/GB300 NVL72, 140 kW, 1,55 t | 4 server HGX B300 DLC da 14 kW, 0,75 t | Classe Vera Rubin, ~200 kW, ~1,85 t |
| Rack necessari per 5 MW | 36 | 90 | 25 |
| Rack per container IT 40' HC | 9 (limite: potenza per pod e massa) | 16 (limite: lunghezza) | 9 (limite: massa, 27 t) |
| Pod (IT sopra, potenza + CDU sotto) | 4 | 6 | 3 |
| Container 40' HC in totale (con la colonna servizi) | **10** | 14 | 8 |
| Ingombro su 2 piani | **15,2 × 19,0 m = 288 m² (32 % del ponte)** | 15,2 × 26,3 m = 399 m² (44 %) | 15,2 × 15,4 m = 233 m² (26 %) |
| Ingombro su 1 piano | 28,9 × 19,0 m = 549 m² (61 %) | 28,9 × 26,3 m = 759 m² (84 %) | 28,9 × 15,4 m = 443 m² (49 %) |
| Massa sul ponte | **circa 270 t** | circa 360 t | circa 235 t |
| Baricentro sopra il ponte | circa 2,6 m | circa 2,6 m | circa 2,5 m |
| Maturità | Prodotto in consegna (2025-2026) | Prodotto in consegna | Consegne agli hyperscaler dal 2° semestre 2026; 800 V c.c. da sviluppare |
| Calore all'aria residuo | circa 12 % (circa 700 kW) | circa 5 % | circa 3 % |

**Lettura.** La densità del rack conta più di tutto il resto: passare da 56 a 140 kW per rack toglie 4 container e circa 90 t. Il 200 kW toglie altri 2 container, ma porta l'800 V c.c. e una tecnologia non ancora disponibile per un cliente come noi.

**Scelta: A.** La shell va progettata per il rack da 140 kW e deve poter ospitare un rack classe Rubin per pod come caso limite (stessa CDU, stessa massa ammissibile per posizione). B resta compatibile (stesso pod, più pod), utile se l'offtaker porta server HGX.

## 3. Disposizione: perché il pod su 2 piani

Ogni **pod** è una colonna di 2 container 40' High Cube:

- **sotto**: 2 trasformatori MT/BT (A e B), 2 quadri generali BT, 2 CDU. Le masse pesanti in basso, i cavi BT più corti possibile (circa 3 m in verticale), il liquido server confinato in una zona senza apparecchiature IT;
- **sopra**: 9 rack in fila, porte posteriori raffreddate (RDHx), collettori del circuito server, blindosbarre A e B.

Una quinta colonna **servizi**: sotto lo skid scambiatori acqua di mare + pompe del circuito intermedio (la parte "bagnata"), sopra quadro MT, UPS degli ausiliari, controllo e rete.

| Disposizione | Ingombro (config A) | Pro | Contro |
|---|---|---|---|
| **2 piani, 5 colonne (scelta)** | 288 m² | Un terzo del ponte. Masse pesanti in basso. BT corta. Ogni pod è indipendente e si può installare a fasi | Telaio con guide cellulari e passerelle a 2 livelli. Container IT a circa 3 m di quota |
| 1 piano, 2 file | 549 m² | Niente sollevamenti in quota, accessi semplici | 61 % del ponte. Collegamenti BT e liquido più lunghi |
| 3 piani | circa 200–230 m² | Ingombro minimo | Baricentro alto, container IT a 6 m, rizzaggio difficile in rimorchio (forze laterali sul container più alto), servizi e scale complicati. Sconsigliato |

Perché container ISO 40' HC e non moduli su misura: blocchi d'angolo per sollevamento e impilamento, twist-lock, trasporto normale, molti fornitori. È la lezione dell'Easy Modular 25' (modulo non ISO, tutto da progettare). Il 40' HC dà 2,69 m di altezza interna: sufficiente per rack da 2236–2258 mm più blindosbarre e collettori (stretto, vedi [layout](../mechanical/layout-e-masse.md)).

## 4. Sorgente fredda

| | K1: presa 25 m, solo mare | **K2: presa 25 m + chiller di rifinitura (scelta)** | K3: presa 50 m, solo mare |
|---|---|---|---|
| Mare massimo alla presa | 24,7 °C | 24,7 °C | 21,7 °C |
| Liquido ai server (limite 45 °C) | 30,7 °C | 30,7 °C | 27,7 °C |
| Aria ai rack nel giorno peggiore | **31,2 °C** (oltre i 27 °C raccomandati ASHRAE, dentro i 32 °C ammessi A1) | **22 °C** | **28,2 °C** |
| Chiller | No | 2 × 100 % circa 700 kW frigoriferi, condensati sul circuito intermedio, **solo per l'aria** | No |
| PUE giorno peggiore (config A) | 1,068 | 1,092 (1,07 quando il chiller è spento) | 1,068 |
| Rischio | Garanzia server con aria a 31 °C | Compressori a bordo | Tubo di presa più lungo; dipende dalla profondità del fondale |

**Scelta: K2, con lo spazio per passare a K3.** Il liquido dei server non ha bisogno di chiller in nessun caso: il margine sul limite di 45 °C è di 14 K. Il chiller serve solo per la quota d'aria (circa 12 % con i rack NVL72) e lavora solo quando il mare alla presa supera circa 19–20 °C. Se il fondale e la TLP permettono la presa a 50 m, il chiller si può togliere o tenere come riserva. I dettagli sono in [`cooling/dimensionamento-raffreddamento.md`](../cooling/dimensionamento-raffreddamento.md).

## 5. Ridondanza elettrica

| | E1: 2N con UPS centrale | **E2: 2N MT/BT, BBU nel rack (scelta)** | E3: N |
|---|---|---|---|
| Alimentazione da terra | 2 cavi MT 20 kV, 2 × 100 % | 2 cavi MT 20 kV, 2 × 100 % | 1 cavo MT |
| Trasformatori | 8 × 1600 kVA (2 per pod) | 8 × 1600 kVA (2 per pod) | 4 × 2000 kVA |
| Continuità per i server | UPS centrale 2N da circa 5,5 MW per lato + Li-ion | Batterie nel rack (BBU OCP / power shelf con accumulo): circa 1,5–5 min | BBU nel rack |
| Continuità per pompe e controlli | Sull'UPS centrale | UPS dedicato 2N da circa 300 kW con Li-ion | UPS dedicato N |
| Spazio e massa in più | **circa 2–4 container 40' e 40–60 t** (ordine di grandezza, n.v.) | – | – (meno trasformatori) |
| Cosa succede a un guasto | Nessun effetto | Nessun effetto (il rack passa sull'altra linea) | Si ferma un pod (1,26 MW) fino alla visita |

**Scelta: E2.** Senza generatore a bordo l'UPS centrale serve solo a superare pochi minuti; le BBU nel rack fanno lo stesso lavoro senza container in più. Il 2N resta su tutto ciò che si può guastare in sito (cavi, quadri MT, trasformatori, quadri BT, blindosbarre, CDU), perché la piattaforma non è presidiata. Condizione: rack con BBU o power shelf con accumulo, **da verificare con il costruttore dei rack**. Se non disponibili, si ricade su E1. Dettagli in [`electrical/dimensionamento-elettrico.md`](../electrical/dimensionamento-elettrico.md).

## 6. Configurazione raccomandata (A · 2 piani · K2 · E2)

| Voce | Valore |
|---|---|
| Carico IT | 36 rack × 140 kW = **5,04 MW** |
| Container | 10 × 40' HC in 5 colonne da 2 (4 pod + servizi) |
| Ingombro | circa **15,2 × 19,0 m = 288 m²**, altezza circa 6,5 m con la tettoia |
| Massa sul ponte | circa **270 t**, baricentro circa 2,6 m sopra il ponte |
| Potenza al punto di consegna | circa **5,5 MW**, 5,8 MVA; di progetto con margine 15 % circa **6,7 MVA** |
| Alimentazione | 2 cavi sottomarini MT 20 kV 3 × 120 mm² Cu, 2 × 100 %, circa 190 A ciascuno |
| Trasformatori | 8 × 1600 kVA 20/0,415 kV a secco in resina, 2 per pod (A/B) |
| Raffreddamento | DLC: 2 CDU per pod; circuito intermedio ad acqua trattata circa 600 m³/h; acqua di mare circa 700 m³/h (ΔT 7 K); 3 scambiatori in titanio 3 × 50 %; 3 pompe sommerse 3 × 50 %; chiller di rifinitura per l'aria 2 × 100 % |
| PUE | circa **1,07** (inverno, chiller spento) – **1,09** (giorno peggiore) |

## 7. Cosa cambia rispetto ai repo precedenti

| Tema | Pilota Schneider (40 kW) / container (150 kW) | 5 MW |
|---|---|---|
| Alimentazione | BT 400 V da terra, nessun trasformatore sulla TLP (ADR 0001) | **MT 20 kV fino alla TLP, trasformatori a bordo**: in BT servirebbero circa 9600 A. Il vincolo del proprietario della TLP va rinegoziato |
| Massa | ≤ 15 t, baricentro ≤ 1,32 m | circa 270 t, baricentro circa 2,6 m: **nuovi requisiti da chiedere al progettista della TLP** |
| Connessione alla rete | Allaccio esistente da 30 kW | circa 5,5 MW: vicino alla soglia oltre la quale il distributore connette in AT (da verificare) |
| Raffreddamento | Aria (pilota) o DLC + mare senza chiller (150 kW) | DLC + mare come il 150 kW, con chiller di rifinitura solo per l'aria |
| Container | 1 × 20' HC o 1 × 25' non ISO | 10 × 40' HC ISO impilati |

## 8. Domande aperte che decidono il progetto

1. **TLP**: carico ammissibile sul ponte, massa e baricentro ammessi, accelerazioni di rimorchio per questa TLP, profondità del fondale (presa a 50 m?), possibilità di far scendere tubi e pompe lungo le colonne.
2. **Rete**: livello di tensione e soglia di connessione del distributore per circa 6,7 MVA; 2 linee MT da 2 cabine o semisbarre diverse.
3. **Rack**: costruttore, potenza, massa, aria residua, disponibilità di BBU, garanzia in ambiente offshore.
4. **Mare**: profilo di temperatura alla quota di presa, permesso allo scarico di circa 700 m³/h a circa 32 °C (limite di +3 °C a 1000 m, D.Lgs. 152/2006).
5. **Proprietario della TLP**: accetta trasformatori a secco sulla piattaforma?
