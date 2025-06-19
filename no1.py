import random

def input_list_keyboard():
    """
    Ввод списка с клавиатуры с проверкой корректности.
    Пользователь вводит числа через пробел.
    При ошибке ввода повторяется запрос.
    """
    while True:
        try:
            lst = list(map(int, input("Введите элементы списка через пробел: ").split()))
            return lst
        except ValueError:
            print("Некорректный ввод. Пожалуйста, вводите только целые числа.")

def generate_list_auto(size=10, min_val=1, max_val=10):
    """
    Автоматическая генерация списка случайных целых чисел.
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def find_longest_chain_manual(lst):
    """
    Поиск самой длинной цепочки одинаковых элементов без использования стандартных функций.
    Возвращает кортеж (start_index, length).
    """
    max_len = 1
    max_start = 0
    current_len = 1
    current_start = 0

    for i in range(1, len(lst)):
        if lst[i] == lst[i-1]:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 1
            current_start = i

    if current_len > max_len:
        max_len = current_len
        max_start = current_start

    return max_start, max_len

def find_longest_chain_std(lst):
    """
    Поиск самой длинной цепочки одинаковых элементов с использованием стандартных функций.
    Возвращает кортеж (start_index, length).
    """
    max_len = 1
    max_start = 0
    current_len = 1
    current_start = 0

    for i in range(1, len(lst)):
        if lst[i] == lst[i-1]:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 1
            current_start = i

    if current_len > max_len:
        max_len = current_len
        max_start = current_start

    return max_start, max_len

def swap_longest_chains(A, B, find_chain_func):
    """
    Обмен самыми длинными цепочками между списками A и B.
    find_chain_func - функция для поиска цепочки (manual или std).
    Возвращает новые списки после обмена.
    """
    start_A, len_A = find_chain_func(A)
    start_B, len_B = find_chain_func(B)

    chain_A = A[start_A:start_A+len_A]
    chain_B = B[start_B:start_B+len_B]

    A_new = A[:start_A] + A[start_A+len_A:]
    B_new = B[:start_B] + B[start_B+len_B:]

    A_new = A_new[:start_A] + chain_B + A_new[start_A:]
    B_new = B_new[:start_B] + chain_A + B_new[start_B:]

    return A_new, B_new

# Пример использования
if __name__ == "__main__":
    # Ввод или генерация списков
    print("Введите список A или оставьте пустым для генерации:")
    A = input_list_keyboard()
    if not A:
        A = generate_list_auto()

    print("Введите список B или оставьте пустым для генерации:")
    B = input_list_keyboard()
    if not B:
        B = generate_list_auto()

    print("Исходный список A:", A)
    print("Исходный список B:", B)

    # Обмен цепочками с использованием ручного поиска
    A_new, B_new = swap_longest_chains(A, B, find_longest_chain_manual)
    print("Списки после обмена (без стандартных функций):")
    print("A:", A_new)
    print("B:", B_new)

    # Обмен цепочками с использованием стандартных функций
    A_new_std, B_new_std = swap_longest_chains(A, B, find_longest_chain_std)
    print("Списки после обмена (со стандартными функциями):")
    print("A:", A_new_std)
    print("B:", B_new_std)


#feature 22222