import random
import time
import os
import re

start_text = "Введите три значения через пробел:\n"\
       "1) Размер поля по горизонтали (от 1 до 99)\n"\
       "2) Размер поля по вертикали (от 1 до 99)\n"\
       "3) Количество бомб (не более половины всех клеток)\n"\
       "Например '2 2 1' или '99 99 3500'\n: "

pattern = "[1-9]{1}[0-9]?\s[1-9]{1}[0-9]?\s[1-9]{1}[0-9]{0,3}"

while True:
    params = input(start_text)
    if re.fullmatch(pattern, params):
        params = params.split()
        if (int(params[0]) * int(params[1])) / 2 > int(params[2]):
            x = int(params[0])+1
            y = int(params[1])+1
            num_of_bombs = int(params[2])
            break
    print("Ошибка!")

bombs = []  # Координаты бомб

labels = {}  # Координаты меток

main_table = [[0]*(x+1) for _ in range(y+1)]  # Рабочее поле

field = [["X"]*(x+1) for _ in range(y+1)]  # Видимое поле

# Шаблон для проверки координат вокруг выбранной клетки
sample = ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0))

flag = None  # Метка окончания игры


# Обозначаем края поля
for i in range(len(field)):
    if i == 0 or i == y:
        field[i] = ["~~"*x+"~"]
    else:
        field[i][0] = "|"
        field[i][-1] = "|"

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

# Расставляем цифры
for i in bombs:
    for j in sample:
        main_table[i[0] + j[1]][i[1] + j[0]] += 1

# Функция, открывающая клетки
def open_field(y1, x1):
    if not 1 <= x1 < x or not 1 <= y1 < y or field[y1][x1] != "X" or main_table[y1][x1] < 0:
        return None
    if main_table[y1][x1] > 0:
        field[y1][x1] = main_table[y1][x1]
    else:
        field[y1][x1] = "."
        for i in sample:
            open_field(y1+i[0], x1+i[1])

# Функция, устанавливающая метки
def put_label(y1, x1):
    if field[y1][x1] not in "XB":
        return None
    elif field[y1][x1] == "B":
        del labels[(y1, x1)]
        field[y1][x1] = "X"
    elif field[y1][x1] == "X":
        labels[(y1, x1)] = ""
        field[y1][x1] = "B"

# Функция отрисовки поля
def print_field():

    def c_print(color, value):
        asci = f"\033[{color}m {{}}"
        print(asci .format(value), end="")

    os.system("clear")
    print("    ", *[str(i+1)[0] for i in range(x-1)])
    if x-1 > 9:
        print("  ", *[str(i)[1] if i > 9 else " " for i in range(x)])
    for i, j in enumerate(field):
        print(["  ", str(i).ljust(2)][y > i > 0], end="")
        for n in j:
            if str(n).isdigit():
                if n <= 2:
                    c_print(36, n)
                elif 4 >= n > 2:
                    c_print(34, n)
                else:
                    c_print(35, n)
            elif n == "B":
                c_print(33, n)
            elif n == "@":
                c_print(31, n)
            else:
                c_print(37, n)
        print()

# Функция хода
def next_turn():
    print("Чтобы открыть клетку, введите через пробел значение"
          " по горизонтали, за тем по вертикали.")
    print("Чтобы поставить метку, введите через пробел символ 'm'"
          " или 'м', за тем значение по горизонтали,"
          " за тем по вертикали.")
    pattern = "([mм]\s)?[1-9]{1}[0-9]?\s[1-9]{1}[0-9]?"

    def mistake():
        print("Ошибка!")
        time.sleep(0.5)
        return [False, None]

    turn = input("Ход: ")

    if not re.fullmatch(pattern, turn):
        return mistake()

    turn = turn.split()

    if int(turn[-2]) > x-1 or int(turn[-1]) > y-1:
        return mistake()

    return [True, turn]

# Функция проверки на проигрыш
def loose(y1, x1):
    if main_table[y1][x1] < 0:
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

    turn = next_turn()

    if not turn[0]:
        continue

    if turn[1][0] in "mм":
        put_label(int(turn[1][2]), int(turn[1][1]))
        flag = win()
    else:
        open_field(int(turn[1][1]), int(turn[1][0]))
        flag = loose(int(turn[1][1]), int(turn[1][0]))
