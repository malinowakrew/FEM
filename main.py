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
              dict_with_data["ambient temperature"], net_data, dict_with_data["number of points in local net"])

    soe.calculateP()
    soe.calculate_hg()
    soe.calculateCg()

    time = dict_with_data["stop time"]
    data_package = []
    max = 0
    while time:
        time -= dict_with_data["simulation step time"]
        data_package.append(soe.calculations((time-dict_with_data["stop time"])+dict_with_data["simulation step time"]))
        if max < data_package[-1]["t"].max():
            max = data_package[-1]["t"].max()

    pd.Series(data_package).to_csv("data/data_temporary.csv")

    if dict_with_data["style of plot"] == 1:
        fig, axes = plt.subplots(
            nrows=math.ceil(dict_with_data["stop time"] / (3 * dict_with_data["simulation step time"])),
            ncols=3)
        for nr, ax in enumerate(axes.flat):
            temp = data_package[nr]
            im = ax.scatter(temp["x"], temp["y"], c=temp["t"], cmap='viridis', vmin=0, vmax=max)
            ax.plot([0.02, 0.08], [0.02, 0.02], 'k-', lw=2)
            ax.plot([0.02, 0.08], [0.08, 0.08], 'k-', lw=2)
            ax.plot([0.02, 0.02], [0.02, 0.08], 'k-', lw=2)
            ax.plot([0.08, 0.08], [0.02, 0.08], 'k-', lw=2)
            title = "max:" + str(round(temp["t"].max(), 2)) + ", min:" + str(round(temp["t"].min(), 2))
            ax.set_title(label=title, fontsize=9)

        plt.show()

    if dict_with_data["style of plot"] == 2:
        temp = data_package[0]
        plt.scatter(temp["x"], temp["y"], c=temp["con"], cmap='viridis', vmin=0, vmax=max)
        plt.title(label="Krawędzie", fontsize=9)
        plt.show()
        for temp in data_package:
            plt.scatter(temp["x"], temp["y"], c=temp["t"], cmap='viridis', vmin=0, vmax=max)
            plt.plot([0.02, 0.08], [0.02, 0.02], 'k-', lw=2)
            plt.plot([0.02, 0.08], [0.08, 0.08], 'k-', lw=2)
            plt.plot([0.02, 0.02], [0.02, 0.08], 'k-', lw=2)
            plt.plot([0.08, 0.08], [0.02, 0.08], 'k-', lw=2)
            title = "max:" + str(round(temp["t"].max(), 2)) + ", min:" + str(round(temp["t"].min(), 2))
            plt.title(label=title, fontsize=9)
            plt.show()



if __name__ == '__main__':
    stiffnessmatrixcalculateH()

