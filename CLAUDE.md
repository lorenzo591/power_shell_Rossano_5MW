# CLAUDE.md

## Regola fondamentale: mai lavorare su `main`

- Non fare mai commit né push direttamente su `main`. Ogni modifica va su un branch dedicato e si integra con una pull request.

## Contesto del progetto

Powered shell da **5 MW IT** su una TLP (ponte circa 30 × 30 m; sito da confermare: i dati ereditati sono della TLP pilota di Napoli, il nome del repo indica Rossano): container ISO 40' HC impilati, raffreddamento a cold plate con cessione al mare, alimentazione MT da terra. Deriva da `lorenzo591/powered_shell_container` e `lorenzo591/powered_shell_schneider-vertiv` ([`fonti-dai-repository.md`](fonti-dai-repository.md)).

## Struttura

| Cartella | Contenuto |
|---|---|
| `requirements/` | Requisiti con ID (`REQ-IT`, `REQ-PWR`, `REQ-ENV`, `REQ-MEC`) |
| `configurazioni/` | Confronto delle configurazioni e scelta |
| `calcs/` | Script di dimensionamento e risultati generati |
| `electrical/`, `cooling/`, `mechanical/` | Dimensionamento per disciplina |
| `decisions/` | ADR |
| `bom/` | Distinta dei componenti (nessun costo in questa fase) |

## Convenzioni

- I numeri vengono da `calcs/dimensionamento_5mw.py`: si cambiano le ipotesi nello script, si rigenera `calcs/risultati.md` e si aggiornano i documenti che li citano.
- Ogni calcolo riporta ipotesi, dati di ingresso (con l'ID del requisito), norma, risultato, revisione. Unità SI.
- Non inventare dati di componenti: se un valore non viene da un datasheet o dal cliente, segnarlo come ipotesi (n.v.).
- I dati ereditati dalla TLP del pilota (moti, quote, frequenze) sono da riconfermare per la TLP da 5 MW.
