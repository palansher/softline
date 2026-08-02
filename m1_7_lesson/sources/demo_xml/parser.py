import xml.etree.ElementTree as parser

tree = parser.parse('store.xml') #получили дерево элементов

root = tree.getroot() #получили корневой элемент из документа

for item in root:
   if not item is None:
      print(item.text)
      for child in item:
         if not child is None:
            print(child.tag, child.text)

