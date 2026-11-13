import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASSOS NDAYANE VILLAGE", page_icon="🇸🇳", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://googleapis.com');
[data-testid="stHeader"], [data-testid="collapsedControl"], footer { display: none !important; }
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background-color: #F4F7F5; }
.block-container { padding-top: 1.5rem !important; max-width: 1150px; }

.hero-banner {
    background: linear-gradient(135deg, #006B35 0%, #008543 60%, #00A854 100%);
    padding: 25px 20px; border-radius: 16px; text-align: center; color: white;
    box-shadow: 0 8px 20px rgba(0, 133, 67, 0.2); border-bottom: 5px solid #FDEF42; margin-bottom: 20px;
}
.hero-flag { font-size: 55px; margin-bottom: 5px; display: inline-block; }
.hero-title { font-size: 32px; font-weight: 800; letter-spacing: 1.5px; margin: 0; color: #FFFFFF; }
.hero-subtitle { font-size: 15px; font-weight: 500; color: #FDEF42; margin-top: 5px; }
.hero-location { display: inline-block; background-color: rgba(255,255,255,0.15); padding: 4px 14px; border-radius: 20px; font-size: 12px; margin-top: 8px; }

.sages-card { background: #FFFFFF; border-left: 6px solid #F2B705; border-radius: 12px; padding: 18px 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 20px; }
.sages-title { color: #1E293B; font-size: 16px; font-weight: 700; margin-bottom: 10px; }
.sages-list { margin: 0; padding-left: 20px; color: #475569; font-size: 13.5px; line-height: 1.7; }
.badge-warn { background-color: #FEF3C7; color: #B45309; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }
.badge-danger { background-color: #FEE2E2; color: #B91C1C; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }

.kpi-card { background: #FFFFFF; padding: 18px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); text-align: center; border-top: 5px solid #008543; margin-bottom: 10px; }
.kpi-title { font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; }
.kpi-value { font-size: 25px; font-weight: 800; color: #0F172A; margin: 5px 0; }
.kpi-sub { font-size: 12px; color: #64748B; }

.env-card { background: #FFFFFF; padding: 20px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E2E8F0; margin-bottom: 10px; }
.env-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.env-name { font-weight: 700; font-size: 15px; color: #1E293B; }
.env-pct { background-color: #E6F4EA; color: #008543; font-weight: 700; font-size: 13px; padding: 3px 10px; border-radius: 20px; }
.env-amount { font-size: 26px; font-weight: 800; color: #008543; margin: 6px 0; }
.env-desc { font-size: 12px; color: #64748B; }
.section-title { color: #1E293B; font-size: 19px; font-weight: 700; margin-top: 22px; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 2px solid #E2E8F0; }
</style>

<div class='hero-banner'>
    <div class='hero-flag'>🇸🇳</div>
    <h1 class='hero-title'>ASSOS NDAYANE VILLAGE</h1>
    <div class='hero-subtitle'>Tableau de Bord Officiel & Transparence Financière</div>
    <div class='hero-location'>📍 Commune de Tocky Gare • Département de Diourbel</div>
</div>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip()
    df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip()
    df['Mode paiement'] = df['Mode paiement'].fillna('En attente').astype(str).str.strip()
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    df['Nom Complet'] = df['Nom'].fillna('').astype(str).str.strip() + " " + df['Prénom'].fillna('').astype(str).str.strip()
    df = df[df['Nom Complet'].str.len() > 2]

    # RÈGLES DU COMITÉ DES SAGES
    st.markdown("""
    <div class='sages-card'>
        <div class='sages-title'>📜 Charte & Règles du Comité des Sages</div>
        <ul class='sages-list'>
            <li><b>Frais d'adhésion :</b> 1 000 FCFA (pour tout nouveau membre)</li>
            <li><b>Intervention sociale :</b> <b>25 000 FCFA</b> par cas <i>(Hospitalisation, Accident grave/fracture, Sinistres naturels)</i></li>
            <li><b>Cas de décès :</b> <span class='badge-warn'>Exclu</span> <i>(En attente d'arbitrage de l'Assemblée Générale)</i></li>
            <li><b>Discipline :</b> 3 mois de retard = <span class='badge-warn'>Avertissement</span> • +6 mois = <span class='badge-danger'>Radiation définitive</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # FILTRES SUPERPOSÉS
    st.markdown("<div style='color:#008543; font-size:17px; font-weight:700; margin-bottom:8px;'>🔍 Filtrer les données du village</div>", unsafe_allow_html=True)
    mois_choisi = st.selectbox("📅 Période (Mois) :", ["Tous les mois"] + list(df['Date'].unique()))
    residence_choisie = st.selectbox("🏘️ Quartier / Résidence :", ["Toutes les résidences"] + sorted(list(df['Résidence'].unique())))

    df_filtre = df.copy()
    if mois_choisi != "Tous les mois":
        df_filtre = df_filtre[df_filtre['Date'] == mois_choisi]
    if residence_choisie != "Toutes les résidences":
        df_filtre = df_filtre[df_filtre['Résidence'] == residence_choisie]

    # INDICATEURS CLÉS (KPI)
    total_collecte = int(df_filtre['Montant FCFA'].sum())
    membres_total = len(df_filtre)
    membres_cotisants = int((df_filtre['Montant FCFA'] >= 1000).sum())
    membres_retard = membres_total - membres_cotisants
    montant_attendu = membres_total * 1000
    reste_a_recouvrer = max(0, montant_attendu - total_collecte)
    taux_recouvrement = int((membres_cotisants / membres_total * 100)) if membres_total > 0 else 0
    nb_interventions = int(total_collecte * 0.40) // 25000

    st.markdown(f"<div class='section-title'>📈 Situation Financière ({mois_choisi} • {residence_choisie})</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card' style='border-top-color:#008543;'><div class='kpi-title'>💰 Total Collecté</div><div class='kpi-value' style='color:#008543;'>{total_collecte:,} F</div><div class='kpi-sub'>Sur {montant_attendu:,} F attendus</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card' style='border-top-color:#E31B23;'><div class='kpi-title'>⏳ Reste à Recouvrer</div><div class='kpi-value' style='color:#E31B23;'>{reste_a_recouvrer:,} F</div><div class='kpi-sub'>{membres_retard} membre(s) en attente</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card' style='border-top-color:#F2B705;'><div class='kpi-title'>📊 Participation</div><div class='kpi-value' style='color:#B45309;'>{taux_recouvrement} %</div><div class='kpi-sub'>{membres_cotisants} / {membres_total} à jour</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card' style='border-top-color:#0284C7;'><div class='kpi-title'>🤝 Capacité Sociale</div><div class='kpi-value' style='color:#0284C7;'>{nb_interventions} cas</div><div class='kpi-sub'>Aides de 25 000 F possibles</div></div>", unsafe_allow_html=True)

    # RÉPARTITION DES ENVELOPPES
    st.markdown("<div class='section-title'>🏦 Répartition Automatique des Enveloppes</div>", unsafe_allow_html=True)
    fonds_dev = int(total_collecte * 0.60)
    fonds_sante = int(total_collecte * 0.25)
    fonds_sinistres = int(total_collecte * 0.15)

    f1, f2, f3 = st.columns(3)
    f1.markdown(f"<div class='env-card'><div class='env-header'><span class='env-name'>🏗️ Développement</span><span class='env-pct'>60 %</span></div><div class='env-amount'>{fonds_dev:,} FCFA</div><div class='env-desc'>Épargne bloquée (Projet Électricité)</div></div>", unsafe_allow_html=True)
    f2.markdown(f"<div class='env-card'><div class='env-header'><span class='env-name'>🩺 Santé & Accidents</span><span class='env-pct' style='background:#E0F2FE;color:#0284C7;'>25 %</span></div><div class='env-amount' style='color:#0284C7;'>{fonds_sante:,} FCFA</div><div class='env-desc'>Hospitalisation & fractures (25 000 F/cas)</div></div>", unsafe_allow_html=True)
    f3.markdown(f"<div class='env-card'><div class='env-header'><span class='env-name'>🌪️ Sinistres & Village</span><span class='env-pct' style='background:#FEF3C7;color:#B45309;'>15 %</span></div><div class='env-amount' style='color:#B45309;'>{fonds_sinistres:,} FCFA</div><div class='env-desc'>Incendie, inondation, orage, bien commun</div></div>", unsafe_allow_html=True)

    # GRAPHIQUES & STATUTS
    col_graph, col_statut = st.columns([1.15, 1])
    with col_graph:
        st.markdown("<div class='section-title'>🏘️ Collecte par Résidence (FCFA)</div>", unsafe_allow_html=True)
        st.bar_chart(df_filtre.groupby('Résidence')['Montant FCFA'].sum().sort_values(ascending=False), color="#008543")

    with col_statut:
        st.markdown("<div class='section-title'>⚖️ Discipline & Statuts (Sages)</div>", unsafe_allow_html=True)
        df_hist = df.copy()
        df_hist['Impaye'] = (df_hist['Montant FCFA'] < 1000).astype(int)
        suivi = df_hist.groupby(['Nom Complet', 'Résidence'])['Impaye'].sum().reset_index()
        suivi['Statut'] = suivi['Impaye'].apply(lambda x: "🔴 Radié (+6 mois)" if x >= 6 else ("🟠 Avertissement (3-5 mois)" if x >= 3 else (f"🟡 En retard ({x} mois)" if x > 0 else "🟢 À jour")))
        if residence_choisie != "Toutes les résidences":
            suivi = suivi[suivi['Résidence'] == residence_choisie]
        st.dataframe(suivi[['Nom Complet', 'Résidence', 'Statut']], use_container_width=True, height=310)

    # REGISTRE DÉTAILLÉ
    st.markdown("<div class='section-title'>📋 Registre Détaillé des Transactions</div>", unsafe_allow_html=True)
