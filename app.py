import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(
    page_title="ASSOS NDAYANE VILLAGE", 
    page_icon="🇸🇳", 
    layout="centered"
)

# Design, styles CSS professionnels et blocage TOTAL des icônes GitHub / Streamlit
st.markdown("""
    <style>
    /* Masquer la barre supérieure de Streamlit/GitHub */
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 2rem !important; }
    
    /* Alignement et styles des titres */
    .header-container {
        text-align: center;
        padding-top: 10px;
        padding-bottom: 20px;
    }
    .flag-style {
        font-size: 70px;
        margin: 0px;
        padding: 0px;
        line-height: 1;
    }
    .main-title { 
        color: #008543; /* Vert du Sénégal */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        font-weight: 800; 
        font-size: 38px;
        letter-spacing: 1px;
        margin-top: 5px;
        margin-bottom: 0px; 
    }
    .sub-title { 
        color: #E31B23; /* Rouge du Sénégal */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px; 
        font-weight: 600; 
        letter-spacing: 0.5px;
        margin-top: 2px;
        margin-bottom: 20px; 
    }
    /* Boîtes de statistiques */
    .stat-box { 
        padding: 20px; 
        background-color: #F8F9FA; 
        border: 1px solid #E0E0E0; 
        border-radius: 8px; 
        text-align: center; 
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05); 
    }
    .fonds-title { font-size: 15px; font-weight: bold; color: #333333; }
    .fonds-montant { color: #008543; font-size: 22px; font-weight: bold; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# EN-TÊTE OFFICIEL
st.markdown("""
    <div class='header-container'>
        <div class='flag-style'>🇸🇳</div>
        <h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1>
        <p class='sub-title'>Ventilation Automatique de la Caisse</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 2. Lecture du fichier cotisations.csv
try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    
    # Nettoyage des données textuelles
    df['Date'] = df['Date'].fillna('Inconnu').astype(str).str.strip()
    df['Résidence'] = df['Résidence'].fillna('Non spécifiée').astype(str).str.strip()
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    
    # Fusion Nom et Prénom pour l'affichage si besoin
    df['Nom'] = df['Nom'].fillna('').astype(str).str.strip()
    df['Prénom'] = df['Prénom'].fillna('').astype(str).str.strip()
    df['Nom Complet'] = df['Nom'] + " " + df['Prénom']
    df = df[df['Nom Complet'].str.len() > 2]

    # --- BARRE LATERALE DE FILTRES (SIDEBAR) ---
    st.sidebar.markdown("### 🔍 Filtres de Recherche")
    
    # Filtre par Mois (colonne 'Date' de votre fichier)
    liste_mois = ["Tous les mois"] + list(df['Date'].unique())
    mois_choisi = st.sidebar.selectbox("Sélectionner le Mois :", liste_mois)
    
    # Filtre par Résidence (quartier)
    liste_residence = ["Toutes les résidences"] + list(df['Résidence'].unique())
    residence_choisie = st.sidebar.selectbox("Sélectionner la Résidence :", liste_residence)

    # Application des filtres sur les données
    df_filtre = df.copy()
    if mois_choisi != "Tous les mois":
        df_filtre = df_filtre[df_filtre['Date'] == mois_choisi]
    if residence_choisie != "Toutes les résidences":
        df_filtre = df_filtre[df_filtre['Résidence'] == residence_choisie]

    # Calcul des statistiques dynamiques basées sur les filtres
    total_collecte = int(df_filtre['Montant FCFA'].sum())
    membres_total = len(df_filtre)
    membres_cotisants = int((df_filtre['Montant FCFA'] >= 1000).sum())
    membres_retard = membres_total - membres_cotisants

    # --- AFFICHAGE DU BILAN DU MOIS ---
    st.write(f"### 📈 Bilan filtré : {mois_choisi} | {residence_choisie}")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(label="Membres Recensés", value=f"{membres_total}")
    with col_b:
        st.metric(label="Membres Ayant Cotisé", value=f"{membres_cotisants}")
    with col_c:
        st.metric(label="Restant à Recouvrer", value=f"{membres_retard} pers.", delta=f"-{membres_retard}" if membres_retard > 0 else "0", delta_color="inverse")

    st.success(f"💰 **Montant total collecté sur ce filtre : {total_collecte:,} FCFA**")
    st.write("---")

    # --- VENTILATION AUTOMATIQUE (METHODE 1) ---
    st.write("### 📊 Répartition automatique (Selon la Charte)")

    fonds_dev = int(total_collecte * 0.60)
    fonds_sante = int(total_collecte * 0.20)
    fonds_deces = int(total_collecte * 0.12)
    fonds_bien_commun = int(total_collecte * 0.08)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='stat-box'><span class='fonds-title'>🏗️ 1. Fonds de Développement (60%)</span><br><span style='color:gray; font-size:12px;'>Bloqué pour l'Électricité</span><div class='fonds-montant'>{fonds_dev:,} FCFA</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-box'><span class='fonds-title'>🩺 2. Enveloppe Santé (20%)</span><br><span style='color:gray; font-size:12px;'>Urgences médicales</span><div class='fonds-montant'>{fonds_sante:,} FCFA</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><span class='fonds-title'>🕊️ 3. Enveloppe Décès / Sinistres (12%)</span><br><span style='color:gray; font-size:12px;'>Soutien aux familles</span><div class='fonds-montant'>{fonds_deces:,} FCFA</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-box'><span class='fonds-title'>💧 4. Enveloppe Bien Commun (8%)</span><br><span style='color:gray; font-size:12px;'>Petites réparations, école</span><div class='fonds-montant'>{fonds_bien_commun:,} FCFA</div></div>", unsafe_allow_html=True)

    # --- AFFICHAGE DE LA LISTE DETAILLEE (OPTIONNEL POUR MIEUX VOIR) ---
    st.write("---")
    st.write("### 👥 Détail des membres filtrés")
    # On affiche uniquement les colonnes importantes pour le village
    st.dataframe(df_filtre[['Date', 'Nom Complet', 'Résidence', 'Montant FCFA', 'Mode paiement']], use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Erreur de lecture du fichier 'cotisations.csv'. Détails : {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>ASSOS NDAYANE VILLAGE | Version 2.0 avec Filtres Avancés</p>", unsafe_allow_html=True)
