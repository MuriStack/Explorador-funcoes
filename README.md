# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos matemáticos interativos.

## Sobre o projeto

O Explorador de Funções permite analisar **uma função isoladamente** ou **comparar duas funções**, inserindo coeficientes ou expressões matemáticas diretamente.

A versão **2.5** acrescenta a opção **Expressão**, que permite escrever funções como `x^2 - 4*x + 3`, `sin(x)`, `log(x)` e `1/x`. Os modos anteriores, a exportação de PNG e o tema escuro com bordas arredondadas permanecem disponíveis.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Alternância entre os modos **1 função** e **2 funções**.
- Seleção independente de **Afim**, **Quadrática** ou **Expressão** para `f(x)` e `g(x)`, com a opção de expressão em uma linha própria para facilitar o uso.
- Campos adaptados para digitar coeficientes ou escrever a expressão diretamente.
- Gráficos interativos com zoom e movimentação.
- Destaque de raízes, vértices e interseções visíveis no intervalo.
- Cálculo do discriminante **Δ** e do vértice para funções quadráticas, inclusive expressões polinomiais reconhecidas.
- Classificação de funções afins e indicação da concavidade de parábolas.
- Identificação de até duas interseções reais ou de curvas coincidentes quando ambas são polinômios de grau até 2.
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

Selecione **1 função** ou **2 funções**. Em cada função, escolha **Afim**, **Quadrática** ou **Expressão**. Na opção Expressão, digite uma fórmula usando `x` e clique em **GERAR GRÁFICO**.

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
- **`visualizacao.py`** — desenho de retas, parábolas e pontos notáveis.
- **`interface.py`** — interface, entrada por coeficientes ou expressão e exportação de PNG.
- **`expressoes.py`** — interpretação segura e avaliação das expressões digitadas.
- **`explorador.py`** — versão original no terminal.

## Próximos passos

- Ampliar a análise numérica de funções não polinomiais.
- Melhorar os recursos de navegação e personalização do gráfico.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.