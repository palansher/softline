# Импорт модуля для работы с регулярными выражениями
import re

# Импорт типов для аннотаций (улучшает читаемость и проверку кода)
from typing import Dict, List, Any

# Объявление функции с аннотацией типов
def parse_cisco_config(config_text: str) -> Dict[str, Any]:
    """
    Парсинг конфигурации Cisco для извлечения VLAN и IP
    """
    # Создание словаря для хранения результатов парсинга
    result = {
        'vlans': [],        # список VLAN
        'interfaces': [],   # список интерфейсов
        'ip_addresses': []  # список IP-адресов
    }
    
    # Поиск VLAN
    # Регулярное выражение для поиска VLAN:
    # - vlan + пробелы + цифры (сохраняем в группу 1)
    # - перевод строки + пробелы + name + пробелы + любые непробельные символы (группа 2)
    vlan_pattern = r'vlan\s+(\d+)\s*\n\s*name\s+(\S+)'
    
    # Поиск всех совпадений VLAN в тексте конфигурации
    # re.IGNORECASE - игнорирование регистра (vlan/VLAN)
    vlans = re.findall(vlan_pattern, config_text, re.IGNORECASE)
    
    # Обработка найденных VLAN
    for vlan_id, vlan_name in vlans:
        # Добавление VLAN в результат
        result['vlans'].append({
            'id': int(vlan_id),         # преобразование ID в число
            'name': vlan_name.strip()   # удаление пробелов в начале/конце имени
        })
    
    # Поиск интерфейсов с IP-адресами
    # Регулярное выражение для поиска интерфейсов:
    # - interface + пробелы + любые непробельные символы (группа 1 - имя интерфейса)
    # - перевод строки + любое содержимое (группа 2 - конфигурация интерфейса)
    # (?=\ninterface|\n!\n|$) - позитивный просмотр вперед: до следующего интерфейса, ! или конца строки
    interface_pattern = r'interface\s+(\S+)\s*\n(.*?)(?=\ninterface|\n!\n|$)'
    
    # Поиск всех интерфейсов
    # re.IGNORECASE - игнорирование регистра
    interfaces = re.findall(interface_pattern, config_text, re.DOTALL | re.IGNORECASE)
    
    # Обработка найденных интерфейсов
    for interface_name, interface_config in interfaces:
        # Создание структуры для хранения информации об интерфейсе
        interface_info = {
            'name': interface_name.strip(),  # имя интерфейса без пробелов
            'ip_address': None,              # IP-адрес (пока неизвестен)
            'vlan': None,                    # VLAN (пока неизвестен)
            'description': None              # описание (пока неизвестно)
        }
        
        # Поиск IP-адреса в конфигурации интерфейса
        # Регулярное выражение для поиска IP-адреса и маски:
        # - ip address + пробелы + IPv4 адрес (группа 1) + пробелы + маска (группа 2)
        ip_match = re.search(r'ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', 
                            interface_config, re.IGNORECASE)
        if ip_match:
            # Форматирование IP-адреса в виде "адрес/маска"
            interface_info['ip_address'] = f"{ip_match.group(1)}/{ip_match.group(2)}"
            
            # Добавление IP-адреса в общий список
            result['ip_addresses'].append({
                'interface': interface_name.strip(),  # имя интерфейса
                'ip_address': ip_match.group(1),      # IP-адрес
                'subnet_mask': ip_match.group(2)      # маска подсети
            })
        
        # Поиск VLAN для интерфейса
        # Регулярное выражение для поиска VLAN в интерфейсе:
        # - switchport access vlan + пробелы + цифры (ID VLAN)
        vlan_match = re.search(r'switchport access vlan\s+(\d+)', 
                              interface_config, re.IGNORECASE)
        if vlan_match:
            # Сохранение ID VLAN как числа
            interface_info['vlan'] = int(vlan_match.group(1))
        
        # Поиск описания интерфейса
        # Регулярное выражение для поиска описания:
        # - description + пробелы + любой текст до перевода строки
        desc_match = re.search(r'description\s+(.+?)\n', 
                              interface_config, re.IGNORECASE)
        if desc_match:
            # Сохранение описания без пробелов по краям
            interface_info['description'] = desc_match.group(1).strip()
        
        # Добавление информации об интерфейсе в результат
        result['interfaces'].append(interface_info)
    
    # Возврат результата парсинга
    return result

# Пример использования
# Многострочная строка с примером конфигурации Cisco
cisco_config = """
!
vlan 10
 name Management
!
vlan 20
 name Users
!
interface GigabitEthernet0/1
 description Uplink to core
 ip address 192.168.1.1 255.255.255.0
!
interface GigabitEthernet0/2
 switchport mode access
 switchport access vlan 10
!
"""

# Вызов функции парсинга
parsed = parse_cisco_config(cisco_config)

# Вывод результатов
print("VLANs:", parsed['vlans'])
print("IP Addresses:", parsed['ip_addresses'])