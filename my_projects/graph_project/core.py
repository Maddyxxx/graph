import json


class Calculate:

    def __init__(self, data):
        self.data = data

    def prepare(self):
        """
        Данная функция приводит исходные данные к нужному формату:
        возвращает:
            - w_data - список исходных чисел в нужном формате [int, int, ...]
            - result, - список из нулей длины max_len
            - max_vec_len - максимальная длина вектора
        """
        w_data, result, max_len = [], [], 0

        for item in self.data:
            try:
                new_item = [int(i) for i in item.split(',')]
            except:
                new_item = [float(i) for i in item.split(',')]
            w_data.append(new_item)

        for i in w_data:
            max_len = len(i) if max_len < len(i) else max_len

        for graph in w_data:
            if len(graph) < max_len:
                while len(graph) != max_len:
                    graph.append(0)
        while len(result) != max_len:
            result.append(0)

        return w_data, result, max_len

    def add(self):
        """
        Сложение векторов
        """
        data, result, max_len = self.prepare()
        for i in range(max_len):
            for graph in data:
                result[i] += graph.pop(0)
        return str(result)[1:-1]

    def multiple(self):
        """
        Умножение векторов
        """
        data, result, max_len = self.prepare()
        mul_result = [1 for _ in result]
        for i in range(max_len):
            for graph in data:
                mul_result[i] *= graph.pop(0)
        return str(mul_result)[1:-1]

    def count_length_vector(self):
        """
        Подсчет длины вектора/векторов
        """
        result = []
        data = self.prepare()[0]
        for graph in data:
            length = 0
            for num in graph:
                length += num ** 2
            result.append(round(length ** 0.5, 2))
        return str(result)[1:-1]


def calculate(data, operation):
    """
    Принимает на вход:
     - строковое значение векторов формата '['vector_1', 'vector_2',....]'
     - тип операции: 'mul'/'add'/'len'

    Вычисляет результат и возвращает его в строковом виде
    При неудачном вычислении возвращает ошибку
    """
    calc = Calculate(data)
    operations = ['add', 'mul', 'length']
    if operation in operations:
        try:
            if operation == 'add':
                result = calc.add()
            elif operation == 'mul':
                result = calc.multiple()
            else:
                result = calc.count_length_vector()
        except Exception as exc:
            result = str(exc)
    else:
        return 'Ошибка! Неверная операция'
    return result


def resize(data):
    """
    Если добавляется число в вектор, то для избежания критических ошибок
    при выполнении операций в других векторах добавляется нулевая компонента
    """
    calc = Calculate(data)
    resized = calc.prepare()[0]
    return [str(i)[1:-1] for i in resized]

