from typing import Any, Dict


class ConsumerConfig:
    TOPIC = "Automobile"
    PARTITION = 0
    BOOTSTRAP_SERVERS = "localhost:9092"
    GROUP_ID = "automobile_group"
    CLIENT_ID = "automobile_client_id"

    @staticmethod
    def get_consumer_config() -> Dict[str, Any]:
        return {
            "bootstrap_servers": ConsumerConfig.BOOTSTRAP_SERVERS,
            "group_id": ConsumerConfig.GROUP_ID,
            "client_id": ConsumerConfig.CLIENT_ID,
            "auto_offset_reset": "earliest",
            "enable_auto_commit": True,
            "auto_commit_interval_ms": 1_000,
            "max_poll_records": 50,
            "session_timeout_ms": 15_000,
        }