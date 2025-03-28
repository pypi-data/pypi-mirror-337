import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import webbrowser
import numpy as np
from matplotlib import colors
import glob

def get_color_scale(min_intensity, max_intensity, num_colors=100):
    """
    Generate a color scale from light red to dark purple based on intensity range
    
    Parameters:
    min_intensity (float): Minimum intensity value
    max_intensity (float): Maximum intensity value
    num_colors (int): Number of colors in the scale
    
    Returns:
    dict: Dictionary mapping intensity values to hex color codes
    """
    # Create a list of colors from light red to dark purple
    color_list = []
    
    # Generate color scale from light red to dark purple
    red_to_purple = colors.LinearSegmentedColormap.from_list(
        'red_to_purple', 
        [(1, 0.8, 0.8),      # Light red
         (1, 0.5, 0.5),      # Medium red
         (0.8, 0.4, 0.6),    # Red-purple
         (0.6, 0.2, 0.6),    # Medium purple
         (0.4, 0.1, 0.4)]    # Dark purple
    )
    
    # Generate evenly spaced colors
    for i in range(num_colors):
        rgba = red_to_purple(i / (num_colors - 1))
        # Convert to hex
        hex_color = colors.rgb2hex(rgba)
        color_list.append(hex_color)
    
    # Create a mapping from intensity to color
    intensity_range = np.linspace(min_intensity, max_intensity, num_colors)
    color_map = {intensity: color for intensity, color in zip(intensity_range, color_list)}
    
    return color_map

def get_color_for_intensity(intensity, color_map):
    """
    Get the closest color for a given intensity value
    
    Parameters:
    intensity (float): Intensity value
    color_map (dict): Dictionary mapping intensity values to hex color codes
    
    Returns:
    str: Hex color code
    """
    # Find the closest intensity in the color map
    intensities = np.array(list(color_map.keys()))
    idx = np.abs(intensities - intensity).argmin()
    return list(color_map.values())[idx]

def check_for_pca_images():
    """
    Check if PCA images from symptom_pca.py exist and return a list of found images
    
    Returns:
    list: List of paths to found PCA images
    """
    pca_images = []
    default_pca_files = [
        'output/symptom_term_loadings.png',
        'output/symptom_term_clusters.png'
    ]
    
    for img_path in default_pca_files:
        if os.path.exists(img_path):
            pca_images.append(img_path)
            print(f"Found PCA image: {img_path}")
    
    return pca_images

def create_cluster_visualization(data_path, cluster_path, output_path='symptom_clusters.html', pca_images=None):
    """
    Create a visualization with color-coded cluster highlighting based on intensity and save as HTML
    
    Parameters:
    data_path (str): Path to original symptom data CSV
    cluster_path (str): Path to CSV with cluster information
    output_path (str): Path to save the HTML output
    pca_images (list, optional): List of paths to PCA images to include
    """
    print(f"Loading data from {data_path}")
    # Load the original data
    df = pd.read_csv(data_path)
    
    print(f"Loading cluster data from {cluster_path}")
    # Load the cluster data
    cluster_df = pd.read_csv(cluster_path)
    
    # Ensure data has the right format
    if 'Week' not in df.columns:
        print("Error: 'Week' column not found in data")
        return False
    
    # Get symptom columns, excluding cluster and avg_intensity columns
    symptom_cols = [col for col in df.columns if col not in ['Week', 'cluster', 'avg_intensity']]
    
    # Auto-detect PCA images if not provided
    if pca_images is None:
        pca_images = check_for_pca_images()
    
    # Create figure
    fig = go.Figure()
    
    # Add a trace for each symptom
    for symptom in symptom_cols:
        fig.add_trace(
            go.Scatter(
                x=df['Week'],
                y=df[symptom],
                mode='lines',
                name=symptom,
                hovertemplate='<b>%{fullData.name}</b><br>Week: %{x}<br>Value: %{y}<extra></extra>'
            )
        )
    
    # Add cluster highlighting if available
    if 'cluster' in cluster_df.columns and 'avg_intensity' in cluster_df.columns:
        print("Adding cluster highlighting")
        # Get weeks with cluster assignments
        clustered_weeks = cluster_df.dropna(subset=['cluster'])
        
        # Group weeks by cluster
        clusters = {}
        for _, row in clustered_weeks.iterrows():
            cluster_num = int(row['cluster'])
            week = row['Week']
            intensity = row['avg_intensity']
            
            if cluster_num not in clusters:
                clusters[cluster_num] = {'weeks': [], 'intensity': intensity}
            clusters[cluster_num]['weeks'].append(week)
        
        # Get intensity range for color mapping
        min_intensity = min([info['intensity'] for info in clusters.values()])
        max_intensity = max([info['intensity'] for info in clusters.values()])
        
        print(f"Intensity range: {min_intensity} to {max_intensity}")
        
        # Create color scale
        color_map = get_color_scale(min_intensity, max_intensity)
        
        # Add shaded areas for each cluster
        for cluster_num, info in clusters.items():
            weeks = sorted(info['weeks'])
            intensity = info['intensity']
            
            # Get color for this intensity
            color = get_color_for_intensity(intensity, color_map)
            
            # Convert to rgba with alpha
            rgb = colors.hex2color(color)
            rgba = f"rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, 0.25)"
            
            # Find min and max values for y-axis
            y_min = min([df[col].min() for col in symptom_cols]) * 0.9
            y_max = max([df[col].max() for col in symptom_cols]) * 1.1
            
            # Group consecutive weeks
            week_groups = []
            current_group = []
            
            for week in weeks:
                if not current_group:
                    current_group = [week]
                elif week_groups and week != current_group[-1]:
                    week_groups.append(current_group)
                    current_group = [week]
                else:
                    current_group.append(week)
            
            if current_group:
                week_groups.append(current_group)
            
            # Add shapes for cluster regions using interactive hover elements instead of static annotations
            for group in week_groups:
                start_week = min(group)
                end_week = max(group)
                
                # Create an invisible scatter trace for each cluster region that will show hover info
                # This trace is positioned at the top of the cluster region to make hovering easy
                fig.add_trace(
                    go.Scatter(
                        x=[start_week, end_week],
                        y=[y_max, y_max],
                        mode='lines',
                        line=dict(width=0),
                        fill='tozeroy',
                        fillcolor=rgba,
                        opacity=0.8,
                        showlegend=False,
                        hoverinfo='text',
                        hovertext=f'<b>Cluster {cluster_num}</b><br>Intensity: {intensity:.2f}<br>Weeks: {start_week}-{end_week}',
                        hoverlabel=dict(bgcolor='white'),
                        name=f'Cluster {cluster_num}',
                    )
                )
                
                # Add a transparent rectangle for the entire cluster region
                # This won't have hover info but creates the visual highlight
                fig.add_shape(
                    type="rect",
                    x0=start_week,
                    y0=y_min,
                    x1=end_week,
                    y1=y_max,
                    fillcolor=rgba,
                    opacity=0.8,
                    layer="below",
                    line_width=0
                )
        
        # --- MODIFIED: Add intensity scale as a separate legend to the right of the plot ---
        # Create custom intensity scale traces for the legend
        legend_intensities = np.linspace(min_intensity, max_intensity, 5)
        
        # Create a dummy invisible trace to add a section title to the legend
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(size=0),
                showlegend=True,
                name='<b>Intensity Scale</b>',
                legendgroup='intensity_scale',
                legendgrouptitle=dict(text='Intensity Scale'),
            )
        )
        
        # Add a trace for each intensity level
        for intensity in legend_intensities:
            color = get_color_for_intensity(intensity, color_map)
            # Convert to rgba with alpha
            rgb = colors.hex2color(color)
            rgba = f"rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, 0.25)"
            
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color=rgba,
                        line=dict(color=color, width=1)
                    ),
                    showlegend=True,
                    name=f"{intensity:.1f}",
                    legendgroup='intensity_scale',
                )
            )
    
    # Add PCA images if provided
    if pca_images and isinstance(pca_images, list) and len(pca_images) > 0:
        print(f"Adding {len(pca_images)} PCA images")
        
        # Filter to only include existing images
        valid_images = [img for img in pca_images if os.path.exists(img)]
        num_images = len(valid_images)
        
        if (num_images > 0):
            # Import base64 for image encoding
            import base64
            
            # Add each PCA image as an HTML iframe with the image
            img_html = ""
            for i, img_path in enumerate(valid_images):
                try:
                    with open(img_path, "rb") as img_file:
                        encoded_image = base64.b64encode(img_file.read()).decode('ascii')
                        img_name = os.path.basename(img_path).replace('.png', '').replace('_', ' ').title()
                        
                        # Add image div with better styling for readability
                        img_html += f"""
                        <div style="display: inline-block; margin: 15px; text-align: center; width: 45%; vertical-align: top;">
                            <h3 style="margin-bottom: 10px;">{img_name}</h3>
                            <img src="data:image/png;base64,{encoded_image}" style="max-width: 100%; max-height: 400px; border: 1px solid #ddd; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                        </div>
                        """
                        print(f"Added image: {img_path}")
                except Exception as e:
                    print(f"Error adding image {img_path}: {e}")
            
            # Store images for later use in the HTML
            fig._images_html = img_html
    
    # Update layout with additional settings for hovering and legend positioning
    fig.update_layout(
        title={
            'text': 'Symptom Search Trends with Depth First Search-identified Clusters Highlighted',
            'x': 0.5,  # Center the title
            'font': {
                'size': 18,
                'weight': 'bold'  # Make the title bold
            }
        },
        xaxis_title='Week',
        yaxis_title='Search Frequency',
        legend_title='Symptoms',
        hovermode='closest',  # Changed from 'x unified' to 'closest' for better cluster hovering
        template='plotly_white',
        # Add extra height for legend and PCA images
        height=900 if hasattr(fig, '_images_html') else 700,
        margin=dict(t=70, r=150, b=150, l=50),  # Increased right margin for legend
        # Configure the legend to show on the right side with grouped items
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,  # Place legend outside the plot area
            traceorder="grouped",  # Group legends by their legendgroup
            groupclick="toggleitem",  # Click behavior
            font=dict(size=10),
            itemsizing="constant"  # Keep marker sizes constant in legend
        )
    )
    
    # Save as HTML
    print(f"Saving visualization to {output_path}")
    
    # Check if we have PCA images to include
    if hasattr(fig, '_images_html') and fig._images_html:
        # Custom HTML with PCA images
        plot_div = fig.to_html(include_plotlyjs=True, full_html=False)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Symptom Search Trends with Intensity-Based Cluster Highlighting</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    border-radius: 5px;
                }}
                .plot-container {{
                    width: 100%;
                    margin-bottom: 30px;
                }}
                .pca-container {{
                    margin-top: 30px;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                    text-align: center;
                }}
                h2 {{
                    color: #333;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                    margin-top: 30px;
                }}
                .pca-description {{
                    text-align: left;
                    margin: 20px 0;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="plot-container">
                    {plot_div}
                </div>
                
                <div class="pca-container">
                    <h2>PCA Analysis of Search Terms</h2>
                    <div class="pca-description">
                        <p>The Principal Component Analysis (PCA) visualizations below show how different search terms cluster together based on their temporal patterns. 
                        These visualizations help identify which symptoms tend to co-occur in search behavior and their relationships to each other.</p>
                    </div>
                    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
                        {fig._images_html}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    else:
        # Standard Plotly HTML export without PCA images
        fig.write_html(
            output_path,
            include_plotlyjs=True,
            full_html=True
        )
    
    # Open in browser
    try:
        print(f"Opening {output_path} in browser")
        # Get the absolute path
        abs_path = os.path.abspath(output_path)
        # Create a file URL
        file_url = f'file://{abs_path}'
        # Open in browser
        webbrowser.open(file_url)
        print("Browser opened successfully")
        return True
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"Please manually open: {abs_path}")
        return False

def find_latest_enhanced_csv():
    """
    Find the most recent enhanced CSV file in the output/data_enhanced directory
    """
    # Check if output/data_enhanced directory exists
    if not os.path.exists('output/data_enhanced'):
        print("Error: output/data_enhanced directory not found")
        return None, None
    
    # Look for CSV files in output/data_enhanced directory
    csv_files = glob.glob('output/data_enhanced/*.csv')
    
    if not csv_files:
        print("Error: No CSV files found in output/data_enhanced directory")
        return None, None
    
    # Sort by modification time, newest first
    csv_files.sort(key=os.path.getmtime, reverse=True)
    latest_csv = csv_files[0]
    
    print(f"Found latest enhanced CSV: {latest_csv}")
    
    # For cluster data, we use the same file
    return latest_csv, latest_csv

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create symptom cluster visualization with intensity-based coloring')
    parser.add_argument('--data', '-d', help='Path to symptom data CSV (optional, auto-detected from data_enhanced folder)')
    parser.add_argument('--clusters', '-c', help='Path to cluster data CSV (optional, same as data path by default)')
    parser.add_argument('--output', '-o', default='symptom_clusters.html', help='Output HTML file')
    parser.add_argument('--pca-images', '-p', nargs='+', help='Paths to PCA images to include')
    parser.add_argument('--auto-pca', '-a', action='store_true', 
                        help='Automatically look for PCA images (symptom_term_loadings.png and symptom_term_clusters.png)')
    
    args = parser.parse_args()
    
    # Determine data and cluster paths
    data_path = args.data
    cluster_path = args.clusters
    
    # If data path is not provided, try to auto-detect it
    if not data_path:
        data_path, auto_cluster_path = find_latest_enhanced_csv()
        if not data_path:
            print("Could not auto-detect data file. Please ensure the output/data_enhanced directory exists.")
            exit(1)
        
        # If cluster path is not provided, use the auto-detected path
        if not cluster_path:
            cluster_path = auto_cluster_path
    
    # If cluster path is still not set, use data path
    if not cluster_path:
        cluster_path = data_path
    
    # Determine PCA images to use
    pca_images = None
    
    # First check if specific PCA images were provided
    if args.pca_images:
        pca_images = args.pca_images
        print(f"Using specified PCA images: {pca_images}")
    # Then check if auto-detection is enabled
    elif args.auto_pca or True:  # Always auto-detect by default
        pca_images = check_for_pca_images()
        if pca_images:
            print(f"Auto-detected PCA images: {pca_images}")
    
    # Run the visualization
    create_cluster_visualization(data_path, cluster_path, args.output, pca_images)
    