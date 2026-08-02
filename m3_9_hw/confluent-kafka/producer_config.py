"""Модуль конфигурации Kafka Producer.

Содержит параметры подключения к кластеру и настройки надежности отправки.
"""

import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProducerConfig:
    """Конфигурация параметров Kafka Producer."""

    topic: str = os.getenv("KAFKA_TOPIC", "car_shop")
    partition: int | None = None
    bootstrap_servers: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9091,localhost:9092,localhost:9093"
    )

    def get_producer_config(self) -> dict[str, Any]:
        """Возвращает словарь настроек для инициализации KafkaProducer.

        ПРОДАКШЕН-ПРАКТИКА:
        Здесь собраны ключевые настройки надежности (Durability & Ordering).
        """
        return {
            # Список брокеров для первичного подключения и вычитки метаданных кластера.
            "bootstrap_servers": [
                server.strip() for server in self.bootstrap_servers.split(",") if server.strip()
            ],
            # acks="all" (или -1): Продюсер ждет подтверждения от Лидера и ВСЕХ In-Sync реплик (ISR).
            # ГАРАНТИЯ: Исключает потерю сообщений при падении ведущего брокера.
            "acks": "all",
            # Таймаут ответа от брокера на запрос записи.
            "request_timeout_ms": 5000,
            # Размер локального буфера накопителя в байтах перед отправкой пачкой.
            "batch_size": 8192,
            # Максимальное время блокировки .send(), если буфер памяти продюсера переполнен.
            "max_block_ms": 120000,
            # Уникальный идентификатор клиентуры для логирования и мониторинга на стороне Kafka.
            "client_id": "car-kafka-producer",
            # Количество повторных попыток отправки при временных сбоях сети или Rebalance.
            "retries": 3,
            # МАКСИМАЛЬНО ВАЖНО ДЛЯ ПОРЯДКА:
            # Ограничение 1 параллельным некоммитнутым запросом на соединение.
            # ГАРАНТИЯ: Гарантирует строгий порядок сообщений! Если повтор (retry) пойдет
            # для сообщения #1, сообщение #2 не улетит вперед него.
            "max_in_flight_requests_per_connection": 1,
        }
