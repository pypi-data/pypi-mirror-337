import sys
import os
import matplotlib.pyplot as plt

from onetjobsInf.pca_run import pca_scaleid, create_biplot, merge_categories_data, write_loadings_to_csv

# Download and merge Skills and Abilities data
categories = ["Skills", "Abilities"]
combined_matrix = merge_categories_data(categories=categories, version="29_2", scale_id="LV")

print("Combined matrix dimensions:", combined_matrix.shape)
print("\nColumns in combined matrix:", combined_matrix.columns)

# Perform PCA on combined data
principal_components, prop_var = pca_scaleid(matrix=combined_matrix, k=2)

# Print results
print("\nPrincipal Components:")
print(principal_components.head(10))
print("\nProportion of variance explained:", prop_var)

# Write loadings to CSV file
output_dir = os.path.join(os.path.dirname(__file__), 'example_data')
output_file = os.path.join(output_dir, 'pca_loadings_skills_abilities.csv')
loadings_df = write_loadings_to_csv(combined_matrix, principal_components, prop_var, output_file)


# Create biplot of combined data
create_biplot(matrix=combined_matrix, principal_components=principal_components, plot_type='loadings')
create_biplot(matrix=combined_matrix, principal_components=principal_components, plot_type='scores')