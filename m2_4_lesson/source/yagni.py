def parse_str_step_second(info):
    if info:
        print('Выполняем дополнительные преобразования со строкой')


def parse_str_step_first(info:str):
    if info:
        print('Преобразуем строку')
        parse_str_step_second(info)

parse_str_step_first('test')