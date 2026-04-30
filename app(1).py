import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, datetime
import json
import io

# ============================================================
# CONFIGURATION PAGE
# ============================================================
st.set_page_config(
    page_title="VentaScope — Collecte & Analyse des Ventes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PERSONNALISÉ
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #13131a !important;
    border-right: 1px solid #2a2a3d;
}

/* Titres */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    color: #e8e8f0 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #13131a;
    border: 1px solid #2a2a3d;
    border-radius: 12px;
    padding: 1rem;
    border-top: 2px solid #f0c040;
}
[data-testid="stMetricLabel"] { color: #8888aa !important; font-size: 0.72rem !important; letter-spacing: 1px; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #f0c040 !important; font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

/* Boutons */
.stButton > button {
    background: #f0c040 !important;
    color: #0a0a0f !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #ffd060 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(240,192,64,0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: #0a0a0f !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #2a2a3d;
    border-radius: 12px;
    overflow: hidden;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: #13131a !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid #2a2a3d !important;
}
[data-baseweb="tab"] {
    color: #8888aa !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
}
[aria-selected="true"] {
    background: #f0c040 !important;
    color: #0a0a0f !important;
}

/* Success / info */
.stSuccess { background: rgba(78,205,196,0.1) !important; border: 1px solid #4ecdc4 !important; border-radius: 8px !important; }
.stWarning { background: rgba(240,192,64,0.1) !important; border: 1px solid #f0c040 !important; border-radius: 8px !important; }
.stError   { background: rgba(224,92,58,0.1) !important; border: 1px solid #e05c3a !important; border-radius: 8px !important; }

/* Divider */
hr { border-color: #2a2a3d !important; }

/* Card custom */
.card {
    background: #13131a;
    border: 1px solid #2a2a3d;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-gold  { background: rgba(240,192,64,0.15); color: #f0c040; }
.badge-teal  { background: rgba(78,205,196,0.15); color: #4ecdc4; }
.badge-red   { background: rgba(224,92,58,0.15);  color: #e05c3a; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DONNÉES DE DÉMONSTRATION
# ============================================================
DEMO_DATA = [
    {"date": "2025-01-05", "vendeur": "Alima Ngo", "produit": "Laptop Dell", "categorie": "Informatique", "quantite": 2, "prix_unitaire": 450000, "total": 900000, "region": "Centre", "canal": "Boutique physique", "statut": "Complétée", "client": "Société Bingo"},
    {"date": "2025-01-08", "vendeur": "Boris Kamga", "produit": "Forfait Pro", "categorie": "Services", "quantite": 5, "prix_unitaire": 85000, "total": 425000, "region": "Littoral", "canal": "En ligne", "statut": "Complétée", "client": "SARL Étoile"},
    {"date": "2025-01-12", "vendeur": "Alima Ngo", "produit": "Smartphone Tecno", "categorie": "Électronique", "quantite": 3, "prix_unitaire": 120000, "total": 360000, "region": "Ouest", "canal": "Boutique physique", "statut": "Complétée", "client": "Particulier"},
    {"date": "2025-01-15", "vendeur": "Cédric Fouda", "produit": "Chaise bureau", "categorie": "Mobilier", "quantite": 10, "prix_unitaire": 35000, "total": 350000, "region": "Centre", "canal": "Partenaire", "statut": "En attente", "client": "Admin Lycée"},
    {"date": "2025-01-18", "vendeur": "Boris Kamga", "produit": "Imprimante HP", "categorie": "Informatique", "quantite": 1, "prix_unitaire": 180000, "total": 180000, "region": "Littoral", "canal": "En ligne", "statut": "Complétée", "client": "Cabinet ABC"},
    {"date": "2025-02-02", "vendeur": "Diana Meka", "produit": "Sac cuir", "categorie": "Vêtements", "quantite": 4, "prix_unitaire": 55000, "total": 220000, "region": "Nord", "canal": "Boutique physique", "statut": "Complétée", "client": "Boutique Mode"},
    {"date": "2025-02-10", "vendeur": "Cédric Fouda", "produit": "Tablette Samsung", "categorie": "Électronique", "quantite": 2, "prix_unitaire": 210000, "total": 420000, "region": "Sud", "canal": "Téléphone", "statut": "Complétée", "client": "École Primaire"},
    {"date": "2025-02-14", "vendeur": "Alima Ngo", "produit": "Logiciel Compta", "categorie": "Informatique", "quantite": 1, "prix_unitaire": 320000, "total": 320000, "region": "Centre", "canal": "En ligne", "statut": "Annulée", "client": "PME Soleil"},
    {"date": "2025-03-01", "vendeur": "Boris Kamga", "produit": "Clim 1.5CV", "categorie": "Électronique", "quantite": 2, "prix_unitaire": 280000, "total": 560000, "region": "Littoral", "canal": "Boutique physique", "statut": "Complétée", "client": "Hôtel Palace"},
    {"date": "2025-03-15", "vendeur": "Diana Meka", "produit": "Formation Excel", "categorie": "Services", "quantite": 15, "prix_unitaire": 20000, "total": 300000, "region": "Ouest", "canal": "En ligne", "statut": "Complétée", "client": "Groupe Banque"},
]

# ============================================================
# SESSION STATE
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(DEMO_DATA)
if "show_payment" not in st.session_state:
    st.session_state["show_payment"] = False
if "pending_record" not in st.session_state:
    st.session_state["pending_record"] = None

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================
def fmt_fcfa(val):
    if val >= 1_000_000:
        return f"{val/1_000_000:.1f} M FCFA"
    elif val >= 1_000:
        return f"{val/1_000:.0f} K FCFA"
    return f"{val:,.0f} FCFA"

def get_df():
    return st.session_state.data.copy()

def save_record(record):
    new_row = pd.DataFrame([record])
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

PLOTLY_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#8888aa", "family": "DM Mono"},
    "colorway": ["#f0c040", "#e05c3a", "#4ecdc4", "#a78bfa", "#fb923c", "#34d399", "#f472b6", "#60a5fa"],
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='background:#f0c040; color:#0a0a0f; font-family:Syne,sans-serif;
                    font-weight:800; font-size:1.4rem; padding:10px 20px;
                    border-radius:10px; display:inline-block; margin-bottom:8px;'>VS</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem; color:#e8e8f0;'>
            Venta<span style='color:#f0c040'>Scope</span>
        </div>
        <div style='color:#55556a; font-size:0.7rem; margin-top:4px;'>Plateforme Commerciale & Analytique</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    df = get_df()
    total = len(df)
    ca = df[df["statut"] != "Annulée"]["total"].sum()

    st.markdown(f"""
    <div style='background:#1c1c28; border:1px solid #2a2a3d; border-radius:10px; padding:1rem; margin-bottom:1rem;'>
        <div style='color:#55556a; font-size:0.65rem; letter-spacing:1px; text-transform:uppercase;'>Enregistrements</div>
        <div style='color:#f0c040; font-family:Syne,sans-serif; font-weight:800; font-size:1.6rem;'>{total}</div>
        <div style='color:#55556a; font-size:0.65rem; letter-spacing:1px; text-transform:uppercase; margin-top:8px;'>Chiffre d'affaires</div>
        <div style='color:#4ecdc4; font-family:Syne,sans-serif; font-weight:700; font-size:1rem;'>{fmt_fcfa(ca)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='color:#55556a; font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px;'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", ["➕ Saisie des données", "📋 Base de données", "📊 Analyse descriptive"], label_visibility="collapsed")

    st.divider()
    st.markdown("""
    <div style='color:#55556a; font-size:0.65rem; text-align:center; line-height:1.6;'>
        © 2025 VentaScope<br>
        Tous droits réservés<br>
        <span style='color:#f0c040;'>Commerce & Ventes — Cameroun</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE 1 — SAISIE
# ============================================================
if page == "➕ Saisie des données":

    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1.5rem; border-bottom: 1px solid #2a2a3d; margin-bottom: 2rem;'>
        <!-- LOGO -->
        <div style='display:inline-flex; align-items:center; gap:14px; margin-bottom:1rem;'>
            <div style='background:#f0c040; color:#0a0a0f; font-family:Syne,sans-serif;
                        font-weight:900; font-size:2rem; width:60px; height:60px;
                        border-radius:14px; display:flex; align-items:center; justify-content:center;'>VS</div>
            <div style='text-align:left;'>
                <div style='font-family:Syne,sans-serif; font-weight:800; font-size:2.2rem;
                            color:#e8e8f0; letter-spacing:-1px; line-height:1;'>
                    Venta<span style='color:#f0c040;'>Scope</span>
                </div>
                <div style='color:#55556a; font-size:0.72rem; letter-spacing:2px; text-transform:uppercase; margin-top:2px;'>
                    Application de Collecte & Analyse des Ventes
                </div>
            </div>
        </div>
        <br/>
        <div style='display:inline-block; background:rgba(240,192,64,0.1); border:1px solid rgba(240,192,64,0.3);
                    color:#f0c040; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;
                    padding:4px 14px; border-radius:20px; margin-bottom:12px;'>
            Plateforme de gestion commerciale
        </div>
        <h1 style='font-size:2rem; letter-spacing:-1px; margin:8px 0 0;'>
            Saisie des <span style='color:#f0c040; font-style:italic;'>transactions</span>
        </h1>
        <p style='color:#8888aa; font-size:0.85rem; margin-top:8px;'>
            Enregistrez vos ventes commerciales. L'analyse se met à jour automatiquement.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_saisie", clear_on_submit=True):
        st.markdown("<div style='color:#8888aa; font-size:0.72rem; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:1rem;'>Informations de la vente</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            f_date = st.date_input("📅 Date de vente *", value=date.today())
            f_produit = st.text_input("📦 Produit / Service *", placeholder="Ex: Laptop Dell, Forfait Pro…")
            f_quantite = st.number_input("🔢 Quantité *", min_value=1, value=1)
            f_region = st.selectbox("🗺️ Région", ["Centre", "Littoral", "Ouest", "Nord", "Sud", "Adamaoua", "Est", "Nord-Ouest", "Sud-Ouest", "Extrême-Nord"])
            f_statut = st.selectbox("✅ Statut", ["Complétée", "En attente", "Annulée"])

        with col2:
            f_vendeur = st.text_input("👤 Vendeur *", placeholder="Nom du vendeur")
            f_categorie = st.selectbox("🏷️ Catégorie", ["Électronique", "Informatique", "Services", "Vêtements", "Mobilier", "Alimentation", "Autre"])
            f_prix = st.number_input("💰 Prix unitaire (FCFA) *", min_value=0, value=0, step=1000)
            f_canal = st.selectbox("📡 Canal de vente", ["Boutique physique", "En ligne", "Téléphone", "Partenaire"])
            f_client = st.text_input("🏢 Client", placeholder="Nom ou réf. client (optionnel)")

        f_remarques = st.text_area("📝 Remarques", placeholder="Observations, conditions particulières…", height=80)

        st.divider()
        col_a, col_b, col_c = st.columns([2, 1, 1])
        with col_b:
            total_preview = f_quantite * f_prix
            st.markdown(f"<div style='color:#8888aa; font-size:0.72rem;'>Total estimé</div><div style='color:#f0c040; font-family:Syne,sans-serif; font-weight:700; font-size:1.1rem;'>{fmt_fcfa(total_preview)}</div>", unsafe_allow_html=True)
        with col_c:
            submitted = st.form_submit_button("✓ Enregistrer", use_container_width=True)

    if submitted:
        if not f_vendeur or not f_produit or f_prix <= 0:
            st.error("⚠️ Veuillez remplir tous les champs obligatoires (Vendeur, Produit, Prix).")
        else:
            record = {
                "date": str(f_date),
                "vendeur": f_vendeur,
                "produit": f_produit,
                "categorie": f_categorie,
                "quantite": f_quantite,
                "prix_unitaire": f_prix,
                "total": f_quantite * f_prix,
                "region": f_region,
                "canal": f_canal,
                "statut": f_statut,
                "client": f_client or "—",
                "remarques": f_remarques,
            }
            st.session_state["pending_record"] = record
            st.session_state["show_payment"] = True

# ============================================================
# MODULE PAIEMENT — 4 moyens : Orange Money, MTN MoMo, Carte, Chèque
# ============================================================
import time, random, string

def gen_ref(prefix):
    return prefix + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

def recap_montant(record, montant, border_color):
    st.markdown(f"""
    <div style='background:#1c1c28; border:1px solid {border_color}; border-radius:12px;
                padding:1.2rem; margin-bottom:1.2rem;'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <div style='color:#8888aa; font-size:0.68rem; letter-spacing:1px; text-transform:uppercase;'>
                    Montant à payer</div>
                <div style='color:{border_color}; font-family:Syne,sans-serif; font-weight:800; font-size:1.8rem;'>
                    {fmt_fcfa(montant)}</div>
            </div>
            <div style='text-align:right;'>
                <div style='color:#8888aa; font-size:0.68rem; letter-spacing:1px; text-transform:uppercase;'>Produit</div>
                <div style='color:#e8e8f0; font-size:0.9rem; font-weight:600;'>{record["produit"]}</div>
                <div style='color:#8888aa; font-size:0.75rem;'>
                    {record["quantite"]} unité(s) × {fmt_fcfa(record["prix_unitaire"])}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def confirmation_box(montant, ref, couleurs, detail):
    c1, c2 = couleurs
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,{c1},{c2}); border-radius:16px; padding:2rem;
                text-align:center; margin:1rem 0; box-shadow:0 8px 32px rgba(0,0,0,0.3);'>
        <div style='font-size:3rem; margin-bottom:0.5rem;'>✅</div>
        <div style='color:white; font-family:Syne,sans-serif; font-weight:800; font-size:1.5rem; margin-bottom:0.5rem;'>
            Paiement Réussi !</div>
        <div style='color:rgba(255,255,255,0.9); font-size:0.9rem; margin-bottom:1rem;'>
            {fmt_fcfa(montant)} — {detail}</div>
        <div style='background:rgba(255,255,255,0.2); border-radius:8px; padding:0.6rem 1.2rem; display:inline-block;'>
            <span style='color:white; font-size:0.8rem; letter-spacing:1px;'>
                Référence : <strong>{ref}</strong></span>
        </div>
        <div style='color:rgba(255,255,255,0.7); font-size:0.72rem; margin-top:0.8rem;'>📲 Confirmation envoyée</div>
    </div>
    """, unsafe_allow_html=True)

def annuler_paiement():
    st.session_state["show_payment"] = False
    st.session_state["pending_record"] = None
    st.rerun()

def finaliser(record, remarque, ref, couleurs, detail):
    record["statut"] = "Complétée"
    record["remarques"] = remarque
    save_record(record)
    st.session_state["show_payment"] = False
    st.session_state["pending_record"] = None
    confirmation_box(record["total"], ref, couleurs, detail)
    st.balloons()

if st.session_state.get("show_payment") and st.session_state.get("pending_record"):
    record = st.session_state["pending_record"]
    montant = record["total"]

    st.markdown("""
    <div style='margin:1.5rem 0 1rem;'>
        <div style='color:#8888aa; font-size:0.68rem; letter-spacing:2px;
                    text-transform:uppercase; margin-bottom:8px;'>Choisissez votre moyen de paiement</div>
        <h2 style='font-size:1.5rem; letter-spacing:-0.5px; margin:0;'>
            💳 Paiement <span style='color:#f0c040;'>sécurisé</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Sélecteur 4 modes
    mode_paiement = st.radio(
        "",
        ["🟠 Orange Money", "🟡 MTN Mobile Money", "💳 Carte bancaire", "📝 Chèque bancaire"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.divider()

    # ═══════════════════════════════
    # 1. ORANGE MONEY
    # ═══════════════════════════════
    if mode_paiement == "🟠 Orange Money":
        st.markdown("""
        <div style='background:linear-gradient(135deg,#ff6600,#ff8c00); border-radius:14px;
                    padding:1.2rem 1.5rem; margin-bottom:1.2rem; box-shadow:0 6px 24px rgba(255,102,0,0.25);
                    display:flex; align-items:center; gap:12px;'>
            <div style='background:white; border-radius:50%; width:44px; height:44px;
                        display:flex; align-items:center; justify-content:center; font-size:1.4rem;'>🟠</div>
            <div>
                <div style='color:white; font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem;'>Orange Money</div>
                <div style='color:rgba(255,255,255,0.8); font-size:0.7rem; letter-spacing:1px;'>Paiement mobile sécurisé — Cameroun</div>
            </div>
        </div>""", unsafe_allow_html=True)

        recap_montant(record, montant, "#ff6600")
        with st.form("form_om"):
            col1, col2 = st.columns(2)
            with col1: om_num = st.text_input("📱 Numéro Orange Money *", placeholder="6XX XX XX XX", max_chars=12)
            with col2: om_nom = st.text_input("👤 Nom du titulaire *", placeholder="Nom complet")
            om_pin = st.text_input("🔐 Code PIN *", type="password", placeholder="••••••", max_chars=6)
            st.markdown("<div style='background:rgba(255,102,0,0.08);border:1px solid rgba(255,102,0,0.2);border-radius:8px;padding:0.8rem;font-size:0.75rem;color:#8888aa;'>🔒 Sécurisé · Confirmation SMS après paiement</div>", unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca: ann = st.form_submit_button("✕ Annuler", use_container_width=True)
            with cb: pay = st.form_submit_button("🟠 Payer", use_container_width=True)
        if ann: annuler_paiement()
        if pay:
            if not om_num or not om_nom or not om_pin: st.error("⚠️ Remplissez tous les champs.")
            elif not om_num.replace(" ","").isdigit(): st.error("⚠️ Numéro invalide.")
            elif len(om_pin) < 4: st.error("⚠️ PIN trop court.")
            else:
                with st.spinner("🟠 Connexion Orange Money…"): time.sleep(1.5)
                with st.spinner("🔐 Vérification…"): time.sleep(1.5)
                with st.spinner("💸 Traitement…"): time.sleep(2)
                ref = gen_ref("OM-")
                finaliser(record, f"Orange Money {om_num} — Réf: {ref}", ref, ("#ff6600","#ff8c00"), f"Orange Money · {om_num}")

    # ═══════════════════════════════
    # 2. MTN MOBILE MONEY
    # ═══════════════════════════════
    elif mode_paiement == "🟡 MTN Mobile Money":
        st.markdown("""
        <div style='background:linear-gradient(135deg,#ffcc00,#ff9900); border-radius:14px;
                    padding:1.2rem 1.5rem; margin-bottom:1.2rem; box-shadow:0 6px 24px rgba(255,204,0,0.25);
                    display:flex; align-items:center; gap:12px;'>
            <div style='background:white; border-radius:50%; width:44px; height:44px;
                        display:flex; align-items:center; justify-content:center; font-size:1.4rem;'>🟡</div>
            <div>
                <div style='color:#0a0a0f; font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem;'>MTN Mobile Money</div>
                <div style='color:rgba(0,0,0,0.6); font-size:0.7rem; letter-spacing:1px;'>MoMo · Paiement mobile sécurisé — Cameroun</div>
            </div>
        </div>""", unsafe_allow_html=True)

        recap_montant(record, montant, "#ffcc00")
        with st.form("form_mtn"):
            col1, col2 = st.columns(2)
            with col1: mtn_num = st.text_input("📱 Numéro MTN MoMo *", placeholder="6XX XX XX XX", max_chars=12)
            with col2: mtn_nom = st.text_input("👤 Nom du titulaire *", placeholder="Nom complet")
            mtn_pin = st.text_input("🔐 Code PIN MoMo *", type="password", placeholder="••••••", max_chars=6)
            st.markdown("<div style='background:rgba(255,204,0,0.08);border:1px solid rgba(255,204,0,0.2);border-radius:8px;padding:0.8rem;font-size:0.75rem;color:#8888aa;'>🔒 Sécurisé · Confirmation SMS après paiement</div>", unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca: ann = st.form_submit_button("✕ Annuler", use_container_width=True)
            with cb: pay = st.form_submit_button("🟡 Payer via MoMo", use_container_width=True)
        if ann: annuler_paiement()
        if pay:
            if not mtn_num or not mtn_nom or not mtn_pin: st.error("⚠️ Remplissez tous les champs.")
            elif not mtn_num.replace(" ","").isdigit(): st.error("⚠️ Numéro invalide.")
            elif len(mtn_pin) < 4: st.error("⚠️ PIN trop court.")
            else:
                with st.spinner("🟡 Connexion MTN MoMo…"): time.sleep(1.5)
                with st.spinner("🔐 Vérification du compte…"): time.sleep(1.5)
                with st.spinner("💸 Débit en cours…"): time.sleep(2)
                ref = gen_ref("MTN-")
                finaliser(record, f"MTN MoMo {mtn_num} — Réf: {ref}", ref, ("#ffcc00","#ff9900"), f"MTN MoMo · {mtn_num}")

    # ═══════════════════════════════
    # 3. CARTE BANCAIRE
    # ═══════════════════════════════
    elif mode_paiement == "💳 Carte bancaire":
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a3e,#2d2d6b); border-radius:14px;
                    padding:1.2rem 1.5rem; margin-bottom:1.2rem; box-shadow:0 6px 24px rgba(26,26,62,0.4);
                    display:flex; align-items:center; gap:12px;'>
            <div style='background:white; border-radius:8px; width:52px; height:34px;
                        display:flex; align-items:center; justify-content:center; font-size:1.2rem;'>💳</div>
            <div>
                <div style='color:white; font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem;'>Carte Bancaire</div>
                <div style='color:rgba(255,255,255,0.7); font-size:0.7rem; letter-spacing:1px;'>Visa · Mastercard · 3D Secure</div>
            </div>
        </div>""", unsafe_allow_html=True)

        recap_montant(record, montant, "#a78bfa")

        st.markdown("""
        <div style='background:linear-gradient(135deg,#1c1c28,#2a2a3d); border:1px solid #a78bfa;
                    border-radius:16px; padding:1.5rem; margin-bottom:1.2rem;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:1.2rem;'>
                <span style='color:#a78bfa; font-weight:700; font-size:0.9rem; letter-spacing:2px;'>VENTABANK</span>
                <span style='font-size:1.1rem;'>💳</span>
            </div>
            <div style='color:#e8e8f0; font-size:1rem; letter-spacing:5px; margin-bottom:1.2rem;'>
                •••• •••• •••• ••••</div>
            <div style='display:flex; justify-content:space-between; font-size:0.75rem;'>
                <div><div style='color:#55556a; font-size:0.6rem;'>TITULAIRE</div>
                     <div style='color:#e8e8f0;'>VOTRE NOM</div></div>
                <div><div style='color:#55556a; font-size:0.6rem;'>EXPIRE</div>
                     <div style='color:#e8e8f0;'>MM/AA</div></div>
                <div style='color:#a78bfa; font-weight:700;'>VISA</div>
            </div>
        </div>""", unsafe_allow_html=True)

        with st.form("form_carte"):
            col1, col2 = st.columns(2)
            with col1: c_nom = st.text_input("👤 Nom sur la carte *", placeholder="NOM PRÉNOM")
            with col2: c_num = st.text_input("💳 Numéro *", placeholder="1234 5678 9012 3456", max_chars=19)
            col3, col4, col5 = st.columns(3)
            with col3: c_mois = st.selectbox("📅 Mois *", [f"{i:02d}" for i in range(1,13)])
            with col4: c_annee = st.selectbox("📅 Année *", [str(y) for y in range(2025,2032)])
            with col5: c_cvv = st.text_input("🔐 CVV *", type="password", placeholder="•••", max_chars=3)
            c_type = st.selectbox("🏦 Réseau", ["Visa", "Mastercard"])
            st.markdown("<div style='background:rgba(167,139,250,0.08);border:1px solid rgba(167,139,250,0.2);border-radius:8px;padding:0.8rem;font-size:0.75rem;color:#8888aa;'>🔒 3D Secure · SSL · Aucune donnée stockée</div>", unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca: ann = st.form_submit_button("✕ Annuler", use_container_width=True)
            with cb: pay = st.form_submit_button("💳 Payer maintenant", use_container_width=True)
        if ann: annuler_paiement()
        if pay:
            num_clean = c_num.replace(" ","").replace("-","")
            if not c_nom or not c_num or not c_cvv: st.error("⚠️ Remplissez tous les champs.")
            elif len(num_clean) != 16 or not num_clean.isdigit(): st.error("⚠️ Numéro de carte invalide (16 chiffres).")
            elif len(c_cvv) != 3 or not c_cvv.isdigit(): st.error("⚠️ CVV invalide (3 chiffres).")
            else:
                with st.spinner("💳 Connexion au terminal…"): time.sleep(1.5)
                with st.spinner("🔐 Authentification 3D Secure…"): time.sleep(2)
                with st.spinner("✅ Autorisation bancaire…"): time.sleep(1.5)
                ref = gen_ref("CB-")
                finaliser(record, f"Carte {c_type} •••• {num_clean[-4:]} — Réf: {ref}", ref, ("#1a1a3e","#4c4ca0"), f"Carte {c_type} •••• {num_clean[-4:]}")

    # ═══════════════════════════════
    # 4. CHÈQUE BANCAIRE
    # ═══════════════════════════════
    elif mode_paiement == "📝 Chèque bancaire":
        st.markdown("""
        <div style='background:linear-gradient(135deg,#2d4a2d,#3d6b3d); border-radius:14px;
                    padding:1.2rem 1.5rem; margin-bottom:1.2rem; box-shadow:0 6px 24px rgba(45,74,45,0.4);
                    display:flex; align-items:center; gap:12px;'>
            <div style='background:white; border-radius:8px; width:44px; height:44px;
                        display:flex; align-items:center; justify-content:center; font-size:1.4rem;'>📝</div>
            <div>
                <div style='color:white; font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem;'>Chèque Bancaire</div>
                <div style='color:rgba(255,255,255,0.7); font-size:0.7rem; letter-spacing:1px;'>Paiement par chèque certifié</div>
            </div>
        </div>""", unsafe_allow_html=True)

        recap_montant(record, montant, "#4ecdc4")

        # Aperçu chèque visuel
        st.markdown(f"""
        <div style='background:#fffef0; border:2px solid #d4c060; border-radius:12px;
                    padding:1.5rem; margin-bottom:1.2rem; color:#333; font-family:serif;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:1rem;'>
                <div style='font-size:0.7rem; color:#666;'>CHÈQUE BANCAIRE</div>
                <div style='font-size:0.7rem; color:#666;'>N° ___________</div>
            </div>
            <div style='margin-bottom:0.8rem;'>
                <span style='font-size:0.72rem; color:#888;'>Payez contre ce chèque la somme de : </span>
                <span style='font-weight:700; color:#333; font-size:0.85rem;'>{fmt_fcfa(montant)}</span>
            </div>
            <div style='border-top:1px dashed #ccc; margin:0.8rem 0; padding-top:0.8rem;'>
                <div style='font-size:0.7rem; color:#888;'>À l'ordre de : <strong>VentaScope Commerce</strong></div>
            </div>
            <div style='display:flex; justify-content:space-between; margin-top:1rem;'>
                <div style='font-size:0.7rem; color:#888;'>Date : __________</div>
                <div style='font-size:0.7rem; color:#888;'>Signature : _________________</div>
            </div>
        </div>""", unsafe_allow_html=True)

        with st.form("form_cheque"):
            col1, col2 = st.columns(2)
            with col1: ch_num = st.text_input("📋 Numéro du chèque *", placeholder="Ex: 0012345678")
            with col2: ch_banque = st.text_input("🏦 Banque émettrice *", placeholder="Ex: BICEC, Afriland, SCB…")
            col3, col4 = st.columns(2)
            with col3: ch_titulaire = st.text_input("👤 Nom du titulaire *", placeholder="Nom complet")
            with col4: ch_date = st.date_input("📅 Date du chèque *", value=date.today())
            ch_montant = st.number_input("💰 Montant inscrit sur le chèque (FCFA) *", min_value=0, value=int(montant), step=1000)
            st.markdown("<div style='background:rgba(78,205,196,0.08);border:1px solid rgba(78,205,196,0.2);border-radius:8px;padding:0.8rem;font-size:0.75rem;color:#8888aa;line-height:1.6;'>⚠️ Le chèque sera vérifié avant validation définitive · Délai de compensation : 2-3 jours ouvrables</div>", unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca: ann = st.form_submit_button("✕ Annuler", use_container_width=True)
            with cb: pay = st.form_submit_button("📝 Valider le chèque", use_container_width=True)
        if ann: annuler_paiement()
        if pay:
            if not ch_num or not ch_banque or not ch_titulaire: st.error("⚠️ Remplissez tous les champs.")
            elif ch_montant != int(montant): st.error(f"⚠️ Le montant du chèque doit être {fmt_fcfa(montant)}.")
            else:
                with st.spinner("📝 Enregistrement du chèque…"): time.sleep(1.5)
                with st.spinner("🏦 Vérification bancaire…"): time.sleep(2)
                ref = gen_ref("CHQ-")
                record["statut"] = "En attente"
                record["remarques"] = f"Chèque N°{ch_num} — {ch_banque} — Réf: {ref}"
                save_record(record)
                st.session_state["show_payment"] = False
                st.session_state["pending_record"] = None
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#2d4a2d,#4ecdc4); border-radius:16px;
                            padding:2rem; text-align:center; margin:1rem 0;'>
                    <div style='font-size:3rem; margin-bottom:0.5rem;'>📝</div>
                    <div style='color:white; font-family:Syne,sans-serif; font-weight:800; font-size:1.3rem; margin-bottom:0.5rem;'>
                        Chèque Enregistré !</div>
                    <div style='color:rgba(255,255,255,0.9); font-size:0.85rem; margin-bottom:1rem;'>
                        Chèque N°{ch_num} · {ch_banque} · {fmt_fcfa(montant)}</div>
                    <div style='background:rgba(255,255,255,0.2); border-radius:8px; padding:0.6rem 1.2rem; display:inline-block;'>
                        <span style='color:white; font-size:0.8rem;'>Référence : <strong>{ref}</strong></span>
                    </div>
                    <div style='color:rgba(255,255,255,0.7); font-size:0.72rem; margin-top:0.8rem;'>
                        ⏳ Statut "En attente" jusqu'à compensation bancaire (2-3 jours)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()

# ============================================================
# PAGE 2 — BASE DE DONNÉES
# ============================================================
elif page == "📋 Base de données":

    st.markdown("""
    <h1 style='font-size:2.2rem; letter-spacing:-1px; margin-bottom:4px;'>
        Base de <span style='color:#f0c040; font-style:italic;'>données</span>
    </h1>
    <p style='color:#8888aa; font-size:0.85rem; margin-bottom:2rem;'>Toutes les transactions enregistrées</p>
    """, unsafe_allow_html=True)

    df = get_df()

    # Filtres
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Rechercher", placeholder="Vendeur, produit…")
    with col2:
        cat_filter = st.multiselect("Catégorie", df["categorie"].unique().tolist())
    with col3:
        statut_filter = st.multiselect("Statut", df["statut"].unique().tolist())

    # Appliquer filtres
    filtered = df.copy()
    if search:
        mask = filtered.apply(lambda row: search.lower() in str(row).lower(), axis=1)
        filtered = filtered[mask]
    if cat_filter:
        filtered = filtered[filtered["categorie"].isin(cat_filter)]
    if statut_filter:
        filtered = filtered[filtered["statut"].isin(statut_filter)]

    st.markdown(f"<div style='color:#55556a; font-size:0.78rem; margin-bottom:1rem;'>{len(filtered)} résultat(s) trouvé(s)</div>", unsafe_allow_html=True)

    # Tableau
    if filtered.empty:
        st.info("Aucune donnée trouvée. Modifiez les filtres ou saisissez des données.")
    else:
        display_cols = ["date", "vendeur", "produit", "categorie", "quantite", "prix_unitaire", "total", "region", "canal", "statut", "client"]
        st.dataframe(
            filtered[display_cols].rename(columns={
                "date": "Date", "vendeur": "Vendeur", "produit": "Produit",
                "categorie": "Catégorie", "quantite": "Qté",
                "prix_unitaire": "P.U (FCFA)", "total": "Total (FCFA)",
                "region": "Région", "canal": "Canal", "statut": "Statut", "client": "Client"
            }),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # Export
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Export CSV", csv, "ventes_data.csv", "text/csv", use_container_width=True)
    with col_e2:
        json_str = filtered.to_json(orient="records", force_ascii=False, indent=2)
        st.download_button("⬇ Export JSON", json_str, "ventes_data.json", "application/json", use_container_width=True)
    with col_e3:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            filtered.to_excel(writer, index=False, sheet_name="Ventes")
        st.download_button("⬇ Export Excel", buffer.getvalue(), "ventes_data.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    # Supprimer toutes les données
    st.divider()
    if st.button("🗑️ Réinitialiser les données", type="secondary"):
        st.session_state.data = pd.DataFrame(columns=df.columns)
        st.rerun()

# ============================================================
# PAGE 3 — ANALYSE DESCRIPTIVE
# ============================================================
elif page == "📊 Analyse descriptive":

    st.markdown("""
    <h1 style='font-size:2.2rem; letter-spacing:-1px; margin-bottom:4px;'>
        Analyse <span style='color:#f0c040; font-style:italic;'>descriptive</span>
    </h1>
    <p style='color:#8888aa; font-size:0.85rem; margin-bottom:2rem;'>
        Statistiques et visualisations automatiques — Commerce & Ventes
    </p>
    """, unsafe_allow_html=True)

    df = get_df()

    if df.empty:
        st.warning("Aucune donnée disponible. Commencez par saisir des ventes.")
        st.stop()

    df_valid = df[df["statut"] != "Annulée"]

    # ---- KPIs ----
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Total ventes", len(df), help="Nombre total de transactions")
    with col2:
        st.metric("💰 Chiffre d'affaires", fmt_fcfa(df_valid["total"].sum()), help="CA hors annulées")
    with col3:
        st.metric("📈 Vente moyenne", fmt_fcfa(df_valid["total"].mean()), help="Moyenne par transaction")
    with col4:
        st.metric("🏆 Vente maximale", fmt_fcfa(df_valid["total"].max()), help="Transaction la plus élevée")

    st.divider()

    # ---- GRAPHIQUES ----
    tab1, tab2, tab3 = st.tabs(["📊 Graphiques", "📐 Statistiques", "🔎 Corrélations"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Camembert catégories
            cat_data = df.groupby("categorie")["total"].sum().reset_index()
            fig1 = px.pie(cat_data, names="categorie", values="total",
                          title="Ventes par catégorie",
                          color_discrete_sequence=["#f0c040","#e05c3a","#4ecdc4","#a78bfa","#fb923c","#34d399","#f472b6"])
            fig1.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0", showlegend=True)
            fig1.update_traces(textfont_color="#0a0a0f")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Barres régions
            reg_data = df.groupby("region")["total"].sum().reset_index().sort_values("total", ascending=True)
            fig2 = px.bar(reg_data, x="total", y="region", orientation="h",
                          title="CA par région (FCFA)",
                          color="total", color_continuous_scale=["#1c1c28","#f0c040"])
            fig2.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0", coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)

        # Évolution temporelle
        time_data = df_valid.groupby("date")["total"].sum().reset_index().sort_values("date")
        fig3 = px.area(time_data, x="date", y="total",
                       title="Évolution du chiffre d'affaires dans le temps",
                       color_discrete_sequence=["#f0c040"])
        fig3.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
        fig3.update_traces(line_width=2, fillcolor="rgba(240,192,64,0.15)")
        st.plotly_chart(fig3, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            # Canal de vente
            canal_data = df["canal"].value_counts().reset_index()
            canal_data.columns = ["canal", "count"]
            fig4 = px.pie(canal_data, names="canal", values="count",
                          title="Répartition par canal de vente", hole=0.4,
                          color_discrete_sequence=["#f0c040","#e05c3a","#4ecdc4","#a78bfa"])
            fig4.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
            st.plotly_chart(fig4, use_container_width=True)

        with col4:
            # Statuts
            statut_data = df["statut"].value_counts().reset_index()
            statut_data.columns = ["statut", "count"]
            colors = {"Complétée": "#4ecdc4", "En attente": "#f0c040", "Annulée": "#e05c3a"}
            fig5 = px.bar(statut_data, x="statut", y="count",
                          title="Distribution des statuts",
                          color="statut",
                          color_discrete_map=colors)
            fig5.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0", showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)

        # Top vendeurs
        vendeur_data = df.groupby("vendeur")["total"].sum().reset_index().sort_values("total", ascending=False)
        fig6 = px.bar(vendeur_data, x="vendeur", y="total",
                      title="Performance des vendeurs (CA total FCFA)",
                      color="total", color_continuous_scale=["#1c1c28","#e05c3a","#f0c040"])
        fig6.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0", coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    with tab2:
        st.markdown("<h3 style='margin-bottom:1rem;'>Statistiques descriptives</h3>", unsafe_allow_html=True)

        numeric_cols = ["prix_unitaire", "quantite", "total"]
        labels = {"prix_unitaire": "Prix unitaire (FCFA)", "quantite": "Quantité", "total": "Montant total (FCFA)"}

        stats_rows = []
        for col in numeric_cols:
            s = df[col]
            stats_rows.append({
                "Variable": labels[col],
                "N": len(s),
                "Minimum": f"{s.min():,.0f}",
                "Maximum": f"{s.max():,.0f}",
                "Somme": f"{s.sum():,.0f}",
                "Moyenne (μ)": f"{s.mean():,.2f}",
                "Médiane": f"{s.median():,.2f}",
                "Écart-type (σ)": f"{s.std():,.2f}",
                "Q1 (25%)": f"{s.quantile(0.25):,.2f}",
                "Q3 (75%)": f"{s.quantile(0.75):,.2f}",
                "Variance": f"{s.var():,.2f}",
                "Asymétrie": f"{s.skew():,.3f}",
                "Kurtosis": f"{s.kurtosis():,.3f}",
            })

        stats_df = pd.DataFrame(stats_rows).set_index("Variable")
        st.dataframe(stats_df, use_container_width=True)

        st.divider()

        # Distribution prix
        st.markdown("<h3>Distribution des montants</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(df, x="total", nbins=15,
                                    title="Histogramme des montants totaux",
                                    color_discrete_sequence=["#f0c040"])
            fig_hist.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            fig_box = px.box(df, y="total", x="categorie",
                             title="Boîte à moustaches par catégorie",
                             color="categorie",
                             color_discrete_sequence=["#f0c040","#e05c3a","#4ecdc4","#a78bfa","#fb923c","#34d399","#f472b6"])
            fig_box.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0", showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

    with tab3:
        st.markdown("<h3 style='margin-bottom:1rem;'>Analyse des corrélations</h3>", unsafe_allow_html=True)

        corr = df[["prix_unitaire", "quantite", "total"]].corr()
        fig_corr = px.imshow(corr,
                             text_auto=True,
                             title="Matrice de corrélation",
                             color_continuous_scale=["#e05c3a", "#13131a", "#f0c040"],
                             zmin=-1, zmax=1)
        fig_corr.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
        st.plotly_chart(fig_corr, use_container_width=True)

        # Scatter
        col1, col2 = st.columns(2)
        with col1:
            fig_sc1 = px.scatter(df, x="prix_unitaire", y="total",
                                 color="categorie", size="quantite",
                                 title="Prix unitaire vs Montant total",
                                 color_discrete_sequence=["#f0c040","#e05c3a","#4ecdc4","#a78bfa","#fb923c","#34d399","#f472b6"])
            fig_sc1.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
            st.plotly_chart(fig_sc1, use_container_width=True)
        with col2:
            fig_sc2 = px.scatter(df, x="quantite", y="total",
                                 color="statut", size="prix_unitaire",
                                 title="Quantité vs Montant total",
                                 color_discrete_map={"Complétée":"#4ecdc4","En attente":"#f0c040","Annulée":"#e05c3a"})
            fig_sc2.update_layout(**PLOTLY_THEME, title_font_color="#e8e8f0")
            st.plotly_chart(fig_sc2, use_container_width=True)
