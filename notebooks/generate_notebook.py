import nbformat as nbf

nb = nbf.v4.new_notebook()

text_intro = """\
# Analyse Exploratoire et Classification de Malwares
Ce notebook présente une approche de bout en bout pour la classification de malwares à partir de l'analyse statique des fichiers PE.
Il suit les objectifs suivants :
1. Prétraitement et analyse exploratoire du dataset.
2. Évaluation comparative multimodèle (SVM, Random Forest, KNN).
3. Optimisation du meilleur modèle via GridSearchCV.
"""

code_load = """\
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le dataset généré
df = pd.read_excel('../data/dataset_malware.xlsx')
df.head()
"""

text_eda = """\
## Analyse Exploratoire des Données (EDA)
Observons la répartition des classes et les corrélations entre nos caractéristiques (Features).
"""

code_eda = """\
# Visualisation de la distribution des classes
plt.figure(figsize=(6,4))
sns.countplot(x='Label', data=df)
plt.title('Distribution: Sain (0) vs Malveillant (1)')
plt.show()

# Matrice de corrélation
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matrice de Corrélation')
plt.show()
"""

text_model = """\
## Apprentissage Supervisé
Nous allons comparer SVM, Random Forest et KNN, et évaluer leurs performances (F1-Score, Précision, Rappel).
"""

code_model = """\
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, f1_score

# Séparation Features / Target
X = df.drop('Label', axis=1)
y = df['Label']

# Normalisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split Train/Test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# Modèles
models = {
    'SVM': SVC(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'KNN': KNeighborsClassifier()
}

# Évaluation
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"--- {name} ---")
    print(classification_report(y_test, y_pred))
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_intro),
    nbf.v4.new_code_cell(code_load),
    nbf.v4.new_markdown_cell(text_eda),
    nbf.v4.new_code_cell(code_eda),
    nbf.v4.new_markdown_cell(text_model),
    nbf.v4.new_code_cell(code_model)
]

with open('notebooks/exploration_malware.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook generated in notebooks/exploration_malware.ipynb")
