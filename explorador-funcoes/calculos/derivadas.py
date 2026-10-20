import math

from .expressoes import Expressao
from .matematica import avaliar_polinomio


def calcular_tangente(funcao, x):
    if not math.isfinite(x):
        raise ValueError("Informe um valor finito de x.")

    polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
    if polinomio is not None:
        a, b, _ = polinomio
        y = avaliar_polinomio(polinomio, x)
        inclinacao = 2 * a * x + b
        if not math.isfinite(y) or not math.isfinite(inclinacao):
            raise ValueError("O resultado é grande demais para ser representado.")
        return y, inclinacao

    y = funcao.calcular(x)
    if not math.isfinite(y):
        raise ValueError("A função não está definida no ponto escolhido.")

    escala = max(1.0, abs(x))
    estimativas = []
    for divisor in (1.0, 4.0, 16.0, 64.0):
        h = 0.001 * escala / divisor
        if x - h == x or x + h == x:
            continue
        esquerda = funcao.calcular(x - h)
        direita = funcao.calcular(x + h)
        if not all(math.isfinite(v) for v in (esquerda, direita)):
            continue
        inclinacao_esquerda = (y - esquerda) / h
        inclinacao_direita = (direita - y) / h
        media = (inclinacao_esquerda + inclinacao_direita) / 2
        if not all(math.isfinite(v) for v in (
            inclinacao_esquerda, inclinacao_direita, media,
        )):
            continue
        estimativas.append((inclinacao_esquerda, inclinacao_direita, media))

    if len(estimativas) < 2:
        raise ValueError(
            "Não foi possível determinar a derivada neste ponto. "
            "Ele pode estar na borda do domínio da função."
        )

    esquerda, direita, inclinacao = estimativas[-1]
    tolerancia = 0.002 + 0.005 * abs(inclinacao)
    if abs(esquerda - direita) > tolerancia:
        raise ValueError(
            "A derivada não está definida neste ponto: "
            "as inclinações dos dois lados são diferentes."
        )

    anterior = estimativas[-2][2]
    if abs(inclinacao - anterior) > 0.004 + 0.01 * abs(inclinacao):
        raise ValueError(
            "A inclinação não se estabilizou perto deste ponto. "
            "Tente outro valor de x."
        )

    return y, inclinacao