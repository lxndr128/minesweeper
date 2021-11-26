#Нет защиты от неправильного ввода
import random
import os

print("CHELLO EVERYBODY!!!!!")

x = int(input("Размер поля по горизонтали:"))+1

y = int(input("Размер поля по вертикали:"))+1

num_of_bombs = int(input("Количество бомб:"))

bombs = [] # Координаты бомб

labels = dict() # Координаты меток

main_table = [[0]*(x+1) for _ in range(y+1)] # Рабочее поле

field = [["X"]*(x+1) for _ in range(y+1)] # Видимое поле

sample = ((1,1),(-1,1),(1,-1),(-1,-1),(0,1),(1,0),(0,-1),(-1,0)) # Шаблон для проверки координат вокруг выбранной клетки

flag = None # Метка окончания игры


#Обозначаем края поля
for i in field:
    if field.index(i)==0 or field.index(i)==y:
        field[field.index(i)] = ["~~"*x]
    else:
        field[field.index(i)][0] = "|"
        field[field.index(i)][-1] = "|"

# Расставляем бомбы
for _ in range(num_of_bombs):
    while True:
        x1, y1 = random.randint(1, x-1), random.randint(1, y-1)
        if main_table[y1][x1] == -9:
            continue
        else:
            main_table[y1][x1] = -9
            bombs.append((y1, x1))
            break
bombs = tuple(bombs)

# Расставляем цифры
for i in bombs:
    for j in sample:
        main_table[i[0] + j[1]][i[1] + j[0]] += 1

# Переводим рабочее поле в кортеж, т.к. менять его больше не требуется
main_table = tuple(main_table)

# Функция, открывающая клетки
def open_field(y1, x1):
    if not 1<=x1<x or not 1<=y1<y or field[y1][x1] != "X" or main_table[y1][x1] < 0:
        return None
    if main_table[y1][x1] > 0:
        field[y1][x1] = main_table[y1][x1]
    else:
        field[y1][x1] = "."
        for i in sample:
            open_field(y1+i[0], x1+i[1])

# Функция, устанавливающая метки
def put_label(y1, x1):
    if field[y1][x1] != "X" and field[y1][x1] != "B":
        return None
    elif field[y1][x1] == "B":
        del labels[(y1,x1)]
        field[y1][x1] = "X"
    elif field[y1][x1] == "X":
        labels[(y1,x1)] = ""
        field[y1][x1] = "B"

# Функция отрисовки поля
def print_field():
    os.system("cls")
    for i in field:
        print(*i)

# Функция проверки на проигрыш
def loose(y1, x1):
    if main_table[y1][x1]<0:
        field[y1][x1] = "@"
        print_field()
        print("ВЫ ПРОИГРАЛИ!")
        return False
    else:
        return None

# Функция проверки на победу
def win():
    if set(bombs) == set(labels.keys()):
            print_field()
            print("ВЫ ПОБЕДИЛИ!")
            return True
    else:
        return None

while flag == None:
    print_field()
    print("Чтобы открыть клетку, введите через пробел значение по горизонтали, за тем по вертикали.")
    print("Чтобы поставить метку, введите через пробел символ m или м, за тем значение по горизонтали, за тем по вертикали.")
    turn = input("Ход:").split()
    if len(turn)==3 and turn[0] in "mм":
        put_label(int(turn[2]),int(turn[1]))
        flag = win()
    else:
        open_field(int(turn[1]),int(turn[0]))
        flag = loose(int(turn[1]),int(turn[0]))
