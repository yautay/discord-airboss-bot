import math

import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from scipy.interpolate import interp1d
from modules.Keys import KeysCSV as K, KeysGRV as GRV
from modules.Utils import Utils
from modules.Base_Plotter import BasePlotter


class PlotterGRV(BasePlotter):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.__airframe = self.airframe
        self.__data = self.data[[K.x(), K.z()]]
        self.__grv_limits = self.__grv_limits_data()
        print("GRV data:\n", self.__data)
        print("GRV limits:\n", self.__grv_limits)

    @staticmethod
    def __grv_limits_data():
        return {
            GRV.limits(): {
                GRV.___lul___(): -3,
                GRV.__lul__(): -1,
                GRV.lul(): -.5,
                GRV.ok(): 0,
                GRV.lur(): .5,
                GRV.__lur__(): 1,
                GRV.___lur___(): 3,
            }
        }

    def plot_grv_graph(self, save: bool = False):
        with plt.style.context('Solarize_Light2'):
            df = self.__data
            fig, ax = plt.subplots()

            # X-axis setup
            x_axis_limit_left = 11
            x_axis_limit_right = 0
            ax.set_xlim(x_axis_limit_left, x_axis_limit_right)
            ax.set_xlabel('distance [Cbls]')

            # Y-axis setup
            y_axis_limit_low = 1.5
            y_axis_limit_hi = -.1
            ax.set_ylim(y_axis_limit_low, y_axis_limit_hi)
            ax.set_ylabel('lateral offset [Cbls]')

            longitudinal_correction_in_ft: int = 250
            lateral_correction_in_ft = -22

            def grove_dev_component(grv_limit: float, x: float, fb_correction: float = 9,
                                    lateral_correction: float = lateral_correction_in_ft) -> float:
                rads = math.radians(grv_limit + fb_correction)
                return math.tan(rads) * x + Utils.feet_to_cbl(lateral_correction)

            # GRV Limits
            grv_limits_x_axis = numpy.linspace(x_axis_limit_left, x_axis_limit_right, x_axis_limit_left)
            grv___lul___limit = self.__grv_limits[GRV.limits()][GRV.___lul___()]
            grv__lul__limit = self.__grv_limits[GRV.limits()][GRV.__lul__()]
            grv_lul_limit = self.__grv_limits[GRV.limits()][GRV.lul()]
            grv_ok_limit = self.__grv_limits[GRV.limits()][GRV.ok()]
            grv_lur_limit = self.__grv_limits[GRV.limits()][GRV.lur()]
            grv__lur__limit = self.__grv_limits[GRV.limits()][GRV.__lur__()]
            grv___lur___limit = self.__grv_limits[GRV.limits()][GRV.___lur___()]

            lon_corr = Utils.feet_to_cbl(longitudinal_correction_in_ft)
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv___lul___limit, grv_limits_x_axis)
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__LUL__")
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv__lul__limit, grv_limits_x_axis)
                    , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="LUL")
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv_lul_limit, grv_limits_x_axis)
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(LUL)")
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv_ok_limit, grv_limits_x_axis)
                    , color='black', alpha=.5, linestyle='--', linewidth=.5, label="__OK__")
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv_lur_limit, grv_limits_x_axis)
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(LUR)")
            v = ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv__lur__limit, grv_limits_x_axis)
                        , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="LUR")
            ax.plot(grv_limits_x_axis + lon_corr, grove_dev_component(grv___lur___limit, grv_limits_x_axis)
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__LUR__")

            ax.fill_between(grv_limits_x_axis + lon_corr,
                            grove_dev_component(grv_lul_limit, grv_limits_x_axis),
                            grove_dev_component(grv_lur_limit, grv_limits_x_axis),
                            color='green', alpha=.1)
            ax.fill_between(grv_limits_x_axis + lon_corr,
                            grove_dev_component(grv_lul_limit, grv_limits_x_axis),
                            grove_dev_component(grv__lul__limit, grv_limits_x_axis),
                            color='orange', alpha=.1)
            ax.fill_between(grv_limits_x_axis + lon_corr,
                            grove_dev_component(grv_lur_limit, grv_limits_x_axis),
                            grove_dev_component(grv__lur__limit, grv_limits_x_axis),
                            color='orange', alpha=.1)
            ax.fill_between(grv_limits_x_axis + lon_corr,
                            grove_dev_component(grv__lul__limit, grv_limits_x_axis),
                            grove_dev_component(grv___lul___limit, grv_limits_x_axis),
                            color='red', alpha=.1)
            ax.fill_between(grv_limits_x_axis + lon_corr,
                            grove_dev_component(grv__lur__limit, grv_limits_x_axis),
                            grove_dev_component(grv___lur___limit, grv_limits_x_axis),
                            color='red', alpha=.1)

            # Brakepoints plot
            ax.axvline(x=Utils.mile_quarts(1, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--',
                       linewidth=1, label="1/4 Nm")
            ax.axvline(x=Utils.mile_quarts(2, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--',
                       linewidth=1, label="1/2 Nm'")
            ax.axvline(x=Utils.mile_quarts(3, mtrs=False, cbls=True), color='black', alpha=.5, linestyle='--',
                       linewidth=1, label="3/4 Nm'")
            ax.axvline(x=Utils.mile_quarts(4, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--',
                       linewidth=1, label="1 Nm'")

            # GRV plot
            df_X_smooth = np.linspace(
                Utils.mtrs_to_cbls(df.X.min()), Utils.mtrs_to_cbls(df.X.max()), int(len(df.X) * 100))
            f = interp1d(Utils.mtrs_to_cbls(df.X), Utils.mtrs_to_cbls(df.Z), kind='quadratic')
            df_GRV_smooth = f(df_X_smooth)
            ax.plot(df_X_smooth, df_GRV_smooth, linewidth=.75, label="int")
            ax.grid(False)

            # inset axes....
            # axins = ax.inset_axes([0.5, 0.6, 0.5, 0.4])
            # x1, x2, y1, y2 = 0.2, 2.5, 125, 0
            # axins.set_xlim(x1, x2)
            # axins.set_ylim(y1, y2)
            # axins.set_xticklabels([])
            # axins.set_yticklabels([])
            # axins.
            # ax.indicate_inset_zoom(axins, edgecolor="black")

        if save:
            plt.savefig('GRV_example.png', bbox_inches='tight', dpi=300)
        plt.show()
