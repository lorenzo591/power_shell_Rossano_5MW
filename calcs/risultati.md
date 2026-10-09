# Risultati del dimensionamento (generato)

> File generato da `calcs/dimensionamento_5mw.py`. Non modificare a mano: cambiare le ipotesi nello script e rigenerare. Tutti i valori sono ipotesi di concept.

## 1. Configurazioni IT (presa a 25 m, senza chiller)

| Config | Rack di riferimento | kW/rack | Rack necessari | Rack per container IT | Pod (IT + potenza) | Container totali | IT di progetto (kW) | Capacità IT installabile (kW) |
|---|---|---|---|---|---|---|---|---|
| A | A - rack classe GB300 NVL72 (140 kW), pod ISO 40' su 2 piani | 140 | 36 | 9 | 4 | 10 | 5.040 | 5.040 |
| B | B - server HGX 8-GPU 4U DLC, 4 per rack (56 kW), pod ISO 40' su 2 piani | 56 | 90 | 16 | 6 | 14 | 5.040 | 5.376 |
| C | C - rack classe Vera Rubin (~200 kW, 800 V c.c.), pod ISO 40' su 2 piani | 200 | 25 | 9 | 3 | 8 | 5.000 | 5.400 |

## 2. Ausiliari, perdite e PUE

Casi di raffreddamento: **K1** presa a 25 m senza chiller · **K2** presa a 25 m con chiller di rifinitura sul solo circuito dell'aria · **K3** presa a 50 m senza chiller.

| Voce (kW) | A-K1 | A-K2 | A-K3 | B-K1 | B-K2 | B-K3 | C-K1 | C-K2 | C-K3 |
|---|---|---|---|---|---|---|---|---|---|
| Carico IT | 5.040 | 5.040 | 5.040 | 5.040 | 5.040 | 5.040 | 5.000 | 5.000 | 5.000 |
| Pompe circuito server (TCS, nelle CDU) | 61 | 61 | 61 | 65 | 65 | 65 | 53 | 53 | 53 |
| Pompe circuito intermedio (FWS) | 57 | 58 | 57 | 57 | 58 | 57 | 56 | 56 | 56 |
| Pompe acqua di mare | 73 | 75 | 73 | 74 | 74 | 74 | 72 | 73 | 72 |
| Ventole aria/acqua e RDHx | 14 | 14 | 14 | 7 | 7 | 7 | 5 | 5 | 5 |
| Chiller di rifinitura (picco estivo) | 0 | 118 | 0 | 0 | 62 | 0 | 0 | 40 | 0 |
| HVAC container, deumidificazione | 30 | 30 | 30 | 42 | 42 | 42 | 24 | 24 | 24 |
| Antivegetativo e filtri | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Perdite trasformatori | 38 | 38 | 38 | 39 | 39 | 39 | 35 | 35 | 35 |
| Perdite distribuzione BT | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Perdite UPS ausiliari | 9 | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 8 |
| Controlli, luci, telecom, sicurezza | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| **Totale ausiliari e perdite** | 342 | 463 | 342 | 354 | 417 | 354 | 313 | 355 | 313 |
| **Potenza totale al punto di consegna** | 5.382 | 5.503 | 5.382 | 5.394 | 5.457 | 5.394 | 5.313 | 5.355 | 5.313 |
| **PUE (giorno peggiore)** | 1,068 | 1,092 | 1,068 | 1,070 | 1,083 | 1,070 | 1,063 | 1,071 | 1,063 |

## 3. Catena delle temperature (giorno peggiore) e portate

| Grandezza | A-K1 | A-K2 | A-K3 | B-K1 | B-K2 | B-K3 | C-K1 | C-K2 | C-K3 |
|---|---|---|---|---|---|---|---|---|---|
| Mare alla presa, massimo (°C) | 24,7 | 24,7 | 21,7 | 24,7 | 24,7 | 21,7 | 24,7 | 24,7 | 21,7 |
| Scarico a mare (°C, limite 35) | 31,7 | 31,7 | 28,7 | 31,7 | 31,7 | 28,7 | 31,7 | 31,7 | 28,7 |
| Mandata FWS (°C) | 27,2 | 27,2 | 24,2 | 27,2 | 27,2 | 24,2 | 27,2 | 27,2 | 24,2 |
| Mandata liquido ai server TCS (°C, limite 45) | 30,7 | 30,7 | 27,7 | 30,7 | 30,7 | 27,7 | 30,7 | 30,7 | 27,7 |
| Aria ai rack dopo RDHx (°C) | 31,2 | 22,0 | 28,2 | 31,2 | 22,0 | 28,2 | 31,2 | 22,0 | 28,2 |
| Calore al liquido dei server (kW) | 4.435 | 4.435 | 4.435 | 4.788 | 4.788 | 4.788 | 4.850 | 4.850 | 4.850 |
| Calore all'aria totale (kW) | 708 | 708 | 708 | 372 | 372 | 372 | 242 | 242 | 242 |
| Calore ceduto al mare (kW) | 5.422 | 5.543 | 5.422 | 5.450 | 5.513 | 5.450 | 5.345 | 5.387 | 5.345 |
| Portata TCS totale (m³/h) | 399 | 399 | 399 | 431 | 431 | 431 | 349 | 349 | 349 |
| Portata FWS (m³/h, ΔT 8 K) | 584 | 597 | 584 | 587 | 594 | 587 | 575 | 580 | 575 |
| Portata acqua di mare (m³/h, ΔT 7 K) | 682 | 697 | 682 | 685 | 693 | 685 | 672 | 677 | 672 |

## 4. Elettrico (caso K2, il più gravoso)

| Grandezza | A | B | C |
|---|---|---|---|
| Potenza attiva totale (kW) | 5.503 | 5.457 | 5.355 |
| Potenza apparente, cos φ 0,95 (kVA) | 5.792 | 5.745 | 5.637 |
| Con margine 15 % (kVA) | 6.661 | 6.606 | 6.482 |
| Corrente MT a 20 kV per cavo, 2 × 100 % (A) | 192 | 191 | 187 |
| Trasformatori 20/0,415 kV a secco | 8 × 1.600 kVA | 12 × 1.250 kVA | 6 × 2.500 kVA |
| Potenza apparente per pod (kVA) | 1.366 | 911 | 1.807 |
| Carico di ogni trasformatore in 2N normale | 43 % | 36 % | 36 % |
| Carico di ogni trasformatore con il gemello fuori | 85 % | 73 % | 72 % |
| Corrente nominale BT per trasformatore (A) | 2.226 | 1.739 | 3.478 |
| Cortocircuito BT ai morsetti, uk 6 % (kA) | 37,1 | 29,0 | 58,0 |
| Corrente per rack per lato A o B a 415 V (A) | 199 | 79 | 284 |
| Carichi meccanici critici sotto UPS (kW) | 233 | 230 | 212 |

Sezione minima del cavo MT per tenere 16 kA per 1 s (Cu, XLPE, k = 143): **112 mm²** → si sceglie 3 × 120 mm² Cu (o 3 × 185 mm² Al). La portata (circa 300 A in posa sottomarina, da verificare sul catalogo) supera largamente la corrente di esercizio.

Caduta di tensione sul cavo MT (config A, 192 A, 350 m, 3 × 120 mm² Cu): 25,7 V = **0,13 %**: trascurabile.

Confronto con l'alimentazione in BT da terra (ADR 0001 dei repo precedenti): a 400 V servirebbero **9.614 A**, cioè circa 25 cavi da 240 mm² per fase su 250-350 m. Non praticabile: a 5 MW la MT fino alla TLP è obbligata.

## 5. Masse, baricentro e ingombri (presa 25 m)

| Grandezza | A | B | C |
|---|---|---|---|
| Container IT pieno (t, max lordo ISO 30,48) | 24,4 | 23,3 | 27,1 |
| Container inferiore potenza + CDU (t) | 20,6 | 19,4 | 24,2 |
| Skid scambiatori e pompe FWS (t) | 22,3 | 22,3 | 22,3 |
| Container MT e controllo (t) | 16,7 | 16,7 | 16,7 |
| Telaio, guide, passerelle (t) | 28,5 | 37,5 | 24,0 |
| **Massa totale sul ponte (t)** | 268 | 358 | 235 |
| Baricentro verticale sopra il ponte (m) | 2,55 | 2,63 | 2,49 |
| Ingombro 2 piani L × W (m) | 15,2 × 19,0 | 15,2 × 26,3 | 15,2 × 15,4 |
| Area 2 piani (m²) / quota del ponte 30 × 30 | 288 / 32 % | 399 / 44 % | 233 / 26 % |
| Ingombro 1 piano L × W (m) | 28,9 × 19,0 | 28,9 × 26,3 | 28,9 × 15,4 |
| Area 1 piano (m²) / quota del ponte | 549 / 61 % | 759 / 84 % | 443 / 49 % |
| Densità IT su ingombro 2 piani (kW/m²) | 17,5 | 12,6 | 21,4 |

Nota: una dimensione sopra 30 m o una quota oltre il 100 % indica che la soluzione a 1 piano non sta sul ponte 30 × 30 con questa disposizione.

## 6. Container superiore in rimorchio (config A)

Accelerazioni del documento SIZ0PLT001 rev 0 (TLP del pilota, da rifare per la TLP da 5 MW), fattore 1,3 proposto nel repo container.

| Grandezza | Valore |
|---|---|
| Forza laterale sul container IT (kN) | 107 |
| Momento ribaltante alla base (kNm) | 130 |
| Momento stabilizzante del peso (kNm) | 333 |
| Forza verticale massima (kN) | 366 |
| Prova di racking trasversale ISO 1496-1 (kN, riferimento) | 150 |

Il peso basta contro il ribaltamento, ma la forza laterale è dello stesso ordine della prova di racking di un container integro, e il container IT ha porte laterali che indeboliscono la parete. Servono **guide cellulari / telaio esterno** che portino le forze orizzontali al ponte, non solo twist-lock.

