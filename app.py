#!/usr/bin/python3
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_ag_grid as dag
import plotly.express as px
import json
import pandas as pd
from pathlib import Path

storage="data"
courses=json.load(open("courselist.json","r"))
departments=list(courses.keys())
program_outcomes=json.load(open("pos.json","r"))
sdep,scourse=None,None
app = Dash()
dfex = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/wind_dataset.csv")
coldefs=[{"field":x} for x in list(dfex.columns)]
#print("COLDEFS:",coldefs)
app.layout = html.Div([
    html.H1(children='IEU İşletme AQAS', style={'textAlign':'center'}),
    dcc.Input(
            id="passwd",
            type="password",
            placeholder="Enter password here",
        ),
    html.H2(children='Activity to learning outcomes (A-PO) matrix', style={'textAlign':'center'}),
    dcc.Dropdown(dict((d,d) for d in courses.keys()), 'dba', id='dropdown-departments'),
    dcc.Dropdown(courses["dba"],courses["dba"][0],id='dropdown-courses'),
    html.Ol(id="los",children="Learning outcomes: ..."),
    dag.AgGrid(
        id="alo-grid",
        defaultColDef={"editable": True},
        #cellClassRules = {"bg-danger": "params.data.sickDays >= 5"}
        #rowData=dfex.to_dict("records"),#pd.read_csv(Path(storage)/"a-to-lo"/"dba"/"BUS 210.csv").to_dict("records"),
        #columnDefs=coldefs,
        #columnSize="sizeToFit",
        #dashGridOptions={
        # "rowDragManaged": True,
        # "rowDragEntireRow": True
        #    },
        ),
    html.Div(id="alo-output"),
    html.H2(children="Learning outcomes to Program outcomes (LO-PO) matrix"),
    html.Ol(id="pos",children="Program outcomes: ..."),
    dag.AgGrid(
        id="lopo-grid",
        defaultColDef={"editable": True},
    ),
    html.Div(id="lopo-output"),
    html.H2(children="Bu LO-PO matrix her PO ne kadar destek veriyor?"),
    html.P("(Course program outcomes matrix burada otomatik oluşacak ama henüz formülünü düşünmedik)"),
    html.H2(children="Grade list"),
    html.P("Dosya yüklenecek ve görüntülenecek"),
    html.H2(children="Bu grade'ler ve matrisler her LO ne kadar sağladı?"),
    html.P("Burada raporlanacak ama henüz formülünü düşünmedik"),
    ]
)
@callback(
    Output('dropdown-courses', 'options'),
    Input('dropdown-departments', 'value')
)
def update_courselist(department):
    opts = [{'label':opt, 'value':opt} for opt in courses[department]]
    #print(department,opts)
    return opts

@callback(
    Output("alo-grid", "rowData"),
    Output("alo-grid", "columnDefs"),
    Input('dropdown-departments', 'value'),
    Input("dropdown-courses", "value"),
    prevent_initial_call=True,
)
def update_alogrid(department,course):
    print("Loading alo grid for",department,"---",course)
    fname=course+".csv"
    df=pd.read_csv(Path(storage)/"a-to-lo"/department/fname)
    coldefs=[{"field":x,"editable":False} for x in list(df.columns)[:3]] +         [{"field":x,'cellStyle': {
            "function": "params.value && {'backgroundColor': 'rgb(255,0,0,0.2)'}"
        }
        } for x in list(df.columns)[3:]]
    global sdep
    global scourse
    sdep,scourse=department,course
    print("UPDATED DEPT-COURSE",sdep,"-",scourse)
    return df.to_dict("records"),coldefs

@callback(
    Output("lopo-grid", "rowData"),
    Output("lopo-grid", "columnDefs"),
    Input('dropdown-departments', 'value'),
    Input("dropdown-courses", "value"),
    prevent_initial_call=True,
)
def update_lopogrid(department,course):
    print("Loading lopo grid for",department,"---",course)
    fname=course+".csv"
    df=pd.read_csv(Path(storage)/"lo-to-po"/department/fname)
    coldefs=[{"field":x,"editable":False} for x in list(df.columns)[:1]] +         [{"field":x,'cellStyle': {
            "function": "params.value && {'backgroundColor': 'rgb(255,0,0,0.2)'}"
        }
        } for x in list(df.columns)[1:]]
    global sdep
    global scourse
    sdep,scourse=department,course
    return df.to_dict("records"),coldefs

@callback(
    Output("los", "children"),
    Input('dropdown-departments', 'value'),
    Input("dropdown-courses", "value"),
    prevent_initial_call=True,
)
def update_courselos(department,course):
    fname=course+".json"
    los=json.load(open(Path(storage)/"lo-list"/department/fname,"r"))
    return [html.H3(children="Learning outcomes list")]+[html.Li(children=x) for x in los]

@callback(
    Output("pos", "children"),
    Input('dropdown-departments', 'value'),
    Input("dropdown-courses", "value"),
    prevent_initial_call=True,
)
def update_coursepos(department,course):
    pos=program_outcomes[department]
    return [html.H3(children="Program outcomes list")]+[html.Li(children=x) for x in pos]


@callback(
    Output("alo-output", "children"), 
    Input("alo-grid", "cellValueChanged"),
    Input('passwd', 'value'),
    #Input("dropdown-courses", "value"),
    State("alo-grid", "rowData"),

    prevent_initial_call=True,
)
def save_alo(cell_changed,passwd,row_data):
    #print("ROW_DATA",row_data)
    if passwd!="111":return "INVALID PASSWORD"
    df=pd.DataFrame(row_data)
    print("LENDF",len(df))
    if not cell_changed:return "PASSWORD OK"
    if len(df)==0:return ""
    print("SAVING ALO",sdep,scourse)
    fname=scourse+".csv"
    df.to_csv(Path(storage)/"a-to-lo"/sdep/fname,index=False)
    return f"UPDATED: {cell_changed}"

@callback(
    Output("lopo-output", "children"), 
    Input("lopo-grid", "cellValueChanged"),
    Input('passwd', 'value'),
    State("lopo-grid", "rowData"),
    prevent_initial_call=True,
)
def save_lopo(cell_changed,passwd,row_data):
    #print("ROW_DATA",row_data)
    if passwd!="111":return "INVALID PASSWORD"
    df=pd.DataFrame(row_data)
    print("LENDF",len(df))
    if not cell_changed:return "PASSWORD OK"
    if len(df)==0:return ""
    print("SAVING LOPO",sdep,scourse)
    fname=scourse+".csv"
    df.to_csv(Path(storage)/"lo-to-po"/sdep/fname,index=False)
    return f"UPDATED: {cell_changed}"

server = app.server
if __name__ == "__main__":
    app.run(debug=True)