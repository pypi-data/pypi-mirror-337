def echoprint(code: str) -> None:
    """
    Транслирует код на языке echo в Python и выполняет его.
    
    Поддерживает:
    - Команды `ECHOPRINT=<текст>` → `print("<текст>")`
    - Пустые строки и пробелы
    - Экранирование кавычек в тексте
    
    Пример:
        from echo import echoprint
        echoprint('ECHOPRINT=Hello, World!')
    """
    for line in code.splitlines():
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("ECHOPRINT="):
            text = line[len("ECHOPRINT="):].strip()
            text = text.replace('"', '\\"')  # Экранируем кавычки
            python_code = f'print("{text}")'
            exec(python_code)