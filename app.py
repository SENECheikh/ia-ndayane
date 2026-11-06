import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="IA Vigilance - ADN Ndayane", page_icon="🇸🇳", layout="centered")

# Design aux couleurs du Sénégal (Vert, Or, Rouge)
st.markdown("""
    <style>
    .main-title { color: #008543; font-family: 'Helvetica Neue', sans-serif; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .sub-title { color: #E31B23; text-align: center; font-size: 18px; font-weight: 500; margin-bottom: 25px; }
    div.stButton > button:first-child { background-color: #FDEF42; color: #000000; font-weight: bold; border: 2px solid #008543; width: 100%; border-radius: 8px; height: 3em; }
    div.stButton > button:first-child:hover { background-color: #008543; color: #FFFFFF; border: 2px solid #FDEF42; }
    .valide-box { padding: 20px; background-color: #E6F4EA; border-left: 8px solid #008543; border-radius: 8px; color: #137333; margin-bottom: 15px;}
    .refuse-box { padding: 20px; background-color: #FCE8E6; border-left: 8px solid #E31B23; border-radius: 8px; color: #C5221F; margin-bottom: 15px;}
    .stat-box { padding: 15px; background-color: #F8F9FA; border: 1px solid #E0E0E0; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("<h1 style='text-align: center; font-size: 70px; margin-bottom:0;'>🇸🇳</h1>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>ADN NDAYANE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Système d'IA conforme à la Charte de Répartition</p>", unsafe_allow_html=True)
st.write("---")

# 2. Chargement des données réelles (votre fichier cotisations.csv)
try:
    df = pd.read_csv("cotisations.csv")
    # Nettoyage des colonnes
    df.columns = df.columns.str.strip()
    
    # Nettoyage et fusion Nom/Prénom
    df['Nom'] = df['Nom'].fillna('').astype(str).str.strip()
    df['Prénom'] = df['Prénom'].fillna('').astype(str).str.strip()
    df['Nom Complet'] = df['Nom'] + " " + df['Prénom']
    
    # Supprimer les lignes vides ou de statistiques du bas si elles existent
    df = df[df['Nom Complet'].str.len() > 2]
    df = df.sort_values(by='Nom Complet')
    
    # --- TABLEAU DE BORD DE LA COLLECTE (METHODE 1) ---
    st.write("### 📊 Calculateur Automatique de Répartition (Méthode 1)")
    
    # Calcul du montant total collecté sur le fichier
    df['Montant FCFA'] = pd.to_numeric(df['Montant FCFA'], errors='coerce').fillna(0)
    total_collecte = int(df['Montant FCFA'].sum())
    
    # Application des pourcentages exacts de votre document
    fonds_dev = int(total_collecte * 0.60)
    fonds_sante = int(total_collecte * 0.20)
    fonds_bien_commun = int(total_collecte * 0.08)
    fonds_deces = int(total_collecte * 0.12)
    
    st.info(f"💰 **Montant total enregistré ce mois-ci : {total_collecte:,} FCFA**")
    
    # Affichage des 4 blocs de répartition en colonnes
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='stat-box'><b>🏗️ Dével. (60%)</b><br><span style='color:#008543; font-size:18px; font-weight:bold;'>{fonds_dev:,} FCFA</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-box' style='margin-top:10px;'><b>🩺 Santé (20%)</b><br><span style='color:#008543; font-size:18px; font-weight:bold;'>{fonds_sante:,} FCFA</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-box'><b>💧 Bien Commun (8%)</b><br><span style='color:#008543; font-size:18px; font-weight:bold;'>{fonds_bien_commun:,} FCFA</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-box' style='margin-top:10px;'><b>🕊️ Décès / Sinistre (12%)</b><br><span style='color:#008543; font-size:18px; font-weight:bold;'>{fonds_deces:,} FCFA</span></div>", unsafe_allow_html=True)

    st.write("---")
    
    # --- EVALUATION DES CAS (METHODE 2) ---
    st.write("### 🤖 Évaluation Sociale de Vigilance (Méthode 2)")
    
    liste_membres = df['Nom Complet'].unique()
    nom_selectionne = st.selectbox("1. Sélectionner le membre demandeur :", liste_membres)
    
    type_evenement = st.selectbox(
        "2. Quel est le motif de la demande ?",
        ["Sélectionner...", "Urgence Santé (Évacuation, Ordonnance)", "Bien Commun (Réparation, Puits, École)", "Solidarité Décès / Sinistre", "Autre motif privé (Baptême, Mariage, etc.)"]
    )
    
    beneficiaire = st.text_input("3. Indiquer le bénéficiaire direct au village :")
    montant_demande = st.number_input("4. Montant nécessaire (en FCFA) :", min_value=0, step=5000, value=0)
    
    st.write("")
    bouton = st.button("🚀 EFFECTUER LE CONTRÔLE FINANCIER")
    
    if bouton:
        if type_evenement == "Sélectionner..." or not beneficiaire or montant_demande == 0:
            st.warning("⚠️ Veuillez remplir tous les champs du formulaire avec un montant supérieur à 0.")
        else:
            # Vérification si le membre a payé au moins 1000 FCFA
            ligne_membre = df[df['Nom Complet'] == nom_selectionne].iloc[0]
            a_cotise = float(ligne_membre['Montant FCFA']) >= 1000
            
            if not a_cotise:
                st.markdown(f"""
                    <div class='refuse-box'>
                        <h3>🔴 DEMANDE REFUSÉE (Membre non à jour)</h3>
                        <p><b>Raison :</b> Le membre <b>{nom_selectionne}</b> n'est pas à jour de sa cotisation de 1 000 FCFA pour le mois sélectionné.</p>
                        <p><i>Règle de vigilance : Les droits sociaux sont suspendus tant que la cotisation n'est pas régularisée sur Wave.</i></p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Santé" in type_evenement:
                # Plafond Santé : 50 000 FCFA
                montant_valide = min(montant_demande, 50000)
                depassement = "⚠️ Le montant demandé dépassait le plafond. Ajusté à 50 000 FCFA." if montant_demande > 50000 else ""
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 DEMANDE VALIDÉE</h3>
                        <p><b>Enveloppe impactée :</b> Enveloppe A (Urgences Santé)</p>
                        <p><b>Montant accordé :</b> <b>{montant_valide:,} FCFA</b> (Plafond max : 50 000 FCFA)</p>
                        <p style='color:orange;'><b>{depassement}</b></p>
                        <p><b>Instruction :</b> Décaisser l'argent pour l'urgence médicale de : <i>{beneficiaire}</i>.</p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Bien Commun" in type_evenement:
                # Plafond Bien Commun : 25 000 FCFA
                montant_valide = min(montant_demande, 25000)
                depassement = "⚠️ Le montant demandé dépassait le plafond. Ajusté à 25 000 FCFA." if montant_demande > 25000 else ""
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 DEMANDE VALIDÉE</h3>
                        <p><b>Enveloppe impactée :</b> Enveloppe B (Bien Commun)</p>
                        <p><b>Montant accordé :</b> <b>{montant_valide:,} FCFA</b> (Plafond max : 25 000 FCFA selon le projet)</p>
                        <p style='color:orange;'><b>{depassement}</b></p>
                        <p><b>Instruction :</b> Financement autorisé pour l'infrastructure collective.</p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Décès" in type_evenement:
                # Forfait Fixe de 50 000 FCFA
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 FORFAIT DEUIL VALIDÉ</h3>
                        <p><b>Enveloppe impactée :</b> Enveloppe C (Solidarité Décès / Sinistre)</p>
                        <p><b>Montant accordé :</b> <b>50 000 FCFA</b> (Forfait Fixe obligatoire)</p>
                        <p><b>Instruction :</b> Remettre l'enveloppe de soutien de 50 000 FCFA à la famille pour les funérailles.</p>
                    </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                    <div class='refuse-box'>
                        <h3>🔴 DEMANDE REFUSÉE (Motif non social)</h3>
                        <p><b>Motif :</b> {type_evenement}</p>
                        <p><b>Règle appliquée :</b> L'utilisation des fonds pour des fêtes privées (baptêmes, mariages) est strictement interdite par la Charte de Ndayane.</p>
                    </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Erreur d'intégration. Assurez-vous que le fichier est bien nommé 'cotisations.csv' sur votre GitHub. Détails : {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>Association pour le Développement de Ndayane (Diourbel) | Code Python Automatisé</p>", unsafe_allow_html=True)
