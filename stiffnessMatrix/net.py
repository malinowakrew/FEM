def net(H, W, nH: int, nW: int):
    delta_h = (H / (nH - 1))
    delta_w = (W / (nW - 1))

    wezly = []
    for i in range(0, nH):
        for j in range(0, nW):
            wezly.append([(i * delta_h), j * delta_w])

    elementy = []
    for j in range(0, nW - 1):
        for c in range(0, nH - 1):
            i = c + j * nH
            elementy.append([i, i + nH, i + nH + 1, i + 1])

    krawedzie = [0 for i in wezly]
    for numberNode, node in enumerate(wezly):
        if node[1] == H or node[0] == W:
            krawedzie[numberNode] = 1.0


    return ({"wezly": wezly, "elementy": elementy, "krawedzie": krawedzie})

class globalNet():
    def __init__(self)->None:
        self.wezly = self.net()



