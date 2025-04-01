# Kafka Replay CLI

[![PyPI version](https://badge.fury.io/py/kafka-replay.svg)](https://pypi.org/project/kafka-replay/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A simple command-line tool to fetch Kafka messages from a specific time range. Useful for replaying messages or debugging Kafka topics.

---

## 🚀 Installation

Install from PyPI:

```sh
pip install kafka-replay
```
---

🔧 Usage


```sh
kafka-replay --broker <KAFKA_BROKER> --topic <TOPIC> --start-time "<START_TIME>" --end-time "<END_TIME>"
```
Example:
```sh
kafka-replay --broker "localhost:9092" --topic "my_topic" --start-time "2024-03-31 10:00:00" --end-time "2024-03-31 11:00:00"
```
To save the output to a file:

```sh
kafka-replay --broker "localhost:9092" --topic "my_topic" --start-time "2024-03-31 10:00:00" --end-time "2024-03-31 11:00:00" --output results.json
```
---
Using as a Library
You can also use it in Python scripts:

```python
from kafka_replay import KafkaReplay

kafka = KafkaReplay(broker="localhost:9092", topic="my_topic")
messages = kafka.fetch_messages("2024-03-31 10:00:00", "2024-03-31 11:00:00")

print(messages)

```
---

🛠 Features
Fetch Kafka messages between a given time range.

Supports CLI and Python API usage.

Saves output as JSON file (optional).

Graceful error handling.

---
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
---
🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.
---
Next Steps
Add tests

Improve performance for large data fetches

Support for different output formats (CSV, Parquet, etc.)

---
🌟 Show Your Support

If you find this tool helpful, please consider ⭐ starring the repository on GitHub!
