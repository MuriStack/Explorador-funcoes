import math

from expressoes import Expressao
from matematica import avaliar_polinomio


class CursorPrecisao:
    def __init__(self, canvas, funcoes, toolbar, status):
        self.canvas = canvas
        self.funcoes = funcoes
        self.toolbar = toolbar
        self.status = status
        self.status_base = status.get()
        self.eixo = canvas.figure.axes[0]
        self.cores = [linha.get_color() for linha in self.eixo.lines[:len(funcoes)]]
        self.ponto, = self.eixo.plot(
            [], [], marker="o", linestyle="none", markersize=9,
            markeredgecolor="#ffffff", markeredgewidth=1.5,
            zorder=12, visible=False, label="_nolegend_",
        )
        self.etiqueta = self.eixo.annotate(
            "", (0, 0), xytext=(12, 12), textcoords="offset points",
            fontsize=10, color="#eff6ff", fontweight="medium",
            bbox=dict(
                boxstyle="round,pad=0.55", facecolor="#18283e",
                edgecolor="#526d8b", alpha=0.96,
            ),
            zorder=13, visible=False, annotation_clip=False,
        )
        self.canvas.mpl_connect("motion_notify_event", self.mover)
        self.canvas.mpl_connect("figure_leave_event", self.sair)

    def ocultar(self, restaurar_status=False):
        if self.ponto.get_visible() or self.etiqueta.get_visible():
            self.ponto.set_visible(False)
            self.etiqueta.set_visible(False)
            self.canvas.draw_idle()
        if restaurar_status:
            self.status.set(self.status_base)

    def sair(self, _evento):
        self.ocultar(restaurar_status=True)

    def mover(self, evento):
        if self.toolbar is not None and self.toolbar.mode:
            self.ocultar()
            return

        if evento.inaxes is not self.eixo or evento.xdata is None or evento.ydata is None:
            self.ocultar(restaurar_status=True)
            return

        x = float(evento.xdata)
        y_mouse = float(evento.ydata)
        if not math.isfinite(x) or not math.isfinite(y_mouse):
            self.ocultar(restaurar_status=True)
            return

        melhor = None
        for indice, (nome, funcao) in enumerate(self.funcoes):
            try:
                y = (
                    funcao.calcular(x) if isinstance(funcao, Expressao)
                    else avaliar_polinomio(funcao, x)
                )
                if not math.isfinite(y):
                    continue
                px, py = self.eixo.transData.transform((x, y))
                distancia = math.hypot(px - evento.x, py - evento.y)
                if distancia <= 28 and (melhor is None or distancia < melhor[0]):
                    melhor = (distancia, nome, x, y, self.cores[indice], px, py)
            except (ValueError, OverflowError, ZeroDivisionError, TypeError):
                continue

        if melhor is None:
            self.ocultar()
            self.status.set(f"Cursor livre  •  x = {x:.6f}  •  y = {y_mouse:.6f}")
            return

        _, nome, x_ponto, y_ponto, cor, px, py = melhor
        self.ponto.set_data([x_ponto], [y_ponto])
        self.ponto.set_markerfacecolor(cor)
        self.ponto.set_visible(True)

        self.etiqueta.xy = (x_ponto, y_ponto)
        self.etiqueta.set_text(
            f"{nome}(x)\nx = {x_ponto:.6f}\ny = {y_ponto:.6f}"
        )
        limite = self.eixo.bbox
        deslocamento_x = -155 if px > limite.x1 - 165 else 12
        deslocamento_y = -73 if py > limite.y1 - 85 else 12
        self.etiqueta.set_position((deslocamento_x, deslocamento_y))
        self.etiqueta.get_bbox_patch().set_edgecolor(cor)
        self.etiqueta.set_visible(True)
        self.status.set(
            f"{nome}(x)  •  x = {x_ponto:.6f}  •  y = {y_ponto:.6f}"
        )
        self.canvas.draw_idle()