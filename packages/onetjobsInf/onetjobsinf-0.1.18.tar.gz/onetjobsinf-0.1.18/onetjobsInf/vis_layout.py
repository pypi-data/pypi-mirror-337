from dash import Dash, html, dcc
import pandas as pd
import os
import json

# Layout.py includes all the HTML and CSS for the dashboard.
# It defines the layout of the app, including dropdowns for selecting occupations and datasets,
# as well as the radar plots for visualizing the selected data.

def update_title_options(folder_path):
    """
    Update the title options for the dropdown based on the static dataset.
    This function reads the 'Occupation Data.txt' file and creates a list of unique titles
    with their corresponding O*NET-SOC codes for the dropdown options.
    """
    # Load the static dataset for titles
    static_titles_df = pd.read_csv(os.path.join(folder_path, 'Occupation Data.txt'), sep='\t')
    titles = static_titles_df['Title'].unique()
    options = [{'label': f"{title} ({static_titles_df[static_titles_df['Title'] == title]['O*NET-SOC Code'].values[0]})", 'value': static_titles_df[static_titles_df['Title'] == title]['O*NET-SOC Code'].values[0]} for title in titles]
    return options

def create_layout(app: Dash):
    """
    Create the layout for the Dash app.
    This includes the dropdowns for selecting occupations and datasets,
    as well as the radar plots for visualizing the selected data.
    """
    folder_path = os.path.join(os.path.dirname(__file__), 'src_data/')
    title_options = update_title_options(folder_path)
    with open(os.path.join(folder_path, 'element_name_dict.json'), 'r') as f:
        element_options = json.load(f)

    layout = html.Div([
        html.Div([
            # Right side: Description and O*NET attribution stacked vertically
            html.Div([
                html.H1("Job Comparison Dashboard", style={'text-align': 'center', 'margin-bottom': '20px', 'font-family': 'sans-serif', 'font-size': '32px', 'color': 'royalblue'}),
                html.Div("This app allows you to compare up to 2 occupations using O*NET data. You can select the datasets and metrics you want to visualize for both occupations. Click \"Update Graph\" to see your selections on the radar plots.", style={'margin-bottom': '20px', 'width': '100%', 'font-family': 'sans-serif'}),
                html.Div([
                    html.P(style={"text-align": "center"}, children=[
                        html.A(href="https://services.onetcenter.org/", title="This app incorporates information from O*NET Web Services. Click to learn more."),
                        html.Img(src="https://www.onetcenter.org/image/link/onet-in-it.svg", style={"width": "100px", "height": "45px", "border": "none"}, alt="O*NET in-it")
                    ]),
                    html.P(children=[
                        "This site incorporates information from ",
                        html.A("O*NET Web Services", href="https://services.onetcenter.org/"),
                        " by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). O*NET® is a trademark of USDOL/ETA."
                    ], style={'font-size': '12px', 'padding': '10px'})
                ])
            ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '4%' }),
            # Left side: Dropdowns
            html.Div([
                html.Div("1. Select up to 2 Occupations, represented by O*NET-SOC codes, to visualize.", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                dcc.Dropdown(
                    id='title-dropdown',
                    options=title_options,
                    multi=True,
                    placeholder="Select 2 titles",
                    value=['15-2041.01', '19-1041.00'],  # Default selected O*NET-SOC codes
                    style={'width': '100%', 'margin-bottom': '20px'}
                ),
                html.Div("2. Select which datasets you would like for comparison of the occupations.", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                html.Div([
                    dcc.Checklist(
                        id='dataset-checklist',
                        options=[
                            {'label': 'Skills', 'value': 'Skills'},
                            {'label': 'Knowledge', 'value': 'Knowledge'},
                            {'label': 'Abilities', 'value': 'Abilities'}
                        ],
                        value=['Skills'],  # Default selected datasets
                        labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                        style={'margin-bottom': '20px'}
                    )
                ]),
                html.Div("3. Select as many metrics as you would like to visualize for the selected occupations.", style={'font-weight': 'bold'}),
                html.Div("Value represents \'importance\' on a scale of 0 to 7. Please note that not all metrics have confidence intervals.", style={'font-size':'12px', 'margin-bottom': '10px'}),
                html.Div(id='element-dropdowns-container', children=[
                    html.Div([
                        dcc.Dropdown(
                            id='skills-dropdown',
                            options=[{'label': metric, 'value': metric} for metric in element_options['skills']],  # Skills dropdown shown by default
                            multi=True,
                            placeholder="Select Skills",
                            value=['Mathematics', 'Writing', 'Science'],
                            style={'width': '100%', 'margin-bottom': '10px'}  # Default selected skills
                        ),
                        dcc.Dropdown(
                            id='knowledge-dropdown',
                            options=[{'label': metric, 'value': metric} for metric in element_options['knowledge']],  
                            multi=True,
                            placeholder="Select Knowledge",
                            style={'width': '100%', 'margin-bottom': '20px'}  # Initially hidden, will be shown based on dataset selection
                        ),
                        dcc.Dropdown(
                            id='abilities-dropdown',
                            options=[{'label': metric, 'value': metric} for metric in element_options['abilities']],  
                            multi=True,
                            placeholder="Select Abilities",
                            style={'width': '100%', 'margin-bottom': '20px'}  # Initially hidden, will be shown based on dataset selection
                        )
                    ]),
                ]),
                html.Div("4. Click the button below to update the radar plots with your selections.", style={'font-weight': 'bold', 'margin-bottom': '10px', 'margin-top': '10px'}),
                html.Button('Update Graph', id='update-button', style={'font-size': '14px', 'padding': '10px 10px', 'background-color': 'white'}),
            ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0',  'backgroundColor': '#e6f7ff', 'padding': '20px', 'border-radius': '10px'}),
            
            
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
        html.Div(id='radar-plots', children=[
            dcc.Graph(id=f'radar-plot-{i}', style={'display': 'inline-block', 'width': '49%'}) for i in range(2)
        ])
    ])
    return layout