import math
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)

from matematica import calcular_intersecao, classificar_funcao, descrever_raiz
from visualizacao import exibir_grafico


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
            bd=0, height=40, width=110,
        )
        self.borda = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1,
            fill=CAMPO, outline=BORDA, width=1,
        )
        self.entrada = tk.Entry(
            self, bg=CAMPO, fg=TEXTO, insertbackground=TEXTO,
            relief="flat", highlightthickness=0, bd=0,
            font=("DejaVu Sans", 11),
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
    def __init__(self, parent, texto, comando):
        super().__init__(
            parent, bg=PAINEL, height=48,
            highlightthickness=0, bd=0,
            cursor="hand2", takefocus=True,
        )
        self.comando = comando
        self.fundo = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1,
            fill=DESTAQUE, outline="",
        )
        self.rotulo = self.create_text(
            10, 24, text=texto, fill=FUNDO,
            font=("DejaVu Sans", 11, "bold"), anchor="center",
        )
        self.bind("<Configure>", self.ajustar)
        self.bind("<Enter>", lambda _evento: self.itemconfigure(self.fundo, fill="#7dd3fc"))
        self.bind("<Leave>", lambda _evento: self.itemconfigure(self.fundo, fill=DESTAQUE))
        self.bind("<Button-1>", lambda _evento: self.comando())
        self.bind("<Return>", lambda _evento: self.comando())
        self.bind("<space>", lambda _evento: self.comando())
        self.bind("<FocusIn>", lambda _evento: self.itemconfigure(self.fundo, outline=TEXTO, width=2))
        self.bind("<FocusOut>", lambda _evento: self.itemconfigure(self.fundo, outline="", width=0))

    def ajustar(self, evento):
        self.coords(
            self.fundo,
            *pontos_arredondados(1, 1, evento.width - 1, evento.height - 1, 14),
        )
        self.coords(self.rotulo, evento.width / 2, evento.height / 2)


class BotaoModo(tk.Canvas):
    def __init__(self, parent, texto, comando):
        super().__init__(
            parent, bg=PAINEL, height=40, width=120,
            highlightthickness=0, bd=0, cursor="hand2", takefocus=True,
        )
        self.comando = comando
        self.selecionado = False
        self.fundo = self.create_polygon(
            0, 0, 1, 0, 1, 1, 0, 1, fill=CAMPO, outline="",
        )
        self.rotulo = self.create_text(
            10, 20, text=texto, fill=SUAVE,
            font=("DejaVu Sans", 10, "bold"), anchor="center",
        )
        self.bind("<Configure>", self.ajustar)
        self.bind("<Button-1>", lambda _evento: self.comando())
        self.bind("<Return>", lambda _evento: self.comando())
        self.bind("<space>", lambda _evento: self.comando())

    def ajustar(self, evento):
        self.coords(
            self.fundo,
            *pontos_arredondados(1, 1, evento.width - 1, evento.height - 1, 12),
        )
        self.coords(self.rotulo, evento.width / 2, evento.height / 2)

    def definir_selecionado(self, selecionado):
        self.selecionado = selecionado
        self.itemconfigure(self.fundo, fill=DESTAQUE if selecionado else CAMPO)
        self.itemconfigure(self.rotulo, fill=FUNDO if selecionado else SUAVE)


class ExploradorApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Explorador de Funções 2.2")
        self.janela.geometry("1280x800")
        self.janela.minsize(990, 660)
        self.janela.configure(bg=FUNDO)

        self.figura = None
        self.canvas = None
        self.toolbar = None
        self.campos = {}
        self.modo = "duas"

        self.criar_interface()
        self.gerar_grafico()

    @staticmethod
    def texto(parent, conteudo, tamanho=11, cor=TEXTO, negrito=False):
        return tk.Label(
            parent, text=conteudo, bg=parent["bg"], fg=cor,
            font=("DejaVu Sans", tamanho, "bold" if negrito else "normal"),
            anchor="w", justify="left",
        )

    def criar_grupo(self, parent, titulo, campos):
        grupo = tk.Frame(parent, bg=PAINEL)
        self.texto(grupo, titulo, 9, SUAVE, True).pack(anchor="w", pady=(8, 3))
        linha = tk.Frame(grupo, bg=PAINEL)
        linha.pack(fill="x")
        linha.columnconfigure(0, weight=1, uniform="campos")
        linha.columnconfigure(1, weight=1, uniform="campos")
        for indice, (chave, rotulo, valor) in enumerate(campos):
            coluna = tk.Frame(linha, bg=PAINEL)
            coluna.grid(
                row=0, column=indice, sticky="ew",
                padx=(0, 5) if indice == 0 else (5, 0),
            )
            self.texto(coluna, rotulo, 9, SUAVE).pack(anchor="w", pady=(0, 3))
            entrada = CampoArredondado(coluna, valor)
            entrada.pack(fill="x")
            entrada.bind_enter(self.gerar_grafico)
            self.campos[chave] = entrada
        grupo.pack(fill="x")
        return grupo

    def criar_interface(self):
        topo = tk.Frame(self.janela, bg=FUNDO, padx=28, pady=23)
        topo.pack(fill="x")
        self.texto(topo, "EXPLORADOR DE FUNÇÕES", 20, TEXTO, True).pack(anchor="w")
        self.texto(
            topo, "Laboratório interativo de funções afins", 10, SUAVE
        ).pack(anchor="w", pady=(6, 0))

        corpo = tk.Frame(self.janela, bg=FUNDO, padx=24, pady=6)
        corpo.pack(fill="both", expand=True)

        barra = CartaoArredondado(corpo, largura=310, raio=24, margem=21)
        barra.pack(side="left", fill="y", padx=(0, 16))
        lateral = barra.conteudo

        self.texto(lateral, "PARÂMETROS", 12, DESTAQUE, True).pack(
            anchor="w", pady=(0, 7)
        )
        self.texto(lateral, "QUANTAS FUNÇÕES?", 9, SUAVE, True).pack(
            anchor="w", pady=(3, 5)
        )
        selecao = tk.Frame(lateral, bg=PAINEL)
        selecao.pack(fill="x", pady=(0, 5))
        self.botao_uma = BotaoModo(
            selecao, "1 função", lambda: self.alterar_modo("uma")
        )
        self.botao_uma.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.botao_duas = BotaoModo(
            selecao, "2 funções", lambda: self.alterar_modo("duas")
        )
        self.botao_duas.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.botao_duas.definir_selecionado(True)

        self.grupo_f = self.criar_grupo(
            lateral, "FUNÇÃO f(x)",
            (("af", "a · angular", "2"), ("bf", "b · linear", "1")),
        )
        self.grupo_g = self.criar_grupo(
            lateral, "FUNÇÃO g(x)",
            (("ag", "a · angular", "-1"), ("bg", "b · linear", "4")),
        )
        self.grupo_intervalo = self.criar_grupo(
            lateral, "INTERVALO",
            (("inicio", "Início", "-5"), ("fim", "Fim", "5")),
        )

        BotaoArredondado(
            lateral, "GERAR GRÁFICO  ↗", self.gerar_grafico
        ).pack(fill="x", pady=(13, 10))

        tk.Frame(lateral, bg=BORDA, height=1).pack(fill="x")
        self.texto(
            lateral, "ANÁLISE MATEMÁTICA", 11, DESTAQUE, True
        ).pack(anchor="w", pady=(10, 7))

        self.resultado = tk.StringVar(value="")
        tk.Label(
            lateral, textvariable=self.resultado, bg=PAINEL, fg=TEXTO,
            anchor="nw", justify="left", font=("DejaVu Sans", 10),
            wraplength=255,
        ).pack(anchor="w", fill="x")

        painel_grafico = CartaoArredondado(corpo, raio=24, margem=17)
        painel_grafico.pack(side="right", fill="both", expand=True)
        direita = painel_grafico.conteudo
        self.texto(
            direita, "VISUALIZAÇÃO CARTESIANA", 11, SUAVE, True
        ).pack(anchor="w", pady=(2, 10))

        self.area_grafico = tk.Frame(direita, bg=PAINEL)
        self.area_grafico.pack(fill="both", expand=True)

        self.status = tk.StringVar(value="Pronto")
        tk.Label(
            self.janela, textvariable=self.status, bg=FUNDO,
            fg=SUAVE, anchor="w", font=("DejaVu Sans", 9),
            padx=28, pady=12,
        ).pack(fill="x")

    def alterar_modo(self, modo):
        if self.modo == modo:
            return
        self.modo = modo
        self.botao_uma.definir_selecionado(modo == "uma")
        self.botao_duas.definir_selecionado(modo == "duas")
        if modo == "uma":
            self.grupo_g.pack_forget()
        else:
            self.grupo_g.pack(fill="x", before=self.grupo_intervalo)
        self.gerar_grafico()

    def ler_coeficiente(self, chave):
        valor = float(self.campos[chave].get().strip().replace(",", "."))
        if not math.isfinite(valor):
            raise ValueError("Use apenas números finitos.")
        return valor

    def gerar_grafico(self):
        try:
            af = self.ler_coeficiente("af")
            bf = self.ler_coeficiente("bf")
            exibir_g = self.modo == "duas"
            ag = self.ler_coeficiente("ag") if exibir_g else None
            bg = self.ler_coeficiente("bg") if exibir_g else None

            inicio = int(self.campos["inicio"].get())
            fim = int(self.campos["fim"].get())
            if inicio >= fim:
                raise ValueError("O início deve ser menor que o fim.")
            if fim - inicio > 1000:
                raise ValueError("O intervalo deve ter até 1000 unidades.")

            situacao, intersecao = (
                calcular_intersecao(af, bf, ag, bg)
                if exibir_g else (None, None)
            )
            if intersecao is not None and not all(
                math.isfinite(v) for v in intersecao
            ):
                raise ValueError("Os resultados excederam o limite numérico.")

            nova_figura = exibir_grafico(
                af, bf, ag, bg, inicio, fim, intersecao,
                mostrar=False, tema_escuro=True, exibir_g=exibir_g,
            )
        except (ValueError, OverflowError) as erro:
            messagebox.showerror("Entrada inválida", str(erro))
            return

        descricao_f = (
            f"f(x) = {af:g}x + ({bf:g})\n"
            f"{classificar_funcao(af).capitalize()}\n"
            f"Raiz: {descrever_raiz(af, bf)}"
        )
        if exibir_g:
            if situacao == "coincidentes":
                descricao = "Retas coincidentes"
            elif situacao == "paralelas":
                descricao = "Retas paralelas"
            else:
                x, y = intersecao
                descricao = f"({x:.2f}, {y:.2f})"
                if not inicio <= x <= fim:
                    descricao += "\n(fora do intervalo)"
            descricao_f += (
                f"\n\ng(x) = {ag:g}x + ({bg:g})\n"
                f"{classificar_funcao(ag).capitalize()}\n"
                f"Raiz: {descrever_raiz(ag, bg)}\n\n"
                f"Interseção: {descricao}"
            )
        self.resultado.set(descricao_f)

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

        nome_modo = "1 função" if not exibir_g else "2 funções"
        self.status.set(
            f"Gráfico atualizado  •  {nome_modo}  •  Intervalo [{inicio}, {fim}]"
        )


if __name__ == "__main__":
    janela = tk.Tk()
    app = ExploradorApp(janela)
    janela.mainloop()