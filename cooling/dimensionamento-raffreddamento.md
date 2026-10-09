# Dimensionamento del raffreddamento (configurazione A · K2)

- Revisione: A (2026-10-09).
- Numeri: [`calcs/risultati.md`](../calcs/risultati.md) §2 e §3. Decisioni: [ADR 0002](../decisions/0002-cold-plate-e-acqua-di-mare.md).
- Metodo e proprietà dei fluidi: come `cooling/calcs/bilancio-termico-pue.md` del repo `powered_shell_container` (Q = ṁ · cp · ΔT; P pompa = ρ · g · V · H / η). PUE secondo ISO/IEC 30134-2, confine all'arrivo MT sulla TLP.

## 1. Architettura: tre circuiti chiusi e uno aperto

```
 chip ─ cold plate ─ TCS (PG25 o acqua trattata) ─ CDU ─┐
                                                       │   FWS, circuito intermedio
 aria residua ─ porte posteriori RDHx ─ circuito aria ─┤   (acqua trattata, chiuso)
                    (chiller di rifinitura d'estate) ──┤
 perdite di trasformatori e quadri ─ unità aria/acqua ─┘
                                                       │
                       scambiatori a piastre in titanio, 3 × 50 %
                                                       │
           mare ← scarico a circa 32 °C ── pompe sommerse 3 × 50 % ← presa a 25 m (o 50 m)
```

- **TCS** (circuito server): dentro ogni pod, dalle 2 CDU del container inferiore ai collettori dei 9 rack. È il solo circuito che entra nei server.
- **FWS** (circuito intermedio): anello unico tra le 8 CDU, le unità aria/acqua e gli scambiatori. L'acqua di mare non entra mai nei container dei pod.
- **Acqua di mare**: solo nello skid scambiatori (container servizi, sotto) e nelle tubazioni verso le pompe sommerse.

Si esclude l'aria esterna (salina, CX): tutti i container sono chiusi, in leggera sovrappressione, deumidificati (obiettivo ISA-71.04 G1).

## 2. Catena delle temperature, giorno peggiore

| Punto | K1 presa 25 m | **K2 presa 25 m + chiller** | K3 presa 50 m |
|---|---|---|---|
| Mare alla presa (massimo 1987–2023) | 24,7 °C | 24,7 °C | 21,7 °C |
| FWS in mandata (avvicinamento scambiatore 2 K + 0,5 K) | 27,2 °C | 27,2 °C | 24,2 °C |
| Liquido ai server, TCS (avvicinamento CDU 3,5 K) | 30,7 °C | 30,7 °C | 27,7 °C |
| Margine sul limite dei server (45 °C, classe W45) | 14 K | 14 K | 17 K |
| Aria ai rack dopo le RDHx | 31,2 °C | **22 °C** | 28,2 °C |
| Scarico a mare (ΔT 7 K; limite 35 °C) | 31,7 °C | 31,7 °C | 28,7 °C |

**Lato liquido.** Nessuna configurazione ha bisogno di chiller: anche con il mare al massimo il liquido arriva ai server sotto i 31 °C. Il margine si può usare per tenere la mandata TCS più alta (35–40 °C) e ridurre portate e pompe.

**Lato aria.** Il rack classe NVL72 cede all'aria circa il 12 % della potenza (alimentatori, schede di rete, switch). Con il solo mare l'aria arriva a circa 31 °C nel giorno peggiore: dentro i 32 °C ammessi ASHRAE A1, fuori dai 27 °C raccomandati. Per un data center commerciale con server di terzi e garanzie del costruttore, si aggiunge un **chiller di rifinitura** solo per il circuito dell'aria (K2). Con la presa a 50 m (K3) l'aria resta a circa 28 °C: il chiller diventa una riserva.

## 3. Bilancio termico (configurazione A)

| Voce | kW |
|---|---|
| Calore al liquido (88 % di 5040 kW) | 4435 |
| Calore all'aria dai rack (12 %) | 605 |
| Perdite trasformatori, distribuzione BT, involucri (sole) | 103 |
| Pompe, ventole, chiller, HVAC, controlli (tutto finisce in acqua) | circa 400 |
| **Calore ceduto al mare** | **circa 5540** |

## 4. Componenti e taglie

| Circuito | Componente | Quantità | Taglia (ipotesi) | Esempi di prodotto (da verificare) |
|---|---|---|---|---|
| TCS | CDU liquido-liquido a pavimento | 8 (2 per pod, ciascuna regge il pod da sola) | circa 1,2–1,4 MW, circa 100 m³/h, avvicinamento 3–4 K; pompe ridondanti a velocità variabile | Vertiv CoolChip CDU 1350/2300, Motivair (Schneider) MCDU, CoolIT CHx, nVent |
| TCS | Collettori di rack, raccordi rapidi con fermo meccanico, tubazioni inox 316L | 36 rack | circa 11 m³/h per rack (1,5 L/min per kW) | – |
| TCS | Fluido | circa 2–3 m³ per pod | PG25 o acqua trattata secondo il costruttore (≤ 25 µS/cm, filtri 25–50 µm) | Linee guida OCP |
| Aria | Porte posteriori raffreddate (RDHx) | 36 | circa 17–20 kW ciascuna; passive se le ventole del rack bastano | Motivair ChilledDoor, Vertiv, USystems |
| Aria | Unità aria/acqua nel container inferiore | 4 + 4 | circa 15 kW (perdite di trasformatori e quadri) | Ventilconvettori a soffitto o InRow CW |
| Aria | **Chiller di rifinitura** condensato ad acqua sul FWS | 2 × 100 % | circa **700 kW frigoriferi**, acqua all'aria a circa 18 °C, COP circa 6; lavora con il mare sopra circa 19–20 °C | Chiller a vite o centrifughi oil-free condensati ad acqua, in involucro chiuso |
| FWS | Pompe | 3 × 50 % | circa 300 m³/h a 25 m ciascuna, circa 30 kW | Grundfos TPE / NBE, Wilo |
| FWS | Vaso di espansione a membrana, trattamento, degasatore | 1 set | – | Reflex |
| Mare | Scambiatori a piastre in titanio, guarnizioni EPDM | **3 × 50 %** | circa 2,8 MW ciascuno, avvicinamento 2 K; uno si pulisce mentre gli altri due lavorano | Alfa Laval serie T20/M15, Kelvion NT |
| Mare | Pompe sommerse in acciaio 904L o super duplex | **3 × 50 %** | circa **350 m³/h a 25 m** ciascuna, circa 37 kW | Grundfos SP R (taglia grande), KSB UPA |
| Mare | Filtri autopulenti | 2 × 100 % | circa 700 m³/h, 250–500 µm, super duplex o 254SMO | Amiad, Filtersafe |
| Mare | Antivegetativo | 1 | Anodi rame/alluminio (MGPS) o elettroclorazione con limiti di cloro allo scarico | Cathelco/Evac, De Nora SANILEC |
| Mare | Tubazioni di presa e scarico | 1 + 1 | **DN350** (circa 2 m/s a 700 m³/h), super duplex o vetroresina, lungo le colonne della TLP | – |

Portate complessive: TCS circa 400 m³/h (somma dei pod), FWS circa **600 m³/h** (ΔT 8 K), mare circa **700 m³/h** (ΔT 7 K).

## 5. Presa e scarico a mare

- **Prevalenza delle pompe**: la profondità della presa non aggiunge dislivello statico (il tubo è pieno d'acqua). Si solleva solo dal pelo libero al ponte (circa 5 m, da riconfermare per questa TLP) più filtri, scambiatori, tubi e diffusore di scarico: circa 25 m.
- **Presa a 50 m (K3)**: guadagna circa 3 K d'estate e toglie quasi del tutto il chiller. Serve un fondale di almeno 55–60 m e un tubo di presa più lungo lungo una colonna della TLP.
- **Scarico**: circa 700 m³/h a circa 32 °C. Il D.Lgs. 152/2006 (All. 5, Tab. 3) chiede ≤ 35 °C allo scarico e ≤ +3 °C a 1000 m. A questa portata serve uno **studio di dispersione del pennacchio** e probabilmente un diffusore in profondità. È il permesso più critico (Autorità di Sistema Portuale, Regione).
- **Durante il rimorchio** il circuito dell'acqua di mare è fermo: pompe sommerse protette o installate dopo.

## 6. Esercizio a carico parziale (fase iniziale)

Con pochi pod accesi (per esempio 1 pod, circa 1,26 MW):

- 1 scambiatore e 1 pompa di mare bastano; pompe a velocità variabile regolate sulla temperatura;
- le CDU dei pod spenti restano ferme, il FWS circola solo dove serve;
- il PUE sale (ausiliari fissi), ma resta sotto circa 1,15.

## 7. Rischi principali

1. Temperatura reale del mare alla quota di presa (il dataset va qualificato: se sono medie mensili, i picchi giornalieri sono più alti).
2. Permesso allo scarico termico di circa 5,5 MW.
3. Biofouling a questa portata: filtri, antivegetativo, scambiatori da pulire a rotazione.
4. Perdite di glicole (se TCS in PG25): vasche di contenimento sotto CDU e collettori, rilevazione perdite.
5. Garanzia dei server con aria fino a 31 °C (K1) o con installazione offshore in generale.

## 8. Da verificare

- Avvicinamenti di CDU (3–4 K) e scambiatori (2 K) con i fornitori.
- Quota d'aria residua del rack scelto (12 % ipotizzato).
- Prevalenze reali delle pompe con il percorso dei tubi sulla TLP.
- Temperatura ammessa all'aria dai rack e dai componenti di rete.
