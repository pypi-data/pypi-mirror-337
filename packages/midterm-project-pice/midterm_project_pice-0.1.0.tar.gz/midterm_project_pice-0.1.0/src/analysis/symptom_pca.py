import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 


def pca_on_search_terms(data):
    """
    Perform PCA to cluster search terms.
    This analyzes which search terms correlate and cluster together.
    """
    # Ensure we're working with numeric data only
    data = data.select_dtypes(include=[np.number])
    
    # Check for constant columns and remove them
    std_values = data.std()
    constant_cols = std_values[std_values < 1e-10].index.tolist()
    if constant_cols:
        print(f"Warning: Removing constant columns: {constant_cols}")
        data = data.drop(columns=constant_cols)
    
    # Transpose data: rows = search terms, columns = time points
    X = data.T.values

    # Standardize: subtract mean and divide by std (z-score)
    mean_vec = np.mean(X, axis=1, keepdims=True)
    std_vec = np.std(X, axis=1, ddof=1, keepdims=True)  # use ddof=1 for sample std
    
    # Prevent division by zero - replace zeros with 1 to keep original values
    std_vec[std_vec < 1e-10] = 1
    X_standardized = (X - mean_vec) / std_vec
    
    # Safety check for NaN or inf values
    if np.isnan(X_standardized).any() or np.isinf(X_standardized).any():
        # Try to identify problematic columns
        print("Problematic rows in the transposed data:")
        for i, symptom in enumerate(data.columns):
            row_data = X[i]
            if np.isnan(row_data).any() or np.isinf(row_data).any():
                print(f"  {symptom}: {row_data}")
        raise ValueError("Data contains NaN or inf values after standardization")
    
    # Calculate covariance matrix
    cov_matrix = np.cov(X_standardized)
    
    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # Ensure values are real (not complex)
    eigenvalues = np.real(eigenvalues)
    eigenvectors = np.real(eigenvectors)
    
    # Sort eigenvalues and eigenvectors in descending order
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Calculate explained variance ratio
    explained_variance = eigenvalues / np.sum(eigenvalues)
    
    # Project terms onto principal components
    PC = np.dot(X_standardized.T, eigenvectors)
    
    return PC, eigenvectors, eigenvalues, explained_variance, data.columns

def main():
    # Add argument parsing for file input
    import argparse
    
    parser = argparse.ArgumentParser(description='Perform PCA on symptom search trends data')
    parser.add_argument('--input', type=str, default="data/cleaned_pytrends_data.csv",
                        help='Input CSV file (default: cleaned_pytrends_data.csv)')
    
    args = parser.parse_args()
    
    try:
        # Load the cleaned data
        filename = args.input
        print(f"Loading data from {filename}")
        df = pd.read_csv(filename)
        
        # Remove date and non-numeric columns if present
        if 'date' in df.columns:
            df = df.drop(columns=['date'])
        if 'Week' in df.columns:
            df = df.drop(columns=['Week'])
            
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Perform PCA on search terms
        PC, eigenvectors, eigenvalues, explained_variance, terms = pca_on_search_terms(numeric_df)
        
        # Print which search terms load on each component
        loadings = pd.DataFrame(eigenvectors[:, :3], index=terms, columns=['PC1', 'PC2', 'PC3'])
        print("\nSearch term loadings on principal components:")
        print(loadings)
        
        # Print variance explained
        print("\nVariance explained by each component:")
        for i, var in enumerate(explained_variance[:5]):
            print(f"PC{i+1}: {var:.4f} ({var*100:.2f}%)")

        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        
        # Create heatmap of loadings
        plt.figure(figsize=(12, 10))
        sns.heatmap(loadings, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Search Term Loadings on Principal Components')
        plt.tight_layout()
        plt.savefig('output/symptom_term_loadings.png')
        print("\nHeatmap saved as 'symptom_term_loadings.png'")
        
        # Create scatter plot of terms on PC1 vs PC2
        plt.figure(figsize=(12, 10))
        plt.scatter(eigenvectors[:, 0], eigenvectors[:, 1], alpha=0)  # Invisible points
        for i, term in enumerate(terms):
            plt.text(eigenvectors[i, 0], eigenvectors[i, 1], term, ha='center', va='center')
            
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        plt.xlabel(f'PC1 ({explained_variance[0]*100:.2f}%)')
        plt.ylabel(f'PC2 ({explained_variance[1]*100:.2f}%)')
        plt.title('Search Terms Projected onto PC1 and PC2')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/symptom_term_clusters.png')
        print("Term cluster plot saved as 'symptom_term_clusters.png'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()