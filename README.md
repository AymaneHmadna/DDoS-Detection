# DDoS Detection

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-Structured_Streaming-E25A1C.svg)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Message_Broker-231F20.svg)
![Cassandra](https://img.shields.io/badge/Cassandra-Hot_Path-1287B1.svg)
![Hadoop](https://img.shields.io/badge/Hadoop_HDFS-Cold_Path-FCCC26.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

## Overview
[cite_start]This project implements a robust Big Data pipeline designed to ingest, process, and visualize network traffic in real-time to detect cyberattacks (specifically DDoS)[cite: 5]. [cite_start]Built on a **Lambda Architecture** [cite: 6][cite_start], it captures raw TCP/IP packets at the network interface [cite: 23] [cite_start]and processes them through a high-throughput, fault-tolerant streaming engine[cite: 16].

## Architecture & Tech Stack
[cite_start]Every component was selected to handle specific Big Data constraints (Volume, Velocity, Variety)[cite: 7]:

* [cite_start]**Ingestion (Scapy):** Low-level packet sniffing capturing source IPs, target ports, and metadata[cite: 22, 23].
* [cite_start]**Buffer/Broker (Apache Kafka):** Acts as a high-performance buffer (topic: `network-traffic`) to decouple ingestion from processing, handling potential backpressure and preventing packet loss[cite: 8, 9, 11].
* [cite_start]**Stream Processing (Apache Spark Structured Streaming):** Consumes the Kafka stream, applies detection logic (e.g., volumetric analysis and port 6666 filtering) in micro-batches with in-memory processing and exactly-once semantics[cite: 13, 14, 15, 16].
* [cite_start]**Speed Layer / Hot Path (Apache Cassandra):** A write-heavy NoSQL database storing real-time alerts and metrics for immediate, low-latency dashboard querying[cite: 16].
* [cite_start]**Batch Layer / Cold Path (Hadoop HDFS):** A distributed data lake archiving raw JSON attack logs for future Machine Learning model training[cite: 16, 17, 18].
* [cite_start]**Visualization (Streamlit):** Live monitoring dashboard updating every 2 seconds to reflect system status (Active/Critical)[cite: 28, 66, 73].
* [cite_start]**Infrastructure (Docker Compose):** Fully containerized environment orchestrating Zookeeper, Kafka, Namenode, Datanode, Spark, and Cassandra[cite: 18].

## Project Structure
* [cite_start]`docker-compose.yml`: Infrastructure orchestration and virtual network configuration[cite: 18, 19].
* [cite_start]`real_sniffer.py`: Network interface listener injecting packet data into Kafka[cite: 22, 23].
* [cite_start]`spark_processor.py`: The core engine processing the stream and writing simultaneously to Cassandra and HDFS[cite: 24, 25].
* [cite_start]`attacker.py`: Offensive script simulating a massive UDP flood (DDoS) on port 6666 to test system reactivity[cite: 26].
* [cite_start]`app.py`: Streamlit-based real-time monitoring dashboard[cite: 28].

## Quickstart Guide

**1. Deploy the Infrastructure**
```bash
docker-compose up -d
