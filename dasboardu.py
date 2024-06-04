import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


combined_df = pd.read_csv('modified_data.csv') # change PATH here

combined_df['date'] = pd.to_datetime(combined_df['date'])
combined_df = combined_df.drop(['station_name', 'station_id'], axis=1)

test_df = combined_df[['date', 'RR', 'RH_avg']]

# Explanation dictionary for each column
explanations = {
    'RR': "RR merupakan curah hujan dalam satuan mm. Dari grafik diatas bisa terlihat bahwa terdapat pola pada tiap akhir dan awal tahun dimana curah hujan tertinggi ditemukan.",
    'RH_avg': "RH_avg merupakan kelembapan rata dalam satuan persentase. Dari grafik diatas bisa terlihat bahwa terdapat pola pada tiap akhir dan awal tahun dimana kelembapan rata-rata membentuk gelombang."
}

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard"),

    html.H2("Time Series Plot"),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col}
                 for col in test_df.columns if col != 'date'],
        value='RR'
    ),
    dcc.Graph(id='time-series-plot'),
    html.Div(id='explanation-div')
])


@app.callback(
    [Output('time-series-plot', 'figure'),
     Output('explanation-div', 'children')],
    Input('column-dropdown', 'value')
)
def update_line_chart(column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=test_df['date'], y=test_df[column], mode='lines', name=column))
    fig.update_layout(
        title=f'Time Series of {column}', xaxis_title='Date', yaxis_title=column)

    explanation = explanations.get(column, "No explanation available.")
    return fig, dcc.Markdown(explanation)


if __name__ == '__main__':
    app.run_server(debug=True)
