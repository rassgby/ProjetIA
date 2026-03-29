import streamlit as st
import requests
import pandas as pd
import time

# Configuration globale de la page
st.set_page_config(
    page_title="Scanner de Malwares PE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remplacement du style CSS de base pour embellir l'interface
st.markdown("""
    <style>
    .malicious-box {
        background-color: #ffcccc;
        color: #990000;
        border-left: 8px solid #ff0000;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .benign-box {
        background-color: #ccffcc;
        color: #006600;
        border-left: 8px solid #00cc00;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---> Barre latérale (Sidebar) <---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/shield.png", width=100)
    st.title("À propos du Projet")
    st.info(
        "Ce projet démontre comment l'**apprentissage supervisé** peut classifier "
        "des fichiers exécutables en tant que sains (benign) ou malveillants "
        "via une **analyse statique** sans risque d'exécution."
    )
    st.markdown("---")
    st.markdown("### ⚙️ Moteur d'Analyse")
    st.markdown("- **Algorithme :** SVM optimisé")
    st.markdown("- **F1-Score :** ~1.00 (CV)")
    st.markdown("- **Format analysé :** PE (.exe, .dll)")
    st.markdown("---")
    st.caption("Développé pour l'évaluation Machine Learning • Mars 2026")

# ---> Zone principale <---
st.title("🛡️ Détecteur Intelligent de Malwares")
st.markdown("Analysez vos fichiers exécutables Windows en toute sécurité. Notre modèle d'Intelligence Artificielle inspecte la structure du fichier avec l'algorithme SVM pour détecter des anomalies.")

st.markdown("### 1. Uploadez un fichier")
uploaded_file = st.file_uploader("📥 Glissez-déposez un exécutable (.exe ou .dll) ici", type=['exe', 'dll'], help="La taille est indicative, l'analyse porte sur la structure.")

if uploaded_file is not None:
    st.markdown("### 2. Résultats de l'Analyse")
    
    # Barre de progression pour améliorer l'expérience utilisateur
    progress_text = "Décompression et analyse de la structure PE en cours..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.005) # Petite pause simulant le temps de calcul
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

    with st.spinner("Interrogation du modèle IA (API FastAPI)..."):
        try:
            # Envoi du fichier à FastAPI
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
            start_time = time.time()
            response = requests.post("http://localhost:8000/predict/", files=files)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                
                # Disposition en 2 colonnes pour l'alerte et les compteurs
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Affichage d'une boîte d'alerte personnalisée
                    if result['prediction'] == "Malicious":
                        st.markdown(f'<div class="malicious-box"><h3>🚨 ATTENTION : Fichier Malveillant</h3><p>Le fichier <b>{result["filename"]}</b> présente une structure typique de malware. <br>Niveau de confiance : <b>{result["confidence"]}</b>.</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="benign-box"><h3>✅ Fichier Sain</h3><p>Aucun comportement suspect détecté dans <b>{result["filename"]}</b>. <br>Niveau de confiance : <b>{result["confidence"]}</b>.</p></div>', unsafe_allow_html=True)
                
                with col2:
                    st.metric(label="⏱️ Durée", value=f"{end_time - start_time:.3f} s")
                    st.metric(label="🔌 Statut API", value="Connecté", delta="200 OK")
                
                st.markdown("---")
                st.markdown("### 🔍 Caractéristiques Structurelles Extraites")
                st.write("Voici les métadonnées que l'Intelligence Artificielle a analysées (Features) :")
                
                features = result['features_extracted']
                
                # Remplacement du vieux tableau par des métriques visuelles stylisées
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Taille du Binaire", f"{features.get('SizeOfImage', 0) / 1024:.1f} KB")
                
                # l'Entropie (si > 7, c'est souvent packé/crypté)
                entropy = features.get('Entropy', 0)
                m2.metric("Entropie (0-8)", f"{entropy:.2f}", delta="Élevée (packé?)" if entropy > 7.0 else "Normale", delta_color="inverse")
                
                m3.metric("Nb de Sections", features.get('NumberOfSections', 0))
                m4.metric("Nb d'Imports", features.get('Imports', 0))
                m5.metric("Nb d'Exports", features.get('Exports', 0))
                
                # Accordéon pour les logs / data brutes
                with st.expander("Voir la réponse JSON brute du backend"):
                    st.json(result)
                    
            else:
                st.error(f"❌ Erreur du serveur ({response.status_code}): {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ L'API FastAPI n'est pas accessible.")
            st.info("Avez-vous bien lancé la commande `python3 app/main.py` dans un second terminal ?")

st.markdown("<br><br><center><small>Interface propulsée par Streamlit & FastAPI</small></center>", unsafe_allow_html=True)
