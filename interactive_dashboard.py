import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
from statsmodels.tsa.holtwinters import ExponentialSmoothing
df = pd.read_excel("C:\\Users\\sonti\\OneDrive\\Desktop\\sales_with_season.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
product_options = ['ALL'] + sorted(df['Product_ID'].unique())
app = Dash(__name__)
app.layout = html.Div([
    html.H1(" Retail Sales Dashboard with Forecasting",
            style={'textAlign': 'center', 'color': "#181716"}),
    html.Div([
        html.Div([
            html.Label(" Select Region:"),
            dcc.Dropdown(
                id='region_filter',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                multi=True, placeholder="Select Region(s)"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label(" Select Season:"),
            dcc.Dropdown(
                id='season_filter',
                options=[{'label': s, 'value': s} for s in sorted(df['Season'].unique())],
                multi=True, placeholder="Select Season(s)"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),

        html.Div([
            html.Label(" Select Product:"),
            dcc.Dropdown(
                id='product_filter',
                options=[{'label': p, 'value': p} for p in product_options],
                multi=True, placeholder="Select Product(s)"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin': '10px'}),
    ]),
    html.Br(),
    html.Div([
        html.Div([dcc.Graph(id='revenue_by_season')],
                 style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='units_by_season')],
                 style={'width': '48%', 'display': 'inline-block'}),
    ]),
    html.Div([
        html.Div([dcc.Graph(id='sales_trend')],
                 style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='discount_pie')],
                 style={'width': '48%', 'display': 'inline-block'}),
    ]),
    html.Div([
        html.Div([dcc.Graph(id='forecast_chart')],
                 style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='seasonal_fluctuations')],
                 style={'width': '48%', 'display': 'inline-block'}),
    ])
])
@app.callback(
    [Output('revenue_by_season', 'figure'),
     Output('units_by_season', 'figure'),
     Output('sales_trend', 'figure'),
     Output('discount_pie', 'figure'),
     Output('forecast_chart', 'figure'),
     Output('seasonal_fluctuations', 'figure')],
    [Input('region_filter', 'value'),
     Input('season_filter', 'value'),
     Input('product_filter', 'value')]
)
def update_dashboard(selected_regions, selected_seasons, selected_products):
    filtered_df = df.copy()
    if selected_products and "ALL" not in selected_products:
        filtered_df = filtered_df[filtered_df['Product_ID'].isin(selected_products)]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_seasons:
        filtered_df = filtered_df[filtered_df['Season'].isin(selected_seasons)]
    fig1 = px.bar(filtered_df, x='Season', y='Revenue', color='Region',
                  title='Revenue by Season and Region', barmode='group')
    fig2 = px.bar(filtered_df, x='Season', y='Units_Sold', color='Region',
                  title='Units Sold by Season and Region', barmode='group')
    fig3 = px.line(filtered_df, x='Date', y='Revenue', color='Region',
                   title='Sales Trend Over Time')
    avg_discount = filtered_df.groupby('Season')['Discount'].mean().reset_index()
    fig4 = px.pie(avg_discount, names='Season', values='Discount',
                  title='Average Discount by Season', hole=0.3)
    forecast_fig = go.Figure()
    try:
        ts = filtered_df.groupby('Date')['Revenue'].sum().sort_index()
        ts = ts.resample('ME').sum().ffill()
        if len(ts) > 4:
            try:
                model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=4)
                fit = model.fit()
            except:
                model = ExponentialSmoothing(ts, trend='add', seasonal=None)
                fit = model.fit()

            forecast = fit.forecast(4)

            forecast_fig.add_trace(go.Scatter(x=ts.index, y=ts.values, mode='lines', name='Actual'))
            forecast_fig.add_trace(go.Scatter(x=forecast.index, y=forecast.values,
                                              mode='lines+markers', name='Forecast'))
        forecast_fig.update_layout(title=" Time-Series Forecast (Next 4 Months)",
                                   xaxis_title="Date", yaxis_title="Revenue")
    except:
        forecast_fig.update_layout(title="Forecast Unavailable")
    seasonal_fig = px.box(filtered_df, x='Season', y='Units_Sold', color='Region',
                          title=' Seasonal Demand Fluctuations')

    return fig1, fig2, fig3, fig4, forecast_fig, seasonal_fig
if __name__== '__main__':
    app.run(debug=True)