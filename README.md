# Powered shell 5 MW IT su TLP

Dimensionamento preliminare di un data center containerizzato da **5 MW IT** con raffreddamento a **cold plate (DLC)** e cessione del calore al **mare**, su una tension leg platform (TLP) con ponte di circa **30 × 30 m**, usando container **ISO 40' High Cube impilati**.

Deriva dai repository `lorenzo591/powered_shell_container` (150 kW DLC) e `lorenzo591/powered_shell_schneider-vertiv` (pilota 40 kW): vedi [`fonti-dai-repository.md`](fonti-dai-repository.md).

## Risultato in breve (configurazione raccomandata)

| Voce | Valore |
|---|---|
| IT | 36 rack × 140 kW (classe GB300 NVL72) = 5,04 MW |
| Moduli | 10 container 40' HC: 4 pod da 2 piani (sotto trasformatori + CDU, sopra 9 rack) + 1 colonna servizi |
| Ingombro | circa 15,2 × 19,0 m = **288 m², un terzo del ponte**; altezza circa 6,5 m |
| Massa | circa 270 t, baricentro circa 2,6 m sopra il ponte |
| Elettrico | 2 cavi MT 20 kV 2 × 100 %, 8 trasformatori a secco 1600 kVA (2N), BBU nel rack, UPS 2N 300 kW solo per pompe e controlli. Circa 5,5 MW / 6,7 MVA di progetto |
| Raffreddamento | DLC senza chiller sul liquido (server a circa 31 °C, limite 45 °C); mare circa 700 m³/h, scambiatori in titanio 3 × 50 %; chiller di rifinitura solo per l'aria residua |
| PUE | circa 1,07–1,09 |

## Da dove partire

| Documento | Contenuto |
|---|---|
| [`configurazioni/confronto-configurazioni.md`](configurazioni/confronto-configurazioni.md) | Le configurazioni (densità rack, piani, sorgente fredda, ridondanza) e la scelta |
| [`configurazioni/general-compute-loi.md`](configurazioni/general-compute-loi.md) | Opzioni rack della LOI General Compute: densità, massa sul ponte scomposta, fattibilità |
| [`mechanical/predesign-tlp-rossano.md`](mechanical/predesign-tlp-rossano.md) | Pre-design della TLP a Rossano: potenza massima su 50 × 50 m, scafo, tendini, limite di profondità, rischi del sito |
| [`mechanical/tlp-5mw-rossano.md`](mechanical/tlp-5mw-rossano.md) | **TLP minima da 5 MW a Rossano (450 m)**: geometria, verifiche, installazione |
| [`viewer/tlp-5mw-rossano.html`](viewer/tlp-5mw-rossano.html) | Modello 3D della TLP da 5 MW con le verifiche |
| [`viewer/tlp-rossano.html`](viewer/tlp-rossano.html) | Modello 3D della variante massima su ponte 50 × 50 m (solo riferimento) |
| [`electrical/dimensionamento-elettrico.md`](electrical/dimensionamento-elettrico.md) | Potenza, MT, trasformatori, BT, continuità, unifilare concept |
| [`cooling/dimensionamento-raffreddamento.md`](cooling/dimensionamento-raffreddamento.md) | Catena termica, portate, componenti, presa e scarico |
| [`mechanical/layout-e-masse.md`](mechanical/layout-e-masse.md) | Layout dei container, masse, baricentro, rimorchio |
| [`requirements/requisiti.md`](requirements/requisiti.md) | Requisiti con ID |
| [`decisions/`](decisions/) | Decisioni di progetto (ADR) |
| [`bom/distinta-preliminare.md`](bom/distinta-preliminare.md) | Componenti principali e quantità |
| [`calcs/risultati.md`](calcs/risultati.md) | Tutti i numeri, generati da `python3 calcs/dimensionamento_5mw.py` |

## Domande aperte principali

0. **Sito**: i dati di sito ripresi dai repo precedenti (mare, moti, distanza dalla costa) sono della TLP pilota di Napoli. Se il sito è Rossano, come dice il nome del repository, vanno sostituiti.
1. Massa, baricentro e carichi ammessi dalla TLP; accelerazioni di rimorchio della nuova TLP; profondità del fondale.
2. Trasformatori sulla TLP (il proprietario del pilota li escludeva).
3. Livello di connessione alla rete (MT o AT) per circa 6,7 MVA.
4. Rack scelto: potenza, massa, aria residua, BBU, garanzia offshore.
5. Permesso allo scarico termico di circa 5,5 MW in mare.
