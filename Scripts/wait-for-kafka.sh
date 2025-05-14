#!/bin/bash

KAFKA_HOST=${KAFKA_BOOTSTRAP_SERVERS:-kafka:9092}
echo "Waiting for Kafka at $KAFKA_HOST..."

until echo > /dev/tcp/$(echo $KAFKA_HOST | cut -d: -f1)/$(echo $KAFKA_HOST | cut -d: -f2); do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 3
done

echo "Kafka is up!"
exec "$@"
