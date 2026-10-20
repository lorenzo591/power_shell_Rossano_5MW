# Opzioni della LOI General Compute sul ponte da 5 MW (generato)

> Generato da `calcs/general_compute_loi.py`, che riusa le funzioni di `dimensionamento_5mw.py`. Non modificare a mano. Ipotesi di concept: masse dei rack e potenza d-Matrix n.v.; trasformatori da 1250 kVA per pod in tutti i casi (cautelativo per i pod a bassa potenza).

## 1. Rack, container, ingombro

| Opzione | kW/rack | Rack | Pod | Container 40' HC | Disposizione sul ponte 30 × 30 | IT su ingombro (kW/m²) | Calore all'aria per rack (kW) | Nota |
|---|---|---|---|---|---|---|---|---|
| NVIDIA HGX B300 DLC, 4 server | 56 | 90 | 6 | 14 | 1 fila, 26,3 × 15,2 m | 12,5 | 2,8 | ~14 kW per server (GC). Coincide con la config B |
| NVIDIA HGX B300 DLC, 2 server | 28 | 179 | 12 | 26 | 2 file, 26,3 × 28,9 m | 6,6 | 1,4 | Rack da 28 kW usato nel calcolatore TCO di GC |
| Cerebras CS-3, 2 sistemi | 46 | 109 | 7 | 16 | 1 fila, 29,9 × 15,2 m | 11,0 | 4,6 | 23 kW per sistema (GC); circa 90 % all'acqua di impianto (flopper.io, n.v.) |
| d-Matrix Corsair SquadRack | 45 | 112 | 7 | 16 | 1 fila, 29,9 × 15,2 m | 11,0 | 45,0 | 64 schede × 600 W (GC) + 8 host: 45 kW stima n.v. Solo aria |
| SambaNova SN50 SambaRack | 20 | 250 | 16 | 34 | non sta: 1 fila 62,6 m, 2 file 33,5 m | 5,3 | 20,0 | 20 kW medi per rack (GC), picco non pubblicato. Solo aria |
| Positron Atlas, 10 server | 20 | 250 | 16 | 34 | non sta: 1 fila 62,6 m, 2 file 33,5 m | 5,3 | 20,0 | 2 kW per server 4U (GC); 10 server = 40U. Solo aria |
| Positron Atlas, 6 server | 12 | 417 | 27 | 56 | non sta: 1 fila 102,7 m, 2 file 51,7 m | 3,3 | 12,0 | Rack mostrato da GC (6 server). Solo aria |

## 2. Massa sul ponte scomposta (t)

| Voce | NVIDIA HGX B300 DLC, 4 server | NVIDIA HGX B300 DLC, 2 server | Cerebras CS-3, 2 sistemi | d-Matrix Corsair SquadRack | SambaNova SN50 SambaRack | Positron Atlas, 10 server | Positron Atlas, 6 server | Rif. config A (140 kW) |
|---|---|---|---|---|---|---|---|---|
| Rack IT (pieni) | 72 | 86 | 112 | 101 | 205 | 205 | 259 | 56 |
| Porte posteriori RDHx | 12 | 23 | 13 | 13 | 31 | 31 | 52 | 4 |
| Container IT: involucro, blindosbarre, tubi TCS, antincendio, ancoraggi | 56 | 113 | 66 | 66 | 150 | 150 | 254 | 38 |
| Container inferiori: trasformatori, quadri BT, CDU | 116 | 233 | 136 | 136 | 310 | 310 | 524 | 82 |
| Skid scambiatori e pompe FWS | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| Container MT e controllo | 17 | 17 | 17 | 17 | 17 | 17 | 17 | 17 |
| Telaio con guide cellulari, passerelle | 38 | 64 | 42 | 42 | 82 | 82 | 132 | 28 |
| Tubazioni e cavi tra i container | 18 | 32 | 20 | 20 | 42 | 42 | 70 | 12 |
| Pompe di mare e colonne di presa | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| **Totale sul ponte** | **358** | **599** | **436** | **425** | **868** | **868** | **1.338** | **268** |
| Rapporto con la config A | 1,3× | 2,2× | 1,6× | 1,6× | 3,2× | 3,2× | 5,0× | 1,0× |
| Massa per kW IT (kg/kW) | 72 | 120 | 87 | 85 | 174 | 174 | 268 | 54 |
| Container IT pieno (t, max ISO 30,48) | 23,3 | 18,5 | 27,3 | 25,7 | 24,1 | 24,1 | 20,9 | 24,4 |
| Baricentro sopra il ponte (m) | 2,63 | 2,59 | 2,76 | 2,73 | 2,79 | 2,79 | 2,73 | 2,55 |

