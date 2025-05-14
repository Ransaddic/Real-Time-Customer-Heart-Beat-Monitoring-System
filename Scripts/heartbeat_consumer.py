import logging
from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Now access them
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
# Setup logging
logging.basicConfig(
    filename='logs/consumer.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname= dbname,
            user= user,
            password=password,
            host=host,
            port= port
        )
        logging.info("Connected to PostgreSQL database.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

# Validate heart rate range
def is_valid(data):
    return 40 <= data.get('heart_rate', 0) <= 180

# Insert data into the database
def insert_heartbeat(cursor, data):
    cursor.execute("""
        INSERT INTO heartbeat_data (customer_id, timestamp, heart_rate)
        VALUES (%s, %s, %s)
    """, (
        data['customer_id'],
        datetime.fromisoformat(data['timestamp']),
        data['heart_rate']
    ))
    logging.info(f"Inserted data: {data}")

def main():
    logging.info("Starting Kafka Consumer...")

    conn = connect_to_db()
    cursor = conn.cursor()

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    consumer = KafkaConsumer(
        'heartbeat',
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='heartbeat_group'
    )

    try:
        for message in consumer:
            data = message.value
            logging.info(f"Received: {data}")

            if is_valid(data):
                try:
                    insert_heartbeat(cursor, data)
                    conn.commit()
                except Exception as db_err:
                    logging.error(f"DB Insert Error: {db_err}")
            else:
                logging.warning(f"Invalid data skipped: {data}")
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user.")
    finally:
        cursor.close()
        conn.close()
        consumer.close()
        logging.info("Resources cleaned up and consumer shut down.")

if __name__ == "__main__":
    main()
