# Задание 3.9 - Запись и чтение объектов в/из Kafka (confluent-kafka)

- [Задание 3.9 - Запись и чтение объектов в/из Kafka (confluent-kafka)](#задание-39---запись-и-чтение-объектов-виз-kafka-confluent-kafka)
  - [Что делать](#что-делать)
    - [Создать 2 класса](#создать-2-класса)
    - [Отправить в Kafka 10 сообщений](#отправить-в-kafka-10-сообщений)
    - [Считать из Kafka полученные сообщения](#считать-из-kafka-полученные-сообщения)
  - [Требования](#требования)
  - [Особенности реализации](#особенности-реализации)
    - [kafka module](#kafka-module)
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

## Требования

`pip install confluent-kafka`

## Особенности реализации

### kafka module

Использована современная и более быстрая confluent-kafka. Лучше подходит для продакшен.

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
/home/vp/code/learn-python/.venv/bin/python /home/vp/code/learn-python/m3_9_hw/confluent-kafka/producer.py
2026-08-02 16:11:03,191 [INFO] __main__: Подготовка к отправке сообщения #0 (ID: 111f7ffa-b4cd-440e-8a60-9de3904a43ea)
2026-08-02 16:11:03,191 [INFO] __main__: Подготовка к отправке сообщения #1 (ID: b241c89b-17e6-4253-b5f4-e696ebb22514)
2026-08-02 16:11:03,191 [INFO] __main__: Подготовка к отправке сообщения #2 (ID: 46d5d09a-e789-41c1-8820-61c7df616da8)
2026-08-02 16:11:03,192 [INFO] __main__: Подготовка к отправке сообщения #3 (ID: 3c277037-b691-479c-bd56-5d936ecaf6e3)
2026-08-02 16:11:03,192 [INFO] __main__: Подготовка к отправке сообщения #4 (ID: aa3d7c2a-f60a-4ba0-8fcf-956dd890548b)
2026-08-02 16:11:03,192 [INFO] __main__: Подготовка к отправке сообщения #5 (ID: 317c67ff-ccba-4045-ad2e-fd4eff179b52)
2026-08-02 16:11:03,192 [INFO] __main__: Подготовка к отправке сообщения #6 (ID: 9bfaed18-5e1f-415d-b51d-52e7570d169f)
2026-08-02 16:11:03,192 [INFO] __main__: Подготовка к отправке сообщения #7 (ID: ee3d3c26-c900-44a9-8dc8-32946ca53d7e)
2026-08-02 16:11:03,193 [INFO] __main__: Подготовка к отправке сообщения #8 (ID: 7170581c-b8d6-4aa2-9724-817b52d70c2b)
2026-08-02 16:11:03,193 [INFO] __main__: Подготовка к отправке сообщения #9 (ID: 0b3d513e-e2b3-46fa-9325-ea0a0d27cd42)
2026-08-02 16:11:03,193 [INFO] __main__: Сброс буфера (flush) и ожидание доставки всех 10 сообщений...
2026-08-02 16:11:03,197 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 80]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 81]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 82]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 83]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 84]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 85]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 86]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 87]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 88]
2026-08-02 16:11:03,198 [INFO] __main__: Сообщение доставлено в топик 'car_shop' [партиция 0, оффсет 89]
2026-08-02 16:11:03,198 [INFO] __main__: Все 10 сообщений успешно обработаны.
```

### Consumer

```text
/home/vp/code/learn-python/.venv/bin/python /home/vp/code/learn-python/m3_9_hw/confluent-kafka/consumer.py
2026-08-02 16:12:06,673 [INFO] __main__: Kafka Consumer успешно запущен. Ожидание сообщений...
2026-08-02 16:12:06,732 [INFO] __main__: Сообщение #1 | Partition: 0 | Offset: 80 | Key: 111f7ffa-b4cd-440e-8a60-9de3904a43ea | Car: Car(brand={'name': 'Isuzu'}, model='Impulse', year=1992, category='Sedan', vin='WHXK8ZYUXUS899770', color='MediumVioletRed', id='111f7ffa-b4cd-440e-8a60-9de3904a43ea')
2026-08-02 16:12:06,732 [INFO] __main__: Сообщение #2 | Partition: 0 | Offset: 81 | Key: b241c89b-17e6-4253-b5f4-e696ebb22514 | Car: Car(brand={'name': 'Hyundai'}, model='Genesis', year=2009, category='Sedan, Hatchback', vin='R139W7P72JTAG3486', color='DarkSlateBlue', id='b241c89b-17e6-4253-b5f4-e696ebb22514')
2026-08-02 16:12:06,732 [INFO] __main__: Сообщение #3 | Partition: 0 | Offset: 82 | Key: 46d5d09a-e789-41c1-8820-61c7df616da8 | Car: Car(brand={'name': 'Dodge'}, model='Stealth', year=1995, category='SUV', vin='LUVJL9UK0D9MR5400', color='SlateGray', id='46d5d09a-e789-41c1-8820-61c7df616da8')
2026-08-02 16:12:06,732 [INFO] __main__: Сообщение #4 | Partition: 0 | Offset: 83 | Key: 3c277037-b691-479c-bd56-5d936ecaf6e3 | Car: Car(brand={'name': 'Kia'}, model='Rondo', year=2009, category='Pickup', vin='G1PZAFVF7RWDY8453', color='SlateBlue', id='3c277037-b691-479c-bd56-5d936ecaf6e3')
2026-08-02 16:12:06,732 [INFO] __main__: Сообщение #5 | Partition: 0 | Offset: 84 | Key: aa3d7c2a-f60a-4ba0-8fcf-956dd890548b | Car: Car(brand={'name': 'Lexus'}, model='LS', year=2009, category='SUV', vin='5V87YG2J6MJLZ0668', color='PowderBlue', id='aa3d7c2a-f60a-4ba0-8fcf-956dd890548b')
2026-08-02 16:12:06,733 [INFO] __main__: Сообщение #6 | Partition: 0 | Offset: 85 | Key: 317c67ff-ccba-4045-ad2e-fd4eff179b52 | Car: Car(brand={'name': 'Pontiac'}, model='GTO', year=2005, category='SUV', vin='STC0X71CX1YUG8618', color='Coral', id='317c67ff-ccba-4045-ad2e-fd4eff179b52')
2026-08-02 16:12:06,733 [INFO] __main__: Сообщение #7 | Partition: 0 | Offset: 86 | Key: 9bfaed18-5e1f-415d-b51d-52e7570d169f | Car: Car(brand={'name': 'INFINITI'}, model='G', year=2009, category='SUV', vin='FJABGUY0122S03917', color='DarkOrange', id='9bfaed18-5e1f-415d-b51d-52e7570d169f')
2026-08-02 16:12:06,733 [INFO] __main__: Сообщение #8 | Partition: 0 | Offset: 87 | Key: ee3d3c26-c900-44a9-8dc8-32946ca53d7e | Car: Car(brand={'name': 'Toyota'}, model='Corolla', year=2012, category='Van/Minivan', vin='FKG2CJKH8VV7J0527', color='MediumSeaGreen', id='ee3d3c26-c900-44a9-8dc8-32946ca53d7e')
2026-08-02 16:12:06,733 [INFO] __main__: Сообщение #9 | Partition: 0 | Offset: 88 | Key: 7170581c-b8d6-4aa2-9724-817b52d70c2b | Car: Car(brand={'name': 'FIAT'}, model='500', year=2018, category='SUV', vin='1W0ASK9K10GR17514', color='MediumVioletRed', id='7170581c-b8d6-4aa2-9724-817b52d70c2b')
2026-08-02 16:12:06,733 [INFO] __main__: Сообщение #10 | Partition: 0 | Offset: 89 | Key: 0b3d513e-e2b3-46fa-9325-ea0a0d27cd42 | Car: Car(brand={'name': 'Cadillac'}, model='Catera', year=2000, category='Pickup', vin='UTYPTY277H3W41619', color='Beige', id='0b3d513e-e2b3-46fa-9325-ea0a0d27cd42')
2026-08-02 16:12:06,733 [INFO] __main__: Достигнут лимит сообщений (10). Завершение работы.
2026-08-02 16:12:06,739 [INFO] __main__: Kafka Consumer закрыт.
```
