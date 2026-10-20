# 📈 Explorador de Funções

Aplicação em **Python** para explorar e comparar funções afins em uma interface gráfica interativa.

## Sobre o projeto

O Explorador de Funções permite definir duas funções afins, identificar raízes, classificações e interseções e visualizar os resultados no plano cartesiano. A versão **2.1 — Dark Edition** apresenta uma interface escura com **painéis, campos e botão de cantos arredondados**, gráficos personalizados e um painel integrado de análise matemática.

## Demonstração

![Interface do Explorador de Funções](images/interface.png)

## Funcionalidades

- Interface gráfica escura, com painéis e campos arredondados e coeficientes de `f(x)` e `g(x)` organizados em pares.
- Gráfico interativo com zoom e movimentação.
- Classificação de funções crescentes, decrescentes ou constantes.
- Cálculo e identificação de raízes e interseção.
- Identificação de funções paralelas e coincidentes.
- Configuração do intervalo e atualização do gráfico sem reiniciar.
- Validação de valores informados.
- Versão alternativa executada pelo terminal.

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

Para usar a versão de terminal:

```bash
python explorador.py
```

## Organização do código

- **`matematica.py`** — cálculos e classificações.
- **`visualizacao.py`** — montagem dos gráficos e estilos.
- **`interface.py`** — janela, controles e interação com o usuário.
- **`explorador.py`** — aplicação no terminal.

## Próximos passos

- Permitir salvar gráficos como imagens.
- Melhorar a edição e o gerenciamento de funções.
- Expandir o suporte para outros tipos de funções.

## Autor

Desenvolvido por [MuriStack](https://github.com/MuriStack).

---

Projeto educacional que integra programação, matemática e visualização gráfica.