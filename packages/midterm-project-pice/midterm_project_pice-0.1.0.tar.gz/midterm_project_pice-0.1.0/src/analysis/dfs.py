import pandas as pd
import numpy as np
import os
from typing import List, Set, Dict, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

def standardize_symptoms(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize each symptom across time (z-score per column)."""
    scaler = StandardScaler()
    df_std = pd.DataFrame(scaler.fit_transform(df), index=df.index, columns=df.columns)
    return df_std

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

def find_pattern_clusters(df_std: pd.DataFrame, threshold: float = 0.7) -> List[Set[str]]:
    """Find clusters of weeks with similar symptom patterns using DFS."""
    graph = build_similarity_graph(df_std, threshold)
    visited, clusters = set(), []

    for week in graph:
        if week not in visited:
            cluster = dfs(graph, week, visited)
            if len(cluster) > 1:
                clusters.append(cluster)

    return sorted(clusters, key=len, reverse=True)

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

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze weekly symptom patterns in search trends')
    parser.add_argument('--input', type=str, default="data/cleaned_pytrends_data.csv",
                        help='Input CSV file (default: cleaned_pytrends_data.csv)')
    parser.add_argument('--threshold', type=float, default=0.80,
                        help='Similarity threshold (default: 0.80)')
    parser.add_argument('--output', type=str, default="enhanced_clusters.csv",
                        help='Output CSV file name (default: enhanced_clusters.csv)')
    args = parser.parse_args()

    try:
        print(f"Loading data from {args.input}...")
        df = pd.read_csv(args.input)

        # Set the appropriate index
        if 'date' in df.columns:
            df.set_index('date', inplace=True)
        if 'Week' in df.columns:
            df.set_index('Week', inplace=True)

        # Run the analysis and get both the clusters and enhanced dataframe
        results, enhanced_df = analyze_symptom_patterns(df, args.threshold)
        
        # Create data_enhanced directory if it doesn't exist
        output_dir = "output/data_enhanced"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        
        # Save the enhanced dataframe to CSV in the data_enhanced directory
        output_path = os.path.join(output_dir, args.output)
        enhanced_df.to_csv(output_path)
        print(f"Enhanced dataframe with cluster information saved to: {output_path}")
        
        return results, enhanced_df

    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    main()