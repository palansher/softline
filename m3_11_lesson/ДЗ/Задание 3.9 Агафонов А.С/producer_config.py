from typing import Any, Dict


class ProducerConfig:
    TOPIC = "Automobile"
    PARTITION = 0
    BOOTSTRAP_SERVERS = "localhost:9092"

    @staticmethod
    def get_producer_config() -> Dict[str, Any]:
        return {
            "bootstrap_servers": ProducerConfig.BOOTSTRAP_SERVERS,
            "acks": "all",
            "request_timeout_ms": 5_000,
            "batch_size": 8_192,
            "client_id": 'automobile-producer',
            'retries': 3,
            'enable_idempotence': True,
        }