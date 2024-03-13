from dash import Dash, html, dash_table
from dash import dcc, Input, Output
import pandas as pd
import plotly.express as px

def plot_pH(df, col):
	fig = px.scatter(df, x=col, y='pH', trendline='ols')
	return fig

def plot_category(df, col):
	fig = px.scatter(df, x='Unnamed: 0', y=col, color='target')
	fig.update_xaxes(visible=False, showticklabels=False)
	return fig

df = pd.read_csv('winequality.csv')
cols = df.columns.to_list()[1:]
flag = None

app = Dash(__name__)
app.layout = html.Div([
	dash_table.DataTable(data=df.to_dict('records'), page_size=10),
	dcc.Dropdown(['regression model', 'classification model'], id='model-choice', style={'width': 300}),
	html.Div(id='model-choice-container', style={'height': 30}),
	dcc.Dropdown(cols, id='cols', style={'width': 300}),
	html.Div(id='graph-container')
])

@app.callback(
	Output('model-choice-container', 'children'),
	Input('model-choice', 'value')
)
def update_output(value):
	global flag
	flag = value
	return f'You have selected {value}' if value is not None else []

@app.callback(
	Output('graph-container', 'children'),
	Input('cols', 'value')
)
def upate_output_2(value):
	if value is not None:
		fig = {}
		if flag=='regression model':
			fig = plot_pH(df, value)
		elif flag=='classification model':
			fig = plot_category(df, value)
		else:
			pass
		return [dcc.Graph(figure=fig, style={'width': 900, 'height': 600})]
	else:
		return []

if __name__ == '__main__':
	app.run_server(debug=True)
