# Import necessary libraries
import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import seaborn as sns
from ipyleaflet import Map
from palmerpenguins import load_penguins
from shiny import reactive

# Load the Palmer Penguins dataset into a Pandas DataFrame
penguins_df = load_penguins()

# Define the UI sidebar and main content items
ui.page_opts(title="Penguin Data Monsuru")

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute", "Choose a Column", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", value=20)
    ui.input_slider("seaborn_bin_count", "Number of Seaborn Bins", 1, 20, 5)
    ui.input_checkbox_group("selected_species_list", "Select Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie"], inline=True)
    ui.input_text("Text", "Enter text", "Hello Shiny")
    ui.hr()
    ui.a("GitHub", href="https://github.com/don4ye/cintel-02-data.git", target="_blank")

# Add your layout for the main content area below
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Penguin Mass")

        @render_widget
        def plot():
            scatterplot = px.histogram(
                data_frame=filtered_data(),  # Use filtered_data instead of penguins_df
                x=input.selected_attribute(),  # Use the selected attribute here
                nbins=input.plotly_bin_count(),
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="Selected Attribute",  # Update the x-axis title
            )

            return scatterplot

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Penguin Mass")

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
        def seaborn_histogram():
            ax = sns.histplot(data=filtered_data(), x=input.selected_attribute(), bins=input.seaborn_bin_count())  
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Selected Attribute")  # Update the x-axis label
            ax.set_ylabel("Count")
            return ax

    with ui.card(full_screen=True):
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data())

        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(filtered_data())

    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        
        @render_plotly
        def plotly_scatterplot():
            scatterplot = px.scatter(filtered_data(), x="bill_length_mm", y="bill_depth_mm", color="species")
            return scatterplot

    with ui.card(full_screen=True):
        ui.card_header("An ipyleaflet Map")

        @render_widget  
        def map():
            return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)

    with ui.card(full_screen=True):
        ui.card_header("Input Text")

        @render.text
        def text():
            return input.Text()

# Reactive calculations and effects
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
