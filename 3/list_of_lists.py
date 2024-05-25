# Исходный список списков
a = [[1, 2, 3], [4, 5, 6]]

# Cписок словарей
b = [{f"k{x.index(j)+1}": j for j in x} for x in a]
print(b)
