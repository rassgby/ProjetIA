import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score, confusion_matrix

def train_and_evaluate():
    # Load dataset
    print("Loading dataset...")
    df = pd.read_excel('data/dataset_malware.xlsx')
    
    # Preprocessing
    print("Preprocessing data...")
    X = df.drop('Label', axis=1)
    y = df['Label']
    
    # Normalisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)
    
    # Models
    models = {
        'SVM': SVC(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'KNN': KNeighborsClassifier()
    }
    
    results = {}
    
    # Train and evaluate
    print("\nEvaluating models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        
        results[name] = f1
        print(f"--- {name} ---")
        print(f"F1-Score: {f1:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}\n")
        
    # Find best model
    best_model_name = max(results, key=results.get)
    print(f"Best model based on F1-Score: {best_model_name}")
    
    # Optimize best model
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
    
    # Final evaluation
    y_pred_opt = best_estimator.predict(X_test)
    print(f"\nFinal {best_model_name} Performance on Test Set:")
    print(classification_report(y_test, y_pred_opt))
    
    # Save model and scaler
    joblib.dump(best_estimator, 'app/model/malware_classifier.pkl')
    joblib.dump(scaler, 'app/model/scaler.pkl')
    print("Model and scaler saved to app/model/")

if __name__ == '__main__':
    train_and_evaluate()
