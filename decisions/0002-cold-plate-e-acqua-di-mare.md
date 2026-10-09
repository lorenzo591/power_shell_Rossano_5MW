# 0002 — Cold plate (DLC) con cessione al mare; chiller solo per la quota d'aria

- Data: 2026-10-09
- Stato: proposta
- Riprende ADR 0002 e 0004 del repo `powered_shell_container`, scalati a 5 MW

## Contesto

- Cliente, 2026-10-09: raffreddamento a cold plate, non più ad aria.
- Mare alla presa a 25 m: massimo circa 24,7 °C; a 50 m circa 21,7 °C (REQ-ENV-005, 006).
- I rack classe NVL72 cedono all'aria circa il 12 % (circa 600 kW su 5 MW).

## Decisione

1. TCS → CDU (2 per pod) → FWS chiuso ad acqua trattata → scambiatori a piastre in titanio 3 × 50 % → acqua di mare con pompe sommerse 3 × 50 %.
2. Nessun chiller sul liquido dei server: mandata circa 31 °C contro un limite di 45 °C.
3. Quota d'aria con porte posteriori raffreddate (RDHx) sul FWS e **chiller di rifinitura condensati ad acqua 2 × 100 % (circa 700 kW)** che lavorano solo con il mare sopra circa 19–20 °C.
4. Se il fondale permette la presa a 50 m, il chiller può diventare una riserva (aria circa 28 °C senza chiller).

## Alternative considerate

- **Solo mare a 25 m (K1)**: aria fino a circa 31 °C, fuori dai 27 °C raccomandati: rischio sulla garanzia dei server.
- **Dry cooler ad aria**: batterie alettate in aria salina CX, molto spazio sul ponte, aria fino a 38 °C. Scartato.
- **Immersione**: fluido a pelo libero su una struttura in mare, massa elevata. Scartato.

## Conseguenze

- Portata di mare circa 700 m³/h, scarico a circa 32 °C: permesso e studio di dispersione obbligatori.
- PUE circa 1,07–1,09.
- Compressori a bordo (solo nei chiller), refrigerante in volume chiuso: verifica EN 378.
