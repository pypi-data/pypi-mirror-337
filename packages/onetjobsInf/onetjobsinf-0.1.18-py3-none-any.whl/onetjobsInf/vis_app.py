from dash import Dash, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import os
import sys

# Importing the necessary functions from other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'onetjobsInf')))
from vis_layout import create_layout
from vis_download_files import download_txtfile_aspd

# This script sets up a Dash application for visualizing O*NET data using radar plots.
app = Dash(__name__)
app.layout = create_layout(app)

# Dictionary to cache fetched datasets
dataset_cache = {}

def generate_url(dataset_name):
    """
    Generate the URL for downloading the specified dataset from O*NET Center.
    """
    base_url = 'https://www.onetcenter.org/dl_files/database/db_25_1_text/'
    return f'{base_url}{dataset_name}.txt'

def fetch_dataset(dataset_name):
    """
    Fetch the specified dataset from the O*NET Center, using a cache to avoid redundant downloads.
    """
    # Check if the dataset is already in the cache  
    if dataset_name in dataset_cache:
        return dataset_cache[dataset_name]
    url = generate_url(dataset_name)
    df = download_txtfile_aspd(url)
    dataset_cache[dataset_name] = df
    return df

@app.callback(
    Output('skills-dropdown', 'style'),
    Output('knowledge-dropdown', 'style'),
    Output('abilities-dropdown', 'style'),
    Input('dataset-checklist', 'value')
)
def update_dropdown_visibility(selected_datasets):
    """
    Update the visibility of the skills, knowledge, and abilities dropdowns based on the selected datasets.
    """
    skills_style = {'display': 'block', 'width': '100%'} if 'Skills' in selected_datasets else {'display': 'none'}
    knowledge_style = {'display': 'block', 'width': '100%'} if 'Knowledge' in selected_datasets else {'display': 'none'}
    abilities_style = {'display': 'block', 'width': '100%'} if 'Abilities' in selected_datasets else {'display': 'none'}
    return skills_style, knowledge_style, abilities_style

@app.callback(
    [Output(f'radar-plot-{i}', 'figure') for i in range(2)],
    Input('update-button', 'n_clicks'),
    State('dataset-checklist', 'value'),
    State('title-dropdown', 'value'),
    State('skills-dropdown', 'value'),
    State('knowledge-dropdown', 'value'),
    State('abilities-dropdown', 'value')
)
def update_radar_plots(n_clicks, selected_datasets, selected_titles, selected_skills, selected_knowledge, selected_abilities):
    """
    Update the radar plots based on the selected datasets, titles, and skills/knowledge/abilities.
    """
    figures = []
    for i in range(2):
        if i < len(selected_titles):
            title = selected_titles[i]
            combined_df = pd.DataFrame()
            for dataset in selected_datasets:
                df = fetch_dataset(dataset)
                if dataset == "Skills":
                    filtered_df = df.loc[
                        (df['O*NET-SOC Code'] == title) &
                        (df['Element Name'].isin(selected_skills)) &
                        (df['Scale ID'] == "IM")
                    ].copy()  
                    # Prepend "Skill: " to distinguish skill elements
                    filtered_df.loc[:, 'Element Name'] = "Skill: " + filtered_df['Element Name']
                elif dataset == "Knowledge":
                    filtered_df = df.loc[
                        (df['O*NET-SOC Code'] == title) &
                        (df['Element Name'].isin(selected_knowledge)) &
                        (df['Scale ID'] == "IM")
                    ].copy()  # Use .copy() to avoid the warning
                    # Prepend "Knowledge: " to distinguish knowledge elements
                    filtered_df.loc[:, 'Element Name'] = "Knowledge: " + filtered_df['Element Name']
                elif dataset == "Abilities":
                    filtered_df = df.loc[
                        (df['O*NET-SOC Code'] == title) &
                        (df['Element Name'].isin(selected_abilities)) &
                        (df['Scale ID'] == "IM")
                    ].copy()  # Use .copy() to avoid the warning
                    # Prepend "Abilities: " to distinguish ability elements
                    filtered_df.loc[:, 'Element Name'] = "Ability: " + filtered_df['Element Name']
                else:
                    filtered_df = pd.DataFrame()

                if not filtered_df.empty:
                    combined_df = pd.concat([combined_df, filtered_df], ignore_index=True)

            data = []

            for col in ['Data Value', 'Lower CI Bound', 'Upper CI Bound']:
                fill = 'blue' if col == 'Data Value' else None
                line_color = 'black' if col in ['Lower CI Bound', 'Upper CI Bound'] else None
                if col in combined_df.columns:
                    r_values = combined_df[col].tolist()
                    theta_values = combined_df['Element Name'].tolist()
                    # Append the first element to the end to close the radar plot
                    r_values.append(r_values[0])
                    theta_values.append(theta_values[0])
                    fill = 'toself' if col == 'Data Value' else None
                    data.append(go.Scatterpolar(
                        r=r_values,
                        theta=theta_values,
                        fill=fill,
                        line=dict(color=line_color),
                        name=f'{col}'
                    ))
            figure = {
                'data': data,
                'layout': go.Layout(
                    title=f'Radar Plot for {title}',
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 7]
                        )
                    ),
                    showlegend=True
                )
            }
            figures.append(figure)
        else:
            empty_data = [go.Scatterpolar(
                r=[0] * len(selected_titles),
                theta=selected_titles,
                fill='toself',
                name='Empty'
            )]
            empty_figure = {
                'data': empty_data,
                'layout': go.Layout(
                    title='Empty Radar Plot',
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )
                    ),
                    showlegend=False
                )
            }
            figures.append(empty_figure)

    return figures

if __name__ == '__main__':
    app.run_server(debug=False)

def vis_app_run():
    """
    Run the Dash application for visualizing O*NET data.
    """
    app.run_server(debug=False)