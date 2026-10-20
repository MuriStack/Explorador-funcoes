import matplotlib.pyplot as plt

from matematica import (
    calcular_funcao,
    calcular_raiz,
    classificar_funcao,
    descrever_raiz,
)


def exibir_grafico(af, bf, ag, bg, inicio, fim, intersecao, mostrar=True):
    valores_x = list(range(inicio, fim + 1))

    valores_yf = [
        calcular_funcao(x, af, bf) for x in valores_x
    ]
    valores_yg = [
        calcular_funcao(x, ag, bg) for x in valores_x
    ]

    plt.figure(figsize=(10, 6))

    plt.plot(
        valores_x, valores_yf,
        color="red", marker="o", label="f(x)"
    )
    plt.plot(
        valores_x, valores_yg,
        color="blue", marker="o", label="g(x)"
    )

    for nome, a, b, cor, deslocamento in [
        ("f", af, bf, "red", (5, 10)),
        ("g", ag, bg, "blue", (5, -18)),
    ]:
        raiz = calcular_raiz(a, b)

        if raiz is not None:
            plt.scatter(
                raiz, 0,
                color=cor, marker="x", s=100,
                label=f"Raiz de {nome}"
            )

            plt.annotate(
                f"({raiz:.2f}, 0)",
                (raiz, 0),
                xytext=deslocamento,
                textcoords="offset points",
                color=cor
            )

    if intersecao is not None:
        x_intersecao, y_intersecao = intersecao

        if inicio <= x_intersecao <= fim:
            plt.scatter(
                x_intersecao, y_intersecao,
                color="green", label="Interseção",
                zorder=3, s=100
            )

            plt.annotate(
                f"({x_intersecao:.2f}, {y_intersecao:.2f})",
                (x_intersecao, y_intersecao),
                textcoords="offset points",
                xytext=(8, 8)
            )

    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")

    plt.title("Gráficos das funções afins")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()

    texto_analise = (
        f"f(x): {classificar_funcao(af)}\n"
        f"Raiz de f: {descrever_raiz(af, bf)}\n\n"
        f"g(x): {classificar_funcao(ag)}\n"
        f"Raiz de g: {descrever_raiz(ag, bg)}"
    )

    plt.gca().text(
        0.02, 0.98,
        texto_analise,
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(
            boxstyle="round",
            facecolor="white",
            alpha=0.9
        )
    )

    figura = plt.gcf()

    if mostrar:
        plt.show()

    return figura