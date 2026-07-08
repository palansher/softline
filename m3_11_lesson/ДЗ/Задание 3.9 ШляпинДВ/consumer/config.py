from typing import Dict, Any


class KafkaConsumerConfig:
    TOPIC = "my_cars"
    BOOTSTRAP_SERVERS = "localhost:9091,localhost:9092,localhost:9093"
    GROUP_ID = "cars_group"
    CLIENT_ID = "cars_client"

    @staticmethod
    def get_consumer_config() -> Dict[str, Any]:
        return {
            'bootstrap_servers': KafkaConsumerConfig.BOOTSTRAP_SERVERS.split(','),
            'group_id': KafkaConsumerConfig.GROUP_ID,
            'client_id': KafkaConsumerConfig.CLIENT_ID,
            'auto_offset_reset': 'earliest',
            'enable_auto_commit': True,
            'auto_commit_interval_ms': 1000,
            'max_poll_records': 500 ,
            'session_timeout_ms': 30000
        }