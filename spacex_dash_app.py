import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

spacex_df = pd.read_csv(DATA_URL)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = dash.Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": site, "value": site}
    for site in sorted(spacex_df["Launch Site"].dropna().unique())
]

app.layout = html.Div(
    [
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 36},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=site_options,
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
            style={"width": "80%", "margin": "0 auto"},
        ),
        html.Br(),
        dcc.Graph(id="success-pie-chart"),
        html.P("Payload range (kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={i: str(i) for i in range(0, 10001, 2500)},
            value=[0, 10000],
        ),
        dcc.Graph(id="success-payload-scatter-chart"),
    ],
    style={"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"},
)


@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        grouped = (
            spacex_df.groupby("Launch Site", as_index=False)["class"].sum()
        )
        return px.pie(
            grouped,
            values="class",
            names="Launch Site",
            title="Total Successful Launches by Site",
        )

    filtered = spacex_df[spacex_df["Launch Site"] == entered_site]
    counts = filtered["class"].value_counts().rename_axis("class").reset_index(name="count")
    counts["Outcome"] = counts["class"].map({0: "Failure", 1: "Success"})
    return px.pie(
        counts,
        values="count",
        names="Outcome",
        title=f"Launch Outcomes for {entered_site}",
    )


@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def get_payload_chart(entered_site, payload_range):
    low, high = payload_range
    filtered = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ]
    if entered_site != "ALL":
        filtered = filtered[filtered["Launch Site"] == entered_site]

    return px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title="Payload Mass vs. Launch Outcome",
        labels={"class": "Landing Outcome (0 = failure, 1 = success)"},
    )


if __name__ == "__main__":
    app.run(debug=True)
