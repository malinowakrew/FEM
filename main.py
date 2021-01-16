# This is a sample Python script.

"""
Edyta Mróz https://github.com/malinowakrew/FEM/
"""
from SOE.SOE import *
from data.reader import Reader

def stiffnessmatrixcalculateH():

    np.set_printoptions(linewidth=np.inf)
    reader = Reader()
    dict_with_data = reader.read()

    net_data = list(dict_with_data.values())[:4]

    soe = SOE(dict_with_data["stop time"], dict_with_data["simulation step time"], dict_with_data["conductivity"],
              dict_with_data["initial temperature"],dict_with_data["density"], dict_with_data["specific heat"],
              dict_with_data["alfa"],
              dict_with_data["ambient temperature"], net_data, dict_with_data["number of points in local net"],
              dict_with_data["warming_gage"],
              dict_with_data["warming_specific_heat"],
              dict_with_data["warming_density"],

              dict_with_data["warming_conductivity_factor"],
              dict_with_data["air_specific_heat"],
              dict_with_data["air_density"],

              dict_with_data["air_conductivity_factor"],
              dict_with_data["brick_gage"],
              dict_with_data["brick_specific_heat"],
              dict_with_data["brick_density"],
              dict_with_data["brick_conductivity_factor"]
              )

    soe.calculateP()
    soe.calculate_hg()
    soe.calculateCg()
    #soe.drawStiffnessMatrix()


    time = dict_with_data["stop time"]
    data_package = []
    max = 0
    min = 0
    while time > 0:
        time -= dict_with_data["simulation step time"]
        data_package.append(soe.calculations((time-dict_with_data["stop time"])+dict_with_data["simulation step time"]))
        if max < data_package[-1]["t"].max():
            max = data_package[-1]["t"].max()

        if min > data_package[-1]["t"].min():
            min = data_package[-1]["t"].min()

    pd.Series(data_package).to_csv("data/data_temporary.csv")

    if dict_with_data["style of plot"] == 1:
        fig, axes = plt.subplots(
            nrows=math.ceil(dict_with_data["stop time"] / (3 * dict_with_data["simulation step time"])),
            ncols=3)
        for nr, ax in enumerate(axes.flat):
            temp = data_package[nr]
            im = ax.scatter(temp["x"], temp["y"], c=temp["t"], cmap='viridis', vmin=min, vmax=max)
            # a = dict_with_data["brick_gage"]
            # b = net_data[0] - dict_with_data["brick_gage"]
            # ax.plot([a, b], [a, a], 'k-', lw=2)
            # ax.plot([a, b], [b, b], 'k-', lw=2)
            # ax.plot([a, a], [a, b], 'k-', lw=2)
            # ax.plot([b, b], [a, b], 'k-', lw=2)
            #
            # a = dict_with_data["warming_gage"]
            # b = net_data[0] - dict_with_data["warming_gage"]
            # ax.plot([a, b], [a, a], 'k-', lw=2)
            # ax.plot([a, b], [b, b], 'k-', lw=2)
            # ax.plot([a, a], [a, b], 'k-', lw=2)
            # ax.plot([b, b], [a, b], 'k-', lw=2)
            title = "max:" + str(round(temp["t"].max(), 2)) + ", min:" + str(round(temp["t"].min(), 2))
            ax.set_title(label=title, fontsize=9)

        plt.show()

    if dict_with_data["style of plot"] == 2:
        temp = data_package[0]
        plt.scatter(temp["x"], temp["y"], c=temp["edges"], cmap='viridis', vmin=0, vmax=0.16)
        plt.title(label="", fontsize=9)
        plt.show()
        temp = data_package[0]
        plt.scatter(temp["x"], temp["y"], c=temp["con"], cmap='viridis', vmin=0, vmax=dict_with_data["brick_conductivity_factor"])
        a = dict_with_data["brick_gage"]
        b = net_data[0] - dict_with_data["brick_gage"]
        plt.plot([a, b], [a, a], 'k-', lw=2)
        plt.plot([a, b], [b, b], 'k-', lw=2)
        plt.plot([a, a], [a, b], 'k-', lw=2)
        plt.plot([b, b], [a, b], 'k-', lw=2)

        a = dict_with_data["warming_gage"]
        b = net_data[0] - dict_with_data["warming_gage"]
        plt.plot([a, b], [a, a], 'k-', lw=2)
        plt.plot([a, b], [b, b], 'k-', lw=2)
        plt.plot([a, a], [a, b], 'k-', lw=2)
        plt.plot([b, b], [a, b], 'k-', lw=2)
        plt.title(label="Materiały", fontsize=9)
        plt.show()
        for i in temp['con']:
            print(f"Conductivity {i}")
        for temp in data_package:
            plt.scatter(temp["x"], temp["y"], c=temp["t"], cmap='viridis', vmin=min, vmax=max)
            a = dict_with_data["brick_gage"]
            b = net_data[0] - dict_with_data["brick_gage"]
            plt.plot([a, b], [a, a], 'k-', lw=2)
            plt.plot([a, b], [b, b], 'k-', lw=2)
            plt.plot([a, a], [a, b], 'k-', lw=2)
            plt.plot([b, b], [a, b], 'k-', lw=2)

            a = dict_with_data["warming_gage"]
            b = net_data[0] - dict_with_data["warming_gage"]
            plt.plot([a, b], [a, a], 'k-', lw=2)
            plt.plot([a, b], [b, b], 'k-', lw=2)
            plt.plot([a, a], [a, b], 'k-', lw=2)
            plt.plot([b, b], [a, b], 'k-', lw=2)
            title = "max:" + str(round(temp["t"].max(), 2)) + ", min:" + str(round(temp["t"].min(), 2))
            plt.title(label=title, fontsize=9)
            plt.show()



if __name__ == '__main__':
    k=0.032
    c=1500.0
    ro=900.0
    w=0.0001
    asr=k/(c*ro)
    dtime=(w*w)/(0.5*asr)
    print("Dtime {}".format(dtime))
    stiffnessmatrixcalculateH()

