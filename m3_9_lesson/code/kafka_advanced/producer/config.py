from typing import Dict, Any


class ProducerConfig:
    TOPIC = "topic2"
    PARTITION = 0
    BOOTSTRAP_SERVERS = "localhost:9091,localhost:9092,localhost:9093"

    # Если вы используете прокси, раскомментируйте и настройте:
    # PROXY_URL = "socks5://proxy-host:1080"  # или "http://proxy-host:8080"

    @staticmethod
    def get_producer_config() -> Dict[str, Any]:
        """Возвращаем конфигурацию для Кафка продюсера"""
        config = {
            'bootstrap_servers': ProducerConfig.BOOTSTRAP_SERVERS.split(','),
            'acks': 'all',
            'request_timeout_ms': 5000,
            'batch_size': 8192,
            'max_block_ms': 120000,
            'client_id': 'person-kafka-producer',
            'retries': 3,
            'enable_idempotence': True,
        }

        # Если используется прокси, добавляем proxy_url
        # if hasattr(ProducerConfig, 'PROXY_URL'):
        #     config['proxy_url'] = ProducerConfig.PROXY_URL

        return config