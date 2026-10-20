# 📈 Explorador de Funções

Aplicação em **Python** para analisar, comparar e exportar gráficos de funções afins e quadráticas.

## Sobre o projeto

O Explorador de Funções permite analisar **uma função isoladamente** ou **comparar duas funções**, escolhendo independentemente funções afins (`ax + b`) ou quadráticas (`ax² + bx + c`).

Na versão **2.4**, a interface ganhou o botão **Salvar gráfico**, que permite exportar o gráfico atual em **PNG**, escolhendo o nome e a pasta de destino. O aplicativo mantém o tema escuro e os componentes arredondados.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Alternância entre os modos **1 função** e **2 funções**.
- Seleção independente de função **afim** ou **quadrática** para `f(x)` e `g(x)`.
- Campos de coeficientes adaptados ao tipo de função.
- Gráficos interativos com zoom e movimentação.
- Destaque de raízes, vértices e interseções visíveis no intervalo.
- Cálculo do discriminante **Δ** e do vértice para funções quadráticas.
- Classificação de funções afins e indicação da concavidade de parábolas.
- Identificação de até duas interseções reais ou de curvas coincidentes.
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

Selecione **1 função** ou **2 funções**, escolha o tipo de cada uma e configure os coeficientes.

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

## Organização do código

- **`matematica.py`** — cálculo de raízes, discriminante, vértice e interseções.
- **`visualizacao.py`** — desenho de retas, parábolas e pontos notáveis.
- **`interface.py`** — interface, análise matemática e exportação de PNG.
- **`explorador.py`** — versão original no terminal.

## Próximos passos

- Melhorar a edição e o gerenciamento de funções.
- Permitir personalizar mais opções dos gráficos.
- Expandir o suporte para outros tipos de funções.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional para integrar programação, matemática e visualização gráfica.