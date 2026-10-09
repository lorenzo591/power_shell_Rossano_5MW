"""Dimensionamento preliminare della powered shell da 5 MW IT su TLP.

Uso:  python3 calcs/dimensionamento_5mw.py
Scrive calcs/risultati.md e i disegni SVG in mechanical/.

Tutti i valori di ingresso sono IPOTESI di concept salvo dove indicato
(vedi colonna "fonte" nei dizionari). Unità SI; potenze in kW, masse in t.
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# 1. Dati di ingresso comuni
# ---------------------------------------------------------------------------

P_IT_TARGET = 5000.0  # kW, REQ-IT-001

# Container ISO 40' High Cube (ISO 668, 1AAA)
C40 = dict(L=12.192, W=2.438, H=2.896, L_int=12.03, W_int=2.35, H_int=2.69,
           max_gross=30.48)
TARE_40_OFFSHORE = 6.0  # t: 40' HC con pavimento rinforzato, isolamento, CX, porte laterali (ipotesi)

# Sorgente fredda: temperatura massima del mare alla presa (dataset Napoli 1987-2023,
# riportato in powered_shell_schneider-vertiv, confronto-inrow-cw, ipotesi I8)
SEA = {
    "25 m": dict(t_max=24.7, t_p99=23.4, t_min=12.7),
    "50 m": dict(t_max=21.7, t_p99=20.2, t_min=12.7),
}

# Proprietà fluidi (come bilancio-termico-pue.md del repo powered_shell_container)
CP_SEA, RHO_SEA = 3.99, 1025.0
CP_W, RHO_W = 4.18, 1000.0
CP_PG25, RHO_PG25 = 3.9, 1020.0
G = 9.81

# Avvicinamenti (ipotesi, da confermare con i fornitori)
APP_HX_SEA = 2.0     # K, scambiatore a piastre in titanio
DT_FWS_PICK = 0.5    # K, riscaldamento nel circuito prima delle utenze
APP_CDU = 3.5        # K, CDU liquido-liquido
APP_RDHX_AIR = 4.0   # K, aria in uscita dalla porta posteriore sopra l'acqua in ingresso

DT_SEA = 7.0   # K sull'acqua di mare (scarico <= 35 °C, REQ-ENV-018)
DT_FWS = 8.0   # K sul circuito intermedio
LIMIT_TCS = 45.0  # °C, ingresso liquido ai server (classe W45, NVIDIA MGX / HGX)

# ---------------------------------------------------------------------------
# 2. Configurazioni IT (rack di riferimento)
# ---------------------------------------------------------------------------

CONFIGS = {
    "A": dict(
        nome="A - rack classe GB300 NVL72 (140 kW), pod ISO 40' su 2 piani",
        rack_kw=140.0, rack_t=1.55, liq_frac=0.88, tcs_lpm_per_kw=1.5,
        racks_per_it=9, trafo_kva=1600, trafo_per_pod=2, lv_v=415.0,
        note="GB200/GB300 NVL72: 120-155 kW, 1,36-1,58 t, 87-90 % al liquido (ricerca DLC, repo container)",
    ),
    "B": dict(
        nome="B - server HGX 8-GPU 4U DLC, 4 per rack (56 kW), pod ISO 40' su 2 piani",
        rack_kw=56.0, rack_t=0.75, liq_frac=0.95, tcs_lpm_per_kw=1.5,
        racks_per_it=16, trafo_kva=1250, trafo_per_pod=2, lv_v=415.0,
        note="HGX B300 ~14 kW/server, 95 % al liquido (bilancio termico repo container)",
    ),
    "C": dict(
        nome="C - rack classe Vera Rubin (~200 kW, 800 V c.c.), pod ISO 40' su 2 piani",
        rack_kw=200.0, rack_t=1.85, liq_frac=0.97, tcs_lpm_per_kw=1.2,
        racks_per_it=9, trafo_kva=2500, trafo_per_pod=2, lv_v=415.0,
        note="Vera Rubin NVL: ~190 kW, ~1,8 t, 100 % liquido dichiarato, 800 V c.c. (fonte secondaria, n.v.)",
    ),
}

# Masse di allestimento (t) - ipotesi, vedi mechanical/layout-e-masse.md
IT_FIXED_T = dict(rdhx_per_rack=0.12, busway=0.6, tcs_piping_fluid=1.2,
                  fire_hvac_light=0.6, frame_anchors=1.0)
TRAFO_T = {1250: 3.0, 1600: 3.6, 2500: 5.4}  # trasformatori a secco in resina (ordine di grandezza)
LV_BOARD_T = 1.5      # t per quadro BT generale (per linea)
CDU_T = 1.3           # t per CDU a pavimento, piena
POD_LOWER_MISC_T = 1.8  # tubazioni, raffreddamento locale, supporti, antincendio

# Perdite trasformatori a secco <= 24 kV, Reg. UE 548/2014 Tier 2 (Po, Pk in kW)
TRAFO_LOSS = {1250: (1.80, 11.0), 1600: (2.20, 14.0), 2500: (3.10, 21.0)}

PF = 0.95          # fattore di potenza complessivo (ipotesi)
MARGIN = 1.15      # margine di progetto sulla potenza al punto di consegna
V_MT = 20_000.0    # V, media tensione e-distribuzione (ipotesi da verificare)
GANGWAY = 1.2      # m, passerella tra le colonne di container
EDGE = 1.0         # m, passerella perimetrale
END_ACCESS = 1.5   # m, spazio alle testate (porte, scale)


def ceil_div(a: float, b: float) -> int:
    return int(math.ceil(a / b - 1e-9))


def pump_kw(flow_m3h: float, head_m: float, eta: float, rho: float) -> float:
    return rho * G * (flow_m3h / 3600.0) * head_m / eta / 1000.0


def size(cfg: dict, intake: str, trim_chiller: bool) -> dict:
    """Bilancio elettrico e termico di una configurazione."""
    r = {}
    n_racks = ceil_div(P_IT_TARGET, cfg["rack_kw"])
    n_pods = ceil_div(n_racks, cfg["racks_per_it"])
    racks_inst = n_pods * cfg["racks_per_it"]
    p_it = n_racks * cfg["rack_kw"]  # carico IT di progetto (rack necessari)
    r.update(n_racks=n_racks, n_pods=n_pods, racks_slots=racks_inst, p_it=p_it,
             p_it_cap=racks_inst * cfg["rack_kw"])

    # --- calore ---
    q_liq = p_it * cfg["liq_frac"]
    q_air_it = p_it - q_liq
    n_containers = 2 * n_pods + 2  # pod (IT + potenza/CDU) + colonna servizi (2)
    q_envelope = 4.0 * n_containers  # kW, sole e aria esterna (stima, calcolo da fare)

    # --- portate e pompe ---
    tcs_m3h = q_liq * cfg["tcs_lpm_per_kw"] * 60 / 1000
    p_tcs = pump_kw(tcs_m3h, 30.0, 0.55, RHO_PG25)

    # trasformatori: in 2N ognuno porta metà del carico del pod
    n_tr = n_pods * cfg["trafo_per_pod"]
    s_pod = (p_it / n_pods) * 1.03 / PF  # kVA per pod (IT + ausiliari del pod)
    load_tr = (s_pod / cfg["trafo_per_pod"]) / cfg["trafo_kva"]
    po, pk = TRAFO_LOSS[cfg["trafo_kva"]]
    p_tr_loss = n_tr * (po + pk * load_tr ** 2)

    p_lv_dist = 0.005 * p_it        # blindosbarre e cavi BT
    p_ctrl = 25.0                  # BMS, rete di gestione, luci, rivelazione, telecom
    p_hvac = 3.0 * n_containers    # ventilconvettori, deumidificazione, sovrappressione
    p_mgps = 10.0                  # antivegetativo, filtri autopulenti

    q_air_total = q_air_it + p_tr_loss + p_lv_dist + q_envelope
    p_fans = 0.02 * q_air_total  # ventole delle unità aria/acqua e RDHx attive

    p_chiller = 0.0
    if trim_chiller:
        p_chiller = q_air_total / 6.0  # COP ~6, condensato sul FWS (ipotesi)

    # iterazione semplice: il calore al mare dipende dalle pompe
    p_sea = p_fws = 0.0
    for _ in range(5):
        p_aux_partial = p_tcs + p_fws + p_sea + p_fans + p_chiller + p_hvac + p_mgps + p_ctrl
        p_ups_mech = 0.04 * (p_tcs + p_fws + p_sea + p_ctrl)  # UPS 2N per pompe e controlli
        q_to_sea = p_it + p_aux_partial + p_tr_loss + p_lv_dist + p_ups_mech + q_envelope
        fws_m3h = q_to_sea / (CP_W * DT_FWS) / RHO_W * 3600
        sea_m3h = q_to_sea / (CP_SEA * DT_SEA) / RHO_SEA * 3600
        p_fws = pump_kw(fws_m3h, 25.0, 0.70, RHO_W)
        p_sea = pump_kw(sea_m3h, 25.0, 0.65, RHO_SEA)

    p_mech = p_tcs + p_fws + p_sea + p_fans + p_chiller + p_hvac + p_mgps
    p_losses = p_tr_loss + p_lv_dist + p_ups_mech
    p_aux = p_mech + p_losses + p_ctrl
    p_tot = p_it + p_aux
    pue = p_tot / p_it

    # --- temperature (giorno peggiore) ---
    t_sea = SEA[intake]["t_max"]
    t_fws = t_sea + APP_HX_SEA + DT_FWS_PICK
    t_tcs = t_fws + APP_CDU
    t_air = (18.0 + APP_RDHX_AIR) if trim_chiller else (t_fws + APP_RDHX_AIR)
    t_dis = t_sea + DT_SEA

    # --- elettrico ---
    s_tot = p_tot / PF
    s_design = s_tot * MARGIN
    i_mt = s_design * 1000 / (math.sqrt(3) * V_MT)
    i_lv_tr = cfg["trafo_kva"] * 1000 / (math.sqrt(3) * cfg["lv_v"])
    ik_lv = cfg["trafo_kva"] / (math.sqrt(3) * cfg["lv_v"] / 1000 * 0.06) / 1000  # kA, uk 6 %
    i_rack_side = cfg["rack_kw"] * 1000 / (math.sqrt(3) * cfg["lv_v"] * 0.98)

    r.update(q_liq=q_liq, q_air_it=q_air_it, q_air_total=q_air_total, q_env=q_envelope,
             q_to_sea=q_to_sea, tcs_m3h=tcs_m3h, fws_m3h=fws_m3h, sea_m3h=sea_m3h,
             p_tcs=p_tcs, p_fws=p_fws, p_sea=p_sea, p_fans=p_fans, p_chiller=p_chiller,
             p_hvac=p_hvac, p_mgps=p_mgps, p_ctrl=p_ctrl, p_tr_loss=p_tr_loss,
             p_lv_dist=p_lv_dist, p_ups_mech=p_ups_mech, p_mech=p_mech,
             p_losses=p_losses, p_aux=p_aux, p_tot=p_tot, pue=pue,
             t_sea=t_sea, t_fws=t_fws, t_tcs=t_tcs, t_air=t_air, t_dis=t_dis,
             s_tot=s_tot, s_design=s_design, i_mt=i_mt, n_tr=n_tr, load_tr=load_tr,
             s_pod=s_pod, i_lv_tr=i_lv_tr, ik_lv=ik_lv, i_rack_side=i_rack_side,
             n_containers=n_containers, ups_mech_kw=(p_tcs + p_fws + p_sea + p_ctrl + p_fans))
    return r


# ---------------------------------------------------------------------------
# 3. Masse, baricentro, ingombri
# ---------------------------------------------------------------------------

def masses(cfg: dict, r: dict) -> dict:
    n = cfg["racks_per_it"]
    it = (TARE_40_OFFSHORE + n * (cfg["rack_t"] + IT_FIXED_T["rdhx_per_rack"])
          + IT_FIXED_T["busway"] + IT_FIXED_T["tcs_piping_fluid"]
          + IT_FIXED_T["fire_hvac_light"] + IT_FIXED_T["frame_anchors"])
    lower = (TARE_40_OFFSHORE + cfg["trafo_per_pod"] * (TRAFO_T[cfg["trafo_kva"]] + LV_BOARD_T)
             + 2 * CDU_T + POD_LOWER_MISC_T)
    # colonna servizi: sotto skid scambiatori/pompe FWS (bagnato), sopra MT + controllo
    hx_skid = TARE_40_OFFSHORE + 3 * 2.5 + 3 * 0.8 + 2 * 1.2 + 4.0  # HX Ti, pompe FWS, filtri, tubi+acqua
    mv_ctrl = TARE_40_OFFSHORE + 10 * 0.4 + 2 * 0.6 + 4 * 0.49 + 1.0 + 1.5 + 1.0
    frame = 6.0 + 4.5 * (r["n_pods"] + 1)   # telaio con guide cellulari, passerelle, scale
    pipes_cables = 2.5 * (r["n_pods"] + 1)
    sea_pumps_risers = 8.0
    total = (r["n_pods"] * (it + lower) + hx_skid + mv_ctrl + frame + pipes_cables
             + sea_pumps_risers)

    # baricentro verticale sopra il ponte
    z0 = 0.15  # m, appoggi/twist-lock sul telaio di base
    zc_low = z0 + 0.40 * C40["H"]
    zc_up = z0 + C40["H"] + 0.42 * C40["H"]
    mom = (r["n_pods"] * (lower * zc_low + it * zc_up) + hx_skid * zc_low + mv_ctrl * zc_up
           + frame * 2.2 + pipes_cables * 3.0 + sea_pumps_risers * -5.0)
    zg = mom / total
    return dict(it=it, lower=lower, hx_skid=hx_skid, mv_ctrl=mv_ctrl, frame=frame,
                pipes_cables=pipes_cables, sea_pumps=sea_pumps_risers, total=total, zg=zg)


def footprint(n_pods: int, tiers: int = 2) -> dict:
    cols = n_pods + 1  # +1 colonna servizi
    if tiers == 2:
        rows = 1
        ncols = cols
    else:  # 1 piano: 2 file di container
        rows = 2
        ncols = cols
    width = ncols * C40["W"] + (ncols - 1) * GANGWAY + 2 * EDGE
    length = rows * C40["L"] + (rows + 1) * END_ACCESS
    h = tiers * C40["H"] + 0.15 + 0.6  # + telaio e tettoia parasole
    return dict(width=width, length=length, area=width * length, height=h,
                share=width * length / 900.0)


def tow_check(m_top: float) -> dict:
    """Container superiore in rimorchio: dati SIZ0PLT001 (TLP pilota), fattore 1,3."""
    f = 1.3
    ay, az = 3.36 * f, 11.18
    f_lat = m_top * ay  # kN
    h_cg = 0.42 * C40["H"]
    m_ov = f_lat * h_cg
    w = m_top * az
    restoring = w * C40["W"] / 2
    return dict(f_lat=f_lat, m_ov=m_ov, restoring=restoring, f_vert=m_top * 11.54 * f,
                racking_iso=150.0)


# ---------------------------------------------------------------------------
# 4. Uscita
# ---------------------------------------------------------------------------

def fmt(x: float, d: int = 0) -> str:
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def svg_layout(n_pods: int, path_plan: Path, path_sec: Path) -> None:
    s = 30.0  # px per m
    fp = footprint(n_pods)
    W, L = 30.0, 30.0
    pad = 20
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*s+2*pad+260}" height="{L*s+2*pad}" '
           f'font-family="Helvetica,Arial,sans-serif" font-size="12">',
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           f'<rect x="{pad}" y="{pad}" width="{W*s}" height="{L*s}" fill="#eef3f7" stroke="#5b7083" '
           f'stroke-dasharray="6 4"/>',
           f'<text x="{pad+6}" y="{pad+16}" fill="#5b7083">Ponte TLP 30 × 30 m (ipotesi)</text>']
    x0 = pad + (W - fp["width"]) / 2 * s
    y0 = pad + 3.0 * s
    out.append(f'<rect x="{x0}" y="{y0}" width="{fp["width"]*s}" height="{fp["length"]*s}" '
               f'fill="#dfe7ee" stroke="#33475b"/>')
    x = x0 + EDGE * s
    for i in range(n_pods + 1):
        yc = y0 + END_ACCESS * s
        svc = i == n_pods
        fill = "#f6d7a7" if svc else "#a9cce3"
        out.append(f'<rect x="{x}" y="{yc}" width="{C40["W"]*s}" height="{C40["L"]*s}" fill="{fill}" '
                   f'stroke="#1b2631"/>')
        label = "SERVIZI" if svc else f"POD {i+1}"
        sub1 = "sopra: MT + controllo" if svc else "sopra: IT 9 rack"
        sub2 = "sotto: scambiatori + pompe" if svc else "sotto: trafo A/B + CDU"
        cx = x + C40["W"] * s / 2
        cy = yc + C40["L"] * s / 2
        for k, t in enumerate((label, sub1, sub2)):
            tx = cx + (k - 1) * 18 + 4
            out.append(f'<text x="{tx}" y="{cy}" text-anchor="middle" '
                       f'transform="rotate(-90 {tx} {cy})" '
                       f'font-weight="{"bold" if k == 0 else "normal"}">{t}</text>')
        if i < n_pods:
            gx = x + C40["W"] * s
            out.append(f'<rect x="{gx}" y="{yc}" width="{GANGWAY*s}" height="{C40["L"]*s}" '
                       f'fill="#ffffff" stroke="#9aa9b8" stroke-dasharray="3 3"/>')
        x += (C40["W"] + GANGWAY) * s
    # pompe sommerse e cavi
    by = y0 + fp["length"] * s + 1.5 * s
    out.append(f'<rect x="{x0}" y="{by}" width="{fp["width"]*s}" height="{2.0*s}" fill="#d5f5e3" stroke="#1e8449"/>')
    out.append(f'<text x="{x0+8}" y="{by+18}">Pozzetti pompe sommerse (3 × 50 %) e risalite cavi MT A/B, '
               f'lungo le colonne della TLP</text>')
    lx = pad + W * s + 20
    legend = [
        f"Ingombro moduli: {fmt(fp['width'],1)} × {fmt(fp['length'],1)} m",
        f"= {fmt(fp['area'])} m² ({fmt(fp['share']*100)} % del ponte)",
        f"Altezza: circa {fmt(fp['height'],1)} m (2 piani 40' HC)",
        "Azzurro: pod IT (2 container 40' HC)",
        "Arancio: colonna servizi",
        "Bianco: passerelle 1,2 m (accesso",
        "  posteriore ai rack), su 2 livelli",
    ]
    for k, t in enumerate(legend):
        out.append(f'<text x="{lx}" y="{pad + 30 + 18*k}">{t}</text>')
    out.append("</svg>")
    path_plan.write_text("\n".join(out), encoding="utf-8")

    # sezione trasversale
    hs = 40.0
    ncols = n_pods + 1
    width = fp["width"]
    sec = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width*hs+80}" height="{9*hs}" '
           f'font-family="Helvetica,Arial,sans-serif" font-size="12">',
           '<rect width="100%" height="100%" fill="#ffffff"/>']
    deck_y = 8 * hs
    sec.append(f'<line x1="10" y1="{deck_y}" x2="{width*hs+70}" y2="{deck_y}" stroke="#1b2631" stroke-width="3"/>')
    sec.append(f'<text x="14" y="{deck_y+16}">Ponte TLP (circa +5 m sul mare in esercizio)</text>')
    x = 40 + EDGE * hs
    for i in range(ncols):
        svc = i == ncols - 1
        for tier in range(2):
            y = deck_y - 0.15 * hs - (tier + 1) * C40["H"] * hs
            fill = ("#f6d7a7" if svc else ("#a9cce3" if tier == 1 else "#c8d6e5"))
            sec.append(f'<rect x="{x}" y="{y}" width="{C40["W"]*hs}" height="{C40["H"]*hs}" '
                       f'fill="{fill}" stroke="#1b2631"/>')
            if svc:
                t = "MT+ctrl" if tier == 1 else "HX+pompe"
            else:
                t = "IT" if tier == 1 else "trafo+CDU"
            sec.append(f'<text x="{x + C40["W"]*hs/2}" y="{y + C40["H"]*hs/2}" text-anchor="middle">{t}</text>')
        x += (C40["W"] + GANGWAY) * hs
    top = deck_y - 0.15 * hs - 2 * C40["H"] * hs
    sec.append(f'<line x1="30" y1="{top - 0.6*hs}" x2="{width*hs+50}" y2="{top - 0.6*hs}" '
               f'stroke="#7f8c8d" stroke-width="4"/>')
    sec.append(f'<text x="40" y="{top - 0.6*hs - 6}">Tettoia parasole / telaio superiore</text>')
    sec.append("</svg>")
    path_sec.write_text("\n".join(sec), encoding="utf-8")


def main() -> None:
    lines: list[str] = []
    w = lines.append
    w("# Risultati del dimensionamento (generato)")
    w("")
    w("> File generato da `calcs/dimensionamento_5mw.py`. Non modificare a mano: cambiare le ipotesi "
      "nello script e rigenerare. Tutti i valori sono ipotesi di concept.")
    w("")

    results = {}
    for key, cfg in CONFIGS.items():
        for intake in ("25 m", "50 m"):
            for trim in (False, True):
                results[(key, intake, trim)] = size(cfg, intake, trim)

    # 1. Sintesi configurazioni (presa 25 m, senza chiller)
    w("## 1. Configurazioni IT (presa a 25 m, senza chiller)")
    w("")
    w("| Config | Rack di riferimento | kW/rack | Rack necessari | Rack per container IT | Pod (IT + potenza) | "
      "Container totali | IT di progetto (kW) | Capacità IT installabile (kW) |")
    w("|---|---|---|---|---|---|---|---|---|")
    for key, cfg in CONFIGS.items():
        r = results[(key, "25 m", False)]
        w(f"| {key} | {cfg['nome']} | {fmt(cfg['rack_kw'])} | {r['n_racks']} | {cfg['racks_per_it']} | "
          f"{r['n_pods']} | {r['n_containers']} | {fmt(r['p_it'])} | {fmt(r['p_it_cap'])} |")
    w("")

    # 2. Bilancio potenze e PUE
    w("## 2. Ausiliari, perdite e PUE")
    w("")
    w("Casi di raffreddamento: **K1** presa a 25 m senza chiller · **K2** presa a 25 m con chiller di "
      "rifinitura sul solo circuito dell'aria · **K3** presa a 50 m senza chiller.")
    w("")
    w("| Voce (kW) | " + " | ".join(f"{k}-K1 | {k}-K2 | {k}-K3" for k in CONFIGS) + " |")
    w("|---|" + "---|" * (3 * len(CONFIGS)))
    cases = []
    for k in CONFIGS:
        cases += [results[(k, "25 m", False)], results[(k, "25 m", True)], results[(k, "50 m", False)]]
    rows = [
        ("Carico IT", "p_it"), ("Pompe circuito server (TCS, nelle CDU)", "p_tcs"),
        ("Pompe circuito intermedio (FWS)", "p_fws"), ("Pompe acqua di mare", "p_sea"),
        ("Ventole aria/acqua e RDHx", "p_fans"), ("Chiller di rifinitura (picco estivo)", "p_chiller"),
        ("HVAC container, deumidificazione", "p_hvac"), ("Antivegetativo e filtri", "p_mgps"),
        ("Perdite trasformatori", "p_tr_loss"), ("Perdite distribuzione BT", "p_lv_dist"),
        ("Perdite UPS ausiliari", "p_ups_mech"), ("Controlli, luci, telecom, sicurezza", "p_ctrl"),
        ("**Totale ausiliari e perdite**", "p_aux"), ("**Potenza totale al punto di consegna**", "p_tot"),
    ]
    for label, k in rows:
        w(f"| {label} | " + " | ".join(fmt(c[k]) for c in cases) + " |")
    w("| **PUE (giorno peggiore)** | " + " | ".join(fmt(c["pue"], 3) for c in cases) + " |")
    w("")

    # 3. Catena termica
    w("## 3. Catena delle temperature (giorno peggiore) e portate")
    w("")
    w("| Grandezza | " + " | ".join(f"{k}-K1 | {k}-K2 | {k}-K3" for k in CONFIGS) + " |")
    w("|---|" + "---|" * (3 * len(CONFIGS)))
    trows = [
        ("Mare alla presa, massimo (°C)", "t_sea", 1), ("Scarico a mare (°C, limite 35)", "t_dis", 1),
        ("Mandata FWS (°C)", "t_fws", 1), ("Mandata liquido ai server TCS (°C, limite 45)", "t_tcs", 1),
        ("Aria ai rack dopo RDHx (°C)", "t_air", 1), ("Calore al liquido dei server (kW)", "q_liq", 0),
        ("Calore all'aria totale (kW)", "q_air_total", 0), ("Calore ceduto al mare (kW)", "q_to_sea", 0),
        ("Portata TCS totale (m³/h)", "tcs_m3h", 0), ("Portata FWS (m³/h, ΔT 8 K)", "fws_m3h", 0),
        ("Portata acqua di mare (m³/h, ΔT 7 K)", "sea_m3h", 0),
    ]
    for label, k, d in trows:
        w(f"| {label} | " + " | ".join(fmt(c[k], d) for c in cases) + " |")
    w("")

    # 4. Elettrico
    w("## 4. Elettrico (caso K2, il più gravoso)")
    w("")
    w("| Grandezza | " + " | ".join(CONFIGS) + " |")
    w("|---|" + "---|" * len(CONFIGS))
    el = {k: results[(k, "25 m", True)] for k in CONFIGS}
    erows = [
        ("Potenza attiva totale (kW)", lambda r, c: fmt(r["p_tot"])),
        ("Potenza apparente, cos φ 0,95 (kVA)", lambda r, c: fmt(r["s_tot"])),
        ("Con margine 15 % (kVA)", lambda r, c: fmt(r["s_design"])),
        ("Corrente MT a 20 kV per cavo, 2 × 100 % (A)", lambda r, c: fmt(r["i_mt"])),
        ("Trasformatori 20/0,415 kV a secco", lambda r, c: f"{r['n_tr']} × {fmt(c['trafo_kva'])} kVA"),
        ("Potenza apparente per pod (kVA)", lambda r, c: fmt(r["s_pod"])),
        ("Carico di ogni trasformatore in 2N normale", lambda r, c: f"{fmt(r['load_tr']*100)} %"),
        ("Carico di ogni trasformatore con il gemello fuori", lambda r, c: f"{fmt(r['load_tr']*200)} %"),
        ("Corrente nominale BT per trasformatore (A)", lambda r, c: fmt(r["i_lv_tr"])),
        ("Cortocircuito BT ai morsetti, uk 6 % (kA)", lambda r, c: fmt(r["ik_lv"], 1)),
        ("Corrente per rack per lato A o B a 415 V (A)", lambda r, c: fmt(r["i_rack_side"])),
        ("Carichi meccanici critici sotto UPS (kW)", lambda r, c: fmt(r["ups_mech_kw"])),
    ]
    for label, f in erows:
        w(f"| {label} | " + " | ".join(f(el[k], CONFIGS[k]) for k in CONFIGS) + " |")
    w("")
    # sezione minima cavo MT per corto circuito
    ik_mt, t_sc, k_cu = 16.0, 1.0, 143.0
    s_min = ik_mt * 1000 * math.sqrt(t_sc) / k_cu
    w(f"Sezione minima del cavo MT per tenere {fmt(ik_mt)} kA per {fmt(t_sc)} s (Cu, XLPE, k = 143): "
      f"**{fmt(s_min)} mm²** → si sceglie 3 × 120 mm² Cu (o 3 × 185 mm² Al). La portata (circa 300 A "
      f"in posa sottomarina, da verificare sul catalogo) supera largamente la corrente di esercizio.")
    w("")
    # caduta di tensione MT
    r_km, x_km, L = 0.196, 0.11, 0.35
    i = el["A"]["i_mt"]
    dv = math.sqrt(3) * i * L * (r_km * PF + x_km * math.sin(math.acos(PF)))
    w(f"Caduta di tensione sul cavo MT (config A, {fmt(i)} A, {fmt(L*1000)} m, 3 × 120 mm² Cu): "
      f"{fmt(dv,1)} V = **{fmt(dv/V_MT*100,2)} %**: trascurabile.")
    w("")
    # confronto BT da terra
    i_bt = el["A"]["s_design"] * 1000 / (math.sqrt(3) * 400)
    w(f"Confronto con l'alimentazione in BT da terra (ADR 0001 dei repo precedenti): a 400 V servirebbero "
      f"**{fmt(i_bt)} A**, cioè circa {ceil_div(i_bt, 400)} cavi da 240 mm² per fase su 250-350 m. "
      f"Non praticabile: a 5 MW la MT fino alla TLP è obbligata.")
    w("")

    # 5. Masse e ingombri
    w("## 5. Masse, baricentro e ingombri (presa 25 m)")
    w("")
    w("| Grandezza | " + " | ".join(CONFIGS) + " |")
    w("|---|" + "---|" * len(CONFIGS))
    ms = {k: masses(CONFIGS[k], results[(k, "25 m", False)]) for k in CONFIGS}
    fps = {k: footprint(results[(k, "25 m", False)]["n_pods"]) for k in CONFIGS}
    fp1 = {k: footprint(results[(k, "25 m", False)]["n_pods"], tiers=1) for k in CONFIGS}
    mrows = [
        ("Container IT pieno (t, max lordo ISO 30,48)", lambda k: fmt(ms[k]["it"], 1)),
        ("Container inferiore potenza + CDU (t)", lambda k: fmt(ms[k]["lower"], 1)),
        ("Skid scambiatori e pompe FWS (t)", lambda k: fmt(ms[k]["hx_skid"], 1)),
        ("Container MT e controllo (t)", lambda k: fmt(ms[k]["mv_ctrl"], 1)),
        ("Telaio, guide, passerelle (t)", lambda k: fmt(ms[k]["frame"], 1)),
        ("**Massa totale sul ponte (t)**", lambda k: fmt(ms[k]["total"])),
        ("Baricentro verticale sopra il ponte (m)", lambda k: fmt(ms[k]["zg"], 2)),
        ("Ingombro 2 piani L × W (m)", lambda k: f"{fmt(fps[k]['length'],1)} × {fmt(fps[k]['width'],1)}"),
        ("Area 2 piani (m²) / quota del ponte 30 × 30", lambda k: f"{fmt(fps[k]['area'])} / {fmt(fps[k]['share']*100)} %"),
        ("Ingombro 1 piano L × W (m)", lambda k: f"{fmt(fp1[k]['length'],1)} × {fmt(fp1[k]['width'],1)}"),
        ("Area 1 piano (m²) / quota del ponte", lambda k: f"{fmt(fp1[k]['area'])} / {fmt(fp1[k]['share']*100)} %"),
        ("Densità IT su ingombro 2 piani (kW/m²)", lambda k: fmt(results[(k, '25 m', False)]["p_it"] / fps[k]["area"], 1)),
    ]
    for label, f in mrows:
        w(f"| {label} | " + " | ".join(f(k) for k in CONFIGS) + " |")
    w("")
    w("Nota: una dimensione sopra 30 m o una quota oltre il 100 % indica che la soluzione a 1 piano non sta "
      "sul ponte 30 × 30 con questa disposizione.")
    w("")

    # 6. Rimorchio
    w("## 6. Container superiore in rimorchio (config A)")
    w("")
    tc = tow_check(ms["A"]["it"])
    w("Accelerazioni del documento SIZ0PLT001 rev 0 (TLP del pilota, da rifare per la TLP da 5 MW), "
      "fattore 1,3 proposto nel repo container.")
    w("")
    w("| Grandezza | Valore |")
    w("|---|---|")
    w(f"| Forza laterale sul container IT (kN) | {fmt(tc['f_lat'])} |")
    w(f"| Momento ribaltante alla base (kNm) | {fmt(tc['m_ov'])} |")
    w(f"| Momento stabilizzante del peso (kNm) | {fmt(tc['restoring'])} |")
    w(f"| Forza verticale massima (kN) | {fmt(tc['f_vert'])} |")
    w(f"| Prova di racking trasversale ISO 1496-1 (kN, riferimento) | {fmt(tc['racking_iso'])} |")
    w("")
    w("Il peso basta contro il ribaltamento, ma la forza laterale è dello stesso ordine della prova di racking "
      "di un container integro, e il container IT ha porte laterali che indeboliscono la parete. Servono "
      "**guide cellulari / telaio esterno** che portino le forze orizzontali al ponte, non solo twist-lock.")
    w("")

    (ROOT / "calcs" / "risultati.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    svg_layout(results[("A", "25 m", False)]["n_pods"], ROOT / "mechanical" / "layout-pianta-config-a.svg",
               ROOT / "mechanical" / "layout-sezione-config-a.svg")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
