import streamlit as st

# Configuration de la page et du design
st.set_page_config(
    page_title="IA Vigilance - ADN Ndayane",
    page_icon="🇸🇳",
    layout="centered"
)

# Style CSS pour appliquer les couleurs du Sénégal (Vert, Or, Rouge)
st.markdown("""
    <style>
    /* Couleur du titre principal */
    .main-title {
        color: #008543; /* Vert du Sénégal */
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #E31B23; /* Rouge du Sénégal */
        text-align: center;
        font-size: 18px;
        font-weight: 500;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    /* Bouton personnalisé couleur Or/Jaune */
    div.stButton > button:first-child {
        background-color: #FDEF42; /* Or du Sénégal */
        color: #000000;
        font-weight: bold;
        border: 2px solid #008543;
        width: 100%;
        border-radius: 8px;
        height: 3em;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #008543;
        color: #FFFFFF;
        border: 2px solid #FDEF42;
    }
    /* Cadres de résultats */
    .valide-box {
        padding: 20px;
        background-color: #E6F4EA;
        border-left: 8px solid #008543;
        border-radius: 8px;
        color: #137333;
    }
    .refuse-box {
        padding: 20px;
        background-color: #FCE8E6;
        border-left: 8px solid #E31B23;
        border-radius: 8px;
        color: #C5221F;
    }
    </style>
""", unsafe_allow_html=True)

# Affichage du Drapeau du Sénégal et du Titre
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Utilisation d'un emoji de grand drapeau ou image SVG officielle
    st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom:0;'>🇸🇳</h1>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ADN NDAYANE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Système d'IA & Vigilance Financière Communautaire</p>", unsafe_allow_html=True)

st.write("---")
st.write("### 📋 Formulaire d'évaluation d'une demande sociale")
st.write("Le Trésorier ou le Secrétaire doit remplir les champs ci-dessous pour interroger l'IA.")

# Simulation de la base de données locale des 85 membres
membres_db = {
    "Samba Diouf (ID: 01)": {"a_jour": True},
    "Ami Collé (ID: 02)": {"a_jour": True},
    "Modou Sène (ID: 03)": {"a_jour": True},
    "Ibrahima Ka (ID: 04)": {"a_jour": False},  # En retard
    "Fatou Binetou Diop (ID: 05)": {"a_jour": True}
}

# Formulaire interactif
nom_selectionne = st.selectbox("1. Sélectionner le membre demandeur :", list(membres_db.keys()))

type_evenement = st.selectbox(
    "2. Quel est le domaine ou motif de la demande ?",
    ["Sélectionner...", "Santé (Évacuation, Ordonnance)", "Décès (Forfait funérailles)", "Baptême / Mariage", "Fête religieuse (Magal, Gamou)", "Autre besoin privé"]
)

beneficiaire = st.text_input("3. Qui est le bénéficiaire direct au village ? (Ex: Fils, Épouse, Maman, Lui-même...)")
montant = st.number_input("4. Montant demandé (en FCFA) :", min_value=0, step=5000, value=15000)

st.write("")
analyser = st.button("🚀 INTERROGER L'IA DE VIGILANCE")

# Logique de décision de l'IA affichée au clic
if analyser:
    if type_evenement == "Sélectionner..." or not beneficiaire:
        st.warning("⚠️ Veuillez remplir tous les champs du formulaire avant d'interroger l'IA.")
    else:
        st.write("### 🤖 Verdict de l'IA de Ndayane :")
        
        # Vérification du statut de cotisation
        est_a_jour = membres_db[nom_selectionne]["a_jour"]
        
        if not est_a_jour:
            st.markdown(f"""
                <div class='refuse-box'>
                    <h3>🔴 DEMANDE REFUSÉE</h3>
                    <p><b>Raison :</b> Le membre <b>{nom_selectionne}</b> présente un retard de cotisation supérieur à 3 mois. Selon l'Article 1 de la Charte, ses droits sociaux sont temporairement suspendus.</p>
                    <p><i>Conseil de l'IA : Invitez le membre à régulariser ses cotisations en retard pour réactiver immédiatement ses droits.</i></p>
                </div>
            """, unsafe_allow_html=True)
            
        elif "Santé" in type_evenement:
            st.markdown(f"""
                <div class='valide-box'>
                    <h3>🟢 DEMANDE VALIDÉE</h3>
                    <p><b>Enveloppe :</b> Santé & Urgences Médicales (Enveloppe A - 50% du bloc social)</p>
                    <p><b>Action pour le Trésorier :</b> Vous pouvez décaisser la somme de <b>{montant:,} FCFA</b>.</p>
                    <p><b>Règle appliquée :</b> Le membre est à jour et le motif correspond à une urgence vitale visant à soigner un proche à charge ({beneficiaire}). Un reçu de caisse doit être signé.</p>
                </div>
            """, unsafe_allow_html=True)
            
        elif "Décès" in type_evenement:
            forfait_deces = min(montant, 50000)
            st.markdown(f"""
                <div class='valide-box'>
                    <h3>🟢 DEMANDE VALIDÉE</h3>
                    <p><b>Enveloppe :</b> Solidarité Décès (Enveloppe C - 20% du bloc social)</p>
                    <p><b>Action pour le Trésorier :</b> Remettre le forfait deuil de <b>{forfait_deces:,} FCFA</b> à la famille.</p>
                    <p><b>Règle appliquée :</b> Événement de deuil éligible pour un membre actif. L'aide est plafonnée à 50 000 FCFA maximum pour préserver la caisse.</p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
                <div class='refuse-box'>
                    <h3>🔴 DEMANDE REFUSÉE</h3>
                    <p><b>Raison :</b> Le motif sélectionné (<b>{type_evenement}</b>) concerne un événement festif ou privé.</p>
                    <p><b>Règle appliquée :</b> L'Article 5 de la Charte de Ndayane interdit strictement l'utilisation de l'argent collectif pour les mariages, baptêmes ou fêtes privées. Ces fonds appartiennent au développement du village.</p>
                </div>
            """, unsafe_allow_html=True)

# Bas de page officiel
st.write("")
st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Association pour le Développement de Ndayane — Commune de Tocky Gare, Diourbel, Sénégal.<br><i>Outil sécurisé par arbre de décision économétrique sous Python.</i></p>", unsafe_allow_html=True)
