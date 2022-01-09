# Гра "Життя" (Conway's Game of Life). Python 3. Nov, 2021. Karolina Yakymenko

import time
import os
import random
import sys

def clear_console():
    # Функція очищує консоль за допомогою системної команди, яка залежить від ОС користувача.

    if sys.platform.startswith('win'): # Windows
        os.system("cls")
    elif sys.platform.startswith('linux'): # Linux
        os.system("clear")
    elif sys.platform.startswith('darwin'): # Mac OS X 
        os.system("clear")
    else:
        print("Не вдається очистити термінал. Ваша операційна система не підтримується.\n\r")


def resize_console(rows, cols):
    """
    Функція змінює розмір консолі залежно від розміру рядків x стовпців:
    rows: Int - кількість рядків
    cols: Int – кількість стовпців
    """

    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        os.system(command)
    elif sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3, cols=cols + cols)
        os.system(command)
    else:
        print("Не вдається змінити розмір терміналу. Ваша операційна система не підтримується.\n\r")


def create_initial_grid(rows, cols):
    """
    Функція створює випадковий список списків, який містить 1 і 0, які являють собою клітинки в грі.
     rows: Int - кількість рядків, які буде мати сітка гри
     cols: Int - кількість стовпців, які буде мати сітка гри
     grid: Int[][] - список списків, що містить 1 для живих клітин і 0 для мертвих клітин
    """

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            # Генерується випадкове число і на основі вирішується, додати живу чи мертву клітинку до сітки
            if random.randint(0, 7) == 0:
                grid_rows += [1]
            else:
                grid_rows += [0]
        grid += [grid_rows]
    return grid


def print_grid(rows, cols, grid, generation):
    """
    Друк сітки у консолі
    grid: Int[][] - список списків, які будуть використовуватися для представлення сітки гри
    generation: Int - поточне покоління сітки гри
    """

    clear_console()

    # Вихідний рядок для зменшення мерехтіння, викликане друком кількох рядків
    output_str = " "

    # Компіляція вихідного рядку, друк його на консолі
    output_str += "Покоління {0} - Щоб вийти з програми, натисніть <Ctrl-C>                         \n\r".format(generation)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                output_str += ". "
            else:
                output_str += "■ "
        output_str += "\n\r"
    print(output_str, end=" ")


def create_next_grid(rows, cols, grid, next_grid):
    """
    Функція аналізує поточне покоління гри і визначає, які клітини живуть і вмирають у наступному
    next_grid: Int[][] - список списків, які будуть використовуватися для представлення наступного покоління гри
    """

    for row in range(rows):
        for col in range(cols):
            # Отримати кількість живих клітин, суміжних із клітинкою в grid[row][col]
            live_neighbors = get_live_neighbors(row, col, rows, cols, grid)

            # Якщо кількість навколишніх живих клітин < 2 або > 3, ми робимо клітинку в grid[row][col] мертвою 
            if live_neighbors < 2 or live_neighbors > 3:
                next_grid[row][col] = 0
            # Якщо кількість навколишніх живих клітин дорівнює 3 і клітина раніше була мертвою, перетворити її на живу клітинку
            elif live_neighbors == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            # Якщо кількість навколишніх живих клітин становить 3 і клітинка в grid[row][col] жива, вона лишається живою
            else:
                next_grid[row][col] = grid[row][col]


def get_live_neighbors(row, col, rows, cols, grid):
    """
    Функція підраховує кількість живих клітин, що оточують центральну клітинку в grid[row][cell].
    row: Int - Рядок центральної клітинки
    col: Int - Стовпчик центральної комірки
    return: Int - Кількість живих клітин, що оточують клітинку в grid[row][cell].
    """

    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Необхідно підрахувати центральну клітинку, розташовану в grid[row][col]
            if not (i == 0 and j == 0):
                # За допомогою оператора за модулем (%) сітка обертається навколо
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]
    return life_sum


def grid_changing(rows, cols, grid, next_grid):
    """
    Функція перевіряє, чи сітка поточного покоління гри збігається з сіткою наступного покоління.
    grid: Int[][] - список списків, які будуть використовуватися для представлення сітки поточного покоління гри
    next_grid: Int[][] - Список списків, які будуть використовуватися для представлення сітки наступного покоління гри
    return: Boolean - чи є сітка поточного покоління такою ж, як і сітка наступного покоління
    """

    for row in range(rows):
        for col in range(cols):
            # Якщо клітинка в grid[row][col] не дорівнює next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def get_integer_value(prompt, low, high):
    """
    Функція запитує користувача ввести ціле число за заданими межами.
    prompt: String - рядок, де запропоновується користувачеві ввести дані
    low: Int - нижня межа, в межах якої користувач повинен ввести число
    high: Int - верхня межа, в межах якої користувач повинен ввести число
    return: допустиме введене значення, яке ввів користувач
    """

    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Введене значення не було дійсним цілим числом.")
            continue
        if value < low or value > high:
            print("Вхідні дані не були у межах <= {0} та >= {1}.".format(low, high))
        else:
            break
    return value


def run_game():
    """
    Функція просить користувача внести вхідні дані, щоб налаштувати гру.
    """

    clear_console()

    # Отримати кількість рядків і стовпців для сітки гри
    rows = get_integer_value("Введіть кількість рядків (10-45): ", 10, 45)
    clear_console()
    cols = get_integer_value("Введіть кількість стовпців (10-45): ", 10, 45)

    # Кількість поколінь, для яких має працювати гра
    generations = 5000
    resize_console(rows, cols)

    # Створити початкові випадкові сітки гри
    current_generation = create_initial_grid(rows, cols)
    next_generation = create_initial_grid(rows, cols)

    # Виконати послідовність гри
    gen = 1
    for gen in range(1, generations + 1):
        if not grid_changing(rows, cols, current_generation, next_generation):
            break
        print_grid(rows, cols, current_generation, gen)
        create_next_grid(rows, cols, current_generation, next_generation)
        time.sleep(1 / 5.0)
        current_generation, next_generation = next_generation, current_generation

    print_grid(rows, cols, current_generation, gen)
    return input("Натисніть <Enter> для виходу або r для повторного запуску: ")


# Почати гру
run = "r"
while run == "r":
    out = run_game()
    run = out
