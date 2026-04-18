import ast
import concurrent.futures
from typing import Any

# Nodes do AST que representam imports — ambos são perigosos
_BLOCKED_NODES = (ast.Import, ast.ImportFrom)

# Builtins que não fazem sentido num contexto de análise de dados
_BLOCKED_BUILTINS = {
    "open", "exec", "eval", "compile", "__import__",
    "breakpoint", "input", "memoryview",
}

_SAFE_BUILTINS = {
    k: v for k, v in __builtins__.items()  # type: ignore
    if k not in _BLOCKED_BUILTINS
} if isinstance(__builtins__, dict) else {
    k: getattr(__builtins__, k)
    for k in dir(__builtins__)
    if k not in _BLOCKED_BUILTINS
}


def _validate_ast(code: str) -> None:
    """
    Percorre a árvore sintática do código e rejeita qualquer import
    ou builtin perigoso antes de executar qualquer coisa.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Código com sintaxe inválida: {e}")

    for node in ast.walk(tree):
        if isinstance(node, _BLOCKED_NODES):
            raise PermissionError("Imports não são permitidos no código gerado.")


def _run_in_namespace(code: str, df: Any) -> Any:
    """
    Executa o código num namespace isolado onde o único
    símbolo disponível é o DataFrame (`df`).
    """
    namespace = {
        "__builtins__": _SAFE_BUILTINS,
        "df": df,
    }
    exec(code, namespace)  # noqa: S102

    # Convenção: o LLM deve sempre atribuir o resultado à variável `result`
    if "result" not in namespace:
        raise ValueError("O código não atribuiu nenhum valor à variável `result`.")

    return namespace["result"]


def safe_execute(code: str, df: Any, timeout_seconds: int = 5) -> Any:
    """
    Ponto de entrada público. Aplica as três camadas em sequência:
    1. Validação AST  →  rejeita imports e builtins bloqueados
    2. Timeout        →  mata execuções que demoram demais
    3. Namespace      →  limita o que o código pode enxergar
    """
    _validate_ast(code)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_run_in_namespace, code, df)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            raise TimeoutError("Execução excedeu o limite de tempo permitido.")