"""Opzioni rack della LOI General Compute applicate alla powered shell da 5 MW IT.

Riusa le funzioni di dimensionamento_5mw.py (stessa disposizione a pod 40' HC su
2 piani, 16 rack per container IT, colonna servizi) cambiando solo il rack.
Scrive calcs/risultati-general-compute.md.

Fonti dei dati dei rack: schede prodotto su https://www.generalcompute.com/
(consultato 2026-10-15). Masse dei rack e potenza del rack d-Matrix: ipotesi n.v.
"""

from __future__ import annotations

import math
from pathlib import Path

import dimensionamento_5mw as d

ROOT = Path(__file__).resolve().parent.parent
F = d.fmt
RACKS_PER_IT = 16  # limite di lunghezza del 40' HC con rack da 600 mm (come config B)

# nome, kW/rack, massa rack (t, ipotesi n.v.), quota di calore al liquido, nota
OPTIONS = [
    ("NVIDIA HGX B300 DLC, 4 server", 56.0, 0.75, 0.95,
     "~14 kW per server (GC). Coincide con la config B"),
    ("NVIDIA HGX B300 DLC, 2 server", 28.0, 0.45, 0.95,
     "Rack da 28 kW usato nel calcolatore TCO di GC"),
    ("Cerebras CS-3, 2 sistemi", 46.0, 1.00, 0.90,
     "23 kW per sistema (GC); circa 90 % all'acqua di impianto (flopper.io, n.v.)"),
    ("d-Matrix Corsair SquadRack", 45.0, 0.90, 0.0,
     "64 schede × 600 W (GC) + 8 host: 45 kW stima n.v. Solo aria"),
    ("SambaNova SN50 SambaRack", 20.0, 0.80, 0.0,
     "20 kW medi per rack (GC), picco non pubblicato. Solo aria"),
    ("Positron Atlas, 10 server", 20.0, 0.80, 0.0,
     "2 kW per server 4U (GC); 10 server = 40U. Solo aria"),
    ("Positron Atlas, 6 server", 12.0, 0.60, 0.0,
     "Rack mostrato da GC (6 server). Solo aria"),
]

DECK_SIDE = 30.0  # m, ponte TLP circa 30 × 30


def option_case(kw: float, rack_t: float, liq: float) -> dict:
    cfg = dict(d.CONFIGS["B"], rack_kw=kw, rack_t=rack_t, liq_frac=liq,
               racks_per_it=RACKS_PER_IT)
    n_racks = math.ceil(d.P_IT_TARGET / kw)
    n_pods = math.ceil(n_racks / RACKS_PER_IT)
    m = d.masses(cfg, dict(n_pods=n_pods))
    cols = n_pods + 1
    w1 = cols * d.C40["W"] + (cols - 1) * d.GANGWAY + 2 * d.EDGE
    l1 = d.C40["L"] + 2 * d.END_ACCESS
    c2 = math.ceil(cols / 2)
    w2 = c2 * d.C40["W"] + (c2 - 1) * d.GANGWAY + 2 * d.EDGE
    l2 = 2 * d.C40["L"] + 3 * d.END_ACCESS
    fits1 = w1 <= DECK_SIDE and l1 <= DECK_SIDE
    fits2 = w2 <= DECK_SIDE and l2 <= DECK_SIDE
    if fits1:
        lay, area = f"1 fila, {F(w1, 1)} × {F(l1, 1)} m", w1 * l1
    elif fits2:
        lay, area = f"2 file, {F(w2, 1)} × {F(l2, 1)} m", w2 * l2
    else:
        lay, area = f"non sta: 1 fila {F(w1, 1)} m, 2 file {F(w2, 1)} m", min(w1 * l1, w2 * l2)
    rack_mass = n_pods * RACKS_PER_IT * rack_t
    rdhx = n_pods * RACKS_PER_IT * d.IT_FIXED_T["rdhx_per_rack"]
    it_shell = m["it"] - RACKS_PER_IT * (rack_t + d.IT_FIXED_T["rdhx_per_rack"])
    return dict(n_racks=n_racks, n_pods=n_pods, n_cont=2 * n_pods + 2, m=m,
                rack_mass=rack_mass, rdhx=rdhx, it_shell_tot=n_pods * it_shell,
                lower_tot=n_pods * m["lower"], layout=lay, fits=fits1 or fits2,
                area=area, q_air_rack=kw * (1 - liq))


def main() -> None:
    a = d.CONFIGS["A"]
    ref = d.masses(a, dict(n_pods=math.ceil(math.ceil(d.P_IT_TARGET / a["rack_kw"]) / a["racks_per_it"])))
    res = [(o, option_case(o[1], o[2], o[3])) for o in OPTIONS]

    L = []
    L.append("# Opzioni della LOI General Compute sul ponte da 5 MW (generato)\n")
    L.append("> Generato da `calcs/general_compute_loi.py`, che riusa le funzioni di "
             "`dimensionamento_5mw.py`. Non modificare a mano. Ipotesi di concept: masse dei "
             "rack e potenza d-Matrix n.v.; trasformatori da 1250 kVA per pod in tutti i casi "
             "(cautelativo per i pod a bassa potenza).\n")

    L.append("## 1. Rack, container, ingombro\n")
    L.append("| Opzione | kW/rack | Rack | Pod | Container 40' HC | Disposizione sul ponte 30 × 30 | IT su ingombro (kW/m²) | Calore all'aria per rack (kW) | Nota |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for o, r in res:
        L.append(f"| {o[0]} | {F(o[1], 0)} | {r['n_racks']} | {r['n_pods']} | {r['n_cont']} | "
                 f"{r['layout']} | {F(d.P_IT_TARGET / r['area'], 1)} | {F(r['q_air_rack'], 1)} | {o[4]} |")
    L.append("")

    L.append("## 2. Massa sul ponte scomposta (t)\n")
    hdr = ["Voce"] + [o[0] for o, _ in res] + ["Rif. config A (140 kW)"]
    L.append("| " + " | ".join(hdr) + " |")
    L.append("|" + "---|" * len(hdr))
    n_a_pods = math.ceil(math.ceil(d.P_IT_TARGET / a["rack_kw"]) / a["racks_per_it"])
    ref_rack = n_a_pods * a["racks_per_it"] * a["rack_t"]
    ref_rdhx = n_a_pods * a["racks_per_it"] * d.IT_FIXED_T["rdhx_per_rack"]
    rows = [
        ("Rack IT (pieni)", lambda r: r["rack_mass"], ref_rack),
        ("Porte posteriori RDHx", lambda r: r["rdhx"], ref_rdhx),
        ("Container IT: involucro, blindosbarre, tubi TCS, antincendio, ancoraggi",
         lambda r: r["it_shell_tot"], n_a_pods * ref["it"] - ref_rack - ref_rdhx),
        ("Container inferiori: trasformatori, quadri BT, CDU", lambda r: r["lower_tot"],
         n_a_pods * ref["lower"]),
        ("Skid scambiatori e pompe FWS", lambda r: r["m"]["hx_skid"], ref["hx_skid"]),
        ("Container MT e controllo", lambda r: r["m"]["mv_ctrl"], ref["mv_ctrl"]),
        ("Telaio con guide cellulari, passerelle", lambda r: r["m"]["frame"], ref["frame"]),
        ("Tubazioni e cavi tra i container", lambda r: r["m"]["pipes_cables"], ref["pipes_cables"]),
        ("Pompe di mare e colonne di presa", lambda r: r["m"]["sea_pumps"], ref["sea_pumps"]),
    ]
    for name, f, rv in rows:
        L.append(f"| {name} | " + " | ".join(f"{F(f(r), 0)}" for _, r in res) + f" | {F(rv, 0)} |")
    L.append("| **Totale sul ponte** | " + " | ".join(f"**{F(r['m']['total'], 0)}**" for _, r in res)
             + f" | **{F(ref['total'], 0)}** |")
    L.append("| Rapporto con la config A | " + " | ".join(f"{F(r['m']['total'] / ref['total'], 1)}×" for _, r in res)
             + " | 1,0× |")
    L.append("| Massa per kW IT (kg/kW) | " + " | ".join(f"{F(1000 * r['m']['total'] / d.P_IT_TARGET, 0)}" for _, r in res)
             + f" | {F(1000 * ref['total'] / d.P_IT_TARGET, 0)} |")
    L.append("| Container IT pieno (t, max ISO 30,48) | " + " | ".join(f"{F(r['m']['it'], 1)}" for _, r in res)
             + f" | {F(ref['it'], 1)} |")
    L.append("| Baricentro sopra il ponte (m) | " + " | ".join(f"{F(r['m']['zg'], 2)}" for _, r in res)
             + f" | {F(ref['zg'], 2)} |")
    L.append("")
    out = ROOT / "calcs" / "risultati-general-compute.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
