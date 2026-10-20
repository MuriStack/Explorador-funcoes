import math
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from derivadas import calcular_tangente
from extremos import encontrar_extremos
from expressoes import Expressao
from matematica import (
    criar_polinomio,
    descrever_comportamento,
    descrever_raizes_polinomio,
    discriminante,
    raizes_reais,
    vertice,
)
from intersecoes import encontrar_intersecoes, encontrar_raizes
from visualizacao import desenhar_funcoes


FUNDO = "#080f1e"
PAINEL = "#111c2e"
CAMPO = "#1c2a40"
TEXTO = "#eff6ff"
SUAVE = "#9fb0c9"
DESTAQUE = "#38bdf8"
BORDA = "#293b54"


def pontos_arredondados(x1, y1, x2, y2, raio):
    raio = max(0, min(raio, (x2 - x1) / 2, (y2 - y1) / 2))
    pontos = []
    for centro_x, centro_y, angulo_inicial in (
        (x2 - raio, y1 + raio, -90),
        (x2 - raio, y2 - raio, 0),
        (x1 + raio, y2 - raio, 90),
        (x1 + raio, y1 + raio, 180),
    ):
        for passo in range(9):
            angulo = math.radians(angulo_inicial + passo * 90 / 8)
            pontos.extend((
                centro_x + raio * math.cos(angulo),
                centro_y + raio * math.sin(angulo),
            ))
    return pontos


class CartaoArredondado(tk.Canvas):
    def __init__(self, parent, largura=None, raio=22, margem=18):
        super().__init__(
            parent, bg=FUNDO, highlightthickness=0,
            bd=0, width=largura or 500,
        )
        self.raio = raio
        self.margem = margem
        self.borda = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1,
            fill=PAINEL, outline=BORDA, width=1,
        )
        self.conteudo = tk.Frame(self, bg=PAINEL)
        self.janela_interna = self.create_window(
            margem, margem, anchor="nw", window=self.conteudo,
        )
        self.bind("<Configure>", self.ajustar)

    def ajustar(self, evento):
        largura = max(1, evento.width)
        altura = max(1, evento.height)
        self.coords(
            self.borda,
            *pontos_arredondados(1, 1, largura - 1, altura - 1, self.raio),
        )
        self.itemconfigure(
            self.janela_interna,
            width=max(1, largura - 2 * self.margem),
            height=max(1, altura - 2 * self.margem),
        )


class CampoArredondado(tk.Canvas):
    def __init__(self, parent, valor):
        super().__init__(
            parent, bg=PAINEL, highlightthickness=0,
            bd=0, height=39, width=105,
        )
        self.borda = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1,
            fill=CAMPO, outline=BORDA, width=1,
        )
        self.entrada = tk.Entry(
            self, bg=CAMPO, fg=TEXTO, insertbackground=TEXTO,
            relief="flat", highlightthickness=0, bd=0,
            font=("DejaVu Sans", 10),
        )
        self.entrada.insert(0, valor)
        self.area_entrada = self.create_window(
            13, 9, window=self.entrada, anchor="nw",
        )
        self.bind("<Configure>", self.ajustar)
        self.entrada.bind("<FocusIn>", self.focar)
        self.entrada.bind("<FocusOut>", self.desfocar)
        self.bind("<Button-1>", lambda _evento: self.entrada.focus_set())

    def ajustar(self, evento):
        largura = max(1, evento.width)
        altura = max(1, evento.height)
        self.coords(
            self.borda,
            *pontos_arredondados(1, 1, largura - 1, altura - 1, 12),
        )
        self.itemconfigure(
            self.area_entrada,
            width=max(1, largura - 26),
            height=max(1, altura - 18),
        )

    def focar(self, _evento):
        self.itemconfigure(self.borda, outline=DESTAQUE, width=2)

    def desfocar(self, _evento):
        self.itemconfigure(self.borda, outline=BORDA, width=1)

    def get(self):
        return self.entrada.get()

    def set(self, valor):
        self.entrada.delete(0, "end")
        self.entrada.insert(0, str(valor))

    def bind_enter(self, comando):
        self.entrada.bind("<Return>", lambda _evento: comando())


class SliderArredondado(tk.Canvas):
    def __init__(self, parent, valor, minimo, maximo, passo, comando):
        super().__init__(
            parent, height=28, width=110, bg=PAINEL,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.valor = float(valor)
        self.minimo = float(minimo)
        self.maximo = float(maximo)
        self.passo = float(passo)
        self.comando = comando
        self.bind("<Configure>", self.redesenhar)
        self.bind("<Button-1>", self.arrastar)
        self.bind("<B1-Motion>", self.arrastar)
        self.bind("<Left>", lambda _evento: self.mover_passo(-1))
        self.bind("<Right>", lambda _evento: self.mover_passo(1))
        self.bind("<Home>", lambda _evento: self.definir(self.minimo, True))
        self.bind("<End>", lambda _evento: self.definir(self.maximo, True))

    def redesenhar(self, _evento=None):
        self.delete("all")
        largura = self.winfo_width()
        if largura < 34:
            return
        esquerda, direita, centro = 13, largura - 13, 14
        fracao = (self.valor - self.minimo) / (self.maximo - self.minimo)
        x = esquerda + (direita - esquerda) * fracao
        self.create_line(
            esquerda, centro, direita, centro,
            fill=BORDA, width=5, capstyle="round",
        )
        self.create_line(
            esquerda, centro, x, centro,
            fill=DESTAQUE, width=5, capstyle="round",
        )
        self.create_oval(
            x - 7, centro - 7, x + 7, centro + 7,
            fill=DESTAQUE, outline=PAINEL, width=2,
        )

    def definir(self, valor, notificar=False):
        if not math.isfinite(float(valor)):
            return
        if valor < self.minimo or valor > self.maximo:
            folga = max(1.0, abs(float(valor)))
            self.minimo = min(self.minimo, -math.ceil(folga * 1.2))
            self.maximo = max(self.maximo, math.ceil(folga * 1.2))
        novo = max(self.minimo, min(self.maximo, round(float(valor) / self.passo) * self.passo))
        novo = round(novo, 8)
        if novo == self.valor:
            return
        self.valor = novo
        self.redesenhar()
        if notificar:
            self.comando(novo)

    def arrastar(self, evento):
        self.focus_set()
        largura = self.winfo_width()
        if largura <= 26:
            return
        proporcao = max(0.0, min(1.0, (evento.x - 13) / (largura - 26)))
        self.definir(self.minimo + proporcao * (self.maximo - self.minimo), True)

    def mover_passo(self, direcao):
        self.definir(self.valor + direcao * self.passo, True)
        return "break"


class BotaoArredondado(tk.Canvas):
    def __init__(self, parent, texto, comando, cor=DESTAQUE, contorno=False):
        super().__init__(
            parent, bg=PAINEL, height=44,
            highlightthickness=0, bd=0,
            cursor="hand2", takefocus=True,
        )
        self.comando = comando
        self.cor = cor
        self.contorno = contorno
        self.fundo = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1,
            fill=CAMPO if contorno else cor,
            outline=BORDA if contorno else "",
            width=1,
        )
        self.rotulo = self.create_text(
            10, 22, text=texto,
            fill=TEXTO if contorno else FUNDO,
            font=("DejaVu Sans", 10, "bold"), anchor="center",
        )
        self.bind("<Configure>", self.ajustar)
        self.bind("<Enter>", lambda _evento: self.itemconfigure(
            self.fundo, fill="#314761" if contorno else "#7dd3fc"
        ))
        self.bind("<Leave>", lambda _evento: self.itemconfigure(
            self.fundo, fill=CAMPO if contorno else cor
        ))
        self.bind("<Button-1>", lambda _evento: self.comando())
        self.bind("<Return>", lambda _evento: self.comando())
        self.bind("<space>", lambda _evento: self.comando())

    def ajustar(self, evento):
        self.coords(
            self.fundo,
            *pontos_arredondados(1, 1, evento.width - 1, evento.height - 1, 14),
        )
        self.coords(self.rotulo, evento.width / 2, evento.height / 2)


class BotaoModo(tk.Canvas):
    def __init__(self, parent, texto, comando, altura=36):
        super().__init__(
            parent, bg=PAINEL, height=altura, width=110,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.comando = comando
        self.fundo = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1, fill=CAMPO, outline="",
        )
        self.rotulo = self.create_text(
            10, altura / 2, text=texto, fill=SUAVE,
            font=("DejaVu Sans", 9, "bold"), anchor="center",
        )
        self.bind("<Configure>", self.ajustar)
        self.bind("<Button-1>", lambda _evento: self.comando())
        self.bind("<Return>", lambda _evento: self.comando())
        self.bind("<space>", lambda _evento: self.comando())

    def ajustar(self, evento):
        self.coords(
            self.fundo,
            *pontos_arredondados(1, 1, evento.width - 1, evento.height - 1, 11),
        )
        self.coords(self.rotulo, evento.width / 2, evento.height / 2)

    def definir_selecionado(self, selecionado):
        self.itemconfigure(self.fundo, fill=DESTAQUE if selecionado else CAMPO)
        self.itemconfigure(self.rotulo, fill=FUNDO if selecionado else SUAVE)


class SeletorArredondado(tk.Canvas):
    def __init__(self, parent, variavel, opcoes, comando):
        super().__init__(
            parent, bg=PAINEL, width=115, height=40,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.variavel = variavel
        self.opcoes = tuple(opcoes)
        self.comando = comando
        self.habilitado = True
        self.sobre = False
        self.focado = False
        self.rastro = self.variavel.trace_add("write", self.atualizar_rotulo)
        self.menu = tk.Menu(
            self, tearoff=False, bg=CAMPO, fg=TEXTO,
            activebackground="#314761", activeforeground=TEXTO,
            bd=1, relief="flat", font=("DejaVu Sans", 10),
        )
        self.bind("<Configure>", self.redesenhar)
        self.bind("<Enter>", self.entrar)
        self.bind("<Leave>", self.sair)
        self.bind("<FocusIn>", self.focar)
        self.bind("<FocusOut>", self.desfocar)
        self.bind("<Button-1>", self.abrir)
        self.bind("<Return>", self.abrir)
        self.bind("<space>", self.abrir)
        self.bind("<Down>", self.selecionar_seguinte)
        self.bind("<Up>", self.selecionar_anterior)

    def redesenhar(self, _evento=None):
        self.delete("all")
        largura = self.winfo_width()
        altura = self.winfo_height()
        if largura < 40 or altura < 12:
            return
        destaque = self.habilitado and (self.sobre or self.focado)
        self.create_polygon(
            *pontos_arredondados(1, 1, largura - 1, altura - 1, 12),
            fill="#253750" if destaque else CAMPO,
            outline=DESTAQUE if destaque else BORDA,
            width=1.5 if destaque else 1,
        )
        cor = TEXTO if self.habilitado else SUAVE
        self.create_text(
            13, altura / 2, text=f"{self.variavel.get()}(x)",
            fill=cor, font=("DejaVu Sans", 10, "bold"), anchor="w",
        )
        x = largura - 18
        self.create_line(
            x - 5, altura / 2 - 2, x, altura / 2 + 3,
            x + 5, altura / 2 - 2,
            fill=DESTAQUE if destaque else SUAVE,
            width=2, capstyle="round", joinstyle="round",
        )

    def atualizar_rotulo(self, *_args):
        self.redesenhar()

    def atualizar_opcoes(self, opcoes, habilitado):
        self.opcoes = tuple(opcoes)
        self.habilitado = habilitado
        self.configure(cursor="hand2" if habilitado else "arrow")
        self.redesenhar()

    def fechar_menu(self):
        self.menu.unpost()

    def selecionar(self, valor):
        self.fechar_menu()
        if not self.habilitado or valor not in self.opcoes:
            return
        if self.variavel.get() == valor:
            return
        self.variavel.set(valor)
        self.comando(None)

    def abrir(self, _evento=None):
        if not self.habilitado:
            return "break"
        self.focus_set()
        self.fechar_menu()
        self.menu.delete(0, "end")
        for nome in self.opcoes:
            self.menu.add_command(
                label=f"{nome}(x)",
                command=lambda valor=nome: self.selecionar(valor),
            )
        try:
            self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
        finally:
            self.menu.grab_release()
        return "break"

    def selecionar_seguinte(self, _evento=None):
        if self.habilitado and self.opcoes:
            atual = self.variavel.get()
            indice = self.opcoes.index(atual) if atual in self.opcoes else -1
            self.selecionar(self.opcoes[(indice + 1) % len(self.opcoes)])
        return "break"

    def selecionar_anterior(self, _evento=None):
        if self.habilitado and self.opcoes:
            atual = self.variavel.get()
            indice = self.opcoes.index(atual) if atual in self.opcoes else 0
            self.selecionar(self.opcoes[(indice - 1) % len(self.opcoes)])
        return "break"

    def entrar(self, _evento):
        self.sobre = True
        self.redesenhar()

    def sair(self, _evento):
        self.sobre = False
        self.redesenhar()

    def focar(self, _evento):
        self.focado = True
        self.redesenhar()

    def desfocar(self, _evento):
        self.focado = False
        self.redesenhar()

    def destroy(self):
        self.variavel.trace_remove("write", self.rastro)
        self.fechar_menu()
        self.menu.destroy()
        super().destroy()


class AlternadorVisibilidade(tk.Canvas):
    def __init__(self, parent, texto, variavel, comando):
        super().__init__(
            parent, bg=PAINEL, width=125, height=36,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.texto = texto
        self.variavel = variavel
        self.comando = comando
        self.habilitado = True
        self.sobre = False
        self.rastro = variavel.trace_add("write", self.alterou_variavel)
        self.bind("<Configure>", self.redesenhar)
        self.bind("<Enter>", self.entrar)
        self.bind("<Leave>", self.sair)
        self.bind("<Button-1>", self.alternar)
        self.bind("<Return>", self.alternar)
        self.bind("<space>", self.alternar)

    def redesenhar(self, _evento=None):
        self.delete("all")
        largura, altura = self.winfo_width(), self.winfo_height()
        if largura < 30 or altura < 12:
            return
        ativo = self.variavel.get()
        destaque = self.habilitado and self.sobre
        self.create_polygon(
            *pontos_arredondados(1, 1, largura - 1, altura - 1, 11),
            fill="#263a52" if destaque else CAMPO,
            outline=DESTAQUE if destaque else BORDA,
            width=1,
        )
        self.create_oval(
            9, altura / 2 - 8, 25, altura / 2 + 8,
            fill=DESTAQUE if ativo and self.habilitado else PAINEL,
            outline=DESTAQUE if ativo and self.habilitado else SUAVE,
            width=1.5,
        )
        if ativo:
            self.create_line(
                13, altura / 2, 16, altura / 2 + 3,
                21, altura / 2 - 4,
                fill=FUNDO if self.habilitado else SUAVE,
                width=2, capstyle="round", joinstyle="round",
            )
        self.create_text(
            33, altura / 2, text=self.texto, anchor="w",
            fill=TEXTO if self.habilitado else SUAVE,
            font=("DejaVu Sans", 9),
        )

    def alterou_variavel(self, *_args):
        self.redesenhar()

    def definir_habilitado(self, habilitado):
        self.habilitado = habilitado
        self.configure(cursor="hand2" if habilitado else "arrow")
        self.redesenhar()

    def alternar(self, _evento=None):
        if self.habilitado:
            self.variavel.set(not self.variavel.get())
            self.comando()
        return "break"

    def entrar(self, _evento):
        self.sobre = True
        self.redesenhar()

    def sair(self, _evento):
        self.sobre = False
        self.redesenhar()

    def destroy(self):
        self.variavel.trace_remove("write", self.rastro)
        super().destroy()


class BotaoRecolher(tk.Canvas):
    def __init__(self, parent, comando):
        super().__init__(
            parent, bg=FUNDO, width=30, height=66,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.comando = comando
        self.recolhido = False
        self.sobre = False
        self.bind("<Configure>", self.redesenhar)
        self.bind("<Enter>", self.entrar)
        self.bind("<Leave>", self.sair)
        self.bind("<Button-1>", self.acionar)
        self.bind("<Return>", self.acionar)
        self.bind("<space>", self.acionar)

    def redesenhar(self, _evento=None):
        self.delete("all")
        largura = self.winfo_width()
        altura = self.winfo_height()
        self.create_polygon(
            *pontos_arredondados(1, 1, largura - 1, altura - 1, 12),
            fill="#314761" if self.sobre else CAMPO,
            outline=DESTAQUE if self.sobre else BORDA,
            width=1,
        )
        self.create_text(
            largura / 2, altura / 2 - 1,
            text="❯" if self.recolhido else "❮",
            fill=DESTAQUE if self.sobre else SUAVE,
            font=("DejaVu Sans", 14, "bold"),
        )

    def definir_recolhido(self, recolhido):
        self.recolhido = recolhido
        self.redesenhar()

    def entrar(self, _evento):
        self.sobre = True
        self.redesenhar()

    def sair(self, _evento):
        self.sobre = False
        self.redesenhar()

    def acionar(self, _evento):
        self.focus_set()
        self.comando()


class BarraRolagemMinimalista(tk.Canvas):
    def __init__(self, parent, command):
        super().__init__(
            parent, bg=PAINEL, width=13,
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self.command = command
        self.inicio = 0.0
        self.fim = 1.0
        self.deslocamento = None
        self.hover = False
        self.bind("<Configure>", self.redesenhar)
        self.bind("<Button-1>", self.clicar)
        self.bind("<B1-Motion>", self.arrastar)
        self.bind("<ButtonRelease-1>", self.soltar)
        self.bind("<Enter>", self.entrar)
        self.bind("<Leave>", self.sair)

    def set(self, inicio, fim):
        self.inicio = max(0.0, min(float(inicio), 1.0))
        self.fim = max(self.inicio, min(float(fim), 1.0))
        self.redesenhar()

    def geometria_thumb(self):
        altura = max(self.winfo_height() - 12, 1)
        proporcao = self.fim - self.inicio
        tamanho = min(altura, max(34, altura * proporcao))
        curso = max(altura - tamanho, 0)
        topo = 6 + curso * (self.inicio / max(1 - proporcao, 0.00001))
        return topo, topo + tamanho, curso

    def redesenhar(self, _evento=None):
        self.delete("all")
        largura = self.winfo_width()
        altura = self.winfo_height()
        if largura < 4 or altura < 20:
            return
        self.create_polygon(
            *pontos_arredondados(5, 3, largura - 5, altura - 3, 2),
            fill="#182336", outline="",
        )
        if self.fim - self.inicio >= 0.99999:
            return
        topo, base, _ = self.geometria_thumb()
        self.create_polygon(
            *pontos_arredondados(3, topo, largura - 3, base, 3),
            fill="#a7adb6" if self.hover or self.deslocamento is not None else "#7c858f",
            outline="", tags="thumb",
        )

    def clicar(self, evento):
        if self.fim - self.inicio >= 0.99999:
            return
        topo, base, curso = self.geometria_thumb()
        if topo <= evento.y <= base:
            self.deslocamento = evento.y - topo
        else:
            self.deslocamento = (base - topo) / 2
            self.mover(evento.y, curso)
        self.redesenhar()

    def mover(self, posicao, curso=None):
        if curso is None:
            _, _, curso = self.geometria_thumb()
        if curso <= 0 or self.deslocamento is None:
            return
        tamanho_visivel = self.fim - self.inicio
        deslocamento = (posicao - self.deslocamento - 6) / curso
        fracao = max(0.0, min(deslocamento, 1.0)) * (1 - tamanho_visivel)
        self.command("moveto", fracao)

    def arrastar(self, evento):
        self.mover(evento.y)

    def soltar(self, _evento):
        self.deslocamento = None
        self.redesenhar()

    def entrar(self, _evento):
        self.hover = True
        self.redesenhar()

    def sair(self, _evento):
        self.hover = False
        self.redesenhar()


class CursorPrecisao:
    def __init__(self, canvas, funcoes, toolbar, status, visibilidade_funcoes, visibilidade_elementos):
        self.canvas = canvas
        self.eixo = canvas.figure.axes[0]
        self.funcoes = funcoes
        self.visibilidade_funcoes = visibilidade_funcoes
        self.visibilidade_elementos = visibilidade_elementos
        self.toolbar = toolbar
        self.status = status
        self.status_base = status.get()
        self.cores = [
            linha.get_color()
            for linha in self.eixo.lines[:len(funcoes)]
        ]
        self.ponto, = self.eixo.plot(
            [], [], marker="o", linestyle="None", markersize=8,
            markeredgecolor="#ffffff", markeredgewidth=1.5,
            zorder=20, visible=False, label="_nolegend_",
        )
        self.etiqueta = self.eixo.annotate(
            "", xy=(0, 0), xytext=(12, 12),
            textcoords="offset points", fontsize=10,
            color=TEXTO,
            bbox=dict(
                boxstyle="round,pad=0.5", facecolor=CAMPO,
                edgecolor=DESTAQUE, alpha=0.96,
            ),
            zorder=21, visible=False,
        )
        self.conexoes = [
            self.canvas.mpl_connect("motion_notify_event", self.movimentar),
            self.canvas.mpl_connect("figure_leave_event", self.sair),
        ]

    def desconectar(self):
        for conexao in self.conexoes:
            self.canvas.mpl_disconnect(conexao)
        self.conexoes.clear()

    def ocultar(self, restaurar_status=False):
        if self.ponto.get_visible() or self.etiqueta.get_visible():
            self.ponto.set_visible(False)
            self.etiqueta.set_visible(False)
            self.canvas.draw_idle()
        if restaurar_status:
            self.status.set(self.status_base)

    def sair(self, _evento):
        self.ocultar(restaurar_status=True)

    def movimentar(self, evento):
        if not self.visibilidade_elementos["curvas"].get():
            self.ocultar(restaurar_status=True)
            return
        if getattr(self, "foco", None) is not None and self.foco.selecionado is not None:
            self.ocultar()
            return

        if self.toolbar is not None and self.toolbar.mode:
            self.ocultar(restaurar_status=True)
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
            if not self.visibilidade_funcoes[nome].get():
                continue
            try:
                if isinstance(funcao, Expressao):
                    y = funcao.calcular(x)
                else:
                    a, b, c = funcao
                    y = (a * x + b) * x + c
                if not math.isfinite(y):
                    continue
                px, py = self.eixo.transData.transform((x, y))
                if not math.isfinite(px) or not math.isfinite(py):
                    continue
                distancia = math.hypot(px - evento.x, py - evento.y)
                if distancia <= 18 and (melhor is None or distancia < melhor[0]):
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
        deslocamento_y = -75 if py > limite.y1 - 85 else 12
        self.etiqueta.set_position((deslocamento_x, deslocamento_y))
        self.etiqueta.get_bbox_patch().set_edgecolor(cor)
        self.etiqueta.set_visible(True)
        self.status.set(
            f"{nome}(x)  •  x = {x_ponto:.6f}  •  y = {y_ponto:.6f}"
        )
        self.canvas.draw_idle()


class FocoPontosNotaveis:
    def __init__(
        self, canvas, funcoes, intersecoes, par, toolbar, cursor, status,
        raizes=None, extremos=None, visibilidade_funcoes=None,
        visibilidade_elementos=None,
    ):
        self.canvas = canvas
        self.eixo = canvas.figure.axes[0]
        self.toolbar = toolbar
        self.cursor = cursor
        self.status = status
        self.par = par
        self.visibilidade_funcoes = visibilidade_funcoes
        self.visibilidade_elementos = visibilidade_elementos
        self.limites_iniciais = (self.eixo.get_xlim(), self.eixo.get_ylim())
        self.selecionado = None
        self.pontos = []
        self.cores = {
            nome: linha.get_color()
            for (nome, _), linha in zip(funcoes, self.eixo.lines)
        }

        if intersecoes is not None and intersecoes[0] == "pontos":
            for x, y in intersecoes[1]:
                self.registrar(
                    f"Interseção {par[0]}/{par[1]}", x, y, "#4ade80",
                    "intersecoes",
                )

        for nome, funcao in funcoes:
            polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
            cor = self.cores[nome]
            if polinomio is not None:
                ponto_vertice = vertice(polinomio)
                if ponto_vertice is not None:
                    self.registrar(
                        f"Vértice de {nome}(x)", *ponto_vertice, cor,
                        "vertices", nome,
                    )
            lista_raizes = (
                raizes[nome][1] if raizes is not None
                else raizes_reais(polinomio) if polinomio is not None else []
            )
            for raiz in lista_raizes:
                self.registrar(
                    f"Raiz de {nome}(x)", raiz, 0.0, cor, "raizes", nome,
                )
            for tipo, x, y in (extremos or {}).get(nome, []):
                descricao = "Máximo local" if tipo == "maximo" else "Mínimo local"
                cor_extremo = "#fb7185" if tipo == "maximo" else "#c084fc"
                self.registrar(
                    f"{descricao} de {nome}(x)", x, y,
                    cor_extremo, "extremos", nome,
                )

        self.marcador, = self.eixo.plot(
            [], [], marker="o", markersize=12, linestyle="None",
            markeredgecolor="#ffffff", markeredgewidth=2,
            color="#4ade80", zorder=25, visible=False,
            label="_nolegend_",
        )
        self.etiqueta = self.eixo.annotate(
            "", xy=(0, 0), xytext=(18, 18),
            textcoords="offset points", fontsize=10, color=TEXTO,
            bbox=dict(
                boxstyle="round,pad=0.6", facecolor=CAMPO,
                edgecolor="#4ade80", alpha=0.97,
            ),
            zorder=26, visible=False,
        )
        self.conexao = self.canvas.mpl_connect("button_press_event", self.clicar)

    def registrar(self, descricao, x, y, cor, categoria, nome=None):
        if not math.isfinite(x) or not math.isfinite(y):
            return
        limite_x = self.limites_iniciais[0]
        if min(limite_x) <= x <= max(limite_x):
            self.pontos.append((descricao, x, y, cor, categoria, nome))

    def ponto_visivel(self, ponto):
        _, _, _, _, categoria, nome = ponto
        if not self.visibilidade_elementos[categoria].get():
            return False
        if categoria == "intersecoes":
            return all(self.visibilidade_funcoes[n].get() for n in self.par)
        return nome is None or self.visibilidade_funcoes[nome].get()

    def remover_ponto_tangente(self):
        self.pontos = [ponto for ponto in self.pontos if ponto[4] != "tangente"]
        if self.selecionado is not None and self.selecionado[4] == "tangente":
            self.selecionado = None
            self.marcador.set_visible(False)
            self.etiqueta.set_visible(False)

    def definir_ponto_tangente(self, nome, x, y):
        self.remover_ponto_tangente()
        self.registrar(
            f"Tangente de {nome}(x)", x, y, "#fb923c", "tangente", nome,
        )

    def atualizar_visibilidade(self):
        if self.selecionado is not None and not self.ponto_visivel(self.selecionado):
            self.selecionado = None
            self.marcador.set_visible(False)
            self.etiqueta.set_visible(False)
            self.cursor.ocultar(restaurar_status=True)

    def clicar(self, evento):
        if (
            evento.button != 1
            or evento.inaxes is not self.eixo
            or (self.toolbar is not None and self.toolbar.mode)
            or evento.x is None
            or evento.y is None
        ):
            return

        candidato = None
        menor_distancia = 16.0
        for ponto in self.pontos:
            if not self.ponto_visivel(ponto):
                continue
            descricao, x, y, cor = ponto[:4]
            px, py = self.eixo.transData.transform((x, y))
            if not math.isfinite(px) or not math.isfinite(py):
                continue
            if not self.eixo.bbox.contains(px, py):
                continue
            distancia = math.hypot(evento.x - px, evento.y - py)
            if (
                distancia < menor_distancia - 1e-6
                or (
                    candidato is not None
                    and abs(distancia - menor_distancia) <= 1e-6
                    and (
                        ponto[4] == "tangente"
                        or (
                            ponto[4] == "extremos"
                            and candidato[4] not in ("tangente", "extremos")
                        )
                    )
                )
            ):
                menor_distancia = distancia
                candidato = ponto

        if candidato is None:
            return

        descricao, x, y, cor = candidato[:4]
        self.cursor.ocultar()
        self.selecionado = candidato
        self.eixo.set_xlim(x - self.amplitude(self.eixo.get_xlim()) / 14,
                           x + self.amplitude(self.eixo.get_xlim()) / 14)
        self.eixo.set_ylim(y - self.amplitude(self.eixo.get_ylim()) / 14,
                           y + self.amplitude(self.eixo.get_ylim()) / 14)
        self.marcador.set_data([x], [y])
        self.marcador.set_markerfacecolor(cor)
        self.marcador.set_visible(True)
        self.etiqueta.xy = (x, y)
        self.etiqueta.set_text(f"{descricao}\nx = {x:.6f}\ny = {y:.6f}")
        self.etiqueta.get_bbox_patch().set_edgecolor(cor)
        self.etiqueta.set_visible(True)
        self.status.set(f"{descricao}  •  x = {x:.6f}  •  y = {y:.6f}")
        self.canvas.draw_idle()

    @staticmethod
    def amplitude(limites):
        return abs(limites[1] - limites[0])

    def restaurar(self):
        self.eixo.set_xlim(self.limites_iniciais[0])
        self.eixo.set_ylim(self.limites_iniciais[1])
        self.selecionado = None
        self.marcador.set_visible(False)
        self.etiqueta.set_visible(False)
        self.cursor.ocultar()
        self.status.set(self.cursor.status_base)
        self.canvas.draw_idle()

    def desconectar(self):
        self.canvas.mpl_disconnect(self.conexao)


class ExploradorApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Explorador de Funções 3.7")
        self.janela.geometry("1360x840")
        self.janela.minsize(1050, 660)
        self.janela.configure(bg=FUNDO)

        self.figura = None
        self.parametros_visiveis = True
        self.canvas = None
        self.toolbar = None
        self.cursor_precisao = None
        self.foco_pontos = None
        self.campos = {}
        self.sliders = {}
        self.atualizacao_pendente = None
        self.atualizacao_tangente_pendente = None
        self.aba_ativa = "funcoes"
        self.quantidade_funcoes = 2
        self.primeira_intersecao = tk.StringVar(value="f")
        self.segunda_intersecao = tk.StringVar(value="g")
        self.funcao_tangente = tk.StringVar(value="f")
        self.tangente_ativa = False
        self.tangente_artistas = []
        self.funcoes_atuais = {}
        self.intervalo_atual = (-5, 5)
        self.visibilidade_elementos = {
            nome: tk.BooleanVar(value=True)
            for nome in (
                "curvas", "raizes", "vertices", "extremos",
                "intersecoes", "grade", "legenda", "tangente",
            )
        }
        self.visibilidade_funcoes = {
            nome: tk.BooleanVar(value=True) for nome in "fghij"
        }
        self.tipos = {nome: "Afim" for nome in "fghij"}
        self.botoes_tipo = {}
        self.rotulos = {}
        self.campos_c = {}
        self.campos_ab = {}
        self.campos_expressao = {}

        self.criar_interface()
        self.gerar_grafico()

    @staticmethod
    def texto(parent, conteudo, tamanho=11, cor=TEXTO, negrito=False):
        return tk.Label(
            parent, text=conteudo, bg=parent["bg"], fg=cor,
            font=("DejaVu Sans", tamanho, "bold" if negrito else "normal"),
            anchor="w", justify="left",
        )

    def criar_par_de_campos(self, parent, definicoes):
        linha = tk.Frame(parent, bg=PAINEL)
        linha.pack(fill="x", pady=(5, 0))
        linha.columnconfigure(0, weight=1, uniform="parametros")
        linha.columnconfigure(1, weight=1, uniform="parametros")
        for indice, (chave, rotulo, valor) in enumerate(definicoes):
            coluna = tk.Frame(linha, bg=PAINEL)
            coluna.grid(
                row=0, column=indice, sticky="ew",
                padx=(0, 5) if indice == 0 else (5, 0),
            )
            rotulo_widget = self.texto(coluna, rotulo, 9, SUAVE)
            rotulo_widget.pack(anchor="w", pady=(0, 3))
            entrada = CampoArredondado(coluna, valor)
            entrada.pack(fill="x")
            entrada.bind_enter(self.gerar_grafico)
            self.campos[chave] = entrada
            self.rotulos[chave] = rotulo_widget
            self.criar_slider_campo(coluna, chave, entrada, valor)
        return linha

    def criar_slider_campo(self, parent, chave, entrada, valor):
        eh_intervalo = chave in ("inicio", "fim")
        minimo, maximo, passo = (-20, 20, 1) if eh_intervalo else (-10, 10, 0.1)
        slider = SliderArredondado(
            parent, float(valor), minimo, maximo, passo,
            lambda numero, campo=entrada, nome=chave: self.ajustar_com_slider(
                nome, campo, numero
            ),
        )
        slider.pack(fill="x", pady=(3, 0))
        self.sliders[chave] = slider
        entrada.entrada.bind(
            "<FocusOut>",
            lambda _evento, nome=chave: self.sincronizar_slider(nome),
            add="+",
        )
        entrada.entrada.bind(
            "<Return>",
            lambda _evento, nome=chave: self.sincronizar_slider(nome),
            add="+",
        )
        return slider

    def sincronizar_slider(self, chave):
        try:
            numero = float(self.campos[chave].get().replace(",", "."))
            self.sliders[chave].definir(numero)
        except (ValueError, OverflowError):
            return

    def ajustar_com_slider(self, chave, campo, valor):
        campo.set(f"{valor:g}")
        if self.atualizacao_pendente is not None:
            self.janela.after_cancel(self.atualizacao_pendente)
        self.atualizacao_pendente = self.janela.after(
            200, self.atualizar_grafico_com_slider,
        )

    def atualizar_grafico_com_slider(self):
        self.atualizacao_pendente = None
        try:
            inicio = int(self.campos["inicio"].get())
            fim = int(self.campos["fim"].get())
            if inicio >= fim:
                self.status.set("Ajuste o intervalo: início deve ser menor que fim.")
                return
        except ValueError:
            return
        self.gerar_grafico(silencioso=True)

    def mostrar_aba(self, nome):
        if nome == self.aba_ativa and self.paginas[nome].winfo_manager():
            return
        self.fechar_menus()
        for chave, pagina in self.paginas.items():
            if chave == nome:
                pagina.pack(fill="both", expand=True)
            else:
                pagina.pack_forget()
            self.botoes_abas[chave].definir_selecionado(chave == nome)
        self.aba_ativa = nome
        self.rolagem.yview_moveto(0)

    def criar_grupo_funcao(self, parent, nome, valores):
        grupo = tk.Frame(parent, bg=PAINEL)
        self.texto(grupo, f"FUNÇÃO {nome}(x)", 9, SUAVE, True).pack(
            anchor="w", pady=(11, 5)
        )

        selecao = tk.Frame(grupo, bg=PAINEL)
        selecao.pack(fill="x")
        selecao.columnconfigure(0, weight=1, uniform="tipos")
        selecao.columnconfigure(1, weight=1, uniform="tipos")
        selecao_tipo = {}
        for indice, tipo in enumerate(("Afim", "Quadrática")):
            botao = BotaoModo(
                selecao, tipo, lambda n=nome, t=tipo: self.alterar_tipo(n, t)
            )
            botao.grid(
                row=0, column=indice, sticky="ew",
                padx=(0, 4) if indice == 0 else (4, 0),
            )
            selecao_tipo[tipo] = botao

        botao_expressao = BotaoModo(
            selecao, "Expressão", lambda n=nome: self.alterar_tipo(n, "Expressão")
        )
        botao_expressao.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(7, 0)
        )
        selecao_tipo["Expressão"] = botao_expressao
        self.botoes_tipo[nome] = selecao_tipo
        selecao_tipo["Afim"].definir_selecionado(True)

        a, b, c = valores
        self.campos_ab[nome] = self.criar_par_de_campos(
            grupo,
            ((f"a{nome}", "a · angular", a),
             (f"b{nome}", "b · linear", b)),
        )
        linha_c = tk.Frame(grupo, bg=PAINEL)
        self.texto(linha_c, "c · constante", 9, SUAVE).pack(
            anchor="w", pady=(3, 3)
        )
        entrada_c = CampoArredondado(linha_c, c)
        entrada_c.pack(fill="x")
        entrada_c.bind_enter(self.gerar_grafico)
        self.campos[f"c{nome}"] = entrada_c
        self.criar_slider_campo(linha_c, f"c{nome}", entrada_c, c)
        self.campos_c[nome] = linha_c
        linha_expressao = tk.Frame(grupo, bg=PAINEL)
        self.texto(
            linha_expressao, "Escreva a função de x", 9, SUAVE
        ).pack(anchor="w", pady=(4, 3))
        campo = CampoArredondado(
            linha_expressao, {"f": "sin(x)", "g": "cos(x)", "h": "x^2", "i": "sqrt(x)", "j": "1/x"}[nome]
        )
        campo.pack(fill="x")
        campo.bind_enter(self.gerar_grafico)
        self.campos[f"expressao_{nome}"] = campo
        self.campos_expressao[nome] = linha_expressao
        grupo.pack(fill="x")
        return grupo

    def criar_alternadores(self, parent, opcoes):
        linha = None
        botoes = {}
        for indice, (nome, titulo, variavel) in enumerate(opcoes):
            if indice % 2 == 0:
                linha = tk.Frame(parent, bg=PAINEL)
                linha.pack(fill="x", pady=(0, 6))
            botao = AlternadorVisibilidade(
                linha, titulo, variavel, self.aplicar_visibilidade,
            )
            botao.pack(
                side="left", fill="x", expand=True,
                padx=(0, 4) if indice % 2 == 0 else (4, 0),
            )
            botoes[nome] = botao
        return botoes

    def atualizar_botoes_visibilidade(self):
        for nome, botao in self.botoes_visibilidade_funcoes.items():
            botao.definir_habilitado(nome in self.nomes_ativos)

    def aplicar_visibilidade(self):
        if self.figura is None:
            return
        eixo = self.figura.axes[0]
        visiveis = self.visibilidade_elementos
        funcoes = self.visibilidade_funcoes
        par = (self.primeira_intersecao.get(), self.segunda_intersecao.get())
        for artista in eixo.get_children():
            identificador = artista.get_gid()
            if not identificador:
                continue
            categoria, _, nome = identificador.partition(":")
            if categoria == "curva":
                mostrar = visiveis["curvas"].get() and funcoes[nome].get()
            elif categoria in ("raiz", "vertice", "extremo"):
                chave = {
                    "raiz": "raizes", "vertice": "vertices", "extremo": "extremos",
                }[categoria]
                mostrar = visiveis[chave].get() and funcoes[nome].get()
            elif categoria == "intersecao":
                mostrar = (
                    visiveis["intersecoes"].get()
                    and all(funcoes[n].get() for n in par)
                )
            elif categoria == "tangente":
                mostrar = visiveis["tangente"].get() and funcoes[nome].get()
            else:
                continue
            artista.set_visible(mostrar)

        eixo.grid(visiveis["grade"].get())
        legenda_antiga = eixo.get_legend()
        if legenda_antiga is not None:
            legenda_antiga.remove()
        if visiveis["legenda"].get():
            handles, labels = eixo.get_legend_handles_labels()
            unicos = {}
            for handle, label in zip(handles, labels):
                if handle.get_visible():
                    unicos.setdefault(label, handle)
            if unicos:
                legenda = eixo.legend(
                    unicos.values(), unicos.keys(), loc="upper right",
                    facecolor=PAINEL, edgecolor=BORDA, fontsize=9,
                )
                for texto in legenda.get_texts():
                    texto.set_color(TEXTO)

        if self.cursor_precisao is not None:
            self.cursor_precisao.ocultar(restaurar_status=True)
        if self.foco_pontos is not None:
            self.foco_pontos.atualizar_visibilidade()
        self.canvas.draw_idle()

    def criar_interface(self):
        topo = tk.Frame(self.janela, bg=FUNDO, padx=28, pady=20)
        topo.pack(fill="x")
        self.texto(topo, "EXPLORADOR DE FUNÇÕES", 20, TEXTO, True).pack(anchor="w")
        self.texto(
            topo, "Laboratório interativo de gráficos matemáticos", 10, SUAVE
        ).pack(anchor="w", pady=(5, 0))

        corpo = tk.Frame(self.janela, bg=FUNDO, padx=24, pady=5)
        corpo.pack(fill="both", expand=True)

        self.painel_parametros = CartaoArredondado(
            corpo, largura=374, raio=24, margem=17,
        )
        self.painel_parametros.pack(side="left", fill="y", padx=(0, 9))
        lateral = self.painel_parametros.conteudo
        cabecalho_abas = tk.Frame(lateral, bg=PAINEL)
        cabecalho_abas.pack(fill="x", pady=(0, 12))
        self.botoes_abas = {}
        for chave, titulo in (
            ("funcoes", "FUNÇÕES"),
            ("analises", "ANÁLISES"),
            ("visual", "VISUAL"),
        ):
            botao = BotaoModo(
                cabecalho_abas, titulo,
                lambda aba=chave: self.mostrar_aba(aba), altura=39,
            )
            botao.pack(side="left", fill="x", expand=True, padx=2)
            self.botoes_abas[chave] = botao

        self.faixa_alternancia = tk.Frame(corpo, bg=FUNDO, width=34)
        self.faixa_alternancia.pack(side="left", fill="y", padx=(0, 10))
        self.faixa_alternancia.pack_propagate(False)
        self.botao_recolher = BotaoRecolher(
            self.faixa_alternancia, self.alternar_parametros,
        )
        self.botao_recolher.place(relx=0.5, rely=0.5, anchor="center")

        rolagem = tk.Canvas(lateral, bg=PAINEL, highlightthickness=0, bd=0)
        barra_rolagem = BarraRolagemMinimalista(
            lateral, command=rolagem.yview,
        )
        barra_rolagem.pack(side="right", fill="y")
        rolagem.pack(side="left", fill="both", expand=True)
        rolagem.configure(yscrollcommand=self.atualizar_rolagem)
        self.rolagem = rolagem
        self.barra_rolagem = barra_rolagem
        interno = tk.Frame(rolagem, bg=PAINEL)
        janela_interna = rolagem.create_window((0, 0), window=interno, anchor="nw")
        interno.bind(
            "<Configure>",
            lambda _evento: rolagem.configure(scrollregion=rolagem.bbox("all")),
        )
        rolagem.bind(
            "<Configure>",
            lambda evento: rolagem.itemconfigure(janela_interna, width=evento.width),
        )
        self.paginas = {
            chave: tk.Frame(interno, bg=PAINEL)
            for chave in ("funcoes", "analises", "visual")
        }
        self.pagina_funcoes = self.paginas["funcoes"]
        self.pagina_analises = self.paginas["analises"]
        self.pagina_visual = self.paginas["visual"]
        self.paginas["funcoes"].pack(fill="both", expand=True)
        self.botoes_abas["funcoes"].definir_selecionado(True)

        self.texto(self.pagina_funcoes, "PARÂMETROS", 12, DESTAQUE, True).pack(
            anchor="w", pady=(0, 7)
        )
        self.texto(self.pagina_funcoes, "QUANTAS FUNÇÕES?", 9, SUAVE, True).pack(
            anchor="w", pady=(3, 5)
        )
        selecao_modo = tk.Frame(self.pagina_funcoes, bg=PAINEL)
        selecao_modo.pack(fill="x")
        self.botao_uma = BotaoModo(
            selecao_modo, "1 função", lambda: self.alterar_modo("uma")
        )
        self.botao_uma.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.botao_duas = BotaoModo(
            selecao_modo, "2 funções", lambda: self.alterar_modo("duas")
        )
        self.botao_duas.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.botao_duas.definir_selecionado(True)

        controles = tk.Frame(self.pagina_funcoes, bg=PAINEL)
        controles.pack(fill="x", pady=(8, 3))
        botao_adicionar = BotaoArredondado(
            controles, "+ ADICIONAR", self.adicionar_funcao, contorno=True
        )
        botao_adicionar.configure(width=125)
        botao_adicionar.pack(side="left", fill="x", expand=True, padx=(0, 4))
        botao_remover = BotaoArredondado(
            controles, "− REMOVER", self.remover_funcao, contorno=True
        )
        botao_remover.configure(width=125)
        botao_remover.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self.indicador_funcoes = self.texto(self.pagina_funcoes, "2 de 5 funções", 9, SUAVE)
        self.indicador_funcoes.pack(anchor="w", pady=(2, 0))

        self.texto(self.pagina_analises, "ANÁLISES", 12, DESTAQUE, True).pack(
            anchor="w", pady=(0, 9)
        )
        self.grupo_selecao_intersecoes = tk.Frame(self.pagina_analises, bg=PAINEL)
        self.grupo_selecao_intersecoes.pack(fill="x", pady=(13, 0))
        self.texto(
            self.grupo_selecao_intersecoes, "INTERSEÇÕES ENTRE FUNÇÕES",
            9, SUAVE, True,
        ).pack(anchor="w", pady=(0, 6))
        linha_seletores = tk.Frame(self.grupo_selecao_intersecoes, bg=PAINEL)
        linha_seletores.pack(fill="x")
        self.seletores_intersecoes = []
        for indice, variavel in enumerate((
            self.primeira_intersecao, self.segunda_intersecao,
        )):
            coluna = tk.Frame(linha_seletores, bg=PAINEL)
            coluna.pack(
                side="left", fill="x", expand=True,
                padx=(0, 5) if indice == 0 else (5, 0),
            )
            self.texto(
                coluna, "Primeira" if indice == 0 else "Segunda", 9, SUAVE,
            ).pack(anchor="w", pady=(0, 4))
            seletor = SeletorArredondado(
                coluna, variavel, ("f", "g"), self.alterar_par_intersecoes,
            )
            seletor.pack(fill="x")
            self.seletores_intersecoes.append(seletor)

        self.texto(self.pagina_visual, "PERSONALIZAR GRÁFICO", 12, DESTAQUE, True).pack(
            anchor="w", pady=(0, 9)
        )
        grupo_visibilidade = tk.Frame(self.pagina_visual, bg=PAINEL)
        grupo_visibilidade.pack(fill="x", pady=(15, 0))
        self.texto(
            grupo_visibilidade, "ELEMENTOS VISÍVEIS", 9, SUAVE, True,
        ).pack(anchor="w", pady=(0, 6))
        elementos = (
            ("curvas", "Curvas"),
            ("raizes", "Raízes"),
            ("vertices", "Vértices"),
            ("extremos", "Máx./mín."),
            ("intersecoes", "Interseções"),
            ("grade", "Grade"),
            ("legenda", "Legenda"),
            ("tangente", "Tangente"),
        )
        self.criar_alternadores(
            grupo_visibilidade,
            ((nome, titulo, self.visibilidade_elementos[nome]) for nome, titulo in elementos),
        )
        self.texto(
            grupo_visibilidade, "FUNÇÕES INDIVIDUAIS", 9, SUAVE, True,
        ).pack(anchor="w", pady=(12, 6))
        self.botoes_visibilidade_funcoes = self.criar_alternadores(
            grupo_visibilidade,
            ((nome, f"{nome}(x)", self.visibilidade_funcoes[nome]) for nome in "fghij"),
        )
        self.atualizar_botoes_visibilidade()

        grupo_tangente = tk.Frame(self.pagina_analises, bg=PAINEL)
        grupo_tangente.pack(fill="x", pady=(15, 0))
        self.texto(
            grupo_tangente, "DERIVADA E RETA TANGENTE", 9, SUAVE, True,
        ).pack(anchor="w", pady=(0, 6))
        linha_tangente = tk.Frame(grupo_tangente, bg=PAINEL)
        linha_tangente.pack(fill="x")
        coluna_funcao = tk.Frame(linha_tangente, bg=PAINEL)
        coluna_funcao.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.texto(coluna_funcao, "Função", 9, SUAVE).pack(anchor="w", pady=(0, 4))
        self.seletor_tangente = SeletorArredondado(
            coluna_funcao, self.funcao_tangente, ("f", "g"),
            lambda _evento: None,
        )
        self.seletor_tangente.pack(fill="x")
        coluna_x = tk.Frame(linha_tangente, bg=PAINEL)
        coluna_x.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.texto(coluna_x, "Posição x", 9, SUAVE).pack(anchor="w", pady=(0, 4))
        self.campo_tangente_x = CampoArredondado(coluna_x, "2")
        self.campo_tangente_x.pack(fill="x")
        self.campo_tangente_x.bind_enter(self.tracar_tangente)
        self.slider_tangente = SliderArredondado(
            coluna_x, 2, -20, 20, 0.1,
            self.ajustar_tangente_slider,
        )
        self.slider_tangente.pack(fill="x", pady=(3, 0))
        self.campo_tangente_x.entrada.bind(
            "<FocusOut>", lambda _evento: self.sincronizar_tangente_slider(),
            add="+",
        )
        BotaoArredondado(
            grupo_tangente, "TRAÇAR TANGENTE", self.tracar_tangente,
            contorno=True,
        ).pack(fill="x", pady=(9, 4))
        self.tangente_resumo = tk.StringVar(
            value="Escolha a função e o valor de x."
        )
        tk.Label(
            grupo_tangente, textvariable=self.tangente_resumo,
            bg=PAINEL, fg=SUAVE, anchor="w", justify="left",
            font=("DejaVu Sans", 9), wraplength=260,
        ).pack(anchor="w", fill="x", pady=(3, 0))

        self.grupos_funcoes = {}
        for nome, valores in (
            ("f", ("2", "1", "0")),
            ("g", ("-1", "4", "0")),
            ("h", ("1", "0", "0")),
            ("i", ("-2", "1", "0")),
            ("j", ("0", "3", "0")),
        ):
            grupo = self.criar_grupo_funcao(self.pagina_funcoes, nome, valores)
            self.grupos_funcoes[nome] = grupo
            if nome in "hij":
                grupo.pack_forget()

        self.grupo_intervalo = tk.Frame(self.pagina_funcoes, bg=PAINEL)
        self.texto(self.grupo_intervalo, "INTERVALO", 9, SUAVE, True).pack(
            anchor="w", pady=(11, 0)
        )
        self.criar_par_de_campos(
            self.grupo_intervalo,
            (("inicio", "Início", "-5"), ("fim", "Fim", "5")),
        )
        self.grupo_intervalo.pack(fill="x")

        BotaoArredondado(
            self.pagina_funcoes, "GERAR GRÁFICO  ↗", self.gerar_grafico
        ).pack(fill="x", pady=(14, 6))
        BotaoArredondado(
            self.pagina_visual, "SALVAR GRÁFICO  ↓", self.salvar_grafico, contorno=True
        ).pack(fill="x", pady=(0, 12))

        tk.Frame(self.pagina_analises, bg=BORDA, height=1).pack(fill="x")
        self.texto(
            self.pagina_analises, "ANÁLISE MATEMÁTICA", 11, DESTAQUE, True
        ).pack(anchor="w", pady=(12, 8))
        self.resultado = tk.StringVar(value="")
        tk.Label(
            self.pagina_analises, textvariable=self.resultado,
            bg=PAINEL, fg=TEXTO, anchor="nw", justify="left",
            font=("DejaVu Sans", 10), wraplength=275,
        ).pack(anchor="w", fill="x", pady=(0, 15))

        painel_grafico = CartaoArredondado(corpo, raio=24, margem=17)
        painel_grafico.pack(side="left", fill="both", expand=True)
        direita = painel_grafico.conteudo
        cabecalho_grafico = tk.Frame(direita, bg=PAINEL)
        cabecalho_grafico.pack(fill="x", pady=(2, 4))
        self.texto(
            cabecalho_grafico, "VISUALIZAÇÃO CARTESIANA", 11, SUAVE, True
        ).pack(side="left")
        self.texto(
            cabecalho_grafico, "GRÁFICO INTERATIVO", 8, DESTAQUE, True
        ).pack(side="right")

        navegacao = tk.Frame(direita, bg=PAINEL)
        navegacao.pack(fill="x", pady=(5, 7))
        self.botao_mover = BotaoModo(
            navegacao, "MOVER", self.alternar_mover, altura=36
        )
        self.botao_mover.configure(width=105)
        self.botao_mover.pack(side="left", padx=(0, 6))
        self.botao_zoom = BotaoModo(
            navegacao, "ZOOM", self.alternar_zoom, altura=36
        )
        self.botao_zoom.configure(width=105)
        self.botao_zoom.pack(side="left")
        self.botao_restaurar = BotaoArredondado(
            navegacao, "RESTAURAR VISÃO",
            self.restaurar_visualizacao, contorno=True,
        )
        self.botao_restaurar.configure(width=176, height=36)
        self.botao_restaurar.itemconfigure(
            self.botao_restaurar.fundo, outline="#64748b", width=2,
        )
        self.botao_restaurar.pack(side="right")

        self.texto(
            direita, "Clique nos pontos notáveis para aproximar. Use Mover ou Zoom para navegar.",
            9, SUAVE,
        ).pack(anchor="w", pady=(0, 8))
        self.area_grafico = tk.Frame(direita, bg=PAINEL)
        self.area_grafico.pack(fill="both", expand=True)

        self.vincular_rolagem(interno)
        self.vincular_rolagem(rolagem)
        self.vincular_rolagem(barra_rolagem)

        self.status = tk.StringVar(value="Pronto")
        tk.Label(
            self.janela, textvariable=self.status, bg=FUNDO,
            fg=SUAVE, anchor="w", font=("DejaVu Sans", 9),
            padx=28, pady=11,
        ).pack(fill="x")

    def alternar_parametros(self):
        if self.parametros_visiveis:
            self.painel_parametros.pack_forget()
            self.parametros_visiveis = False
        else:
            self.painel_parametros.pack(
                side="left", fill="y", padx=(0, 9),
                before=self.faixa_alternancia,
            )
            self.parametros_visiveis = True

        self.botao_recolher.definir_recolhido(not self.parametros_visiveis)
        self.janela.update_idletasks()
        if self.canvas is not None:
            self.canvas.draw_idle()

    def ajustar_tangente_slider(self, valor):
        self.campo_tangente_x.set(f"{valor:g}")
        if self.atualizacao_tangente_pendente is not None:
            self.janela.after_cancel(self.atualizacao_tangente_pendente)
        if self.tangente_ativa:
            self.atualizacao_tangente_pendente = self.janela.after(
                120, self.atualizar_tangente_com_slider,
            )

    def atualizar_tangente_com_slider(self):
        self.atualizacao_tangente_pendente = None
        if self.tangente_ativa:
            self.tracar_tangente(silencioso=True)

    def sincronizar_tangente_slider(self):
        try:
            valor = float(self.campo_tangente_x.get().replace(",", "."))
            self.slider_tangente.definir(valor)
        except (ValueError, OverflowError):
            return

    def fechar_menus(self):
        for seletor in getattr(self, "seletores_intersecoes", ()):
            seletor.fechar_menu()
        seletor_tangente = getattr(self, "seletor_tangente", None)
        if seletor_tangente is not None:
            seletor_tangente.fechar_menu()

    def atualizar_rolagem(self, inicio, fim):
        self.barra_rolagem.set(inicio, fim)
        self.fechar_menus()

    def rolar_painel(self, direcao):
        self.fechar_menus()
        self.rolagem.yview_scroll(direcao, "units")
        return "break"

    def vincular_rolagem(self, widget):
        widget.bind(
            "<Button-4>", lambda _evento: self.rolar_painel(-3), add="+"
        )
        widget.bind(
            "<Button-5>", lambda _evento: self.rolar_painel(3), add="+"
        )
        widget.bind(
            "<MouseWheel>",
            lambda evento: self.rolar_painel(
                -3 if evento.delta > 0 else 3
            ),
            add="+",
        )
        for filho in widget.winfo_children():
            self.vincular_rolagem(filho)

    @property
    def nomes_ativos(self):
        return "fghij"[:self.quantidade_funcoes]

    def definir_quantidade(self, quantidade):
        if not 1 <= quantidade <= 5 or quantidade == self.quantidade_funcoes:
            return
        self.quantidade_funcoes = quantidade
        for indice, nome in enumerate("fghij"):
            grupo = self.grupos_funcoes[nome]
            if indice < quantidade and not grupo.winfo_manager():
                grupo.pack(fill="x", before=self.grupo_intervalo)
            elif indice >= quantidade and grupo.winfo_manager():
                grupo.pack_forget()
        self.botao_uma.definir_selecionado(quantidade == 1)
        self.botao_duas.definir_selecionado(quantidade == 2)
        self.indicador_funcoes.configure(text=f"{quantidade} de 5 funções")
        self.atualizar_botoes_visibilidade()
        self.atualizar_seletores_intersecoes()
        self.seletor_tangente.atualizar_opcoes(tuple(self.nomes_ativos), True)
        if self.funcao_tangente.get() not in self.nomes_ativos:
            self.funcao_tangente.set(self.nomes_ativos[0])
            self.tangente_ativa = False
            self.tangente_resumo.set("Escolha a função e o valor de x.")
        self.gerar_grafico()

    def atualizar_seletores_intersecoes(self):
        nomes = tuple(self.nomes_ativos)
        for seletor in self.seletores_intersecoes:
            seletor.atualizar_opcoes(nomes, len(nomes) >= 2)
        if len(nomes) < 2:
            return
        if self.primeira_intersecao.get() not in nomes:
            self.primeira_intersecao.set(nomes[0])
        if self.segunda_intersecao.get() not in nomes:
            self.segunda_intersecao.set(nomes[1])
        if self.primeira_intersecao.get() == self.segunda_intersecao.get():
            self.segunda_intersecao.set(
                next(n for n in nomes if n != self.primeira_intersecao.get())
            )

    def alterar_par_intersecoes(self, _evento):
        if self.primeira_intersecao.get() == self.segunda_intersecao.get():
            opcoes = tuple(self.nomes_ativos)
            self.segunda_intersecao.set(
                next(n for n in opcoes if n != self.primeira_intersecao.get())
            )
        self.gerar_grafico()

    def alterar_modo(self, modo):
        self.definir_quantidade(1 if modo == "uma" else 2)

    def adicionar_funcao(self):
        self.definir_quantidade(self.quantidade_funcoes + 1)

    def remover_funcao(self):
        self.definir_quantidade(self.quantidade_funcoes - 1)

    def alterar_tipo(self, nome, tipo):
        if self.tipos[nome] == tipo:
            return
        self.tipos[nome] = tipo
        for nome_tipo, botao in self.botoes_tipo[nome].items():
            botao.definir_selecionado(nome_tipo == tipo)
        if tipo == "Expressão":
            self.campos_ab[nome].pack_forget()
            self.campos_c[nome].pack_forget()
            self.campos_expressao[nome].pack(fill="x", pady=(4, 0))
        else:
            self.campos_expressao[nome].pack_forget()
            self.campos_ab[nome].pack(fill="x", pady=(5, 0))
            if tipo == "Quadrática":
                self.campos_c[nome].pack(fill="x", pady=(4, 0))
                self.rotulos[f"a{nome}"].configure(text="a · x²")
                self.rotulos[f"b{nome}"].configure(text="b · x")
            else:
                self.campos_c[nome].pack_forget()
                self.rotulos[f"a{nome}"].configure(text="a · angular")
                self.rotulos[f"b{nome}"].configure(text="b · linear")
        if nome in self.nomes_ativos:
            self.gerar_grafico()

    def ler_numero(self, chave):
        valor = float(self.campos[chave].get().strip().replace(",", "."))
        if not math.isfinite(valor):
            raise ValueError("Use apenas números finitos.")
        return valor

    def obter_polinomio(self, nome):
        if self.tipos[nome] == "Expressão":
            return Expressao(self.campos[f"expressao_{nome}"].get())
        a = self.ler_numero(f"a{nome}")
        b = self.ler_numero(f"b{nome}")
        c = self.ler_numero(f"c{nome}") if self.tipos[nome] == "Quadrática" else 0
        return criar_polinomio(self.tipos[nome], a, b, c)

    @staticmethod
    def formatar_numero(valor):
        if abs(valor) < 0.0000001:
            valor = 0.0
        return f"{valor:.4f}".rstrip("0").rstrip(".")

    def descrever_polinomio(self, nome, polinomio, raizes=None):
        if isinstance(polinomio, Expressao):
            if polinomio.polinomio is None:
                situacao, pontos = raizes or ("sem_raizes", [])
                if situacao == "todos":
                    descricao = "Função nula no intervalo analisado"
                elif situacao == "sem_raizes":
                    descricao = "Nenhuma raiz encontrada no intervalo (busca numérica)"
                else:
                    descricao = "Raízes numéricas: " + ", ".join(
                        f"{x:.6f}" for x in pontos[:12]
                    )
                    if len(pontos) > 12:
                        descricao += f" ... e mais {len(pontos) - 12}"
                return f"{nome}(x) = {polinomio.texto}\n{descricao}"
            descricao = self.descrever_polinomio(nome, polinomio.polinomio)
            linhas = descricao.split("\n")
            linhas[0] = f"{nome}(x) = {polinomio.texto}"
            return "\n".join(linhas)
        a, b, c = polinomio
        numero = self.formatar_numero
        if a == 0:
            formula = f"{nome}(x) = {numero(b)}x {('+' if c >= 0 else '-')} {numero(abs(c))}"
        else:
            formula = (
                f"{nome}(x) = {numero(a)}x² "
                f"{('+' if b >= 0 else '-')} {numero(abs(b))}x "
                f"{('+' if c >= 0 else '-')} {numero(abs(c))}"
            )

        linhas = [formula, descrever_comportamento(polinomio)]
        delta = discriminante(polinomio)
        if delta is not None:
            linhas.append(f"Δ = {numero(delta)}")
        linhas.append(f"Raízes: {descrever_raizes_polinomio(polinomio)}")
        ponto = vertice(polinomio)
        if ponto is not None:
            vx, vy = ponto
            linhas.append(f"Vértice: ({numero(vx)}, {numero(vy)})")
        return "\n".join(linhas)

    def gerar_grafico(self, silencioso=False):
        if self.atualizacao_pendente is not None:
            self.janela.after_cancel(self.atualizacao_pendente)
            self.atualizacao_pendente = None
        try:
            funcoes = [
                (nome, self.obter_polinomio(nome)) for nome in self.nomes_ativos
            ]

            inicio = int(self.campos["inicio"].get())
            fim = int(self.campos["fim"].get())
            if inicio >= fim:
                raise ValueError("O início deve ser menor que o fim.")
            if fim - inicio > 1000:
                raise ValueError("O intervalo deve ter até 1000 unidades.")

            for _, funcao in funcoes:
                polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
                if polinomio is None:
                    continue
                valores = [discriminante(polinomio)]
                valores.extend(vertice(polinomio) or ())
                for valor in valores:
                    if valor is not None and not math.isfinite(valor):
                        raise ValueError("Os coeficientes geraram números muito grandes.")

            raizes_por_funcao = {
                nome: encontrar_raizes(funcao, inicio, fim)
                for nome, funcao in funcoes
            }
            extremos_por_funcao = {
                nome: encontrar_extremos(funcao, inicio, fim)
                for nome, funcao in funcoes
            }

            par = (
                self.primeira_intersecao.get(), self.segunda_intersecao.get(),
            )
            intersecoes = None
            if len(funcoes) >= 2:
                disponiveis = dict(funcoes)
                if par[0] not in disponiveis or par[1] not in disponiveis:
                    raise ValueError("Selecione duas funções disponíveis.")
                intersecoes = encontrar_intersecoes(
                    disponiveis[par[0]], disponiveis[par[1]], inicio, fim,
                )

            nova_figura = desenhar_funcoes(
                funcoes, inicio, fim, mostrar=False, tema_escuro=True,
                intersecoes=intersecoes, par_intersecoes=par,
                raizes=raizes_por_funcao, extremos=extremos_por_funcao,
            )

        except (ValueError, OverflowError, ZeroDivisionError) as erro:
            if silencioso:
                self.status.set(f"Ajuste os valores: {erro}")
            else:
                messagebox.showerror("Entrada inválida", str(erro))
            return

        descricoes = [
            self.descrever_polinomio(nome, polinomio, raizes_por_funcao[nome])
            for nome, polinomio in funcoes
        ]
        if intersecoes is not None:
            situacao, pontos = intersecoes
            if situacao == "coincidentes":
                texto_intersecao = "Curvas coincidentes no intervalo analisado"
            elif situacao == "sem_intersecao":
                texto_intersecao = "Nenhuma interseção encontrada no intervalo"
            else:
                texto_intersecao = "\n".join(
                    f"({x:.6f}, {y:.6f})" for x, y in pontos[:12]
                )
                if len(pontos) > 12:
                    texto_intersecao += f"\n... e mais {len(pontos) - 12} ponto(s)"
            descricoes.append(
                f"INTERSEÇÕES {par[0]}/{par[1]}\n{texto_intersecao}"
            )
        resumo_extremos = []
        for nome, pontos in extremos_por_funcao.items():
            for tipo, x, y in pontos[:10]:
                titulo = "Máximo" if tipo == "maximo" else "Mínimo"
                resumo_extremos.append(
                    f"{titulo} de {nome}(x): ({x:.6f}, {y:.6f})"
                )
            if len(pontos) > 10:
                resumo_extremos.append(
                    f"{nome}(x): e mais {len(pontos) - 10} ponto(s)"
                )
        descricoes.append(
            "MÁXIMOS E MÍNIMOS LOCAIS\n" + (
                "\n".join(resumo_extremos)
                if resumo_extremos else "Nenhum extremo local encontrado no intervalo"
            )
        )
        self.resultado.set("\n\n".join(descricoes))

        if self.foco_pontos is not None:
            self.foco_pontos.desconectar()
            self.foco_pontos = None
        if self.cursor_precisao is not None:
            self.cursor_precisao.desconectar()
            self.cursor_precisao = None
        if self.toolbar is not None:
            self.toolbar.destroy()
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        if self.figura is not None:
            plt.close(self.figura)

        self.figura = nova_figura
        self.funcoes_atuais = dict(funcoes)
        self.intervalo_atual = (inicio, fim)
        self.tangente_artistas = []
        self.figura.set_tight_layout(True)
        self.canvas = FigureCanvasTkAgg(
            self.figura, master=self.area_grafico
        )
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.area_grafico, pack_toolbar=False
        )
        self.toolbar.update()
        self.atualizar_navegacao()

        numero_funcoes = len(funcoes)
        self.status.set(
            f"Gráfico atualizado  •  {numero_funcoes} "
            f"{'função' if numero_funcoes == 1 else 'funções'}"
            f"  •  Intervalo [{inicio}, {fim}]"
        )
        self.cursor_precisao = CursorPrecisao(
            self.canvas, funcoes, self.toolbar, self.status,
            self.visibilidade_funcoes, self.visibilidade_elementos,
        )
        self.foco_pontos = FocoPontosNotaveis(
            self.canvas, funcoes, intersecoes, par, self.toolbar,
            self.cursor_precisao, self.status, raizes=raizes_por_funcao,
            extremos=extremos_por_funcao,
            visibilidade_funcoes=self.visibilidade_funcoes,
            visibilidade_elementos=self.visibilidade_elementos,
        )
        self.cursor_precisao.foco = self.foco_pontos
        if self.tangente_ativa:
            self.tracar_tangente(silencioso=True)
        else:
            self.aplicar_visibilidade()

    def remover_tangente(self):
        for artista in self.tangente_artistas:
            artista.remove()
        self.tangente_artistas.clear()
        if self.foco_pontos is not None:
            self.foco_pontos.remover_ponto_tangente()

    def tracar_tangente(self, silencioso=False):
        if self.figura is None:
            return
        try:
            nome = self.funcao_tangente.get()
            if nome not in self.funcoes_atuais:
                raise ValueError("Selecione uma função ativa.")
            try:
                x = float(self.campo_tangente_x.get().strip().replace(",", "."))
            except ValueError:
                raise ValueError("Digite um número válido para x.") from None
            if not math.isfinite(x):
                raise ValueError("Digite um valor finito para x.")
            if not self.intervalo_atual[0] <= x <= self.intervalo_atual[1]:
                raise ValueError("O valor de x deve estar dentro do intervalo do gráfico.")
            y, inclinacao = calcular_tangente(self.funcoes_atuais[nome], x)
        except (ValueError, OverflowError, ZeroDivisionError) as erro:
            if silencioso:
                self.remover_tangente()
                self.tangente_ativa = False
                self.tangente_resumo.set(f"Tangente indisponível: {erro}")
                self.aplicar_visibilidade()
            else:
                self.remover_tangente()
                self.tangente_ativa = False
                self.tangente_resumo.set("Tangente indisponível no ponto escolhido.")
                self.aplicar_visibilidade()
                messagebox.showerror("Derivada indisponível", str(erro))
            return

        self.remover_tangente()
        eixo = self.figura.axes[0]
        cor = "#fb923c"
        linha = eixo.axline(
            (x, y), slope=inclinacao, color=cor,
            linestyle="--", linewidth=2.0,
            label=f"Tangente de {nome}(x)", zorder=10,
        )
        ponto = eixo.scatter(
            [x], [y], color=cor, edgecolors="#ffffff", linewidths=1.2,
            s=95, zorder=11, label="_nolegend_",
        )
        for artista in (linha, ponto):
            artista.set_gid(f"tangente:{nome}")
        self.tangente_artistas = [linha, ponto]
        if self.foco_pontos is not None:
            self.foco_pontos.definir_ponto_tangente(nome, x, y)
        self.tangente_ativa = True
        self.tangente_resumo.set(
            f"{nome}'({x:.4f}) = {inclinacao:.6f}\n"
            f"Ponto: ({x:.6f}, {y:.6f})"
        )
        self.aplicar_visibilidade()
        self.status.set(
            f"Tangente de {nome}(x) em x = {x:.4f} "
            f"• inclinação = {inclinacao:.6f}"
        )

    def atualizar_navegacao(self):
        modo = getattr(self.toolbar.mode, "name", "NONE") if self.toolbar else "NONE"
        self.botao_mover.definir_selecionado(modo == "PAN")
        self.botao_zoom.definir_selecionado(modo == "ZOOM")

    def alternar_mover(self):
        if self.toolbar is None:
            return
        if self.toolbar.mode.name == "ZOOM":
            self.toolbar.zoom()
        self.toolbar.pan()
        self.atualizar_navegacao()
        if self.toolbar.mode.name == "PAN":
            self.status.set("Mover ativo  •  arraste para deslocar o gráfico")
        elif self.cursor_precisao is not None:
            self.status.set(self.cursor_precisao.status_base)

    def alternar_zoom(self):
        if self.toolbar is None:
            return
        if self.toolbar.mode.name == "PAN":
            self.toolbar.pan()
        self.toolbar.zoom()
        self.atualizar_navegacao()
        if self.toolbar.mode.name == "ZOOM":
            self.status.set("Zoom ativo  •  arraste para selecionar uma região")
        elif self.cursor_precisao is not None:
            self.status.set(self.cursor_precisao.status_base)

    def restaurar_visualizacao(self):
        if self.toolbar is not None:
            if self.toolbar.mode.name == "PAN":
                self.toolbar.pan()
            elif self.toolbar.mode.name == "ZOOM":
                self.toolbar.zoom()
            self.atualizar_navegacao()
        if self.foco_pontos is not None:
            self.foco_pontos.restaurar()

    def salvar_grafico(self):
        if self.figura is None:
            messagebox.showwarning("Sem gráfico", "Gere um gráfico antes de salvar.")
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar gráfico como PNG",
            defaultextension=".png",
            filetypes=[("Imagem PNG", "*.png")],
            initialfile="grafico_funcoes.png",
            parent=self.janela,
        )
        if not caminho:
            return

        try:
            self.figura.savefig(
                caminho,
                format="png",
                dpi=220,
                facecolor=self.figura.get_facecolor(),
                bbox_inches="tight",
            )
        except (OSError, ValueError, RuntimeError) as erro:
            messagebox.showerror("Erro ao salvar", f"Não foi possível salvar o gráfico.\n\n{erro}")
            return

        self.status.set(f"Gráfico salvo em: {caminho}")
        messagebox.showinfo("Gráfico salvo", "Imagem PNG exportada com sucesso.")


if __name__ == "__main__":
    janela = tk.Tk()
    app = ExploradorApp(janela)
    janela.mainloop()