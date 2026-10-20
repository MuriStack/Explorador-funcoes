import math
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from expressoes import Expressao
from matematica import (
    calcular_intersecoes_polinomios,
    criar_polinomio,
    descrever_comportamento,
    descrever_raizes_polinomio,
    discriminante,
    raizes_reais,
    vertice,
)
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

    def bind_enter(self, comando):
        self.entrada.bind("<Return>", lambda _evento: comando())


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
    def __init__(self, canvas, funcoes, toolbar, status):
        self.canvas = canvas
        self.eixo = canvas.figure.axes[0]
        self.funcoes = funcoes
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
    def __init__(self, canvas, funcoes, intersecoes, toolbar, cursor, status):
        self.canvas = canvas
        self.eixo = canvas.figure.axes[0]
        self.toolbar = toolbar
        self.cursor = cursor
        self.status = status
        self.limites_iniciais = (self.eixo.get_xlim(), self.eixo.get_ylim())
        self.selecionado = None
        self.pontos = []
        self.cores = {
            nome: linha.get_color()
            for (nome, _), linha in zip(funcoes, self.eixo.lines)
        }

        if intersecoes is not None and intersecoes[0] == "pontos":
            for x, y in intersecoes[1]:
                self.registrar("Interseção f/g", x, y, "#4ade80")

        for nome, funcao in funcoes:
            polinomio = funcao.polinomio if isinstance(funcao, Expressao) else funcao
            if polinomio is None:
                continue
            cor = self.cores[nome]
            ponto_vertice = vertice(polinomio)
            if ponto_vertice is not None:
                self.registrar(f"Vértice de {nome}(x)", *ponto_vertice, cor)
            for raiz in raizes_reais(polinomio):
                self.registrar(f"Raiz de {nome}(x)", raiz, 0.0, cor)

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

    def registrar(self, descricao, x, y, cor):
        if not math.isfinite(x) or not math.isfinite(y):
            return
        limite_x = self.eixo.get_xlim()
        if min(limite_x) <= x <= max(limite_x):
            self.pontos.append((descricao, x, y, cor))

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
        for descricao, x, y, cor in self.pontos:
            px, py = self.eixo.transData.transform((x, y))
            if not math.isfinite(px) or not math.isfinite(py):
                continue
            if not self.eixo.bbox.contains(px, py):
                continue
            distancia = math.hypot(evento.x - px, evento.y - py)
            if distancia < menor_distancia:
                menor_distancia = distancia
                candidato = (descricao, x, y, cor)

        if candidato is None:
            return

        descricao, x, y, cor = candidato
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
        self.janela.title("Explorador de Funções 2.8")
        self.janela.geometry("1300x820")
        self.janela.minsize(1000, 670)
        self.janela.configure(bg=FUNDO)

        self.figura = None
        self.canvas = None
        self.toolbar = None
        self.cursor_precisao = None
        self.foco_pontos = None
        self.campos = {}
        self.quantidade_funcoes = 2
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
        return linha

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

    def criar_interface(self):
        topo = tk.Frame(self.janela, bg=FUNDO, padx=28, pady=20)
        topo.pack(fill="x")
        self.texto(topo, "EXPLORADOR DE FUNÇÕES", 20, TEXTO, True).pack(anchor="w")
        self.texto(
            topo, "Laboratório interativo de gráficos matemáticos", 10, SUAVE
        ).pack(anchor="w", pady=(5, 0))

        corpo = tk.Frame(self.janela, bg=FUNDO, padx=24, pady=5)
        corpo.pack(fill="both", expand=True)

        barra = CartaoArredondado(corpo, largura=335, raio=24, margem=17)
        barra.pack(side="left", fill="y", padx=(0, 16))
        lateral = barra.conteudo

        rolagem = tk.Canvas(lateral, bg=PAINEL, highlightthickness=0, bd=0)
        barra_rolagem = BarraRolagemMinimalista(
            lateral, command=rolagem.yview,
        )
        barra_rolagem.pack(side="right", fill="y")
        rolagem.pack(side="left", fill="both", expand=True)
        rolagem.configure(yscrollcommand=barra_rolagem.set)
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

        self.texto(interno, "PARÂMETROS", 12, DESTAQUE, True).pack(
            anchor="w", pady=(0, 7)
        )
        self.texto(interno, "QUANTAS FUNÇÕES?", 9, SUAVE, True).pack(
            anchor="w", pady=(3, 5)
        )
        selecao_modo = tk.Frame(interno, bg=PAINEL)
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

        controles = tk.Frame(interno, bg=PAINEL)
        controles.pack(fill="x", pady=(8, 3))
        BotaoArredondado(
            controles, "+ ADICIONAR", self.adicionar_funcao, contorno=True
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        BotaoArredondado(
            controles, "− REMOVER", self.remover_funcao, contorno=True
        ).pack(side="left", fill="x", expand=True, padx=(4, 0))
        self.indicador_funcoes = self.texto(interno, "2 de 5 funções", 9, SUAVE)
        self.indicador_funcoes.pack(anchor="w", pady=(2, 0))

        self.grupos_funcoes = {}
        for nome, valores in (
            ("f", ("2", "1", "0")),
            ("g", ("-1", "4", "0")),
            ("h", ("1", "0", "0")),
            ("i", ("-2", "1", "0")),
            ("j", ("0", "3", "0")),
        ):
            grupo = self.criar_grupo_funcao(interno, nome, valores)
            self.grupos_funcoes[nome] = grupo
            if nome in "hij":
                grupo.pack_forget()

        self.grupo_intervalo = tk.Frame(interno, bg=PAINEL)
        self.texto(self.grupo_intervalo, "INTERVALO", 9, SUAVE, True).pack(
            anchor="w", pady=(11, 0)
        )
        self.criar_par_de_campos(
            self.grupo_intervalo,
            (("inicio", "Início", "-5"), ("fim", "Fim", "5")),
        )
        self.grupo_intervalo.pack(fill="x")

        BotaoArredondado(
            interno, "GERAR GRÁFICO  ↗", self.gerar_grafico
        ).pack(fill="x", pady=(14, 6))
        BotaoArredondado(
            interno, "SALVAR GRÁFICO  ↓", self.salvar_grafico, contorno=True
        ).pack(fill="x", pady=(0, 12))

        tk.Frame(interno, bg=BORDA, height=1).pack(fill="x")
        self.texto(
            interno, "ANÁLISE MATEMÁTICA", 11, DESTAQUE, True
        ).pack(anchor="w", pady=(12, 8))
        self.resultado = tk.StringVar(value="")
        tk.Label(
            interno, textvariable=self.resultado,
            bg=PAINEL, fg=TEXTO, anchor="nw", justify="left",
            font=("DejaVu Sans", 10), wraplength=275,
        ).pack(anchor="w", fill="x", pady=(0, 15))

        painel_grafico = CartaoArredondado(corpo, raio=24, margem=17)
        painel_grafico.pack(side="right", fill="both", expand=True)
        direita = painel_grafico.conteudo
        cabecalho_grafico = tk.Frame(direita, bg=PAINEL)
        cabecalho_grafico.pack(fill="x", pady=(2, 4))
        self.texto(
            cabecalho_grafico, "VISUALIZAÇÃO CARTESIANA", 11, SUAVE, True
        ).pack(side="left")
        self.botao_restaurar = BotaoArredondado(
            cabecalho_grafico, "RESTAURAR VISÃO",
            self.restaurar_visualizacao, contorno=True,
        )
        self.botao_restaurar.configure(width=176, height=36)
        self.botao_restaurar.itemconfigure(
            self.botao_restaurar.fundo, outline="#64748b", width=2,
        )
        self.botao_restaurar.pack(side="right")
        self.texto(
            direita, "Clique em uma raiz, vértice ou interseção para aproximar.",
            9, SUAVE,
        ).pack(anchor="w", pady=(0, 9))
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

    def rolar_painel(self, direcao):
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

    def descrever_polinomio(self, nome, polinomio):
        if isinstance(polinomio, Expressao):
            if polinomio.polinomio is None:
                return (
                    f"{nome}(x) = {polinomio.texto}\n"
                    "Análise algébrica disponível para polinômios de grau até 2."
                )
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

    def gerar_grafico(self):
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

            intersecoes = None
            polinomios = [
                funcao.polinomio if isinstance(funcao, Expressao) else funcao
                for _, funcao in funcoes
            ]
            if len(funcoes) >= 2 and all(p is not None for p in polinomios[:2]):
                intersecoes = calcular_intersecoes_polinomios(
                    polinomios[0], polinomios[1]
                )
                if not all(
                    math.isfinite(valor)
                    for ponto in intersecoes[1] for valor in ponto
                ):
                    raise ValueError("A interseção gerou números muito grandes.")

            nova_figura = desenhar_funcoes(
                funcoes, inicio, fim, mostrar=False, tema_escuro=True
            )

        except (ValueError, OverflowError, ZeroDivisionError) as erro:
            messagebox.showerror("Entrada inválida", str(erro))
            return

        descricoes = [
            self.descrever_polinomio(nome, polinomio)
            for nome, polinomio in funcoes
        ]
        if intersecoes is not None:
            situacao, pontos = intersecoes
            if situacao == "coincidentes":
                texto_intersecao = "Curvas coincidentes"
            elif situacao == "sem_intersecao":
                texto_intersecao = "Sem interseção real"
            else:
                texto_intersecao = "\n".join(
                    f"({self.formatar_numero(x)}, {self.formatar_numero(y)})"
                    + (" · fora do intervalo" if not inicio <= x <= fim else "")
                    for x, y in pontos
                )
            descricoes.append(f"INTERSEÇÕES f/g\n{texto_intersecao}")
        if len(funcoes) >= 2 and intersecoes is None:
            descricoes.append(
                "INTERSEÇÕES f/g\nCálculo disponível para polinômios de grau até 2."
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
        self.canvas = FigureCanvasTkAgg(
            self.figura, master=self.area_grafico
        )
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.toolbar = NavigationToolbar2Tk(
            self.canvas, self.area_grafico, pack_toolbar=False
        )
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill="x")

        numero_funcoes = len(funcoes)
        self.status.set(
            f"Gráfico atualizado  •  {numero_funcoes} "
            f"{'função' if numero_funcoes == 1 else 'funções'}"
            f"  •  Intervalo [{inicio}, {fim}]"
        )
        self.cursor_precisao = CursorPrecisao(
            self.canvas, funcoes, self.toolbar, self.status
        )
        self.foco_pontos = FocoPontosNotaveis(
            self.canvas, funcoes, intersecoes, self.toolbar,
            self.cursor_precisao, self.status,
        )
        self.cursor_precisao.foco = self.foco_pontos

    def restaurar_visualizacao(self):
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