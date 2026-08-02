"""Модуль конфигурации Confluent Kafka Producer."""

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProducerConfig:
    """Конфигурация параметров Confluent Kafka Producer."""

    topic: str = os.getenv("KAFKA_TOPIC", "car_shop")
    partition: int | None = None
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093"
    )

    def get_producer_config(self) -> dict[str, Any]:
        """Возвращает словарь настроек в формате librdkafka (confluent-kafka)."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "client.id": "car-kafka-producer",
            # Гарантии надежности (acks='all' или -1)
            "acks": "all",
            "retries": 3,
            # Ограничение 1 некоммитнутого запроса для сохранения строгого порядка
            "max.in.flight.requests.per.connection": 1,
            # Размер локальной очереди сообщений в память
            "queue.buffering.max.messages": 100000,
        }
