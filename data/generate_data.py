import pandas as pd
import numpy as np

def generate_pe_dataset(n_samples=1000):
    np.random.seed(42)
    
    # Simulate benign files (label 0)
    benign_size = np.random.normal(500000, 100000, n_samples // 2)
    benign_entropy = np.random.normal(5.5, 0.5, n_samples // 2)
    benign_sections = np.random.randint(3, 7, n_samples // 2)
    benign_imports = np.random.normal(150, 50, n_samples // 2)
    benign_exports = np.random.normal(20, 10, n_samples // 2)
    
    # Simulate malicious files (label 1)
    malicious_size = np.random.normal(100000, 50000, n_samples // 2)
    malicious_entropy = np.random.normal(7.2, 0.6, n_samples // 2) # Higher entropy often indicates packing
    malicious_sections = np.random.randint(2, 10, n_samples // 2)
    malicious_imports = np.random.normal(30, 20, n_samples // 2) # Fewer imports if packed
    malicious_exports = np.random.normal(5, 5, n_samples // 2)
    
    # Combine
    size = np.concatenate([benign_size, malicious_size])
    entropy = np.concatenate([benign_entropy, malicious_entropy])
    sections = np.concatenate([benign_sections, malicious_sections])
    imports = np.concatenate([benign_imports, malicious_imports])
    exports = np.concatenate([benign_exports, malicious_exports])
    
    labels = np.concatenate([np.zeros(n_samples // 2), np.ones(n_samples // 2)])
    
    # Create DataFrame
    df = pd.DataFrame({
        'SizeOfImage': np.abs(size),
        'Entropy': np.clip(entropy, 0, 8),
        'NumberOfSections': sections,
        'Imports': np.abs(imports),
        'Exports': np.abs(exports),
        'Label': labels
    })
    
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

if __name__ == '__main__':
    df = generate_pe_dataset(2000)
    df.to_excel('data/dataset_malware.xlsx', index=False)
    print("Dataset generated and saved to data/dataset_malware.xlsx")
