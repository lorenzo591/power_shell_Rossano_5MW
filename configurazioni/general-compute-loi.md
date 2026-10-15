# Opzioni della LOI General Compute: densità e massa sul ponte da 5 MW

- Revisione: C (2026-10-15). Aggiunte la §5 (prezzi e token per kW) e la §6 (costo del token e mercati per velocità).
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

## 5. Prezzi e token per kW (indagine di mercato, 2026-10-15)

Dati di mercato, non di progetto: **nessuno è un'offerta**, tutti n.v. Le fonti misurano cose diverse (modello, lunghezza dei prompt, precisione, versione del software), quindi i confronti valgono come ordine di grandezza.

### 5.1 Prezzo dell'hardware per kW

| Sistema | Prezzo stimato | kW | $/kW | Fonte |
|---|---|---|---|---|
| GB300 NVL72 (72 GPU) | 4,0–5,0 M$ (stime giornalistiche fino a 6–6,5 M$) | ~140 | **29–36 k$** (fino a ~45 k$) | Morgan Stanley (costo dei componenti, via LinkedIn); ordini piccoli (Data Gravity) |
| Rack HGX B300 (16 GPU) | 1,2 M$ | 28 | 43 k$ | Calcolatore TCO di GC |
| Cerebras CS-3 | 2,6 M$ | 46 | 57 k$ | Calcolatore TCO di GC (non chiaro se per sistema o per rack) |
| SambaNova SN50 (rack) | 1,6 M$ (noleggio 95 k$/mese) | 19–20 | 80–84 k$ | Calcolatore TCO di GC |
| Positron Atlas (server) | 175 k$ | 1,8–2 | 88–97 k$ | Positron |
| d-Matrix SquadRack | non pubblico | ~45 | – | – |

### 5.2 Token prodotti per kW (tok/s per kW IT)

Dipende soprattutto dalla **velocità per utente** richiesta (tok/s/utente): le GPU servono molti utenti lenti, i chip "decode" pochi utenti veloci.

| Modello | Sistema | 76 | 120 | 164 | 250 | 500 | 1000 | 2000 | Fonte |
|---|---|---|---|---|---|---|---|---|---|
| DeepSeek R1 671B | GB200 NVL72 | **3.074** | 2.132 | 437 | – | – | – | – | SemiAnalysis InferenceX, 8k/1k |
| DeepSeek R1 671B | GB300 NVL72 | ~4.150 a bassa interattività (MLPerf server) | | | | | | | MLPerf v6.0 (NVIDIA): 8.064 tok/s/GPU, ~1,95 kW/GPU |
| DeepSeek 671B | HGX B300 (rack 28 kW) | – | – | – | 102 | 45 | – | – | GC (stima da InferenceX) |
| DeepSeek 671B | SambaNova SN50 | – | – | – | 1.617 | 842 | 421 | – | GC, benchmark interno |
| MiniMax M2.7 230B | HGX B300 | – | – | – | 631 | – | – | – | GC |
| MiniMax M2.7 230B | SambaNova SN50 | – | – | – | 1.432 | 1.200 | 763 | 726 | GC, benchmark interno |
| MiniMax M2.7 230B | Cerebras CS-3 | – | – | – | – | – | – | 48 | GC |
| Llama 70B | Positron Atlas | ~675 a 152 tok/s/utente (batch 8) | | | | | | | Positron |

### 5.3 Lettura

- **A velocità normale (chat, API, 50–120 tok/s/utente) l'NVL72 è il migliore** sia in token per kW (circa 2.000–4.000 tok/s/kW su DeepSeek R1) sia in prezzo per kW (circa 30–36 k$/kW, il più basso della tabella). Capitale per unità di produzione: circa 8–10 $ per tok/s.
- **Sopra circa 150–200 tok/s/utente le GPU crollano** (GB200: da 3.074 a 437 tok/s/kW passando da 76 a 164 tok/s/utente). Lì SN50 dichiara 4–16 volte più token per kW del B300. È il mercato a cui punta GC (agenti, coding).
- I numeri SN50 e Cerebras sono **benchmark interni di GC**, che rivende quei prodotti; GC pubblica solo velocità da 250 tok/s/utente in su, dove le GPU sono più deboli. Il software delle GPU migliora in fretta: GB300 su DeepSeek R1 in MLPerf è passato da 2.907 a 8.064 tok/s/GPU in un anno.
- **Per la TLP conta anche la massa**: con 5 MW di NVL72 (268 t) si producono circa 15 milioni di tok/s, circa 56.000 tok/s per tonnellata sul ponte. SN50 a 250 tok/s/utente: circa 8 milioni di tok/s su 868 t, circa 9.300 tok/s per tonnellata.
- Conclusione: le posizioni rack da 140 kW a liquido restano la scelta giusta. Un tenant che vuole velocità molto alte per utente può usare Cerebras (46 kW, liquido) nelle stesse posizioni; SN50 e Positron restano esclusi per massa e ingombro (§3).

Fonti: [generalcompute.com](https://www.generalcompute.com/) (calcolatore TCO e dati di benchmark nel codice della pagina) · [SemiAnalysis InferenceX](https://inferencex.semianalysis.com/compare/deepseek-r1-b200-vs-gb200) · [NVIDIA, MLPerf](https://developer.nvidia.com/blog/nvidia-extreme-co-design-delivers-new-mlperf-inference-records/) · [Data Gravity, costo NVL72](https://www.datagravity.dev/p/how-much-does-an-nvidia-nvl72-cost) · [Spheron, GB300 vs GB200](https://www.spheron.network/blog/gb300-nvl72-vs-gb200-nvl72-pricing-availability-2026/) · [Positron Atlas](https://positron.ai/atlas).

## 6. Costo del token "a costo" e mercato per velocità

### 6.1 Costo per milione di token di output

Costo mensile per kW IT diviso per i token prodotti in un mese. Ipotesi (le stesse del calcolatore TCO di GC, salvo il PUE):

- Ammortamento hardware 48 mesi, nessun interesse. Energia 0,10 $/kWh (0,20 $/kWh come sensibilità) × PUE 1,07 (`calcs/risultati.md`). Altri costi operativi 3.000 $/rack/mese.
- **Escluso il costo della powered shell** (TLP, impianti, cavo MT): non ancora stimato in questa fase.
- Utilizzo 100 % (limite teorico) e 60 % (realistico).
- Token di output. I dati di GC escludono il prefill; quelli InferenceX e MLPerf lo comprendono.
- GB300 NVL72: prezzo 4,5 M$ con le prestazioni misurate sul GB200 (InferenceX), quindi stima prudente.

| Sistema e modello | tok/s/utente | tok/s per kW | $/M token, utilizzo 100 % | $/M token, utilizzo 60 % |
|---|---|---|---|---|
| NVL72, DeepSeek R1 (MLPerf GB300) | bassa | ~4.150 | 0,07 | 0,12 |
| NVL72, DeepSeek R1 (InferenceX GB200) | 76 | 3.074 | **0,10** | **0,16** |
| NVL72, DeepSeek R1 | 120 | 2.132 | 0,14 | 0,23 |
| NVL72, DeepSeek R1 | 164 | 437 | 0,67 | 1,12 |
| SN50, DeepSeek 671B (GC) | 250 | 1.617 | 0,47 | 0,78 |
| SN50, DeepSeek 671B (GC) | 500 | 842 | 0,90 | 1,50 |
| SN50, DeepSeek 671B (GC) | 1000 | 421 | 1,80 | 3,00 |
| HGX B300, DeepSeek 671B (GC) | 250 | 102 | 4,0 | 6,7 |
| HGX B300, DeepSeek 671B (GC) | 500 | 45 | 9,1 | 15,2 |
| HGX B300, MiniMax 230B (GC) | 250 | 631 | 0,65 | 1,08 |
| SN50, MiniMax 230B (GC) | 250 / 2000 | 1.432 / 726 | 0,53 / 1,04 | 0,88 / 1,74 |
| Cerebras, MiniMax 230B (GC) | 2000 | 48 | 10,5 | 17,5 |
| Positron, Llama 70B (Positron) | 152 | ~675 | 1,28 | 2,13 |

Con l'energia a 0,20 $/kWh i costi salgono del 4–10 %: l'ammortamento dell'hardware pesa molto più dell'energia. Verifica: InferenceX dà 0,090 $/M token per il GB200 a 76 tok/s/utente, coerente con lo 0,095 calcolato qui.

Prezzi di vendita di riferimento (OpenRouter, riportati nel codice di GC), per milione di token di output: DeepSeek 671B 0,43 $ · MiniMax M2.7 1,28 $ · Kimi K2.6 3,60 $ · GLM 5.2 4,28 $.

Il dato Cerebras (48 tok/s per kW) è probabilmente sottostimato: sembra misurato con pochi utenti contemporanei. Da chiedere a GC.

### 6.2 Mercati per velocità

| Fascia (tok/s/utente) | Usi | Sistema più economico | Prezzo e volume |
|---|---|---|---|
| < 50 | Lavori batch: documenti, dati sintetici, valutazioni | GPU NVL72 al massimo carico | Prezzo più basso, volumi grandi |
| 50–150 | Chat, API, copilot (una persona legge 5–10 parole al secondo) | **GPU NVL72** | **Mercato più grande**: prezzi bassi, volumi massimi |
| 150–500 | Agenti, coding, ragionamento lungo | Chip decode (SN50); GPU in calo | Mercato premium in crescita |
| 500–2000+ | Catene di agenti, voce in tempo reale | Cerebras, SN50 | Nicchia, prezzo per token alto |

La velocità non è una proprietà del rack ma un punto di lavoro scelto da chi lo gestisce: lo stesso NVL72 può servire 76 tok/s/utente a 0,10 $/M o 164 tok/s/utente a 0,67 $/M.

La TLP con rack NVL72 si colloca nella **fascia 50–150 tok/s/utente**: la "fabbrica di token" a basso costo e grandi volumi. Come powered shell vendiamo kW di potenza; la fascia la sceglie il tenant. Le posizioni a liquido da 140 kW accettano anche Cerebras per la fascia veloce.
