a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

columns = 3
rows = 5
b = []
for i in a:
    for j in range(columns):
        b.append(j)
    b.append(i)

print(b)