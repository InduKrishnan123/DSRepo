# Import required libraries
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Load SpaceX launch data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Launch Site Dropdown
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] +
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),

    html.Br(),

    # Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # Payload Range Slider
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    marks={i: str(i) for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),

    html.Br(),

    # Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Pie Chart Callback
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,
                     names='Launch Site',
                     values='class',  # ✅ corrected to lowercase 'class'
                     title='Total Success Launches for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(site_counts,
                     names='class',
                     values='count',
                     title=f'Success vs Failure for Site: {entered_site}')
    return fig

# Scatter Chart Callback
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',  # ✅ corrected to lowercase 'class'
                         color='Booster Version Category',
                         title='Payload vs Launch Outcome for All Sites')
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df,
                         x='Payload Mass (kg)',
                         y='class',  # ✅ corrected to lowercase 'class'
                         color='Booster Version Category',
                         title=f'Payload vs Launch Outcome for Site: {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8060)
