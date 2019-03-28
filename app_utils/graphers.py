import plotly.graph_objs as go

class PlotlyGrapher():
    '''Contains all the graphing functions'''

    def __init__(self):
        self.placeholder_data = {
            'label': ['a', 'b'],
            'value': [1,2],
            'name': 'var1'
        }

    def _empty_graph(func):
        placeholder_data = [{
            'label': ['a', 'b'],
            'value': [1,2],
            'name': 'var1'
        }]

        def inner(self, data=None):
            if not data:
                # print('Detected empty function call')
                return func(self, data=placeholder_data)
            return func(self, data)
        return inner

    @_empty_graph
    def time_line(self, data, mode='lines+markers'):
        traces = [go.Scatter(
            x=t['label'],
            y=t['value'],
            name=t['name'],
            mode=mode,
        ) for t in data]

        layout = go.Layout(
            margin=dict(l=40, r=25, b=40, t=0, pad=4)
        )
        return {'data': traces, 'layout': layout}

    @_empty_graph
    def pie_chart(self, data):
        traces = [go.Pie(labels=s['label'], values=s['value']) for s in data]
        layout = go.Layout(
            margin=dict(l=0, r=0, b=0, t=4, pad=8),
            legend=dict(orientation="h"),
        )

        return {'data': traces, 'layout': layout}

    @_empty_graph
    def bar_chart(self, data, barmode='stack'):

        traces = [go.Bar(
            x=b['label'], y=b['value'], name=b['name']
        ) for b in data]

        layout = go.Layout(
            barmode=barmode,
            margin=dict(l=40, r=25, b=40, t=0, pad=4),
        )

        return {'data': traces, 'layout': layout}

    @_empty_graph
    def histogram(self, data, barmode='overlay'):
        traces = [go.Histogram(x=h['values'], opacity=0.75) for h in data]   
        layout = go.Layout(
            barmode=barmode,
            margin=dict(l=40, r=25, b=40, t=0, pad=4),
        )
        return {'data': traces, 'layout': layout}


    def sankey_diag(self, flows):
        # for k, f in flows.items()   :
        #     print(f.unique())
        #     print(k, len(f))
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color='black',
                width=0.5
            ),
            
            label=flows['label'],
            # color=["blue", "blue", "blue", "blue", "blue", "blue"]
        )
        link=dict(
            source=flows['source'],
            target=flows['target'],
            value=flows['value'],
            
        )    
        trace = go.Sankey(node=node, link=link)
        
        layout = go.Layout(
            margin=dict(l=40, r=25, b=40, t=40, pad=4),
        )
        
        return {'data': [trace], 'layout': layout}
