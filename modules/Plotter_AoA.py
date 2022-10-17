import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import Keys
from modules.Keys import \
    KeysCSV as K, \
    KeysAoA as AoA, \
    KeysAirframes as Airframe
from modules.Base_Plotter import BasePlotter
from modules.Utils import Utils


class PlotterAoA(BasePlotter):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.__airframe = self.airframe
        self.__data = self.data[[K.x(), K.aoa()]]
        self.__airframe_limits = self.__airframes_data()
        print("AoA data:\n", self.__data)
        print("Airframe limits: ", self.__airframe_limits)

    def __airframes_data(self):
        if self.__airframe == 1:
            return {
                Airframe.type(): Airframe.f18(),
                AoA.limits(): {
                    AoA.slo_hi(): 9.8,
                    AoA.slo_med(): 9.3,
                    AoA.slo_lo(): 8.8,
                    AoA.ok(): 8.1,
                    AoA.fast_lo(): 7.4,
                    AoA.fast_med(): 6.9,
                    AoA.fast_hi(): 6.3,
                }
            }

    def plot_aoa_graph(self, save: bool = False):
        with plt.style.context('Solarize_Light2'):
            df = self.__data
            fig, ax = plt.subplots()

            # X-axis setup
            x_axis_limit_left = 11
            x_axis_limit_right = 0
            ax.set_xlim(x_axis_limit_left, x_axis_limit_right)
            ax.set_xlabel('distance [Cbls]')

            # Y-axis setup
            y_axis_limit_low = self.__airframe_limits[AoA.limits()][AoA.fast_hi()] - .5
            y_axis_limit_hi = self.__airframe_limits[AoA.limits()][AoA.slo_hi()] + .5
            ax.set_ylim(y_axis_limit_low, y_axis_limit_hi)
            ax.set_ylabel('AoA [deg]')

            # AoA Limits
            aoa_limits_x_axis = numpy.linspace(x_axis_limit_left, x_axis_limit_right, x_axis_limit_left)
            slo_hi_limit = self.__airframe_limits[AoA.limits()][AoA.slo_hi()]
            slo_med_limit = self.__airframe_limits[AoA.limits()][AoA.slo_med()]
            slo_lo_limit = self.__airframe_limits[AoA.limits()][AoA.slo_lo()]
            ok_limit = self.__airframe_limits[AoA.limits()][AoA.ok()]
            fst_lo_limit = self.__airframe_limits[AoA.limits()][AoA.fast_lo()]
            fst_med_limit = self.__airframe_limits[AoA.limits()][AoA.fast_med()]
            fst_hi_limit = self.__airframe_limits[AoA.limits()][AoA.fast_hi()]

            slo_hi_line = numpy.linspace(slo_hi_limit, slo_hi_limit, x_axis_limit_left)
            slo_med_line = numpy.linspace(slo_med_limit, slo_med_limit, x_axis_limit_left)
            slo_lo_line = numpy.linspace(slo_lo_limit, slo_lo_limit, x_axis_limit_left)
            ok_line = numpy.linspace(ok_limit, ok_limit, x_axis_limit_left)
            fst_lo_line = numpy.linspace(fst_lo_limit, fst_lo_limit, x_axis_limit_left)
            fst_med_line = numpy.linspace(fst_med_limit, fst_med_limit, x_axis_limit_left)
            fst_hi_line = numpy.linspace(fst_hi_limit, fst_hi_limit, x_axis_limit_left)

            ax.plot(aoa_limits_x_axis, slo_hi_line, color='red', alpha=.5, linestyle='--', linewidth=.5,
                    label="__SLO__")
            ax.plot(aoa_limits_x_axis, slo_med_line, color='orange', alpha=.5, linestyle='--', linewidth=.5,
                    label="SLO")
            ax.plot(aoa_limits_x_axis, slo_lo_line, color='green', alpha=.5, linestyle='--', linewidth=.5,
                    label="(SLO)")
            ax.plot(aoa_limits_x_axis, ok_line, color='black', alpha=.5, linestyle='--', linewidth=.5,
                    label="__OK__")
            ax.plot(aoa_limits_x_axis, fst_lo_line, color='green', alpha=.5, linestyle='--', linewidth=.5,
                    label="(F)")
            ax.plot(aoa_limits_x_axis, fst_med_line, color='orange', alpha=.5, linestyle='--', linewidth=.5,
                    label="F")
            ax.plot(aoa_limits_x_axis, fst_hi_line, color='red', alpha=.5, linestyle='--', linewidth=.5,
                    label="__F__")

            ax.fill_between(aoa_limits_x_axis, slo_lo_line, fst_lo_line, color='green', alpha=.1)
            ax.fill_between(aoa_limits_x_axis, fst_lo_line, fst_med_line, color='orange', alpha=.1)
            ax.fill_between(aoa_limits_x_axis, slo_lo_line, slo_med_line, color='orange', alpha=.1)
            ax.fill_between(aoa_limits_x_axis, fst_med_line, fst_hi_line, color='red', alpha=.1)
            ax.fill_between(aoa_limits_x_axis, slo_med_line, slo_hi_line, color='red', alpha=.1)

            # Brakepoints plot
            ax.axvline(x=Utils.mile_quarts(1, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--', linewidth=1, label="1/4 Nm")
            ax.axvline(x=Utils.mile_quarts(2, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--', linewidth=1, label="1/2 Nm'")
            ax.axvline(x=Utils.mile_quarts(3, mtrs=False, cbls=True), color='black', alpha=.5, linestyle='--', linewidth=1, label="3/4 Nm'")
            ax.axvline(x=Utils.mile_quarts(4, mtrs=False, cbls=True), color='black', alpha=.25, linestyle='--', linewidth=1, label="1 Nm'")


            # AoA plot
            df_X_smooth = np.linspace(
                Utils.mtrs_to_cbls(df.X.min()), Utils.mtrs_to_cbls(df.X.max()), int(len(df.X) * 100))
            f = interp1d(Utils.mtrs_to_cbls(df.X), df.AoA, kind='quadratic')
            df_AoA_smooth = f(df_X_smooth)
            ax.plot(df_X_smooth, df_AoA_smooth, linewidth=.75, label="int")

            ax.grid(False)

        if save:
            plt.savefig('AoA_example.png', bbox_inches='tight', dpi=300)
        plt.show()
