from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self):
        pass

class ParserForXml(Parser):
    def parse(self,path):
        print('Выполняем извлечение данных из xml документа')

class ParserForJson(Parser):
    def parse(self,path):
        print('Выполняем извлечение данных из json документа')

class StrategyImpl:
    @staticmethod
    def parse_doc(path):
        ext = path.split('.')[-1]
        match ext:
            case 'xml':
                parser = ParserForXml()
            case 'json':
                parser = ParserForJson()
            case _:
                raise Exception('Тип файла некорректный')
        parser.parse(path)

StrategyImpl.parse_doc('test.xml')