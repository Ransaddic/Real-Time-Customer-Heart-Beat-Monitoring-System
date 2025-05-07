# Import the necessary libraries

from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

# PostgreSQL connection
conn = psycopg2.connect(
    dbname='heart_monitor',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5433'
)
cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    'heartbeat',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='heartbeat_group'
)

def is_valid(data):
    return 40 <= data['heartbeat'] <= 180  # basic anomaly filter

for message in consumer:
    data = message.value
    print("Received:", data)

    if is_valid(data):
        try:
            cursor.execute("""
                INSERT INTO heartbeat_data (customer_id, timestamp, heart_rate)
                VALUES (%s, %s, %s)
            """, (data['ids'], datetime.fromisoformat(data['timestamp']), data['heartbeat']))
            conn.commit()
        except Exception as e:
            print("DB Insert Error:", e)
    else:
        print("Invalid data skipped:", data)

