#Interface gráfica (Tkinter + matplotlib)

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

from constants import CORES_UNICAS, LIMITES, VALORES_PADRAO
from simulation import SimuladorCassino
from utils import obter_cores, formatar_reais


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Cassino — Lei dos Grandes Números & House Edge")
        self.root.geometry("1250x820")
        self.root.minsize(880, 560)

        self.anim = None
        self.saldos = None
        self.linhas = []
        self.saldo_inicial = 1000.0
        self.n_partidas = 0
        self.x_dados = None

        self._construir_interface()

    # Interface
    def _construir_interface(self):
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        painel = ttk.Frame(self.root, padding=14)
        painel.grid(row=0, column=0, sticky="ns")

        ttk.Label(
            painel, text="Parâmetros da Simulação", font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 12))

        self.var_jogadores = self._campo(painel, "Número de jogadores:", VALORES_PADRAO["n_jogadores"])
        self.var_saldo = self._campo(painel, "Saldo inicial (R$):", VALORES_PADRAO["saldo_inicial"])
        self.var_aposta = self._campo(painel, "Valor da aposta (R$):", VALORES_PADRAO["aposta"])
        self.var_edge = self._campo(painel, "Margem da casa / house edge (%):", VALORES_PADRAO["house_edge"])
        self.var_partidas = self._campo(painel, "Número de partidas:", VALORES_PADRAO["n_partidas"])
        self.var_velocidade = self._campo(painel, "Velocidade da animação (ms/frame):", VALORES_PADRAO["velocidade"])

        ttk.Separator(painel, orient="horizontal").pack(fill="x", pady=12)

        self.var_multicolor = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            painel,
            text="Cada jogador com uma cor diferente",
            variable=self.var_multicolor,
            command=self._alternar_cor_unica,
        ).pack(anchor="w", pady=(0, 6))

        ttk.Label(painel, text="Cor única (se desmarcares acima):").pack(anchor="w")
        self.var_cor_unica = tk.StringVar(value="Vermelho")
        self.combo_cor = ttk.Combobox(
            painel,
            textvariable=self.var_cor_unica,
            values=list(CORES_UNICAS.keys()),
            state="disabled",
            width=16,
        )
        self.combo_cor.pack(anchor="w", pady=(2, 12))

        ttk.Separator(painel, orient="horizontal").pack(fill="x", pady=12)

        self.btn_iniciar = ttk.Button(
            painel, text="▶  Iniciar Simulação", command=self.iniciar_simulacao
        )
        self.btn_iniciar.pack(fill="x", pady=(0, 8))

        self.btn_parar = ttk.Button(
            painel, text="⏹  Parar Animação", command=self.parar_animacao, state="disabled"
        )
        self.btn_parar.pack(fill="x")

        #janela responsiva
        direita = ttk.Frame(self.root, padding=(0, 14, 14, 14))
        direita.grid(row=0, column=1, sticky="nsew")
        direita.columnconfigure(0, weight=1)
        direita.rowconfigure(0, weight=1)
        direita.rowconfigure(1, weight=0)

        self.fig = Figure(figsize=(8, 5.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=direita)
        self._preparar_eixo_vazio()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        stats = ttk.Frame(direita, padding=(6, 14, 6, 0))
        stats.grid(row=1, column=0, sticky="ew")
        stats.columnconfigure(0, weight=1)
        stats.columnconfigure(1, weight=1)

        self.lbl_lucro_pessoas = ttk.Label(
            stats, text="Quantidade de pessoas no lucro: —", font=("Segoe UI", 11)
        )
        self.lbl_lucro_pessoas.grid(row=0, column=0, sticky="w")

        self.lbl_partidas = ttk.Label(
            stats, text="Quantidade de partidas: —", font=("Segoe UI", 11)
        )
        self.lbl_partidas.grid(row=0, column=1, sticky="w")

        self.lbl_prejuizo_pessoas = ttk.Label(
            stats, text="Quantidade de pessoas no prejuízo: —", font=("Segoe UI", 11)
        )
        self.lbl_prejuizo_pessoas.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.lbl_lucro_cassino = ttk.Label(
            stats, text="Lucro do Cassino: —", font=("Segoe UI", 11, "bold"), foreground="#1a7a1a"
        )
        self.lbl_lucro_cassino.grid(row=1, column=1, sticky="w", pady=(6, 0))

    def _campo(self, parent, rotulo, valor_padrao):
        ttk.Label(parent, text=rotulo).pack(anchor="w")
        var = tk.StringVar(value=valor_padrao)
        ttk.Entry(parent, textvariable=var, width=20).pack(anchor="w", pady=(2, 8))
        return var

    def _alternar_cor_unica(self):
        self.combo_cor.configure(state="disabled" if self.var_multicolor.get() else "readonly")

    def _preparar_eixo_vazio(self):
        self.ax.clear()
        self.ax.set_title("Saldo por Partida", fontsize=14)
        self.ax.set_xlabel("Partidas")
        self.ax.set_ylabel("Saldo (R$)")
        self.ax.grid(True, alpha=0.3)
        if hasattr(self, "canvas"):
            self.canvas.draw_idle()

    # validação de parâmetros
    def _ler_parametros(self):
        try:
            n_jogadores = int(self.var_jogadores.get())
            saldo_inicial = float(self.var_saldo.get().replace(",", "."))
            aposta = float(self.var_aposta.get().replace(",", "."))
            house_edge = float(self.var_edge.get().replace(",", "."))
            n_partidas = int(self.var_partidas.get())
            velocidade = int(self.var_velocidade.get())
        except ValueError:
            messagebox.showerror("Entrada inválida", "Verifica se todos os campos contêm números válidos.")
            return None

        erros = []
        lo, hi = LIMITES["n_jogadores"]
        if not (lo <= n_jogadores <= hi):
            erros.append(f"Número de jogadores deve estar entre {lo} e {hi}.")
        if saldo_inicial <= 0:
            erros.append("Saldo inicial deve ser maior que 0.")
        if aposta <= 0:
            erros.append("Valor da aposta deve ser maior que 0.")
        lo, hi = LIMITES["house_edge"]
        if not (lo <= house_edge < hi):
            erros.append(f"Margem da casa deve estar entre {lo} e {hi} (%).")
        lo, hi = LIMITES["n_partidas"]
        if not (lo <= n_partidas <= hi):
            erros.append(f"Número de partidas deve estar entre {lo} e {hi}.")
        if velocidade < 1:
            erros.append("Velocidade deve ser um número positivo de milissegundos.")

        if erros:
            messagebox.showerror("Entrada inválida", "\n".join(erros))
            return None

        return dict(
            n_jogadores=n_jogadores, saldo_inicial=saldo_inicial, aposta=aposta,
            house_edge=house_edge, n_partidas=n_partidas, velocidade=velocidade,
        )

    # simulação e animação
    def iniciar_simulacao(self):
        params = self._ler_parametros()
        if params is None:
            return

        self.parar_animacao()

        sim = SimuladorCassino(
            params["n_jogadores"], params["saldo_inicial"], params["aposta"],
            params["house_edge"], params["n_partidas"],
        )
        self.saldos = sim.simular()
        self.saldo_inicial = params["saldo_inicial"]
        self.n_partidas = params["n_partidas"]
        self.x_dados = np.arange(self.n_partidas + 1)

        self._preparar_eixo_vazio()

        n_jogadores = params["n_jogadores"]
        if self.var_multicolor.get():
            cores = obter_cores("hsv", n_jogadores)
        else:
            cores = [CORES_UNICAS[self.var_cor_unica.get()]] * n_jogadores

        self.linhas = [
            self.ax.plot([], [], lw=0.9, color=cores[i], alpha=0.85)[0]
            for i in range(n_jogadores)
        ]
        self.ax.axhline(self.saldo_inicial, color="gray", ls="--", lw=1, alpha=0.6)

        margem = max(self.saldos.std() * 0.15, self.saldos.max() * 0.02, 1.0)
        ymin = max(0, self.saldos.min() - margem)
        ymax = self.saldos.max() + margem
        self.ax.set_xlim(0, max(self.n_partidas, 1))
        self.ax.set_ylim(ymin, ymax if ymax > ymin else ymin + 1)

        # agrupa as partidas em blocos para manter a animação fluida
        max_frames = 250
        passo = max(1, self.n_partidas // max_frames)
        frames = list(range(passo, self.n_partidas + 1, passo))
        if not frames or frames[-1] != self.n_partidas:
            frames.append(self.n_partidas)

        self.btn_iniciar.configure(state="disabled")
        self.btn_parar.configure(state="normal")
        self._atualizar_estatisticas(0)

        self.anim = FuncAnimation(
            self.fig,
            self._atualizar_frame,
            frames=frames,
            interval=params["velocidade"],
            blit=False,
            repeat=False,
        )
        self.canvas.draw_idle()

    def _atualizar_frame(self, frame):
        for i, linha in enumerate(self.linhas):
            linha.set_data(self.x_dados[: frame + 1], self.saldos[: frame + 1, i])
        self._atualizar_estatisticas(frame)
        if frame >= self.n_partidas:
            self._finalizar_animacao()
        return self.linhas

    def _atualizar_estatisticas(self, frame):
        saldos_atuais = self.saldos[frame, :]
        lucro = int(np.sum(saldos_atuais > self.saldo_inicial))
        prejuizo = int(np.sum(saldos_atuais < self.saldo_inicial))
        lucro_cassino = float(np.sum(self.saldo_inicial - saldos_atuais))

        self.lbl_lucro_pessoas.configure(text=f"Quantidade de pessoas no lucro: {lucro}")
        self.lbl_prejuizo_pessoas.configure(text=f"Quantidade de pessoas no prejuízo: {prejuizo}")
        self.lbl_partidas.configure(text=f"Quantidade de partidas: {frame}")

        cor = "#1a7a1a" if lucro_cassino >= 0 else "#a11111"
        self.lbl_lucro_cassino.configure(
            text=f"Lucro do Cassino: {formatar_reais(lucro_cassino)} reais", foreground=cor
        )

    def _finalizar_animacao(self):
        self.btn_iniciar.configure(state="normal")
        self.btn_parar.configure(state="disabled")

    def parar_animacao(self):
        if self.anim is not None:
            try:
                self.anim.event_source.stop()
            except Exception:
                pass
            self.anim = None
        self.btn_iniciar.configure(state="normal")
        self.btn_parar.configure(state="disabled")
