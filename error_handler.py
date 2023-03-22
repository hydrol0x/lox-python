global had_error
had_error = False

def report(line: int, where: str, message: str):
    print(f"[line {line};{where}] ERROR: {message}")
    had_error = True

def error(line: int, message: str):
    report(line, "", message)