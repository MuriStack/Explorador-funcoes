# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos matemáticos interativos.

## Sobre o projeto

O Explorador de Funções permite analisar **uma função isoladamente** ou **comparar até cinco funções**, inserindo coeficientes ou expressões matemáticas diretamente.

A versão **2.5** acrescentou a opção **Expressão**, que permite escrever funções como `x^2 - 4*x + 3`, `sin(x)`, `log(x)` e `1/x`. A versão **2.6** permite adicionar e remover curvas no mesmo gráfico, até cinco funções simultâneas (`f`, `g`, `h`, `i` e `j`), mantendo a exportação PNG e o tema escuro com bordas arredondadas.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Visualização de **1 a 5 funções** no mesmo plano cartesiano, usando **+ ADICIONAR** e **− REMOVER**.
- **Barra de rolagem lateral** visível, com suporte à roda do mouse sobre campos e botões para acessar todas as funções e análises.
- Atalhos **1 função** e **2 funções** para alternar rapidamente entre as quantidades mais comuns.
- Seleção independente de **Afim**, **Quadrática** ou **Expressão** para cada função ativa, de `f(x)` até `j(x)`, com a opção de expressão em uma linha própria para facilitar o uso.
- Campos adaptados para digitar coeficientes ou escrever a expressão diretamente.
- Gráficos interativos com zoom e movimentação.
- Destaque de raízes, vértices e interseções visíveis no intervalo.
- Cálculo do discriminante **Δ** e do vértice para funções quadráticas, inclusive expressões polinomiais reconhecidas.
- Classificação de funções afins e indicação da concavidade de parábolas.
- Cálculo de até duas interseções reais **entre f(x) e g(x)** quando ambas são polinômios de grau até 2. As demais funções têm gráficos, raízes e vértices próprios quando aplicáveis.
- Configuração do intervalo e atualização do gráfico sem reiniciar a aplicação.
- Exportação do gráfico atual como **imagem PNG** pela interface.
- Validação de entradas, com mensagens de erro.
- Versão tradicional de terminal preservada para comparar duas funções afins.

## Tecnologias utilizadas

- **Python** — cálculos e organização do programa.
- **Tkinter** — interface gráfica e janela de seleção do arquivo.
- **Matplotlib** — gráficos, navegação e exportação em PNG.
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
    ├── interface.py
    └── expressoes.py
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

Use **+ ADICIONAR** e **− REMOVER** para trabalhar com 1 a 5 funções (ou os atalhos **1 função** e **2 funções**). Para cada função ativa, escolha **Afim**, **Quadrática** ou **Expressão** e clique em **GERAR GRÁFICO**. Role o painel lateral com a **barra vertical ou a roda do mouse** para acessar as demais funções, os botões e a análise. O aplicativo conserva os campos das funções ocultas caso você volte a adicioná-las durante a mesma sessão.

### 4. Exporte um gráfico

1. Clique em **GERAR GRÁFICO** para atualizar a visualização.
2. Clique em **SALVAR GRÁFICO**.
3. Escolha a pasta e o nome do arquivo.
4. Confirme a gravação em **PNG**.

A imagem exportada contém **somente o gráfico**, sem o painel de controles da aplicação. Ela é independente da captura de tela usada na seção **Demonstração** do README.

A versão de terminal permanece disponível para comparar **duas funções afins**:

```bash
python explorador.py
```

## Como escrever expressões

Exemplos aceitos:

```text
x^2 - 4*x + 3
sin(x)
cos(x) + 2
log(x)
sqrt(x)
1/x
2*x + 5
```

Use `*` para multiplicar, como em `2*x`. Tanto `^` quanto `**` representam potência. As funções trigonométricas usam **radianos**. Também são aceitas as constantes `pi` e `e`, além das funções `tan`, `asin`, `acos`, `atan`, `ln`, `log10`, `exp` e `abs`.

As expressões são validadas antes da execução; trechos que não sejam operações ou funções matemáticas permitidas são rejeitados. Os cálculos de raízes, vértices e interseções são preservados quando a expressão corresponde a um polinômio de grau até 2. Para outras expressões, esta versão oferece o gráfico, mas ainda não calcula esses pontos automaticamente.

## Organização do código

- **`matematica.py`** — cálculo de raízes, discriminante, vértice e interseções.
- **`visualizacao.py`** — desenho simultâneo de até cinco funções, com cores distintas e pontos notáveis.
- **`interface.py`** — gerenciamento de 1 a 5 funções, entrada por coeficientes ou expressão e exportação PNG.
- **`expressoes.py`** — interpretação segura e avaliação das expressões digitadas.
- **`explorador.py`** — versão original no terminal.

## Limitações atuais

- O cálculo automático de interseções considera **f(x) e g(x)**, quando são polinômios de grau até 2; pares adicionais ainda não possuem interseção calculada.
- Expressões não polinomiais são desenhadas, mas ainda não possuem análise automática de raízes, vértices ou interseções.

## Próximos passos

- Permitir selecionar pares de funções para calcular interseções.
- Ampliar a análise numérica de funções não polinomiais.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.