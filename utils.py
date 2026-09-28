#geração de cores e formatação de números

import matplotlib
import matplotlib.cm


def obter_cores(nome_colormap, n):
    try:
        cmap = matplotlib.colormaps[nome_colormap]
    except Exception:
        cmap = matplotlib.cm.get_cmap(nome_colormap)
    if n <= 1:
        return [cmap(0.0)]
    return [cmap(i / (n - 1)) for i in range(n)]


def formatar_reais(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return texto
