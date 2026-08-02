"""Модуль конфигурации Confluent Kafka Consumer."""

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConsumerConfig:
    """Конфигурация параметров Confluent Kafka Consumer."""

    topic: str = os.getenv("KAFKA_TOPIC", "car_shop")
    group_id: str = os.getenv("KAFKA_GROUP_ID", "car_group")
    client_id: str = os.getenv("KAFKA_CLIENT_ID", "car_client")
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093"
    )

    def get_consumer_config(self) -> dict[str, Any]:
        """Возвращает словарь настроек для Confluent Consumer."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group_id,
            "client.id": self.client_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "auto.commit.interval.ms": 1000,
            "session.timeout.ms": 30000,
        }
