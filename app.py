import pandas as pd
import plotly.express as px
import seaborn as sns
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from ipyleaflet import Map
from shinywidgets import render_widget

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    # Add a second-level header to the sidebar
    ui.h2("Sidebar")
    # Add dropdown input to choose a column
    ui.input_selectize("selected_attribute", "Choose a Column", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
    # Add numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", value=20)
    # Add slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 20, 5)
    # Add checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Select Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie"], inline=True)
    # Add a horizontal rule to the sidebar
    ui.hr()
    # Add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/don4ye/cintel-02-data.git", target="_blank")

ui.page_opts(title="Penguin Data Monsuru")

# Create a layout with a single column to display the DataTable, Data Grid, Plotly Histogram, Seaborn Histogram, Plotly Scatterplot, ipyleaflet Map, and Shiny Text Input
with ui.layout_columns():
    # Define a function to render the DataTable
    @render.data_frame
    def render_penguins_df():
        # Return the DataFrame directly
        return penguins_df
    
    # Define a function to render the Data Grid
    @render.data_frame  
    def render_penguins_data_grid():
        # Return the Data Grid
        return render.DataGrid(penguins_df)
    
    # Define a function to render the Plotly Histogram
    @render_plotly
    def plot():
        # Create the Plotly Histogram
        histogram = px.histogram(
            data_frame=penguins_df,
            x="body_mass_g",
            nbins=input.plotly_bin_count()
        ).update_layout(
            title={"text": "Penguin Mass", "x": 0.5},
            yaxis_title="Count",
            xaxis_title="Body Mass (g)",
        )

        return histogram
    
    # Define a function to render the Seaborn Histogram
    @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")  
    def seaborn_histogram():
        ax = sns.histplot(data=penguins_df, x="body_mass_g", bins=input.seaborn_bin_count())  
        ax.set_title("Palmer Penguins")
        ax.set_xlabel("Mass (g)")
        ax.set_ylabel("Count")
        return ax
    
    # Define a function to render the Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            # Create a Plotly scatterplot using Plotly Express
            scatterplot = px.scatter(penguins_df, x="bill_length_mm", y="bill_depth_mm", color="species")
            return scatterplot
    
    # Define a function to render the ipyleaflet Map
    @render_widget  
    def map():
        return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)
    
    # Define a function to render the Shiny Text Input and Text
    with ui.card(full_screen=True):
        ui.card_header("Shiny Text Input and Text")
        
        ui.input_text("Text", "Enter text", "Hello Shiny")
        ui.p("You entered:")
        
        @render.text  
        def text():
            return input.Text()
