import math

import matplotlib.pyplot as plt

from expressoes import Expressao
from matematica import (
    avaliar_polinomio,
    calcular_intersecoes_polinomios,
    descrever_raizes_polinomio,
    descrever_comportamento,
    raizes_reais,
    vertice,
)


def desenhar_funcoes(
    funcoes, inicio, fim, mostrar=False, tema_escuro=True,
    intersecoes=None, par_intersecoes=("f", "g"), raizes=None,
):
    cores = {
        "fundo": "#0b1220" if tema_escuro else "#ffffff",
        "painel": "#111c2e" if tema_escuro else "#ffffff",
        "texto": "#e8efff" if tema_escuro else "#202938",
        "grade": "#334155" if tema_escuro else "#d8dee8",
        "f": "#38bdf8" if tema_escuro else "#ef4444",
        "g": "#f472b6" if tema_escuro else "#2563eb",
        "h": "#fbbf24" if tema_escuro else "#d97706",
        "i": "#a78bfa" if tema_escuro else "#7c3aed",
        "j": "#2dd4bf" if tema_escuro else "#0d9488",
        "intersecao": "#4ade80" if tema_escuro else "#16a34a",
        "vertice": "#fbbf24" if tema_escuro else "#ca8a04",
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
        eixo.plot(xs, ys, color=cor, linewidth=2.5, label=f"{nome}(x)")

        lista_raizes = (
            raizes[nome][1] if raizes is not None
            else raizes_reais(polinomio) if polinomio is not None else []
        )
        raizes_visiveis = [raiz for raiz in lista_raizes if inicio <= raiz <= fim]
        for indice, raiz in enumerate(raizes_visiveis):
            eixo.scatter(
                raiz, 0, color=cor, marker="X", s=100, zorder=5,
                label=f"Raiz de {nome}" if indice == 0 else None,
            )
            if len(raizes_visiveis) <= 6:
                eixo.annotate(
                    f"({raiz:.4f}, 0)", (raiz, 0),
                    xytext=(9, 12), textcoords="offset points",
                    color=cor, fontsize=9,
                )

        ponto_vertice = vertice(polinomio) if polinomio is not None else None
        if ponto_vertice is not None:
            vx, vy = ponto_vertice
            if inicio <= vx <= fim:
                eixo.scatter(vx, vy, color=cores["vertice"], marker="D",
                             s=85, zorder=6, label=f"Vértice de {nome}")
                eixo.annotate(f"V ({vx:.2f}, {vy:.2f})", (vx, vy),
                              xytext=(10, -22), textcoords="offset points",
                              color=cores["vertice"], fontsize=9)

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
            eixo.scatter(
                x, y, color=cores["intersecao"], s=100,
                zorder=7,
                label=(
                    f"Interseção {par_intersecoes[0]}/{par_intersecoes[1]}"
                    if indice == 0 else None
                ),
            )
            if len(pontos) <= 6:
                eixo.annotate(
                    f"({x:.4f}, {y:.4f})", (x, y),
                    xytext=(10, 12), textcoords="offset points",
                    color=cores["intersecao"], fontsize=9,
                )

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

    if not tema_escuro:
        linhas = []
        for nome, funcao in funcoes:
            polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
            if polinomio is None:
                linhas.extend([f"{nome}(x): {funcao.texto}", ""])
            else:
                linhas.extend([
                    f"{nome}(x): {descrever_comportamento(polinomio)}",
                    f"Raízes: {descrever_raizes_polinomio(polinomio)}",
                    "",
                ])
        eixo.text(0.02, 0.98, "\n".join(linhas).strip(),
                  transform=eixo.transAxes, va="top",
                  bbox=dict(boxstyle="round", facecolor="white", alpha=0.9))

    figura.tight_layout()
    if mostrar:
        plt.show()
    return figura


def exibir_grafico(
    af, bf, ag, bg, inicio, fim, intersecao,
    mostrar=True, tema_escuro=False, exibir_g=True,
):
    funcoes = [("f", (0.0, af, bf))]
    if exibir_g:
        funcoes.append(("g", (0.0, ag, bg)))
    return desenhar_funcoes(funcoes, inicio, fim,
                           mostrar=mostrar, tema_escuro=tema_escuro)