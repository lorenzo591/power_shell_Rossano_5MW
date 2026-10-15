"""Pre-dimensionamento di una TLP per la powered shell al largo di Rossano.

Livello: studio di fattibilità con regole empiriche, non progetto. Ogni ipotesi
è segnata qui sotto; i dati meteomarini del sito sono stime da sostituire con
uno studio dedicato. Scrive calcs/risultati-tlp.md.

Metodo:
1. Ponte da 50 × 50 m: quante file e colonne di container 40' HC su 2 piani,
   quanti pod e quindi quanta potenza IT (rack classe NVL72, poi classe Rubin).
2. Massa del topside: masse del modello dei pod (dimensionamento_5mw.py) più
   ponte, sottostazione, gru, contingenza.
3. Scafo: dislocamento = topside + scafo + pretensione dei tendini + zavorra,
   con le frazioni tipiche delle mini-TLP.
4. Tendini: sezione d'acciaio per resistenza (tensione di tempesta) e per il
   periodo di sussulto (heave) sotto 3,5 s; massa dei tendini al variare della
   profondità (450-2000 m).
5. Franco sotto il ponte (air gap) con l'onda centenaria stimata.
"""

from __future__ import annotations

import math
from pathlib import Path

import dimensionamento_5mw as d

ROOT = Path(__file__).resolve().parent.parent
F = d.fmt
G = 9.81
RHO_SW = 1.025  # t/m³

# --- 1. Ponte e potenza ------------------------------------------------------
DECK = 50.0  # m, lato massimo indicato dal cliente (2026-10-15)
STRIP_MIN = 20.0  # m, fascia per sottostazione AT/MT, gru, pompe di mare, approdo (ipotesi)
RACKS_PER_POD = 9  # come config A (limite di potenza e massa per pod)
PODS_PER_SERVICE = 4  # una colonna servizi (skid HX + MT/controllo) ogni 4 pod, come la config A
RACK_CLASSES = {"NVL72 (140 kW)": 140.0, "Rubin (200 kW)": 200.0}

# --- 2. Masse del topside (t) ----------------------------------------------------
DECK_STEEL_T_M2 = 0.6     # t/m², ponte principale a graticcio con travi per moduli (ipotesi n.v.)
HV_SUBSTATION_T = 300.0   # t, 2 trasformatori AT/MT, quadri GIS/MT, edificio (ipotesi n.v.)
CRANE_SAFETY_T = 200.0    # t, gru, scialuppe/zattere, antincendio, approdo (ipotesi n.v.)
CONTINGENCY = 1.15        # margine di stima sul topside

# --- 3. Scafo -------------------------------------------------------------------
HULL_FRAC = 0.25        # acciaio dello scafo / dislocamento (mini-TLP 0,2-0,3)
PRETENSION_FRAC = 0.25  # pretensione dei tendini / dislocamento (0,2-0,3)
BALLAST_FRAC = 0.05     # zavorra e carichi variabili / dislocamento
N_COL = 4
COL_DRAFT = 26.0        # m, immersione delle colonne (ipotesi)
PONTOON_H, PONTOON_W = 7.0, 7.0  # m, sezione dei pontoni

# --- 4. Tendini -----------------------------------------------------------------
N_TENDON = 8            # 2 per colonna
E_STEEL = 2.07e8        # kN/m²
SIGMA_ALLOW = 0.6 * 485e3  # kN/m², 60 % dello snervamento X70
STORM_FACTOR = 2.2      # tensione massima di tempesta / pretensione (ipotesi)
HEAVE_T_MAX = 3.5       # s, periodo di sussulto massimo (lontano dall'energia delle onde)
ADDED_MASS_HEAVE = 0.25  # massa aggiunta in heave / dislocamento (ipotesi)
DEPTHS = [450.0, 1000.0, 1500.0, 2000.0]

# --- 5. Meteomare (stime per lo Ionio settentrionale, n.v.) ------------------------
HS_100 = 8.5            # m, onda significativa centenaria (da studio meteomarino)
TP_100 = 12.0           # s
CREST_FACTOR = 0.6      # cresta / altezza massima (onda non lineare)
SURGE_TIDE = 0.6        # m, marea + sovralzo
RUNUP = 1.5             # m, amplificazione dell'onda sulle colonne
AIR_GAP_MARGIN = 1.5    # m
OFFSET_FRAC = 0.07      # spostamento orizzontale in tempesta / profondità (TLP 5-10 %)


def deck_capacity(kw_rack: float) -> list[dict]:
    """Varianti di disposizione sul ponte 50 × 50 m."""
    out = []
    pitch = d.C40["W"] + d.GANGWAY
    cols_per_row = int((DECK - 2 * d.EDGE + d.GANGWAY) // pitch)
    for rows in (2, 3):
        length = rows * d.C40["L"] + (rows + 1) * d.END_ACCESS
        strip = DECK - length
        cols = rows * cols_per_row
        n_serv = math.ceil(cols / (PODS_PER_SERVICE + 1))
        pods = cols - n_serv
        while math.ceil(pods / PODS_PER_SERVICE) > n_serv:
            pods -= 1
        p_mw = pods * RACKS_PER_POD * kw_rack / 1000
        out.append(dict(rows=rows, cols=cols, pods=pods, serv=n_serv, strip=strip,
                        p_mw=p_mw, ok_strip=strip >= STRIP_MIN))
    return out


def topside_mass(pods: int) -> dict:
    cfg = d.CONFIGS["A"]
    n_serv = math.ceil(pods / PODS_PER_SERVICE)
    m = d.masses(cfg, dict(n_pods=pods))
    # la funzione conta una sola colonna servizi: si aggiungono le altre
    extra_serv = (n_serv - 1) * (m["hx_skid"] + m["mv_ctrl"])
    modules = m["total"] + extra_serv
    deck = DECK * DECK * DECK_STEEL_T_M2
    total = (modules + deck + HV_SUBSTATION_T + CRANE_SAFETY_T) * CONTINGENCY
    return dict(modules=modules, deck=deck, hv=HV_SUBSTATION_T, crane=CRANE_SAFETY_T,
                total=total)


def hull(w_top: float) -> dict:
    disp = w_top / (1 - HULL_FRAC - PRETENSION_FRAC - BALLAST_FRAC)
    vol = disp / RHO_SW
    spacing = DECK - 12.0  # interasse delle colonne sotto il ponte (ipotesi)
    v_pont = N_COL * (spacing - 0) * PONTOON_H * PONTOON_W * 0.85
    v_cols = vol - v_pont
    dcol = math.sqrt(v_cols / (N_COL * COL_DRAFT) * 4 / math.pi)
    return dict(disp=disp, hull=HULL_FRAC * disp, pret=PRETENSION_FRAC * disp,
                spacing=spacing, dcol=dcol)


GM_MIN = 2.0         # m, altezza metacentrica minima all'installazione, prima del tiro dei tendini
TOPSIDE_ZG_ABOVE_DECK = 4.0  # m, baricentro del topside sopra l'intradosso del ponte (container su 2 piani + ponte)


def free_float_gm(w_top: float, h: dict, air_gap: float, dcol: float) -> dict:
    """Stabilità all'installazione: scafo zavorrato fino all'immersione di esercizio, tendini
    non ancora in tiro. La pretensione è sostituita da acqua di zavorra sul fondo (fase critica)."""
    mass = h["disp"]
    vol = mass / RHO_SW
    a_col = math.pi * dcol ** 2 / 4
    v_pont = N_COL * h["spacing"] * PONTOON_H * PONTOON_W * 0.85
    draft = PONTOON_H + (vol - v_pont) / (N_COL * a_col)
    kb = (v_pont * PONTOON_H / 2 + (vol - v_pont) * (PONTOON_H + draft) / 2) / vol
    i_wp = N_COL * (math.pi * dcol ** 4 / 64 + a_col * (h["spacing"] / 2) ** 2)
    bm = i_wp / vol
    # baricentri: scafo a metà dell'altezza delle colonne in esercizio, zavorra sul fondo, topside sopra il ponte
    z_deck = COL_DRAFT + air_gap
    ballast = (BALLAST_FRAC + PRETENSION_FRAC) * h["disp"]
    kg = (h["hull"] * 0.45 * z_deck + ballast * 1.5
          + w_top * (z_deck + TOPSIDE_ZG_ABOVE_DECK)) / mass
    return dict(draft=draft, kb=kb, bm=bm, kg=kg, gm=kb + bm - kg)


def column_for_stability(w_top: float, h: dict, air_gap: float) -> tuple[float, dict]:
    dcol = 4.0
    while dcol < 30:
        r = free_float_gm(w_top, h, air_gap, dcol)
        if r["gm"] >= GM_MIN:
            return dcol, r
        dcol += 0.1
    return dcol, r


OP_DRAFT = 22.0  # m, immersione di esercizio scelta (pontoni ben sotto le onde)


def hull_by_stability(w_top: float, air_gap: float, spacing: float) -> dict:
    """Scafo con colonne dimensionate per GM ≥ GM_MIN all'installazione, immersione OP_DRAFT.
    La spinta in eccesso diventa pretensione dei tendini."""
    v_pont = N_COL * spacing * PONTOON_H * PONTOON_W * 0.85
    z_deck = OP_DRAFT + air_gap
    dcol = 6.0
    while dcol < 30:
        a_col = math.pi * dcol ** 2 / 4
        vol = v_pont + N_COL * a_col * (OP_DRAFT - PONTOON_H)
        disp = vol * RHO_SW
        steel = HULL_FRAC * disp
        pret = disp - w_top - steel - BALLAST_FRAC * disp
        kb = (v_pont * PONTOON_H / 2 + (vol - v_pont) * (PONTOON_H + OP_DRAFT) / 2) / vol
        bm = N_COL * (math.pi * dcol ** 4 / 64 + a_col * (spacing / 2) ** 2) / vol
        ballast = disp - w_top - steel  # all'installazione: pretensione sostituita da zavorra
        kg = (steel * 0.45 * z_deck + ballast * 1.5 + w_top * (z_deck + TOPSIDE_ZG_ABOVE_DECK)) / disp
        gm = kb + bm - kg
        if gm >= GM_MIN and pret > 0:
            break
        dcol += 0.1
    return dict(dcol=dcol, disp=disp, hull=steel, pret=pret, gm=gm, pret_frac=pret / disp)


def tendons(disp: float, pret: float, depth: float) -> dict:
    t_max = pret * G / N_TENDON * STORM_FACTOR  # kN per tendine
    a_str = t_max / SIGMA_ALLOW
    m_heave = disp * (1 + ADDED_MASS_HEAVE) * 1000  # kg
    k_req = m_heave * (2 * math.pi / HEAVE_T_MAX) ** 2  # N/m
    a_heave = k_req * depth / (N_TENDON * E_STEEL * 1000)
    a = max(a_str, a_heave)
    mass = a * 7.85 * depth * N_TENDON  # t
    k = N_TENDON * E_STEEL * 1000 * a / depth
    t_heave = 2 * math.pi * math.sqrt(m_heave / k)
    wet = mass * (1 - RHO_SW / 7.85)  # peso in acqua dei tendini (t), da portare con la spinta
    return dict(wet=wet, wet_ratio=wet / pret, t_max=t_max, a=a, governs="periodo" if a_heave > a_str else "resistenza",
                mass=mass, t_heave=t_heave, offset=OFFSET_FRAC * depth,
                setdown=depth - math.sqrt(depth ** 2 - (OFFSET_FRAC * depth) ** 2))


def main() -> None:
    L = ["# Pre-dimensionamento TLP al largo di Rossano (generato)\n",
         "> Generato da `calcs/tlp_predesign.py`. Studio di fattibilità con regole empiriche: "
         "tutti i valori sono ipotesi n.v., i dati meteomarini sono stime da sostituire con lo studio di sito.\n"]

    L.append("## 1. Potenza massima sul ponte 50 × 50 m (container 40' HC su 2 piani)\n")
    L.append("| Rack | File di container | Colonne | Pod IT | Colonne servizi | Fascia libera per AT/MT, gru, pompe (m) | Potenza IT (MW) |")
    L.append("|---|---|---|---|---|---|---|")
    cases = []
    for name, kw in RACK_CLASSES.items():
        for v in deck_capacity(kw):
            flag = "" if v["ok_strip"] else " (fascia stretta)"
            L.append(f"| {name} | {v['rows']} | {v['cols']} | {v['pods']} | {v['serv']} | "
                     f"{F(v['strip'], 1)}{flag} | **{F(v['p_mw'], 1)}** |")
            if kw == 140.0:
                cases.append((v["rows"], v["pods"], v["p_mw"]))
    L.append("")

    sd450 = 450.0 - math.sqrt(450.0 ** 2 - (OFFSET_FRAC * 450.0) ** 2)
    air_gap = CREST_FACTOR * 1.86 * HS_100 + SURGE_TIDE + RUNUP + AIR_GAP_MARGIN + sd450
    L.append("## 2. Topside, scafo e tendini (rack NVL72)\n")
    hdr = "| Grandezza | " + " | ".join(f"{r} file, {F(p, 1)} MW" for r, _, p in cases) + " |"
    L.append(hdr)
    L.append("|---|" + "---|" * len(cases))
    tops = [topside_mass(pods) for _, pods, _ in cases]
    hulls0 = [hull(t["total"]) for t in tops]
    hulls = [hull_by_stability(t["total"], air_gap, h0["spacing"]) for t, h0 in zip(tops, hulls0)]
    rows = [
        ("Moduli IT, potenza e servizi (t)", [t["modules"] for t in tops], 0),
        ("Ponte in acciaio 50 × 50 (t)", [t["deck"] for t in tops], 0),
        ("Sottostazione AT/MT (t)", [t["hv"] for t in tops], 0),
        ("Gru, salvataggio, antincendio (t)", [t["crane"] for t in tops], 0),
        (f"**Topside con contingenza {F((CONTINGENCY - 1) * 100)} % (t)**", [t["total"] for t in tops], 0),
        ("Dislocamento minimo per il solo galleggiamento (t)", [h["disp"] for h in hulls0], 0),
        ("Colonne del solo galleggiamento: GM all'installazione (m)",
         [free_float_gm(t["total"], h, air_gap, h["dcol"])["gm"] for t, h in zip(tops, hulls0)], 1),
        (f"**Diametro delle 4 colonne per GM ≥ {F(GM_MIN)} m all'installazione (m)**", [h["dcol"] for h in hulls], 1),
        (f"Interasse delle colonne (m)", [h0["spacing"] for h0 in hulls0], 0),
        (f"**Dislocamento a {F(OP_DRAFT)} m di immersione (t)**", [h["disp"] for h in hulls], 0),
        ("Acciaio dello scafo (t)", [h["hull"] for h in hulls], 0),
        ("Pretensione totale dei tendini (t)", [h["pret"] for h in hulls], 0),
        ("Pretensione / dislocamento", [h["pret_frac"] for h in hulls], 2),
        ("Massa per MW IT, scafo + topside (t/MW)",
         [(t["total"] + h["hull"]) / c[2] for t, h, c in zip(tops, hulls, cases)], 0),
    ]
    for name, vals, dd in rows:
        L.append(f"| {name} | " + " | ".join(F(v, dd) for v in vals) + " |")
    L.append("")

    L.append("## 3. Tendini al variare della profondità\n")
    for (r, pods, p), h in zip(cases, hulls):
        L.append(f"**{r} file, {F(p, 1)} MW** (dislocamento {F(h['disp'])} t, "
                 f"{N_TENDON} tendini, tensione di tempesta {F(STORM_FACTOR, 1)} × pretensione)\n")
        L.append("| Profondità (m) | Tensione max per tendine (MN) | Sezione d'acciaio (cm²) | Governa | "
                 "Massa tendini (t) | Peso in acqua / pretensione | Periodo di sussulto (s) | Spostamento in tempesta (m) | Abbassamento (m) |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for z in DEPTHS:
            t = tendons(h["disp"], h["pret"], z)
            L.append(f"| {F(z)} | {F(t['t_max'] / 1000, 1)} | {F(t['a'] * 1e4)} | {t['governs']} | "
                     f"{F(t['mass'])} | {F(t['wet_ratio'] * 100)} % | {F(t['t_heave'], 1)} | {F(t['offset'])} | {F(t['setdown'], 1)} |")
        L.append("")

    hmax = 1.86 * HS_100
    crest = CREST_FACTOR * hmax
    sd = tendons(hulls[0]["disp"], hulls[0]["pret"], 450.0)["setdown"]
    air = crest + SURGE_TIDE + RUNUP + AIR_GAP_MARGIN + sd
    L.append("## 4. Franco sotto il ponte (onda centenaria stimata)\n")
    L.append("| Grandezza | Valore |")
    L.append("|---|---|")
    L.append(f"| Hs centenaria (m), stima n.v. | {F(HS_100, 1)} |")
    L.append(f"| Tp (s), stima n.v. | {F(TP_100, 1)} |")
    L.append(f"| Onda massima Hmax = 1,86 Hs (m) | {F(hmax, 1)} |")
    L.append(f"| Cresta sul medio mare (m) | {F(crest, 1)} |")
    L.append(f"| + marea e sovralzo, risalita sulle colonne, margine, abbassamento a 450 m (m) | "
             f"{F(SURGE_TIDE + RUNUP + AIR_GAP_MARGIN + sd, 1)} |")
    L.append(f"| **Intradosso del ponte sul medio mare (m)** | **{F(air, 1)}** |")
    L.append("")
    out = ROOT / "calcs" / "risultati-tlp.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
