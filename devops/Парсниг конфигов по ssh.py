# Импорт библиотеки paramiko для работы с SSH соединениями
import paramiko
# Импорт библиотеки re для работы с регулярными выражениями
import re
# Импорт функции getpass для безопасного ввода пароля
from getpass import getpass

# Определение функции для парсинга конфигурации по SSH
def ssh_config_parser(hostname, username, password, command):
    """
    Парсинг конфигурации с устройства по SSH
    """
    # Создаем экземпляр SSH клиента
    client = paramiko.SSHClient()
    
    # Настраиваем политику автоматического добавления хоста в known_hosts
    # AutoAddPolicy - автоматически добавляет хост, не проверяя его подлинность
    # (используется для тестов, в production нужно использовать более безопасные методы)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Блок try для обработки возможных ошибок подключения
    try:
        # Вывод сообщения о подключении
        print(f"🔗 Подключаемся к {hostname}...")
        # Установка SSH соединения с устройством
        client.connect(
            hostname=hostname,    # IP адрес или hostname устройства
            username=username,    # Имя пользователя для аутентификации
            password=password,    # Пароль для аутентификации
            timeout=10            # Таймаут подключения в секундах
        )
        
        # Вывод сообщения о выполняемой команде
        print(f"⚡ Выполняем команду: {command}")
        # Выполнение команды на удаленном устройстве
        # stdin - для ввода, stdout - вывод команды, stderr - ошибки
        stdin, stdout, stderr = client.exec_command(command)
        
        # Чтение и декодирование вывода команды из bytes в строку UTF-8
        output = stdout.read().decode('utf-8')
        # Чтение и декодирование ошибок команды
        error = stderr.read().decode('utf-8')
        
        # Проверка наличия ошибок в stderr
        if error:
            # Вывод сообщения об ошибке
            print(f"❌ Ошибка: {error}")
            # Возврат None в случае ошибки
            return None
        
        # Возврат результата выполнения команды
        return output
        
    # Обработка любых исключений, которые могут возникнуть при подключении
    except Exception as e:
        # Вывод сообщения об ошибке подключения
        print(f"❌ Ошибка подключения: {e}")
        # Возврат None в случае ошибки
        return None
        
    # Блок finally выполняется всегда, даже если возникло исключение
    finally:
        # Закрытие SSH соединения
        client.close()

# Определение функции для парсинга конфигурации интерфейсов
def parse_interface_config(config_text):
    """
    Парсинг конфигурации интерфейсов
    """
    # Создание пустого списка для хранения интерфейсов
    interfaces = []
    # Переменная для хранения текущего обрабатываемого интерфейса
    current_interface = None
    
    # Итерация по всем строкам конфигурации
    for line in config_text.split('\n'):
        # Удаление пробелов в начале и конце строки
        line = line.strip()
        
        # Проверка, начинается ли строка с 'interface' (начало конфига интерфейса)
        if line.startswith('interface'):
            # Если уже есть текущий интерфейс, добавляем его в список
            if current_interface:
                interfaces.append(current_interface)
            # Создание нового интерфейса
            current_interface = {
                'name': line.split()[1],  # Второе слово в строке - имя интерфейса
                'config': [line]          # Начало конфигурации интерфейса
            }
        # Если есть текущий интерфейс, добавляем строку в его конфигурацию
        elif current_interface:
            current_interface['config'].append(line)
        # Обработка глобальных настроек (не интерфейсы и не комментарии)
        elif line and not line.startswith('!'):
            # Вывод глобальных настроек
            print(f"🌐 Глобальная настройка: {line}")
    
    # Добавление последнего интерфейса после завершения цикла
    if current_interface:
        interfaces.append(current_interface)
    
    # Возврат списка всех найденных интерфейсов
    return interfaces

# Проверка, запущен ли скрипт напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    # Запрос данных для подключения у пользователя
    # Ввод IP адреса устройства
    hostname = input("Введите IP устройства: ")
    # Ввод имени пользователя
    username = input("Введите имя пользователя: ")
    # Безопасный ввод пароля (без отображения на экране)
    password = getpass("Введите пароль: ")
    
    # Команда для получения полной конфигурации устройства
    command = "show running-config"
    
    # Вызов функции для получения конфигурации по SSH
    config = ssh_config_parser(hostname, username, password, command)
    
    # Проверка, что конфигурация успешно получена
    if config:
        # Вывод начала конфигурации (первые 500 символов или вся если меньше)
        print("\n📋 Полная конфигурация:")
        # Если конфиг длиннее 500 символов, показываем начало и многоточие
        print(config[:500] + "..." if len(config) > 500 else config)
        
        # Парсинг интерфейсов из полученной конфигурации
        interfaces = parse_interface_config(config)
        
        # Вывод количества найденных интерфейсов
        print(f"\n🎯 Найдено интерфейсов: {len(interfaces)}")
        # Итерация по первым трем интерфейсам для демонстрации
        for interface in interfaces[:3]:  # Покажем первые 3
            # Вывод имени интерфейса
            print(f"\n📡 Интерфейс: {interface['name']}")
            # Вывод заголовка для конфигурации
            print("Конфигурация:")
            # Итерация по первым пяти строкам конфигурации интерфейса
            for line in interface['config'][:5]:  # Первые 5 строк конфига
                # Вывод строки конфигурации с отступом
                print(f"  {line}")