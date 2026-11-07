import streamlit as st
import pandas as pd

# 1. Configuration de la page et masquage complet de la barre GitHub
st.set_page_config(page_title="ASSOS NDAYANE - Prévoyance", page_icon="🇸🇳", layout="centered")

st.markdown("""
    <style>
    /* Sécurité absolue : masquer la barre supérieure de Streamlit/GitHub */
    [data-testid="stHeader"] { display: none !important; }
    .block-container { padding-top: 2rem !important; }
    
    /* Titres professionnels aux couleurs du Sénégal */
    .header-container { text-align: center; padding-bottom: 20px; }
    .flag-style { font-size: 70px; margin: 0px; line-height: 1; }
    .main-title { color: #008543; font-family: 'Segoe UI', sans-serif; font-weight: 800; font-size: 36px; margin-top: 5px; margin-bottom: 0px; }
    .sub-title { color: #E31B23; font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: 600; margin-top: 2px; margin-bottom: 20px; }
    
    /* Bouton d'interrogation Or/Jaune */
    div.stButton > button:first-child { background-color: #FDEF42; color: #000000; font-weight: bold; border: 2px solid #008543; width: 100%; border-radius: 8px; height: 3em; }
    div.stButton > button:first-child:hover { background-color: #008543; color: #FFFFFF; border: 2px solid #FDEF42; }
    
    /* Boîtes de dialogues de résultats */
    .valide-box { padding: 20px; background-color: #E6F4EA; border-left: 8px solid #008543; border-radius: 8px; color: #137333; margin-bottom: 15px;}
    .refuse-box { padding: 20px; background-color: #FCE8E6; border-left: 8px solid #E31B23; border-radius: 8px; color: #C5221F; margin-bottom: 15px;}
    </style>
""", unsafe_allow_html=True)

# EN-TÊTE DU MODULE DE PRÉVOYANCE
st.markdown("""
    <div class='header-container'>
        <div class='flag-style'>🇸🇳</div>
        <h1 class='main-title'>ASSOS NDAYANE VILLAGE</h1>
        <p class='sub-title'>Méthode 2 : Système de Prévoyance & Contrôle Social</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# 2. Lecture sécurisée du fichier cotisations.csv
try:
    df = pd.read_csv("cotisations.csv")
    df.columns = df.columns.str.strip()
    
    # Nettoyage et fusion prénom/nom pour une recherche simplifiée
    df['Nom'] = df['Nom'].fillna('').astype(str).str.strip()
    df['Prénom'] = df['Prénom'].fillna('').astype(str).str.strip()
    df['Nom Complet'] = df['Nom'] + " " + df['Prénom']
    
    # Suppression des lignes vides
    df = df[df['Nom Complet'].str.len() > 2]
    df = df.sort_values(by='Nom Complet')
    liste_membres = df['Nom Complet'].unique()
    
    st.write("### 📋 Formulaire d'Évaluation de Vigilance")
    st.write("Renseignez les critères de la demande pour obtenir le verdict automatique de l'IA :")
    
    # Formulaire utilisateur interactif
    nom_selectionne = st.selectbox("1. Sélectionner le membre demandeur :", liste_membres)
    
    type_evenement = st.selectbox(
        "2. Quel est le motif de la demande d'aide ?",
        ["Sélectionner...", "Urgence Santé (Évacuation, Ordonnance médicale)", "Bien Commun (Réparation infrastructures village)", "Solidarité Décès / Sinistre lourd", "Autre besoin privé (Baptême, Mariage, Cérémonie)"]
    )
    
    beneficiaire = st.text_input("3. Indiquer le nom du bénéficiaire au village :")
    montant_demande = st.number_input("4. Montant d'argent nécessaire (en FCFA) :", min_value=0, step=5000, value=0)
    
    st.write("")
    bouton = st.button("🚀 EFFECTUER LE CONTRÔLE FINANCIER DE L'IA")
    
    if bouton:
        if type_evenement == "Sélectionner..." or not beneficiaire or montant_demande == 0:
            st.warning("⚠️ Veuillez remplir tous les champs obligatoires et inscrire un montant supérieur à 0.")
        else:
            st.write("### 🤖 Décision de l'IA basée sur la Charte :")
            
            # Vérification du statut de paiement dans la colonne 'Montant FCFA'
            ligne_membre = df[df['Nom Complet'] == nom_selectionne].iloc
            valeur_payee = pd.to_numeric(ligne_membre.get('Montant FCFA', 0), errors='coerce')
            if pd.isna(valeur_payee):
                valeur_payee = 0
                
            a_cotise = float(valeur_payee) >= 1000
            
            # Application stricte de la Charte de Vigilance
            if not a_cotise:
                st.markdown(f"""
                    <div class='refuse-box'>
                        <h3>🔴 DEMANDE REFUSÉE (Membre non à jour)</h3>
                        <p><b>Raison :</b> Le membre <b>{nom_selectionne}</b> ne figure pas comme ayant réglé sa cotisation de 1 000 FCFA pour le mois en cours.</p>
                        <p><i>Règle appliquée : Les enveloppes de solidarité sont réservées exclusivement aux membres actifs et à jour.</i></p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Santé" in type_evenement:
                # Application du plafond Santé : 50 000 FCFA max
                montant_valide = min(montant_demande, 50000)
                note_plafond = "⚠️ Le montant demandé dépassait la limite autorisée. Le montant a été ajusté au plafond de 50 000 FCFA." if montant_demande > 50000 else ""
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 ENVELOPPE SANTÉ VALIDÉE</h3>
                        <p><b>Enveloppe d'imputation :</b> Enveloppe A (Santé - 20% de la collecte globale)</p>
                        <p><b>Montant accordé au Trésorier :</b> <span style='font-size:20px; font-weight:bold;'>{montant_valide:,} FCFA</span> (Limite max : 50 000 FCFA)</p>
                        <p style='color:#b58105; font-weight:600;'>{note_plafond}</p>
                        <p><b>Bénéficiaire enregistré :</b> {beneficiaire}</p>
                        <p><i>Note : Veuillez faire signer le reçu de caisse d'urgence.</i></p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Bien Commun" in type_evenement:
                # Application du plafond Bien Commun : 25 000 FCFA max
                montant_valide = min(montant_demande, 25000)
                note_plafond = "⚠️ Le montant demandé dépassait le budget alloué par cas. Ajusté au plafond de 25 000 FCFA." if montant_demande > 25000 else ""
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 FINANCEMENT BIEN COMMUN VALIDÉ</h3>
                        <p><b>Enveloppe d'imputation :</b> Enveloppe B (Bien Commun - 8% de la collecte globale)</p>
                        <p><b>Montant alloué :</b> <span style='font-size:20px; font-weight:bold;'>{montant_valide:,} FCFA</span> (Limite max : 25 000 FCFA)</p>
                        <p style='color:#b58105; font-weight:600;'>{note_plafond}</p>
                        <p><b>Projet communautaire visé :</b> {beneficiaire}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            elif "Décès" in type_evenement:
                # ALIGNÉ SUR LES AUTRES : Application du plafond Décès de 50 000 FCFA max
                montant_valide = min(montant_demande, 50000)
                note_plafond = "⚠️ Le montant demandé dépassait la limite autorisée. Le montant a été ajusté au plafond de 50 000 FCFA." if montant_demande > 50000 else ""
                st.markdown(f"""
                    <div class='valide-box'>
                        <h3>🟢 ENVELOPPE DÉCÈS / SINISTRE VALIDÉE</h3>
                        <p><b>Enveloppe d'imputation :</b> Enveloppe C (Décès / Sinistres - 12% de la collecte globale)</p>
                        <p><b>Montant accordé au Trésorier :</b> <span style='font-size:20px; font-weight:bold;'>{montant_valide:,} FCFA</span> (Limite max : 50 000 FCFA)</p>
                        <p style='color:#b58105; font-weight:600;'>{note_plafond}</p>
                        <p><b>Famille soutenue :</b> Concession de {nom_selectionne} (Défunt : {beneficiaire})</p>
                    </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                    <div class='refuse-box'>
                        <h3>🔴 DEMANDE INTERDITE (Dépense non sociale)</h3>
                        <p><b>Motif détecté :</b> Dépense privée / Cérémoniale ({type_evenement})</p>
                        <p><b>Règle de la Charte de Ndayane :</b> Il est strictement interdit d'utiliser l'argent collectif pour les fêtes privées (baptêmes, mariages, Magal, Gamou). Ces fonds appartiennent au développement du village.</p>
                    </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Erreur d'accès aux données. Assurez-vous que le fichier 'cotisations.csv' est présent sur GitHub. Détails : {e}")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>ASSOS NDAYANE VILLAGE | Module Prévoyance Harmonisé</p>", unsafe_allow_html=True)
