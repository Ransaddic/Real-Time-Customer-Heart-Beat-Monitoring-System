# Import necessary libraries
from kafka import KafkaProducer
import json
import time
import random
from faker import Faker
from datetime import datetime

# Initialize Faker and Kafka producer
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Simulate 5 unique customer IDs
CUSTOMER_IDS = [fake.uuid4() for _ in range(5)]

def generate_heartbeat():
    return {
        "customer_id": random.choice(CUSTOMER_IDS),
        "timestamp": datetime.now().isoformat(),
        "heart_rate": random.randint(60, 100)
    }

def send_heartbeat_data():
    while True:
        data = generate_heartbeat()
        producer.send('heartbeat', value=data)
        print(f"[Produced] {data}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        print("Starting Heartbeat Data Producer...")
        send_heartbeat_data()
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        producer.close()
