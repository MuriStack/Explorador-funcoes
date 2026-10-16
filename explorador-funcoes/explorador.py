import matplotlib.pyplot as plt


def calcular_funcao(x, a, b):
    return a * x + b


af = float(input("Digite o coeficiente angular de f(x): "))
bf = float(input("Digite o coeficiente linear de f(x): "))

ag = float(input("Digite o coeficiente angular de g(x): "))
bg = float(input("Digite o coeficiente linear de g(x): "))

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

plt.show()