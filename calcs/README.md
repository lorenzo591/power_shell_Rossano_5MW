# Calcoli

- `dimensionamento_5mw.py`: bilancio elettrico e termico, PUE, portate, masse, baricentro, ingombri e verifica di rimorchio per le configurazioni A, B, C e i casi di raffreddamento K1, K2, K3. Genera `risultati.md` e i disegni SVG in `mechanical/`.
- Uso: `python3 calcs/dimensionamento_5mw.py` (Python 3, solo libreria standard).
- Le ipotesi sono tutte in testa allo script, con la fonte.
- `general_compute_loi.py`: applica i rack della LOI General Compute (B300, Cerebras, d-Matrix, SN50, Positron) alla stessa disposizione a pod e scompone la massa sul ponte. Genera `risultati-general-compute.md`. Uso: `python3 calcs/general_compute_loi.py`.
