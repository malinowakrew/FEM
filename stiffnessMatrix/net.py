def net(H, W, nH: int, nW: int,
        warming_gage, brick_gage,
        warming_conductivity_factor, air_conductivity_factor, brick_conductivity_factor,
        warming_specific_heat,
        warming_density,
        air_specific_heat,
        air_density,
        brick_specific_heat,
        brick_density
        ):
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
        if node[1] == W or node[0] == H:
            edges[numberNode] = 1.0
        if node[0] == 0.0 or node[1] == 0.0:
            edges[numberNode] = 1.0

    conductivity = []
    specific_heat = []
    density = []
    for numberNode, node in enumerate(nodes):
        if warming_gage < node[1] < W-warming_gage and warming_gage < node[0] < H-warming_gage:
            if brick_gage < node[1] < W-brick_gage and brick_gage < node[0] < H-brick_gage:
                conductivity.append(air_conductivity_factor)
                specific_heat.append(air_specific_heat)
                density.append(air_density)
                print("#")
            else:
                conductivity.append(warming_conductivity_factor)
                specific_heat.append(warming_specific_heat)
                density.append(warming_density)
                print("/")
        else:
            conductivity.append(brick_conductivity_factor)
            specific_heat.append(brick_specific_heat)
            density.append(brick_density)
            print("*")


    return ({"wezly": nodes,
             "elementy": elements,
             "krawedzie": edges,
             "wspolczynnik_przewodzenia": conductivity,
             "specific heat": specific_heat,
             "density": density})

class globalNet():
    def __init__(self)->None:
        self.wezly = self.net()



