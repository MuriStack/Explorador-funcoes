import math
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matematica import (
    calcular_intersecoes_polinomios,
    criar_polinomio,
    descrever_comportamento,
    descrever_raizes_polinomio,
    discriminante,
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


class ExploradorApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Explorador de Funções 2.4")
        self.janela.geometry("1300x820")
        self.janela.minsize(1000, 670)
        self.janela.configure(bg=FUNDO)

        self.figura = None
        self.canvas = None
        self.toolbar = None
        self.campos = {}
        self.modo = "duas"
        self.tipos = {"f": "Afim", "g": "Afim"}
        self.botoes_tipo = {}
        self.rotulos = {}
        self.campos_c = {}

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
        selecao_tipo = {}
        for tipo in ("Afim", "Quadrática"):
            botao = BotaoModo(
                selecao, tipo, lambda n=nome, t=tipo: self.alterar_tipo(n, t)
            )
            botao.pack(
                side="left", fill="x", expand=True,
                padx=(0, 5) if tipo == "Afim" else (5, 0),
            )
            selecao_tipo[tipo] = botao
        self.botoes_tipo[nome] = selecao_tipo
        selecao_tipo["Afim"].definir_selecionado(True)

        a, b, c = valores
        self.criar_par_de_campos(
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
        grupo.pack(fill="x")
        return grupo

    def criar_interface(self):
        topo = tk.Frame(self.janela, bg=FUNDO, padx=28, pady=20)
        topo.pack(fill="x")
        self.texto(topo, "EXPLORADOR DE FUNÇÕES", 20, TEXTO, True).pack(anchor="w")
        self.texto(
            topo, "Laboratório interativo de funções afins e quadráticas", 10, SUAVE
        ).pack(anchor="w", pady=(5, 0))

        corpo = tk.Frame(self.janela, bg=FUNDO, padx=24, pady=5)
        corpo.pack(fill="both", expand=True)

        barra = CartaoArredondado(corpo, largura=335, raio=24, margem=17)
        barra.pack(side="left", fill="y", padx=(0, 16))
        lateral = barra.conteudo

        rolagem = tk.Canvas(lateral, bg=PAINEL, highlightthickness=0, bd=0)
        rolagem.pack(side="left", fill="both", expand=True)
        barra_rolagem = tk.Scrollbar(
            lateral, orient="vertical", command=rolagem.yview,
            bg=CAMPO, troughcolor=PAINEL,
        )
        barra_rolagem.pack(side="right", fill="y")
        rolagem.configure(yscrollcommand=barra_rolagem.set)
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
        rolagem.bind("<Button-4>", lambda _evento: rolagem.yview_scroll(-3, "units"))
        rolagem.bind("<Button-5>", lambda _evento: rolagem.yview_scroll(3, "units"))
        rolagem.bind("<MouseWheel>", lambda evento: rolagem.yview_scroll(
            -1 if evento.delta > 0 else 1, "units"
        ))

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

        self.grupo_f = self.criar_grupo_funcao(interno, "f", ("2", "1", "0"))
        self.grupo_g = self.criar_grupo_funcao(interno, "g", ("-1", "4", "0"))

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
        self.texto(
            direita, "VISUALIZAÇÃO CARTESIANA", 11, SUAVE, True
        ).pack(anchor="w", pady=(2, 10))
        self.area_grafico = tk.Frame(direita, bg=PAINEL)
        self.area_grafico.pack(fill="both", expand=True)

        self.status = tk.StringVar(value="Pronto")
        tk.Label(
            self.janela, textvariable=self.status, bg=FUNDO,
            fg=SUAVE, anchor="w", font=("DejaVu Sans", 9),
            padx=28, pady=11,
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

    def alterar_tipo(self, nome, tipo):
        if self.tipos[nome] == tipo:
            return
        self.tipos[nome] = tipo
        for nome_tipo, botao in self.botoes_tipo[nome].items():
            botao.definir_selecionado(nome_tipo == tipo)
        if tipo == "Quadrática":
            self.campos_c[nome].pack(fill="x", pady=(4, 0))
            self.rotulos[f"a{nome}"].configure(text="a · x²")
            self.rotulos[f"b{nome}"].configure(text="b · x")
        else:
            self.campos_c[nome].pack_forget()
            self.rotulos[f"a{nome}"].configure(text="a · angular")
            self.rotulos[f"b{nome}"].configure(text="b · linear")
        if nome == "f" or self.modo == "duas":
            self.gerar_grafico()

    def ler_numero(self, chave):
        valor = float(self.campos[chave].get().strip().replace(",", "."))
        if not math.isfinite(valor):
            raise ValueError("Use apenas números finitos.")
        return valor

    def obter_polinomio(self, nome):
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
            funcoes = [("f", self.obter_polinomio("f"))]
            if self.modo == "duas":
                funcoes.append(("g", self.obter_polinomio("g")))

            inicio = int(self.campos["inicio"].get())
            fim = int(self.campos["fim"].get())
            if inicio >= fim:
                raise ValueError("O início deve ser menor que o fim.")
            if fim - inicio > 1000:
                raise ValueError("O intervalo deve ter até 1000 unidades.")

            for _, polinomio in funcoes:
                valores = [discriminante(polinomio)]
                valores.extend(vertice(polinomio) or ())
                for valor in valores:
                    if valor is not None and not math.isfinite(valor):
                        raise ValueError("Os coeficientes geraram números muito grandes.")

            intersecoes = None
            if len(funcoes) == 2:
                intersecoes = calcular_intersecoes_polinomios(
                    funcoes[0][1], funcoes[1][1]
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
            descricoes.append(f"INTERSEÇÕES\n{texto_intersecao}")
        self.resultado.set("\n\n".join(descricoes))

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
            f"Gráfico atualizado  •  "
            f"{'2 funções' if numero_funcoes == 2 else '1 função'}"
            f"  •  Intervalo [{inicio}, {fim}]"
        )

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