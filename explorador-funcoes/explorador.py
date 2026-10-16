import matplotlib.pyplot as plt


def calcular_funcao(x, a, b):
    return a * x + b


def analisar_funcao(nome, a, b):
    print(f"\n--- Análise da função {nome}(x) ---")
    print(f"Coeficiente angular: {a}")
    print(f"Coeficiente linear: {b}")

    if a > 0:
        print("Classificação: crescente")
    elif a < 0:
        print("Classificação: decrescente")
    else:
        print("Classificação: constante")

    if a != 0:
        raiz = -b / a
        print(f"Raiz: {raiz}")
    elif b == 0:
        print("Raiz: todos os números reais")
    else:
        print("Raiz: não possui")



af = float(input("Digite o coeficiente angular de f(x): "))
bf = float(input("Digite o coeficiente linear de f(x): "))

ag = float(input("Digite o coeficiente angular de g(x): "))
bg = float(input("Digite o coeficiente linear de g(x): "))

analisar_funcao("f", af, bf)
analisar_funcao("g", ag, bg)

inicio = int(input("Onde o intervalo deve começar? "))
fim = int(input("Onde o intervalo deve terminar? "))

valores_x = list(range(inicio, fim + 1))

valores_yf = []
valores_yg = []

for x in valores_x:
    valores_yf.append(calcular_funcao(x, af, bf))
    valores_yg.append(calcular_funcao(x, ag, bg))

if af != ag:
    x_intersecao = (bg - bf) / (af - ag)
    y_intersecao = calcular_funcao(x_intersecao, af, bf)

    print(f"Ponto de interseção: ({x_intersecao}, {y_intersecao})")

    if inicio <= x_intersecao <= fim:
        print("O ponto está dentro do intervalo do gráfico.")
    else:
        print("O ponto está fora do intervalo do gráfico.")

else:
    if bf == bg:
        print("As funções são coincidentes.")
    else:
        print("As funções são paralelas e não se cruzam.")

plt.plot(valores_x, valores_yf, color="red", marker="o", label="f(x)")
plt.plot(valores_x, valores_yg, color="blue", marker="o", label="g(x)")

if af != 0:
    raiz_f = -bf / af
    plt.scatter(raiz_f, 0, color="red", marker="x", s=100,
                label="Raiz de f")

if ag != 0:
    raiz_g = -bg / ag
    plt.scatter(raiz_g, 0, color="blue", marker="x", s=100,
                label="Raiz de g")


if af != 0:
    plt.annotate(
        f"({raiz_f:.2f}, 0)",
        (raiz_f, 0),
        xytext=(5, 10),
        textcoords="offset points",
        color="red"
    )

if ag != 0:
    plt.annotate(
        f"({raiz_g:.2f}, 0)",
        (raiz_g, 0),
        xytext=(5, -18),
        textcoords="offset points",
        color="blue"
    )


if af != ag and inicio <= x_intersecao <= fim:
    plt.scatter(x_intersecao, y_intersecao, color="green",
                label="Interseção", zorder=3, s = 100)
    
    plt.annotate(
    f"({x_intersecao:.2f}, {y_intersecao:.2f})",
    (x_intersecao, y_intersecao),
    textcoords="offset points",
    xytext=(8, 8),
    )

plt.axhline(y=0, color="black")
plt.axvline(x=0, color="black")

plt.title("Gráficos das funções afins")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()


texto_analise = (
    f"f(x): {'crescente' if af > 0 else 'decrescente' if af < 0 else 'constante'}\n"
    f"Raiz de f: {-bf / af if af != 0 else 'não possui raiz única'}\n\n"
    f"g(x): {'crescente' if ag > 0 else 'decrescente' if ag < 0 else 'constante'}\n"
    f"Raiz de g: {-bg / ag if ag != 0 else 'não possui raiz única'}"
)

plt.gca().text(
    0.02, 0.98,
    texto_analise,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
)

plt.show()