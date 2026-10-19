from matematica import analisar_funcao, calcular_intersecao
from visualizacao import exibir_grafico


def main():
    af = float(input("Digite o coeficiente angular de f(x): "))
    bf = float(input("Digite o coeficiente linear de f(x): "))

    ag = float(input("Digite o coeficiente angular de g(x): "))
    bg = float(input("Digite o coeficiente linear de g(x): "))

    analisar_funcao("f", af, bf)
    analisar_funcao("g", ag, bg)

    inicio = int(input("Onde o intervalo deve começar? "))
    fim = int(input("Onde o intervalo deve terminar? "))

    if inicio >= fim:
        print("Erro: o início deve ser menor que o fim.")
        return

    situacao, intersecao = calcular_intersecao(
        af, bf, ag, bg
    )

    if situacao == "coincidentes":
        print("As funções são coincidentes.")

    elif situacao == "paralelas":
        print("As funções são paralelas e não se cruzam.")

    else:
        x, y = intersecao

        print(f"Ponto de interseção: ({x}, {y})")

        if inicio <= x <= fim:
            print("O ponto está dentro do intervalo do gráfico.")
        else:
            print("O ponto está fora do intervalo do gráfico.")

    exibir_grafico(
        af, bf, ag, bg, inicio, fim, intersecao
    )


if __name__ == "__main__":
    main()
