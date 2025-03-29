# EchoPyLang - что это?
Echopylang - это библиотека которая позволяет встроить типо язык программирования под названием Echo. Позволяет программировать скрипты echo внутри Python IDE и выполняются эти скрипты при помощи интерпретатора Python что позволяет сохранять эти скрипты в .py файлах

# Установка
Установить библиотеку можно этой командой:
pip install echopylang

# Импорты
from echopylang import var - для переменных
from echopylang import echoprint - для вывода данных 
from echopylang import ECHOMATH - для математических операций

# Примеры использования 

Взаимодействие с переменными:
var.username = "Alex"
var.balance = 100.50
var.is_active = True

var.balance += 20.25

echoprint(f"User: {var.username}, Balance: ${var.balance}")

Описание:
var.username = "Alex"
var.balance = 100.50
var.is_active = True - Задаёт нужные значения переменных
var.balance += 20.25 - Добавляет 20.25 в значение
echoprint(f"User: {var.username}, Balance: ${var.balance}") - Выводит значения переменных

Математические операции:
ECHOMATH.mathoperation = "2 * (3 + 4)"  

var.x = 5
var.y = 3
ECHOMATH.mathoperation = "var.x ** var.y" 

ECHOMATH.mathoperation = "math.sqrt(var.x)"  

Описание: 
ECHOMATH.mathoperation = "2 * (3 + 4)"  - Простое вычисление 
var.x = 5
var.y = 3
ECHOMATH.mathoperation = "var.x ** var.y" - Вычисление с переменными
ECHOMATH.mathoperation = "math.sqrt(var.x)" - Выведет два и степень

Вывод данных:
echoprint("Hello World!") 

echoprint(f"Remaining balance: ${var.balance:.2f}")

echoprint("""
Transaction Details:
- Amount: $20.25
- New Balance: ${0}
""".format(var.balance))

Описание:
echoprint("Hello World!") - Простой вывод
echoprint(f"Remaining balance: ${var.balance:.2f}") - Вывод с переменными
echoprint("""
Transaction Details:
- Amount: $20.25
- New Balance: ${0}
""".format(var.balance)) - Многострочный вывод 

Это пока что все функции библиотеки но с обновлениями библиотеки этой функции будут пополнятся!