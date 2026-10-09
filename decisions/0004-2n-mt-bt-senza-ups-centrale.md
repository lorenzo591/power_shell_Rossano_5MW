# 0004 — 2N in MT e BT, batterie nel rack, nessun UPS centrale per l'IT

- Data: 2026-10-09
- Stato: proposta (condizionata alla disponibilità di BBU per il rack scelto)

## Contesto

- Piattaforma non presidiata: un guasto interno deve essere tollerato fino alla visita successiva.
- Nessun generatore a bordo: l'autonomia serve solo per pochi minuti.
- Un UPS centrale 2N per circa 5,5 MW con Li-ion richiederebbe circa 2–4 container e 40–60 t in più (n.v.).

## Decisione

- 2 cavi MT, 2 semisbarre, 2 trasformatori e 2 quadri BT per pod, 2 blindosbarre fino al rack (A/B).
- Continuità dei server con **BBU nel rack** o power shelf con accumulo (1,5–5 min).
- UPS 2N da circa 300 kW solo per pompe, CDU e controlli: il liquido deve circolare anche durante una mancanza rete.

## Alternative considerate

- **E1, UPS centrale 2N**: nessuna dipendenza dal rack, ma molto spazio e massa. Ricaduta se le BBU non sono disponibili.
- **E3, N**: più leggera, ma un guasto ferma un pod da 1,26 MW fino alla visita.

## Conseguenze

- Il costruttore dei rack deve confermare BBU, durata e vita delle celle (REQ-IT-009).
- Litio in ogni rack: da considerare nella valutazione del rischio incendio.
- Ogni trasformatore lavora al 43 % in esercizio normale, all'85 % con il gemello fuori.
