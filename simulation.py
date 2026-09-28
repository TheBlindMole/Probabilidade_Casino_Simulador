import numpy as np


class SimuladorCassino:
    """Simula o saldo de vários jogadores ao longo de várias partidas."""

    def __init__(self, n_jogadores, saldo_inicial, aposta, house_edge_pct, n_partidas):
        self.n_jogadores = n_jogadores
        self.saldo_inicial = saldo_inicial
        self.aposta = aposta
        self.house_edge_pct = house_edge_pct
        self.n_partidas = n_partidas
        # com house edge 0% a moeda é justa (p = 0.5)
        # reduz essa probabilidade de vitória do jogador
        self.p_vitoria = 0.5 * (1 - house_edge_pct / 100)

    def simular(self, seed=None):
        """Devolve uma matriz (n_partidas + 1, n_jogadores) com o saldo de
        cada jogador ao longo do tempo (linha 0 = saldo inicial)."""
        rng = np.random.default_rng(seed)
        n, m = self.n_partidas, self.n_jogadores
        saldos = np.empty((n + 1, m), dtype=float)
        saldos[0, :] = self.saldo_inicial

        for t in range(1, n + 1):
            saldo_anterior = saldos[t - 1, :]
            pode_apostar = saldo_anterior >= self.aposta
            venceu = rng.random(m) < self.p_vitoria
            delta = np.where(venceu, self.aposta, -self.aposta)
            # sem saldo = incapacitado para apostar
            delta = np.where(pode_apostar, delta, 0.0)
            saldos[t, :] = saldo_anterior + delta

        return saldos
