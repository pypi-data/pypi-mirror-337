[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Aem1sI_4)

# Midterm Project PICE

**Due Date:** March 27, 2025  
**Status:** 0 days late  
**Team Members:** Isaac, Chris, Parker, Elvira

## Introduction

This repository contains a comprehensive toolkit for analyzing Google Search Trends data related to influenza symptoms. Our aim is to gain insights into how different symptom search terms correlate with each other and identify temporal clusters in search patterns. By analyzing these patterns, we can potentially identify distinct phases of disease prevalence or public health concerns throughout flu seasons.

**Demo:** Check out our [live visualization example](https://ptope.github.io/symptom_visualization/) to see the final output of this package using static data.

## Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser (for Selenium-based data collection)
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/hsph-bst236/midterm-project-pice.git
   cd midterm-project-pice
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   The requirements.txt file includes the following main dependencies:
   - pytrends
   - selenium
   - pandas
   - numpy
   - matplotlib
   - scikit-learn
   - plotly

3. Download ChromeDriver (if using Selenium):
   Make sure to download the appropriate version that matches your Chrome browser from: https://sites.google.com/chromium.org/driver/

---

## How to Use the Package

### Installation
To install the package, use the following command:
```bash
pip install midterm-project-pice-0.1.0.tar.gz
```

### Running the Package from the Command Line

#### 1. Get Google Search Trends Data
To collect Google Search Trends data, use the following command:
```bash
python -m analysis.gst_pytrends --year 2022
```

**Valid Options for `--year`:**  
- 2020, 2021, 2022, 2023  
- Default is 2023 (if you don't specify the year).

#### 2. Run Principal Component Analysis (PCA)
To perform PCA on the collected data, use:
```bash
python -m analysis.symptom_pca
```

#### 3. Run Depth First Search (DFS) Clustering
To identify temporal clusters in the symptom search trends, use:
```bash
python -m analysis.dfs
```

---

## Usage

### Data Collection

Our toolkit offers three methods to collect Google Trends data:

#### Method 1: Using PyTrends (Recommended)

This is the primary method that works behind the scenes without visible browser activity:

```bash
# Default usage (collects data for 2023-2024)
python gst_pytrends.py

# To specify a different year (e.g., 2022-2023)
python gst_pytrends.py --year 2022
```

**Note:** PyTrends occasionally encounters rate limits (429 errors). For best results, run during evening hours when Google's servers typically have lower traffic.

#### Method 2: Using Selenium (Fallback)

If PyTrends fails, use the Selenium-based approach:

```bash
python gst_selenium.py
```

This will open a Chrome browser window that interacts with Google Trends' interface.

#### Method 3: Using Pre-collected Historical Data

The package includes historical data files for previous flu seasons (2020-2024) in the `data_from_gst_website` directory:
```bash
data_from_gst_website/
├── df_20_21.csv  # 2020-2021 flu season
├── df_21_22.csv  # 2021-2022 flu season
├── df_22_23.csv  # 2022-2023 flu season
└── df_23_24.csv  # 2023-2024 flu season (partial)
```
The package will first try to obtain Google Search Trends data. If it fails after the pre-specified number of retries, it will let the user know and automatically read in the pre-downloaded data. The user does not need to do anything.

### Data Analysis

After collecting data, run the following scripts in sequence:

1. **Principal Component Analysis (PCA):**
   ```bash
   # Default usage (auto-detects latest data)
   python symptom_pca.py

   # Specify input data manually
   python symptom_pca.py --input data_from_gst_website/df_21_22.csv

   # Customize output location
   python symptom_pca.py --input data_from_gst_website/df_21_22.csv --output output/pca_2021/
   ```
   This generates visualizations showing how symptom terms cluster together, including:
   - Term loadings on principal components
   - Explained variance per component
   - Heatmap of term loadings
   - Scatter plot of terms in PC1-PC2 space

2. **Depth First Search (DFS) Clustering:**
   ```bash
   # Default usage (auto-detects latest data)
   python 03_dfs.py

   # Specify input data manually
   python 03_dfs.py --input data_from_gst_website/df_21_22.csv

   # Customize similarity threshold and output
   python 03_dfs.py --input data_from_gst_website/df_21_22.csv --threshold 0.85 --output output/clusters_2021/enhanced_clusters.csv
   ```
   This identifies temporal clusters in the symptom search trends and generates an enhanced CSV file with cluster assignments.

3. **Visualization:**
   ```bash
   python 04_visualization.py
   ```
   
   Optional arguments:
   ```bash
   python 04_visualization.py --data path/to/data.csv --clusters path/to/clusters.csv --output custom_output.html
   ```

   For complete customization:
   ```bash
   python 04_visualization.py \
     --data data_enhanced/enhanced_clusters.csv \
     --output custom_viz.html \
     --pca-images symptom_term_loadings.png symptom_term_clusters.png
   ```

   The visualization will automatically open in your default web browser.

---

## Implementation Details

### Principal Component Analysis (PCA)

Our PCA implementation analyzes which search terms correlate and cluster together, offering insights into symptom co-occurrence patterns. The core functionality is implemented in the `pca_on_search_terms` function:

```python
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
```

Key aspects of our PCA implementation:

1. **Data Preparation:**
   - We transpose the data matrix to treat search terms as variables (rows) and time points as observations (columns)
   - We standardize the data using z-scores to ensure all terms are on a comparable scale

2. **Core PCA Steps:**
   - Calculate the covariance matrix of standardized data
   - Compute eigenvalues and eigenvectors of the covariance matrix
   - Sort components by explained variance (descending order)
   - Project the original data onto the principal components

3. **Visualization:**
   - Heatmap of term loadings on principal components
   - Scatter plot showing terms in PC1-PC2 space to visualize clustering
   - Variance explained by each component

The PCA reveals which symptoms tend to be searched together and how they group into meaningful clusters, helping to identify different types of illness patterns or phases.

### Depth First Search (DFS) Clustering Algorithm

Our temporal clustering algorithm uses Depth First Search to identify periods with similar symptom search patterns. The implementation is based on a constrained graph where:

1. **Nodes** represent individual weeks
2. **Edges** connect only adjacent weeks that have similar symptom patterns
3. **Similarity** is measured using cosine similarity with a user-defined threshold

#### Building the Similarity Graph

The graph construction is implemented in the `build_similarity_graph` function:

```python
def build_similarity_graph(df_std: pd.DataFrame, threshold: float = 0.7) -> Dict[str, Set[str]]:
    """Build graph connecting neighboring weeks with similar standardized symptom patterns."""
    graph = {week: set() for week in df_std.index}
    weeks = sorted(df_std.index)
    values = df_std.values

    for i in range(len(weeks) - 1):
        sim = cosine_similarity([values[i]], [values[i + 1]])[0][0]
        if sim >= threshold:
            w1, w2 = weeks[i], weeks[i + 1]
            graph[w1].add(w2)
            graph[w2].add(w1)

    return graph
```

**Key Constraints:**
1. **Adjacent Weeks Only:** The graph construction explicitly iterates through consecutive pairs of weeks (`i` and `i+1`), ensuring that only temporally adjacent weeks can be connected. This constraint is crucial as it enforces the temporal continuity of our clusters.

2. **Similarity Threshold:** An edge is only added between adjacent weeks if their cosine similarity meets or exceeds the threshold (default 0.7). This means weeks with dissimilar symptom patterns are effectively disconnected in the graph, even if they are adjacent in time.

3. **Cosine Similarity:** We use cosine similarity to measure the similarity between standardized symptom vectors of adjacent weeks:
   - Cosine similarity measures the cosine of the angle between two vectors
   - Values range from -1 (completely opposite) to 1 (identical)
   - A value of 0 indicates orthogonality (no correlation)
   - Our implementation applies a threshold (e.g., 0.7) to only connect weeks with high similarity

   The formula for cosine similarity between two vectors A and B is:
   
   ```
   similarity = cos(θ) = (A·B)/(||A||·||B||)
   ```
   
   Where:
   - A·B is the dot product of vectors A and B
   - ||A|| and ||B|| are the Euclidean norms (magnitudes) of vectors A and B
   
   In our context, each vector represents the standardized symptom search frequencies for a week. Cosine similarity is particularly useful for our analysis because:
   
   - It measures the similarity of patterns regardless of magnitude
   - It works well with high-dimensional data (many symptom terms)
   - It captures whether symptom search terms rise and fall together, even if the absolute values differ
   - Values close to 1 indicate weeks with very similar symptom search patterns

#### Depth First Search Implementation

The DFS algorithm is implemented as follows:

```python
def dfs(graph: Dict[str, Set[str]], start: str, visited: Set[str]) -> Set[str]:
    """Depth-first search to find a connected cluster of weeks."""
    stack, cluster = [start], set()
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            cluster.add(node)
            stack.extend(graph[node] - visited)
    return cluster
```

The DFS traversal:
1. Starts from an unvisited week
2. Uses a stack to track weeks to visit
3. For each week, adds all connected (similar) neighboring weeks to the stack
4. Continues until all connected weeks have been visited
5. Returns the complete cluster of connected weeks

#### Cluster Identification

The overall cluster finding process is implemented in `find_pattern_clusters`:

```python
def find_pattern_clusters(df_std: pd.DataFrame, threshold: float = 0.80) -> List[Set[str]]:
    """Find clusters of weeks with similar symptom patterns using DFS."""
    graph = build_similarity_graph(df_std, threshold)
    visited, clusters = set(), []

    for week in graph:
        if week not in visited:
            cluster = dfs(graph, week, visited)
            if len(cluster) > 1:
                clusters.append(cluster)

    return sorted(clusters, key=len, reverse=True)
```

This function:
1. Builds the similarity graph with the adjacency and threshold constraints
2. Uses DFS to explore each connected component in the graph
3. Collects clusters containing at least two weeks
4. Returns clusters sorted by size (largest first)

#### Enhancing Data with Cluster Information

The final step in our process is to enhance the original data with cluster assignments and calculate summary statistics:

```python
def analyze_symptom_patterns(df: pd.DataFrame, threshold: float = 0.80) -> Tuple[Dict[str, List[Set[str]]], pd.DataFrame]:
    """
    Standardize data, cluster similar weeks, and rank clusters by average symptom intensity.
    Returns both the clusters dictionary and the enhanced dataframe with cluster info.
    """
    df_std = standardize_symptoms(df)
    clusters = find_pattern_clusters(df_std, threshold)

    # Create a copy of the original dataframe to add cluster information
    enhanced_df = df.copy()
    
    # Initialize new columns with NaN values
    enhanced_df['cluster'] = np.nan
    enhanced_df['avg_intensity'] = np.nan

    cluster_info = []
    for i, cluster in enumerate(clusters):
        cluster_list = list(cluster)
        avg_intensity = df.loc[cluster_list].sum().sum() / len(cluster)
        cluster_info.append((cluster, avg_intensity))

    # Sort clusters by intensity
    cluster_info.sort(key=lambda x: -x[1])
    
    # Assign cluster numbers and average intensities to the dataframe
    for cluster_num, (cluster, intensity) in enumerate(cluster_info, 1):
        # For each week in the cluster, assign the cluster number and intensity
        for week in cluster:
            enhanced_df.loc[week, 'cluster'] = cluster_num
            enhanced_df.loc[week, 'avg_intensity'] = intensity

    print(f"\nClusters at {int(threshold * 100)}% similarity threshold (ranked by intensity):")
    for i, (cluster, intensity) in enumerate(cluster_info):
        print(f"  Cluster {i+1}: {len(cluster)} weeks, avg intensity = {intensity:.1f} - {sorted(cluster)[:3]}...")

    # Return both the original clusters dictionary and the enhanced dataframe
    return {"clusters_{0}".format(int(threshold*100)): [info[0] for info in cluster_info]}, enhanced_df
```

This function:
1. Standardizes the symptom data
2. Identifies clusters using the DFS approach
3. Calculates average symptom intensity for each cluster
4. Ranks clusters by intensity (highest first)
5. Enhances the original dataframe with cluster assignments
6. Returns both the cluster information and the enhanced dataframe

### Important Notes on DFS Implementation

While we use DFS to identify connected components in our graph, it's worth noting that our specific graph structure (with constraints on adjacency) means that:

1. A standard linear scan of consecutive weeks could also identify these clusters
2. The DFS algorithm is not strictly necessary for this specific constrained case
3. The adjacency constraint ensures that all clusters are temporally contiguous, which aligns with our goal of identifying distinct disease phases

**Disclaimer on DFS Usage:** It's important to note that in our current implementation, which strictly limits connections to adjacent weeks, the DFS algorithm is actually more complex than needed. A simpler linear scan checking for similarity between consecutive weeks would produce identical clusters. 

We chose to implement DFS for the following reasons:
- **Educational Value:** DFS is a fundamental graph algorithm and provides valuable learning experience
- **Extensibility:** Our implementation can be easily extended to handle more complex graph structures
- **Future Enhancements:** If we later decide to allow connections between non-adjacent weeks (e.g., connecting weeks with similar patterns across different years), the DFS approach would still be valid without requiring a significant rewrite

In a more general implementation where weeks could be connected based on other criteria besides adjacency (for example, allowing connections between weeks that are 52 weeks apart to capture year-over-year patterns), DFS would be essential for properly identifying the resulting non-linear clusters.

The threshold parameter allows users to control how restrictive the clustering is:
- Higher thresholds (e.g., 0.9) produce smaller, more tightly similar clusters
- Lower thresholds (e.g., 0.6) produce larger, more inclusive clusters

## Expected Output

1. **Data Collection:**
   - `cleaned_pytrends_data.csv`: Processed Google Trends data with standardized search interest values.

2. **PCA Analysis:**
   - `symptom_term_loadings.png`: Heatmap showing term loadings on principal components
   - `symptom_term_clusters.png`: Scatter plot of terms in PC1-PC2 space

3. **DFS Clustering:**
   - `data_enhanced/enhanced_clusters.csv`: Original data enriched with cluster assignments

4. **Visualization:**
   - `symptom_clusters.html`: Interactive visualization showing:
     - Weekly symptom search trends with color-coded clusters
     - Hover functionality for detailed information
     - Dynamic legend to toggle symptom categories
     - PCA visualization images

## Report

### Problem Definition

We aimed to identify patterns in Google Search Trends data related to influenza symptoms to understand:
1. How different symptom search terms correlate and cluster together
2. How search patterns change over time, potentially indicating disease prevalence phases

### Challenges and Solutions

#### Data Collection Challenges

1. **Google Trends Limitations:**
   - Limited to 5 terms per search
   - Relative scaling of search interest
   
   **Solution:** We implemented an "anchor term" approach, using "soccer" as a consistently high-volume search term to standardize scaling across batches.

2. **Rate Limiting:**
   - Google frequently returns 429 (Too Many Requests) errors
   
   **Solution:** 
   - Implemented randomized delays between requests
   - Batch processing with small groups (3 terms at a time)
   - Developed dual-approach system with PyTrends and Selenium
   - Added fallback to pre-downloaded data when API fails

#### Analysis Methodology

1. **Principal Component Analysis (PCA):**
   - Standardized search interest values
   - Identified which symptom terms tend to move together
   - Reduced dimensionality to visualize term relationships
   - Discovered meaningful clusters of related symptoms

2. **Temporal Clustering with DFS:**
   - Used z-scores to standardize symptom search frequencies
   - Built similarity graph connecting weeks with similar pattern signatures
   - Applied DFS to identify connected components (clusters)
   - Ranked clusters by average symptom intensity
   - Generated enhanced dataset with cluster assignments for visualization

### Key Findings

1. Symptom search terms naturally group into distinct clusters, potentially representing different illness types or phases.
2. Search patterns show clear temporal clustering, indicating distinct periods of disease prevalence with outbreaks identified in December and January. 
3. The methodology successfully identifies seasonal patterns in influenza-related searches.

## Contributions

- **Isaac:** 
  - Drafted package structure and DFS code
  - Set up the project structure and requirements

- **Chris:** 
  - Created the Selenium-based fallback method
  - Package structuring, worked with trends
  - Designed and implemented the visualization interface
  - Set up the project structure and requirements

- **Parker:** 
  - Designed and implemented the visualization interface
  - Built off of Elvira's DFS code
  - Package structuring
  - Set up the project structure and requirements
  - Integrated components and ensured compatibility between modules

- **Elvira:** 
  - Wrote original pytrends code
  - Wrote original PCA code
  - Built off Isaac's DFS code to generate meaningful similarity matrix
  - Built original workflow between programs, ensuring compatibility between modules
  - Helped in verifying and valdiating package structure and functionality
