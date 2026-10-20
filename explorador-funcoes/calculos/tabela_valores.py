import math

from .expressoes import Expressao
from .matematica import avaliar_polinomio


MAX_LINHAS = 1001


def avaliar_funcao(funcao, x):
    try:
        valor = (
            funcao.calcular(x)
            if isinstance(funcao, Expressao)
            else avaliar_polinomio(funcao, x)
        )
        valor = float(valor)
        if math.isfinite(valor):
            return 0.0 if valor == 0.0 else valor
    except (ValueError, OverflowError, ZeroDivisionError, TypeError):
        pass
    return None


def gerar_tabela(funcoes, inicio, fim, passo):
    if not all(math.isfinite(n) for n in (inicio, fim, passo)):
        raise ValueError("Use valores numéricos finitos.")
    if inicio >= fim:
        raise ValueError("O início do intervalo deve ser menor que o fim.")
    if passo <= 0:
        raise ValueError("O passo deve ser maior que zero.")
    if not funcoes:
        raise ValueError("Adicione pelo menos uma função.")

    intervalos = (fim - inicio) / passo
    if not math.isfinite(intervalos) or intervalos >= MAX_LINHAS:
        raise ValueError(
            f"O passo é muito pequeno. A tabela aceita até {MAX_LINHAS} linhas."
        )

    quantidade = int(math.floor(intervalos + 1e-12)) + 1
    quantidade = min(quantidade, MAX_LINHAS)
    linhas = []
    for indice in range(quantidade):
        x = inicio + indice * passo
        if x > fim + 1e-10 * max(1.0, abs(fim)):
            break
        if math.isclose(x, fim, rel_tol=1e-12, abs_tol=1e-12):
            x = fim
        x = 0.0 if x == 0 else x
        linhas.append((x, *(avaliar_funcao(funcao, x) for _, funcao in funcoes)))

    return linhas