import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('images', exist_ok=True)

# Load dataset
df = pd.read_excel('data/dataset_malware.xlsx')

# 1. Class distribution
plt.figure(figsize=(8,5))
sns.countplot(x='Label', data=df, palette='Set2')
plt.title('Distribution des classes: Sain (0) vs Malveillant (1)')
plt.xlabel('Classe')
plt.ylabel('Nombre d\'échantillons')
plt.savefig('images/class_distribution.png', bbox_inches='tight')
plt.close()

# 2. Correlation matrix
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matrice de Corrélation des Features')
plt.savefig('images/correlation_matrix.png', bbox_inches='tight')
plt.close()

# 3. Entropy distribution
plt.figure(figsize=(8,5))
sns.histplot(data=df, x='Entropy', hue='Label', kde=True, palette='Set1', bins=30)
plt.title('Distribution de l\'Entropie par Classe')
plt.xlabel('Entropie')
plt.ylabel('Fréquence')
plt.savefig('images/entropy_distribution.png', bbox_inches='tight')
plt.close()

# 4. Model comparison
models = ['SVM', 'Random Forest', 'KNN']
f1_scores = [1.000, 0.998, 1.000]
plt.figure(figsize=(8,5))
sns.barplot(x=models, y=f1_scores, palette='viridis')
plt.ylim(0.95, 1.05)
plt.title('Comparaison du F1-Score des Modèles')
plt.ylabel('F1-Score')
for i, v in enumerate(f1_scores):
    plt.text(i, v + 0.005, str(v), color='black', ha='center')
plt.savefig('images/model_comparison.png', bbox_inches='tight')
plt.close()
