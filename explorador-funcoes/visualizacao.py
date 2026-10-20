import matplotlib.pyplot as plt

from matematica import (
    calcular_funcao,
    calcular_raiz,
    classificar_funcao,
    descrever_raiz,
)

def exibir_grafico(
    af, bf, ag, bg, inicio, fim, intersecao,
    mostrar=True, tema_escuro=False
):
    cores = {
        "fundo": "#0b1220" if tema_escuro else "#ffffff",
        "painel": "#111c2e" if tema_escuro else "#ffffff",
        "texto": "#e8efff" if tema_escuro else "#202938",
        "grade": "#334155" if tema_escuro else "#d8dee8",
        "f": "#38bdf8" if tema_escuro else "#ef4444",
        "g": "#f472b6" if tema_escuro else "#2563eb",
        "intersecao": "#4ade80" if tema_escuro else "#16a34a",
    }

    figura, eixo = plt.subplots(figsize=(9, 6))
    figura.patch.set_facecolor(cores["fundo"])
    eixo.set_facecolor(cores["painel"])

    valores_x = list(range(inicio, fim + 1))
    valores_yf = [calcular_funcao(x, af, bf) for x in valores_x]
    valores_yg = [calcular_funcao(x, ag, bg) for x in valores_x]

    eixo.plot(
        valores_x, valores_yf, color=cores["f"],
        linewidth=2.5, label="f(x)"
    )
    eixo.plot(
        valores_x, valores_yg, color=cores["g"],
        linewidth=2.5, label="g(x)"
    )

    for nome, a, b, cor, deslocamento in [
        ("f", af, bf, cores["f"], (8, 12)),
        ("g", ag, bg, cores["g"], (8, -18)),
    ]:
        raiz = calcular_raiz(a, b)
        if raiz is not None and inicio <= raiz <= fim:
            eixo.scatter(
                raiz, 0, color=cor, marker="X", s=100,
                zorder=5, label=f"Raiz de {nome}"
            )
            eixo.annotate(
                f"({raiz:.2f}, 0)", (raiz, 0),
                xytext=deslocamento, textcoords="offset points",
                color=cor, fontsize=9
            )

    if intersecao is not None:
        x_intersecao, y_intersecao = intersecao
        if inicio <= x_intersecao <= fim:
            eixo.scatter(
                x_intersecao, y_intersecao,
                color=cores["intersecao"], s=115, zorder=6,
                label="Interseção"
            )
            eixo.annotate(
                f"({x_intersecao:.2f}, {y_intersecao:.2f})",
                (x_intersecao, y_intersecao),
                xytext=(10, 12), textcoords="offset points",
                color=cores["intersecao"], fontsize=10
            )

    eixo.axhline(0, color=cores["texto"], alpha=0.55, linewidth=1)
    eixo.axvline(0, color=cores["texto"], alpha=0.55, linewidth=1)
    eixo.set_xlim(inicio, fim)
    eixo.set_title(
        "Comparação de funções afins",
        color=cores["texto"], fontsize=14, pad=18
    )
    eixo.set_xlabel("x", color=cores["texto"])
    eixo.set_ylabel("y", color=cores["texto"])
    eixo.tick_params(colors=cores["texto"])
    for borda in eixo.spines.values():
        borda.set_color(cores["grade"])

    eixo.grid(True, color=cores["grade"], alpha=0.5, linestyle="--")
    legenda = eixo.legend(
        loc="upper right", facecolor=cores["painel"],
        edgecolor=cores["grade"], fontsize=9
    )
    for texto in legenda.get_texts():
        texto.set_color(cores["texto"])

    if not tema_escuro:
        texto_analise = (
            f"f(x): {classificar_funcao(af)}\n"
            f"Raiz de f: {descrever_raiz(af, bf)}\n\n"
            f"g(x): {classificar_funcao(ag)}\n"
            f"Raiz de g: {descrever_raiz(ag, bg)}"
        )
        eixo.text(
            0.02, 0.98, texto_analise,
            transform=eixo.transAxes, va="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.9)
        )

    figura.tight_layout()

    if mostrar:
        plt.show()

    return figura