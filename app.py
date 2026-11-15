import streamlit as st
import pandas as pd

# 1. Configuration simple de la page
st.set_page_config(page_title="ASSOS NDAYANE VILLAGE", page_icon="🇸🇳", layout="wide")

# Masquer uniquement la barre technique du haut
st.markdown("<style>[data-testid='stHeader'] {display: none !important;}</style>", unsafe_allow_html=True)

# EN-TÊTE SIMPLE
st.markdown("<h1 style='text-align: center; color: #008543;'>🇸🇳 ASSOS NDAYANE VILLAGE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #E31B23; font-weight: bold;'>Situation Financière : Recettes, Dépenses & Reste en Caisse</p>", unsafe_allow_html=True)
st.write("---")

try:
    # A. CHARGEMENT DES RECETTES (Cotisations)
    df_recettes = pd.read_csv("cotisations.csv")
    df_recettes.columns = df_recettes.columns.str.strip()
    df_recettes['Date'] = df_recettes['Date'].fillna('Inconnu').astype(str).str.strip()
    df_recettes['Résidence'] = df_recettes['Résidence'].fillna('Non spécifiée').astype(str).str.strip()
    df_recettes['Montant FCFA'] = pd.to_numeric(df_recettes['Montant FCFA'], errors='coerce').fillna(0)
    df_recettes['Nom Complet'] = df_recettes['Nom'].fillna('').astype(str).str.strip() + " " + df_recettes['Prénom'].fillna('').astype(str).str.strip()
    df_recettes = df_recettes[df_recettes['Nom Complet'].str.len() > 2]

    # B. CHARGEMENT DES DÉPENSES (Si le fichier existe)
    try:
        df_depenses = pd.read_csv("depenses.csv")
        df_depenses.columns = df_depenses.columns.str.strip()
        df_depenses['Date'] = df_depenses['Date'].fillna('Inconnu').astype(str).str.strip()
        df_depenses['Montant Sorti'] = pd.to_numeric(df_depenses['Montant Sorti'], errors='coerce').fillna(0)
    except:
        df_depenses = pd.DataFrame(columns=['Date', 'Enveloppe', 'Montant Sorti', 'Motif'])

    # --- RÈGLES DU COMITÉ DES SAGES ---
    st.info("""
    📜 **Règles du Comité des Sages :**
    * **Adhésion :** 1 000 FCFA
    * **Intervention sociale :** 25 000 FCFA (Hospitalisation, Accident grave, Sinistres naturels)
    * **Décès exclu** (en attente d'arbitrage AG)
    * **Retard 3 mois :** Avertissement | **Retard +6 mois :** Radiation
    """)

    # --- FILTRES SUPERPOSÉS ---
    st.subheader("🔍 Filtres")
    mois_choisi = st.selectbox("Période (Mois) :", ["Tous les mois"] + list(df_recettes['Date'].unique()))
    residence_choisie = st.selectbox("Quartier / Résidence :", ["Toutes les résidences"] + sorted(list(df_recettes['Résidence'].unique())))

    st.write("---")

    # Application des filtres sur les recettes
    df_rec_filtre = df_recettes.copy()
    if mois_choisi != "Tous les mois":
        df_rec_filtre = df_rec_filtre[df_rec_filtre['Date'] == mois_choisi]
    if residence_choisie != "Toutes les résidences":
        df_rec_filtre = df_rec_filtre[df_rec_filtre['Résidence'] == residence_choisie]

    # Application du filtre mois sur les dépenses
    df_dep_filtre = df_depenses.copy()
    if mois_choisi != "Tous les mois":
        df_dep_filtre = df_dep_filtre[df_dep_filtre['Date'] == mois_choisi]

    # --- CALCULS FINANCIERS GLOBAUX ---
    total_recettes = int(df_rec_filtre['Montant FCFA'].sum())
    total_depenses = int(df_dep_filtre['Montant Sorti'].sum()) if residence_choisie == "Toutes les résidences" else 0
    reste_en_caisse = total_recettes - total_depenses

    # --- SECTION 1 : RECETTES, DÉPENSES & RESTE EN CAISSE ---
    st.subheader(f"💰 Bilan Général ({mois_choisi})")
    c1, c2, c3 = st.columns(3)
    c1.metric("📥 Total Recettes (Entrées)", f"{total_recettes:,} FCFA")
    c2.metric("📤 Total Dépenses (Sorties)", f"{total_depenses:,} FCFA")
    c3.metric("🏦 Reste en Caisse (Solde)", f"{reste_en_caisse:,} FCFA")

    st.write("---")

    # --- SECTION 2 : RÉPARTITION PAR ENVELOPPE (60% / 25% / 15%) ---
    st.subheader("📊 Détail par Enveloppe (Recettes - Dépenses = Reste)")
    
    # Calcul des entrées théoriques selon les % des Sages
    rec_dev = int(total_recettes * 0.60)
    rec_sante = int(total_recettes * 0.25)
    rec_sinistres = int(total_recettes * 0.15)

    # Calcul des sorties par enveloppe
    dep_dev = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Developpement']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0
    dep_sante = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Sante']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0
    dep_sinistres = int(df_dep_filtre[df_dep_filtre['Enveloppe'] == 'Sinistres']['Montant Sorti'].sum()) if not df_dep_filtre.empty else 0

    # Tableau récapitulatif clair
    tableau_caisse = pd.DataFrame({
        "Enveloppe": ["🏗️ Développement (60%)", "🩺 Santé & Accidents (25%)", "🌪️ Sinistres & Bien Commun (15%)"],
        "Recettes (Entrées)": [f"{rec_dev:,} F", f"{rec_sante:,} F", f"{rec_sinistres:,} F"],
        "Dépenses (Sorties)": [f"{dep_dev:,} F", f"{dep_sante:,} F", f"{dep_sinistres:,} F"],
        "Reste en Caisse": [f"{rec_dev - dep_dev:,} F", f"{rec_sante - dep_sante:,} F", f"{rec_sinistres - dep_sinistres:,} F"]
    })
    st.table(tableau_caisse)

    st.write("---")

    # --- SECTION 3 : GRAPHIQUE & SUIVI DES MEMBRES ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏘️ Recettes par Résidence")
        st.bar_chart(df_rec_filtre.groupby('Résidence')['Montant FCFA'].sum(), color="#008543")

    with col2:
        st.subheader("⚖️ Statut des Membres (Règle des Sages)")
        df_hist = df_recettes.copy()
        df_hist['Impaye'] = (df_hist['Montant FCFA'] < 1000).astype(int)
        suivi = df_hist.groupby(['Nom Complet', 'Résidence'])['Impaye'].sum().reset_index()
        suivi['Statut'] = suivi['Impaye'].apply(lambda x: "🔴 Radié (+6 mois)" if x >= 6 else ("🟠 Avertissement (3-5 mois)" if x >= 3 else (f"🟡 En retard ({x} mois)" if x > 0 else "🟢 À jour")))
        if residence_choisie != "Toutes les résidences":
            suivi = suivi[suivi['Résidence'] == residence_choisie]
        st.dataframe(suivi[['Nom Complet', 'Résidence', 'Statut']], use_container_width=True, height=300)

    st.write("---")

    # --- SECTION 4 : LISTE DES DÉPENSES & COTISATIONS ---
    st.subheader("📤 Historique des Dépenses")
    if not df_dep_filtre.empty:
        st.dataframe(df_dep_filtre, use_container_width=True)
    else:
        st.write("Aucune dépense enregistrée pour cette période.")

    st.subheader("📥 Registre des Cotisations")
    st.dataframe(df_rec_filtre[['Date', 'Nom Complet', 'Résidence', 'Montant FCFA', 'Mode paiement']], use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Erreur de lecture : {e}")
