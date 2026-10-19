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
