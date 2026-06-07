def my_decorator(f): #f - это ссылка на функцию test_func
    def action():
        print('Сейчас будет запущена функция test_func')
        f()
        print('Действия после вызова test_func')
    return action

@my_decorator
def test_func():
    print('Функция запущена')

test_func()