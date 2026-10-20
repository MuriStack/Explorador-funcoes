import math


def calcular_funcao(x, a, b):
    return a * x + b


def classificar_funcao(a):
    if a > 0:
        return "crescente"
    if a < 0:
        return "decrescente"
    return "constante"


def calcular_raiz(a, b):
    if a == 0:
        return None
    raiz = -b / a
    return 0.0 if raiz == 0 else raiz


def descrever_raiz(a, b):
    if a == 0:
        return "todos os números reais" if b == 0 else "não possui"
    return str(calcular_raiz(a, b))


def calcular_intersecao(af, bf, ag, bg):
    if af == ag:
        if bf == bg:
            return "coincidentes", None
        return "paralelas", None
    x = (bg - bf) / (af - ag)
    y = calcular_funcao(x, af, bf)
    return "intersecao", (x, y)


def analisar_funcao(nome, a, b):
    print(f"\n--- Análise da função {nome}(x) ---")
    print(f"Coeficiente angular: {a}")
    print(f"Coeficiente linear: {b}")
    print(f"Classificação: {classificar_funcao(a)}")
    print(f"Raiz: {descrever_raiz(a, b)}")


def criar_polinomio(tipo, a, b, c=0.0):
    if tipo == "Afim":
        return (0.0, a, b)
    if tipo == "Quadrática":
        if a == 0:
            raise ValueError("Em uma função quadrática, o coeficiente a deve ser diferente de zero.")
        return (a, b, c)
    raise ValueError("Tipo de função inválido.")


def avaliar_polinomio(polinomio, x):
    a, b, c = polinomio
    return (a * x + b) * x + c


def raizes_reais(polinomio):
    a, b, c = polinomio
    if a == 0:
        if b == 0:
            return []
        return [-c / b]

    delta = b * b - 4 * a * c
    if delta < 0:
        return []
    if math.isclose(delta, 0.0, rel_tol=1e-12, abs_tol=1e-12):
        return [-b / (2 * a)]
    raiz_delta = math.sqrt(delta)
    return sorted([(-b - raiz_delta) / (2 * a), (-b + raiz_delta) / (2 * a)])


def discriminante(polinomio):
    a, b, c = polinomio
    if a == 0:
        return None
    return b * b - 4 * a * c


def vertice(polinomio):
    a, b, c = polinomio
    if a == 0:
        return None
    x = -b / (2 * a)
    return (x, avaliar_polinomio(polinomio, x))


def descrever_raizes_polinomio(polinomio):
    a, b, c = polinomio
    if a == 0 and b == 0:
        return "todos os reais" if c == 0 else "não possui"
    raizes = raizes_reais(polinomio)
    if not raizes:
        return "sem raízes reais"
    return ", ".join(f"{0.0 if x == 0 else x:.3f}" for x in raizes)


def descrever_comportamento(polinomio):
    a, b, _ = polinomio
    if a != 0:
        return "Concavidade para cima" if a > 0 else "Concavidade para baixo"
    return classificar_funcao(b).capitalize()


def calcular_intersecoes_polinomios(primeiro, segundo):
    diferenca = tuple(x - y for x, y in zip(primeiro, segundo))
    if diferenca == (0.0, 0.0, 0.0):
        return "coincidentes", []
    a, b, c = diferenca
    if a == 0 and b == 0:
        return "sem_intersecao", []
    xs = raizes_reais(diferenca)
    pontos = [(x, avaliar_polinomio(primeiro, x)) for x in xs]
    return ("pontos", pontos) if pontos else ("sem_intersecao", [])