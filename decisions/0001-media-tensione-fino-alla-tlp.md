# 0001 — Media tensione fino alla TLP, trasformatori a secco a bordo

- Data: 2026-10-09
- Stato: proposta
- Supera, per questo progetto, l'ADR 0001 dei repo `powered_shell_container` e `powered_shell_schneider-vertiv` (BT 400 V da terra, nessun trasformatore sulla TLP)

## Contesto

- Potenza al punto di consegna circa 5,5 MW, di progetto circa 6,7 MVA (`calcs/risultati.md` §4).
- In BT a 400 V servirebbero circa 9600 A, cioè circa 25 cavi da 240 mm² per fase su 250–350 m.
- Il proprietario della TLP del pilota escludeva trasformatori a bordo.

## Decisione

- 2 cavi sottomarini MT 20 kV (da confermare), 3 × 120 mm² Cu con fibra ottica integrata, 2 × 100 %.
- Quadro MT a 2 semisbarre senza SF6 nella colonna servizi.
- 8 trasformatori a secco in resina 1600 kVA 20/0,415 kV, 2 per pod, nel container inferiore di ogni pod.

## Alternative considerate

- **BT da terra**: non praticabile a questa potenza.
- **MT con trasformatori a terra e BT a 690 V**: circa 5600 A, ancora troppi cavi; e i server richiedono 415/240 V.
- **Trasformatori in olio o estere**: più compatti, ma liquido infiammabile e da contenere su una piattaforma non presidiata.

## Conseguenze

- Il vincolo "nessun trasformatore sulla TLP" va rinegoziato con il proprietario (REQ-PWR-007).
- Entrano a bordo quadri MT: personale qualificato PES/PAV per le manovre, procedure di accesso.
- Il calore dei trasformatori (circa 40 kW) si smaltisce sul circuito intermedio con unità aria/acqua, senza aria esterna.
