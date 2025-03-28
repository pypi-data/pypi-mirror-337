import os
import time

def print_banner(custom_text="by https://github.com/foxius", animate=True):
    # Цвета ANSI
    re = "\033[1;31m"  # Красный
    cy = "\033[1;36m"  # Циан
    reset = "\033[0m"  # Сброс цвета

    # ASCII-арт баннера
    banner = [
        f"{re}╔═╗{cy}┌─┐{re}═╦═",
        f"{re}╚═╗{cy}├─┤{re} ║",
        f"{re}╚═╝{cy}┴ ┴{re}═╩═",
        f"{reset}{custom_text}"
    ]

    # Очистка терминала (работает на Windows и Unix)
    os.system('cls' if os.name == 'nt' else 'clear')

    if animate:
        # Анимация появления символов
        for line in banner:
            for char in line:
                print(char, end='', flush=True)
                time.sleep(0.02)  # Задержка для эффекта
            print()  # Переход на новую строку
    else:
        # Обычный вывод без анимации
        for line in banner:
            print(line)

    print(reset)  # Сбрасываем цвет в конце