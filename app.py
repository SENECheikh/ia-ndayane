import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_title="IA Vigilance - ADN Ndayane", page_icon="🇸🇳", layout="centered")

# Design aux couleurs du Sénégal (Vert, Or, Rouge)
st.markdown("""
    <style>
    .main-title { color: #008543; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .sub-title { color: #E31B23; text-align: center; font-size: 18px; font-weight: 500; margin-bottom: 30px; }
    div.stButton > button:first-child { background-color: #FDEF42; color: #000000; font-weight: bold; border: 2px solid #008543; width: 100%; border-radius: 8px; height: 3em; }
    div.stButton > button:first-child:hover { background-color: #008543; color: #FFFFFF; border: 2px solid #FDEF42; }
    .valide-box { padding: 20px; background-color: #E6F4EA; border-left: 8px solid #008543; border-radius: 8px; color: #137333; }
    .refuse-box { padding: 20px; background-color: #FCE8E6; border-left: 8px solid #E31B23; border-radius: 8px; color: #C5221F; }
    </style>
""", unsafe_allow_html=True)

# En-tête de l'application
st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🇸🇳</h1>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>ADN NDAYANE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Système d'IA & Vigilance Financière Communautaire</p>", unsafe_allow_html=True)
st.write("---")

# CHARGEMENT DU FICHIER DE COTISATION (En priorité Excel, sinon CSV)
df = None
filename_used = ""

for name in ["cotisations.csv", "Tableau_Bord_IA_Ndayane.xlsx"]:
    try:
        if name.endswith('.csv'):
            df = pd.read_csv(name)
        else:
            df = pd.read_excel(name)
        filename_used = name
        break
    except:
        continue

if df is not None:
    try:
        # Nettoyage des noms de colonnes
        df.columns = df.columns.str.strip()
        
        # Création d'une identité propre en fusionnant Nom et Prénom
        df['Nom'] = df['Nom'].fillna('').astype(str).str.strip()
        df['Prénom'] = df['Prénom'].fillna('').astype(str).str.strip()
        df['Nom Complet'] = df['Nom'] + " " + df['Prénom']
        
        # Filtrer les lignes vides ou de statistiques globales dans votre structure
        df = df[df['Nom Complet'] != " "]
        
        # Tri alphabétique pour faciliter la recherche du Trésorier
        df = df.sort_values(by='Nom Complet')
        liste_membres = df['Nom Complet'].unique()
        
        st.write("### 📋 Formulaire d'évaluation d'une demande sociale")
        
        # 1. Menu déroulant dynamique branché sur vos données réelles
        nom_selectionne = st.selectbox("1. Sélectionner le membre demandeur :", liste_membres)
        
        type_evenement = st.selectbox(
            "2. Quel est le domaine ou motif de la demande ?",
            ["Sélectionner...", "Santé (Évacuation, Ordonnance)", "Décès (Forfait funérailles)", "Baptême / Mariage", "Fête religieuse (Magal, Gamou)"]
        )
        
        beneficiaire = st.text_input("3. Qui est le bénéficiaire direct au village ? (Ex: Fils, Épouse, Maman...)")
        montant = st.number_input("4. Montant demandé (en FCFA) :", min_value=0, step=5000, value=0)
        
        st.write("")
        analyser = st.button("🚀 INTERROGER L'IA DE VIGILANCE")
        
        if analyser:
            if type_evenement == "Sélectionner..." or not beneficiaire or montant == 0:
                st.warning("⚠️ Veuillez remplir tous les champs et indiquer un montant supérieur à 0.")
            else:
                st.write("### 🤖 Verdict de l'IA de Ndayane :")
                
                # Extraction des données financières du membre sélectionné
                ligne_membre = df[df['Nom Complet'] == nom_selectionne].iloc[0]
                
                # Une personne est considérée à jour si le montant FCFA récolté est égal ou supérieur à 1000
                valeur_cotisation = ligne_membre.get('Montant FCFA', 0)
                if pd.isna(valeur_cotisation):
                    valeur_cotisation = 0
                    
                est_a_jour = float(valeur_cotisation) >= 1000
                
                if not est_a_jour:
                    st.markdown(f"""
                        <div class='refuse-box'>
                            <h3>🔴 DEMANDE REFUSÉE</h3>
                            <p><b>Raison :</b> Le membre <b>{nom_selectionne}</b> n'est pas à jour. Aucun paiement de 1 000 FCFA trouvé dans le fichier pour le mois en cours.</p>
                            <p><i>Conseil de vigilance : Invitez le membre à verser sa cotisation sur le compte Wave de l'association pour débloquer ses droits sociaux.</i></p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                elif "Santé" in type_evenement:
                    st.markdown(f"""
                        <div class='valide-box'>
                            <h3>🟢 DEMANDE VALIDÉE</h3>
                            <p><b>Enveloppe :</b> Santé & Urgences Médicales (Enveloppe A)</p>
                            <p><b>Action pour le Trésorier :</b> Vous pouvez décaisser la somme de <b>{montant:,} FCFA</b>.</p>
                            <p><b>Justification :</b> Adhérent à jour. L'aide finance une urgence de santé directe pour ({beneficiaire}) vivant à Ndayane.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                elif "Décès" in type_evenement:
                    forfait_deces = min(montant, 50000)
                    st.markdown(f"""
                        <div class='valide-box'>
                            <h3>🟢 DEMANDE VALIDÉE</h3>
                            <p><b>Enveloppe :</b> Solidarité Décès (Enveloppe C)</p>
                            <p><b>Action pour le Trésorier :</b> Remettre le forfait funérailles de <b>{forfait_deces:,} FCFA</b> à la famille.</p>
                            <p><b>Justification :</b> Événement éligible. L'aide est plafonnée conformément aux règles de prévoyance de l'association.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.markdown(f"""
                        <div class='refuse-box'>
                            <h3>🔴 DEMANDE REFUSÉE</h3>
                            <p><b>Raison :</b> Le motif ('{type_evenement}') concerne une festivité privée.</p>
                            <p><b>Règle appliquée :</b> L'argent de la caisse sociale est exclusivement réservé au développement et aux accidents de la vie. Les baptêmes et mariages ne sont pas pris en charge.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"⚠️ Erreur lors de la lecture des données. Vérifiez que la structure du fichier n'a pas été modifiée. Détails : {e}")
else:
    st.error("⚠️ Aucun fichier de données trouvé. Veuillez charger 'cotisations.csv' ou 'Tableau_Bord_IA_Ndayane.xlsx' sur votre espace GitHub.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Association pour le Développement de Ndayane (Tocky Gare, Diourbel) — Connecté en temps réel à votre fichier.</p>", unsafe_allow_html=True)
