import os
from modules.Plotter import Plotter


def correct_csv(dir:str, file: str):
    if "CORR" not in  file:
        with open(os.path.join(dir, file), "r") as data_file:
            tmp_file = data_file.readlines()
            if "#" in tmp_file[0]:
                tmp_line = tmp_file[0][1:]
                tmp_file[0] = tmp_line
            with open(os.path.join(dir, "CORR-" + file), "w") as corr_file:
                corr_file.writelines(tmp_file)

work_dir = "assets"
file_list = os.listdir(work_dir)

for file in file_list:
    correct_csv(work_dir, file)

file_list = os.listdir(work_dir)

for file in file_list:

    if "CORR" in file:
        plotter = Plotter(os.path.join(work_dir, file))
        plotter.plot_case1(file_name=str(file.strip(".csv")))
