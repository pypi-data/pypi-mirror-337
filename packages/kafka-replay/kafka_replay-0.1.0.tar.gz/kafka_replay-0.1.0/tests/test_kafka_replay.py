import time
from datetime import datetime
from confluent_kafka import Producer

BROKER = "localhost:9092"
TOPIC = "test_kafka_replay"

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()} at time {datetime.now()}")

def produce_messages(interval=20, count=10):
    producer = Producer({'bootstrap.servers': BROKER})
    
    for i in range(1, count + 1):
        timestamp = int(time.time() * 1000)  
        message = f"Message {i} at {datetime.fromtimestamp(timestamp / 1000)}"
        
        producer.produce(TOPIC, key=str(i), value=message, callback=delivery_report)
        producer.flush()
        
        print(f"Sent: {message}")
        
        time.sleep(interval)  

if __name__ == "__main__":
    produce_messages()


"""
Test run command:
 python3 test_kafka_replay.py 
Message delivered to test_kafka_replay [0] at offset 18 at time 2025-03-22 22:48:07.926232
Sent: Message 1 at 2025-03-22 22:48:07.919000
Message delivered to test_kafka_replay [0] at offset 19 at time 2025-03-22 22:48:27.948410
Sent: Message 2 at 2025-03-22 22:48:27.944000
Message delivered to test_kafka_replay [0] at offset 20 at time 2025-03-22 22:48:47.955366
Sent: Message 3 at 2025-03-22 22:48:47.952000
Message delivered to test_kafka_replay [0] at offset 21 at time 2025-03-22 22:49:07.974611
Sent: Message 4 at 2025-03-22 22:49:07.971000
Message delivered to test_kafka_replay [0] at offset 22 at time 2025-03-22 22:49:27.999473
Sent: Message 5 at 2025-03-22 22:49:27.994000
Message delivered to test_kafka_replay [0] at offset 23 at time 2025-03-22 22:49:48.022205
Sent: Message 6 at 2025-03-22 22:49:48.019000
Message delivered to test_kafka_replay [0] at offset 24 at time 2025-03-22 22:50:08.045835
Sent: Message 7 at 2025-03-22 22:50:08.042000
Message delivered to test_kafka_replay [0] at offset 25 at time 2025-03-22 22:50:28.069213
Sent: Message 8 at 2025-03-22 22:50:28.066000
Message delivered to test_kafka_replay [0] at offset 26 at time 2025-03-22 22:50:48.090479
Sent: Message 9 at 2025-03-22 22:50:48.088000
Message delivered to test_kafka_replay [0] at offset 27 at time 2025-03-22 22:51:08.110975
Sent: Message 10 at 2025-03-22 22:51:08.108000



cli command to run:

python3 cli.py --broker localhost:9092 --topic test_kafka_replay --start-time "2025-03-22 22:49:27.999473" --end-time "2025-03-22 22:50:48.090479"

[
  {
    "timestamp": 1742663988019,
    "key": "6",
    "value": "Message 6 at 2025-03-22 22:49:48.019000"
  },
  {
    "timestamp": 1742664008042,
    "key": "7",
    "value": "Message 7 at 2025-03-22 22:50:08.042000"
  },
  {
    "timestamp": 1742664028066,
    "key": "8",
    "value": "Message 8 at 2025-03-22 22:50:28.066000"
  },
  {
    "timestamp": 1742664048088,
    "key": "9",
    "value": "Message 9 at 2025-03-22 22:50:48.088000"
  }
]

"""
