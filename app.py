import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="ASSOS NDAYANE VILLAGE", page_icon="🇸🇳", layout="centered")

# Design et styles CSS pour un rendu épuré et professionnel
st.markdown("""
    <style>
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

# EN-TÊTE OFFICIEL DE L'ASSOCIATION
st.markdown("""
    <div class='header-container'>
        <div class='flag-style'>🇸🇳</div>
        <h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1>
        <p class='sub-title'>Ventilation Automatique de la Caisse</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 2. Lecture du fichier cotisations.csv envoyé par le village
try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    
    # Conversion de la colonne Montant en nombre
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    
    # Calcul des statistiques basées sur votre fichier
    total_collecte = int(df['Montant FCFA'].sum())
    membres_total = len(df)
    membres_cotisants = int((df['Montant FCFA'] >= 1000).sum())
    membres_retard = membres_total - membres_cotisants

    # --- AFFICHAGE DU BILAN DU MOIS ---
    st.write("### 📈 Bilan de la collecte du mois")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric(label="Membres Recensés", value=f"{membres_total}")
    with col_b:
        st.metric(label="Membres Ayant Cotisé", value=f"{membres_cotisants}", delta=f"{membres_cotisants} à jour")
    with col_c:
        st.metric(label="Restant à Recouvrer", value=f"{membres_retard} pers.", delta=f"-{membres_retard}", delta_color="inverse")

    st.success(f"💰 **Montant total collecté sur Wave : {total_collecte:,} FCFA**")
    st.write("---")

    # --- VENTILATION AUTOMATIQUE (APPLICATION DES % DE LA CHARTE) ---
    st.write("### 📊 Répartition des enveloppes (Règles de la Charte)")
    st.write("Chaque mois, la somme globale est divisée automatiquement pour protéger l'argent du village :")

    # Calculs stricts des pourcentages de votre document
    fonds_dev = int(total_collecte * 0.60)
    fonds_sante = int(total_collecte * 0.20)
    fonds_deces = int(total_collecte * 0.12)
    fonds_bien_commun = int(total_collecte * 0.08)

    # Affichage en 4 grands blocs visuels
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class='stat-box'>
                <span class='fonds-title'>🏗️ 1. Fonds de Développement (60%)</span><br>
                <span style='color:gray; font-size:12px;'>Bloqué pour l'Électricité / Infrastructures</span>
                <div class='fonds-montant'>{fonds_dev:,} FCFA</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='stat-box'>
                <span class='fonds-title'>🩺 2. Enveloppe Santé (20%)</span><br>
                <span style='color:gray; font-size:12px;'>Urgences médicales et évacuations</span>
                <div class='fonds-montant'>{fonds_sante:,} FCFA</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class='stat-box'>
                <span class='fonds-title'>🕊️ 3. Enveloppe Décès / Sinistres (12%)</span><br>
                <span style='color:gray; font-size:12px;'>Soutien forfaitaire aux familles</span>
                <div class='fonds-montant'>{fonds_deces:,} FCFA</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='stat-box'>
                <span class='fonds-title'>💧 4. Enveloppe Bien Commun (8%)</span><br>
                <span style='color:gray; font-size:12px;'>Petites réparations, école, puits</span>
                <div class='fonds-montant'>{fonds_bien_commun:,} FCFA</div>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Erreur de lecture. Vérifiez que le fichier est bien nommé 'cotisations.csv' sur votre GitHub. Détails : {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>ASSOS NDAYANE VILLAGE | Étape 1 : Validation de la Méthode 1</p>", unsafe_allow_html=True)
