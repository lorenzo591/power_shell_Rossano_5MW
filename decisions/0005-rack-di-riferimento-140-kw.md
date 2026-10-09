# 0005 — Rack di riferimento da 140 kW (classe GB300 NVL72)

- Data: 2026-10-09
- Stato: proposta

## Contesto

- La densità del rack decide numero di container, ingombro e massa (`configurazioni/confronto-configurazioni.md` §2).
- Mercato (ricerca DLC del repo container): NVL72 120–155 kW, HGX 8-GPU circa 14 kW per server, Vera Rubin circa 190–200 kW a 800 V c.c.

## Decisione

- Progettare su rack da **140 kW, circa 1,55 t, 88 % al liquido**: 36 rack, 9 per pod.
- Ogni posizione rack deve poter ospitare un rack classe Rubin (fino a 200 kW, 1,85 t) come caso limite di massa e portata liquida; la potenza del pod resta limitata dai trasformatori.
- Server HGX (56 kW per rack) compatibili, con più pod.

## Alternative considerate

- **B, 56 kW per rack**: 6 pod, 14 container, circa 360 t, 44 % del ponte.
- **C, 200 kW per rack a 800 V c.c.**: 3 pod, 8 container, circa 235 t; tecnologia non ancora disponibile per noi.

## Conseguenze

- Vincoli per i tenant: rack DLC con ingresso liquido fino a 45 °C, alimentazione A/B a 415 V, BBU.
- Altezza interna del 40' HC (2690 mm) sufficiente ma stretta per rack da 2236–2258 mm più blindosbarre.
