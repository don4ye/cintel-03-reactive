import pandas as pd
import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
from palmerpenguins import load_penguins
import seaborn as sns
from ipyleaflet import Map

# Use the built-in function to load the Palmer Penguins dataset
penguins = load_penguins()
ui.page_opts(title="Penguin Data Monsuru")

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
    # Add text input
    ui.input_text("Text", "Enter text", "Hello Shiny")
    # Add a horizontal rule to the sidebar
    ui.hr()
    # Add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/don4ye/cintel-02-data.git", target="_blank")

# Add your layout for the main content area below

# Create a Shiny UI layout with five columns
with ui.layout_columns():
    # First column for the Plotly Histogram
    with ui.card(full_screen=True):  # full_screen option to view expanded plot
        ui.card_header("Plotly Histogram: Penguin Mass")

        @render_widget
        def plot():
            scatterplot = px.histogram(
                data_frame=penguins,
                x="body_mass_g",
                nbins=input.plotly_bin_count(),
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="Body Mass (g)",
            )

            return scatterplot

    # Second column for the Seaborn Histogram
    with ui.card(full_screen=True):  # full_screen option to view expanded plot
        ui.card_header("Seaborn Histogram: Penguin Mass")

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
        def seaborn_histogram():
            ax = sns.histplot(data=penguins, x="body_mass_g", bins=input.seaborn_bin_count())  
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Mass (g)")
            ax.set_ylabel("Count")
            return ax

    # Third column for the data table and data grid
    with ui.card(full_screen=True):  # full_screen option to view expanded table/grid
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(penguins)

        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(penguins)

    # Fourth column for the Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        
        # Define a function to render the Plotly Scatterplot
        @render_plotly
        def plotly_scatterplot():
            # Create a Plotly scatterplot using Plotly Express
            scatterplot = px.scatter(penguins, x="bill_length_mm", y="bill_depth_mm", color="species")
            return scatterplot

    # Fifth column for the ipyleaflet map
    with ui.card(full_screen=True):
        ui.card_header("An ipyleaflet Map")

        @render_widget  
        def map():
            return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)

    # Sixth column for the input text
    with ui.card(full_screen=True):
        ui.card_header("Input Text")

        @render.text
        def text():
            return input.Text()
