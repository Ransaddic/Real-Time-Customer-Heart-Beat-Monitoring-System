# Import necessary libraries
import logging
from kafka import KafkaProducer
import json
import time
import random
from faker import Faker
from datetime import datetime



# Setup logging
logging.basicConfig(
    filename='logs/producer.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Faker and Kafka producer
fake = Faker()

try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    logging.info("Kafka Producer connected successfully.")
except Exception as e:
    logging.error(f"Kafka Producer connection failed: {e}")
    raise

# Simulate 5 unique customer IDs
CUSTOMER_IDS = [fake.uuid4() for _ in range(5)]

def generate_heartbeat():
    heart_rate = random.randint(60, 100)


    return {
        "customer_id": random.choice(CUSTOMER_IDS),
        "timestamp": datetime.now().isoformat(),
        "heart_rate": heart_rate
    }

def send_heartbeat_data():
    while True:
        data = generate_heartbeat()
        try:
            producer.send('heartbeat', value=data)
            logging.info(f"Produced: {data}")
            print(f"[Produced] {data}")  # Optional: minimal console feedback
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        logging.info("Heartbeat Producer started.")
        send_heartbeat_data()
    except KeyboardInterrupt:
        logging.info("Heartbeat Producer stopped by user.")
    finally:
        producer.close()
        logging.info("Kafka Producer connection closed.")
