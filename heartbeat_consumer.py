# Import the necessary libraries
from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

# PostgreSQL connection setup
def connect_to_db():
    return psycopg2.connect(
        dbname='heart_monitor',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5433'
    )

# Validate heart rate range
def is_valid(data):
    return 40 <= data.get('heart_rate', 0) <= 180

def insert_heartbeat(cursor, data):
    cursor.execute("""
        INSERT INTO heartbeat_data (customer_id, timestamp, heart_rate)
        VALUES (%s, %s, %s)
    """, (
        data['customer_id'],
        datetime.fromisoformat(data['timestamp']),
        data['heart_rate']
    ))

def main():
    print("Starting Kafka Consumer...")

    conn = connect_to_db()
    cursor = conn.cursor()

    consumer = KafkaConsumer(
        'heartbeat',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='heartbeat_group'
    )

    try:
        for message in consumer:
            data = message.value
            print("Received:", data)

            if is_valid(data):
                try:
                    insert_heartbeat(cursor, data)
                    conn.commit()
                except Exception as db_err:
                    print("DB Insert Error:", db_err)
            else:
                print("Invalid data skipped:", data)
    except KeyboardInterrupt:
        print("Consumer stopped by user.")
    finally:
        cursor.close()
        conn.close()
        consumer.close()
        print("Resources cleaned up.")

if __name__ == "__main__":
    main()
