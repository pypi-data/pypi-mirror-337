[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Aem1sI_4)


## Overview

The goal of this package is to provide the user with tools to explore the Occupational Information Network (O\*NET) Database. The O\*NET Database is a job exposure matrix that catalogs over 900 occupations and over 250 metrics that describe these occupations, for example in terms of Skills, Knowledge, and Abilities (which are the primary focus of this version of the package).

The package includes three main functionalities in addition to numerous ways of importing and interpreting the O\*NET data. 

The first functionality is a **Principal Components Analysis**. Using the principal component analysis functions in this package allows a user to summarize occupation metrics by describing axes of variability and the relationships between variables and components. This helps to identify patterns and reduce dimensionality in the dataset, and may help a researcher or user relate these variables to real-life outcomes.

The second set of functions in this package are a **Breadth-First Search (BFS) algorithm** designed to identify jobs similar to a given job based on shared skills, abilities, or knowledge. These BFS algorithms traverse the O\*NET database, calculating similarity scores and returning jobs that meet a user-defined similarity threshold. The results provide users with a list of related jobs and the specific attributes that connect them, aiding in career exploration and analysis.

The final set of functions in this package are used to create an **interactive visualization dashboard**. This visualization allows a user to do exploratory data analysis of the contents of the O\*NET datasets and to to contrast the values of occupation metrics between any two jobs. A user can select any two occupations (indexed by name and O\*NET code), and contrast the importance of skills, abilities, or knowledge using radar plots. Each of these three datasets has a number of unique elements which can be selected and compared, most of which also have confidence intervals around the importance estimates. 

For the public, this package can be used as a career exploration tool, allowing users to find occupations that are similar or different to their current occupation. This tool can help people decide whether or not they want to make a career switch. 


## Package Installation


This package is released on PyPI. To install this package, run: 

```bash
pip install onetjobsInf
```

Any function in the package can then be imported for use. See below for usage details.



## Data

This package uses job exposure matrices, available from the O\*NET Research Centre (https://www.onetcenter.org/dictionary/29.2/excel/). The O\*NET database is a periodically updating dataset which contains information for a number of occupations. The information collected includes skills and activities, required knowledge and education, and working environment and conditions. The attributes of each profession are scored on a scale, and O\*NET recommends scaling from 0 to 100 for most applications. 

The data can be downloaded locally or accessed via an API.

## Package Contents

- [Data Scaffolding](#data-scaffolding)
    -[Raw Data](#raw-data)
    -[API](#data-from-api)
- [Algorithm Implementation](#algorithm-implementation)
- [Linear Algebra Application: Principal Component Analysis](#linear-algebra-application-principal-component-analysis)
- [Interactive Visualization](#interactive-visualization)
    - [Visualization Functions](#visualization-files-and-functions)
    - [Updating the Dropdown Menus (from GitHub Source)](#updating-the-dropdown-menus-from-github-source)
- [Contributions](#contributions)

### Data Scaffolding

We have two main types of functions allowing the user to import and use select data from the O\*NET database. One option is to read in the raw .txt files (does not require API use); the other option is to call the O\*NET Web Services API with your credentials. Which type is used in the package, and the specifics of the data scaffolding, depend on the function of interest.

#### Raw Data

**Standardized Data from Any Database Version for PCA**:

Because variables in the O\*NET database often have different scales, the O\*NET website provides recommendations for standardizing these variables from 0 to 100 for ease of interpretation. 

This package implements the following function to download, standardize, and combine data of user-specified O\*NET categories from any user-specified O\*NET version. For principal components analysis, it is important to use standardized data so that one category of data does not dominate the analyses due to differences in scale of variables. The following function defined in `pca_run.py` performs data scaffolding of standardized data from any database version:
    
- `merge_categories_data(categories, version="29_2", scale_id="LV")`
    - **Purpose**: Downloads and scales data from user-specified O\*NET categories and combines these data into a single matrix.
    - **Parameters**:
        - `categories`: List of variables category names (e.g., ["Skills", "Abilities"]). Valid options include "Skills", "Knowledge", "Abilities", "Work Activities," "Work Values", "Work Styles", "Interests."
        - `version`: O\*NET database version with period replaced by underscore (e.g., "29_2" for version 29.2). Other values can be passed as the version parameter to access data from older versions of the database. 
        - `scale_id`: For Knowledge, Skills, Abilities, and Work Activities categories, the O\*NET database provides both Level (LV) and Importance (IM) ratings. When using data from any of these catories, the user should specify which scale identifier to use. Options are:
            - "LV" (Level) 
            - "IM" (Importance)
    - **Output**: DataFrame with one column of "O\*NET-SOC Code," another column of "Element Name" which is a list of occupation variables, and another column as "Scaled Value" which is the data value for the Element Name and O\*NET-SOC Code.

**Data Values and CI Bounds for Visualization**:

For visualization, raw text files are downloaded from the O\*NET database in two ways using functions in `vis_download_files.py`: 

- `download_occups(local_filename='onetjobsInf/src_data/Occupation Data.txt')`:
    - **Purpose**: Downloads the static Occupation Data file into the src_data folder as a text file.
    - **Parameters**: Prepopulated, uses  `local_filename='onetjobsInf/src_data/Occupation Data.txt'` to determine where the static file will be stored.
    - **Output**: Text file with O\*NET-SOC Codes, Titles, and Job Descriptions.

- `download_txtfile_aspd(url)`:
    - **Purpose**: Downloads data from dynamic checklist input O\*NET categories and stores the data as a pandas data frame for use in populating the visualization.
    - **Parameters**:
        - `url`: Provided through combination of base url ("'https://www.onetcenter.org/dl_files/database/db_25_1_text/'") and dataset name chosen by the checklist (current options: Skills, Knowledge, Abilities).
    - **Output**: pandas data frame with columns 'O\*NET-SOC Code', 'Element Name', 'Element ID', 'Scale ID', 'Data Value', 'Lower CI Bound', and 'Upper CI Bound', all required for the visualization. Note that Scale ID is fixed to IM (Importance) in the visualization.

#### Data from API

**Populating the elements of the dataset dropdowns in the visualization**:

Note that the visualization does not dynamically use the API in order to make the visual available to anyone, even without API credentials. The script `vis_call_labels.py` (which calls the following function) can be run if the elements in the dropdowns need to be updated. 

- `get_elements.py(onet_service, table_id, colname='element_name', **query_params)`: 
    - **Purpose**: Obtains all the unique element names from the provided dataset and returns it as a list.
    - **Parameters**:
        - `onet_service`: API call class (`OnetWebService`)
        - `table_id`: Name of the dataset to query in the API. Values currently queried are: Skills, Abilities, Knowledge
        - `colname`: Any feature of the dataset could be chosen, we use element name (string).
        - `query_params`: Additional filter parameters passed to the API call. 
    - **Output**: List of unique values in the column and table specified.

**API Searches**:

In `bfs_[table]_search.py`:

- `get_abilities(onet_service, job_code)`, `get_skills(onet_service, job_code)`, `get_(onet_service, job_code)`:
    - **Purpose**: Obtains the Abilities, Skills, or Knowledge elements and their values for a given job code.
    - **Parameters**:
        - Requires API credentials
        - `onet_service`: API call class (`OnetWebService`)
        - `job_code`: O\*NET-SOC Code for the occupation of interest
    - **Output**: Returns the results of the API call.


### Algorithm Implementation: Breadth First Search

Here, we implement 3 BFS algorithms to find jobs that are similar to the inputted job ID on the basis of their associated skills, abilities, or knowledges. The implementation is primarily located in the `bfs)job_abilities_graph.py`, `bfs_job_knowledge_graph.py`, and `bfs_job_skills_graph.py`. The algorithm functions similarly for the three sets of criteria. For example, to find jobs that are similar to the inputted job on the basis of associated skills, the algorithm
  - Starts with initial job ID 
  - Gets its key skills from API (depending on the file)
  - BFS Algorithm Step-by-Step:
      1. Initialize queue with starting job and its skills data
      2. For each job in queue:
            - Queries the skills of all other jobs in the ONET database 
            - Calculate similarity based on shared skills (number of shared skills / number of skills returned for the original job id)
            - Add jobs that meet similarity threshold to results and queue
            - Continue this algorithm until queue is empty or termination conditions met
      3. Returns list of similar jobs and relevant skills based on the original job ID. 

To run the algorithm from the source code: 

```bash
python src/bfs_job_abilities_graph.py`
```

The user can also specify the following arguments: 
```bash
python src/bfs_job_abilities_graph.py [JOB_ID] [SIMILARITY_TRHESHOLD] [MAX_JOBS]`
```

To run the algorithm from the package:

```python
from onetjobsInf.bfs_job_skills_graph import JobSkillsNetwork

# Initialize the JobSkillsNetwork
network = JobSkillsNetwork()

# Run the algorithm
related_jobs, all_skills = network.explore_job_skills_network("29-2099.01", similarity_threshold=0.75, max_jobs=None)
print(related_jobs)
print(all_skills)
```
or to run tests for all BFS search scripts the associated tests

```bash
python -m unittest onetjobsInf.test.test_BFS_search`
```

In developing these algorithms, we created several API calls that could be useful in and of themselves. The scripts for knowledge, skills, and abilities are structured similar. 



### Linear Algebra Application: Principal Component Analysis

Our package implements Principal Component Analysis (PCA) through computing eigenvalues and eigenvectors, offering several functions for analyzing and visualizing O\*NET occupational data:

#### Main Functions

1. `merge_categories_data(categories, version="29_2", scale_id="LV")`
   - **Purpose**: Downloads and scales data from multiple O\*NET categories and combines these data into a single matrix. See Scaffolding section for more details on scaling.
   - **Parameters**:
     - `categories`: List of variables category names (e.g., ["Skills", "Abilities"]). Valid options include "Skills", "Knowledge", "Abilities", "Work Activities," "Work Values", "Work Styles", "Interests."
     - `version`: O\*NET database version with period replaced by underscore (e.g., "29_2" for version 29.2)
     - `scale_id`: For Knowledge, Skills, Abilities, and Work Activities categories, the O\*NET database provides both Level (LV) and Importance (IM) ratings. When using data from any of these catories, the user should specify which scale identifier to use. Options are:
           - "LV" (Level) 
           - "IM" (Importance)
   - **Output**: DataFrame with one column of "O\*NET-SOC Code," another column of "Element Name" which is a list of occupation variables, and another column as "Scaled Value" which is the data value for the Element Name and O\*NET-SOC Code.

2. `pca_scaleid(matrix, k=2)`
   - **Purpose**: Performs PCA on the provided data matrix
   - **Parameters**:
     - `matrix`: Pandas DataFrame containing the merged occupational data in the format of the output from merge_categories_data
     - `k`: Number of principal components to compute (default=2)
   - **Output**: Tuple containing:
     - Principal components as a DataFrame
     - Array of variance proportions explained by each component

3. `create_biplot(matrix, principal_components, scaling=None, plot_type='loadings')`
   - **Purpose**: Creates visualization of PCA results
   - **Parameters**:
     - `matrix`: Original data matrix used in PCA
     - `principal_components`: PCA results from pca_scaleid()
     - `scaling`: Float value to scale the loadings arrows (None for auto-scaling)
     - `plot_type`: Visualization type:
       - 'scores': Shows only the occupation points
       - 'loadings': Shows only the variable loadings
       - 'both': Shows both scores and loadings (full biplot)
   - **Output**: Matplotlib biplot figure and axes objects showing PCA visualization. The "Scaling factor" value indicated at the top of the plot is the multiplicative factor by which the ploted values have been scaled by. The benefit of scaling is that it spreads out the variable names when plotting the loadings so that the variable names can be read from the biplot. 

4. `write_loadings_to_csv(matrix, principal_components, prop_var, output_file)`
   - **Purpose**: Saves PCA results to a CSV file
   - **Parameters**:
     - `matrix`: Original data matrix used in PCA
     - `principal_components`: PCA results from pca_scaleid()
     - `prop_var`: Array of variance proportions from pca_scaleid()
     - `output_file`: Path where the CSV file should be saved
   - **Output**: CSV file containing:
     - Variable loadings for each principal component
     - Percentage of variance explained by each component

##### Example Usage

```python
# Merge multiple categories of O\*NET data
categories = ["Skills", "Abilities", "Knowledge"]
merged_data = merge_categories_data(categories)

# Perform PCA
pcs, variance = pca_scaleid(merged_data, k=2)

# Create visualization
create_biplot(merged_data, pcs, plot_type='loadings')

# Save results
write_loadings_to_csv(merged_data, pcs, variance, "pca_results.csv")
```

### Interactive Visualization

This package uses `DASH` to make an app in Python with dynamically updating figures, in this case radar plots. Using three dropdowns and a checklist, a user can select which occupations (maximum of 2) to plot the charactersitics ("elements") of. Elements can be pulled from any of two (in the static app) or three (in the most recent version of the package) O\*NET datasets. Dropdowns appear and data is imported as the user selects datasets in the checklist. By clicking the update button, the radar plots refresh their contents with the selections. 

#### Viewing the comparison dashboard

There are two options for visualization depending on your needs. 

##### Static App

If you simply wish to explore occupations based on skills, abilities, and knowledge as collected in the O\*NET database, you can use the static version of the app online. You can access this version of the app at [bst236-onetcompare](https://bst236-onetcompare-a23cabb5a2d4.herokuapp.com/).  

This app is hosted using **Heroku** (link). The github repository for its source code is available at [bst236-onetcompare-app GitHub](https://github.com/panevins/bst236-onetcompare-app). 

##### Local Viewing

To run the app locally, from the package, open a new Python interpreter with the following content. 

```python
from onetjobsInf.vis_app import vis_app_run
vis_app_run()
```
Run this Python script and the address provided to you to view the app locally in your browser. 

If you would like to update any of the data (e.g., using a subset of occupations or metrics, or import a new dataset beyond skills, abilities, and knowledge), or wish to use an alternate published version of the O\*NET data, you may download and modify the source code. To do so, clone the source code GitHub repository:

```bash
git clone https://github.com/panevins/bst236-onetcompare-app
cd onetjobsInf
```

You can then modify the internal functions of this package (described below). To run the app locally and see the changes, run the following on the command line and navigate to the address provided to you to view the app locally. 

```bash
python3 vis_app.py
```

#### Visualization Files and Functions

* `vis_app.py`: 

    1. `fetch_dataset` and `generate_url` are used to import the data as a text file and store it as a pandas data frame for use on the app. The data is only downloaded if it is not already stored locally in the dataset cache. This avoids repeat calls for the same data.
    
    2. `update_dropdown_visibility(selected_datasets)`: Given user input in the form of checked boxes on the app page, dropdowns for each selected dataset appear. If unselected, no metrics from that dataset can be plotted.

    3. `update_radar_plots`: The workhorse function which creates and updates radar plots. It takes as input a click of the \"update\" button, as well as the list of selected datasets, selected occupations (\"titles\") and selected metrics for each selected dataset. It then filters the imported data frames according to the selections, and outputs two radar plots (one for each occupation) with all selected elements on the axes for comparison.

* `vis_layout.py`:

    1. `update_title_options`: Takes the static list of occupations in `src_data/Occupation Data.txt` and imports them to populate the occupation dropdown.

    2. `create_layout`: Includes all the HTML and CSS for the app visualization, as well as the interactive dropdowns, checklist, and button.

* `vis_call_elements.py`: Internal functions used by `vis_call_labels.py` to populate the elements in the dropdowns for each dataset. Requires API credentials; results are stored statically in `src_data/element_name_dict.json`

* `vis_download_files.py`: Function `download_occups` called by `vis_layout.py` to populate the `Occupation Data.txt` file of static occupation titles. Function `download_textfiles_aspd` called by `vis_app.py` to populate the data values when a dataset is selected by checkbox and isn't already in the cache. 


##### Updating the dropdown menus (from GitHub source)

By default, this app uses a static list of occupations and elements to populate the dropdowns. To modify these, first clone the GitHub repository:

```bash
git clone https://github.com/panevins/bst236-onetcompare-app
```

* To update the list of elements (for example, if a new element is added to the O\*NET database or if new datasets are incorporated into the visualization), run the following in the command line:

```bash
python3 vis_call_labels.py
```
You will be prompted to enter your O\*NET Web Services credentials. Information about API access to the O\*NET data can be found at https://services.onetcenter.org/. Once entered, the script will automatically populate the element_name_dict.json called in `layout.py` to populate the dropdowns for each selected dataset.

* To update the list of occupations from O\*NET, we need to read in the text file found at https://www.onetcenter.org/dl_files/database/db_25_1_text/Occupation Data.txt. This can be done in a manner of your choosing, or by running in the command line:

```bash
python3 vis_download_files.py
```

## Contributions

* H Jin: PCA, Scaffolding

* M Carbonneau: BFS, Scaffolding

* P Nevins: Visualization, Scaffolding