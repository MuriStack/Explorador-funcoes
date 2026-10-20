import ast
import math
import operator


FUNCOES = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log,
    "ln": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
}

CONSTANTES = {"pi": math.pi, "e": math.e}
OPERACOES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


class Expressao:
    def __init__(self, texto):
        self.texto = texto.strip()
        if not self.texto or len(self.texto) > 160:
            raise ValueError("Digite uma expressão com até 160 caracteres.")
        try:
            arvore = ast.parse(self.texto.replace("^", "**"), mode="eval")
        except SyntaxError as erro:
            raise ValueError("Expressão inválida. Use, por exemplo, sin(x) ou x^2 - 4*x + 3.") from erro
        if sum(1 for _ in ast.walk(arvore)) > 90:
            raise ValueError("A expressão é muito complexa.")
        self.no = arvore.body
        self._validar(self.no)
        self.polinomio = self._extrair_polinomio(self.no)

    def _validar(self, no):
        if isinstance(no, ast.Constant) and type(no.value) in (int, float):
            if not math.isfinite(no.value) or abs(no.value) > 1_000_000:
                raise ValueError("Use constantes numéricas menores que um milhão.")
            return
        if isinstance(no, ast.Name) and no.id in ("x", *CONSTANTES):
            return
        if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
            self._validar(no.operand)
            return
        if isinstance(no, ast.BinOp) and type(no.op) in OPERACOES:
            self._validar(no.left)
            self._validar(no.right)
            return
        if (
            isinstance(no, ast.Call)
            and isinstance(no.func, ast.Name)
            and no.func.id in FUNCOES
            and len(no.args) == 1
            and not no.keywords
        ):
            self._validar(no.args[0])
            return
        raise ValueError("Expressão não permitida. Use x, operações e funções como sin, cos, sqrt e log.")

    def _avaliar(self, no, x):
        if isinstance(no, ast.Constant):
            return float(no.value)
        if isinstance(no, ast.Name):
            return x if no.id == "x" else CONSTANTES[no.id]
        if isinstance(no, ast.UnaryOp):
            valor = self._avaliar(no.operand, x)
            return -valor if isinstance(no.op, ast.USub) else valor
        if isinstance(no, ast.BinOp):
            esquerda = self._avaliar(no.left, x)
            direita = self._avaliar(no.right, x)
            if isinstance(no.op, ast.Pow) and abs(direita) > 32:
                return math.nan
            return OPERACOES[type(no.op)](esquerda, direita)
        return FUNCOES[no.func.id](self._avaliar(no.args[0], x))

    def calcular(self, x):
        try:
            valor = self._avaliar(self.no, x)
            return float(valor) if math.isfinite(valor) else math.nan
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            return math.nan

    def _extrair_polinomio(self, no):
        if isinstance(no, ast.Constant):
            return (0.0, 0.0, float(no.value))
        if isinstance(no, ast.Name):
            if no.id == "x":
                return (0.0, 1.0, 0.0)
            return (0.0, 0.0, CONSTANTES[no.id])
        if isinstance(no, ast.UnaryOp):
            p = self._extrair_polinomio(no.operand)
            if p is None:
                return None
            return tuple(-n for n in p) if isinstance(no.op, ast.USub) else p
        if not isinstance(no, ast.BinOp):
            return None
        esquerda = self._extrair_polinomio(no.left)
        direita = self._extrair_polinomio(no.right)
        if esquerda is None or direita is None:
            return None
        if isinstance(no.op, (ast.Add, ast.Sub)):
            sinal = 1 if isinstance(no.op, ast.Add) else -1
            return tuple(a + sinal * b for a, b in zip(esquerda, direita))
        if isinstance(no.op, ast.Mult):
            coeficientes = [0.0] * 5
            for i, a in enumerate(reversed(esquerda)):
                for j, b in enumerate(reversed(direita)):
                    coeficientes[i + j] += a * b
            if any(coeficientes[3:]):
                return None
            return tuple(reversed(coeficientes[:3]))
        if isinstance(no.op, ast.Div) and direita[:2] == (0.0, 0.0) and direita[2] != 0:
            return tuple(a / direita[2] for a in esquerda)
        if isinstance(no.op, ast.Pow) and direita[:2] == (0.0, 0.0):
            expoente = direita[2]
            if expoente in (0, 1, 2):
                if expoente == 0:
                    return (0.0, 0.0, 1.0)
                if expoente == 1:
                    return esquerda
                a, b, c = esquerda
                if a != 0:
                    return None
                return (b * b, 2 * b * c, c * c)
        return None