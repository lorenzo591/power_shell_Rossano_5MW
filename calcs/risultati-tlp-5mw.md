# TLP minima per 5 MW al largo di Rossano (generato)

> Generato da `calcs/tlp_5mw.py`. Verifica analitica di primo livello (API RP 2T / DNV-OS-C105): onda regolare di progetto con Morison e fasi sugli elementi, analisi quasi statica dei tendini. Dati di sito in parte stimati (n.v.). Non sostituisce l'analisi idrodinamica.

## 0. Dati di sito usati

| Grandezza | Valore | Fonte |
|---|---|---|
| Fondale | 450 m | Cliente |
| Hs centenaria | 8,2 m | Boa RON di Crotone, stime pubblicate 7,2-8,2 m: si usa la più alta |
| Onda di progetto Hmax = 1,86 Hs | 15,3 m, periodi 10,5, 11,5, 12,5 s | Ipotesi n.v. sul periodo |
| Vento a 10 m, media 1 min, centenario | 32 m/s | Ipotesi n.v. |
| Corrente di superficie | 1,0 m/s | Ipotesi n.v. |
| Hs per la verifica di robustezza | 9,0 m | +10 % |
| Marea + sovralzo | 0,5 m | Ipotesi n.v. |

## A · topside montato in banchina, rimorchio integrato

### Geometria e pesi

| Grandezza | Valore |
|---|---|
| Ponte (m) | 35,0 × 35,0 |
| Intradosso del ponte sul medio mare (m) | 15,0 |
| Interasse delle colonne (m) | 26,0 |
| Diametro delle 4 colonne (m) | 9,0 |
| Immersione (m) | 16,0 |
| Pontoni (larghezza × altezza, m) | 5,0 × 5,0 |
| Moduli IT, potenza, servizi (t) | 240 |
| Ponte in acciaio (t) | 919 |
| Gru, salvataggio, approdo (t) | 80 |
| **Topside con contingenza 15 % (t)** | 1.424 |
| Acciaio dello scafo (t) | 1.720 |
| Zavorra fissa (t) | 177 |
| **Dislocamento (t)** | 5.916 |
| **Pretensione totale (t)** | 2.594 (44 % del dislocamento) |
| GM all'installazione con topside (m) | 1,00 |
| GM dello scafo senza topside (m) | 8,85 |
| Massa per MW IT, topside + scafo (t/MW) | 624 |

### Carichi ambientali e risposta

| Grandezza | Valore |
|---|---|
| Vento sul topside e sulle colonne (kN) | 437 |
| Corrente (kN) | 89 |
| Deriva media d'onda, stima (kN) | 79 |
| Onda che governa: periodo 12,5 s, incidenza 45° |  |
| Forza orizzontale d'onda, ampiezza (kN) | 16.008 |
| Forza verticale d'onda, ampiezza (kN) | 6.730 |
| Momento ribaltante netto al fondo, ampiezza (MN·m) | 117,4 |
| Spostamento medio (m) | 10,7 |
| Spostamento d'onda, ampiezza (m) | 7,1 |
| **Spostamento massimo (m)** (limite 36 m) | 17,8 |
| Abbassamento per lo spostamento (m) | 0,35 |
| Periodo di sussulto (s) | 1,75 |
| Periodo di beccheggio (s) | 1,23 |
| Periodo di surge (s) | 72 |

### Tendini (8, due per colonna)

| Grandezza | Valore |
|---|---|
| Pretensione per tendine (MN) | 3,18 |
| + abbassamento, marea, momento medio (MN) | 0,44 |
| ± onda, con +15 % per 2° ordine e ringing (MN) | 1,70 |
| **Tensione massima in testa (MN)** | 5,32 |
| **Tensione minima in testa (MN)** | 1,16 |
| Tubo scelto (diametro × spessore, mm) | 506 × 13 |
| Acciaio | API 5L X65 (Fy 448 MPa) |
| Utilizzo a trazione (σ / 0,6 Fy) | 0,98 |
| Pressione esterna a 450 m / collasso (con 1,5) | 0,93 |
| Massa di un tendine (t) | 71 |
| Peso in acqua di un tendine (kN, negativo = galleggiante) | -212 |
| Tensione minima al fondo (MN) | 1,16 |
| Tiro di progetto del palo, 1,5 × (tensione massima + spinta del tendine) (MN) | 8,3 |

### Esito delle verifiche

| Verifica | Esito |
|---|---|
| Stabilità all'installazione (GM ≥ 1 m) | OK |
| Tendine: tensione minima ≥ 10 % della pretensione | OK |
| Tendine: nessun allentamento al fondo | OK |
| Tendine: resistenza e collasso a 450 m | OK |
| Spostamento ≤ 8 % del fondale | OK |
| Periodo di sussulto ≤ 3,5 s | OK |
| Franco sotto il ponte | OK |
| Robustezza con Hs 9,0 m: tensione minima 0,99 MN (31 % della pretensione), massima 5,49 MN (≤ 0,8 Fy), franco richiesto 14,4 m | OK |
| Franco: richiesto 13,1 m (cresta 9,7 m + 10 % + abbassamento + marea + 1,5 m) | disponibile 15,0 m |

## B · scafo e tendini prima, topside sollevato in mare

### Geometria e pesi

| Grandezza | Valore |
|---|---|
| Ponte (m) | 24,0 × 24,0 |
| Intradosso del ponte sul medio mare (m) | 15,0 |
| Interasse delle colonne (m) | 18,0 |
| Diametro delle 4 colonne (m) | 6,0 |
| Immersione (m) | 19,0 |
| Pontoni (larghezza × altezza, m) | 5,0 × 5,0 |
| Moduli IT, potenza, servizi (t) | 240 |
| Ponte in acciaio (t) | 432 |
| Gru, salvataggio, approdo (t) | 80 |
| **Topside con contingenza 15 % (t)** | 864 |
| Acciaio dello scafo (t) | 1.200 |
| Zavorra fissa (t) | 103 |
| **Dislocamento (t)** | 3.433 |
| **Pretensione totale (t)** | 1.265 (37 % del dislocamento) |
| GM all'installazione con topside (m) | -5,46 |
| GM dello scafo senza topside (m) | 3,51 |
| Massa per MW IT, topside + scafo (t/MW) | 410 |

### Carichi ambientali e risposta

| Grandezza | Valore |
|---|---|
| Vento sul topside e sulle colonne (kN) | 296 |
| Corrente (kN) | 69 |
| Deriva media d'onda, stima (kN) | 55 |
| Onda che governa: periodo 10,5 s, incidenza 45° |  |
| Forza orizzontale d'onda, ampiezza (kN) | 10.975 |
| Forza verticale d'onda, ampiezza (kN) | 152 |
| Momento ribaltante netto al fondo, ampiezza (MN·m) | 58,7 |
| Spostamento medio (m) | 15,2 |
| Spostamento d'onda, ampiezza (m) | 5,7 |
| **Spostamento massimo (m)** (limite 36 m) | 20,9 |
| Abbassamento per lo spostamento (m) | 0,49 |
| Periodo di sussulto (s) | 1,75 |
| Periodo di beccheggio (s) | 1,56 |
| Periodo di surge (s) | 79 |

### Tendini (8, due per colonna)

| Grandezza | Valore |
|---|---|
| Pretensione per tendine (MN) | 1,55 |
| + abbassamento, marea, momento medio (MN) | 0,32 |
| ± onda, con +15 % per 2° ordine e ringing (MN) | 0,99 |
| **Tensione massima in testa (MN)** | 2,86 |
| **Tensione minima in testa (MN)** | 0,31 |
| Tubo scelto (diametro × spessore, mm) | 406 × 11 |
| Acciaio | API 5L X65 (Fy 448 MPa) |
| Utilizzo a trazione (σ / 0,6 Fy) | 0,78 |
| Pressione esterna a 450 m / collasso (con 1,5) | 0,80 |
| Massa di un tendine (t) | 48 |
| Peso in acqua di un tendine (kN, negativo = galleggiante) | -113 |
| Tensione minima al fondo (MN) | 0,31 |
| Tiro di progetto del palo, 1,5 × (tensione massima + spinta del tendine) (MN) | 4,5 |

### Esito delle verifiche

| Verifica | Esito |
|---|---|
| Tendine: tensione minima ≥ 10 % della pretensione | OK |
| Tendine: nessun allentamento al fondo | OK |
| Tendine: resistenza e collasso a 450 m | OK |
| Spostamento ≤ 8 % del fondale | OK |
| Periodo di sussulto ≤ 3,5 s | OK |
| Franco sotto il ponte | OK |
| Robustezza con Hs 9,0 m: tensione minima 0,22 MN (14 % della pretensione), massima 2,96 MN (≤ 0,8 Fy), franco richiesto 14,5 m | OK |
| Franco: richiesto 13,2 m (cresta 9,7 m + 10 % + abbassamento + marea + 1,5 m) | disponibile 15,0 m |

