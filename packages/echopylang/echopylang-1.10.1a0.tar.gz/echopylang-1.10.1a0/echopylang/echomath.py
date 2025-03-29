import math

class ECHOMATH:
    """Математический модуль для языка echo"""
    
    def __init__(self):
        self._context = {}
        self._safe_globals = {
            'math': math,
            '__builtins__': None
        }
    
    @property
    def mathoperation(self):
        """Геттер для синтаксиса ECHOMATH.mathoperation"""
        return self
    
    @mathoperation.setter
    def mathoperation(self, expr: str):
        """Обработка ECHOMATH.mathoperation=2+2"""
        try:
            # Подстановка переменных (${x} → значение)
            for var, val in self._context.items():
                expr = expr.replace(f'${var}', str(val))
            
            result = eval(expr, {'__builtins__': None}, self._safe_globals)
            print(result)  # Автоматический вывод результата
        except Exception as e:
            print(f"Math Error: {e}")
    
    def set_var(self, name: str, value: float):
        """Установка переменной"""
        self._context[name] = value

# Синглтон-экземпляр
ECHOMATH = ECHOMATH()
