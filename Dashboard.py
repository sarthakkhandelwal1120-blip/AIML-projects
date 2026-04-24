import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.graph_objects as go
import pandas as pd

# -------------------- APP SETUP --------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "NEXUS Analytics"

# -------------------- COLORS --------------------
BG = "#0A0C10"
ACCENT = "#F0A500"
TEXT = "#E2E8F0"
SUB = "#8892A4"

# -------------------- DATA --------------------
monthly_df = pd.DataFrame({
    "month": ["Jan","Feb","Mar","Apr","May","Jun"],
    "revenue": [148000,132000,178000,162000,194000,221000],
})

daily_df = pd.DataFrame({
    "day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    "revenue": [12400,14800,11200,16700,19200,22400,17600],
})

# -------------------- CHART --------------------
def make_chart(view):
    df = monthly_df if view == "monthly" else daily_df
    x = "month" if view == "monthly" else "day"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df["revenue"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=3)
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        height=300
    )
    return fig

# -------------------- TABS --------------------
def tab_overview():
    return html.Div([
        html.H3("Overview", style={"color": TEXT}),

        html.Div([
            html.Button("Daily", id="btn-daily", n_clicks=0),
            html.Button("Monthly", id="btn-monthly", n_clicks=0),
        ], style={"marginBottom": "10px"}),

        dcc.Graph(id="revenue-chart", figure=make_chart("monthly"))
    ])

def tab_products():
    return html.Div([
        html.H3("Products Section", style={"color": TEXT})
    ])

def tab_customers():
    return html.Div([
        html.H3("Customers Section", style={"color": TEXT})
    ])

def tab_ml():
    return html.Div([
        html.H3("ML Insights Section", style={"color": TEXT})
    ])

# -------------------- LAYOUT --------------------
app.layout = html.Div([
    html.H2("⚡ NEXUS Analytics", style={"color": TEXT}),

    html.Div([
        html.Button("Overview", id="tab-overview"),
        html.Button("Products", id="tab-products"),
        html.Button("Customers", id="tab-customers"),
        html.Button("ML Insights", id="tab-ml"),
    ], style={"marginBottom": "20px"}),

    html.Div(id="tab-content")
], style={"background": BG, "padding": "20px"})

# -------------------- TAB SWITCH CALLBACK --------------------
@app.callback(
    Output("tab-content", "children"),
    Input("tab-overview", "n_clicks"),
    Input("tab-products", "n_clicks"),
    Input("tab-customers", "n_clicks"),
    Input("tab-ml", "n_clicks"),
)
def switch_tab(ov, pr, cu, ml):
    ctx = callback_context

    if not ctx.triggered:
        return tab_overview()

    tab = ctx.triggered[0]["prop_id"].split(".")[0]

    if tab == "tab-products":
        return tab_products()
    elif tab == "tab-customers":
        return tab_customers()
    elif tab == "tab-ml":
        return tab_ml()

    return tab_overview()

# -------------------- CHART UPDATE CALLBACK --------------------
@app.callback(
    Output("revenue-chart", "figure"),
    Input("btn-daily", "n_clicks"),
    Input("btn-monthly", "n_clicks"),
    prevent_initial_call=True
)
def update_chart(d, m):
    ctx = callback_context

    if not ctx.triggered:
        return make_chart("monthly")

    btn = ctx.triggered[0]["prop_id"].split(".")[0]

    if btn == "btn-daily":
        return make_chart("daily")

    return make_chart("monthly")

# -------------------- RUN --------------------
if __name__ == "__main__":
    print("\nOpen: http://127.0.0.1:8050\n")
    app.run(debug=True)