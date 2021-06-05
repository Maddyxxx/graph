from django.test import TestCase
from core import calculate
# Create your tests here.
list_2 = ["2,4,6", "1,2,3"]
list_1 = []
# dict_1 = {}
# for item in list_1:
#
#     list_2.append({'name': item})


result = calculate(list_2, 2)
print(result)
