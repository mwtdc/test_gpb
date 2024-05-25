# Исходный список множеств
m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]

# 1. Общее количество чисел
res_1 = sum([len(x) for x in m])
print(res_1)
# 2. Общая сумма чисел
res_2 = sum([sum(x) for x in m])
print(res_2)
# 3. Среднее значение всех чисел
res_3 = sum(sum(subset) for subset in m) / sum(len(subset) for subset in m)
print(res_3)
# 4. Сбор всех множеств в один кортеж
res_4 = tuple(elem for x in m for elem in x)
print(res_4)
