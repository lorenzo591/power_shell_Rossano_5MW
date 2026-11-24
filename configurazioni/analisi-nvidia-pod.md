# NVIDIA POD (DGX SuperPOD / NVL72) sulla powered shell da 5 MW: è adatto?

- Revisione: A (2026-11-24). Prima versione.
- Base: configurazione raccomandata A · 2 piani · K2 · E2 ([`confronto-configurazioni.md`](confronto-configurazioni.md)), numeri da [`calcs/risultati.md`](../calcs/risultati.md).
- Fonti esterne: documentazione pubblica NVIDIA e schede dei costruttori OEM, consultate il 2026-11-24 (elenco in fondo). I valori presi da schede OEM sono **n.v.** finché NVIDIA o il costruttore scelto non li confermano per iscritto.

## 0. Risposta breve

**Sì come architettura, no come acquisto "chiavi in mano" così com'è.**

- La shell è già progettata attorno al rack classe GB300 NVL72, cioè al mattone del DGX SuperPOD. Il pod da 1,26 MW con 9 posizioni rack coincide quasi esattamente con una **scalable unit (SU)** del SuperPOD: 8 rack NVL72, circa 1,1–1,2 MW. **1 pod = 1 SU; 4 pod = 4 SU = 32 rack, 2304 GPU.**
- Liquido, ridondanza elettrica e atmosfera interna sono compatibili con quanto NVIDIA chiede, con margine.
- I punti che non tornano non sono di potenza o di raffreddamento ma di **sito offshore**: trasporto e rimorchio dei rack, supporto e garanzia su una piattaforma non presidiata, assenza di BBU "da minuti" nel rack standard, spazio e aria per rete e storage, potenza per pod insufficiente per la generazione Vera Rubin.
- Raccomandazione: progettare la shell **"SU-aligned / NVL72-ready"** (non legata al marchio DGX), lasciare al tenant la scelta tra DGX SuperPOD e NVL72 OEM, e chiudere con NVIDIA e almeno un OEM le 8 domande del §6 prima di congelare il pod.

## 1. Che cosa si intende per "NVIDIA POD"

| Offerta | Cos'è | Mattone | Potenza tipica | Pertinenza per noi |
|---|---|---|---|---|
| **DGX SuperPOD (GB200/GB300)** | Cluster chiavi in mano NVIDIA: rack DGX GB300, rete InfiniBand/Spectrum-X, storage certificato, software Mission Control, installazione NVIDIA | SU = 8 rack NVL72 (576 GPU) | circa 1,2 MW per SU (dato NVIDIA per GB200) | Alta: è il carico per cui la shell è dimensionata |
| **DGX SuperPOD / BasePOD (B300 HGX)** | Stesso concetto con server 8-GPU DGX B300 | 4 server per rack, circa 56 kW (variante AC) | circa 1,1 MW ogni 32 server (n.v.) | Media: è la nostra configurazione B |
| **NVL72 OEM / Enterprise Reference Architecture** | Rack GB300 NVL72 di Supermicro, HPE, Lenovo, Gigabyte, Dell… con architettura di riferimento NVIDIA | Rack NVL72 | 120–142 kW per rack | Alta: stessa fisica del DGX, contratti di supporto più flessibili |
| **Vera Rubin NVL72 (ex NVL144)** | Generazione successiva, stesso rack "Oberon" MGX, 800 V c.c. opzionale | Rack | circa 190–230 kW per rack (n.v.) | Media: arriva durante la vita della shell |
| **Kyber (Rubin Ultra)** | Rack 800 V c.c. da diverse centinaia di kW | Rack | 600 kW–1 MW (fonti secondarie) | Bassa: 2027–2028, fuori dalla geometria del 40' HC |

## 2. Verifica punto per punto (configurazione A)

| Tema | Cosa chiede un POD NVL72 | Cosa offre la shell | Esito |
|---|---|---|---|
| **Potenza per SU** | 8 rack × circa 140 kW + rete ≈ 1,2 MW | Pod da 1,37 MVA, 2 × 1600 kVA (2N), 9 posizioni rack + 2 posizioni rete | ✅ 1 pod = 1 SU. La 9ª posizione rack resta libera per rete/storage o riserva |
| **Scala** | SuperPOD da 1 a 4+ SU (oltre 4 SU progetto con NVIDIA) | 4 pod | ✅ 4 SU = 32 rack, circa 4,5 MW di calcolo + rete e storage ≈ 5 MW |
| **Liquido ai server** | Compatibile W45; ingresso TCS fino a 45 °C (Lenovo: 2–50 °C) | TCS a circa 31 °C nel giorno peggiore | ✅ 14 K di margine |
| **Portata TCS** | Lenovo GB300: circa 71 L/min per rack a 30 °C, 177 L/min a 45 °C | Ipotesi di progetto 1,5 L/min per kW = 210 L/min per rack | ✅ CDU e pompe sono sovradimensionate per i 31 °C; la portata del progetto serve se si alza la mandata verso 45 °C. Vedi §5.3 |
| **Calore all'aria** | circa 12–15 % del rack, più **rack di rete e storage interamente ad aria** | 12 % su 140 kW + 10–20 kW per pod di rete | ⚠️ La rete di una SU (switch InfiniBand/Spectrum-X, gestione) e lo storage possono valere decine di kW per pod: va rifatto il bilancio dell'aria con la BoM reale (§5.2) |
| **Ridondanza** | NVIDIA chiede un sito almeno Tier III / EN 50600 classe 3 (manutenibile senza fermo, nessun punto singolo di guasto) | 2N da MT ai rack, CDU 2N, mare 3 × 50 % | ✅ L'impianto è allineato. Unico punto singolo: la piattaforma stessa (cavi in un solo corridoio, presa a mare) |
| **Alimentazione del rack** | 6–8 power shelf da 33 kW, ingresso CA trifase, barra 50–54 V c.c. nel rack | Blindosbarre A/B a 415 V, circa 200 A per lato | ✅ Da confermare connettori e numero di prese per il rack scelto |
| **Continuità (BBU)** | Le schede NVL72 trovate **non riportano BBU di serie**; il GB300 ha accumulo per il *power smoothing* (secondi, non minuti) | ADR 0004 (E2) presuppone BBU 1,5–5 min nel rack | ❌ Ipotesi E2 non confermata: vedi §4.2 |
| **Massa del rack** | HPE: circa 1,47 t con alimentazione e raffreddamento (n.v.) | 1,55 t per posizione | ✅ Ipotesi conservativa |
| **Ingombro del rack** | 600 × 1068–1200 × 2236–2296 mm (Vertiv: 2286 mm) | Altezza interna 2690 mm, ipotesi rack 2236–2258 mm | ⚠️ Con il rack Vertiv restano circa 400 mm (non 430) per 2 blindosbarre e rivelazione |
| **Atmosfera** | ISA-71.04 G1, nessuna aria salina | Container chiusi, sovrappressione, filtri chimici, obiettivo G1 | ✅ |
| **Trasporto e moti** | Rack consegnato integrato con imballo e limiti di urto del costruttore; nessun dato pubblico per rimorchio marino | Rimorchio con rollio 20°, Az 11,5 m/s² (TLP pilota) | ❌ Vedi §4.1 |
| **Supporto e garanzia** | Supporto NVIDIA/OEM con sostituzione parti in sito e tempi da contratto | Piattaforma non presidiata, accesso via mare col bel tempo | ❌ Vedi §4.3 |
| **Rete verso terra** | North-south a 100–800 Gb/s per tenant, gestione fuori banda | Fibra da terra prevista nella colonna servizi | ⚠️ Servono almeno 2 fibre in percorsi diversi (oggi non è un requisito) |

## 3. Dove il POD si sposa bene con la shell

1. **Modularità identica.** La SU è l'unità di crescita del SuperPOD, il pod è l'unità di installazione della shell (ADR 0003: un pod alla volta). Si può partire con 1 SU (1,2 MW, 1 pod + servizi) e crescere di una SU alla volta senza rifare l'impianto.
2. **Raffreddamento senza chiller sul liquido.** Il mare a 21–25 °C dà un TCS a 28–31 °C: con un rack W45 il margine è il più ampio che si possa avere. È un argomento di vendita verso NVIDIA e i tenant (PUE circa 1,07–1,09, nessun consumo d'acqua dolce).
3. **2N elettrico.** È più di quanto chiedono le architetture di riferimento NVIDIA per il calcolo; è giustificato qui dal sito non presidiato.
4. **Stesso telaio per due generazioni.** Il rack Oberon/MGX ospita GB300 oggi e Vera Rubin NVL72 domani: le posizioni rack, i collettori e la massa ammessa (già dimensionata per 1,85 t, ADR 0005) restano validi.

## 4. Dove il POD non si sposa con la shell (da risolvere)

### 4.1 Rimorchio e moti

- Le accelerazioni di rimorchio ereditate (rollio 20°, Ay 3,4 m/s², Az 11,5 m/s²) sono molto oltre qualunque limite di trasporto pubblicato per server rack-scale. Il rack NVL72 contiene la spina NVLink (migliaia di cavi in rame, cartucce a innesto) e 18 compute tray con raccordi rapidi: è il componente più sensibile di tutto l'impianto.
- **Conseguenza:** l'opzione "rimorchio con i container IT vuoti e rack installati in banchina" (layout §5, punto 4) diventa **obbligatoria** con un POD NVL72, non un'alternativa. Questo va scritto nel requisito di installazione (REQ-MEC-009) e nel piano di montaggio.
- In esercizio la TLP ha moti piccoli ma frequenze proprie di 6,4–17,2 Hz (REQ-ENV-011, da rifare): serve la **specifica di vibrazione in esercizio** del rack dal costruttore e, se necessario, supporti antivibranti sotto il container IT o sotto i rack (n.v.).

### 4.2 Continuità: niente BBU da minuti nel rack standard

- ADR 0004 sceglie E2 a condizione che il rack abbia BBU da 1,5–5 min. Nelle schede GB300 NVL72 consultate non c'è: il rack ha accumulo per livellare i picchi di potenza, non per superare una mancanza rete.
- Senza generatore a bordo, l'autonomia di pochi minuti serve solo a un arresto ordinato. Per un cluster di addestramento con checkpoint periodici, perdere i rack di colpo costa il lavoro dall'ultimo checkpoint, non l'hardware, **purché le pompe continuino a girare** finché i chip si raffreddano.
- **Proposta (E2-bis):** mantenere il 2N in MT/BT, nessuna BBU obbligatoria nel rack, UPS degli ausiliari (già previsto, circa 300 kW) che tiene CDU, pompe e controlli. Le BBU nel rack diventano un'opzione del tenant (alcuni OEM offrono power shelf con batteria: n.v.). Va registrato come revisione dell'ADR 0004 dopo la risposta dei costruttori; non è necessario ricadere su E1 (UPS centrale, +40–60 t).

### 4.3 Supporto, garanzia e manutenzione senza presidio

- Il SuperPOD è venduto con supporto NVIDIA e installazione NVIDIA o partner; i contratti standard presuppongono accesso al sito in tempi brevi. Sulla TLP l'accesso dipende dal mare.
- Guasti tipici di un NVL72: compute tray, switch tray NVLink, ottiche, alimentatori, perdite ai raccordi. Un compute tray è un componente da circa 30–40 kg (n.v.) che va sostituito da personale addestrato.
- **Conseguenze:** scorta di ricambi a bordo (tray, ottiche, PSU) nella zona libera del container IT (x 8100–12 030 mm), contratto di supporto con tempi legati alla finestra meteo, personale del gestore certificato dal costruttore per le sostituzioni di primo livello, e **clausola esplicita di garanzia per installazione offshore** (già tra le domande aperte del README, punto 4). Senza questa clausola un POD NVIDIA non è finanziabile da un tenant.

### 4.4 Rete e storage: posto e aria

- Una SU NVL72 ha bisogno di switch di calcolo (InfiniBand Quantum-X800 o Spectrum-X), switch di storage e gestione, e lo storage stesso. Nelle architetture di riferimento questi sono **rack separati e raffreddati ad aria**.
- Le 2 posizioni rete per pod (10–20 kW) potrebbero non bastare; la 9ª posizione rack e la zona libera del container IT danno spazio, ma il calore all'aria cresce: il chiller di rifinitura (K2, circa 700 kW) va ricontrollato con la BoM di rete e storage reale.
- Lo storage condiviso tra le 4 SU può stare nella colonna servizi o in un container dedicato: da decidere con il tenant.

### 4.5 La generazione successiva non entra nel pod di oggi

- Una SU Vera Rubin NVL72 (8 rack × circa 190–230 kW, n.v.) vale circa 1,6–1,9 MW: **più dei 1,37 MVA del pod** (2 × 1600 kVA con il gemello al 85 % in guasto).
- Con i trasformatori attuali un pod regge 6 rack Rubin, cioè non una SU intera: si perde la corrispondenza 1 pod = 1 SU proprio quando il tenant aggiorna l'hardware.
- **Raccomandazione:** riservare nel container inferiore lo spazio e le risalite per **2 × 2500 kVA per pod** (configurazione C del confronto) o almeno blindosbarre e quadri BT dimensionati per 2 MW per pod, anche se oggi si installano i 1600 kVA. Il costo di un'eventuale sostituzione dei trasformatori a bordo è molto più alto del sovradimensionamento iniziale (n.v., da quotare).
- La massa del container IT con 9 rack Rubin (circa 27 t, `calcs/risultati.md` §5 config C) resta sotto il limite ISO, ma senza margine per la variante A+.
- Kyber (Rubin Ultra, 800 V c.c., rack da centinaia di kW, 2027–2028) non entra nella geometria del 40' HC: la shell non deve inseguirlo.

### 4.6 Potenza vista dalla rete

- I carichi di addestramento oscillano in modo sincrono (tutte le GPU insieme) con salti di MW in tempi di secondi. Su due cavi sottomarini MT verso una rete locale il distributore può chiedere limiti alle variazioni di potenza.
- Il GB300 ha il *power smoothing* nel rack; va chiesto al costruttore il profilo di potenza della SU e al distributore il limite ammesso (si aggiunge alle domande sulla connessione, REQ-PWR-006).

## 5. Effetti sui documenti di progetto

1. **Pod = SU**: rendere esplicito nel requisito che il pod deve contenere una SU NVIDIA (8 rack NVL72 + rete) con i suoi servizi. Nuovo requisito proposto: REQ-IT-011.
2. **Aria residua**: aggiungere al bilancio termico i rack di rete e storage ad aria (oggi 10–20 kW per pod, da sostituire con la BoM di una SU).
3. **Portata TCS**: oggi 1,5 L/min per kW (circa 210 L/min per rack). Con mandata a circa 31 °C il rack GB300 chiede circa 71–75 L/min (Lenovo, n.v.). Tenere la portata di progetto solo se si vuole poter alzare la mandata verso 40–45 °C; altrimenti CDU e pompe TCS si possono ridurre.
4. **Altezza utile**: verificare l'altezza sopra il rack con il rack più alto del mercato (2286–2296 mm).
5. **ADR 0004**: condizione BBU non soddisfatta dai rack standard → proposta E2-bis (§4.2).
6. **REQ-MEC-009**: installazione dei rack in banchina, mai a bordo durante il rimorchio.
7. **Trasformatori per pod**: riserva per 2 MW per pod (§4.5).

Questi punti **non sono ancora applicati** allo script e ai documenti: vanno decisi prima, perché cambiano i numeri di `calcs/dimensionamento_5mw.py`.

## 6. Domande per NVIDIA e per gli OEM (da inviare)

1. Composizione di una SU GB300 NVL72: numero e potenza dei rack di rete e gestione, quota ad aria, storage consigliato per 4 SU.
2. Specifica di urto e vibrazione del rack NVL72 in trasporto e in esercizio; trasporto ammesso con rack integrato o solo con tray smontati.
3. Disponibilità di power shelf con batteria (BBU) e durata a pieno carico; in alternativa, comportamento del rack a una mancanza rete con le pompe che continuano a girare.
4. Garanzia e supporto per installazione su piattaforma offshore non presidiata: tempi, ricambi a bordo, interventi di primo livello del gestore.
5. Requisiti del programma per data center "DGX-Ready" (o equivalente OEM) e se una shell offshore può esservi qualificata.
6. Profilo di potenza di una SU durante l'addestramento (gradini, tempi, effetto del power smoothing).
7. Vera Rubin NVL72: potenza per rack, massa, portata e temperatura del liquido, 800 V c.c. opzionale o obbligatorio, date di consegna per un cliente non hyperscaler.
8. Tempi di consegna di una SU per un ordine nel 2027.

## 7. In generale: un POD NVIDIA ha senso per noi?

- **Come riferimento di progetto: sì.** Il mercato del calcolo ad alta densità si sta standardizzando sul rack NVL72/MGX e sulla SU da circa 1,2 MW. Una shell dichiarata "compatibile con una SU NVIDIA" è facile da spiegare a tenant e finanziatori, ed è già quasi la nostra configurazione A.
- **Come prodotto da comprare noi: dipende dal modello di business.** Una SU GB300 costa nell'ordine di decine di milioni di euro (n.v.); 4 SU portano il capitale IT ben oltre quello della shell. Se Sizable vende **potenza e raffreddamento** (powered shell), il POD lo compra il tenant e noi garantiamo l'idoneità del sito. Se Sizable vuole vendere **capacità GPU**, il POD diventa l'investimento principale e il rischio dominante diventa il supporto offshore (§4.3), non l'impianto.
- **Non legarsi al marchio DGX.** Gli NVL72 OEM hanno la stessa fisica (stessa SU, stesso rack, stesso liquido) e contratti di supporto più negoziabili: per un sito offshore è il canale più realistico. La shell va specificata per "rack classe NVL72 / MGX Oberon", come già fa l'ADR 0005.
- **Alternativa da tenere aperta: HGX B300 (configurazione B).** Server 8-GPU da circa 14 kW, rack da circa 56 kW e 0,75 t, componenti sostituibili un server alla volta, meno sensibili al trasporto. Costa 4 container e circa 90 t in più, ma per un sito non presidiato con tenant misti (inferenza, clienti più piccoli) la manutenibilità può valere più della densità.
- **Il DC minimo da 20 kW di Napoli** non può ospitare alcun POD NVIDIA (un solo NVL72 vale circa 140 kW): resta corretta la scelta di un server HGX singolo. Può però servire a provare le interfacce che un POD richiede: fibra da terra, monitoraggio remoto, procedure di intervento via mare.

## 8. Fonti consultate (2026-11-24)

- NVIDIA, DGX SuperPOD Reference Architecture GB200 — architettura: <https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-gb200/latest/dgx-superpod-architecture.html> (SU = 8 rack, 1,2 MW per SU, sito Tier III / EN 50600 classe 3)
- NVIDIA, DGX SuperPOD B300: <https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300/latest/dgx-superpod-architecture.html>
- NVIDIA, DGX GB300: <https://www.nvidia.com/en-au/data-center/dgx-gb300>
- NVIDIA, blog OCP 2025 su Vera Rubin e 800 V c.c.: <https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin>
- Lenovo, GB300 NVL72 specifiche ambientali (portata e temperatura del liquido): <https://pubs.lenovo.com/gb300-nvl72/server_specifications_environmental>
- Vertiv, SmartIT for NVIDIA GB300 NVL72 (dimensioni, 142 kW, barra 50 V c.c.): <https://www.vertiv.com/4a9fd7/globalassets/shared/vertiv-smartit-for-nvidia-gb300-nvl72_datasheet_englis_sl-80699.pdf>
- HPE, GB300 NVL72 (massa a pieno carico): <https://www.hpe.com/il/en/collaterals/collateral.a50009224enw.html>
- Gigabyte, GB300 NVL72 GIGAPOD (140 kW, CDU): <https://www.gigabyte.com/Enterprise/GIGAPOD-Pod-Scale/AI-DLC-POD_NVIDIA-GB300-NVL72>
- TrendForce (giugno 2026), 800 V opzionale su Vera Rubin: <https://www.trendforce.com/presscenter/news/20260625-13121.html>
- Tom's Hardware / DCD, Kyber spostato al 2028: <https://www.tomshardware.com/pc-components/gpus/nvidias-kyber-rack-for-rubin-ultra-slips-to-2028>, <https://www.datacenterdynamics.com/en/news/nvidia-pushes-kyber-release-to-2028-following-manufacturing-concerns-report/>
