from dash import Dash, html, dcc
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("daily_sales_output.csv")
df["date"] = pd.to_datetime(df["date"])

daily = df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

price_increase_date = "2021-01-15"

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["sales"],
    mode="lines",
    name="Daily Sales",
    line=dict(color="#E91E8C", width=2),
))

fig.add_vline(
    x=pd.Timestamp(price_increase_date).timestamp() * 1000,
    line_width=2,
    line_dash="dash",
    line_color="orange",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top right",
    annotation_font_size=13,
    annotation_font_color="orange",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    plot_bgcolor="#1e1e2e",
    paper_bgcolor="#1e1e2e",
    font=dict(color="#cdd6f4"),
    xaxis=dict(gridcolor="#313244"),
    yaxis=dict(gridcolor="#313244"),
    legend=dict(bgcolor="#313244"),
    margin=dict(l=60, r=40, t=40, b=60),
)

app = Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "#1e1e2e", "minHeight": "100vh", "padding": "24px", "fontFamily": "sans-serif"},
    children=[
        html.H1(
            "Soul Foods — Pink Morsel Sales Visualiser",
            style={"color": "#cdd6f4", "textAlign": "center", "marginBottom": "8px"},
        ),
        html.P(
            "Daily total sales across all regions. The dashed line marks the Pink Morsel price increase on 15 January 2021.",
            style={"color": "#a6adc8", "textAlign": "center", "marginBottom": "24px"},
        ),
        dcc.Graph(figure=fig, style={"height": "600px"}),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
