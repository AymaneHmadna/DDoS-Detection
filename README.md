# DDoS Detection

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-Structured_Streaming-E25A1C.svg)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Message_Broker-231F20.svg)
![Cassandra](https://img.shields.io/badge/Cassandra-Hot_Path-1287B1.svg)
![Hadoop](https://img.shields.io/badge/Hadoop_HDFS-Cold_Path-FCCC26.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

## Overview
This project implements a robust Big Data pipeline designed to ingest, process, and visualize network traffic in real-time to detect cyberattacks (specifically DDoS). Built on a **Lambda Architecture**, it captures raw TCP/IP packets at the network interface and processes them through a high-throughput, fault-tolerant streaming engine.

## Architecture & Tech Stack
Every component was selected to handle specific Big Data constraints (Volume, Velocity, Variety):

* **Ingestion (Scapy):** Low-level packet sniffing capturing source IPs, target ports, and metadata.
* **Buffer/Broker (Apache Kafka):** Acts as a high-performance buffer (topic: `network-traffic`) to decouple ingestion from processing, handling potential backpressure and preventing packet loss.
* **Stream Processing (Apache Spark Structured Streaming):** Consumes the Kafka stream, applies detection logic (e.g., volumetric analysis and port 6666 filtering) in micro-batches with in-memory processing and exactly-once semantics[cite: 13, 14, 15, 16].
* **Speed Layer / Hot Path (Apache Cassandra):** A write-heavy NoSQL database storing real-time alerts and metrics for immediate, low-latency dashboard querying.
* **Batch Layer / Cold Path (Hadoop HDFS):** A distributed data lake archiving raw JSON attack logs for future Machine Learning model training.
* **Visualization (Streamlit):** Live monitoring dashboard updating every 2 seconds to reflect system status (Active/Critical).
* **Infrastructure (Docker Compose):** Fully containerized environment orchestrating Zookeeper, Kafka, Namenode, Datanode, Spark, and Cassandra.

## Project Structure
* `docker-compose.yml`: Infrastructure orchestration and virtual network configuration.
* `real_sniffer.py`: Network interface listener injecting packet data into Kafka.
* `spark_processor.py`: The core engine processing the stream and writing simultaneously to Cassandra and HDFS.
* `attacker.py`: Offensive script simulating a massive UDP flood (DDoS) on port 6666 to test system reactivity.
* `app.py`: Streamlit-based real-time monitoring dashboard.

## Quickstart Guide

**1.Deploy the Infrastructure**

docker-compose up -d

Wait for all containers (Kafka, Hadoop, Spark, Cassandra) to reach the "Started" state.

**2.Initialize the Kafka Topic**

docker exec -it kafka kafka-topics --create --topic network-traffic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

**3.Setup Cassandra Schema**

docker exec -it cassandra_interne cqlsh -e "CREATE KEYSPACE IF NOT EXISTS projet_logs WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}; CREATE TABLE IF NOT EXISTS projet_logs.resultats_ips (ip text PRIMARY KEY, count int, last_seen timestamp, prediction text);"

**4.Start the Pipeline Components**

Open separate terminals for each process:

*Start the Spark Stream Processor*

docker exec -it mon_dashboard_container python spark_processor.py

*Start the Network Sniffer*

python real_sniffer.py

*Start the Streamlit Dashboard*

docker exec -it mon_dashboard_container streamlit run app.py

Access the dashboard at http://localhost:8501

**5.Simulate an Attack**

python attacker.py
