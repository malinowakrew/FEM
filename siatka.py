def siatka(H, W, nH:int, nW:int):
    delta_h = (H / (nH-1))
    delta_w = (W / (nW-1))

    wezly = []
    for i in range(0, nH):
        for j in range(0, nW):
            wezly.append([(i*delta_h), j*delta_w])


    elementy = []
    for j in range(0, nW-1):
        for c in range(0, nH-1):
            i = c + j*nH
            elementy.append([i, i+nH, i+nH+1, i+1])

    return({"wezly": wezly, "elementy": elementy})

def main():
    sciezka = r"dane.txt"
    with open(sciezka, "r") as plik:
        dane = plik.read()
        plik.close()

    tablica = dane.split("\n")

    tablica_danych = [float(element) for element in tablica[:4]]

    s = siatka(tablica_danych[0], tablica_danych[1], int(tablica_danych[2]), int(tablica_danych[3]))
    print("Węzły")
    print(s["wezly"])
    print("elementy")
    print(s["elementy"])
    print("-----------------")

    for i in s["elementy"][0]:
        print(s["wezly"][i])

    rownanie = tablica[4]

    #print(całka_2_punkty(tablica_danych[0], tablica_danych[1], rownanie, s["wezly"]))


if __name__ == "__main__":
    main()



