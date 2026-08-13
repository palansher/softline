# Чем помогает модуль ast для математических выражений

Чтобы увидеть, как Python "видит" код изнутри, в стандартном модуле `ast` есть  функция — `ast.dump()`.

---

## 🛠 Как вывести AST-дерево в дебаге

В Python 3.9+ у функции `ast.dump()` появился параметр `indent`, который превращает синтаксический "холст" в красиво отформатированное дерево:

```python
import ast

expression = "2 + 3 * 4"

# Парсим строку в дерево объектов AST
# mode="eval" используется для одиночных математических выражений
tree = ast.parse(expression, mode="eval")

# Выводим дерево в консоль с отступами
print(ast.dump(tree, indent=4))

```

---

## 🌳 Что выдает `ast.dump()` для `"2 + 3 * 4"`

Если запустить код выше, вы увидите следующую структуру:

```python
Expression(
    body=BinOp(
        left=Constant(value=2),
        op=Add(),
        right=BinOp(
            left=Constant(value=3),
            op=Mult(),
            right=Constant(value=4)
        )
    )
)

```

---

## 📐 Наглядная схема дерева

Если нарисовать эту структуру графически, то получается следующее дерево:

```text
                  Expression (Корень)
                       │
                   BinOp (+)
                  /         \
                 /           \
         Constant(2)       BinOp (*)
                          /         \
                  Constant(3)     Constant(4)

```

---

## 💡 Почему дерево выглядит именно так?

**`Expression`** — обертка верхнего уровня для вычисляемого выражения.
**`BinOp` (Binary Operation)** — узел бинарной (двухместной) операции. Он всегда состоит из трех частей:

* `left` — левый операнд
* `op` — оператор (`Add`, `Mult`, `Sub`, `Div`)
* `right` — правый операнд

### Автоматический приоритет операций

Обратите внимание: операция умножения `3 * 4` оказалась **ниже по дереву** (упакована в `right` операнд сложения).

При рекурсивном разборе дерева (как в нашем методе `_eval_node`):

* Алгоритм сначала спускается в самый низ правого крыла и вычисляет `3 * 4 = 12`.
* Затем поднимается выше и выполняет `2 + 12 = 14`.

Таким образом, парсер Python автоматически берет на себя всю сложную математическую логику скобок и приоритетов операций еще на этапе построения AST-дерева!

```python
def _eval_node(self, node: ast.AST) -> Number:
        """Рекурсивный разбор абстрактного синтаксического дерева (AST)."""
        match node:
            case ast.Constant(value=int(v) | float(v)):
                return v
            case ast.UnaryOp(op=ast.UAdd(), operand=sub_node):
                return +self._eval_node(sub_node)
            case ast.UnaryOp(op=ast.USub(), operand=sub_node):
                return -self._eval_node(sub_node)
            case ast.BinOp(left=left_node, op=op, right=right_node):
                op_type = type(op)
                if op_type not in self._OPERATORS:
                    raise InvalidExpressionError(f"Неподдерживаемый оператор: {op_type.__name__}")

                left_val = self._eval_node(left_node)
                right_val = self._eval_node(right_node)

                if op_type is ast.Div and right_val == 0:
                    raise DivisionByZeroError("Деление на 0!")

                return self._OPERATORS[op_type](left_val, right_val)
            case _:
                raise InvalidExpressionError("Выражение содержит недопустимые элементы.")

```
