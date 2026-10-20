# 📈 Explorador de Funções

Aplicação em **Python** para explorar e comparar funções afins em uma interface gráfica interativa.

## Sobre o projeto

O Explorador de Funções permite analisar **uma função afim isoladamente** ou **comparar duas funções**, identificando raízes, classificações e, no modo de comparação, pontos de interseção. A versão **2.2** acrescenta a seleção de quantidade de funções e mantém a interface escura com cantos arredondados.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Seleção entre os modos **1 função** e **2 funções**.
- Exibição apenas dos campos necessários ao modo selecionado.
- Interface escura com painéis, botões e campos arredondados.
- Gráfico interativo com zoom e movimentação.
- Classificação de funções crescentes, decrescentes ou constantes.
- Identificação das raízes das funções.
- Cálculo de interseção e identificação de retas paralelas ou coincidentes no modo de duas funções.
- Configuração do intervalo e atualização do gráfico sem reiniciar a aplicação.
- Validação dos valores informados.
- Versão alternativa executada pelo terminal para comparação entre duas funções.

## Tecnologias utilizadas

- **Python** — lógica e organização do programa.
- **Tkinter** — interface gráfica.
- **Matplotlib** — gráficos e ferramentas interativas.
- **Git e GitHub** — controle de versões.

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

### 2. Prepare o ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib
```

No Ubuntu e derivados, se o Tkinter não estiver instalado:

```bash
sudo apt install python3-tk
```

### 3. Abra a interface

```bash
cd explorador-funcoes
python interface.py
```

Selecione **1 função** para analisar somente `f(x)`, ou **2 funções** para comparar `f(x)` e `g(x)`.

Para usar a versão de terminal, que mantém a comparação entre duas funções:

```bash
python explorador.py
```

## Organização do código

- **`matematica.py`** — cálculos e classificações.
- **`visualizacao.py`** — montagem dos gráficos e estilos, com suporte a uma ou duas funções.
- **`interface.py`** — janela, seleção do modo, controles e interação com o usuário.
- **`explorador.py`** — aplicação original no terminal.

## Próximos passos

- Expandir o suporte para funções quadráticas.
- Permitir salvar gráficos como imagens.
- Melhorar a edição e o gerenciamento de funções.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional que integra programação, matemática e visualização gráfica.