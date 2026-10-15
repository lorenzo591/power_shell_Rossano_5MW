# Opzioni della LOI General Compute: densità e massa sul ponte da 5 MW

- Revisione: A (2026-10-15). Prima versione.
- Numeri: [`calcs/risultati-general-compute.md`](../calcs/risultati-general-compute.md), generati da [`calcs/general_compute_loi.py`](../calcs/general_compute_loi.py) con le stesse funzioni di [`dimensionamento_5mw.py`](../calcs/dimensionamento_5mw.py).
- Dati dei rack: schede prodotto su [generalcompute.com](https://www.generalcompute.com/) (consultato 2026-10-15). Masse dei rack, potenza del rack d-Matrix e quota al liquido Cerebras sono **ipotesi n.v.**
- Ipotesi di concept, come il resto del repo.

## 1. Dati di ingresso

- REQ-IT-001: 5000 kW IT. REQ-IT-002: liquido (DLC) come soluzione principale, niente aria.
- REQ-MEC-001: pod di container 40' HC su 2 piani; 16 rack da 600 mm per container IT (come config B).
- REQ-MEC-002: container ≤ 30,48 t (ISO), obiettivo ≤ 26 t. Ponte circa 30 × 30 m. Massa ammessa sul ponte (REQ-MEC-003): TBD.

| Opzione GC | Ruolo | kW/rack | Raffreddamento | Stato (GC) |
|---|---|---|---|---|
| NVIDIA HGX B300 | Prefill | 56 (4 server da ~14 kW); 28 nel calcolatore TCO di GC | Aria, opzione liquido | Disponibile |
| Cerebras CS-3 | Decode, il più veloce | ~46 (2 sistemi da 23 kW) | Liquido, circa 90 % all'acqua di impianto | Disponibile |
| d-Matrix Corsair SquadRack | Decode | ~45 (stima: 64 × 600 W + host) | Solo aria | Disponibile |
| SambaNova SN50 | Decode | ~20 medi (picco non pubblicato) | Solo aria | H2 2026 |
| Positron Atlas | Decode | 2 kW per server 4U: 12 (6 server) – 20 (10 server) | Solo aria | Disponibile |

## 2. Massa sul ponte per opzione (t)

| Voce | B300 DLC 4 srv (56 kW) | B300 DLC 2 srv (28 kW) | Cerebras (46 kW) | d-Matrix (45 kW) | SN50 (20 kW) | Positron 10 srv (20 kW) | Positron 6 srv (12 kW) | Rif. config A (140 kW) |
|---|---|---|---|---|---|---|---|---|
| Rack IT (pieni) | 72 | 86 | 112 | 101 | 205 | 205 | 259 | 56 |
| Porte posteriori RDHx | 12 | 23 | 13 | 13 | 31 | 31 | 52 | 4 |
| Container IT (involucro, blindosbarre, tubi, antincendio, ancoraggi) | 56 | 113 | 66 | 66 | 150 | 150 | 254 | 38 |
| Container inferiori (trasformatori, quadri BT, CDU) | 116 | 233 | 136 | 136 | 310 | 310 | 524 | 82 |
| Skid scambiatori e pompe FWS | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| Container MT e controllo | 17 | 17 | 17 | 17 | 17 | 17 | 17 | 17 |
| Telaio, guide cellulari, passerelle | 38 | 64 | 42 | 42 | 82 | 82 | 132 | 28 |
| Tubazioni e cavi tra i container | 18 | 32 | 20 | 20 | 42 | 42 | 70 | 12 |
| Pompe di mare e colonne di presa | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| **Totale** | **358** | **599** | **436** | **425** | **868** | **868** | **1.338** | **268** |
| Rapporto con la config A | 1,3× | 2,2× | 1,6× | 1,6× | 3,2× | 3,2× | 5,0× | 1,0× |
| kg per kW IT | 72 | 120 | 87 | 85 | 174 | 174 | 268 | 54 |
| Container 40' HC | 14 | 26 | 16 | 16 | 34 | 34 | 56 | 10 |
| Sta sul ponte 30 × 30? | Sì, 1 fila | Sì, 2 file | Sì, 1 fila (29,9 m) | Sì, 1 fila (29,9 m) | **No** | **No** | **No** | Sì |

Come leggere la scomposizione: solo la riga "Rack IT" dipende dal prodotto. Tutto il resto (container, trasformatori, CDU, telaio, tubi) cresce con il **numero di pod**, cioè con l'inverso della densità. Con rack da 20 kW i rack pesano circa 200 t, ma l'infrastruttura che li contiene ne pesa altre 660.

## 3. Valutazione

- **NVIDIA HGX B300 DLC, 4 server per rack: la migliore.** È la config B già studiata: 358 t, 14 container, 95 % del calore al liquido, compatibile con l'architettura acqua di mare. Da chiarire con GC se il rack della LOI è da 4 server (56 kW) o da 2 (28 kW): il rack da 28 kW porta a 599 t e 26 container.
- **Cerebras CS-3: fattibile.** 436 t, sta in una fila da 29,9 m (al limite del ponte). Calore circa 90 % all'acqua, coerente con REQ-IT-002. Il container IT pieno arriva a 27,3 t, sopra l'obiettivo di 26 t: da verificare con la massa reale del rack. Servono i limiti di temperatura dell'acqua di impianto.
- **d-Matrix: densità sufficiente, raffreddamento no.** Massa simile a Cerebras (425 t), ma 45 kW per rack tutti all'aria: in contrasto con REQ-IT-002 e al limite delle porte RDHx. La potenza del rack non è pubblicata.
- **SambaNova SN50 e Positron Atlas: fuori scala, pesano troppo.** Con 12–20 kW per rack servono 250–417 rack, 34–56 container e **868–1.338 t sul ponte, da 3 a 5 volte la config A**. Non stanno sul ponte 30 × 30 né in una fila né in due, e sono raffreddati solo ad aria. Per una piattaforma galleggiante dove ogni tonnellata conta sono **da scartare per il 5 MW**, indipendentemente dalle prestazioni del chip. (Positron resta invece la scelta adatta al DC minimo da 20', dove conta il basso assorbimento per server.)

## 4. Domande per General Compute

1. Quale rack B300 prevede la LOI: 4 server (56 kW) o 2 server (28 kW)? Con opzione DLC?
2. Potenza di picco (non media) dei rack SN50 e d-Matrix.
3. Cerebras CS-3: temperatura e portata dell'acqua di impianto, quota di calore all'aria, massa del rack.
4. Prestazioni in tok/s per kW sul modello di riferimento: a 5 MW conta quanto si produce per kW, non per rack.
