# Calcoli

- `dimensionamento_5mw.py`: bilancio elettrico e termico, PUE, portate, masse, baricentro, ingombri e verifica di rimorchio per le configurazioni A, B, C e i casi di raffreddamento K1, K2, K3. Genera `risultati.md` e i disegni SVG in `mechanical/`.
- Uso: `python3 calcs/dimensionamento_5mw.py` (Python 3, solo libreria standard).
- Le ipotesi sono tutte in testa allo script, con la fonte.
- `general_compute_loi.py`: applica i rack della LOI General Compute (B300, Cerebras, d-Matrix, SN50, Positron) alla stessa disposizione a pod e scompone la massa sul ponte. Genera `risultati-general-compute.md`. Uso: `python3 calcs/general_compute_loi.py`.
- `tlp_predesign.py`: pre-dimensionamento della TLP al largo di Rossano (ponte 50 × 50 m, potenza massima, topside, scafo, tendini da 450 a 2000 m, franco sul mare). Genera `risultati-tlp.md`. Uso: `python3 calcs/tlp_predesign.py`.
- `tlp_5mw.py`: TLP minima per i 5 MW a Rossano (450 m): ricerca della geometria e verifica analitica (stabilità, onda centenaria, vento, corrente, offset, tendini, collasso, franco, pali). Genera `risultati-tlp-5mw.md`. Uso: `python3 calcs/tlp_5mw.py` (circa 1 minuto).
