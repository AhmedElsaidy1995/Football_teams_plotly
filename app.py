import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output, State
from dash.html.Legend import Legend
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


import pandas as pd
pio.templates.default = "plotly_dark"
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "plotly_dark")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_layout(paper_bgcolor="#212529")
    fig.update_layout(plot_bgcolor="#212529")

    return fig
df = pd.read_csv(r'D:\ITI\Phase2\DataVisualization\Project\understat.com.csv')
app=dash.Dash(__name__, external_stylesheets =['https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/css/bootstrap.min.css'],external_scripts=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/js/bootstrap.bundle.min.js"])
app.layout=html.Div([
                        html.Div(children=[
                                    html.H1('Football Teams Analysis in Past Seasons', style={'textAlign':'center'}),
                                    html.P('Using Expected goals (xG) performance metric to evaluate football team and player performance', style={'textAlign':'center'}),
                        ], className="container-fluid p-4 bg-dark text-white text-center"),
                        html.Div(children=[
                            html.Div(children=[
                                html.Div(children=[    
                                    dcc.Dropdown(
                                        id='league-dropdown',
                                        options=[
                                            {'label': 'Premier League', 'value': 'EPL'},
                                            {'label': 'La Liga', 'value': 'La_liga'},
                                            {'label': 'Serie A', 'value': 'Serie_A'},
                                            {'label': 'Bundesliga', 'value': 'Bundesliga'},
                                            {'label': 'Ligue 1', 'value': 'Ligue_1'},
                                            {'label': 'Russian Pro League', 'value': 'RFPL'},
                                        ],
                                            placeholder="Select a League",clearable=False)
                                ], className="col-sm-5"),
                                html.Div(children=[ 
                                        dcc.Dropdown(
                                        id='season-dropdown',
                                        options=[
                                            {'label': '2019-20', 'value': 2019},
                                            {'label': '2018-19', 'value': 2018},
                                            {'label': '2017-18', 'value': 2017},
                                            {'label': '2016-17', 'value': 2016},
                                            {'label': '2015-16', 'value': 2015},
                                            {'label': '2014-15', 'value': 2014}
                                        ],
                                            placeholder="Select a season",clearable=False),
                                ], className="col-sm-5"),
                                html.Div(children=[ 
                                        html.Button(id='submit-button-state', n_clicks=0, children='Submit',className="btn btn-dark",style={'width':'100%'})
                                ], className="col-sm-2"),
                            ], className="row",style={'padding':20}),
                            html.Div(id='header',children=[], className="row"),
                            html.Div(id='header-data',children=[], className="row"),
                            html.Div([
                                dcc.Graph(id='graph1', figure=blank_fig(), className="col-sm-6 shadow-lg p-3 mb-5 bg-dark "),
                                dcc.Graph(id='graph2', figure=blank_fig(), className="col-sm-6 shadow-lg p-3 mb-5 bg-dark "),
                            ], className="row"),
                            html.Div([
                                dcc.Graph(id='graph3', figure=blank_fig(), className="col-sm-6 shadow-lg p-3 mb-5 bg-dark "),
                                dcc.Graph(id='graph4', figure=blank_fig(), className="col-sm-6 shadow-lg p-3 mb-5 bg-dark "),
                            ], className="row")
                        ], className="container mt-4"),

])


@app.callback(
    Output('header','children'),
    Output('header-data','children'),
    Output('graph1','figure'),
    Output('graph2','figure'),
    Output('graph3','figure'),
    Output('graph4','figure'),
    Input('submit-button-state', 'n_clicks'),
    State('league-dropdown','value'),
    State('season-dropdown','value'))
def update_graph(n_clicks,leaguevalue,seasonvalue):
    if leaguevalue!=None and seasonvalue!= None:
        filtered_df=df[(df['league']==leaguevalue) & (df['season']==seasonvalue)]
        filtered_df['xpts_diff'] = filtered_df['xpts_diff']*(-1)

        children1 = [html.Div(id='over', children=[html.H3('Most Over Performers',id='overperformers')],className="col-sm-6"),
                    html.Div(id='under', children=[html.H3('Most Under Performers',id='underperformers')],className="col-sm-6"),]

        over_df=filtered_df[filtered_df['xpts_diff']==filtered_df['xpts_diff'].max()]
        under_df=filtered_df[filtered_df['xpts_diff']==filtered_df['xpts_diff'].min()]
        children2 = [html.Div(children=[html.H4(over_df['team'])],className="col-sm-3"),
                    html.Div(children=[html.H3('+'+ over_df['xpts_diff'].astype(str)+' Points' )],className="col-sm-3",style={'color':'#81c14f'}),
                    html.Div(children=[html.H4(under_df['team'])],className="col-sm-3"),
                    html.Div(children=[html.H3(under_df['xpts_diff'].astype(str)+' Points' )],className="col-sm-3",style={'color':'#F34146'}),]

        fig1 = px.scatter(filtered_df,x="xG", y="scored", color="team",size='position',title ="Team Scoring Efficency",labels=dict(xG="Expected Goals Scored", scored="Goals Scored"))
        fig1.add_trace(go.Scatter(x=[(filtered_df['xG'].min()-5), (filtered_df['xG'].max()+5)],y=[(filtered_df['xG'].min()-5), (filtered_df['xG'].max()+5)],mode="lines",line=go.scatter.Line(color='rgba(200, 200, 200, 0.2)',),showlegend=False))
        fig1.layout.showlegend = False
        fig1.add_annotation(text="High Scoring Efficency",font = { 'color': "#81c14f"},xref="x", yref="y",x=(filtered_df['xG'].min()+5), y=filtered_df['scored'].max(), showarrow=False)
        fig1.add_annotation(text="Low Scoring Efficency",font = { 'color': "#F34146"},xref="x", yref="y",x=(filtered_df['xG'].max()-5), y=filtered_df['scored'].min(), showarrow=False)
        fig1.update_layout(paper_bgcolor="#212529")

        fig2 = px.scatter(filtered_df,x="xGA", y="missed", color="team",size='position',title="Team Conceding Efficency",labels=dict(xGA="Expected Goals Against", missed="Goals Against"))
        fig2.add_trace(go.Scatter(x=[(filtered_df['xGA'].min()-5), (filtered_df['xGA'].max()+5)],y=[(filtered_df['xGA'].min()-5), (filtered_df['xGA'].max()+5)],mode="lines",line=go.scatter.Line(color='rgba(200, 200, 200, 0.2)',),showlegend=False))
        fig2.layout.showlegend = False
        fig2.add_annotation(text="High Conceding Efficency",font = { 'color': "#F34146"},xref="x", yref="y",x=(filtered_df['xGA'].min()+5), y=filtered_df['missed'].max(), showarrow=False)
        fig2.add_annotation(text="Low Conceding Efficency",font = { 'color': "#81c14f"},xref="x", yref="y",x=(filtered_df['xGA'].max()-5), y=filtered_df['missed'].min(), showarrow=False)
        fig2.update_layout(paper_bgcolor="#212529")

        #bar xG vs xGP title="How much Effects Penalties has on each team xG"
        #xpdiff bar
        #deep vs Goals
        #deep_allowed vs conceded goals
        fig3 = px.scatter(filtered_df,x="deep", y="scored", color="team",size='position',title="How Passes completed within 20 yards of goal affect Goals Scored",labels=dict(deep="Passes completed within an estimated 20 yards of goal", scored="Goals Scored"))
        fig3.layout.showlegend = False
        fig3.update_layout(paper_bgcolor="#212529")

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=filtered_df['team'],y=filtered_df['xpts_diff'],name='Expected Points Diffrence',marker_color='rgb(55, 83, 109)',hovertemplate="%{y}%{_xother}"))
        fig4.layout.showlegend = False
        fig4.update_layout(paper_bgcolor="#212529",title="Diffrence between Expected points and points Sorted By Position")

    else:
         fig1=blank_fig()
         fig2=blank_fig()
         fig3=blank_fig()
         fig4=blank_fig()
         children1 = []
         children2 = []

    return children1,children2,fig1,fig2,fig3,fig4

if __name__=='__main__':
    app.run_server(debug=True)

