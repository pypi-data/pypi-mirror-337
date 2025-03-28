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
- Default is 2023 (if you don’t specify the year).

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
