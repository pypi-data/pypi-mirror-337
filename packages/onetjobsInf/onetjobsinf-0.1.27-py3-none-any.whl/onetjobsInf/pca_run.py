# These functions are used to compute the PCA of the data imported from scaffolding
# Done from first principles using numpy and scipy rather than using PCA from sklearn?

import pandas as pd
import numpy as np
# Compute the largest k eigenvalues and eigenvectors, when k << n
# We should only use sparse when k+10 
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
import os

from onetjobsInf.pca_request_data import download_and_process_data

# Transforms the data from long to wide format
# Two rows per occupation (Importance - IM, Level - LV)
def transform_towide(file_path):
    # Load the data
    data = pd.read_csv(file_path, sep='\t')  # Adjust the separator if needed (e.g., ',' for CSV)
    
    # Transform the data from long to wide format
    matrix = data.pivot(index=['O*NET-SOC Code', 'Scale ID'], columns='Element Name', values='Data Value')
    # Print the dimensions of the matrix
    print("Matrix dimensions:", matrix.shape)

    # Fill missing values with 0 or another appropriate value
    matrix = matrix.fillna(0)
    
    return matrix


def pca_scaleid(matrix, k=2):
    # k is number of evals/evecs to compute
    # Select only rows with Scale ID of interest
    lv_rows = matrix

    # Compute the covariance matrix
    covmat = lv_rows.cov()

    # Compute the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = eigs(covmat.values, k=k, which='LM')  # 'LM' selects largest magnitude eigenvalues
    # take only the real part
    eigenvalues = np.real(eigenvalues)
    eigenvectors = np.real(eigenvectors)

    # Return the eigenvectors as principal components
    # Could instead compute PCs as lin combs of original variables?
    principal_components = eigenvectors
    principal_components = pd.DataFrame(principal_components)
    principal_components.columns = [f'PC{i+1}' for i in range(principal_components.shape[1])]

    # Compute the proportion of variance explained
    prop_var = eigenvalues / np.sum(eigenvalues)
    
    return principal_components, prop_var

def create_biplot(matrix, principal_components, scaling=None, plot_type='loadings'):
    """
Create a biplot from PCA results
    
    Parameters:
    -----------
    matrix : pandas DataFrame
        Original data matrix
    principal_components : pandas DataFrame
        Principal components from pca_scaleid
        Scale ID used ('LV' or 'IM')
    scaling : float, optional
        If None, will auto-scale based on data range
    plot_type : str
        Type of plot to create: 'scores', 'loadings', or 'both'
"""
    # Get the scores (project data onto PCs)
    data = matrix
    scores = np.dot(data, principal_components)
    
    # Auto-scaling: make arrows lengths comparable to score spread
    if scaling is None:
        scaling = np.sqrt((scores ** 2).sum(axis=0)).mean() / \
                 np.sqrt((principal_components.values ** 2).sum(axis=0)).mean()
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if plot_type in ['scores', 'both']:
        # Plot scores (observations)
        scatter = ax.scatter(scores[:, 0], scores[:, 1], 
                           c='b', alpha=0.5, 
                           label='Occupations')
        max_range = abs(scores).max().max() * 1.1
        
    if plot_type in ['loadings', 'both']:
        # Plot variable loadings (arrows)
        for i, var in enumerate(data.columns):
            x = principal_components.iloc[i, 0] * scaling
            y = principal_components.iloc[i, 1] * scaling
            ax.arrow(0, 0, x, y, color='r', alpha=0.5, head_width=0.02)
            ax.text(x * 1.05, y * 1.05, var, 
                   color='r', ha='center', va='center', fontsize=8)
        max_range = abs(np.array([x * scaling for x in principal_components.values])).max() * 1.1
    
    if plot_type == 'both':
        max_range = max(
            abs(scores).max().max() * 1.1,
            abs(np.array([x * scaling for x in principal_components.values])).max() * 1.1
        )
    
    # Set axis limits based on what was plotted
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    
    # Add labels and title
    ax.set_xlabel(f'First Principal Component')
    ax.set_ylabel(f'Second Principal Component')
    plot_type_str = 'Scores' if plot_type == 'scores' else 'Loadings' if plot_type == 'loadings' else 'Biplot'
    ax.set_title(f'{plot_type_str} of O*NET Data\nScaling factor = {scaling:.2f}')
    
    # Add grid and legend
    ax.grid(True, alpha=0.3)
    if plot_type in ['scores', 'both']:
        ax.legend()
    
    plt.show()
    return fig, ax

def merge_categories_data(categories, version="29_2", scale_id="LV"):
    """
    Download and merge data from multiple categories.
    Only filter by scale_id for Knowledge, Skills, Abilities, and Work Activities.
    
    Parameters:
    -----------
    categories : list
        List of category names (e.g., ["Skills", "Abilities"])
    version : str
        O*NET database version (default: "29_2")
    scale_id : str
        Scale ID to filter by (e.g., "LV" or "IM")
        
    Returns:
    --------
    pandas.DataFrame
        Merged data matrix with O*NET-SOC Codes as index
    """
    all_data = []
    # Categories that use LV/IM scale IDs
    scale_id_categories = ["Knowledge", "Skills", "Abilities", "Work Activities"]
    
    for category in categories:
        # Download and process data for each category
        scaled_data = download_and_process_data(version=version, category=category)
        
        if scaled_data:
            # Create DataFrame from scaled data
            rows = []
            for data in scaled_data:
                # Only filter by scale_id for specific categories
                if category not in scale_id_categories or data['scale_id'] == scale_id:
                    row = {
                        'O*NET-SOC Code': data['row_data'][0],
                        'Element Name': data['row_data'][2],
                        'Scaled Value': data['scaled']
                    }
                    rows.append(row)
            
            # Convert to DataFrame and continue with existing logic
            df = pd.DataFrame(rows)
            
            # Create pivot table with Element Names as columns
            pivot_df = pd.pivot_table(df,
                                    values='Scaled Value',
                                    index='O*NET-SOC Code',
                                    columns='Element Name',
                                    fill_value=0)
            
            # Add category prefix to column names to avoid duplicates
            pivot_df.columns = [f"{category}_{col}" for col in pivot_df.columns]
            
            all_data.append(pivot_df)
    
    if not all_data:
        return None
    
    # Merge all DataFrames on O*NET-SOC Code
    final_matrix = pd.concat(all_data, axis=1)
    
    # Fill any remaining NaN values with 0
    final_matrix = final_matrix.fillna(0)
    
    return final_matrix

def write_loadings_to_csv(matrix, principal_components, prop_var, output_file):
    """
    Write PCA loadings and variance explained to CSV file
    
    Parameters:
    -----------
    matrix : pandas DataFrame
        Original data matrix
    principal_components : pandas DataFrame
        Principal components from pca_scaleid
    prop_var : numpy array
        Proportion of variance explained by each PC
    output_file : str
        Path to output CSV file
    """
    # Create DataFrame with variable names and their loadings
    loadings_df = pd.DataFrame(
        principal_components.values,
        columns=[f'PC{i+1}' for i in range(principal_components.shape[1])],
        index=matrix.columns
    )
    
    # Add variance explained as a final row
    var_explained = pd.DataFrame(
        [prop_var * 100],  # Convert to percentage
        columns=loadings_df.columns,
        index=['% Variance Explained']
    )
    
    final_df = pd.concat([loadings_df, var_explained])
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to CSV
    final_df.to_csv(output_file)
    print(f"Loadings written to: {output_file}")
    
    return final_df

