import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(
    page_title="ASSOS NDAYANE VILLAGE - Tableau de Bord", 
    page_icon="🇸🇳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS PERSONNALISÉ (DESIGN PREMIUM AUX COULEURS DU SÉNÉGAL)
st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* Masquer les éléments techniques Streamlit/GitHub */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    footer { visibility: hidden; }
    
    /* Police globale et fond doux */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background-color: #F4F7F5;
    }
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 1150px;
    }

    /* BANNIÈRE D'EN-TÊTE OFFICIELLE */
    .hero-banner {
        background: linear-gradient(135deg, #006B35 0%, #008543 60%, #00A854 100%);
        padding: 30px 20px;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 25px rgba(0, 133, 67, 0.2);
        border-bottom: 5px solid #FDEF42;
        margin-bottom: 25px;
    }
    .hero-flag {
        font-size: 58px;
        margin-bottom: 5px;
        display: inline-block;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 0;
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .hero-subtitle {
        font-size: 15px;
        font-weight: 500;
        color: #FDEF42;
        margin-top: 6px;
        letter-spacing: 0.5px;
    }
    .hero-location {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.15);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        margin-top: 10px;
        color: #FFFFFF;
    }

    /* ENCADRÉ RÈGLES DU COMITÉ DES SAGES */
    .sages-card {
        background: #FFFFFF;
        border-left: 6px solid #F2B705;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    .sages-title {
        color: #1E293B;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .sages-list {
        margin: 0;
        padding-left: 20px;
        color: #475569;
        font-size: 14px;
        line-height: 1.8;
    }
    .badge-warn {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-danger {
        background-color: #FEE2E2;
        color: #B91C1C;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 12px;
    }

    /* CONTENEUR DE FILTRES */
    .filter-header {
        color: #008543;
        font-size: 18px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* CARTES KPI (INDICATEURS CLÉS) */
    .kpi-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        text-align: center;
        border-top: 5px solid #008543;
        transition: transform 0.2s ease;
        margin-bottom: 12px;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
    }
    .kpi-icon {
        font-size: 26px;
        margin-bottom: 6px;
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin: 6px 0;
    }
    .kpi-sub {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }

    /* CARTES DES ENVELOPPES FINANCIÈRES */
    .env-card {
        background: #FFFFFF;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 12px;
    }
    .env-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .env-name {
        font-weight: 700;
        font-size: 15px;
        color: #1E293B;
    }
    .env-pct {
        background-color: #E6F4EA;
        color: #008543;
        font-weight: 700;
        font-size: 13px;
        padding: 3px 10px;
        border-radius: 20px;
    }
    .env-amount {
        font-size: 28px;
        font-weight: 800;
        color: #008543;
        margin: 8px 0;
    }
    .env-desc {
        font-size: 12.5px;
        color: #64748B;
    }

    /* TITRES DE SECTIONS */
    .section-title {
        color: #1E293B;
        font-size: 20px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BANNIÈRE D'EN-TÊTE
st.markdown("""
    <div class='hero-banner'>
        <div class='hero-flag'>🇸🇳</div>
        <h1 class='hero-title'>ASSOS NDAYANE VILLAGE</h1>
        <div class='hero-subtitle'>Tableau de Bord Officiel & Transparence Financière</div>
        <div class='hero-location'>📍 Commune de Tocky Gare • Département de Diourbel</div>
    </div>
""", unsafe_allow_html=True)

# 4. CHARGEMENT ET TRAITEMENT DES DONNÉES
try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    
    # Nettoyage des colonnes
    df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip()
    df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip()
    df['Mode paiement'] = df['Mode paiement'].fillna('En attente').astype(str).str.strip()
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    
    df['Nom'] = df['Nom'].fillna('').astype(str).str.strip()
    df['Prénom'] = df['Prénom'].fillna('').astype(str).str.strip()
    df['Nom Complet'] = df['Nom'] + " " + df['Prénom']
    df = df[df['Nom Complet'].str.len() > 2]

    # --- BLOC 1 : RÈGLES DU COMITÉ DES SAGES (AU-DESSUS) ---
    st.markdown("""
        <div class='sages-card'>
            <div class='sages-title'>📜 Charte & Règles du Comité des Sages</div>
            <ul class='sages-list'>
                <li><b>Frais d'adhésion :</b> 1 000 FCFA (pour tout nouveau membre)</li>
                <li><b>Intervention sociale :</b> <b>25 000 FCFA</b> par cas <i>(Hospitalisation, Accident grave/fracture, Sinistres naturels : incendie, inondation, orage)</i></li>
                <li><b>Cas de décès :</b> <span class='badge-warn'>Exclu</span> <i>(En attente d'un arbitrage de l'Assemblée Générale)</i></li>
                <li><b>Discipline & Arriérés :</b> 3 mois de retard = <span class='badge-warn'>Avertissement</span> • Au-delà de 6 mois = <span class='badge-danger'>Radiation définitive</span></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # --- BLOC 2 : FILTRES DU TABLEAU DE BORD (EN DESSOUS) ---
    st.markdown("<div class='filter-header'>🔍 Filtrer les données du village</div>", unsafe_allow_html=True)
    liste_mois = ["Tous les mois"] + list(df['Date'].unique())
    mois_choisi = st.selectbox("📅 Période (Mois) :", liste_mois)
    
    liste_residence = ["Toutes les résidences"] + sorted(list(df['Résidence'].unique()))
    residence_choisie = st.selectbox("🏘️ Quartier / Résidence :", liste_residence)

    # Application des filtres
    df_filtre = df.copy()
    if mois_choisi != "Tous les mois":
        df_filtre = df_filtre[df_filtre['Date'] == mois_choisi]
    if residence_choisie != "Toutes les résidences":
        df_filtre = df_filtre[df_filtre['Résidence'] == residence_choisie]

    # --- CALCULS DES INDICATEURS CLÉS (KPI) ---
    total_collecte = int(df_filtre['Montant FCFA'].sum())
    membres_total = len(df_filtre)
    membres_cotisants = int((df_filtre['Montant FCFA'] >= 1000).sum())
    membres_retard = membres_total - membres_cotisants
    montant_attendu = membres_total * 1000
    reste_a_recouvrer = max(0, montant_attendu - total_collecte)
    taux_recouvrement = int((membres_cotisants / membres_total * 100)) if membres_total > 0 else 0

    # --- SECTION 1 : VUE D'ENSEMBLE DE LA TRÉSORERIE ---
    st.markdown(f"<div class='section-title'>📈 Situation Financière ({mois_choisi} • {residence_choisie})</div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class='kpi-card' style='border-top-color:#008543;'>
                <div class='kpi-icon'>💰</div>
                <div class='kpi-title'>Total Collecté</div>
                <div class='kpi-value' style='color:#008543;'>{total_collecte:,} F</div>
                <div class='kpi-sub'>Sur {montant_attendu:,} F attendus</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class='kpi-card' style='border-top-color:#E31B23;'>
                <div class='kpi-icon'>⏳</div>
                <div class='kpi-title'>Reste à Recouvrer</div>
                <div class='kpi-value' style='color:#E31B23;'>{reste_a_recouvrer:,} F</div>
                <div class='kpi-sub'>{membres_retard} membre(s) en attente</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class='kpi-card' style='border-top-color:#F2B705;'>
                <div class='kpi-icon'>📊</div>
                <div class='kpi-title'>Participation</div>
