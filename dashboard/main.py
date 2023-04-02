from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from data import config
from data import queries

class ElasticsearchClient:
    def __init__(self):
        self.client = Elasticsearch(hosts=[config.ELASTICSEARCH_HOST])

    def search(self, index, body):
        return self.client.search(index=index, body=body)

class DataProcessor:
    def __init__(self, data):
        self.df = self.clean_data(data)
        self.layout = go.Layout(title='My Home Network Traffic Dashboard')
        self.figures = self.create_visualizations()

    def clean_data(self, data):
        df = pd.json_normalize(data)
        df = df[['@timestamp', 'source.ip', 'source.port', 'destination.ip', 'destination.port', 'event.duration', 'event.action']]
        df['@timestamp'] = pd.to_datetime(df['@timestamp'], utc=True)
        df['event.duration'] = pd.to_timedelta(df['event.duration'])
        df['event.duration_ms'] = df['event.duration'] / pd.Timedelta(milliseconds=1)
        df['hour'] = df['@timestamp'].dt.hour
        df['day'] = df['@timestamp'].dt.date
        df['protocol'] = np.where(df['destination.port'] == 80, 'HTTP', 'HTTPS')
        return df

    def create_visualizations(self):
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=self.df['@timestamp'], y=self.df['event.duration_ms'], mode='markers', name='Response Time'))

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=self.df['day'], y=self.df['event.duration_ms'], name='Response Time'))

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=self.df['hour'], y=self.df['event.duration_ms'], name='Response Time'))

        fig4 = go.Figure()
        fig4.add_trace(go.Pie(values=self.df['protocol'].value_counts(), labels=self.df['protocol'].unique(), name='Protocol'))

        figs = [fig1, fig2, fig3, fig4]

        for fig in figs:
            fig.update_layout(self.layout)

        return figs


class Dashboard:
    def __init__(self):
        self.es_client = ElasticsearchClient()
        self.data = self.get_data()
        self.data_processor = DataProcessor(self.data)

    def get_data(self):
        data = []
        for index in range(config.DAYS_TO_QUERY):
            res = self.es_client.search(index='network-traffic-*', body=queries.traffic_query(index))
            data += res['hits']['hits']
        return data

    def display_visualizations(self):
        for fig in self.data_processor.figures:
            fig.show()

dashboard = Dashboard()
dashboard.display_visualizations()