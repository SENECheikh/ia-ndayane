import streamlit as st
import pandas as pd

# 1. Configuration de la page (sans barre latérale)
st.set_page_config(
    page_title="ASSOS NDAYANE VILLAGE - Tableau de Bord", 
    page_icon="🇸🇳", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Design aux couleurs du Sénégal (Vert, Or, Rouge) et masquage des menus techniques
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 1.5rem !important; }
    
    .header-container { text-align: center; padding-bottom: 10px; }
    .flag-style { font-size: 65px; margin: 0px; line-height: 1; }
    .main-title { color: #008543; font-family: 'Segoe UI', sans-serif; font-weight: 800; font-size: 36px; margin-top: 5px; margin-bottom: 0px; }
    .sub-title { color: #E31B23; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: 600; margin-top: 2px; margin-bottom: 15px; }
    
    /* Cartes de statistiques */
    .kpi-card { 
        padding: 18px; 
        background-color: #F8F9FA; 
        border-top: 4px solid #008543;
        border-radius: 8px; 
        text-align: center; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        margin-bottom: 10px;
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

    # --- ZONE DE FILTRES ET RÈGLES DIRECTEMENT VISIBLE SUR MOBILE ---
    col_filtres, col_regles = st.columns([1, 1.2])
    
    with col_filtres:
        st.markdown("### 🔍 Filtres du Tableau de Bord")
        liste_mois = ["Tous les mois"] + list(df['Date'].unique())
        mois_choisi = st.selectbox("Période (Mois) :", liste_mois)
        
        liste_residence = ["Toutes les résidences"] + sorted(list(df['Résidence'].unique()))
        residence_choisie = st.selectbox("Quartier / Résidence :", liste_residence)

    with col_regles:
        st.info("""
        📜 **Règles du Comité des Sages :**
        * **Adhésion :** 1 000 FCFA
        * **Intervention sociale :** 25 000 FCFA *(Hospitalisation, Accident grave, Sinistres naturels)*
        * **Décès exclu** *(en attente d'arbitrage AG)*
        * **Retard 3 mois :** Avertissement | **Retard +6 mois :** Radiation
        """)

    st.write("---")

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
        enveloppe_sociale_globale = int(total_collecte * 0.40)
        nb_interventions = enveloppe_sociale_globale // 25000
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Capacité Sociale</div><div class='kpi-value'>{nb_interventions} cas</div><div class='kpi-sub'>Aides de 25 000 F possibles</div></div>", unsafe_allow_html=True)

    st.write("---")

    # --- SECTION 2 : VENTILATION DES FONDS (SANS LE DÉCÈS) ---
    st.subheader("🏦 Répartition des Enveloppes (Charte Révisée)")
    
    fonds_dev = int(total_collecte * 0.60)
    fonds_sante_accident = int(total_collecte * 0.25)
    fonds_sinistres_commun = int(total_collecte * 0.15)

    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("🏗️ Développement (60%)", f"{fonds_dev:,} FCFA", "Projet Électricité / Infrastructures")
    col_f2.metric("🩺 Santé & Accidents (25%)", f"{fonds_sante_accident:,} FCFA", "Hospitalisation, fractures, blessures graves")
    col_f3.metric("🌪️ Sinistres & Bien Commun (15%)", f"{fonds_sinistres_commun:,} FCFA", "Incendie, inondation, orage, village")

    st.write("---")

    # --- SECTION 3 : GRAPHIQUES PAR QUARTIER & SUIVI DES MEMBRES ---
    col_graph, col_statut = st.columns([1.2, 1])

    with col_graph:
        st.subheader("🏘️ Collecte par Résidence (FCFA)")
        df_quartier = df_filtre.groupby('Résidence')['Montant FCFA'].sum().sort_values(ascending=False)
        st.bar_chart(df_quartier, color="#008543")

    with col_statut:
        st.subheader("⚖️ Suivi Règlement (Comité des Sages)")
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
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>ASSOS NDAYANE VILLAGE — Commune de Tocky Gare, Diourbel | Charte révisée par le Comité des Sages</p>", unsafe_allow_html=True)
