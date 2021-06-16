from pprint import pprint

from core import calculate, resize

G = {  # 4х уровневый граф
    'vectors': [
        {
            'vectors': [
                {'vectors': ['1, 2, 3', '3, 4, 5'], 'op': 'add'},
                '7, 7, 7',
            ],
            'op': 'mul'
        },
        {
            'vectors': [
                {'vectors': ['3, 4, 5, 9', '3, 5, 6, 2'], 'op': 'len'},
                '7, 8, 9',
                {'vectors': ['1, 2, 9, 9', '8, 3, 4', ], 'op': 'mul'}
            ],
            'op': 'add'
        },
        {
            'vectors': [
                '12, 45, 14',
                {'vectors': [
                    '31, 18, 34',
                    '54, 6, 23, 89',
                    {'vectors': ['3, 6, 17, 21, 17', '7, 31, 2, 31, 66'], 'op': 'mul'},
                ],
                    'op': 'add'
                },
                '45, 12'
            ],
            'op': 'add'
        },
        {
            'vectors': [
                '13, 81, 42',
                '34, 16, 99',
                {'vectors': ['1, 2, 13, 21, 17', '7, 31, 2, 1'], 'op': 'len'},
            ],
            'op': 'mul'
        },
    ],
    'op': 'mul'
}

graphs_view = [
    {'vectors': ['13, 81, 42', '34, 16, 99'], 'op': 'mul'},
    {'vectors': ['3, 6, 17, 21, 17', '7, 31, 2, 31, 66'], 'op': 'mul'},
    {'vectors': ['31, 18, 34', '54, 6, 23, 89'], 'op': 'add'}
]

data_2 = ['2, 3, 4', '3, 1, 9, 2']
test_d = resize(data_2)
print(test_d)

print(calculate(data_2, 'len'))