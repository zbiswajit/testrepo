# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                 ],
                 value='ALL',
                 placeholder="Select site",
                 searchable=True,
                 multi=False),
    
    html.Br(),
    
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        min=0,
        max=10000,
        step=1000,
        value=[min(spacex_df['Payload Mass (kg)']), max(spacex_df['Payload Mass (kg)'])]
    ),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback to update the pie chart based on the selected site
@app.callback(Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        selected_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(selected_data, names='class', title=f'Success Launches at {selected_site}')
    return fig

# Callback to update the scatter chart based on the payload range selected
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('payload-slider', 'value')])
def update_scatter_chart(payload_range):
    # Filter the DataFrame based on the selected payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create a scatter chart using plotly express
    scatter_chart = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Launch Site',
        title='Correlation between Payload Mass and Launch Success',
        labels={'Payload Mass (kg)': 'Payload Mass', 'class': 'Launch Success'},
        height=400
    )

    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
