from dash import Dash, html, dcc, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("daily_sales_output.csv")
df["date"] = pd.to_datetime(df["date"])

PRICE_INCREASE_DATE = "2021-01-15"

REGION_COLORS = {
    "all":   "#E91E8C",
    "north": "#89b4fa",
    "south": "#a6e3a1",
    "east":  "#f38ba8",
    "west":  "#fab387",
}

app = Dash(__name__)

app.index_string = """<!DOCTYPE html>
<html>
<head>
  {%metas%}
  <title>Soul Foods Visualiser</title>
  {%favicon%}
  {%css%}
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #11111b; font-family: 'Inter', sans-serif; }

    .page-wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 40px 24px 60px;
    }

    .header {
      text-align: center;
      margin-bottom: 36px;
    }
    .header h1 {
      font-size: 2.2rem;
      font-weight: 800;
      background: linear-gradient(90deg, #E91E8C, #f38ba8, #fab387);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 10px;
    }
    .header p {
      color: #a6adc8;
      font-size: 0.95rem;
      max-width: 600px;
      margin: 0 auto;
      line-height: 1.6;
    }

    .card {
      background: #1e1e2e;
      border: 1px solid #313244;
      border-radius: 16px;
      padding: 28px 32px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    .filter-label {
      color: #cdd6f4;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }

    .radio-wrap {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 28px;
    }

    /* Style the Dash RadioItems labels */
    .radio-wrap label {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: #313244;
      color: #cdd6f4;
      padding: 8px 20px;
      border-radius: 999px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      border: 2px solid transparent;
      transition: background 0.2s, border-color 0.2s, color 0.2s;
      user-select: none;
    }
    .radio-wrap label:hover {
      background: #45475a;
    }
    .radio-wrap input[type="radio"] {
      accent-color: #E91E8C;
      width: 15px;
      height: 15px;
    }
    .radio-wrap input[type="radio"]:checked + span,
    .radio-wrap input[type="radio"]:checked {
      /* highlight handled by JS accent-color */
    }
  </style>
</head>
<body>
  {%app_entry%}
  <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>"""

app.layout = html.Div(className="page-wrap", children=[
    html.Div(className="header", children=[
        html.H1("Soul Foods — Pink Morsel Sales"),
        html.P(
            "Daily Pink Morsel sales by region. "
            "The dashed line marks the price increase on 15 January 2021 — "
            "use the filter below to explore how each region performed."
        ),
    ]),
    html.Div(className="card", children=[
        html.P("Filter by region", className="filter-label"),
        html.Div(className="radio-wrap", children=[
            dcc.RadioItems(
                id="region-filter",
                options=[
                    {"label": "All regions", "value": "all"},
                    {"label": "North",       "value": "north"},
                    {"label": "South",       "value": "south"},
                    {"label": "East",        "value": "east"},
                    {"label": "West",        "value": "west"},
                ],
                value="all",
                inline=True,
                inputStyle={"marginRight": "0"},
            ),
        ]),
        dcc.Graph(id="sales-chart", style={"height": "520px"}),
    ]),
])


@callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    color = REGION_COLORS.get(region, "#E91E8C")
    label = "All Regions" if region == "all" else region.capitalize()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["sales"],
        mode="lines",
        name=label,
        line=dict(color=color, width=2.5),
        fill="tozeroy",
        fillcolor=color.replace(")", ", 0.08)").replace("rgb", "rgba") if "rgb" in color else color + "15",
    ))

    fig.add_vline(
        x=pd.Timestamp(PRICE_INCREASE_DATE).timestamp() * 1000,
        line_width=2,
        line_dash="dash",
        line_color="#fab387",
        annotation_text="Price increase — Jan 15 2021",
        annotation_position="top right",
        annotation_font_size=12,
        annotation_font_color="#fab387",
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        plot_bgcolor="#181825",
        paper_bgcolor="#1e1e2e",
        font=dict(color="#cdd6f4", family="Inter, sans-serif", size=13),
        xaxis=dict(gridcolor="#313244", linecolor="#45475a", zeroline=False),
        yaxis=dict(gridcolor="#313244", linecolor="#45475a", zeroline=False),
        legend=dict(bgcolor="#313244", bordercolor="#45475a", borderwidth=1),
        margin=dict(l=60, r=40, t=24, b=60),
        hovermode="x unified",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
