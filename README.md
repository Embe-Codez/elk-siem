# SIEM Project using ELK Stack

This project aims to demonstrate how to set up a Security Information and Event Management (SIEM) system using the Elastic Stack (ELK).

![Alt Text](https://www.elastic.co/guide/en/beats/packetbeat/current/images/flows.png)

## Requirements

* Docker
* Docker Compose
* Python 3.x

## Components

This project consists of the following components:

* Elasticsearch - A distributed, RESTful search and analytics engine capable of solving a growing number of use cases.
* Logstash - A data processing pipeline that ingests data from multiple sources, transforms it, and then sends it to a variety of destinations.
* Kibana - An open source analytics and visualization platform designed to work with Elasticsearch.
* Packetbeat - A lightweight network packet analyzer that sends data to Elasticsearch for storage and analysis.

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It allows you to configure and start multiple Docker containers with a single command. In the context of ELK, Docker Compose is used to define and start the three main components of the Elastic Stack (Elasticsearch, Logstash, and Kibana) in a single command. It also allows you to configure the interconnection between the containers and their dependencies, such as specifying the Elasticsearch host in the Kibana configuration. Docker Compose simplifies the setup process of the ELK stack and makes it easier to deploy the system across different environments.

## Installation

To run this project, follow the steps below:

1. Install Docker on your machine.
2. Clone this repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Run docker-compose up -d to start the services in detached mode.
5. Navigate to http://localhost:5601 in your web browser to access Kibana.

## Configuration

The project is pre-configured to use Packetbeat to collect network traffic data and Logstash to process and send it to Elasticsearch for storage and analysis.

    The logstash/pipeline/logstash.conf file contains the Logstash configuration for processing the network traffic data.

```
input {
  pcap {
    interface => "wlp4s0"
    mode => "normal"
  }
}

output {
  elasticsearch {
    hosts => "elasticsearch:9200"
    index => "logstash-home-network-traffic-%{+YYYY.MM.dd}"
  }
}

```

    The above configuration will process network traffic data collected by Packetbeat and send it to Elasticsearch for storage and analysis.

## Python Code

In addition to the ELK stack components, this project also includes Python code to retrieve and process data from Elasticsearch. The config.py file defines the Elasticsearch host and the number of days to query. The queries.py file includes a function that generates a query to retrieve network traffic data for a specific day. The Dashboard class in the main.py file uses the Elasticsearch Python library to retrieve data using the query generated by traffic_query() and processes it using the DataProcessor class. The DataProcessor class cleans and transforms the data into a Pandas DataFrame and creates visualizations using Plotly. Finally, the display_visualizations() method in the Dashboard class shows the generated visualizations.

## Kibana Dashboard Example

The above screenshot shows an example Kibana dashboard for visualizing network traffic data. It includes a map showing the source and destination IP addresses of network traffic, a line chart showing the volume of traffic over time, and a table showing the details of individual network connections.

## Conclusion

This project demonstrates how to set up a SIEM system using the Elastic Stack. It includes pre-configured components for collecting and processing network traffic data, and provides an example Kibana dashboard for visualizing the data. This project can be extended to include additional data sources and visualizations, depending on the specific use case.