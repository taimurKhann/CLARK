import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from mongodb import MongoDB

mongo_instance = MongoDB("mongodb://127.0.0.1/", 27017)
mongo_client = mongo_instance.connect()
db = mongo_instance.get_db(mongo_client, "mydb")

app =dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H4('Order Fulfilment Duration Report'),
        dcc.Graph(id = 'live-graph-order-fulfilment', animate = False),
        dcc.Interval(
            id = 'graph-update',
            interval = 5000
        )
    ]),
    html.Div([
        html.H4('Open Orders Report'),
        dcc.Graph(id = 'live-graph-open-orders', animate = False),
        dcc.Interval(
            id = 'graph-update2',
            interval = 5000
        )
    ]),
    html.Div([
        html.H4('Probability of a cancelled order depending on the age'),
        dcc.Graph(id = 'live-graph-cancelled_orders_by_age', animate = False),
        dcc.Interval(
            id = 'graph-update3',
            interval = 5000
        )
    ])
])

@app.callback(
    Output('live-graph-order-fulfilment', 'figure'),
    events = [Event('graph-update', 'interval')]
)
def update_graph():
    duration, order_counts = mongo_instance.get_order_fulfilment_records(db)

    data = go.Bar(
            x=duration,
            y=order_counts
            )

    return {
        'data': [data]
    }

@app.callback(
    Output('live-graph-open-orders', 'figure'),
    events = [Event('graph-update2', 'interval')]
)
def update_graph():
    X, Y = mongo_instance.get_open_orders_record(db)

    data = go.Bar(
            x = X,
            y = Y,
            orientation = 'h'
            )

    return {
        'data': [data]
    }

@app.callback(
    Output('live-graph-cancelled_orders_by_age', 'figure'),
    events = [Event('graph-update3', 'interval')]
)
def update_graph():
    customer_age, cancellation_probability = mongo_instance.get_cancelled_orders_by_age_report(db)

    data = go.Pie(
            labels=customer_age,
            values=cancellation_probability
            )

    return {
        'data': [data]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
