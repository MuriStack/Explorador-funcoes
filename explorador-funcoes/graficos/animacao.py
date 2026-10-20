import math
import time

from calculos.tabela_valores import avaliar_funcao


class AnimacaoCurva:
    def __init__(self, janela, canvas, nome, funcao, inicio, fim, atualizar):
        if not all(math.isfinite(valor) for valor in (inicio, fim)) or inicio >= fim:
            raise ValueError("O início do intervalo deve ser menor que o fim.")
        self.janela = janela
        self.canvas = canvas
        self.nome = nome
        self.funcao = funcao
        self.inicio = inicio
        self.fim = fim
        self.atualizar = atualizar
        self.eixo = canvas.figure.axes[0]
        self.progresso = 0.0
        self.executando = False
        self.visivel = True
        self.ativa = False
        self.pendente = None
        self.duracao = 10.0
        self.inicio_tempo = 0.0
        self.encerrada = False
        cor = next(
            (linha.get_color() for linha in self.eixo.lines if linha.get_gid() == f"curva:{nome}"),
            "#38bdf8",
        )
        self.ponto, = self.eixo.plot(
            [], [], marker="o", linestyle="None", markersize=10,
            markerfacecolor=cor, markeredgecolor="#ffffff",
            markeredgewidth=1.5, zorder=18, visible=False, label="_nolegend_",
        )
        self.etiqueta = self.eixo.annotate(
            "", (0, 0), xytext=(12, 12), textcoords="offset points",
            color="#eff6ff", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#1c2a40", edgecolor=cor, alpha=0.96),
            zorder=19, visible=False,
        )
        self.etiqueta.set_in_layout(False)

    def iniciar(self, duracao):
        if not math.isfinite(duracao) or not 1 <= duracao <= 120:
            raise ValueError("A duração deve estar entre 1 e 120 segundos.")
        if self.encerrada:
            return
        if not self.visivel:
            raise ValueError("Ative a curva e a função escolhida na aba Visual.")
        if self.executando:
            return
        self.duracao = duracao
        if self.progresso >= 1:
            self.progresso = 0.0
        self.ativa = True
        self.executando = True
        self.inicio_tempo = time.monotonic() - self.progresso * self.duracao
        self.avancar()

    def avancar(self):
        self.pendente = None
        if not self.executando or self.encerrada:
            return
        self.progresso = min(1.0, max(0.0, (time.monotonic() - self.inicio_tempo) / self.duracao))
        if self.progresso >= 1:
            self.executando = False
        self.desenhar()
        if self.executando:
            self.pendente = self.janela.after(40, self.avancar)

    def pausar(self):
        if self.executando:
            self.progresso = min(1.0, max(0.0, (time.monotonic() - self.inicio_tempo) / self.duracao))
        self.executando = False
        if self.pendente is not None:
            self.janela.after_cancel(self.pendente)
            self.pendente = None
        if not self.encerrada:
            self.desenhar()

    def reiniciar(self):
        if self.encerrada:
            return
        self.pausar()
        self.progresso = 0.0
        self.ativa = True
        self.desenhar()

    def definir_visibilidade(self, visivel):
        if visivel == self.visivel or self.encerrada:
            return
        self.visivel = visivel
        if not visivel:
            self.pausar()
        else:
            self.desenhar()

    def desenhar(self):
        x = self.fim if self.progresso >= 1 else self.inicio + (self.fim - self.inicio) * self.progresso
        y = avaliar_funcao(self.funcao, x)
        mostrar = self.ativa and self.visivel and y is not None
        self.ponto.set_visible(mostrar)
        self.etiqueta.set_visible(mostrar)
        if mostrar:
            self.ponto.set_data([x], [y])
            self.etiqueta.xy = (x, y)
            self.etiqueta.set_text(f"{self.nome}(x)\nx = {x:.6f}\ny = {y:.6f}")
            px, py = self.eixo.transData.transform((x, y))
            borda = self.eixo.bbox
            self.etiqueta.set_position((
                -155 if px > borda.x1 - 165 else 12,
                -75 if py > borda.y1 - 85 else 12,
            ))
        estado = (
            "Função oculta" if not self.visivel else
            "Em execução" if self.executando else
            "Concluída" if self.progresso >= 1 else "Pausada"
        )
        self.atualizar(estado, x, y)
        self.canvas.draw_idle()

    def encerrar(self):
        if self.encerrada:
            return
        self.encerrada = True
        self.executando = False
        if self.pendente is not None:
            self.janela.after_cancel(self.pendente)
            self.pendente = None
        self.ponto.remove()
        self.etiqueta.remove()
