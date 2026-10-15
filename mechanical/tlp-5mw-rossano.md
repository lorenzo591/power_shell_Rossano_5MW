# TLP minima da 5 MW al largo di Rossano (fondale 450 m): verifica

- Revisione: A (2026-10-15). Prima versione.
- Numeri: [`calcs/risultati-tlp-5mw.md`](../calcs/risultati-tlp-5mw.md), generati da [`calcs/tlp_5mw.py`](../calcs/tlp_5mw.py).
- Modello 3D: [`viewer/tlp-5mw-rossano.html`](../viewer/tlp-5mw-rossano.html).
- Norme di riferimento per il metodo: API RP 2T (TLP), DNV-OS-C105 (TLP), DNV-OS-C301 (stabilità), API 5L (tubi dei tendini).

## 1. Cosa è verificato e cosa no

**Verificato analiticamente** per la geometria scelta:
- bilancio di pesi e spinta;
- stabilità al galleggiamento;
- periodi propri di sussulto, beccheggio e surge;
- forze dell'onda di progetto (onda regolare di Airy, formula di Morison su colonne e pontoni, pressione dinamica sul fondo delle colonne, fasi reali su ogni elemento, incidenza a 0° e a 45°, tre periodi);
- vento, corrente, deriva media;
- spostamento orizzontale e abbassamento;
- tensione massima e minima dei tendini;
- resistenza e collasso dei tendini a 450 m;
- franco sotto il ponte;
- tiro di progetto dei pali;
- robustezza con Hs del 10 % più alta.

**Non verificato** (serve l'analisi idrodinamica del progetto di base):
- diffrazione e radiazione con un codice a pannelli;
- onda irregolare e deriva lenta;
- ringing e springing (coperti per ora con +15 % sulla parte d'onda dei tendini);
- fatica dei tendini e dei nodi;
- sisma (impulso verticale nei tendini);
- correnti di torbida sui pali;
- analisi strutturale di scafo e ponte;
- geotecnica dei pali.

**Dati di sito.** L'onda centenaria (Hs 8,2 m) è il valore più alto delle stime pubblicate per la boa RON di Crotone (7,2–8,2 m). Vento (32 m/s), corrente (1,0 m/s) e periodo dell'onda (10,5–12,5 s) sono ipotesi da confermare con uno studio meteomarino del punto scelto.

## 2. Topside

Config A ([`calcs/risultati.md`](../calcs/risultati.md)): 4 pod 40' HC su due piani (IT sopra, potenza e CDU sotto) più una colonna servizi (scambiatori e pompe, MT e controllo). Ingombro dei container circa 19 × 15 m.

Sul ponte servono anche gru, zattere, approdo e arrivo dei cavi: **ponte minimo 24 × 24 m** (dentro il limite di 30 × 30 di REQ-ENV-002).

| Voce | Massa (t) |
|---|---|
| Moduli IT, potenza, servizi, pompe di mare | 240 |
| Ponte in acciaio 24 × 24 m (0,75 t/m²) | 432 |
| Gru, salvataggio, approdo | 80 |
| **Totale con contingenza 15 %** | **864** |

## 3. La TLP più piccola: due modi di installarla

La geometria esce da una ricerca su interasse, diametro delle colonne, immersione e sezione dei pontoni. Il programma tiene quella di dislocamento minimo che passa tutte le verifiche, anche con Hs = 9,0 m.

| | **B · scafo e tendini prima, ponte e container sollevati in mare** (raccomandata) | A · topside montato in banchina, rimorchio integrato |
|---|---|---|
| Ponte | **24 × 24 m** | 35 × 35 m |
| Colonne | **4 × Ø 6,0 m**, interasse 18 m | 4 × Ø 9,0 m, interasse 26 m |
| Pontoni | 5 × 5 m | 5 × 5 m |
| Immersione | 19 m | 16 m |
| Fondo del ponte sul mare | 15 m | 15 m |
| Topside | 864 t | 1.424 t (ponte più grande) |
| Acciaio dello scafo | circa 1.200 t | circa 1.720 t |
| **Dislocamento** | **circa 3.430 t** | circa 5.920 t |
| Pretensione totale | circa 1.270 t (37 %) | circa 2.590 t (44 %) |
| Massa per MW, topside + scafo | circa 410 t/MW | circa 620 t/MW |
| Cosa decide le dimensioni | Tensione minima dei tendini con l'onda di progetto | Stabilità durante il rimorchio con il topside montato |

Perché A è più grande: con 1.400 t a 15–20 m sopra il mare e la pretensione sostituita da zavorra, la piattaforma galleggia senza tendini solo se ha colonne grandi e lontane. B rimanda il carico alto a quando i tendini sono già in tiro: lo scafo serve solo a portare il peso e a tenere i tendini tesi.

## 4. Verifiche della soluzione B

| Verifica | Valore | Limite | Esito |
|---|---|---|---|
| Spostamento orizzontale massimo (medio 15,2 m + onda 5,7 m) | 20,9 m | 36 m (8 % del fondale) | OK |
| Abbassamento per lo spostamento | 0,49 m | compreso nel franco | OK |
| Periodo di sussulto / beccheggio | 1,75 s / 1,56 s | ≤ 3,5 s (lontano dalle onde) | OK |
| Periodo di surge | 79 s | ≫ periodo d'onda | OK |
| Tensione massima per tendine | 2,86 MN | 0,6 Fy sul tubo: utilizzo 0,78 | OK |
| Tensione minima per tendine | 0,31 MN (20 % della pretensione) | ≥ 10 % | OK |
| Collasso idrostatico a 450 m (con 1,5) | utilizzo 0,80 | ≤ 1 | OK |
| Franco richiesto (cresta 9,7 m + 10 % + abbassamento + marea + 1,5 m) | 13,2 m | 15 m disponibili | OK |
| Robustezza con Hs 9,0 m: tensione minima / massima / franco | 0,22 MN / 2,96 MN / 14,5 m | > 10 % / ≤ 0,8 Fy / ≤ 15 m | OK |

Due fatti utili per il progetto:
- **La spinta verticale dell'onda quasi si annulla** (circa 150 kN): la pressione sul fondo delle colonne compensa quella sui pontoni. È l'effetto su cui si progettano le TLP, e va confermato con l'analisi a pannelli.
- **Il carico sui tendini viene dal momento ribaltante** (circa 59 MN·m), non dal sussulto.

**Tendini**: 8 tubi API 5L X65 da **406 × 11 mm**, lunghi circa 430 m, circa 48 t ciascuno. Sono chiusi e leggermente galleggianti (circa −11 t in acqua). Due per colonna, sui supporti esterni. Un tendine si può togliere per ispezione o sostituzione: con 7 su 8, anche con l'onda centenaria, la tensione massima sale a 3,48 MN (utilizzo 0,95) e la minima resta positiva (0,15 MN).

**Fondazioni**: un palo per tendine, o una piastra per colonna. Tiro di progetto circa **4,5 MN per palo** (1,5 × tensione massima più spinta del tendine). Scelta tra palo battuto e palo a suzione dopo il rilievo geotecnico.

## 5. Installazione della soluzione B (decisione REQ-MEC-009)

1. Scafo costruito in un cantiere navale; varo e rimorchio a Corigliano-Rossano o a Crotone. Galleggia stabile da solo (GM 3,5 m).
2. Pali e tendini posati da una nave d'appoggio; lo scafo si zavorra, si collega ai tendini e si toglie zavorra fino alla pretensione.
3. Ponte (circa 500 t) sollevato da una gru galleggiante. Poi i 10 container uno alla volta (17–27 t ciascuno) con la gru della nave, in una finestra di mare calmo. In alternativa ponte e container montati insieme a terra e sollevati in un solo colpo da circa 900 t.
4. Mentre si aggiunge il topside si toglie zavorra, così la pretensione resta nei limiti.

Il sollevamento in mare richiede una nave gru e la certificazione dell'operazione. In cambio lo scafo pesa circa il 40 % in meno di quello della soluzione A.

## 6. Collegamenti

- **Cavo MT**: a 20 kV per 5,5 MW (circa 170 A) su 10–15 km bastano 3 × 185 mm² Cu: caduta di tensione circa 3 %. Il cavo deve essere dinamico tra la TLP e il fondo, con profilo a onda pigra, per assorbire i circa 21 m di spostamento. Due cavi (2N), come in ADR 0004.
- **Presa d'acqua**: il fondale profondo permette di scendere a 100–150 m (acqua intorno ai 14 °C, da verificare con un profilo CTD). Il tubo di presa scende dentro o lungo una colonna e rende inutile il chiller.

## 7. Prossimi passi

1. Scelta del punto e rilievi: batimetria multibeam, geofisica della scarpata (frane, canyon), campioni di terreno per i pali.
2. Studio meteomarino del punto (hindcast + boa di Crotone): Hs, Tp, vento, corrente a 1, 10, 100 e 10.000 anni.
3. Studio sismico del sito per la verifica verticale dei tendini.
4. Progetto di base da parte di un progettista offshore: analisi a pannelli, dominio del tempo, fatica, analisi strutturale.
5. Decisione su REQ-MEC-009 (installazione A o B), con le offerte di cantiere e nave gru.
