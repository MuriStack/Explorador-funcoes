import math

from expressoes import Expressao
from matematica import avaliar_polinomio, vertice


def avaliar(funcao, x):
    try:
        valor = (
            funcao.calcular(x) if isinstance(funcao, Expressao)
            else avaliar_polinomio(funcao, x)
        )
        return valor if math.isfinite(valor) else None
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return None


def refinar_extremo(funcao, esquerda, direita, tipo):
    razao = (math.sqrt(5) - 1) / 2
    sinal = 1 if tipo == "minimo" else -1

    def custo(x):
        valor = avaliar(funcao, x)
        return sinal * valor if valor is not None else math.inf

    c = direita - razao * (direita - esquerda)
    d = esquerda + razao * (direita - esquerda)
    fc, fd = custo(c), custo(d)
    for _ in range(85):
        if direita - esquerda <= 2e-12 * max(1, abs(c), abs(d)):
            break
        if fc <= fd:
            direita, d, fd = d, c, fc
            c = direita - razao * (direita - esquerda)
            fc = custo(c)
        else:
            esquerda, c, fc = c, d, fd
            d = esquerda + razao * (direita - esquerda)
            fd = custo(d)
    return c if fc <= fd else d


def confirmar_extremo(funcao, x, tipo, passo, inicio, fim):
    if not inicio < x < fim:
        return None
    y = avaliar(funcao, x)
    if y is None:
        return None

    sinal = 1 if tipo == "minimo" else -1
    diferencas = []
    for fator in (0.12, 0.4):
        h = passo * fator
        if not inicio < x - h < x + h < fim:
            return None
        esquerda, direita = avaliar(funcao, x - h), avaliar(funcao, x + h)
        if esquerda is None or direita is None:
            return None
        delta_esq = sinal * (esquerda - y)
        delta_dir = sinal * (direita - y)
        escala = max(1.0, abs(y), abs(esquerda), abs(direita))
        if delta_esq < -1e-11 * escala or delta_dir < -1e-11 * escala:
            return None
        diferencas.append((delta_esq, delta_dir))

    if min(diferencas[-1]) <= 1e-12 * max(1.0, abs(y)):
        return None
    return (tipo, x, y)


def encontrar_extremos(funcao, inicio, fim):
    if not all(math.isfinite(numero) for numero in (inicio, fim)) or inicio >= fim:
        raise ValueError("O início do intervalo deve ser menor que o fim.")

    polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
    if polinomio is not None:
        a, _, _ = polinomio
        ponto = vertice(polinomio)
        if a == 0 or ponto is None or not inicio < ponto[0] < fim:
            return []
        if not all(math.isfinite(valor) for valor in ponto):
            return []
        return [("minimo" if a > 0 else "maximo", *ponto)]

    quantidade = min(3600, max(900, int(125 * (fim - inicio))))
    passo = (fim - inicio) / quantidade
    xs = [inicio + passo * indice for indice in range(quantidade + 1)]
    valores = [avaliar(funcao, x) for x in xs]
    encontrados = []

    for indice in range(1, quantidade):
        anterior, atual, proximo = valores[indice - 1:indice + 2]
        if any(valor is None for valor in (anterior, atual, proximo)):
            continue
        if atual < anterior and atual < proximo:
            tipo = "minimo"
        elif atual > anterior and atual > proximo:
            tipo = "maximo"
        else:
            continue

        esquerda, direita = xs[indice - 1], xs[indice + 1]
        x = refinar_extremo(funcao, esquerda, direita, tipo)
        valor_refinado = avaliar(funcao, x)
        if valor_refinado is None or abs(valor_refinado) > 100 * max(1.0, abs(anterior), abs(atual), abs(proximo)):
            continue
        if min(x - esquerda, direita - x) < passo * 0.005:
            continue
        ponto = confirmar_extremo(funcao, x, tipo, passo, inicio, fim)
        if ponto is None:
            continue
        if any(abs(x - outro[1]) < passo * 0.15 for outro in encontrados):
            continue
        encontrados.append(ponto)
        if len(encontrados) >= 60:
            break

    return encontrados