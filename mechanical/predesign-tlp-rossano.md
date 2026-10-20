# Pre-design della TLP al largo di Rossano (fondale 450 m)

- Revisione: A (2026-10-15). Prima versione.
- Numeri: [`calcs/risultati-tlp.md`](../calcs/risultati-tlp.md), generati da [`calcs/tlp_predesign.py`](../calcs/tlp_predesign.py).
- Livello: **studio di fattibilità con regole empiriche** (frazioni tipiche delle mini-TLP, nessuna analisi idrodinamica). I dati meteomarini e sismici del sito sono **stime da sostituire** con studi dedicati. Serve un progettista navale/offshore per la fase successiva.

## 1. Dati di ingresso e ipotesi

| Voce | Valore | Stato |
|---|---|---|
| Sito | Mar Ionio, al largo di Corigliano-Rossano, fondale circa 450 m | Cliente, 2026-10-15 |
| Ponte | Massimo 50 × 50 m | Cliente, 2026-10-15 |
| Moduli | Pod 40' HC su 2 piani, rack 140 kW (classe NVL72), 9 rack per pod, una colonna servizi ogni 4 pod | Config A, `calcs/dimensionamento_5mw.py` |
| Onda centenaria | Hs circa 8,5 m, Tp circa 12 s | **Stima n.v.** per lo Ionio settentrionale |
| Ponte in acciaio | 0,6 t/m² | Ipotesi n.v. |
| Sottostazione AT/MT, gru, salvataggio | 300 t + 200 t | Ipotesi n.v. |
| Scafo | 4 colonne, pontoni ad anello 7 × 7 m, immersione 22 m; acciaio 25 % del dislocamento | Regole empiriche mini-TLP |
| Tendini | 8 (2 per colonna), acciaio X70, tensione di tempesta 2,2 × pretensione, periodo di sussulto ≤ 3,5 s | Regole empiriche |
| Stabilità | GM ≥ 2 m all'installazione, prima del tiro dei tendini, con topside già montato in banchina | Criterio di progetto |

## 2. Potenza massima su un ponte 50 × 50 m

| Disposizione | Pod IT | Potenza IT con rack NVL72 (140 kW) | Con rack classe Rubin (200 kW) | Spazio per sottostazione, gru, pompe |
|---|---|---|---|---|
| **2 file di container** (raccomandata) | 20 | **circa 25 MW** | circa 36 MW | Fascia di 21 × 50 m: adeguata |
| 3 file di container | 31 | **circa 39 MW** | circa 56 MW | Fascia di 7 m: troppo stretta, serve un secondo livello |

Valore realistico: **25 MW con la tecnologia di oggi, circa 35 MW con quella del 2027**, lasciando un'area di servizio vera. Il massimo teorico (circa 39 MW, oltre 50 MW con Rubin) richiede di mettere sottostazione e servizi su un livello superiore.

## 3. Pesi e scafo

| Grandezza | 25 MW (2 file) | 39 MW (3 file) |
|---|---|---|
| Moduli IT, potenza e servizi | 1.256 t | 1.946 t |
| Topside totale con contingenza 15 % | **circa 3.700 t** | **circa 4.500 t** |
| Diametro delle 4 colonne (deciso dalla stabilità, non dal galleggiamento) | circa 10,5 m | circa 11,4 m |
| Interasse delle colonne | 38 m | 38 m |
| Dislocamento a 22 m di immersione | **circa 11.800 t** | **circa 12.800 t** |
| Acciaio dello scafo | circa 3.000 t | circa 3.200 t |
| Pretensione totale dei tendini | circa 4.500 t | circa 4.400 t |
| Tendini a 450 m | circa 1.200 t | circa 1.150 t |
| Massa per MW IT, scafo + topside | circa 270 t/MW | circa 200 t/MW |

Cosa decide le dimensioni:

- **La stabilità all'installazione, non il galleggiamento.** Con colonne dimensionate solo per galleggiare (5–7 m di diametro) la piattaforma si ribalterebbe nella fase in cui è zavorrata e i tendini non sono ancora in tiro (GM fortemente negativo). Servono colonne da 10–11 m. In alternativa si installa lo scafo prima e il topside dopo, in mare con una nave gru (più caro e più rischioso), oppure si usano moduli di stabilità temporanei.
- **L'effetto di scala è forte.** La stessa logica applicata ai 5 MW su 30 × 30 m dà circa 7.800 t di dislocamento e **circa 640 t per MW**, contro 200–270 t/MW del ponte 50 × 50. Una TLP solo per 5 MW è difficile da giustificare: lo scafo costa quasi come per 25 MW.
- **Ordine di grandezza confrontabile con le mini-TLP esistenti** nel Golfo del Messico, alcune proprio su fondali di 450–550 m (riferimento da verificare).

## 4. Fino a che profondità

| Profondità | Tendini | Peso in acqua / pretensione | Periodo di sussulto | Giudizio |
|---|---|---|---|---|
| **450 m (Rossano)** | circa 1.200 t, li decide la resistenza | 23 % | circa 2 s | **Fattibile, profondità comoda per una TLP** |
| 1.000 m | circa 2.600 t | 51 % | circa 3 s | Fattibile, ma metà della pretensione serve a reggere i tendini: scafo più grande |
| 1.500 m | circa 4.100–4.400 t | 78–87 % | 3,5 s (limite) | Al limite: servono tendini galleggianti. È più o meno il record mondiale delle TLP (circa 1.500–1.600 m, da verificare) |
| 2.000 m | circa 7.200–7.800 t | **139–154 %** | 3,5 s | **Non fattibile come TLP**: i tendini pesano più della pretensione disponibile |

**Conclusione:** la TLP va bene fino a circa 1.000 m e, con tendini speciali, fino a 1.500 m. Per 1.500–2.000 m si passa a un **semisommergibile con ormeggi tesi** in poliestere (tecnologia dell'eolico galleggiante e dell'oil & gas). I moti sono più ampi di una TLP ma restano gestibili per i rack se l'ancoraggio è positivo (REQ-MEC-006). A 450 m la TLP è la scelta giusta: è quasi ferma in verticale e in rollio e beccheggio, quindi è la piattaforma galleggiante migliore per l'IT.

## 5. Onde e quota del ponte

- Onda massima centenaria stimata circa 16 m, cresta circa 9,5 m sul medio mare.
- Aggiungendo marea, sovralzo, risalita dell'onda sulle colonne, abbassamento della piattaforma (circa 1 m a 450 m) e margine, l'**intradosso del ponte va a circa 14 m sul mare**, non i circa 5 m della TLP pilota (REQ-ENV-009 da aggiornare).
- Spostamento orizzontale in tempesta circa 30 m a 450 m di fondale. Cavi e tubi verso il fondo devono assorbirlo.

## 6. Rischi specifici di Rossano

1. **Sismica.** La Calabria è tra le zone più sismiche d'Italia. Per una TLP il rischio principale non è lo scuotimento orizzontale, che i tendini disaccoppiano, ma l'impulso verticale trasmesso dall'acqua e i picchi di tensione nei tendini e sulle fondazioni. Serve un'analisi sismica dedicata.
2. **Frane sottomarine e canyon.** La scarpata ionica calabrese è ripida e incisa da canyon, con correnti di torbida. È il rischio più importante per pali e cavi. Servono rilievi batimetrici e geofisici prima di scegliere il punto.
3. **Tsunami.** Nell'area sono documentati tsunami storici. In acqua profonda la TLP ne risente poco; il rischio vero è per il cavo e per l'approdo a terra.
4. **Meteomare.** I valori usati sono stime. Serve uno studio con hindcast dei dati e misure (boe di Crotone e Taranto).

## 7. Opportunità e conseguenze sugli altri impianti

- **Acqua fredda in profondità.** Con 450 m di fondale la presa può scendere a 100–200 m, dove nello Ionio l'acqua resta intorno ai 14 °C tutto l'anno (stima da verificare con profili CTD). Il chiller di rifinitura sparirebbe e il PUE scenderebbe ancora. Il tubo di presa lungo le colonne va previsto nel progetto dello scafo.
- **Elettrico.** A 450 m di fondale la costa è a qualche chilometro (da verificare in carta nautica). Per 25–40 MW il 20 kV non basta: serve un cavo di esportazione a **66 kV** (standard dell'eolico offshore, esiste in versione dinamica per piattaforme galleggianti), due cavi in 2N, con sottostazione 66/20 kV sulla piattaforma. La massa è già compresa nelle 300 t ipotizzate.
- **Accessibilità.** Con il ponte a 14 m e onde alte, l'accesso via mare va progettato (passerella compensata o elicottero). Va previsto un rifugio temporaneo per il personale di manutenzione.

## 8. Giudizio

- **Tecnicamente sostenibile a 450 m**, con un ponte di 50 × 50 m e **25 MW di IT oggi (circa 35 MW con Rubin)**. Servono circa 12.000 t di dislocamento, colonne da circa 11 m e 8 tendini da circa 150 t ciascuno.
- **Profondità massima sensata per la TLP: circa 1.000 m** (1.500 m al limite). A 2.000 m si cambia tipo di piattaforma.
- **Il rack da 140 kW resta essenziale**: con rack a bassa densità (SN50, Positron) la stessa piattaforma porterebbe un terzo della potenza.
- **Prossimi passi:** studio meteomarino e sismico del sito, batimetria e geofisica della scarpata, profilo di temperatura dell'acqua, pre-dimensionamento idrodinamico (RAO, tendini, fatica) da parte di un progettista offshore, ordine di grandezza dei costi di scafo, tendini e installazione.
