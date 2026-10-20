# 📈 Explorador de Funções

Aplicação em **Python** para analisar e comparar funções afins e quadráticas com gráficos interativos.

## Sobre o projeto

O Explorador de Funções permite estudar **uma função isoladamente** ou **comparar duas funções**, escolhendo de forma independente se cada uma é afim (`ax + b`) ou quadrática (`ax² + bx + c`).

A versão **2.3** acrescenta parábolas, discriminante, raízes reais, vértice e interseções entre retas e parábolas. O aplicativo mantém a interface escura com bordas arredondadas.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Alternância entre os modos **1 função** e **2 funções**.
- Seleção independente de função **afim** ou **quadrática** para `f(x)` e `g(x)`.
- Campos de coeficientes que se adaptam ao tipo selecionado.
- Gráficos interativos com zoom e movimentação.
- Identificação de raízes reais e, para quadráticas, cálculo do discriminante **Δ** e do vértice.
- Indicação da concavidade de parábolas e do comportamento de funções afins.
- Identificação de **zero, uma ou duas interseções** entre as funções, ou de curvas coincidentes.
- Destaque das raízes, dos vértices e das interseções presentes no intervalo visualizado.
- Validação dos coeficientes e do intervalo, com mensagens para entradas inválidas.
- Versão tradicional de terminal preservada para comparação entre duas funções afins.

## Tecnologias utilizadas

- **Python** — cálculos matemáticos e organização do programa.
- **Tkinter** — interface gráfica.
- **Matplotlib** — gráficos e ferramentas de navegação.
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

Selecione uma ou duas funções e escolha **Afim** ou **Quadrática** para cada uma. No modo quadrático, o campo do coeficiente `c` aparece automaticamente.

A versão de terminal continua disponível para comparação de **duas funções afins**:

```bash
python explorador.py
```

## Organização do código

- **`matematica.py`** — cálculo de raízes, discriminante, vértice e interseções.
- **`visualizacao.py`** — desenho de retas, parábolas e pontos notáveis.
- **`interface.py`** — seleção de tipos, controles e apresentação dos resultados.
- **`explorador.py`** — versão original no terminal.

## Próximos passos

- Exportação do gráfico como imagem.
- Melhorias na edição e no gerenciamento das funções.
- Expansão para outros tipos de funções.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.