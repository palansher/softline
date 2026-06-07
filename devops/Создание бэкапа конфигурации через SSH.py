# Импорт необходимых библиотек
import psutil          # Для получения системных метрик
import time            # Для работы с временем и задержками
import datetime        # Для работы с датой и временем
import json            # Для работы с JSON форматом
from pathlib import Path  # Для работы с путями файловой системы


# Класс для мониторинга системы
class SystemMonitor:
    # Конструктор класса, инициализирует директорию для логов
    def __init__(self, log_dir="./monitoring_logs"):
        # Преобразуем путь в объект Path для удобной работы
        self.log_dir = Path(log_dir)
        # Создаем директорию, если она не существует (exist_ok=True предотвращает ошибку если директория уже есть)
        self.log_dir.mkdir(exist_ok=True)

    # Метод для получения метрик процессора
    def get_cpu_metrics(self):
        """Получение метрик CPU"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),  # Загрузка CPU за последнюю секунду в процентах
            'cpu_count': psutil.cpu_count(),               # Количество ядер процессора
            'cpu_times': psutil.cpu_times()._asdict()      # Время работы CPU в различных режимах (преобразуем в dict)
        }

    # Метод для получения метрик памяти
    def get_memory_metrics(self):
        """Получение метрик памяти"""
        mem = psutil.virtual_memory()  # Получаем информацию о виртуальной памяти
        return {
            'memory_total': mem.total,        # Общий объем памяти в байтах
            'memory_available': mem.available,  # Доступная память в байтах
            'memory_used': mem.used,          # Используемая память в байтах
            'memory_percent': mem.percent     # Процент использования памяти
        }

    # Метод для получения метрик диска
    def get_disk_metrics(self):
        """Получение метрик диска"""
        disk = psutil.disk_usage('/')  # Получаем информацию о использовании диска для корневой директории
        return {
            'disk_total': disk.total,    # Общий объем диска в байтах
            'disk_used': disk.used,      # Используемое пространство в байтах
            'disk_free': disk.free,      # Свободное пространство в байтах
            'disk_percent': disk.percent  # Процент использования диска
        }

    # Метод для получения сетевых метрик
    def get_network_metrics(self):
        """Получение сетевых метрик"""
        net_io = psutil.net_io_counters()  # Получаем сетевую статистику
        return {
            'bytes_sent': net_io.bytes_sent,      # Всего отправлено байт
            'bytes_recv': net_io.bytes_recv,      # Всего получено байт
            'packets_sent': net_io.packets_sent,  # Всего отправлено пакетов
            'packets_recv': net_io.packets_recv   # Всего получено пакетов
        }

    # Метод для получения всех метрик системы
    def get_all_metrics(self):
        """Получение всех метрик системы"""
        return {
            'timestamp': datetime.datetime.now().isoformat(),  # Текущее время в ISO формате
            'cpu': self.get_cpu_metrics(),                     # Метрики CPU
            'memory': self.get_memory_metrics(),               # Метрики памяти
            'disk': self.get_disk_metrics(),                   # Метрики диска
            'network': self.get_network_metrics()              # Сетевые метрики
        }

    # Метод для логирования метрик в файл
    def log_metrics(self, filename=None):
        """Логирование метрик в файл"""
        # Если имя файла не указано, генерируем его на основе текущей даты
        if filename is None:
            filename = f"metrics_{datetime.datetime.now().strftime('%Y%m%d')}.log"  # Формат: metrics_20231201.log

        # Получаем все метрики системы
        metrics = self.get_all_metrics()
        # Формируем полный путь к файлу лога
        log_file = self.log_dir / filename

        # Открываем файл для добавления данных (режим 'a' - append)
        with open(log_file, 'a') as f:
            # Записываем метрики в формате JSON + перевод строки
            f.write(json.dumps(metrics) + '\n')

        # Возвращаем собранные метрики
        return metrics

    # Метод для бесконечного цикла мониторинга
    def monitor_loop(self, interval=60):
        """Бесконечный цикл мониторинга"""
        print("Запуск мониторинга системы...")
        print("Нажмите Ctrl+C для остановки")

        try:
            # Бесконечный цикл мониторинга
            while True:
                metrics = self.log_metrics()  # Логируем метрики и получаем их
                self.print_summary(metrics)   # Выводим сводку в консоль
                time.sleep(interval)          # Ожидаем указанный интервал
        except KeyboardInterrupt:
            # Обработка прерывания по Ctrl+C
            print("\nМониторинг остановлен")

    # Метод для вывода сводной информации в консоль
    def print_summary(self, metrics):
        """Вывод сводки метрик"""
        print(f"\n--- {metrics['timestamp']} ---")  # Время сбора метрик
        print(f"CPU: {metrics['cpu']['cpu_percent']}%")  # Загрузка CPU
        print(f"Память: {metrics['memory']['memory_percent']}%")  # Использование памяти
        print(f"Диск: {metrics['disk']['disk_percent']}%")  # Использование диска
        # Сетевой трафик: ↑ - отправлено, ↓ - получено
        print(f"Сеть: ↑{metrics['network']['bytes_sent']} ↓{metrics['network']['bytes_recv']} bytes")


# Блок выполнения при запуске скрипта напрямую
if __name__ == "__main__":
    # Создаем экземпляр монитора
    monitor = SystemMonitor()

    # Однократный сбор метрик для демонстрации
    metrics = monitor.get_all_metrics()
    print("Текущие метрики системы:")
    # Выводим метрики в формате JSON с отступами для читаемости
    print(json.dumps(metrics, indent=2))

    # Запуск непрерывного мониторинга с интервалом 10 секунд
    monitor.monitor_loop(interval=10)  # каждые 10 секунд