# Simulador de Cassino — Lei dos Grandes Números & House Edge

![Preview do projeto](https://media.tenor.com/OOz18OcUlxYAAAAM/pluto-anime.gif)

Simula o saldo de vários jogadores ao longo de várias partidas de um jogo
tipo vermelho/preto, onde a probabilidade de vitória é sempre um pouco
menor que 50% (a margem da casa / house edge). Individualmente cada
jogador segue um passeio aleatório imprevisível, mas ao juntar muitos
jogadores e muitas partidas, a Lei dos Grandes Números garante lucro ao
cassino a longo prazo.

## Como correr

Requer Python 3.9+ com `tkinter` (normalmente já incluído), `numpy` e
`matplotlib`:

```bash
pip install -r requirements.txt
python3 main.py
```

## Estrutura do projeto

```
casino_simulator/
├── main.py         # ponto de entrada — arranca a aplicação
├── gui.py          # interface gráfica (Tkinter + matplotlib)
├── simulation.py   # lógica pura da simulação (random walk, house edge)
├── utils.py        # funções auxiliares (cores, formatação de números)
├── constants.py    # constantes e valores por omissão
└── requirements.txt
```

## Uso

No painel esquerdo, ajusta:

- **Número de jogadores**
- **Saldo inicial (R$)**
- **Valor da aposta (R$)**
- **Margem da casa / house edge (%)**
- **Número de partidas**
- **Velocidade da animação (ms/frame)**
- Se cada jogador tem uma cor diferente, ou uma cor única para todos

Clica em **"Iniciar Simulação"** para ver a animação e as estatísticas
(pessoas no lucro/prejuízo, número de partidas, lucro do cassino) a
atualizar em tempo real. A janela é redimensionável — o gráfico e o
layout ajustam-se automaticamente ao tamanho escolhido.
