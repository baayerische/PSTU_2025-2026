import random

# Универсум
U = list(range(-30, 31))

# ===== Реализация операций =====
def union(A, B):
    result = []
    for x in A:
        if x not in result:
            result.append(x)
    for x in B:
        if x not in result:
            result.append(x)
    return result if result else ["0"]

def intersection(A, B):
    result = []
    for x in A:
        if x in B and x not in result:
            result.append(x)
    return result if result else ["0"]

def difference(A, B):
    result = []
    for x in A:
        if x not in B:
            result.append(x)
    return result if result else ["0"]

def sym_difference(A, B):
    result = []
    for x in A:
        if x not in B and x not in result:
            result.append(x)
    for x in B:
        if x not in A and x not in result:
            result.append(x)
    return result if result else ["0"]

def complement(A, U):
    result = []
    for x in U:
        if x not in A:
            result.append(x)
    return result if result else ["0"]

# ===== Задание множества =====
def input_set(name):
    while True:
        print(f"\nКак задать множество {name}?")
        print("1 - ручной ввод")
        print("2 - случайная генерация")
        print("3 - автозаполнение по условию (чётность, кратность, знак)")
        choice = input("Введите номер: ")

        try:
            if choice == "1":
                raw = input(f"Введите элементы множества {name} через пробел (от -30 до 30): ").split()
                nums = []
                for x in raw:
                    if not x.lstrip("-").isdigit():
                        raise ValueError(f"Элемент '{x}' не является числом")
                    num = int(x)
                    if num < -30 or num > 30:
                        raise ValueError(f"Элемент {num} выходит за пределы [-30, 30]")
                    if num in nums:
                        raise ValueError(f"Элемент {num} введён повторно")
                    nums.append(num)
                return nums

            elif choice == "2":
                k = int(input("Сколько случайных элементов? "))
                if k < 0 or k > len(U):
                    raise ValueError("Некорректное количество элементов")
                return random.sample(U, k)

            elif choice == "3":
                print("Условие:")
                print("1 - чётные числа")
                print("2 - нечётные числа")
                print("3 - положительные")
                print("4 - отрицательные")
                print("5 - кратные N")
                cond = input("Выберите: ")

                if cond == "1":
                    return [x for x in U if x % 2 == 0]
                elif cond == "2":
                    return [x for x in U if x % 2 != 0]
                elif cond == "3":
                    return [x for x in U if x > 0]
                elif cond == "4":
                    return [x for x in U if x < 0]
                elif cond == "5":
                    N = int(input("Введите N: "))
                    if N == 0:
                        raise ValueError("N не может быть 0")
                    return [x for x in U if x % N == 0]
                else:
                    raise ValueError("Нет такого условия!")

            else:
                print("Ошибка: нет такого варианта")
        except ValueError as e:
            print("Ошибка:", e)
            print("Попробуйте снова.\n")


# ======= ВЫЧИСЛЕНИЕ ВЫРАЖЕНИЯ =======
def eval_expression(expr, sets):
    expr = expr.replace(" ", "").upper()

    # Поддерживаемые операции: + объединение, * пересечение, - разность, ^ симм.разность, ! дополнение
    # Преобразуем скобки и последовательность действий вручную (через стек)
    def parse(tokens):
        stack = []
        output = []

        prec = {'!': 3, '*': 2, '^': 1, '+': 1, '-': 1}
        right_assoc = {'!'}

        for token in tokens:
            if token in sets:
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:  # операция
                while stack and stack[-1] != '(' and (
                    prec.get(stack[-1], 0) > prec.get(token, 0)
                    or (prec.get(stack[-1], 0) == prec.get(token, 0) and token not in right_assoc)
                ):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            output.append(stack.pop())

        return output

    # Постфиксное вычисление
    def calc(postfix):
        stack = []
        for token in postfix:
            if token in sets:
                stack.append(sets[token])
            elif token == '!':
                a = stack.pop()
                stack.append(complement(a, U))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(union(a, b))
                elif token == '*':
                    stack.append(intersection(a, b))
                elif token == '-':
                    stack.append(difference(a, b))
                elif token == '^':
                    stack.append(sym_difference(a, b))
        return stack[0]

    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] in "()+*-^!":
            tokens.append(expr[i])
            i += 1
        elif expr[i].isalpha():
            tokens.append(expr[i])
            i += 1
        else:
            i += 1
    postfix = parse(tokens)
    return calc(postfix)


# ===== Основная программа =====
def main():
    sets = {"A": input_set("A"), "B": input_set("B"), "C": input_set("C")}

    while True:
        print("\nТекущие множества:")
        for k, v in sets.items():
            print(f"{k} = {v if v else '0'}")

        print("\nОперации:")
        print("1 - объединение (A U B)")
        print("2 - пересечение (A n B)")
        print("3 - разность (A \\ B)")
        print("4 - симметрическая разность (A ^ B)")
        print("5 - дополнение (!A)")
        print("6 - ввести выражение вручную (например (A-B)*C)")
        print("0 - выход")

        op = input("Выберите операцию: ")

        if op == "0":
            break

        if op == "6":
            expr = input("Введите выражение (пример: (A-B)*C или !(A+B)): ")
            res = eval_expression(expr, sets)
        elif op in ["1", "2", "3", "4"]:
            s1 = input("Первое множество (A, B, C): ").upper()
            s2 = input("Второе множество (A, B, C): ").upper()
            if s1 not in sets or s2 not in sets:
                print("Ошибка: нет такого множества")
                continue
            set1, set2 = sets[s1], sets[s2]

            if op == "1":
                res = union(set1, set2)
            elif op == "2":
                res = intersection(set1, set2)
            elif op == "3":
                res = difference(set1, set2)
            else:
                res = sym_difference(set1, set2)

        elif op == "5":
            s1 = input("Какое множество (A, B, C): ").upper()
            if s1 not in sets:
                print("Ошибка: нет такого множества")
                continue
            res = complement(sets[s1], U)
        else:
            print("Ошибка: нет такой операции")
            continue

        print("Результат:", res if res != ["0"] else "0")

        save = input("Сохранить результат в одно из множеств (A, B, C)? (y/n): ").lower()
        if save == "y":
            target = input("Куда сохранить (A, B, C): ").upper()
            if target in sets:
                sets[target] = res if res != ["0"] else []
                print(f"Множество {target} обновлено.")


main()
