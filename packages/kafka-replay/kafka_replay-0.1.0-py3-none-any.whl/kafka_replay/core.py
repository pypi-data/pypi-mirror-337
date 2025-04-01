import os
import logging

from confluent_kafka import Consumer, TopicPartition, KafkaException
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaReplay:
    def __init__(self,broker,topic):

        self.broker = broker
        self.topic = topic 
        self.consumer = Consumer({
            'bootstrap.servers': self.broker,
            'group.id': 'kafka_replay_group',  
            'enable.auto.commit': False
        })

    def get_offsets_from_time(self,timestamp):

        """
        Fetching teh offset info from the given timestamp
        """
        metadata = self.consumer.list_topics(self.topic)
        partitions = metadata.topics[self.topic].partitions.keys()
        if not partitions:
            raise Exception(f"Topic {self.topic} not found")
        
        partitions = [TopicPartition(self.topic, p, timestamp) for p in partitions]
        offsets = self.consumer.offsets_for_times(partitions)

        return {p.partition: o.offset for p,o in zip(partitions,offsets) if o.offset != -1}
    

    def fetch_messages(self, start_time, end_time):
        """
        Fetch messages within a specified time range without committing offsets
        """
        start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)

        results = []
        
        try:
            # Get starting offsets
            starting_offsets = self.get_offsets_from_time(start_timestamp)
            
            # Assign the consumer to the topic partitions at the specified offsets
            tps = [TopicPartition(self.topic, int(p), int(o)) for p, o in starting_offsets.items()]
            self.consumer.assign(tps)
            
            running = True
            
            while running:
                try:
                    msg = self.consumer.poll(1.0)
                    if msg is None:
                        continue
                        
                    if msg.error():
                        logger.error(f"Consumer error: {msg.error()}")
                        continue
                        
                    if msg.timestamp()[1] > end_timestamp:
                        running = False
                        continue
                        
                    results.append({
                        "timestamp": msg.timestamp()[1],
                        "key": msg.key().decode() if msg.key() else None,
                        "value": msg.value().decode() if msg.value() else None
                    })
                except KafkaException as e:
                    logger.error(f"Kafka exception occurred during polling: {e}")
                    running = False
                    
        except ConnectionError as e:
            logger.error(f"Connection error occurred: {e}")
        except KafkaException as e:
            logger.error(f"Kafka exception occurred during setup: {e}")
        finally:
            self.consumer.close()
        
        return results