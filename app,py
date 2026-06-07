import streamlit as st
import math

st.set_page_config(page_title="Substation Calculator", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .block-container { padding: 1rem 1rem 2rem; max-width: 480px; margin: auto; }
    h1 { font-size: 1.2rem !important; font-weight: 700 !important; color: #03223a !important; margin-bottom: 0 !important; }
    h2 { font-size: 1rem !important; font-weight: 600 !important; color: #0a2a42 !important;
         border-left: 4px solid #7ab8d4; padding-left: 8px; margin-top: 1.2rem !important; }
    h3 { font-size: 0.85rem !important; font-weight: 600 !important; color: #0a2a42 !important; margin: 0.8rem 0 0.3rem !important; }
    .stNumberInput label { font-size: 0.82rem !important; color: #03223a !important; font-weight: 500 !important; }
    div[data-testid="stNumberInput"] input {
        background: #ffffff; border: 1px solid #7ab8d4;
        border-radius: 6px; font-size: 0.95rem; color: #03223a;
    }
    .result-card {
        background: #ffffff; border: 1px solid #7ab8d4;
        border-radius: 8px; padding: 0.6rem 0.9rem; margin: 0.4rem 0;
        display: flex; justify-content: space-between; align-items: center;
    }
    .result-label { font-size: 0.78rem; color: #0a2a42; font-weight: 500; }
    .result-value { font-size: 1.05rem; font-weight: 700; color: #03223a; }
    .result-unit  { font-size: 0.72rem; color: #7ab8d4; margin-left: 3px; }
    .flag-ok   { background: #e6f4ea; border-color: #4caf50; }
    .flag-warn { background: #fff8e1; border-color: #f9a825; }
    .flag-fail { background: #fdecea; border-color: #e53935; }
    .flag-text-ok   { color: #2e7d32 !important; }
    .flag-text-warn { color: #f57f17 !important; }
    .flag-text-fail { color: #c62828 !important; }
    .ref-section { background: #f0f8fc; border-radius: 8px; padding: 0.6rem 0.8rem; margin-top: 0.5rem; }
    table { width: 100%; border-collapse: collapse; font-size: 0.75rem; }
    th { background: #e8f4fa; color: #03223a; font-weight: 600;
         padding: 5px 8px; text-align: left; border-bottom: 1px solid #7ab8d4; }
    td { padding: 4px 8px; color: #0a2a42; border-bottom: 0.5px solid #d0e8f2; }
    tr:last-child td { border-bottom: none; }
    .stExpander { border: 1px solid #7ab8d4 !important; border-radius: 8px !important; }
    .divider { border: none; border-top: 1px solid #d0e8f2; margin: 1rem 0 0.5rem; }
    .sub-note { font-size: 0.72rem; color: #5a8fa8; margin: 0.2rem 0 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ Substation Design Calculator")
st.markdown('<p class="sub-note">Primary system — EHV/HV · Preliminary sizing</p>', unsafe_allow_html=True)

# ── REFERENCE TABLES ────────────────────────────────────────────────
with st.expander("📋 Conductor & Equipment Reference"):
    st.markdown('<div class="ref-section">', unsafe_allow_html=True)

    st.markdown("### Overhead line conductors (ACSR)")
    st.markdown("""
<table>
<tr><th>Conductor</th><th>Rating (A)</th><th>Voltage level</th></tr>
<tr><td>Weasel</td><td>175</td><td>11 / 33 kV</td></tr>
<tr><td>Rabbit</td><td>245</td><td>33 kV</td></tr>
<tr><td>Dog</td><td>261</td><td>33 / 66 kV</td></tr>
<tr><td>Lynx</td><td>340</td><td>66 / 110 kV</td></tr>
<tr><td>Panther</td><td>385</td><td>110 kV</td></tr>
<tr><td>Wolf</td><td>415</td><td>110 / 132 kV</td></tr>
<tr><td>Zebra</td><td>550</td><td>110 / 132 / 220 kV</td></tr>
<tr><td>Moose</td><td>655</td><td>220 / 400 kV</td></tr>
<tr><td>Bersfort</td><td>800</td><td>400 kV</td></tr>
<tr><td>Twin Moose</td><td>1300</td><td>400 kV</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### Copper busbar (indoor / GIS)")
    st.markdown("""
<table>
<tr><th>Size (mm)</th><th>Rating (A)</th><th>Voltage level</th></tr>
<tr><td>50 × 6</td><td>630</td><td>11 kV</td></tr>
<tr><td>63 × 6</td><td>800</td><td>11 kV</td></tr>
<tr><td>80 × 8</td><td>1250</td><td>11 / 33 kV</td></tr>
<tr><td>100 × 10</td><td>1600</td><td>33 kV</td></tr>
<tr><td>120 × 10</td><td>2000</td><td>33 kV</td></tr>
<tr><td>160 × 10</td><td>2500</td><td>33 kV</td></tr>
<tr><td>200 × 12</td><td>3150</td><td>33 / 110 kV GIS</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### Circuit breaker — standard ratings (IEC 62271)")
    st.markdown("""
<table>
<tr><th>Voltage</th><th>Current (A)</th><th>Breaking (kA)</th></tr>
<tr><td>11 kV</td><td>630 / 1250</td><td>25 / 31.5</td></tr>
<tr><td>33 kV</td><td>1250 / 2000</td><td>25 / 31.5 / 40</td></tr>
<tr><td>110 kV</td><td>1250 / 2000 / 3150</td><td>31.5 / 40</td></tr>
<tr><td>230 kV</td><td>1250 / 2000 / 3150</td><td>40 / 50</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### CT primary ratios — standard (IEC 61869-2)")
    st.markdown("""
<table>
<tr><th>Voltage</th><th>Standard primary current (A)</th></tr>
<tr><td>11 / 33 kV</td><td>200, 300, 400, 600, 800, 1000, 1200, 1500, 2000</td></tr>
<tr><td>110 / 230 kV</td><td>200, 400, 600, 800, 1000, 1200, 1500, 2000, 2500</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── INPUTS ──────────────────────────────────────────────────────────
st.markdown("## System Inputs")

col1, col2 = st.columns(2)
with col1:
    hv_kv      = st.number_input("HV source voltage (kV)", value=110.0, step=1.0, min_value=1.0)
    lv_kv      = st.number_input("LV system voltage (kV)", value=33.0,  step=1.0, min_value=1.0)
    load_mva   = st.number_input("Total load demand (MVA)", value=40.0, step=1.0, min_value=0.1)
with col2:
    loading_pct = st.number_input("Transformer loading (%)", value=50.0, step=5.0, min_value=1.0, max_value=100.0)
    zpu_pct     = st.number_input("Transformer Zpu (%)", value=10.0, step=0.5, min_value=0.1)
    n_working   = st.number_input("Working transformers", value=1, step=1, min_value=1)

st.markdown("## Conductor Inputs")
st.markdown('<p class="sub-note">Enter from reference table above</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    hv_cond_name   = st.text_input("HV conductor name", value="Zebra")
    hv_cond_rating = st.number_input("HV conductor rating (A)", value=550.0, step=10.0, min_value=1.0)
with col4:
    lv_bus_name    = st.text_input("LV busbar description", value="120×10 Cu")
    lv_bus_rating  = st.number_input("LV busbar rating (A)", value=2000.0, step=50.0, min_value=1.0)

# ── CALCULATIONS ────────────────────────────────────────────────────
SQRT3 = math.sqrt(3)

tr_mva_required = load_mva / (loading_pct / 100.0) / n_working

hv_fl_current = (tr_mva_required * 1000) / (SQRT3 * hv_kv)
lv_fl_current = (tr_mva_required * 1000) / (SQRT3 * lv_kv)

zpu = zpu_pct / 100.0
fault_mva_hv  = (hv_kv ** 2) / zpu / 1000          # in GVA → convert below
fault_mva_hv  = (tr_mva_required) / zpu             # fault MVA referred to transformer base
fault_ka_hv   = (fault_mva_hv * 1000) / (SQRT3 * hv_kv)
fault_ka_lv   = (fault_mva_hv * 1000) / (SQRT3 * lv_kv)

CB_CURRENTS  = [630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000]
CB_BREAKING  = [16, 20, 25, 31.5, 40, 50, 63]
CT_RATIOS    = [200, 300, 400, 600, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000]

def next_standard(val, std_list):
    for s in std_list:
        if s >= val:
            return s
    return std_list[-1]

hv_cb_current  = next_standard(hv_fl_current, CB_CURRENTS)
lv_cb_current  = next_standard(lv_fl_current, CB_CURRENTS)
hv_cb_breaking = next_standard(fault_ka_hv,   CB_BREAKING)
lv_cb_breaking = next_standard(fault_ka_lv,   CB_BREAKING)
hv_ct_ratio    = next_standard(hv_fl_current, CT_RATIOS)
lv_ct_ratio    = next_standard(lv_fl_current, CT_RATIOS)

hv_ok = hv_fl_current <= hv_cond_rating
lv_ok = lv_fl_current <= lv_bus_rating

def result_row(label, value, unit, flag=None):
    card_class = ""
    val_class  = ""
    if flag == "ok":
        card_class = "flag-ok";   val_class = "flag-text-ok"
    elif flag == "warn":
        card_class = "flag-warn"; val_class = "flag-text-warn"
    elif flag == "fail":
        card_class = "flag-fail"; val_class = "flag-text-fail"
    st.markdown(f"""
    <div class="result-card {card_class}">
        <span class="result-label">{label}</span>
        <span>
            <span class="result-value {val_class}">{value}</span>
            <span class="result-unit">{unit}</span>
        </span>
    </div>""", unsafe_allow_html=True)

# ── RESULTS ─────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## Results")

st.markdown("### Transformer")
result_row("Required rating (each)", f"{tr_mva_required:.1f}", "MVA")

st.markdown("### HV side")
result_row("Full-load current", f"{hv_fl_current:.1f}", "A",
           flag="ok" if hv_ok else "fail")
result_row(f"Conductor adequacy ({hv_cond_name}  {hv_cond_rating:.0f} A)",
           "ADEQUATE" if hv_ok else "INADEQUATE", "",
           flag="ok" if hv_ok else "fail")
result_row("Fault current (3φ)", f"{fault_ka_hv:.2f}", "kA")
result_row("Recommended CB current", f"{hv_cb_current}", "A")
result_row("Recommended CB breaking", f"{hv_cb_breaking}", "kA")
result_row("Recommended CT ratio", f"{hv_ct_ratio} / 1", "A")

st.markdown("### LV side")
result_row("Full-load current", f"{lv_fl_current:.1f}", "A",
           flag="ok" if lv_ok else "fail")
result_row(f"Busbar adequacy ({lv_bus_name}  {lv_bus_rating:.0f} A)",
           "ADEQUATE" if lv_ok else "INADEQUATE", "",
           flag="ok" if lv_ok else "fail")
result_row("Fault current (3φ)", f"{fault_ka_lv:.2f}", "kA")
result_row("Recommended CB current", f"{lv_cb_current}", "A")
result_row("Recommended CB breaking", f"{lv_cb_breaking}", "kA")
result_row("Recommended CT ratio", f"{lv_ct_ratio} / 1", "A")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<p class="sub-note">Fault MVA based on transformer Zpu only · Source impedance not included · For preliminary review use only</p>', unsafe_allow_html=True)
