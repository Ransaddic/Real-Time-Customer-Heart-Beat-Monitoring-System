# Import the necessary libraries
from kafka import KafkaProducer
import json
import time
import random
from faker import Faker
from datetime import datetime

fake= Faker()

# Intitialize the Kafka producer
producer= KafkaProducer(
    bootstrap_servers= ['localhost:9092'],
    value_serializer= lambda x: json.dumps(x).encode('utf-8')
)

# Simulate data for five customers
ids= [fake.uuid4() for _ in range(5)]

def generate_heart_beat():
    # Generate a random heart beat value between 60 and 100
    return {
        "ids":random.choice(ids),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "heart_beat": random.randint(60, 100) # Heart beat per minute
    }

while True:
    # Generate a heart beat value
    heart_beat= generate_heart_beat()
    # Send the heart beat value to the Kafka topic
    producer.send('heart_beat', value= heart_beat)
    print(f"Produced: {heart_beat}")
    # Sleep for 1 second before generating the next value
    time.sleep(1)