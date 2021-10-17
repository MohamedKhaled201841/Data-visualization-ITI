import dash
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output,State
import pandas as pd

df = px.data.gapminder()

fig = px.scatter(df, x='gdpPercap', y='lifeExp', animation_frame='year', hover_name='country')
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div(children=[
    dcc.Dropdown(
        id="My_dropdown",
        options = [{'label': f"{i}", 'value': i} for i in df['continent'].unique()],

        multi=True
    ),
    dcc.Graph(id="My_gragh1"),
    dcc.Graph(id="My_gragh2"),
    html.Div(id="My_Div"),
    dcc.Slider(
                id='my-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value = df['year'].min(),
                step = None,
        marks = {str(years): str(years) for years in df['year'].unique()}
    ),
    html. Button(id='submit-button-state', children='Submit', n_clicks=0)

])
@app.callback(
    Output('My_gragh1', 'figure'),
    Output('My_gragh2', 'figure'),
    State('my-slider', 'value'),
    State("My_dropdown","value"),
    Input('submit-button-state',"n_clicks"))
def update_graph(slidervalue,dropdownvalue,n_clicks):
        filtered_df=df[(df.year==slidervalue) & (df.continent.isin(dropdownvalue))]
        fig1=px.scatter(filtered_df,x="gdpPercap", y="lifeExp", size="pop", color="continent",template="plotly_dark")
        fig2 =px.choropleth(filtered_df,color="lifeExp",locations="iso_alpha",hover_name="country",template="plotly_dark")
        return fig1,fig2
app.run_server()