import math

import matplotlib.pyplot as plt

from calculos.expressoes import Expressao
from calculos.matematica import (
    avaliar_polinomio,
    calcular_intersecoes_polinomios,
    raizes_reais,
    vertice,
)


def identificar(artista, categoria, nome=None):
    artista.set_gid(f"{categoria}:{nome}" if nome else categoria)
    return artista


def desenhar_funcoes(
    funcoes, inicio, fim,
    intersecoes=None, par_intersecoes=("f", "g"), raizes=None, extremos=None,
):
    cores = {
        "fundo": "#0b1220",
        "painel": "#111c2e",
        "texto": "#e8efff",
        "grade": "#334155",
        "f": "#38bdf8",
        "g": "#f472b6",
        "h": "#fbbf24",
        "i": "#a78bfa",
        "j": "#2dd4bf",
        "intersecao": "#4ade80",
        "vertice": "#fbbf24",
    }

    figura, eixo = plt.subplots(figsize=(9, 6))
    figura.patch.set_facecolor(cores["fundo"])
    eixo.set_facecolor(cores["painel"])
    xs = [inicio + (fim - inicio) * indice / 400 for indice in range(401)]

    for nome, funcao in funcoes:
        cor = cores[nome]
        polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
        ys = [
            funcao.calcular(x) if isinstance(funcao, Expressao)
            else avaliar_polinomio(funcao, x)
            for x in xs
        ]
        if not any(math.isfinite(y) for y in ys):
            plt.close(figura)
            raise ValueError(f"A função {nome}(x) não possui valores reais no intervalo escolhido.")
        identificar(
            eixo.plot(xs, ys, color=cor, linewidth=2.5, label=f"{nome}(x)")[0],
            "curva", nome,
        )

        lista_raizes = (
            raizes[nome][1] if raizes is not None
            else raizes_reais(polinomio) if polinomio is not None else []
        )
        raizes_visiveis = [raiz for raiz in lista_raizes if inicio <= raiz <= fim]
        for indice, raiz in enumerate(raizes_visiveis):
            identificar(eixo.scatter(
                raiz, 0, color=cor, marker="X", s=100, zorder=5,
                label=f"Raiz de {nome}" if indice == 0 else None,
            ), "raiz", nome)
            if len(raizes_visiveis) <= 6:
                identificar(eixo.annotate(
                    f"({raiz:.4f}, 0)", (raiz, 0),
                    xytext=(9, 12), textcoords="offset points",
                    color=cor, fontsize=9,
                ), "raiz", nome)

        ponto_vertice = vertice(polinomio) if polinomio is not None else None
        if ponto_vertice is not None:
            vx, vy = ponto_vertice
            if inicio <= vx <= fim:
                identificar(eixo.scatter(
                    vx, vy, color=cores["vertice"], marker="D", s=85,
                    zorder=6, label=f"Vértice de {nome}",
                ), "vertice", nome)
                identificar(eixo.annotate(
                    f"V ({vx:.2f}, {vy:.2f})", (vx, vy),
                    xytext=(10, -22), textcoords="offset points",
                    color=cores["vertice"], fontsize=9,
                ), "vertice", nome)

    if extremos:
        for nome, _ in funcoes:
            pontos = extremos.get(nome, [])
            for indice, (tipo, x, y) in enumerate(pontos):
                cor = "#fb7185" if tipo == "maximo" else "#c084fc"
                titulo = "Máximo" if tipo == "maximo" else "Mínimo"
                marcador = "^" if tipo == "maximo" else "v"
                identificar(eixo.scatter(
                    x, y, color=cor, marker=marcador, s=125,
                    edgecolor=cores["painel"], linewidth=1.3, zorder=9,
                    label=f"{titulo} de {nome}(x)" if indice == 0 or not any(
                        anterior[0] == tipo for anterior in pontos[:indice]
                    ) else None,
                ), "extremo", nome)
                if len(pontos) <= 3:
                    identificar(eixo.annotate(
                        f"{titulo}: ({x:.3f}, {y:.3f})", (x, y),
                        xytext=(9, 19), textcoords="offset points",
                        color=cor, fontsize=9,
                    ), "extremo", nome)

    if intersecoes is None and len(funcoes) >= 2:
        polinomios = [
            funcao.polinomio if isinstance(funcao, Expressao) else funcao
            for _, funcao in funcoes[:2]
        ]
        if all(p is not None for p in polinomios):
            intersecoes = calcular_intersecoes_polinomios(*polinomios)

    if intersecoes is not None and intersecoes[0] == "pontos":
        pontos = [
            (x, y) for x, y in intersecoes[1]
            if inicio <= x <= fim and math.isfinite(x) and math.isfinite(y)
        ]
        for indice, (x, y) in enumerate(pontos):
            identificar(eixo.scatter(
                x, y, color=cores["intersecao"], s=100,
                zorder=7,
                label=(
                    f"Interseção {par_intersecoes[0]}/{par_intersecoes[1]}"
                    if indice == 0 else None
                ),
            ), "intersecao")
            if len(pontos) <= 6:
                identificar(eixo.annotate(
                    f"({x:.4f}, {y:.4f})", (x, y),
                    xytext=(10, 12), textcoords="offset points",
                    color=cores["intersecao"], fontsize=9,
                ), "intersecao")

    eixo.axhline(0, color=cores["texto"], alpha=0.55, linewidth=1)
    eixo.axvline(0, color=cores["texto"], alpha=0.55, linewidth=1)
    eixo.set_xlim(inicio, fim)
    titulo = (
        f"Comparação de {len(funcoes)} funções"
        if len(funcoes) > 1 else "Análise de função"
    )
    eixo.set_title(titulo, color=cores["texto"], fontsize=14, pad=18)
    eixo.set_xlabel("x", color=cores["texto"])
    eixo.set_ylabel("y", color=cores["texto"])
    eixo.tick_params(colors=cores["texto"])
    for borda in eixo.spines.values():
        borda.set_color(cores["grade"])
    eixo.grid(True, color=cores["grade"], alpha=0.5, linestyle="--")
    handles, labels = eixo.get_legend_handles_labels()
    unicos = {}
    for handle, label in zip(handles, labels):
        unicos.setdefault(label, handle)
    legenda = eixo.legend(unicos.values(), unicos.keys(),
                          loc="upper right", facecolor=cores["painel"],
                          edgecolor=cores["grade"], fontsize=9)
    for texto in legenda.get_texts():
        texto.set_color(cores["texto"])

    figura.tight_layout()
    return figura
