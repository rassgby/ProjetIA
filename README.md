# Classification de Malwares par Analyse Statique

Ce projet propose un outil de machine learning paré pour la détection de malwares (fichiers PE : `.exe` et `.dll`) sans exécution (analyse statique).

## Objectifs 
- **Entraînement de Modèle** : Comparaison de SVM, RF et KNN.
- **Micro-service** : Déploiement via une API avec FastAPI.
- **Interface Graphique** : Accès simplifié via Streamlit.

## Architecture du projet 

```
├── app/
│   ├── main.py              # API FastAPI pour l'inférence
│   ├── streamlit_app.py     # Interface utilisateur Streamlit
│   └── model/
│       ├── train_model.py   # Script d'entraînement pour générer les modèles
│       ├── malware_classifier.pkl
│       └── scaler.pkl
├── data/
│   ├── generate_data.py     # Script pour générer de fausses données PE (.xlsx)
│   └── dataset_malware.xlsx # Le dataset final
├── notebooks/
│   └── exploration_malware.ipynb  # L'analyse exploratoire et test des modèles (EDA)
├── README.md                # Ce fichier
└── requirements.txt         # Dépendances Python
```

## Étapes de Lancement

### 1. Installation 
```bash
pip install -r requirements.txt
```

### 2. Entraînement et Génération des Données (Optionnel si les .pkl sont déjà là)
```bash
python3 data/generate_data.py
python3 app/model/train_model.py
```

### 3. Lancer l'API (Backend)
Dans un terminal de commandes :
```bash
python3 app/main.py
# L'API FastAPI sera disponible sur http://localhost:8000
```

### 4. Lancer Streamlit (Interface)
Dans un autre terminal :
```bash
streamlit run app/streamlit_app.py
# L'interface Streamlit s'ouvrira sur http://localhost:8501
```

🎉 Uploadez un fichier et obtenez la prédiction instantanée !
