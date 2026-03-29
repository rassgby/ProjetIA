import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

def train_and_evaluate():
    # Load new dataset
    print("Loading dataset...")
    df = pd.read_csv('Copie de DatasetmalwareExtrait.csv')
    
    # 0 is malicious, 1 is legitimate -> let's flip it so 1 is malicious and 0 is benign to match previous convention and malware detection standard
    df['Label'] = 1 - df['legitimate']
    df = df.drop('legitimate', axis=1)

    # Recreate graphs based on new dataset
    os.makedirs('images', exist_ok=True)
    
    plt.figure(figsize=(6,4))
    sns.countplot(x='Label', data=df)
    plt.title('Distribution: Sain (0) vs Malveillant (1)')
    plt.savefig('images/class_distribution.png')
    plt.close()

    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matrice de Corrélation')
    plt.savefig('images/correlation_matrix.png')
    plt.close()

    if 'AddressOfEntryPoint' in df.columns:
        plt.figure(figsize=(6,4))
        sns.boxplot(x='Label', y='AddressOfEntryPoint', data=df)
        plt.title('Distribution de AddressOfEntryPoint selon la nature du fichier')
        plt.savefig('images/entropy_distribution.png') # Reuse filename to avoid changing latex
        plt.close()

    # Preprocessing
    print("Preprocessing data...")
    X = df.drop('Label', axis=1)
    y = df['Label']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)
    
    models = {
        'SVM': SVC(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'KNN': KNeighborsClassifier()
    }
    
    results = {}
    f1_scores = []
    model_names = []
    
    print("\nEvaluating models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        results[name] = f1
        f1_scores.append(f1)
        model_names.append(name)
        print(f"--- {name} ---")
        print(f"F1-Score: {f1:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}\n")
        
    plt.figure(figsize=(6,4))
    sns.barplot(x=model_names, y=f1_scores)
    plt.title('Comparaison des F1-Scores')
    plt.ylim(0.8, 1.0)
    for i, v in enumerate(f1_scores):
        plt.text(i, v + 0.01, f'{v:.4f}', ha='center')
    plt.savefig('images/model_comparison.png')
    plt.close()

    best_model_name = max(results, key=results.get)
    print(f"Best model based on F1-Score: {best_model_name}")
    
    print(f"\nOptimizing {best_model_name}...")
    
    if best_model_name == 'Random Forest':
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='f1', n_jobs=-1)
    elif best_model_name == 'SVM':
        param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto']
        }
        grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=5, scoring='f1', n_jobs=-1)
    else: # KNN
        param_grid = {
            'n_neighbors': [3, 5, 7, 9],
            'weights': ['uniform', 'distance']
        }
        grid_search = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='f1', n_jobs=-1)
        
    grid_search.fit(X_train, y_train)
    best_estimator = grid_search.best_estimator_
    
    print("Best Parameters:", grid_search.best_params_)
    print("Optimized F1-Score (CV):", grid_search.best_score_)
    
    # Save model, scaler and columns list
    joblib.dump(best_estimator, 'app/model/malware_classifier.pkl')
    joblib.dump(scaler, 'app/model/scaler.pkl')
    joblib.dump(list(X.columns), 'app/model/features.pkl')
    print("Model, scaler and feature list saved to app/model/")

if __name__ == '__main__':
    train_and_evaluate()
