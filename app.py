import streamlit as st
import pandas as pd
import unicodedata

st.set_page_config(page_title="ASSOS NDAYANE VILLAGE - Tableau de Bord", page_icon="🇸🇳", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    .header-container { text-align: center; padding-bottom: 10px; }
    .flag-style { font-size: 65px; margin: 0px; line-height: 1; }
    .main-title { color: #008543; font-family: 'Segoe UI', sans-serif; font-weight: 800; font-size: 36px; margin-top: 5px; margin-bottom: 0px; }
    .sub-title { color: #E31B23; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: 600; margin-top: 2px; margin-bottom: 15px; }
    .kpi-card { padding: 18px; background-color: #F8F9FA; border-top: 4px solid #008543; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 10px; }
    .kpi-title { font-size: 14px; font-weight: bold; color: #555555; text-transform: uppercase; }
    .kpi-value { color: #008543; font-size: 26px; font-weight: 800; margin-top: 5px; }
    .kpi-sub { font-size: 12px; color: #888888; margin-top: 3px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='header-container'>
        <div class='flag-style'>🇸🇳</div>
        <h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1>
        <p class='sub-title'>Tableau de Bord Général & Suivi des Cotisations</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

def nettoyer_texte(texte):
    if pd.isna(texte):
        return ""
    texte = str(texte).strip().title()
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
    df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip().replace('', 'Non spécifiée')
    df['Mode paiement'] = df['Mode paiement'].fillna('En attente').astype(str).str.strip()
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    df['Nom Complet'] = (df['Nom'].apply(nettoyer_texte) + " " + df['Prénom'].apply(nettoyer_texte)).str.strip()
    df = df[df['Nom Complet'].str.len() > 2]

    try:
        df_dep = pd.read_csv("depenses.csv")
        df_dep.columns = df_dep.columns.str.strip()
        df_dep['Date'] = df_dep['Date'].fillna('Inconnu').astype(str).str.strip().str.lower()
        df_dep['Montant Sorti'] = pd.to_numeric(df_dep['Montant Sorti'], errors='coerce').fillna(0)
    except:
        df_dep = pd.DataFrame(columns=['Date', 'Enveloppe', 'Montant Sorti', 'Motif'])

    st.info("""
    📜 **Règles du Comité des Sages :**
    * **Adhésion :** 1 000 FCFA
    * **Intervention sociale :** 25 000 FCFA *(Hospitalisation, Accident grave, Sinistres naturels)*
    * **Décès exclu** *(en attente d'arbitrage AG)*
    * **Retard 3 mois :** Avertissement | **Retard +6 mois :** Radiation
    """)

    st.markdown("### 🔍 Filtres du Tableau de Bord")
    mois_choisi = st.selectbox("Période (Mois) :", ["Tous les mois"] + list(df['Date'].unique()))
    residence_choisie = st.selectbox("Quartier / Résidence :", ["Toutes les résidences"] + sorted(list(df['Résidence'].unique())))
    st.write("---")

    df_filtre = df.copy()
    df_dep_filtre = df_dep.copy()
    if mois_choisi != "Tous les mois":
        df_filtre = df_filtre[df_filtre['Date'] == mois_choisi]
        df_dep_filtre = df_dep_filtre[df_dep_filtre['Date'] == mois_choisi]
    if residence_choisie != "Toutes les résidences":
        df_filtre = df_filtre[df_filtre['Résidence'] == residence_choisie]

    tab1, tab2, tab3 = st.tabs(["💰 RECETTES", "📤 DÉPENSES", "🏦 RESTE DE LA CAISSE"])

    with tab1:
        total_collecte = int(df_filtre['Montant FCFA'].sum())
        membres_total = len(df_filtre)
        membres_cotisants = int((df_filtre['Montant FCFA'] >= 1000).sum())
        membres_retard = membres_total - membres_cotisants
        montant_attendu = membres_total * 1000
        reste_a_recouvrer = max(0, montant_attendu - total_collecte)
        taux_recouvrement = int((membres_cotisants / membres_total * 100)) if membres_total > 0 else 0

        st.subheader(f"📈 Situation Financière ({mois_choisi} | {residence_choisie})")
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Collecté</div><div class='kpi-value'>{total_collecte:,} F</div><div class='kpi-sub'>Sur {montant_attendu:,} F attendus</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='kpi-card' style='border-top-color:#E31B23;'><div class='kpi-title'>Reste à Recouvrer</div><div class='kpi-value' style='color:#E31B23;'>{reste_a_recouvrer:,} F</div><div class='kpi-sub'>{membres_retard} ligne(s) en attente</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='kpi-card' style='border-top-color:#FDEF42;'><div class='kpi-title'>Taux de Participation</div><div class='kpi-value'>{taux_recouvrement} %</div><div class='kpi-sub'>{membres_cotisants} / {membres_total} cotisations</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Capacité Sociale</div><div class='kpi-value'>{int(total_collecte * 0.40) // 25000} cas</div><div class='kpi-sub'>Aides de 25 000 F possibles</div></div>", unsafe_allow_html=True)

        st.write("---")
        st.subheader("🏦 Répartition des Enveloppes (Charte Révisée)")
        col_f1, col_f2, col_f3 = st.columns(3)
        col_f1.metric("🏗️ Développement (60%)", f"{int(total_collecte * 0.60):,} FCFA", "Projet Électricité / Infrastructures")
        col_f2.metric("🩺 Santé & Accidents (25%)", f"{int(total_collecte * 0.25):,} FCFA", "Hospitalisation, fractures, blessures graves")
        col_f3.metric("🌪️ Sinistres & Bien Commun (15%)", f"{int(total_collecte * 0.15):,} FCFA", "Incendie, inondation, orage, village")

        st.write("---")
        col_graph, col_statut = st.columns([1.2, 1])
        with col_graph:
            st.subheader("🏘️ Collecte par Résidence (FCFA)")
            st.bar_chart(df_filtre.groupby('Résidence')['Montant FCFA'].sum().sort_values(ascending=False), color="#008543")

        with col_statut:
            st.subheader("⚖️ Suivi Règlement (Comité des Sages)")
            mois_enregistres = df['Date'].nunique()
            paiements_par_membre = df[df['Montant FCFA'] >= 1000].groupby('Nom Complet')['Date'].nunique()
            tous_membres = df[['Nom Complet', 'Résidence']].drop_duplicates(subset=['Nom Complet'])
            tous_membres['Mois_Payes'] = tous_membres['Nom Complet'].map(paiements_par_membre).fillna(0).astype(int)
            tous_membres['Mois_Impayes'] = (mois_enregistres - tous_membres['Mois_Payes']).clip(lower=0)
            tous_membres['Statut'] = tous_membres['Mois_Impayes'].apply(lambda x: "🔴 Radié (+6 mois)" if x >= 6 else ("🟠 Avertissement (3-5 mois)" if x >= 3 else (f"🟡 En retard ({x} mois)" if x > 0 else "🟢 À jour")))
            if residence_choisie != "Toutes les résidences":
                tous_membres = tous_membres[tous_membres['Résidence'] == residence_choisie]
            st.dataframe(tous_membres[['Nom Complet', 'Résidence', 'Statut']].sort_values(by='Statut', ascending=False), use_container_width=True, height=300)

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
        d3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Dép. Santé</div><div class='kpi-value'>{dep_sante:,} F</div><div class='kpi-sub'>25 000 F / intervention</div></div>", unsafe_allow_html=True)
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
        rec_dev_g = int(rec_globale * 0.60)
        rec_sante_g = int(rec_globale * 0.25)
