FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

CMD ["streamlit", "run", "scripts/heartbeat_dashboard.py"]

COPY scripts/wait-for-kafka.sh /app/wait-for-kafka.sh

# Ensure correct line endings and execution rights
RUN apt-get update && apt-get install -y dos2unix \
 && dos2unix /app/wait-for-kafka.sh \
 && chmod +x /app/wait-for-kafka.sh
