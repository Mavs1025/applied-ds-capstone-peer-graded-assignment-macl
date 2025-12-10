# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create a list of launch site options
launch_sites = spacex_df['Launch Site'].unique().tolist()
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
site_options.extend([{'label': site, 'value': site} for site in launch_sites])

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Add Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart for all or selected site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Scatter Chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ------------------------------
# TASK 2: Callback for Pie Chart
# ------------------------------
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Pie chart of success count for all sites
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Filter by site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success vs failure
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']

        fig = px.pie(
            success_counts,
            values='count',
            names='class',
            title=f"Success vs Failure for site: {entered_site}"
        )
        return fig

# -------------------------------------------------
# TASK 4: Callback for Payload vs. Success Scatter
# -------------------------------------------------
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    # Filter by payload range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        fig = px.scatter(
            df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Payload vs. Outcome for All Sites"
        )
        return fig

    else:
        # Filter by selected site
        df_site = df[df['Launch Site'] == selected_site]

        fig = px.scatter(
            df_site,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Payload vs. Outcome for {selected_site}"
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run()