
import argparse
import json
from .core import KafkaReplay
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Kafka Time-Range Fetcher")
    parser.add_argument("--broker", required=True, help="Kafka broker address")
    parser.add_argument("--topic", required=True, help="Kafka topic name")
    parser.add_argument("--start-time", required=True, help="Start time (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end-time", required=True, help="End time (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--output",help="output file to save JSON data (Optional)")

    args = parser.parse_args()
    kafka_replay = KafkaReplay(args.broker, args.topic)
    messages = kafka_replay.fetch_messages(args.start_time, args.end_time)

    if args.output:
        with open(args.output , "w", encoding='utf-8') as f:
            json.dump(messages,f,indent=2)
        logger.info(f"Data saved to {args.output}")
    else:
        logger.info(json.dumps(messages, indent=2))

if __name__ == "__main__":
    main()


# kafka-replay --topic my_topic --start-time "2024-03-21 10:00" --end-time "2024-03-21 11:00"

# kafka-replay --broker localhost:9092 --topic test_kafka_replay --start-time "2025-03-22 22:49:27.999473" --end-time "2025-03-22 22:50:48.090479"

# python3 cli.py --broker localhost:9092 --topic test_kafka_replay --start-time "2025-03-22 22:49:27.999473" --end-time "2025-03-22 22:50:48.090479"

# python3 cli.py --broker localhost:9092 --topic test_kafka_replay --start-time "2025-03-31 11:31:44.569487" --end-time "2025-03-31 11:33:44.700502" --output test.json
