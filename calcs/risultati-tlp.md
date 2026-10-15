# Pre-dimensionamento TLP al largo di Rossano (generato)

> Generato da `calcs/tlp_predesign.py`. Studio di fattibilità con regole empiriche: tutti i valori sono ipotesi n.v., i dati meteomarini sono stime da sostituire con lo studio di sito.

## 1. Potenza massima sul ponte 50 × 50 m (container 40' HC su 2 piani)

| Rack | File di container | Colonne | Pod IT | Colonne servizi | Fascia libera per AT/MT, gru, pompe (m) | Potenza IT (MW) |
|---|---|---|---|---|---|---|
| NVL72 (140 kW) | 2 | 26 | 20 | 6 | 21,1 | **25,2** |
| NVL72 (140 kW) | 3 | 39 | 31 | 8 | 7,4 (fascia stretta) | **39,1** |
| Rubin (200 kW) | 2 | 26 | 20 | 6 | 21,1 | **36,0** |
| Rubin (200 kW) | 3 | 39 | 31 | 8 | 7,4 (fascia stretta) | **55,8** |

## 2. Topside, scafo e tendini (rack NVL72)

| Grandezza | 2 file, 25,2 MW | 3 file, 39,1 MW |
|---|---|---|
| Moduli IT, potenza e servizi (t) | 1.256 | 1.946 |
| Ponte in acciaio 50 × 50 (t) | 1.500 | 1.500 |
| Sottostazione AT/MT (t) | 300 | 300 |
| Gru, salvataggio, antincendio (t) | 200 | 200 |
| **Topside con contingenza 15 % (t)** | 3.745 | 4.537 |
| Dislocamento minimo per il solo galleggiamento (t) | 8.322 | 10.083 |
| Colonne del solo galleggiamento: GM all'installazione (m) | -14,7 | -10,5 |
| **Diametro delle 4 colonne per GM ≥ 2 m all'installazione (m)** | 10,5 | 11,4 |
| Interasse delle colonne (m) | 38 | 38 |
| **Dislocamento a 22 m di immersione (t)** | 11.814 | 12.766 |
| Acciaio dello scafo (t) | 2.954 | 3.192 |
| Pretensione totale dei tendini (t) | 4.525 | 4.399 |
| Pretensione / dislocamento | 0,38 | 0,34 |
| Massa per MW IT, scafo + topside (t/MW) | 266 | 198 |

## 3. Tendini al variare della profondità

**2 file, 25,2 MW** (dislocamento 11.814 t, 8 tendini, tensione di tempesta 2,2 × pretensione)

| Profondità (m) | Tensione max per tendine (MN) | Sezione d'acciaio (cm²) | Governa | Massa tendini (t) | Peso in acqua / pretensione | Periodo di sussulto (s) | Spostamento in tempesta (m) | Abbassamento (m) |
|---|---|---|---|---|---|---|---|---|
| 450 | 12,2 | 420 | resistenza | 1.186 | 23 % | 1,9 | 32 | 1,1 |
| 1.000 | 12,2 | 420 | resistenza | 2.635 | 51 % | 2,9 | 70 | 2,5 |
| 1.500 | 12,2 | 431 | periodo | 4.061 | 78 % | 3,5 | 105 | 3,7 |
| 2.000 | 12,2 | 575 | periodo | 7.219 | 139 % | 3,5 | 140 | 4,9 |

**3 file, 39,1 MW** (dislocamento 12.766 t, 8 tendini, tensione di tempesta 2,2 × pretensione)

| Profondità (m) | Tensione max per tendine (MN) | Sezione d'acciaio (cm²) | Governa | Massa tendini (t) | Peso in acqua / pretensione | Periodo di sussulto (s) | Spostamento in tempesta (m) | Abbassamento (m) |
|---|---|---|---|---|---|---|---|---|
| 450 | 11,9 | 408 | resistenza | 1.152 | 23 % | 2,0 | 32 | 1,1 |
| 1.000 | 11,9 | 408 | resistenza | 2.561 | 51 % | 3,1 | 70 | 2,5 |
| 1.500 | 11,9 | 466 | periodo | 4.388 | 87 % | 3,5 | 105 | 3,7 |
| 2.000 | 11,9 | 621 | periodo | 7.801 | 154 % | 3,5 | 140 | 4,9 |

## 4. Franco sotto il ponte (onda centenaria stimata)

| Grandezza | Valore |
|---|---|
| Hs centenaria (m), stima n.v. | 8,5 |
| Tp (s), stima n.v. | 12,0 |
| Onda massima Hmax = 1,86 Hs (m) | 15,8 |
| Cresta sul medio mare (m) | 9,5 |
| + marea e sovralzo, risalita sulle colonne, margine, abbassamento a 450 m (m) | 4,7 |
| **Intradosso del ponte sul medio mare (m)** | **14,2** |

