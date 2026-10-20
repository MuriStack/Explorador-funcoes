# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos matemáticos interativos.

## Sobre o projeto

O Explorador de Funções permite visualizar **uma a cinco funções simultâneas**, definidas por coeficientes ou expressões matemáticas digitadas diretamente. A versão **2.7** adicionou um **cursor de precisão** para identificar pontos das curvas com seis casas decimais. A versão **2.8** permite clicar em raízes, vértices e interseções para aproximar o gráfico do ponto selecionado, com a possibilidade de restaurar a visualização. A versão **2.9** substitui a barra cinza padrão do Matplotlib por controles de navegação discretos e integrados ao tema da interface. A versão **3.0** introduz um painel de parâmetros recolhível para ampliar a área destinada ao gráfico sem perder as configurações.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Visualização de **1 a 5 funções** no mesmo plano cartesiano, usando **+ ADICIONAR** e **− REMOVER**.
- **Painel de parâmetros recolhível:** pequeno botão com setas entre o painel e o gráfico permite ocultar e reexibir a lateral, liberando mais espaço para a visualização.
- Modos **Afim**, **Quadrática** e **Expressão** para cada função, independentemente.
- **Zoom inteligente:** clique diretamente em uma raiz, vértice ou interseção visível para centralizar e ampliar a visualização, mostrando suas coordenadas com seis casas decimais.
- **Navegação minimalista:** a barra cinza do Matplotlib não aparece mais. Os botões **MOVER** e **ZOOM**, no cabeçalho do gráfico, permitem navegar manualmente sem quebrar a identidade visual.
- **Restaurar visão:** botão com bordas arredondadas e contorno discreto, que retorna aos limites originais do gráfico após usar o zoom inteligente ou a navegação manual e desativa o modo de navegação.
- **Cursor de precisão:** ao aproximar o mouse de uma curva, o programa destaca o ponto e mostra as coordenadas `x` e `y` com seis casas decimais.
- Exibição das coordenadas livres do mouse na barra inferior quando ele está no gráfico, mas longe das curvas.
- O cursor ignora resultados indefinidos e não interfere nas ferramentas de zoom e movimentação.
- Barra de rolagem lateral minimalista, utilizável com a roda do mouse e por arraste.
- Raízes, vértices e interseções de **f(x) e g(x)** para polinômios de grau até 2.
- Cálculo de discriminante e indicação do comportamento das funções aplicáveis.
- Intervalo configurável, gráficos interativos e exportação em PNG.
- Tratamento de entradas inválidas e preservação da versão de terminal.

## Painel recolhível — versão 3.0

O pequeno botão com seta fica na divisória entre os parâmetros e o gráfico:

1. Clique na seta apontada para a esquerda para ocultar o painel lateral e ampliar a área do gráfico.
2. Com o painel oculto, clique na seta apontada para a direita para reabrir os parâmetros.
3. Os valores digitados, os tipos de função escolhidos e a quantidade de curvas continuam preservados. A posição de rolagem lateral também é mantida.
4. A ação não gera um novo gráfico: os limites dos eixos permanecem os mesmos, inclusive após zoom manual ou foco em pontos notáveis.

O botão também pode ser acionado com **Enter** ou **Espaço** quando recebe foco pelo teclado. A barra de rolagem do painel e os recursos matemáticos existentes continuam disponíveis normalmente.

## Como usar o cursor de precisão

1. Execute a interface e gere um gráfico.
2. Mova o mouse **perto de uma curva**, sem ativar o modo de zoom ou movimentação.
3. Um ponto colorido aparece na curva com as coordenadas de até **6 casas decimais**.
4. Ao afastar o cursor, a marcação desaparece. Fora das curvas, a barra inferior mostra a posição do mouse.

Os valores exibidos são calculados a partir da função na posição horizontal do cursor, e não apenas lidos dos pontos usados para desenhar a curva. Para funções com singularidades ou pontos fora do domínio real, não há indicação de ponto nessas posições.

## Como usar o zoom inteligente

1. Gere um gráfico com uma ou mais funções.
2. Clique diretamente em um ponto notável desenhado (raiz, vértice ou interseção entre `f(x)` e `g(x)`).
3. O gráfico será centralizado e ampliado em torno do ponto, com `x` e `y` exibidos com seis casas decimais.
4. Clique novamente no ponto selecionado para ampliar mais, ou clique em **RESTAURAR VISÃO** para retornar aos limites originais.

O clique funciona apenas perto dos pontos matematicamente calculados e atualmente visíveis, enquanto os modos **MOVER** e **ZOOM** estão desativados. As interseções automáticas continuam limitadas a `f(x)` e `g(x)` polinomiais de grau até 2, e as raízes e os vértices continuam sendo destacados apenas nos polinômios de grau até 2. A ampliação não aumenta a precisão numérica dos cálculos, apenas melhora a inspeção visual do ponto.

## Controles de navegação da versão 2.9

A antiga faixa cinza de ferramentas do Matplotlib foi removida da área visível do gráfico. Os controles estão integrados ao cabeçalho escuro da aplicação:

- **MOVER:** clique para ativar e arraste o gráfico com o mouse. Clique novamente para desativar.
- **ZOOM:** clique para ativar e arraste um retângulo sobre o gráfico para ampliar a região. Clique novamente para desativar.
- **RESTAURAR VISÃO:** recupera o enquadramento original, desativa a ferramenta ativa e remove a seleção de um ponto notável.

Os botões **MOVER** e **ZOOM** são mutuamente exclusivos. Com ambos desativados, o cursor de precisão e o clique para zoom inteligente continuam funcionando. O botão **SALVAR GRÁFICO**, no painel lateral, mantém a exportação em PNG. Os controles da interface não aparecem nas imagens exportadas.

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
- **`interface.py`** — painel recolhível, navegação minimalista, cursor de precisão, zoom inteligente e exportação.
- **`expressoes.py`** — avaliação controlada das expressões matemáticas.
- **`cursor_precisao.py`** — cálculo e apresentação das coordenadas durante o movimento do mouse.
- **`explorador.py`** — versão de terminal.

## Limitações atuais

- As interseções automáticas consideram apenas **f(x)** e **g(x)** quando são polinômios de grau até 2.
- Expressões não polinomiais são desenhadas e podem ser exploradas pelo cursor, mas ainda não contam com análise algébrica automática.
- Os valores apresentados possuem seis casas decimais de exibição, sujeitos à precisão numérica do Python.

## Próximos passos

- Ampliar o cálculo de interseções para diferentes pares de funções, incluindo expressões não polinomiais, em uma atualização futura.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.