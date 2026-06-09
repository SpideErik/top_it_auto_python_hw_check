import ast
import multiprocessing
from contextlib import redirect_stdout, redirect_stderr
import contextlib
import io
from io import StringIO


def check_syntax(content: str):
    # Проверка синтаксиса Python
    try:
        ast.parse(content)
    except SyntaxError as e:
        return False, f'Ошибка синтаксиса в тесте: {e.msg} (строка {e.lineno})'

    return True, 'ok'


class EducationSecurity(ast.NodeVisitor):
    def __init__(self, allowed_modules, allowed_functions):
        self.allowed_modules = allowed_modules
        self.allowed_functions = allowed_functions
        self.errors = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name not in self.allowed_modules:
                self.errors.append(f"Запрещен импорт модуля: {alias.name}")

    def visit_ImportFrom(self, node):
        if node.module not in self.allowed_modules:
            self.errors.append(f"Запрещен импорт из модуля: {node.module}")

    def visit_Name(self, node):
        # Блокируем доступ к любым системным именам (напр. __builtins__)
        if node.id.startswith('__'):
            self.errors.append(f"Использование системных имен запрещено: {node.id}")

        # Проверяем, не пытается ли код вызвать запрещенную встроенную функцию
        # (Если это обращение к переменной, а не вызов, проверка тоже сработает)
        # Но для простоты учебных задач мы проверяем именно вызовы в visit_Call.

    def visit_Attribute(self, node):
        # Блокируем доступ к атрибутам вроде obj.__class__ или obj.__subclasses__
        if node.attr.startswith('__'):
            self.errors.append(f"Доступ к системным атрибутам запрещен: .{node.attr}")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Проверяем вызовы функций
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in self.allowed_functions and func_name not in self.allowed_modules:
                # Если это не функция из списка и не название модуля (math.sqrt)
                self.errors.append(f"Функция '{func_name}' не разрешена для этой задачи")
        self.generic_visit(node)



DEF_ALLOWED_MODULES = [
    'math'
]

DEF_ALLOWED_BUILTINS = [
    'print',
    'input',
    'int',
    'float',
    'str',
    'list',
    'range',
    'sorted',
    'min',
    'max',
    'map',
    'sum',
    'len',
    'abs',
]

def check_student_code(content: str, allowed_modules:list[str]|None = None, allowed_builtins=None):
    if not allowed_modules:
        allowed_modules = DEF_ALLOWED_MODULES
    if not allowed_builtins:
        allowed_builtins = DEF_ALLOWED_BUILTINS

    # Статическая проверка (AST)
    try:
        tree = ast.parse(content)
        checker = EducationSecurity(allowed_modules, set(allowed_builtins))
        checker.visit(tree)

        if checker.errors:
            return False, checker.errors

    except SyntaxError as e:
        return False, [f'Ошибка синтаксиса в тесте: {e.msg} (строка {e.lineno})']

    return True, 'ok'


class redirect_stdin(contextlib._RedirectStream):
    """Context manager for temporarily receiving stdin from another source."""
    _stream = "stdin"


def code_wrapper(src, allowed_builtins, allowed_modules, inp, queue):
    try:
        code = compile(src, 'test.py', 'exec')
        import builtins
        safe = {i: getattr(builtins, i) for i in allowed_builtins}
        for i in allowed_modules:
            safe[i] = __import__(i)
        out = StringIO()
        err = StringIO()

        with redirect_stdin(io.StringIO(inp)), redirect_stdout(out), redirect_stderr(err):
            exec(code, {"__builtins__": safe}, {})
        queue.put((True, out.getvalue(), err.getvalue()))
    except Exception as e:
        queue.put((False, '', 'Сбой при выполнении'))


def run_student_code(code, inp, timeout=2.0):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=code_wrapper, args=(code, DEF_ALLOWED_BUILTINS, DEF_ALLOWED_MODULES, inp, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return False, "Превышено время исполнения"
    return q.get()

def run_student_tests(code: str, tests:str):
    lines = tests.splitlines()
    result = []
    i = 0
    while i < len(lines):
        inp = ''
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                break
            inp += lines[i] + '\n'
            i += 1
        out = ''
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                break
            out += lines[i] + '\n'
            i += 1
        test_res = run_student_code(code, inp, 2.0)
        if not test_res[0]:
            result.append(test_res)
        else:
            result.append((test_res[1] == out and test_res[2] == '', test_res[1], test_res[2]))
    return result


if __name__ == '__main__':
    from tkinter.filedialog import askopenfilename
    from pathlib import Path
    fn = askopenfilename(filetypes=[("python", "*.py")])
    if not fn:
        exit()
    print(f'Проверка {fn}')
    src = Path(fn).read_text(encoding='UTF8')
    r = check_student_code(src)
    if not r[0]:
        print('Ошибки проверки:')
        print('\n'.join(r[1]))
        exit()
    fn = askopenfilename(filetypes=[("тесты", "*.txt")])
    if not fn:
        exit()
    print('Запуск тестов')
    r = run_student_tests(src, Path(fn).read_text('UTF8'))
    print(r)
