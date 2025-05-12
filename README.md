
# 💓 Real-Time Customer Heart Beat Monitoring System

This project simulates and monitors real-time heart rate data for multiple customers. It includes a synthetic data generator, real-time Kafka streaming with Python, PostgreSQL for storage (via Docker), and a Streamlit dashboard for visualization.

---

## 📁 Project Structure

```
Real-Time-Customer-Heart-Beat-Monitoring-System/
│
├── logs/
│   ├── consumer.log                # Log file for Kafka consumer events
│   └── producer.log                # Log file for Kafka producer events
│
├── Scripts/
│   ├── heartbeat_consumer.py      # Consumes data from Kafka, validates, and inserts into PostgreSQL
│   ├── heartbeat_producer.py      # Generates synthetic heartbeat data and sends to Kafka
│   ├── heartbeat_dashboard.py     # Streamlit dashboard to visualize heartbeat data
│   ├── docker-compose.yml         # Docker Compose for PostgreSQL container
│   └── postgres_setup.sql         # SQL script to set up heartbeat_data table in PostgreSQL
|
|__ Readme.md                      # This file
|
|__ requirements.txt               # contains all libraries to be installed
```

---

## ⚙️ Components

* Kafka Producer: Simulates heart rate data for 5 customers and sends it to a Kafka topic.

* Kafka Consumer: Reads data from Kafka, validates it, and stores it in PostgreSQL.

* PostgreSQL: Stores the validated heart rate data (Dockerized).

* Streamlit Dashboard: Displays real-time plots and summary stats for each customer.

## 🐳 Docker Setup (PostgreSQL Only)

### 1. Start PostgreSQL Container

Run the PostgreSQL container using Docker Compose:

``docker-compose up -d
``

### 2. Apply SQL Setup

### After the container is running, set up the database:

``docker exec -i <container_id> psql -U postgres -d heart_monitor < Scripts/postgres_setup.sql
``

## ▶️ How to Run

### Start Kafka & Zookeeper (must be pre-installed)

``bin/zookeeper-server-start.sh config/zookeeper.properties
``

``bin/kafka-server-start.sh config/server.properties
``
### 1. Producer

``python Scripts/heartbeat_producer.py
``

### 2. Consumer

``python Scripts/heartbeat_consumer.py
``

### 3. Dashboard

``streamlit run Scripts/heartbeat_dashboard.py
``

## 📊 Dashboard Features

Real-time updates every 5 seconds

Customer selection

Summary metrics: Mean, Min, Max BPM

Line plot of heart rate trends

Tabular view of the latest 100 records

## 🛠️ Requirements

``pip install -r requirements.txt
``
