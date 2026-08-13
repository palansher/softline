import ast

expression = "2 + 3 * 4"

# Парсим строку в дерево объектов AST
# mode="eval" используется для одиночных математических выражений
tree = ast.parse(expression, mode="eval")

# Выводим дерево в консоль с отступами
print(ast.dump(tree, indent=4))
