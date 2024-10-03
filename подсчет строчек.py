import os

total = [i for i in os.listdir() if '.py' in i]
strings = 0
for i in total:
    with open(i, encoding='utf-8') as file:
        strings += len(file.readlines())

print(strings)