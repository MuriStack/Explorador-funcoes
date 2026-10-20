# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos matemáticos interativos.

## Sobre o projeto

O Explorador de Funções permite visualizar **uma a cinco funções simultâneas**, definidas por coeficientes ou expressões matemáticas digitadas diretamente. A versão **2.7** adiciona um **cursor de precisão** para identificar pontos das curvas com seis casas decimais, sem alterar os recursos anteriores.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Visualização de **1 a 5 funções** no mesmo plano cartesiano, usando **+ ADICIONAR** e **− REMOVER**.
- Modos **Afim**, **Quadrática** e **Expressão** para cada função, independentemente.
- **Cursor de precisão:** ao aproximar o mouse de uma curva, o programa destaca o ponto e mostra as coordenadas `x` e `y` com seis casas decimais.
- Exibição das coordenadas livres do mouse na barra inferior quando ele está no gráfico, mas longe das curvas.
- O cursor ignora resultados indefinidos e não interfere nas ferramentas de zoom e movimentação.
- Barra de rolagem lateral minimalista, utilizável com a roda do mouse e por arraste.
- Raízes, vértices e interseções de **f(x) e g(x)** para polinômios de grau até 2.
- Cálculo de discriminante e indicação do comportamento das funções aplicáveis.
- Intervalo configurável, gráficos interativos e exportação em PNG.
- Tratamento de entradas inválidas e preservação da versão de terminal.

## Como usar o cursor de precisão

1. Execute a interface e gere um gráfico.
2. Mova o mouse **perto de uma curva**, sem ativar o modo de zoom ou movimentação.
3. Um ponto colorido aparece na curva com as coordenadas de até **6 casas decimais**.
4. Ao afastar o cursor, a marcação desaparece. Fora das curvas, a barra inferior mostra a posição do mouse.

Os valores exibidos são calculados a partir da função na posição horizontal do cursor, e não apenas lidos dos pontos usados para desenhar a curva. Para funções com singularidades ou pontos fora do domínio real, não há indicação de ponto nessas posições.

## Tecnologias utilizadas

- **Python** — cálculos e organização do programa.
- **Tkinter** — interface gráfica e janela de seleção de arquivos.
- **Matplotlib** — gráficos interativos, navegação e exportação.
- **Git e GitHub** — versionamento do projeto.

## Estrutura do projeto

```text
Explorador-funcoes/
├── README.md
├── .gitignore
├── images/
│   └── interface.png
└── explorador-funcoes/
    ├── explorador.py
    ├── matematica.py
    ├── visualizacao.py
    ├── expressoes.py
    ├── cursor_precisao.py
    └── interface.py
```

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/MuriStack/Explorador-funcoes.git
cd Explorador-funcoes
```

### 2. Prepare o ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib
```

No Ubuntu e derivados, caso não tenha o Tkinter:

```bash
sudo apt install python3-tk
```

### 3. Abra a interface

```bash
cd explorador-funcoes
python interface.py
```

Selecione de uma a cinco funções e escolha **Afim**, **Quadrática** ou **Expressão** para cada uma. Gere o gráfico e aproxime o mouse de uma curva para visualizar o cursor de precisão. A opção **SALVAR GRÁFICO** exporta apenas o gráfico para PNG.

A versão de terminal continua disponível para comparar duas funções afins:

```bash
python explorador.py
```

## Como escrever expressões

Exemplos:

```text
x^2 - 4*x + 3
sin(x)
cos(x) + 2
log(x)
sqrt(x)
1/x
```

Use `*` para multiplicar, como em `2*x`. Tanto `^` quanto `**` representam potência. As funções trigonométricas trabalham em **radianos**. Constantes como `pi` e `e`, e funções como `tan`, `ln`, `exp` e `abs` também são aceitas.

## Organização do código

- **`matematica.py`** — cálculos de raízes, discriminante, vértice e interseções.
- **`visualizacao.py`** — desenho simultâneo de até cinco curvas e seus pontos notáveis.
- **`interface.py`** — controles, apresentação dos resultados e exportação.
- **`expressoes.py`** — avaliação controlada das expressões matemáticas.
- **`cursor_precisao.py`** — cálculo e apresentação das coordenadas durante o movimento do mouse.
- **`explorador.py`** — versão de terminal.

## Limitações atuais

- As interseções automáticas consideram apenas **f(x)** e **g(x)** quando são polinômios de grau até 2.
- Expressões não polinomiais são desenhadas e podem ser exploradas pelo cursor, mas ainda não contam com análise algébrica automática.
- Os valores apresentados possuem seis casas decimais de exibição, sujeitos à precisão numérica do Python.

## Próximos passos

- Permitir clicar em raízes, vértices e interseções para centralizar e aproximar o gráfico automaticamente.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.