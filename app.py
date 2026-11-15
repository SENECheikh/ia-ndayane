import streamlit as st
import pandas as pd
import unicodedata

st.set_page_config(page_title="ASSOS NDAYANE VILLAGE", page_icon="🇸🇳", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid='stHeader'], [data-testid='collapsedControl'] {display: none !important;} .block-container {padding-top: 1.5rem !important;} .header-container {text-align: center; padding-bottom: 10px;} .flag-style {font-size: 65px; margin: 0px; line-height: 1;} .main-title {color: #008543; font-family: 'Segoe UI', sans-serif; font-weight: 800; font-size: 36px; margin-top: 5px; margin-bottom: 0px;} .sub-title {color: #E31B23; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: 600; margin-top: 2px; margin-bottom: 15px;} .kpi-card {padding: 18px; background-color: #F8F9FA; border-top: 4px solid #008543; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px;} .kpi-title {font-size: 14px; font-weight: bold; color: #555555; text-transform: uppercase;} .kpi-value {color: #008543; font-size: 26px; font-weight: 800; margin-top: 5px;} .kpi-sub {font-size: 12px; color: #888888; margin-top: 3px;}</style>", unsafe_allow_html=True)

st.markdown("<div class='header-container'><div class='flag-style'>🇸🇳</div><h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1><p class='sub-title'>Tableau de Bord Général & Suivi des Cotisations</p></div>", unsafe_allow_html=True)
st.write("---")

def nettoyer(t):
    if pd.isna(t): return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(t).strip().title()) if unicodedata.category(c) != 'Mn')

df = pd.read_csv("cotisations.csv")
df.columns = df.columns.str.strip()
df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip().replace('', 'Non spécifiée')
df['Mode paiement'] = df['Mode paiement'].fillna('En attente').astype(str).str.strip()
df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
df['Nom Complet'] = (df['Nom'].apply(nettoyer) + " " + df['Prénom'].apply(nettoyer)).str.strip()
df = df[df['Nom Complet'].str.len() > 2]

try:
    df_dep = pd.read_csv("depenses.csv")
    df_dep.columns = df_dep.columns.str.strip()
    df_dep['Date'] = df_dep['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
    df_dep['Montant Sorti'] = pd.to_numeric(df_dep['Montant Sorti'], errors='coerce').fillna(0)
except:
    df_dep = pd.DataFrame(columns=['Date', 'Enveloppe', 'Montant Sorti', 'Motif'])

st.info("📜 **Règles du Comité des Sages :**\n* **Adhésion :** 1 000 FCFA\n* **Enveloppe Sociale Fixe :** **25 000 FCFA** *(62,5% Santé & Accidents • 37,5% Sinistres & Bien Commun)*\n* **Décès exclu** *(en attente d'arbitrage AG)*\n* **Retard 3 mois :** Avertissement | **Retard +6 mois :** Radiation")

st.markdown("### 🔍 Filtres du Tableau de Bord")
mois_choisi = st.selectbox("Période (Mois) :", ["Tous les mois"] + list(df['Date'].unique()))
residence_choisie = st.selectbox("Quartier / Résidence :", ["Toutes les résidences"] + sorted(list(df['Résidence'].unique())))
st.write("---")

df_filtre = df if mois_choisi == "Tous les mois" else df[df['Date'] == mois_choisi]
df_dep_filtre = df_dep if mois_choisi == "Tous les mois" else df_dep[df_dep['Date'] == mois_choisi]
if residence_choisie != "Toutes les résidences":
    df_filtre = df_filtre[df_filtre['Résidence'] == residence_choisie]

# Enveloppe sociale strictement fixe à 25 000 FCFA
BASE_SOCIALE_FIXE = 25000

tab1, tab2, tab3 = st.tabs(["💰 RECETTES", "📤 DÉPENSES", "🏦 RESTE DE LA CAISSE"])

with tab1:
    total_collecte = int(df_filtre['Montant FCFA'].sum())
    membres_total = len(df_filtre)
    membres_cotisants = int((df_filtre['Montant FCFA'] >= 1000).sum())
    membres_retard = membres_total - membres_cotisants
    montant_attendu = membres_total * 1000
    reste_a_recouvrer = max(0, montant_attendu - total_collecte)
    taux_recouvrement = int((membres_cotisants / membres_total * 100)) if membres_total > 0 else 0

    # Répartition : 25 000 F fixe pour le social (plafonné au total collecté si < 25 000 F), tout le reste au développement
    enveloppe_sociale = min(total_collecte, BASE_SOCIALE_FIXE)
    fonds_dev = max(0, total_collecte - enveloppe_sociale)
    fonds_sante = int(enveloppe_sociale * 0.60)
    fonds_sinistres = enveloppe_sociale - fonds_sante

    st.subheader(f"📈 Situation Financière ({mois_choisi} | {residence_choisie})")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Collecté</div><div class='kpi-value'>{total_collecte:,} F</div><div class='kpi-sub'>Sur {montant_attendu:,} F attendus</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card' style='border-top-color:#E31B23;'><div class='kpi-title'>Reste à Recouvrer</div><div class='kpi-value' style='color:#E31B23;'>{reste_a_recouvrer:,} F</div><div class='kpi-sub'>{membres_retard} ligne(s) en attente</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card' style='border-top-color:#FDEF42;'><div class='kpi-title'>Taux de Participation</div><div class='kpi-value'>{taux_recouvrement} %</div><div class='kpi-sub'>{membres_cotisants} / {membres_total} cotisations</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Budget Social Fixe</div><div class='kpi-value'>{enveloppe_sociale:,} F</div><div class='kpi-sub'>Plafond fixe alloué</div></div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("🏦 Répartition des Enveloppes (Base Sociale Fixe de 25 000 F)")
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("🏗️ Développement (Le Reste)", f"{fonds_dev:,} FCFA", "Total collecté moins les 25 000 F")
    col_f2.metric("🩺 Santé & Accidents (62% des 25k)", f"{fonds_sante:,} FCFA", "Hospitalisation, fractures, blessures")
    col_f3.metric("🌪️ Sinistres & Village (40% des 25k)", f"{fonds_sinistres:,} FCFA", "Incendie, inondation, orage")

    st.write("---")
    col_graph, col_statut = st.columns([1.2, 1])
    with col_graph:
        st.subheader("🏘️ Collecte par Résidence (FCFA)")
        st.bar_chart(df_filtre.groupby('Résidence')['Montant FCFA'].sum().sort_values(ascending=False), color="#008543")

    with col_statut:
        st.subheader("⚖️ Suivi Règlement (Comité des Sages)")
        mois_enregistres = df['Date'].nunique()
        paiements = df[df['Montant FCFA'] >= 1000].groupby('Nom Complet')['Date'].nunique()
        tous = df[['Nom Complet', 'Résidence']].drop_duplicates(subset=['Nom Complet'])
        tous['Impayes'] = (mois_enregistres - tous['Nom Complet'].map(paiements).fillna(0).astype(int)).clip(lower=0)
        tous['Statut'] = tous['Impayes'].apply(lambda x: "🔴 Radié (+6 mois)" if x >= 6 else ("🟠 Avertissement (3-5 mois)" if x >= 3 else (f"🟡 En retard ({x} mois)" if x > 0 else "🟢 À jour")))
        if residence_choisie != "Toutes les résidences":
            tous = tous[tous['Résidence'] == residence_choisie]
        st.dataframe(tous[['Nom Complet', 'Résidence', 'Statut']].sort_values(by='Statut', ascending=False), use_container_width=True, height=300)

    st.write("---")
    st.subheader("📋 Registre Détaillé des Transactions")
    st.dataframe(df_filtre[['Date', 'Nom Complet', 'Résidence', 'Montant FCFA', 'Mode paiement']].sort_values(by=['Date', 'Montant FCFA', 'Nom Complet']), use_container_width=True)

with tab2:
    st.subheader(f"📤 Suivi des Dépenses ({mois_choisi})")
    total_sorties = int(df_dep_filtre['Montant Sorti'].sum())
    dep_dev = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Developpement']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0
    dep_sante = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Sante']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0
    dep_sinistres = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Sinistres']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0

    d1, d2, d3, d4 = st.columns(4)
    d1.markdown(f"<div class='kpi-card' style='border-top-color:#E31B23;'><div class='kpi-title'>Total Dépensé</div><div class='kpi-value' style='color:#E31B23;'>{total_sorties:,} F</div><div class='kpi-sub'>Toutes enveloppes</div></div>", unsafe_allow_html=True)
    d2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Dép. Développement</div><div class='kpi-value'>{dep_dev:,} F</div><div class='kpi-sub'>Infrastructures</div></div>", unsafe_allow_html=True)
    d3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Dép. Santé</div><div class='kpi-value'>{dep_sante:,} F</div><div class='kpi-sub'>Urgences médicales</div></div>", unsafe_allow_html=True)
    d4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Dép. Sinistres</div><div class='kpi-value'>{dep_sinistres:,} F</div><div class='kpi-sub'>Village & Catastrophes</div></div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("📋 Journal des Dépenses Validées")
    if not df_dep_filtre.empty:
        st.dataframe(df_dep_filtre, use_container_width=True)
    else:
        st.info("Aucune dépense enregistrée pour cette période.")

with tab3:
    st.subheader(f"🏦 Solde Réel Disponible en Caisse ({mois_choisi})")
    df_rec_mois = df if mois_choisi == "Tous les mois" else df[df['Date'] == mois_choisi]
    rec_globale = int(df_rec_mois['Montant FCFA'].sum())
    
    env_soc_g = min(rec_globale, BASE_SOCIALE_FIXE)
    rec_dev_g = max(0, rec_globale - env_soc_g)
    rec_sante_g = int(env_soc_g * 0.60)
    rec_sinistres_g = env_soc_g - rec_sante_g
    
    reste_dev = rec_dev_g - dep_dev
    reste_sante = rec_sante_g - dep_sante
    reste_sinistres = rec_sinistres_g - dep_sinistres
    reste_total = rec_globale - total_sorties

    r1, r2, r3, r4 = st.columns(4)
