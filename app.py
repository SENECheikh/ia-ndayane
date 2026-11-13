import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(
    page_title="ASSOS NDAYANE VILLAGE - Tableau de Bord", 
    page_icon="🇸🇳", 
    layout="wide" # Format large pour un vrai tableau de bord
)

# Design aux couleurs du Sénégal (Vert, Or, Rouge) et masquage des menus techniques
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    
    .header-container { text-align: center; padding-bottom: 15px; }
    .flag-style { font-size: 65px; margin: 0px; line-height: 1; }
    .main-title { color: #008543; font-family: 'Segoe UI', sans-serif; font-weight: 800; font-size: 38px; margin-top: 5px; margin-bottom: 0px; }
    .sub-title { color: #E31B23; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: 600; margin-top: 2px; margin-bottom: 15px; }
    
    /* Cartes de statistiques */
    .kpi-card { 
        padding: 18px; 
        background-color: #F8F9FA; 
        border-top: 4px solid #008543;
        border-radius: 8px; 
        text-align: center; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
    }
    .kpi-title { font-size: 14px; font-weight: bold; color: #555555; text-transform: uppercase; }
    .kpi-value { color: #008543; font-size: 26px; font-weight: 800; margin-top: 5px; }
    .kpi-sub { font-size: 12px; color: #888888; margin-top: 3px; }
    </style>
""", unsafe_allow_html=True)

# EN-TÊTE OFFICIEL
st.markdown("""
    <div class='header-container'>
        <div class='flag-style'>🇸🇳</div>
        <h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1>
        <p class='sub-title'>Tableau de Bord Général & Suivi des Cotisations</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 2. Chargement et traitement des données
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

    # --- BARRE LATÉRALE DE FILTRES ---
    st.sidebar.markdown("### 🔍 Filtres du Tableau de Bord")
    liste_mois = ["Tous les mois"] + list(df['Date'].unique())
    mois_choisi = st.sidebar.selectbox("Période (Mois) :", liste_mois)
    
    liste_residence = ["Toutes les résidences"] + sorted(list(df['Résidence'].unique()))
    residence_choisie = st.sidebar.selectbox("Quartier / Résidence :", liste_residence)

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
    st.subheader(f"📈 Situation Financière ({mois_choisi} | {residence_choisie})")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Collecté</div><div class='kpi-value'>{total_collecte:,} F</div><div class='kpi-sub'>Sur {montant_attendu:,} F attendus</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card' style='border-top-color:#E31B23;'><div class='kpi-title'>Reste à Recouvrer</div><div class='kpi-value' style='color:#E31B23;'>{reste_a_recouvrer:,} F</div><div class='kpi-sub'>{membres_retard} membre(s) en attente</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='kpi-card' style='border-top-color:#FDEF42;'><div class='kpi-title'>Taux de Participation</div><div class='kpi-value'>{taux_recouvrement} %</div><div class='kpi-sub'>{membres_cotisants} / {membres_total} membres à jour</div></div>", unsafe_allow_html=True)
    with c4:
        # Calcul du nombre d'interventions sociales possibles (25 000 F / intervention selon les Sages)
        enveloppe_sociale_globale = int(total_collecte * 0.40) # 20% Santé + 12% Décès + 8% Bien Commun
        nb_interventions = enveloppe_sociale_globale // 25000
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Capacité Sociale</div><div class='kpi-value'>{nb_interventions} cas</div><div class='kpi-sub'>Interventions à 25 000 F possibles</div></div>", unsafe_allow_html=True)

    st.write("---")

    # --- SECTION 2 : VENTILATION DES FONDS (RÈGLES DE LA CHARTE) ---
    st.subheader("🏦 Répartition Automatique des Enveloppes")
    
    fonds_dev = int(total_collecte * 0.60)
    fonds_sante = int(total_collecte * 0.20)
    fonds_deces = int(total_collecte * 0.12)
    fonds_bien_commun = int(total_collecte * 0.08)

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    col_f1.metric("🏗️ Développement (60%)", f"{fonds_dev:,} FCFA", "Projet Électricité")
    col_f2.metric("🩺 Urgences Santé (20%)", f"{fonds_sante:,} FCFA", "Hospitalisation / Accident")
    col_f3.metric("🕊️ Solidarité Décès (12%)", f"{fonds_deces:,} FCFA", "Sous arbitrage AG")
    col_f4.metric("💧 Bien Commun (8%)", f"{fonds_bien_commun:,} FCFA", "Sinistres / Village")

    st.write("---")

    # --- SECTION 3 : GRAPHIQUES PAR QUARTIER & SUIVI DES MEMBRES ---
    col_graph, col_statut = st.columns([1.2, 1])

    with col_graph:
        st.subheader("🏘️ Collecte par Résidence (FCFA)")
        # Regroupement des montants par quartier
        df_quartier = df_filtre.groupby('Résidence')['Montant FCFA'].sum().sort_values(ascending=False)
        st.bar_chart(df_quartier, color="#008543")

    with col_statut:
        st.subheader("⚖️ Suivi Règlement (Comité des Sages)")
        # Calcul automatique du statut sur l'ensemble du fichier historique pour détecter les retards cumulés
        df_historique = df.copy()
        df_historique['Mois_Impaye'] = (df_historique['Montant FCFA'] < 1000).astype(int)
        suivi_retards = df_historique.groupby(['Nom Complet', 'Résidence'])['Mois_Impaye'].sum().reset_index()
        
        def definir_statut(nb_retards):
            if nb_retards >= 6:
                return "🔴 Radié (+6 mois)"
            elif nb_retards >= 3:
                return "🟠 Avertissement (3-5 mois)"
            elif nb_retards > 0:
                return f"🟡 En retard ({nb_retards} mois)"
            else:
                return "🟢 À jour"
                
        suivi_retards['Statut'] = suivi_retards['Mois_Impaye'].apply(definir_statut)
        
        # Filtrer l'affichage des statuts si une résidence est sélectionnée
        if residence_choisie != "Toutes les résidences":
            suivi_retards = suivi_retards[suivi_retards['Résidence'] == residence_choisie]
            
        st.dataframe(suivi_retards[['Nom Complet', 'Résidence', 'Statut']], use_container_width=True, height=300)

    st.write("---")

    # --- SECTION 4 : REGISTRE DÉTAILLÉ DES COTISATIONS ---
    st.subheader("📋 Registre Détaillé des Transactions")
    df_affichage = df_filtre[['Date', 'Nom Complet', 'Résidence', 'Montant FCFA', 'Mode paiement']].sort_values(by=['Montant FCFA', 'Nom Complet'], ascending=[True, True])
    st.dataframe(df_affichage, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Erreur lors du chargement des données. Vérifiez que le fichier 'cotisations.csv' est bien présent sur GitHub. Détails : {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>ASSOS NDAYANE VILLAGE — Commune de Tocky Gare, Diourbel | Tableau de Bord Officiel</p>", unsafe_allow_html=True)
