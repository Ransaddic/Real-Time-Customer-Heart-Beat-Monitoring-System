
# Real-Time Customer Heart Beat Monitoring System

This project simulates and monitors customer heartbeats in real-time using Kafka, PostgreSQL, and Streamlit.

## 📦 Project Structure

```
├── docker-compose.yml
├── dashboard/
│   ├── Dockerfile
├── producer/
│   ├── Dockerfile
├── consumer/
│   ├── Dockerfile
├── scripts/
│   ├── heartbeat_producer.py
│   ├── heartbeat_consumer.py
│   ├── heartbeat_dashboard.py
│   ├── wait-for-kafka.sh
├── requirements.txt
```

## 🚀 Features

- Simulates synthetic heartbeat data using a Kafka producer.
- Consumes and stores heartbeat data into PostgreSQL.
- Visualizes real-time data via a Streamlit dashboard.

## 🛠️ Tech Stack

- **Python 3.10**
- **Apache Kafka**
- **PostgreSQL**
- **Streamlit**
- **Docker & Docker Compose**

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-repo/Real-Time-Customer-Heart-Beat-Monitoring-System.git
cd Real-Time-Customer-Heart-Beat-Monitoring-System
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

### 3. Access the Dashboard

Go to [http://localhost:8501](http://localhost:8501) in your browser.

## 🧪 Test the Kafka Connection

```bash
docker exec -it heartbeat_producer ping kafka
```

## 📝 Notes

- Make sure Docker is running.
- PostgreSQL is accessible as `db` inside the Docker network.
- The `wait-for-kafka.sh` script ensures services wait for Kafka to be ready.

## 🧯 Troubleshooting

- `NoBrokersAvailable`: Ensure Kafka and Zookeeper are up before producer/consumer.
- `psycopg2.OperationalError`: Ensure `DB_HOST` matches service name in docker-compose (use `db`).

---

© 2025 Real-Time Heart Beat Monitoring System
