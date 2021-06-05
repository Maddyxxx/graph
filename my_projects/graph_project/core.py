
class Calculate:

    def __init__(self, data):
        self.data = data

    def prepare(self):
        max_len, w_data, result = 0, [], []

        for item in self.data:
            new_item = [int(i) for i in item.split(',')]
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
        data, result, max_len = self.prepare()
        for i in range(max_len):
            for graph in data:
                result[i] += graph.pop(0)
        return str(result)[1:-1]

    def multiple(self):
        data, result, max_len = self.prepare()
        mul_result = [1 for _ in result]
        print(data)
        for i in range(max_len):
            for graph in data:
                print(mul_result[i])
                mul_result[i] *= graph.pop(0)
        return str(mul_result)[1:-1]

    def count_length_vector(self):
        result = []
        for graph in self.data:
            length = 0
            for num in graph:
                length += num ** 2
            result.append(round(length ** 0.5, 2))
        return str(result)[1:-1]


def calculate(data, number):
    calc = Calculate(data)
    if number == 1:
        result = calc.add()
    elif number == 2:
        result = calc.multiple()
    elif number == 3:
        result = calc.count_length_vector()
    else:
        return 'ошибка'
    return result

