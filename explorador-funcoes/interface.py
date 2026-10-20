import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)

from matematica import (
    calcular_intersecao,
    classificar_funcao,
    descrever_raiz,
)
from visualizacao import exibir_grafico


class ExploradorApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Explorador de Funções 2.0")
        self.janela.geometry("1200x750")
        self.janela.minsize(850, 550)

        self.canvas = None
        self.toolbar = None
        self.figura = None

        self.criar_interface()
        self.gerar_grafico()

    def criar_interface(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        principal = ttk.Frame(self.janela, padding=16)
        principal.pack(fill="both", expand=True)

        titulo = ttk.Label(
            principal,
            text="Explorador de Funções",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w")

        subtitulo = ttk.Label(
            principal,
            text="Explore funções afins e visualize seus resultados"
        )
        subtitulo.pack(anchor="w", pady=(0, 16))

        conteudo = ttk.Frame(principal)
        conteudo.pack(fill="both", expand=True)

        lateral = ttk.Frame(conteudo, width=260)
        lateral.pack(side="left", fill="y", padx=(0, 16))
        lateral.pack_propagate(False)

        self.area_grafico = ttk.Frame(conteudo)
        self.area_grafico.pack(
            side="right", fill="both", expand=True
        )

        ttk.Label(
            lateral,
            text="Parâmetros",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 14))

        self.campos = {}

        parametros = [
            ("af", "Coeficiente a de f(x)", "2"),
            ("bf", "Coeficiente b de f(x)", "1"),
            ("ag", "Coeficiente a de g(x)", "-1"),
            ("bg", "Coeficiente b de g(x)", "4"),
            ("inicio", "Início do intervalo", "-5"),
            ("fim", "Fim do intervalo", "5"),
        ]

        for chave, rotulo, valor in parametros:
            ttk.Label(
                lateral, text=rotulo
            ).pack(anchor="w", pady=(6, 2))

            entrada = ttk.Entry(lateral)
            entrada.insert(0, valor)
            entrada.pack(fill="x")

            self.campos[chave] = entrada

        ttk.Button(
            lateral,
            text="Gerar gráfico",
            command=self.gerar_grafico
        ).pack(fill="x", pady=(20, 12))

        ttk.Separator(lateral).pack(fill="x", pady=12)

        ttk.Label(
            lateral,
            text="Análise matemática",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.resultado = tk.StringVar(value="")

        ttk.Label(
            lateral,
            textvariable=self.resultado,
            justify="left",
            wraplength=245
        ).pack(anchor="w", fill="x")

    def gerar_grafico(self):
        try:
            af = float(self.campos["af"].get().replace(",", "."))
            bf = float(self.campos["bf"].get().replace(",", "."))
            ag = float(self.campos["ag"].get().replace(",", "."))
            bg = float(self.campos["bg"].get().replace(",", "."))

            inicio = int(self.campos["inicio"].get())
            fim = int(self.campos["fim"].get())

            if inicio >= fim:
                raise ValueError(
                    "O início deve ser menor que o fim."
                )

            if fim - inicio > 1000:
                raise ValueError(
                    "Escolha um intervalo de até 1000 unidades."
                )

        except ValueError as erro:
            messagebox.showerror(
                "Entrada inválida",
                f"Verifique os valores informados.\n\n{erro}"
            )
            return

        situacao, intersecao = calcular_intersecao(
            af, bf, ag, bg
        )

        if situacao == "coincidentes":
            descricao_intersecao = "Retas coincidentes"

        elif situacao == "paralelas":
            descricao_intersecao = "Retas paralelas"

        else:
            x, y = intersecao
            descricao_intersecao = f"({x:.2f}, {y:.2f})"

        texto = (
            f"f(x) = {af:g}x + ({bf:g})\n"
            f"Tipo: {classificar_funcao(af)}\n"
            f"Raiz: {descrever_raiz(af, bf)}\n\n"
            f"g(x) = {ag:g}x + ({bg:g})\n"
            f"Tipo: {classificar_funcao(ag)}\n"
            f"Raiz: {descrever_raiz(ag, bg)}\n\n"
            f"Interseção:\n{descricao_intersecao}"
        )

        # Remove o gráfico anterior.
        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.figura is not None:
            plt.close(self.figura)

        # Cria um novo gráfico sem abrir outra janela.
        self.figura = exibir_grafico(
            af, bf, ag, bg,
            inicio, fim, intersecao,
            mostrar=False
        )

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=self.area_grafico
        )
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            side="top",
            fill="both",
            expand=True
        )

        self.toolbar = NavigationToolbar2Tk(
            self.canvas,
            self.area_grafico
        )
        self.toolbar.update()

        self.resultado.set(texto)


if __name__ == "__main__":
    janela = tk.Tk()
    app = ExploradorApp(janela)
    janela.mainloop()