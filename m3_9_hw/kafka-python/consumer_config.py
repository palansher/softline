"""Модуль конфигурации Kafka Consumer."""

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConsumerConfig:
    """Конфигурация подключения и параметров Kafka Consumer."""

    topic: str = os.getenv("KAFKA_TOPIC", "car_shop")
    group_id: str = os.getenv("KAFKA_GROUP_ID", "car_group")
    client_id: str = os.getenv("KAFKA_CLIENT_ID", "car_client")
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093"
    )

    def get_consumer_config(self) -> dict[str, Any]:
        """Возвращает словарь настроек для инициализации KafkaConsumer."""
        return {
            "bootstrap_servers": [
                server.strip() for server in self.bootstrap_servers.split(",") if server.strip()
            ],
            "group_id": self.group_id,
            "client_id": self.client_id,
            # auto_offset_reset='earliest': Если группа новая и смещения (offsets)
            # еще не сохранены в __consumer_offsets, читать топик с самого начала.
            "auto_offset_reset": "earliest",
            # Автоматическое сохранение прочитанных смещений (Offset Commit).
            "enable_auto_commit": True,
            "auto_commit_interval_ms": 1000,
            # Максимальное количество сообщений, выгребаемое из Kafka за один poll().
            "max_poll_records": 500,
            # session_timeout_ms: Если консьюмер не присылает heartbeat дольше 30 сек,
            # Координатор считает его мертвым и запускает Rebalance (перебалансировку).
            "session_timeout_ms": 30000,
        }
