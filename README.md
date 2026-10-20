# 📈 Explorador de Funções

Aplicação desenvolvida em **Python** para explorar, comparar e visualizar funções afins por meio de gráficos interativos.

## Sobre o projeto

O Explorador de Funções é uma aplicação que permite analisar duas funções afins simultaneamente, identificando suas características matemáticas e representando seus gráficos no plano cartesiano.

A versão 2.0 introduz uma **interface gráfica desenvolvida com Tkinter**, permitindo que o usuário configure funções e visualize os resultados sem depender da entrada de dados pelo terminal.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Interface gráfica para inserir os coeficientes das funções.
- Visualização simultânea de duas funções afins.
- Identificação de funções crescentes, decrescentes e constantes.
- Cálculo e identificação das raízes.
- Identificação de pontos de interseção.
- Verificação de funções paralelas e coincidentes.
- Configuração do intervalo de visualização.
- Zoom e movimentação pelo gráfico.
- Atualização do gráfico sem reiniciar o programa.
- Tratamento de entradas inválidas.

## Tecnologias utilizadas

- **Python** — linguagem principal do projeto.
- **Tkinter** — construção da interface gráfica.
- **Matplotlib** — geração e interação com os gráficos.
- **Git e GitHub** — versionamento do código.

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

### 2. Crie um ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install matplotlib
```

O Tkinter também deve estar disponível no sistema. No Ubuntu e derivados:

```bash
sudo apt install python3-tk
```

### 4. Execute a aplicação

```bash
cd explorador-funcoes
python interface.py
```

A versão tradicional, baseada no terminal, também continua disponível:

```bash
python explorador.py
```

## Organização do código

O projeto possui uma estrutura modular:

- **`matematica.py`** — funções responsáveis pelos cálculos matemáticos.
- **`visualizacao.py`** — construção e personalização dos gráficos.
- **`interface.py`** — interface gráfica e interação com o usuário.
- **`explorador.py`** — versão original executada pelo terminal.

## Conceitos aplicados

- Funções afins e suas propriedades.
- Coeficientes angular e linear.
- Raízes e pontos de interseção.
- Modularização em Python.
- Programação orientada a objetos.
- Interfaces gráficas.
- Visualização interativa de dados.

## Próximos passos

- Modernizar a aparência da interface.
- Melhorar a personalização dos gráficos.
- Expandir o suporte para outros tipos de funções.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional que integra programação, matemática e visualização gráfica.