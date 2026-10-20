"""TLP minima per la powered shell da 5 MW al largo di Rossano (fondale 450 m).

Verifica analitica di primo livello, sulla traccia di API RP 2T / DNV-OS-C105:
 1. topside della config A (4 pod + 1 colonna servizi, 2 piani) su un ponte minimo;
 2. scafo a 4 colonne con pontoni ad anello; ricerca della geometria di dislocamento
    minimo che rispetta tutte le verifiche;
 3. per la geometria scelta: bilancio dei pesi, stabilità all'installazione, periodi
    propri, onda di progetto (Airy, Morison su colonne e pontoni, fasi reali sugli elementi,
    due incidenze), vento, corrente, offset e abbassamento, tensioni dei tendini massima e
    minima, resistenza e collasso dei tendini, franco sotto il ponte, palo di fondazione.

Non sostituisce l'analisi idrodinamica (diffrazione, onda irregolare, deriva lenta,
ringing/springing, fatica, sisma): quelle restano per il progetto di base.
Scrive calcs/risultati-tlp-5mw.md.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import dimensionamento_5mw as d

ROOT = Path(__file__).resolve().parent.parent
F = d.fmt
G = 9.81
RHO = 1025.0      # kg/m³ acqua di mare
RHO_AIR = 1.225   # kg/m³
E = 2.07e11       # Pa
FY = 448e6        # Pa, X65 (API 5L) per i tendini
NU = 0.3

# ---------------------------------------------------------------------------
# Sito (fonti in mechanical/tlp-5mw-rossano.md)
# ---------------------------------------------------------------------------
DEPTH = 450.0
HS_100 = 8.2       # m, boa RON di Crotone, valore alto delle stime pubblicate (7,2-8,2 m)
TP_100 = 12.0      # s, ipotesi n.v.
H_DES = 1.86 * HS_100       # onda di progetto (Hmax, 3 ore)
T_DES = [10.5, 11.5, 12.5]  # s, periodi esplorati per l'onda di progetto
U_WIND = 32.0      # m/s, vento a 10 m, media 1 min, centenario (ipotesi n.v.)
U_CUR = 1.0        # m/s, corrente di superficie centenaria (ipotesi n.v.)
TIDE_SURGE = 0.5   # m, marea astronomica + sovralzo (Ionio: marea < 0,3 m)

# ---------------------------------------------------------------------------
# Topside
# ---------------------------------------------------------------------------
LAYOUT_W = 19.0    # m, 5 colonne di container (config A, calcs/risultati.md §5)
LAYOUT_L = 15.2    # m, lunghezza del 40' + accessi
DECK_MIN = (24.0, 22.0)   # m, ponte minimo: container + fascia per gru, approdo, arrivo cavi
DECK_STEEL = 0.75  # t/m², ponte a graticcio a un livello con travi per moduli (ipotesi n.v.)
CRANE_T = 35.0     # t, gru di piattaforma
SAFETY_T = 45.0    # t, zattere, approdo, scale, antincendio, telecom
DECK_DEPTH = 3.0   # m, altezza della struttura del ponte
CONT = 1.15        # contingenza sul topside
H_STACK = 2 * 2.896 + 0.6   # m, 2 piani di container + tettoia

# ---------------------------------------------------------------------------
# Scafo
# ---------------------------------------------------------------------------
SHELL_T_M2 = 0.32  # t/m² di superficie bagnata/esterna, compresi rinforzi e paratie (≈ 41 mm equivalenti, n.v.)
CM_COL, CA_COL = 2.0, 1.0    # Morison colonne (D/L < 0,2)
CM_PON_H, CA_PON_H = 2.2, 1.2  # pontone rettangolare, moto orizzontale
CM_PON_V, CA_PON_V = 2.4, 1.4  # pontone rettangolare, moto verticale
CD_COL, CD_PON = 0.7, 1.5
CS_WIND = 1.1      # coefficiente di forma medio del topside
GM_MIN = 1.0       # m, stabilità all'installazione (DNV-OS-C301, unità a colonne)

# ---------------------------------------------------------------------------
# Tendini
# ---------------------------------------------------------------------------
N_T = 8                  # 2 per colonna
SF_TENS = 0.6            # tensione massima ≤ 0,6 Fy (condizione estrema, API RP 2T)
SF_COLLAPSE = 1.5        # margine sul collasso idrostatico
T_MIN_FRAC = 0.10        # tensione minima ≥ 10 % della pretensione (nessun allentamento)
WAVE_EXTRA = 1.15        # +15 % sulla parte d'onda per effetti del 2° ordine e ringing (n.v.)
OFFSET_MAX = 0.08        # spostamento ≤ 8 % del fondale
T_HEAVE_MAX = 3.5        # s
HS_ROBUST = 9.0          # m, verifica di robustezza: Hs +10 % sopra il valore di progetto


def topside(deck_l: float, deck_w: float) -> dict:
    cfg = d.CONFIGS["A"]
    m = d.masses(cfg, dict(n_pods=4))
    # il modello dei pod conta anche pompe e colonne di mare (8 t) e un telaio per un ponte
    # 30 × 30; qui il ponte è a parte: si tolgono il telaio e si tengono le altre voci
    modules = m["total"] - m["frame"]
    deck = deck_l * deck_w * DECK_STEEL
    total = (modules + deck + CRANE_T + SAFETY_T) * CONT
    return dict(modules=modules, deck=deck, crane=CRANE_T, safety=SAFETY_T, total=total)


def wave_number(T: float, h: float = DEPTH) -> float:
    w = 2 * math.pi / T
    k = w * w / G
    for _ in range(50):
        k = w * w / (G * math.tanh(k * h))
    return k


class Hull:
    def __init__(self, s, D, T, b, hp, air, w_top, deck_l, deck_w):
        self.s, self.D, self.T, self.b, self.hp = s, D, T, b, hp
        self.air, self.w_top, self.deck_l, self.deck_w = air, w_top, deck_l, deck_w
        self.a_col = math.pi * D * D / 4
        self.l_pon = s - D          # tratto libero di ogni pontone tra le colonne
        self.v_col = 4 * self.a_col * T
        self.v_pon = 4 * self.l_pon * b * hp
        self.vol = self.v_col + self.v_pon
        self.disp = self.vol * RHO / 1000  # t
        # acciaio dello scafo da superficie esterna
        h_col = T + air
        a_col_sh = 4 * (math.pi * D * h_col + 2 * self.a_col)
        a_pon_sh = 4 * self.l_pon * 2 * (b + hp)
        self.steel = SHELL_T_M2 * (a_col_sh + a_pon_sh)
        self.awp = 4 * self.a_col
        # posizioni (x, y) delle colonne e dei tendini (2 per colonna, sul lato esterno)
        h = s / 2
        self.cols = [(-h, -h), (h, -h), (h, h), (-h, h)]
        # 2 tendini per colonna, sui supporti esterni (porch) lungo la diagonale, a ±1,5 m
        r_p = 0.35 * D + 0.8
        self.tendons = [(cx + math.copysign(r_p, cx) + k * 1.5 * math.copysign(1, cy),
                         cy + math.copysign(r_p, cy) - k * 1.5 * math.copysign(1, cx))
                        for cx, cy in self.cols for k in (-1, 1)]

    # --- masse e baricentri (z dal fondo dello scafo, keel) ---
    def mass_items(self, ballast: float) -> list[tuple[float, float]]:
        z_deck = self.T + self.air
        return [(self.w_top, z_deck + DECK_DEPTH / 2 + 0.55 * H_STACK * 0.6),
                (self.steel, 0.42 * (self.T + self.air)),
                (ballast, self.hp * 0.4)]


def evaluate(s, D, T, b, hp, w_top_fn, air) -> dict | None:
    deck_l = max(DECK_MIN[0], s + D)
    deck_w = max(DECK_MIN[1], s + D)
    top = w_top_fn(deck_l, deck_w)
    H = Hull(s, D, T, b, hp, air, top["total"], deck_l, deck_w)
    if H.l_pon < 2:
        return None
    ballast_op = 0.03 * H.disp  # zavorra fissa di assetto
    pret = H.disp - top["total"] - H.steel - ballast_op   # t, tiro totale in testa ai tendini
    if pret <= 0:
        return None
    r = dict(H=H, top=top, pret=pret, ballast=ballast_op)

    # --- stabilità all'installazione: tendini non in tiro, pretensione sostituita da zavorra ---
    ballast_inst = ballast_op + pret
    items = H.mass_items(ballast_inst)
    m_tot = sum(m for m, _ in items)
    kg = sum(m * z for m, z in items) / m_tot
    v_pon_tot = H.v_pon
    kb = (v_pon_tot * hp / 2 + H.v_col * T / 2) / H.vol
    i_wp = 4 * (math.pi * D ** 4 / 64 + H.a_col * (s / 2) ** 2)
    bm = i_wp / H.vol
    r["gm_inst"] = kb + bm - kg
    # alternativa: scafo senza topside (topside sollevato in mare dopo il tiro dei tendini)
    items_h = [(H.steel, 0.42 * (T + air)), (H.disp - H.steel, hp * 0.4)]
    kg_h = sum(m * z for m, z in items_h) / H.disp
    r["gm_hull_only"] = kb + bm - kg_h
    r["kg"], r["kb"], r["bm"] = kg, kb, bm
    return r


def tendon_section(t_max: float) -> dict:
    """Tubo per resistenza (0,6 Fy) e collasso idrostatico a 450 m (API RP 2T, formula combinata)."""
    p_ext = RHO * G * DEPTH
    best = None
    for od_mm in range(406, 1220, 25):
        od = od_mm / 1000
        for t_mm in range(10, 61):
            t = t_mm / 1000
            a = math.pi * (od - t) * t
            if t_max > SF_TENS * FY * a:
                continue
            pe = 2 * E * (t / od) ** 3 / (1 - NU ** 2)
            py = 2 * FY * t / od
            pc = py * pe / math.sqrt(py ** 2 + pe ** 2)
            if pc < SF_COLLAPSE * p_ext:
                continue
            mass_m = a * 7850
            buoy_m = math.pi * od ** 2 / 4 * RHO
            wet = (mass_m - buoy_m) * G  # N/m (negativo = galleggiante)
            cand = dict(od=od, t=t, a=a, pc=pc, mass_m=mass_m, wet_m=wet)
            if best is None or mass_m < best["mass_m"]:
                best = cand
            break
    return best


def in_place(r: dict, air: float, hdes: float | None = None) -> dict:
    hdes = H_DES if hdes is None else hdes
    H = r["H"]
    s, D, T, b, hp = H.s, H.D, H.T, H.b, H.hp
    z_keel = -T
    t0 = r["pret"] * 1000 * G / N_T   # N per tendine

    # --- vento (media 1 min) sul topside e sulle colonne fuori acqua ---
    a_top = H.deck_w * (DECK_DEPTH + H_STACK)
    a_col_air = 2 * D * air  # 2 colonne esposte (le altre in scia, cautelativo)
    z_top = air + DECK_DEPTH + H_STACK / 2
    v_top = U_WIND * (z_top / 10) ** 0.11
    f_wind = 0.5 * RHO_AIR * CS_WIND * a_top * v_top ** 2 + 0.5 * RHO_AIR * 1.0 * a_col_air * U_WIND ** 2
    m_wind = 0.5 * RHO_AIR * CS_WIND * a_top * v_top ** 2 * (z_top - z_keel) \
        + 0.5 * RHO_AIR * a_col_air * U_WIND ** 2 * (air / 2 - z_keel)

    # --- corrente (profilo lineare fino a 0,3 m/s al fondo dello scafo) ---
    def u_c(z): return U_CUR * (0.3 + 0.7 * (1 + z / T))
    f_cur = m_cur = 0.0
    nz = 40
    for i in range(nz):
        z = -T + (i + 0.5) * T / nz
        dz = T / nz
        if z > -T + hp:
            fc = 0.5 * RHO * CD_COL * D * u_c(z) ** 2 * dz * 4 * 0.8  # 4 colonne, schermatura 0,8
            f_cur += fc
            m_cur += fc * (z - z_keel)
    fp = 0.5 * RHO * CD_PON * hp * u_c(-T + hp / 2) ** 2 * 2 * H.l_pon  # 2 pontoni perpendicolari
    f_cur += fp
    m_cur += fp * hp / 2

    # --- deriva media d'onda (stima: 15 % di vento + corrente, n.v.) ---
    f_drift = 0.15 * (f_wind + f_cur)
    f_mean = f_wind + f_cur + f_drift
    m_mean = m_wind + m_cur + f_drift * (0 - z_keel)

    # --- onda di progetto: Morison inerziale con fasi sugli elementi ---
    m_struct = (r["top"]["total"] + H.steel + r["ballast"]) * 1000
    worst = None
    for Tw in T_DES:
        k = wave_number(Tw)
        w = 2 * math.pi / Tw
        A = hdes / 2
        for head in (0.0, 45.0):
            th = math.radians(head)
            ux, uy = math.cos(th), math.sin(th)
            col_bottoms = []
            elems = []  # (x lungo l'onda, z, volume, Cm_h, Ca_h, Cm_v, Ca_v, orientamento)
            nz = 30
            for cx, cy in H.cols:
                xw = cx * ux + cy * uy
                for i in range(nz):
                    z = -T + (i + 0.5) * T / nz
                    v = H.a_col * T / nz
                    elems.append((xw, z, v, CM_COL, CA_COL, 0.0, 0.0))
                # pressione dinamica sul fondo della colonna (Froude-Krylov verticale), verso l'alto sotto la cresta
                col_bottoms.append(xw)
            # pontoni discretizzati
            h = s / 2
            pons = [((-h, -h), (h, -h)), ((h, -h), (h, h)), ((h, h), (-h, h)), ((-h, h), (-h, -h))]
            npn = 12
            for (x1, y1), (x2, y2) in pons:
                dx, dy = x2 - x1, y2 - y1
                L = math.hypot(dx, dy)
                # componente dell'onda perpendicolare al pontone
                nx, ny = -dy / L, dx / L
                perp = abs(nx * ux + ny * uy)
                for j in range(npn):
                    t = (j + 0.5) / npn
                    px, py = x1 + t * dx, y1 + t * dy
                    xw = px * ux + py * uy
                    v = b * hp * H.l_pon / npn
                    elems.append((xw, -T + hp / 2, v, CM_PON_H * perp, CA_PON_H * perp, CM_PON_V, CA_PON_V))
            fx = fz = 0j
            my = 0j
            ma_h = 0.0
            mom_ca = 0.0
            for xw, z, v, cmh, cah, cmv, cav in elems:
                decay = math.exp(k * z)
                ph = cmath.exp(1j * k * xw)
                ax = -1j * w * w * A * decay * ph
                az = -w * w * A * decay * ph
                dfx = RHO * cmh * v * ax
                dfz = RHO * cmv * v * az
                fx += dfx
                fz += dfz
                my += dfz * xw + dfx * (z - z_keel)
                ma_h += RHO * cah * v
                mom_ca += RHO * cah * v * (z - z_keel)
            for xw in col_bottoms:
                dfz = RHO * G * A * math.exp(-k * T) * H.a_col * cmath.exp(1j * k * xw)
                fz += dfz
                my += dfz * xw
            # moto di surge libero (rigidezza dei tendini trascurabile alla frequenza d'onda)
            acc = fx / (m_struct + ma_h)
            x1 = abs(acc) / w ** 2
            # momento d'inerzia del moto: massa strutturale e massa aggiunta che accelerano
            m_inertia = sum(m * 1000 * z for m, z in r["H"].mass_items(r["ballast"]))  # kg·m dal keel
            my_net = my - acc * (m_inertia + mom_ca)
            # ripartizione sui tendini (rigidezze uguali): ΔT_j = Fz/n + M·x_j / Σx²
            xs = [tx * ux + ty * uy for tx, ty in H.tendons]
            sx2 = sum(x * x for x in xs)
            dts = [abs(fz / N_T + my_net * x / sx2) for x in xs]
            dt_wave = max(dts) * WAVE_EXTRA
            cand = dict(Tw=Tw, head=head, fx=abs(fx), fz=abs(fz), my=abs(my_net), x1=x1,
                        dt_wave=dt_wave, xs=xs, sx2=sx2)
            if worst is None or cand["dt_wave"] > worst["dt_wave"]:
                worst = cand

    # --- offset, abbassamento, tensioni ---
    k_surge = r["pret"] * 1000 * G / DEPTH
    x_mean = f_mean / k_surge
    x_tot = x_mean + worst["x1"]
    setdown = DEPTH - math.sqrt(DEPTH ** 2 - x_tot ** 2)
    dt_setdown = RHO * G * H.awp * setdown / N_T
    dt_tide = RHO * G * H.awp * TIDE_SURGE / N_T
    xs = worst["xs"]
    dt_mean = m_mean * max(xs) / worst["sx2"]
    t_max = t0 + dt_setdown + dt_tide + dt_mean + worst["dt_wave"]
    t_min = t0 - dt_tide - dt_mean - worst["dt_wave"]

    sec = tendon_section(t_max)
    wet_tot = sec["wet_m"] * DEPTH if sec else float("nan")
    t_min_bottom = t_min - max(wet_tot, 0)

    # periodi propri
    k_t = E * sec["a"] / DEPTH if sec else 1.0
    m_heave = m_struct + RHO * CA_PON_V * H.v_pon
    t_heave = 2 * math.pi * math.sqrt(m_heave / (N_T * k_t))
    xs0 = [tx for tx, _ in H.tendons]
    i_pitch = sum(m * 1000 * (z - H.T) ** 2 for m, z in H.mass_items(r["ballast"])) + m_struct * (s / 2) ** 2 * 0.5
    t_pitch = 2 * math.pi * math.sqrt(i_pitch / (k_t * sum(x * x for x in xs0)))
    t_surge = 2 * math.pi * math.sqrt((m_struct + RHO * CA_COL * H.v_col) / k_surge)

    # franco: cresta di Stokes 2° ordine + amplificazione sulle colonne + abbassamento + marea
    kd = wave_number(min(T_DES))
    crest = hdes / 2 + kd * hdes ** 2 / 8 * 2  # cresta con correzione del 2° ordine (acqua profonda, cautelativa)
    air_req = crest * 1.10 + setdown + TIDE_SURGE + 1.5

    return dict(f_wind=f_wind, f_cur=f_cur, f_drift=f_drift, f_mean=f_mean, worst=worst,
                x_mean=x_mean, x_tot=x_tot, setdown=setdown, t0=t0, t_max=t_max, t_min=t_min,
                dt_mean=dt_mean, dt_setdown=dt_setdown, dt_tide=dt_tide, sec=sec, wet_tot=wet_tot,
                t_min_bottom=t_min_bottom, pile=1.5 * (t_max + max(-wet_tot, 0)), t_heave=t_heave, t_pitch=t_pitch, t_surge=t_surge,
                crest=crest, air_req=air_req)


def checks(r, p) -> dict:
    return {
        "Stabilità all'installazione (GM ≥ 1 m)": r["gm_inst"] >= GM_MIN,
        "Tendine: tensione minima ≥ 10 % della pretensione": p["t_min"] >= T_MIN_FRAC * p["t0"],
        "Tendine: nessun allentamento al fondo": p["t_min_bottom"] > 0,
        "Tendine: resistenza e collasso a 450 m": p["sec"] is not None,
        "Spostamento ≤ 8 % del fondale": p["x_tot"] <= OFFSET_MAX * DEPTH,
        "Periodo di sussulto ≤ 3,5 s": p["t_heave"] <= T_HEAVE_MAX,
        "Franco sotto il ponte": p["air_req"] <= r["H"].air + 1e-6,
    }


def search(install_full: bool):
    best = None
    air0 = 15.0
    for s in [x * 1.0 for x in range(18, 41)]:
        for D in [x * 0.5 for x in range(12, 29)]:
            for T in [x * 1.0 for x in range(16, 31)]:
                for b, hp in ((5.0, 5.0), (6.0, 6.0), (7.0, 7.0)):
                    if s - D < 4:
                        continue
                    r = evaluate(s, D, T, b, hp, topside, air0)
                    if r is None:
                        continue
                    if install_full and r["gm_inst"] < GM_MIN:
                        continue
                    if not install_full and r["gm_hull_only"] < GM_MIN:
                        continue
                    if r["pret"] < 0.15 * r["H"].disp:
                        continue
                    p = in_place(r, air0)
                    c = checks(r, p)
                    if not install_full:
                        c.pop("Stabilità all'installazione (GM ≥ 1 m)")
                    if not all(c.values()):
                        continue
                    q = in_place(r, air0, 1.86 * HS_ROBUST)
                    if (q["t_min"] < T_MIN_FRAC * q["t0"] or q["t_max"] > 0.8 * FY * p["sec"]["a"]
                            or q["air_req"] > air0):
                        continue
                    if best is None or r["H"].disp < best[0]["H"].disp:
                        best = (r, p, c, q)
    return best


def main() -> None:
    res = {"full": search(True), "lift": search(False)}
    L = ["# TLP minima per 5 MW al largo di Rossano (generato)\n",
         "> Generato da `calcs/tlp_5mw.py`. Verifica analitica di primo livello (API RP 2T / DNV-OS-C105): "
         "onda regolare di progetto con Morison e fasi sugli elementi, analisi quasi statica dei tendini. "
         "Dati di sito in parte stimati (n.v.). Non sostituisce l'analisi idrodinamica.\n"]
    L.append("## 0. Dati di sito usati\n")
    L.append("| Grandezza | Valore | Fonte |")
    L.append("|---|---|---|")
    L.append(f"| Fondale | {F(DEPTH)} m | Cliente |")
    L.append(f"| Hs centenaria | {F(HS_100, 1)} m | Boa RON di Crotone, stime pubblicate 7,2-8,2 m: si usa la più alta |")
    L.append(f"| Onda di progetto Hmax = 1,86 Hs | {F(H_DES, 1)} m, periodi {', '.join(F(t, 1) for t in T_DES)} s | Ipotesi n.v. sul periodo |")
    L.append(f"| Vento a 10 m, media 1 min, centenario | {F(U_WIND)} m/s | Ipotesi n.v. |")
    L.append(f"| Corrente di superficie | {F(U_CUR, 1)} m/s | Ipotesi n.v. |")
    L.append(f"| Hs per la verifica di robustezza | {F(HS_ROBUST, 1)} m | +10 % |")
    L.append(f"| Marea + sovralzo | {F(TIDE_SURGE, 1)} m | Ipotesi n.v. |")
    L.append("")
    names = {"full": "A · topside montato in banchina, rimorchio integrato",
             "lift": "B · scafo e tendini prima, topside sollevato in mare"}
    for key, sol in res.items():
        L.append(f"## {names[key]}\n")
        if sol is None:
            L.append("Nessuna geometria del campo esplorato soddisfa tutte le verifiche.\n")
            continue
        r, p, c, q = sol
        H = r["H"]
        L.append("### Geometria e pesi\n")
        L.append("| Grandezza | Valore |")
        L.append("|---|---|")
        rows = [
            ("Ponte (m)", f"{F(H.deck_l, 1)} × {F(H.deck_w, 1)}"),
            ("Intradosso del ponte sul medio mare (m)", F(H.air, 1)),
            ("Interasse delle colonne (m)", F(H.s, 1)),
            ("Diametro delle 4 colonne (m)", F(H.D, 1)),
            ("Immersione (m)", F(H.T, 1)),
            ("Pontoni (larghezza × altezza, m)", f"{F(H.b, 1)} × {F(H.hp, 1)}"),
            ("Moduli IT, potenza, servizi (t)", F(r["top"]["modules"])),
            ("Ponte in acciaio (t)", F(r["top"]["deck"])),
            ("Gru, salvataggio, approdo (t)", F(r["top"]["crane"] + r["top"]["safety"])),
            ("**Topside con contingenza 15 % (t)**", F(H.w_top)),
            ("Acciaio dello scafo (t)", F(H.steel)),
            ("Zavorra fissa (t)", F(r["ballast"])),
            ("**Dislocamento (t)**", F(H.disp)),
            ("**Pretensione totale (t)**", f"{F(r['pret'])} ({F(100 * r['pret'] / H.disp)} % del dislocamento)"),
            ("GM all'installazione con topside (m)", F(r["gm_inst"], 2)),
            ("GM dello scafo senza topside (m)", F(r["gm_hull_only"], 2)),
            ("Massa per MW IT, topside + scafo (t/MW)", F((H.w_top + H.steel) / 5.04)),
        ]
        for k_, v in rows:
            L.append(f"| {k_} | {v} |")
        L.append("")
        w = p["worst"]
        L.append("### Carichi ambientali e risposta\n")
        L.append("| Grandezza | Valore |")
        L.append("|---|---|")
        rows = [
            ("Vento sul topside e sulle colonne (kN)", F(p["f_wind"] / 1000)),
            ("Corrente (kN)", F(p["f_cur"] / 1000)),
            ("Deriva media d'onda, stima (kN)", F(p["f_drift"] / 1000)),
            (f"Onda che governa: periodo {F(w['Tw'], 1)} s, incidenza {F(w['head'])}°", ""),
            ("Forza orizzontale d'onda, ampiezza (kN)", F(w["fx"] / 1000)),
            ("Forza verticale d'onda, ampiezza (kN)", F(w["fz"] / 1000)),
            ("Momento ribaltante netto al fondo, ampiezza (MN·m)", F(w["my"] / 1e6, 1)),
            ("Spostamento medio (m)", F(p["x_mean"], 1)),
            ("Spostamento d'onda, ampiezza (m)", F(w["x1"], 1)),
            (f"**Spostamento massimo (m)** (limite {F(OFFSET_MAX * DEPTH)} m)", F(p["x_tot"], 1)),
            ("Abbassamento per lo spostamento (m)", F(p["setdown"], 2)),
            ("Periodo di sussulto (s)", F(p["t_heave"], 2)),
            ("Periodo di beccheggio (s)", F(p["t_pitch"], 2)),
            ("Periodo di surge (s)", F(p["t_surge"], 0)),
        ]
        for k_, v in rows:
            L.append(f"| {k_} | {v} |")
        L.append("")
        sec = p["sec"]
        L.append("### Tendini (8, due per colonna)\n")
        L.append("| Grandezza | Valore |")
        L.append("|---|---|")
        rows = [
            ("Pretensione per tendine (MN)", F(p["t0"] / 1e6, 2)),
            ("+ abbassamento, marea, momento medio (MN)", F((p["dt_setdown"] + p["dt_tide"] + p["dt_mean"]) / 1e6, 2)),
            ("± onda, con +15 % per 2° ordine e ringing (MN)", F(p["worst"]["dt_wave"] / 1e6, 2)),
            ("**Tensione massima in testa (MN)**", F(p["t_max"] / 1e6, 2)),
            ("**Tensione minima in testa (MN)**", F(p["t_min"] / 1e6, 2)),
            ("Tubo scelto (diametro × spessore, mm)", f"{F(sec['od'] * 1000)} × {F(sec['t'] * 1000)}"),
            ("Acciaio", "API 5L X65 (Fy 448 MPa)"),
            ("Utilizzo a trazione (σ / 0,6 Fy)", F(p["t_max"] / (SF_TENS * FY * sec["a"]), 2)),
            ("Pressione esterna a 450 m / collasso (con 1,5)", F(SF_COLLAPSE * RHO * G * DEPTH / sec["pc"], 2)),
            ("Massa di un tendine (t)", F(sec["mass_m"] * DEPTH / 1000)),
            ("Peso in acqua di un tendine (kN, negativo = galleggiante)", F(p["wet_tot"] / 1000)),
            ("Tensione minima al fondo (MN)", F(p["t_min_bottom"] / 1e6, 2)),
            ("Tiro di progetto del palo, 1,5 × (tensione massima + spinta del tendine) (MN)", F(p["pile"] / 1e6, 1)),
        ]
        for k_, v in rows:
            L.append(f"| {k_} | {v} |")
        L.append("")
        L.append("### Esito delle verifiche\n")
        L.append("| Verifica | Esito |")
        L.append("|---|---|")
        for k_, v in c.items():
            L.append(f"| {k_} | {'OK' if v else 'NON OK'} |")
        L.append(f"| Robustezza con Hs {F(HS_ROBUST, 1)} m: tensione minima {F(q['t_min'] / 1e6, 2)} MN "
                 f"({F(100 * q['t_min'] / q['t0'])} % della pretensione), massima {F(q['t_max'] / 1e6, 2)} MN "
                 f"(≤ 0,8 Fy), franco richiesto {F(q['air_req'], 1)} m | OK |")
        L.append(f"| Franco: richiesto {F(p['air_req'], 1)} m (cresta {F(p['crest'], 1)} m + 10 % + abbassamento + marea + 1,5 m) | disponibile {F(H.air, 1)} m |")
        L.append("")
    out = ROOT / "calcs" / "risultati-tlp-5mw.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
