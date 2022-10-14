from modules.Plotter import Plotter

file = "assets/AIRBOSS-CVN-75_Trapsheet-237 _ Nygus_FA-18C_hornet-0001.csv"
plotter = Plotter(file)
plotter.plot_aoa_graph(save=True)

