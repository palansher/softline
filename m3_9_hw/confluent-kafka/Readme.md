# Задание 3.9 - Запись и чтение объектов в/из Kafka

- [Задание 3.9 - Запись и чтение объектов в/из Kafka](#задание-39---запись-и-чтение-объектов-виз-kafka)
  - [Что делать](#что-делать)
    - [Создать 2 класса](#создать-2-класса)
    - [Отправить в Kafka 10 сообщений](#отправить-в-kafka-10-сообщений)
    - [Считать из Kafka полученные сообщения](#считать-из-kafka-полученные-сообщения)
  - [Особенности реализации](#особенности-реализации)
    - [id Объекта - UUID](#id-объекта---uuid)
      - [Как это работает](#как-это-работает)
  - [создание фейковых автомобилей](#создание-фейковых-автомобилей)
    - [Faker](#faker)
  - [Лог результатов](#лог-результатов)
    - [Producer](#producer)
    - [Consumer](#consumer)

## Что делать

### Создать 2 класса

- Марка автомобиля (brand)

- модель автомобиля

У каждого объекта model свойство brand, которое содержит ссылку на объект brand.

### Отправить в Kafka 10 сообщений

сообщения содержат объект класса model (который в свою очередь содержит brand)

### Считать из Kafka полученные сообщения

## Особенности реализации

### id Объекта - UUID

В качестве ID для объекта Car использован уникальный uuid4

Для @dataclass подходит встроенная возможность field(default_factory=...). Она сама вызывает функцию генерации для каждого нового объекта, при этом отлично работает с frozen=True и slots=True без всяких костылей с __post_init__.

#### Как это работает

- uuid.uuid4() генерирует 128-битное случайное уникальное число. Вывод выглядит так: 'c9bf9e57-1685-4c89-bafb-ff5af830be8a'.

- default_factory=lambda: str(uuid.uuid4()) говорит датаклассу: "если при создании Car аргумент id не был передан вручную, выполни эту функцию и запиши результат в id".

- Порядок полей: В dataclass поля со значениями по умолчанию (default или default_factory) должны идти после обычных обязательных полей. Поэтому поле id перенесено в конец.

## создание фейковых автомобилей

### Faker

Библиотека для генерации случайных данных — Faker.

У нее есть отдельный плагин faker-vehicle, который содержит базы реальных марок, моделей, типов кузова и VIN-кодов автомобилей.

`pip install faker faker-vehicle`

см. [car-generate-example-faker.py](car-generate-example-faker.py)

## Лог результатов

### Producer

```text
/home/vp/code/learn-python/.venv/bin/python /home/vp/code/learn-python/m3_9_hw/producer.py
2026-08-02 15:24:42,764 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connecting> [IPv4 ('127.0.0.1', 9091)]>: connecting to localhost:9091 [('127.0.0.1', 9091) IPv4]
2026-08-02 15:24:42,765 [INFO] kafka.conn: Probing node bootstrap-1 broker version
2026-08-02 15:24:42,765 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connecting> [IPv4 ('127.0.0.1', 9091)]>: Connection complete.
2026-08-02 15:24:42,871 [INFO] kafka.conn: Broker version identified as 2.6.0
2026-08-02 15:24:42,872 [INFO] kafka.conn: Set configuration api_version=(2, 6, 0) to skip auto check_version requests on startup
2026-08-02 15:24:42,874 [INFO] __main__: Подготовка к отправке сообщения #0 (ID: 71b0b213-029f-4eab-b2a6-a801fc0d5429)
2026-08-02 15:24:42,876 [INFO] __main__: Подготовка к отправке сообщения #1 (ID: a5b4ac78-83e1-42a3-bb57-0376e274a98e)
2026-08-02 15:24:42,876 [INFO] __main__: Подготовка к отправке сообщения #2 (ID: 84ba1e83-2096-4738-ba62-7e225ab00615)
2026-08-02 15:24:42,876 [INFO] __main__: Подготовка к отправке сообщения #3 (ID: 13d94287-257f-41f5-8b6b-b2e18f334463)
2026-08-02 15:24:42,876 [INFO] __main__: Подготовка к отправке сообщения #4 (ID: 14a537e5-4dae-4a1a-8f6f-569ae449fa0b)
2026-08-02 15:24:42,877 [INFO] __main__: Подготовка к отправке сообщения #5 (ID: 590a3403-d18a-4970-bdcd-0bf2bbdf91e0)
2026-08-02 15:24:42,877 [INFO] __main__: Подготовка к отправке сообщения #6 (ID: 071f5e6e-3402-4e60-8ac3-342307dc431b)
2026-08-02 15:24:42,878 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: connecting to localhost:9092 [('127.0.0.1', 9092) IPv4]
2026-08-02 15:24:42,878 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: Connection complete.
2026-08-02 15:24:42,878 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connected> [IPv4 ('127.0.0.1', 9091)]>: Closing connection. 
2026-08-02 15:24:42,879 [INFO] __main__: Подготовка к отправке сообщения #7 (ID: 3e14d595-465c-42df-a463-fa90385ff57c)
2026-08-02 15:24:42,880 [INFO] __main__: Подготовка к отправке сообщения #8 (ID: 88d59673-c1fc-4d07-8e67-3fb3a5fc7340)
2026-08-02 15:24:42,880 [INFO] __main__: Подготовка к отправке сообщения #9 (ID: 4f14038c-b580-48ad-a3f2-ec5c4299bce7)
2026-08-02 15:24:42,880 [INFO] __main__: Сброс буфера (flush) и ожидание доставки всех 10 сообщений...
2026-08-02 15:24:42,887 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 60]
2026-08-02 15:24:42,888 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 61]
2026-08-02 15:24:42,888 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 62]
2026-08-02 15:24:42,888 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 63]
2026-08-02 15:24:42,889 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 64]
2026-08-02 15:24:42,889 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 65]
2026-08-02 15:24:42,889 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 66]
2026-08-02 15:24:42,894 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 67]
2026-08-02 15:24:42,894 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 68]
2026-08-02 15:24:42,894 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 69]
2026-08-02 15:24:42,895 [INFO] __main__: Все 10 сообщений успешно обработаны.
2026-08-02 15:24:42,895 [INFO] kafka.producer.kafka: Closing the Kafka producer with 9223372036.0 secs timeout.
2026-08-02 15:24:42,895 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connected> [IPv4 ('127.0.0.1', 9092)]>: Closing connection. 
2026-08-02 15:24:42,895 [INFO] __main__: Kafka Producer закрыт.
```

### Consumer

```text
/home/vp/code/learn-python/.venv/bin/python /home/vp/code/learn-python/m3_9_hw/consumer.py
2026-08-02 15:24:29,005 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connecting> [IPv4 ('127.0.0.1', 9091)]>: connecting to localhost:9091 [('127.0.0.1', 9091) IPv4]
2026-08-02 15:24:29,005 [INFO] kafka.conn: Probing node bootstrap-1 broker version
2026-08-02 15:24:29,005 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connecting> [IPv4 ('127.0.0.1', 9091)]>: Connection complete.
2026-08-02 15:24:29,107 [INFO] kafka.conn: Broker version identified as 2.6.0
2026-08-02 15:24:29,107 [INFO] kafka.conn: Set configuration api_version=(2, 6, 0) to skip auto check_version requests on startup
2026-08-02 15:24:29,108 [INFO] kafka.consumer.subscription_state: Updating subscribed topics to: ('car_shop',)
2026-08-02 15:24:29,108 [INFO] __main__: Kafka Consumer успешно запущен. Ожидание сообщений...
2026-08-02 15:24:29,109 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-0 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: connecting to localhost:9093 [('127.0.0.1', 9093) IPv4]
2026-08-02 15:24:29,109 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-0 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: Connection complete.
2026-08-02 15:24:29,109 [INFO] kafka.cluster: Group coordinator for car_group is BrokerMetadata(nodeId='coordinator-3', host='localhost', port=9093, rack=None)
2026-08-02 15:24:29,109 [INFO] kafka.coordinator: Discovered coordinator coordinator-3 for group car_group
2026-08-02 15:24:29,109 [INFO] kafka.coordinator: Starting new heartbeat thread
2026-08-02 15:24:29,110 [INFO] kafka.coordinator.consumer: Revoking previously assigned partitions set() for group car_group
2026-08-02 15:24:29,110 [INFO] kafka.conn: <BrokerConnection node_id=coordinator-3 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: connecting to localhost:9093 [('127.0.0.1', 9093) IPv4]
2026-08-02 15:24:29,110 [INFO] kafka.conn: <BrokerConnection node_id=coordinator-3 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: Connection complete.
2026-08-02 15:24:29,110 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-1 host=localhost:9091 <connected> [IPv4 ('127.0.0.1', 9091)]>: Closing connection. 
2026-08-02 15:24:29,111 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-0 host=localhost:9093 <connected> [IPv4 ('127.0.0.1', 9093)]>: Closing connection. 
2026-08-02 15:24:29,211 [INFO] kafka.coordinator: (Re-)joining group car_group
2026-08-02 15:24:29,212 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: connecting to localhost:9092 [('127.0.0.1', 9092) IPv4]
2026-08-02 15:24:29,212 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: Connection complete.
2026-08-02 15:24:29,214 [INFO] kafka.coordinator: Elected group leader -- performing partition assignments using range
2026-08-02 15:24:29,216 [INFO] kafka.coordinator: Successfully joined group car_group with generation 19
2026-08-02 15:24:29,216 [INFO] kafka.consumer.subscription_state: Updated partition assignment: [TopicPartition(topic='car_shop', partition=0)]
2026-08-02 15:24:29,217 [INFO] kafka.coordinator.consumer: Setting newly assigned partitions {TopicPartition(topic='car_shop', partition=0)} for group car_group
2026-08-02 15:24:29,218 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: connecting to localhost:9092 [('127.0.0.1', 9092) IPv4]
2026-08-02 15:24:29,218 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connecting> [IPv4 ('127.0.0.1', 9092)]>: Connection complete.
2026-08-02 15:24:29,218 [INFO] kafka.conn: <BrokerConnection node_id=bootstrap-2 host=localhost:9092 <connected> [IPv4 ('127.0.0.1', 9092)]>: Closing connection. 
2026-08-02 15:24:29,368 [INFO] kafka.conn: <BrokerConnection node_id=3 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: connecting to localhost:9093 [('127.0.0.1', 9093) IPv4]
2026-08-02 15:24:29,368 [INFO] kafka.conn: <BrokerConnection node_id=3 host=localhost:9093 <connecting> [IPv4 ('127.0.0.1', 9093)]>: Connection complete.
2026-08-02 15:24:42,886 [INFO] __main__: Сообщение #1 | Partition: 0 | Offset: 60 | Key: 71b0b213-029f-4eab-b2a6-a801fc0d5429 | Car: Car(brand={'name': 'Mercury'}, model='Grand Marquis', year=2009, category='Pickup', vin='PTKWSSF00NK7E0426', color='DodgerBlue', id='71b0b213-029f-4eab-b2a6-a801fc0d5429')
2026-08-02 15:24:42,886 [INFO] __main__: Сообщение #2 | Partition: 0 | Offset: 61 | Key: a5b4ac78-83e1-42a3-bb57-0376e274a98e | Car: Car(brand={'name': 'GMC'}, model='Sierra 2500 HD Extended Cab', year=2010, category='Pickup', vin='V0ZLZPAW113XG6825', color='MediumAquaMarine', id='a5b4ac78-83e1-42a3-bb57-0376e274a98e')
2026-08-02 15:24:42,886 [INFO] __main__: Сообщение #3 | Partition: 0 | Offset: 62 | Key: 84ba1e83-2096-4738-ba62-7e225ab00615 | Car: Car(brand={'name': 'Mercedes-Benz'}, model='CL-Class', year=2012, category='Sedan', vin='EY5RMLUC6ZJJ35687', color='GhostWhite', id='84ba1e83-2096-4738-ba62-7e225ab00615')
2026-08-02 15:24:42,886 [INFO] __main__: Сообщение #4 | Partition: 0 | Offset: 63 | Key: 13d94287-257f-41f5-8b6b-b2e18f334463 | Car: Car(brand={'name': 'Dodge'}, model='D350 Club Cab', year=1993, category='SUV', vin='KPK76EH80M8FT7593', color='LightSeaGreen', id='13d94287-257f-41f5-8b6b-b2e18f334463')
2026-08-02 15:24:42,886 [INFO] __main__: Сообщение #5 | Partition: 0 | Offset: 64 | Key: 14a537e5-4dae-4a1a-8f6f-569ae449fa0b | Car: Car(brand={'name': 'Suzuki'}, model='SX4', year=2013, category='Coupe', vin='XVUP0ZWUXAJ4X0676', color='PaleGoldenRod', id='14a537e5-4dae-4a1a-8f6f-569ae449fa0b')
2026-08-02 15:24:42,887 [INFO] __main__: Сообщение #6 | Partition: 0 | Offset: 65 | Key: 590a3403-d18a-4970-bdcd-0bf2bbdf91e0 | Car: Car(brand={'name': 'Nissan'}, model='Sentra', year=1998, category='Pickup', vin='G0ZU9BNL7WDEB1562', color='LightCyan', id='590a3403-d18a-4970-bdcd-0bf2bbdf91e0')
2026-08-02 15:24:42,887 [INFO] __main__: Сообщение #7 | Partition: 0 | Offset: 66 | Key: 071f5e6e-3402-4e60-8ac3-342307dc431b | Car: Car(brand={'name': 'Volkswagen'}, model='Cabrio', year=1998, category='Pickup', vin='MAT2RGUP9U4W45207', color='SeaGreen', id='071f5e6e-3402-4e60-8ac3-342307dc431b')
2026-08-02 15:24:42,895 [INFO] __main__: Сообщение #8 | Partition: 0 | Offset: 67 | Key: 3e14d595-465c-42df-a463-fa90385ff57c | Car: Car(brand={'name': 'Ford'}, model='Mustang', year=2017, category='Pickup', vin='R28JB64A6F7HS3937', color='Turquoise', id='3e14d595-465c-42df-a463-fa90385ff57c')
2026-08-02 15:24:42,895 [INFO] __main__: Сообщение #9 | Partition: 0 | Offset: 68 | Key: 88d59673-c1fc-4d07-8e67-3fb3a5fc7340 | Car: Car(brand={'name': 'BMW'}, model='3 Series', year=2000, category='Coupe', vin='E403X11C9HCXW4556', color='Lavender', id='88d59673-c1fc-4d07-8e67-3fb3a5fc7340')
2026-08-02 15:24:42,895 [INFO] __main__: Сообщение #10 | Partition: 0 | Offset: 69 | Key: 4f14038c-b580-48ad-a3f2-ec5c4299bce7 | Car: Car(brand={'name': 'Lexus'}, model='CT', year=2017, category='Pickup', vin='RHF76BX11M7WE2699', color='Tomato', id='4f14038c-b580-48ad-a3f2-ec5c4299bce7')
2026-08-02 15:24:42,895 [INFO] __main__: Достигнут лимит сообщений (10). Завершение работы.
2026-08-02 15:24:42,899 [INFO] kafka.coordinator: Stopping heartbeat thread
2026-08-02 15:24:42,900 [INFO] kafka.coordinator: Leaving consumer group (car_group).
2026-08-02 15:24:42,908 [INFO] kafka.conn: <BrokerConnection node_id=coordinator-3 host=localhost:9093 <connected> [IPv4 ('127.0.0.1', 9093)]>: Closing connection. 
2026-08-02 15:24:42,908 [INFO] kafka.conn: <BrokerConnection node_id=2 host=localhost:9092 <connected> [IPv4 ('127.0.0.1', 9092)]>: Closing connection. 
2026-08-02 15:24:42,908 [INFO] kafka.conn: <BrokerConnection node_id=3 host=localhost:9093 <connected> [IPv4 ('127.0.0.1', 9093)]>: Closing connection. 
2026-08-02 15:24:42,908 [INFO] __main__: Kafka Consumer закрыт.
```
