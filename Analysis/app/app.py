from shiny import App, ui
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv("quakes-cleaned.csv")
data = data.fillna('')

# Map of plot choices (including the new plots 3, 4, and 5)
SelectMap = {
    "plot1": "Top 10 Geographical Areas with the Most Seismic Activity",
    "plot2": "Top 5 Contributors to Earthquake Measurements",
    "plot3": "Treemap of Depth Errors by Territory",
    "plot4": "Funnel Plot of Seismic Types",
    "plot5": "Line Graph of Top 5 Territories with Highest Number of Explosions"
}

# UI layout of the Shiny app
app_ui = ui.page_fluid(
    ui.h1("Earthquake Data Analysis"),
    
    ui.input_select(
        "SelectMap", "Select Map",
        choices=SelectMap
    ),

    ui.row(
        output_widget("map")        
    ),
)

# Server logic for handling user input and rendering plots
def server(input, output, session):
    @output
    @render_widget
    def map():
        SelectMap = input.SelectMap()

        # Plot 1: Top 10 Geographical Areas with the Most Seismic Activity
        if SelectMap == "plot1":
            seismic_activity_counts = data['Territory'].value_counts().head(10)
            seismic_activity_counts_df = seismic_activity_counts.reset_index()
            seismic_activity_counts_df.columns = ['Territory', 'Count']

            fig = px.bar(
                seismic_activity_counts_df,
                x='Territory',
                y='Count',
                title='Top 10 Geographical Areas with the Most Seismic Activity',
                labels={'Territory': 'Geographical Area', 'Count': 'Number of Seismic Activities'},
                color='Territory'
            )
            fig.update_layout(
                xaxis_title='Geographical Area',
                yaxis_title='Number of Seismic Activities',
                showlegend=False
            )
            return fig

        # Plot 2: Top 5 Contributors to Earthquake Measurements
        if SelectMap == "plot2":
            top_contributors = data['net'].value_counts().head(5)
            fig = px.pie(
                names=top_contributors.index,
                values=top_contributors.values,
                title='Top 5 Contributors to Earthquake Measurements'
            )
            return fig

        # Plot 3: Treemap of Depth Errors by Territory
        if SelectMap == "plot3":
            depth_error_areas = data.groupby('Territory')['depthError'].mean().reset_index()
            depth_error_areas_sorted = depth_error_areas.sort_values(by='depthError', ascending=False)
            fig = px.treemap(
                depth_error_areas_sorted,
                path=['Territory'],
                values='depthError',
                title='Treemap of Depth Errors by Territory',
                labels={'depthError': 'Average Depth Error (km)'}
            )
            return fig

        # Plot 4: Funnel Plot of Seismic Types
        if SelectMap == "plot4":
            most_seismic_activity_types = data['type'].value_counts().reset_index()
            most_seismic_activity_types.columns = ['Type', 'Count']
            fig = px.funnel(
                most_seismic_activity_types,
                x='Count',
                y='Type', 
                title='Funnel Plot of Seismic Types',
                labels={'Count': 'Number of Seismic Events', 'Type': 'Seismic Type'}
            )
            return fig

        # Plot 5: Line Graph of Top 5 Territories with Highest Number of Explosions
        if SelectMap == "plot5":
            explosions_data = data[data['type'].str.lower() == 'explosion']
            top_explosion_territories = explosions_data['Territory'].value_counts().head(5).reset_index()
            top_explosion_territories.columns = ['Territory', 'Count']
            fig = px.line(
                top_explosion_territories,
                x='Territory',
                y='Count',
                title='Line Graph of Top 5 Territories with Highest Number of Explosions',
                labels={'Territory': 'Territory', 'Count': 'Number of Explosions'}
            )
            return fig

# Create the Shiny app
app = App(app_ui, server)
