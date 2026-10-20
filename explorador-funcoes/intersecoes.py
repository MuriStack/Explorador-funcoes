import math

from expressoes import Expressao
from matematica import avaliar_polinomio, calcular_intersecoes_polinomios


def avaliar(funcao, x):
    if isinstance(funcao, Expressao):
        return funcao.calcular(x)
    return avaliar_polinomio(funcao, x)


def diferenca(primeira, segunda, x):
    try:
        y1 = avaliar(primeira, x)
        y2 = avaliar(segunda, x)
        if not math.isfinite(y1) or not math.isfinite(y2):
            return None
        delta = y1 - y2
        if not math.isfinite(delta):
            return None
        return delta
    except (ArithmeticError, ValueError, TypeError, OverflowError):
        return None


def conferir_ponto(primeira, segunda, x):
    try:
        y1 = avaliar(primeira, x)
        y2 = avaliar(segunda, x)
        if not all(math.isfinite(v) for v in (x, y1, y2)):
            return None
        if not math.isclose(y1, y2, rel_tol=1e-9, abs_tol=1e-10):
            return None
        return x, (y1 + y2) / 2
    except (ArithmeticError, ValueError, TypeError, OverflowError):
        return None


def bissecao(primeira, segunda, a, b, fa, fb):
    for _ in range(85):
        meio = (a + b) / 2
        if meio == a or meio == b:
            break
        fm = diferenca(primeira, segunda, meio)
        if fm is None:
            return None
        if fm == 0:
            return meio
        if (fa < 0 < fm) or (fa > 0 > fm):
            b, fb = meio, fm
        else:
            a, fa = meio, fm
    return (a + b) / 2


def minimo_local(primeira, segunda, esquerda, direita):
    proporcao = (math.sqrt(5) - 1) / 2

    def erro(x):
        valor = diferenca(primeira, segunda, x)
        return abs(valor) if valor is not None else math.inf

    c = direita - proporcao * (direita - esquerda)
    d = esquerda + proporcao * (direita - esquerda)
    fc, fd = erro(c), erro(d)
    for _ in range(80):
        if abs(direita - esquerda) <= 1e-12 * max(1.0, abs(c), abs(d)):
            break
        if fc <= fd:
            direita, d, fd = d, c, fc
            c = direita - proporcao * (direita - esquerda)
            fc = erro(c)
        else:
            esquerda, c, fc = c, d, fd
            d = esquerda + proporcao * (direita - esquerda)
            fd = erro(d)
    return c if fc <= fd else d


def encontrar_intersecoes(primeira, segunda, inicio, fim):
    if not all(math.isfinite(n) for n in (inicio, fim)) or inicio >= fim:
        raise ValueError("O intervalo deve ter início menor que o fim.")

    p1 = primeira.polinomio if isinstance(primeira, Expressao) else primeira
    p2 = segunda.polinomio if isinstance(segunda, Expressao) else segunda
    if p1 is not None and p2 is not None:
        situacao, pontos = calcular_intersecoes_polinomios(p1, p2)
        if situacao == "coincidentes":
            return "coincidentes", []
        confirmados = []
        for x, _ in pontos:
            if inicio <= x <= fim:
                ponto = conferir_ponto(primeira, segunda, x)
                if ponto is not None:
                    confirmados.append(ponto)
        return ("pontos", confirmados) if confirmados else ("sem_intersecao", [])

    quantidade = min(5000, max(1400, int(240 * (fim - inicio))))
    passo = (fim - inicio) / quantidade
    xs = [inicio + passo * i for i in range(quantidade + 1)]
    valores = [diferenca(primeira, segunda, x) for x in xs]

    amostra = [valores[int(i * quantidade / 40)] for i in range(41)]
    amostra.extend(
        diferenca(primeira, segunda, inicio + (fim - inicio) * fracao)
        for fracao in (0.07123, 0.21753, 0.43175, 0.68293, 0.89173)
    )
    validos = [valor for valor in amostra if valor is not None]
    if len(validos) >= 4 and all(abs(valor) <= 1e-11 for valor in validos):
        return "coincidentes", []

    candidatos = []
    for i, valor in enumerate(valores):
        if valor is None:
            continue
        if valor == 0:
            candidatos.append(xs[i])
        if i > 0 and valores[i - 1] is not None:
            anterior = valores[i - 1]
            if (anterior < 0 < valor) or (anterior > 0 > valor):
                candidatos.append(bissecao(primeira, segunda, xs[i - 1], xs[i], anterior, valor))
        if 0 < i < quantidade:
            anterior, posterior = valores[i - 1], valores[i + 1]
            if anterior is not None and posterior is not None:
                if abs(valor) <= abs(anterior) and abs(valor) <= abs(posterior):
                    candidatos.append(
                        minimo_local(primeira, segunda, xs[i - 1], xs[i + 1])
                    )

    confirmados = []
    tolerancia_x = max(1e-8, passo * 0.001)
    for candidato in sorted(x for x in candidatos if x is not None):
        if not inicio <= candidato <= fim:
            continue
        ponto = conferir_ponto(primeira, segunda, candidato)
        if ponto is not None and all(abs(ponto[0] - p[0]) > tolerancia_x for p in confirmados):
            confirmados.append(ponto)
        if len(confirmados) == 60:
            break

    return ("pontos", confirmados) if confirmados else ("sem_intersecao", [])