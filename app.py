import streamlit as st
import sqlite3
from datetime import datetime

# Connexion à la base
conn = sqlite3.connect('tutorat.db', check_same_thread=False)
c = conn.cursor()

st.set_page_config(page_title="Tutorat Lycée", layout="wide")
st.title("Tutorat Lycée - Prototype")

# --- LOGIN ---
st.sidebar.header("Connexion")
identifiant = st.sidebar.text_input("Identifiant")
mot_de_passe = st.sidebar.text_input("Mot de passe", type="password")
login_btn = st.sidebar.button("Se connecter")

if login_btn:
    c.execute("SELECT * FROM eleves WHERE identifiant=? AND mot_de_passe=?", (identifiant, mot_de_passe))
    user = c.fetchone()
    if user:
        st.success(f"Bienvenue {user[2]} {user[1]} ! Classe : {user[5]}")
        classe = user[5]
        user_id = user[0]
        user_role = user[7]

        # --- Affichage élèves de la même classe ---
        c.execute("SELECT * FROM eleves WHERE classe=?", (classe,))
        eleves_classe = c.fetchall()

        st.subheader("Élèves de votre classe")
        for e in eleves_classe:
            if e[0] != user_id:
                st.write(f"**{e[2]} {e[1]}** - {e[7]}")
                
                # Affichage matières disponibles pour tutoré
                if user_role == "Tutoré" and e[7] == "Tuteur":
                    c.execute("SELECT nom FROM matieres")
                    matieres = [m[0] for m in c.fetchall()]
                    for m in matieres:
                        if st.button(f"Demander {m} à {e[2]} {e[1]}", key=f"{e[0]}_{m}"):
                            # Ajouter la demande
                            date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                            c.execute("""INSERT INTO demandes (tutore_id, tuteur_id, matiere, statut, date)
                                         VALUES (?,?,?,?,?)""",
                                      (user_id, e[0], m, "en attente", date_now))
                            conn.commit()
                            st.success(f"Demande envoyée pour {m} !")
                            st.info(f"Email de notification envoyé à {e[2]} {e[1]} (simulation).")

        # --- Affichage demandes reçues pour les tuteurs ---
        if user_role == "Tuteur":
            st.subheader("Demandes de tutorat reçues")
            c.execute("SELECT d.id, e.prenom, e.nom, d.matiere, d.statut FROM demandes d JOIN eleves e ON d.tutore_id=e.id WHERE d.tuteur_id=? AND d.statut='en attente'", (user_id,))
            demandes = c.fetchall()
            for d in demandes:
                st.write(f"{d[1]} {d[2]} - {d[3]}")
                col1, col2 = st.columns(2)
                if col1.button("Accepter", key=f"accepter_{d[0]}"):
                    c.execute("UPDATE demandes SET statut='acceptée' WHERE id=?", (d[0],))
                    conn.commit()
                    st.success(f"Tutorat accepté pour {d[3]}")
                if col2.button("Refuser", key=f"refuser_{d[0]}"):
                    c.execute("UPDATE demandes SET statut='refusée' WHERE id=?", (d[0],))
                    conn.commit()
                    st.warning(f"Tutorat refusé pour {d[3]}")

    else:
        st.error("Identifiant ou mot de passe incorrect.")
