def net(H, W, nH: int, nW: int, warming_gage=1.0, brick_gage=2.0, warming_conductivity_factor=0.038,
        air_conductivity_factor=0.025, brick_conductivity_factor=0.16):
    delta_h = (H / (nH - 1))
    delta_w = (W / (nW - 1))

    nodes = []
    for i in range(0, nH):
        for j in range(0, nW):
            nodes.append([(i * delta_h), j * delta_w])

    elements = []
    for j in range(0, nW - 1):
        for c in range(0, nH - 1):
            i = c + j * nH
            elements.append([i, i + nH, i + nH + 1, i + 1])

    edges = [0.0 for i in nodes]
    for numberNode, node in enumerate(nodes):
        if node[1] == H or node[0] == W:
            edges[numberNode] = 1.0
        if node[0] == 0.0 or node[1] == 0.0:
            edges[numberNode] = 1.0

    conductivity = []
    for numberNode, node in enumerate(nodes):
        if warming_gage < node[0] < W-warming_gage and warming_gage < node[1] < H-warming_gage:
            if brick_gage < node[0] < W-brick_gage and brick_gage < node[1] < H-brick_gage:
                conductivity.append(air_conductivity_factor)
                print("HALOHA")
            else:
                conductivity.append(warming_conductivity_factor)
                print("HALOHA")
        else:
            conductivity.append(brick_conductivity_factor)


    return ({"wezly": nodes, "elementy": elements, "krawedzie": edges, "wspolczynnik_przewodzenia": conductivity})

class globalNet():
    def __init__(self)->None:
        self.wezly = self.net()



