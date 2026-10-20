import math

from expressoes import Expressao
from matematica import avaliar_polinomio, raizes_reais


def avaliar_integrando(funcao, x):
    try:
        valor = (
            funcao.calcular(x) if isinstance(funcao, Expressao)
            else avaliar_polinomio(funcao, x)
        )
        if math.isfinite(valor):
            return valor
    except (ArithmeticError, ValueError, TypeError):
        pass
    raise ValueError(
        "A função deve ter valores reais finitos em todo o intervalo. "
        "Integrais impróprias não são suportadas."
    )


def calcular_integral(funcao, inicio, fim):
    if not all(math.isfinite(valor) for valor in (inicio, fim)) or inicio >= fim:
        raise ValueError("Use limites finitos, com início menor que fim.")
    if not math.isfinite(fim - inicio):
        raise ValueError("O intervalo é grande demais para o cálculo.")

    polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
    if polinomio is not None:
        limites = [inicio, *(x for x in raizes_reais(polinomio) if inicio < x < fim), fim]
        parcelas = []
        for esquerda, direita in zip(limites, limites[1:]):
            meio = esquerda + (direita - esquerda) / 2
            valores = [avaliar_integrando(funcao, x) for x in (esquerda, meio, direita)]
            parcelas.append((direita - esquerda) * (valores[0] / 6 + 2 * valores[1] / 3 + valores[2] / 6))
        integral = math.fsum(parcelas)
        area = math.fsum(abs(valor) for valor in parcelas)
    else:
        cache = {}

        def avaliar(x):
            if x not in cache:
                if len(cache) >= 100_000:
                    raise ValueError("O cálculo excedeu o limite de avaliações. Reduza o intervalo.")
                cache[x] = avaliar_integrando(funcao, x)
            return cache[x]

        def simpson(esquerda, direita, valores):
            largura = (direita - esquerda) / 6
            a, m, b = valores
            return (
                largura * (a + 4 * m + b),
                largura * (abs(a) + 4 * abs(m) + abs(b)),
            )

        def refinar(esquerda, direita, valores, anterior, tolerancia, profundidade):
            meio = esquerda + (direita - esquerda) / 2
            quarto = esquerda + (meio - esquerda) / 2
            tres_quartos = meio + (direita - meio) / 2
            if not esquerda < quarto < meio < tres_quartos < direita:
                raise ValueError("Não foi possível atingir a precisão numérica neste intervalo.")
            a, m, b = valores
            valores_esquerda = (a, avaliar(quarto), m)
            valores_direita = (m, avaliar(tres_quartos), b)
            primeira = simpson(esquerda, meio, valores_esquerda)
            segunda = simpson(meio, direita, valores_direita)
            soma = tuple(x + y for x, y in zip(primeira, segunda))
            erros = tuple(novo - velho for novo, velho in zip(soma, anterior))
            if not all(math.isfinite(valor) for valor in (*soma, *erros)):
                raise ValueError("O resultado é grande demais para ser representado.")
            if all(abs(erro) <= 15 * tolerancia for erro in erros):
                return tuple(valor + erro / 15 for valor, erro in zip(soma, erros))
            if profundidade == 0:
                raise ValueError(
                    "O cálculo não convergiu. A função pode ter uma descontinuidade "
                    "ou variar muito rapidamente. Escolha um intervalo contínuo menor."
                )
            esquerda_refinada = refinar(
                esquerda, meio, valores_esquerda, primeira, tolerancia / 2, profundidade - 1,
            )
            direita_refinada = refinar(
                meio, direita, valores_direita, segunda, tolerancia / 2, profundidade - 1,
            )
            return tuple(x + y for x, y in zip(esquerda_refinada, direita_refinada))

        intervalos = []
        limites = [inicio]
        limites.extend(
            inicio + (fim - inicio) * (indice + 0.2 * math.sin(indice * math.sqrt(2))) / 32
            for indice in range(1, 32)
        )
        limites.append(fim)
        for indice in range(32):
            esquerda, direita = limites[indice:indice + 2]
            meio = esquerda + (direita - esquerda) / 2
            valores = tuple(avaliar(x) for x in (esquerda, meio, direita))
            intervalos.append((esquerda, direita, valores, simpson(esquerda, direita, valores)))
        escala = math.fsum(abs(item[3][1]) for item in intervalos)
        tolerancia = max(1e-9, 1e-9 * escala) / 32
        resultados = [refinar(*item, tolerancia, 45) for item in intervalos]
        integral = math.fsum(item[0] for item in resultados)
        area = math.fsum(item[1] for item in resultados)

    if not all(math.isfinite(valor) for valor in (integral, area)):
        raise ValueError("O resultado é grande demais para ser representado.")
    return integral, max(abs(integral), area)
