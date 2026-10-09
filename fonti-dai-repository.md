# Cosa si è ripreso dai repository precedenti

Questo progetto parte dal lavoro su due repository dello stesso committente. Qui si elenca cosa è stato riusato e come, perché i dati restino tracciabili.

| Repository | Cosa è | Stato del progetto |
|---|---|---|
| `lorenzo591/powered_shell_container` | Powered shell su misura da 150 kW IT in un 20' HC, DLC + acqua di mare, senza chiller | Concept rev D |
| `lorenzo591/powered_shell_schneider-vertiv` | Pilota da 40 kW con Schneider Easy Modular 25', server ad aria, InRow | Specifica e domande al fornitore |

## Dati di sito ripresi (da riconfermare per la TLP da 5 MW)

| Dato | Valore | Fonte originale | Uso qui |
|---|---|---|---|
| Sito | TLP davanti al porto di Napoli, circa 200 m dalla costa | Cliente, 2026-09-25 | REQ-ENV-001; lunghezza dei cavi MT |
| Corrosività | CX (ISO 12944-2) | SIZ0PLT001 rev 0 | Container chiusi, nessuna aria esterna, verniciatura CX |
| Moti, accelerazioni di rimorchio, frequenze della piattaforma | Rollio 20°, Ay 3,36 m/s², Az 11,54 m/s²; 6,4–17,2 Hz | SIZ0PLT001 rev 0 (TLP pilota) | Verifica del container superiore, criterio > 21 Hz |
| Esercizio non presidiato, condensa presente | – | SIZ0PLT001 rev 0 | 2N, riavvio automatico, layout senza gocciolamenti |
| Temperatura del mare a 25 / 40 / 50 m | 24,7 / 22,8 / 21,7 °C massimi | Dataset Napoli 1987–2023 (doc. interno 2026-10-02), riportato in `confronto-inrow-cw-sorgenti-freddo.md` | Casi K1, K2, K3 |
| Limite di scarico | ≤ 35 °C, ≤ +3 °C a 1000 m | D.Lgs. 152/2006 | ΔT 7 K sul mare, studio di dispersione |

## Metodi e criteri ripresi

| Da | Cosa | Dove qui |
|---|---|---|
| container, `cooling/calcs/bilancio-termico-pue.md` | Catena chip → TCS → CDU → FWS → titanio → mare; formule; proprietà dei fluidi; prevalenza delle pompe sommerse senza dislivello dalla profondità di presa | `calcs/dimensionamento_5mw.py`, `cooling/` |
| container, ADR 0003 | Acqua di mare solo su skid esterno, mai vicino alle apparecchiature elettriche | Colonna servizi, parte bassa |
| container, ADR 0004 | Il liquido dei server non ha bisogno di chiller con la presa profonda | ADR 0002 |
| container, `mechanical/moti-e-accelerazioni.md` | Fattore 1,3 sulle accelerazioni; ancoraggio a pavimento e in testa; ritenuta positiva; niente supporti elastici; vasche per 15° | `mechanical/layout-e-masse.md` |
| container, ricerca DLC | Potenze, masse e quota al liquido di NVL72, HGX, Rubin; limite 45 °C; rischi di garanzia e biofouling | ADR 0005, configurazioni A/B/C |
| container, distinta | Classi di prodotto (Galaxy, Trihal/PrismaSeT, Canalis, Motivair, Alfa Laval, Grundfos SP R, Amiad, MGPS, VESDA, NetBotz) | `bom/distinta-preliminare.md` |
| schneider-vertiv, mail Schneider 2026-10-08 | Le motocondensanti DX non sono adatte all'ambiente costiero; verniciatura a catalogo C3-M non basta | Nessun condensatore ad aria: chiller condensati ad acqua |
| schneider-vertiv, confronto InRow CW | InRow CW alta temperatura e acqua di mare; chiller condensato ad acqua + free cooling dal mare | Chiller di rifinitura sul FWS (K2) |
| schneider-vertiv, specifiche strutturali 20' | Un container allestito non appoggia solo sui blocchi d'angolo; tavole del fornitore senza carichi da moto | Telaio con guide cellulari, verifica di rimorchio |
| schneider-vertiv, ADR 0007 | Costi di un modulo non ISO | Scelta di container ISO 40' HC |

## Cosa non si è ripreso, e perché

| Vincolo dei repo precedenti | Perché non vale a 5 MW |
|---|---|
| BT 400 V da terra, nessun trasformatore sulla TLP | Circa 9600 A: si passa alla MT (ADR 0001) |
| Massa ≤ 15 t, baricentro ≤ 1,32 m | Riferiti a un singolo container sulla TLP pilota |
| Raffreddamento ad aria con InRow (pilota) | Il cliente chiede cold plate |
| UPS centrale con autonomia | Sostituito da BBU nel rack + UPS solo per pompe e controlli (ADR 0004) |
