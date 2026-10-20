# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos matemáticos interativos.

## Sobre o projeto

O Explorador de Funções permite visualizar **uma a cinco funções simultâneas**, definidas por coeficientes ou expressões matemáticas digitadas diretamente. A versão **2.7** adicionou um **cursor de precisão** para identificar pontos das curvas com seis casas decimais. A versão **2.8** permite clicar em raízes, vértices e interseções para aproximar o gráfico do ponto selecionado, com a possibilidade de restaurar a visualização. A versão **2.9** substitui a barra cinza padrão do Matplotlib por controles de navegação discretos e integrados ao tema da interface. A versão **3.0** introduziu um painel de parâmetros recolhível para ampliar a área do gráfico sem perder as configurações. A versão **3.1** permite selecionar qualquer par de funções ativas, localizar interseções e investigá-las com o zoom inteligente, inclusive quando as funções são expressões não polinomiais.

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
- **Interseções entre quaisquer duas funções ativas**, escolhidas entre `f(x)`, `g(x)`, `h(x)`, `i(x)` e `j(x)`, com resultado destacado no gráfico.
- **Interseções numéricas de expressões**, incluindo casos como `sin(x)` e `cos(x)`, além dos cálculos analíticos entre polinômios de grau até 2.
- Raízes e vértices de funções polinomiais de grau até 2.
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

## Interseções avançadas — versão 3.1

1. Configure **duas ou mais funções** e o intervalo do eixo horizontal.
2. Na seção **INTERSEÇÕES ENTRE FUNÇÕES**, escolha a **Primeira** e a **Segunda** função. Por exemplo, `f` e `h`.
3. Clique em **GERAR GRÁFICO**, se tiver editado algum campo, ou altere os seletores para atualizar automaticamente o resultado.
4. As interseções calculadas aparecem como **pontos verdes** no gráfico e são listadas na análise matemática com **seis casas decimais**.
5. Clique em um desses pontos para usar o **zoom inteligente**. Use **RESTAURAR VISÃO** para retornar ao enquadramento original.

Exemplo com `f(x) = sin(x)` e `h(x) = cos(x)`, no intervalo `[-5, 5]`: o programa encontra aproximadamente três interseções, incluindo `(0.785398, 0.707107)`.

Para dois polinômios de grau até 2, as interseções são calculadas **algebricamente**, respeitando o intervalo selecionado. Para os demais casos, o módulo `intersecoes.py` utiliza amostragem, **bisseção** e busca de mínimos locais da diferença entre as funções, verificando o resultado antes de exibi-lo. Isso também permite encontrar algumas tangências e evitar falsos pontos causados por assíntotas.

O cálculo numérico é **aproximado e limitado ao intervalo configurado**; ele não garante detectar todas as interseções de funções muito oscilatórias ou em situações numericamente difíceis. São destacados até 60 pontos por análise, dos quais até 12 aparecem listados no painel. Resultados sem pontos encontrados não constituem prova matemática de inexistência de interseção.

Ao deixar apenas uma função ativa, os seletores ficam desabilitados. Quando funções são removidas, a seleção é ajustada para manter um par válido, quando possível.

## Como usar o cursor de precisão

1. Execute a interface e gere um gráfico.
2. Mova o mouse **perto de uma curva**, sem ativar o modo de zoom ou movimentação.
3. Um ponto colorido aparece na curva com as coordenadas de até **6 casas decimais**.
4. Ao afastar o cursor, a marcação desaparece. Fora das curvas, a barra inferior mostra a posição do mouse.

Os valores exibidos são calculados a partir da função na posição horizontal do cursor, e não apenas lidos dos pontos usados para desenhar a curva. Para funções com singularidades ou pontos fora do domínio real, não há indicação de ponto nessas posições.

## Como usar o zoom inteligente

1. Gere um gráfico com uma ou mais funções.
2. Clique diretamente em um ponto notável desenhado (raiz, vértice ou interseção do par selecionado).
3. O gráfico será centralizado e ampliado em torno do ponto, com `x` e `y` exibidos com seis casas decimais.
4. Clique novamente no ponto selecionado para ampliar mais, ou clique em **RESTAURAR VISÃO** para retornar aos limites originais.

O clique funciona apenas perto dos pontos matematicamente calculados e atualmente visíveis, enquanto os modos **MOVER** e **ZOOM** estão desativados. As interseções podem ser calculadas para qualquer par de funções ativas. Raízes e vértices continuam sendo destacados automaticamente apenas para polinômios de grau até 2. A ampliação não aumenta a precisão numérica dos cálculos, apenas melhora a inspeção visual do ponto.

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
    ├── intersecoes.py
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

Selecione de uma a cinco funções e escolha **Afim**, **Quadrática** ou **Expressão** para cada uma. Na seção **INTERSEÇÕES ENTRE FUNÇÕES**, escolha as funções que deseja comparar. Gere o gráfico e aproxime o mouse de uma curva para visualizar o cursor de precisão. A opção **SALVAR GRÁFICO** exporta apenas o gráfico para PNG.

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
- **`visualizacao.py`** — desenho simultâneo de até cinco curvas e dos pontos de interseção do par selecionado.
- **`intersecoes.py`** — cálculo analítico e busca numérica de interseções, com validação das soluções.
- **`interface.py`** — painel recolhível, navegação minimalista, cursor de precisão, zoom inteligente e exportação.
- **`expressoes.py`** — avaliação controlada das expressões matemáticas.
- **`cursor_precisao.py`** — módulo independente preservado no repositório; a interface utiliza seu próprio cursor integrado.
- **`explorador.py`** — versão de terminal.

## Limitações atuais

- As interseções numéricas podem deixar de encontrar raízes ou tangências em funções muito oscilatórias ou com comportamento difícil, mesmo dentro do intervalo.
- Somente o **par selecionado** tem suas interseções calculadas; cada análise mostra até 60 pontos.
- Expressões não polinomiais podem ser analisadas numericamente quanto às interseções, mas ainda não possuem análise algébrica geral de raízes ou vértices.
- Os valores apresentados possuem seis casas decimais de exibição, sujeitos à precisão numérica do Python.

## Próximos passos

- Ampliar a identificação de raízes de expressões não polinomiais e aprimorar o tratamento de descontinuidades.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.