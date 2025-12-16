import streamlit as st
import pandas as pd

# Base de données simple
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Nom','Rôle','Matière','Jour','Heure','Salle'])

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("Tutorat Connect")

# Formulaire d'inscription
st.subheader("Ajouter une séance")
nom = st.text_input("Nom")
role = st.selectbox("Rôle", ["Tuteur", "Tutoré"])
matiere = st.text_input("Matière")
jour = st.selectbox("Jour", ["Lundi","Mardi","Mercredi","Jeudi","Vendredi"])
heure = st.text_input("Heure (ex: 14h)")
salle = st.text_input("Salle (ex: CDI)")

if st.button("Ajouter séance"):
    st.session_state.data = st.session_state.data.append(
        {'Nom':nom,'Rôle':role,'Matière':matiere,'Jour':jour,'Heure':heure,'Salle':salle},
        ignore_index=True)
    st.success("Séance ajoutée !")

# Affichage du planning
st.subheader("Planning des séances")
st.dataframe(st.session_state.data)

# Recherche tuteur/tutoré
st.subheader("Chercher un tuteur ou tutoré")
recherche_matiere = st.text_input("Matière à rechercher")
if recherche_matiere:
    resultats = st.session_state.data[st.session_state.data['Matière'].str.contains(recherche_matiere, case=False)]
    st.dataframe(resultats)

# Messagerie simple
st.subheader("Envoyer un message")
expediteur = st.text_input("Votre nom")
destinataire = st.text_input("Nom du destinataire")
message = st.text_area("Message")
if st.button("Envoyer message"):
    st.session_state.messages.append(f"{expediteur} -> {destinataire}: {message}")
    st.success("Message envoyé !")

st.subheader("Messages")
for msg in st.session_state.messages:
    st.write(msg)
