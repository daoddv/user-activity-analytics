import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd

from datetime import date, datetime
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


# ------------------------------------------------------------------------------
# Import data
df = pd.read_csv('./user_activity_clean.csv')

df.index = pd.to_datetime(df['date_validate'])
# print(df)

# print(df.user_group.unique())

def make_dict_radio_item(user_group):
    res = [dict({
        "label": "all",
        "value": "all"
    })]
    
    for u in user_group:
        res.append(dict({
            "label": u,
            "value": u
        }))
        
    return res


user_group = df.user_group.unique()
opts = make_dict_radio_item(user_group)

email_individual = df.email.unique()
opts_email = make_dict_radio_item(email_individual)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    
    html.H3('USER ACTIVITY ANALYSIS (OVERVIEW)'),
    html.Div(className="row",
             children=[
                html.Div(className='three columns div-user-controls',children=[
                        html.H5('User group'),
                        dcc.RadioItems(
                            id= "group_radio",
                            options=opts,
                            value= opts[0]["value"]
                        ),
                        html.H5('User email'),
                        dcc.Dropdown(
                            id="email_dropdown",
                            multi = False,
                            options=opts_email,
                            value = opts[0].get("value", "all")
                        ),
                        html.H5('Period of time'),
                        dcc.DatePickerRange(
                            id='date_input',
                            min_date_allowed=datetime(2020, 1, 1),
                            max_date_allowed=datetime.now(),
                            start_date= date(2020,1,1),
                            end_date= datetime.now(),
                            display_format='DD-MM-YYYY',
                            end_date_placeholder_text="Return"
                        )
                     ]),
                html.Div(className='nine columns div-for-charts bg-grey', children=[
                    dcc.Graph(
                            id='user_activity'
                        )
                ])
             ]
            )
    
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='user_activity', component_property='figure'),
    [Input(component_id='date_input', component_property='start_date'),
     Input(component_id='date_input', component_property='end_date'),
     Input(component_id='group_radio', component_property='value'),
     Input(component_id='email_dropdown', component_property='value')
     ]
    )
def handle_date_picker(start_date, end_date, group_value, email_value):
    print("Start date: {}, End date: {}".format(start_date,end_date))    
    df_new = df.sort_index().loc[start_date:end_date]
    
    user_group_filter = []
    if group_value != 'all':
        user_group_filter = [group_value]
        df_new = df_new[df_new["user_group"].isin(user_group_filter)]
    
    if email_value != 'all':
        email_filter = [email_value]
        df_new = df_new[df_new["email"].isin(email_filter)]

    if df_new.empty:
        
        return dash.no_update
            
    fig = px.scatter(df_new, x="date_validate", y="time_validate", color='user_activity', hover_name="email", hover_data=["user_activity", "user_group", "date_validate", "time_validate"]) #, width=1000, height=500

    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)
#host = '0.0.0.0', port = 8090,   