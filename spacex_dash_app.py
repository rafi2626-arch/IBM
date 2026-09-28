import pandas as pd
import dash

from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


# =========================================================
# LOAD DATA
# =========================================================

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# =========================================================
# CREATE DASH APP
# =========================================================

app = dash.Dash(__name__)


# =========================================================
# APP LAYOUT
# =========================================================

app.layout = html.Div(
    children=[

        # Dashboard title
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40
            }
        ),

        # =================================================
        # TASK 1
        # Launch Site Dropdown
        # =================================================

        dcc.Dropdown(
            id="site-dropdown",

            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"}
            ],

            value="ALL",

            placeholder="Select a Launch Site here",

            searchable=True
        ),

        html.Br(),

        # Pie Chart
        dcc.Graph(
            id="success-pie-chart"
        ),

        html.Br(),

        html.P("Payload range (Kg):"),

        # =================================================
        # TASK 3
        # Payload Range Slider
        # =================================================

        dcc.RangeSlider(
            id="payload-slider",

            min=0,
            max=10000,
            step=1000,

            marks={
                0: "0",
                2500: "2500",
                5000: "5000",
                7500: "7500",
                10000: "10000"
            },

            value=[min_payload, max_payload]
        ),

        html.Br(),

        # Scatter Chart
        dcc.Graph(
            id="success-payload-scatter-chart"
        )
    ]
)


# =========================================================
# TASK 2
# CALLBACK FOR PIE CHART
# =========================================================

@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),

    Input(
        component_id="site-dropdown",
        component_property="value"
    )
)
def get_pie_chart(entered_site):

    # ---------------------------------------------
    # ALL SITES
    # ---------------------------------------------

    if entered_site == "ALL":

        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches By Site"
        )

        return fig

    # ---------------------------------------------
    # SPECIFIC SITE
    # ---------------------------------------------

    else:

        filtered_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names="class",
            title=f"Total Success Launches for site {entered_site}"
        )

        return fig


# =========================================================
# TASK 4
# CALLBACK FOR PAYLOAD SCATTER CHART
# =========================================================

@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure"
    ),

    [
        Input(
            component_id="site-dropdown",
            component_property="value"
        ),

        Input(
            component_id="payload-slider",
            component_property="value"
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # Get selected payload range
    low_payload = payload_range[0]
    high_payload = payload_range[1]

    # Filter according to payload
    filtered_df = spacex_df[
        (
            spacex_df["Payload Mass (kg)"] >= low_payload
        )
        &
        (
            spacex_df["Payload Mass (kg)"] <= high_payload
        )
    ]

    # ---------------------------------------------
    # ALL SITES
    # ---------------------------------------------

    if entered_site == "ALL":

        fig = px.scatter(
            filtered_df,

            x="Payload Mass (kg)",

            y="class",

            color="Booster Version Category",

            title="Correlation between Payload and Success for all Sites"
        )

        return fig

    # ---------------------------------------------
    # SPECIFIC SITE
    # ---------------------------------------------

    else:

        site_df = filtered_df[
            filtered_df["Launch Site"] == entered_site
        ]

        fig = px.scatter(
            site_df,

            x="Payload Mass (kg)",

            y="class",

            color="Booster Version Category",

            title=f"Correlation between Payload and Success for site {entered_site}"
        )

        return fig


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=8050)