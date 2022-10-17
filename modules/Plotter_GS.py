import math

import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from scipy.interpolate import interp1d
from modules.Keys import KeysCSV as K, KeysGS as GS
from modules.Utils import Utils
from modules.Base_Plotter import BasePlotter


class PlotterGS(BasePlotter):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.__airframe = self.airframe
        self.__data = self.data[[K.x(), K.alt(), K.gse()]]
        self.__gs_limits = self.__gs_limits_data()
        print("GS data:\n", self.__data)
        print("GS limits:\n", self.__gs_limits)

    def __gs_limits_data(self):
        if self.__airframe == 9:
            return {
                GS.limits(): {
                    GS.___hi___(): 5.4,
                    GS.__hi__(): 4.9,
                    GS.hi(): 4.2,
                    GS.gs(): 3.5,
                    GS.lo(): 3,
                    GS.__lo__(): 2.3,
                    GS.___lo___(): 2.0,
                }
            }
        else:
            return {
                GS.limits(): {
                    GS.___hi___(): 5.0,
                    GS.__hi__(): 4.3,
                    GS.hi(): 3.9,
                    GS.gs(): 3.5,
                    GS.lo(): 3.2,
                    GS.__lo__(): 2.9,
                    GS.___lo___(): 2.6,
                }
            }

    def plot_gs_graph(self, save: bool = False):
        with plt.style.context('Solarize_Light2'):
            df = self.__data
            fig, ax = plt.subplots()

            # X-axis setup
            x_axis_limit_left = 11
            x_axis_limit_right = 0
            ax.set_xlim(x_axis_limit_left, x_axis_limit_right)
            ax.set_xlabel('distance [Cbls]')

            # Y-axis setup
            y_axis_limit_low = 0
            y_axis_limit_hi = df.Alt.max() + 50
            ax.set_ylim(y_axis_limit_low, y_axis_limit_hi)
            ax.set_ylabel('height [feet]')

            def glideslope_y_component(glideslope: int, x: float or int) -> float:
                rads = math.radians(glideslope)
                return math.tan(rads) * x

            # GS Limits
            gs_limits_x_axis = numpy.linspace(x_axis_limit_left, x_axis_limit_right, x_axis_limit_left)
            gs___hi___limit = self.__gs_limits[GS.limits()][GS.___hi___()]
            gs__hi__limit = self.__gs_limits[GS.limits()][GS.__hi__()]
            gs_hi_limit = self.__gs_limits[GS.limits()][GS.hi()]
            ok_limit = self.__gs_limits[GS.limits()][GS.gs()]
            gs_lo_limit = self.__gs_limits[GS.limits()][GS.lo()]
            gs__lo__limit = self.__gs_limits[GS.limits()][GS.__lo__()]
            gs___lo___limit = self.__gs_limits[GS.limits()][GS.___lo___()]

            IFLOS_correction_in_ft = 275
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs___hi___limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__HI__")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs__hi__limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="H")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs_hi_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(H)")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(ok_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='black', alpha=.5, linestyle='--', linewidth=.5, label="__OK__")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs_lo_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(LO)")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs__lo__limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="LO")
            ax.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs___lo___limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__LO__")

            ax.fill_between(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                            glideslope_y_component(gs_lo_limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            glideslope_y_component(gs_hi_limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            color='green', alpha=.1)
            ax.fill_between(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                            glideslope_y_component(gs_lo_limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            glideslope_y_component(gs__lo__limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            color='orange', alpha=.1)
            ax.fill_between(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                            glideslope_y_component(gs_hi_limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            glideslope_y_component(gs__hi__limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            color='orange', alpha=.1)
            ax.fill_between(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                            glideslope_y_component(gs__lo__limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            glideslope_y_component(gs___lo___limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            color='red', alpha=.1)
            ax.fill_between(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                            glideslope_y_component(gs__hi__limit, Utils.cbl_to_feet(gs_limits_x_axis)),
                            glideslope_y_component(gs___hi___limit, Utils.cbl_to_feet(gs_limits_x_axis)),
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

            # GS coords
            df_X_smooth = np.linspace(
                Utils.mtrs_to_cbls(df.X.min()), Utils.mtrs_to_cbls(df.X.max()), int(len(df.X) * 100))
            gs = interp1d(Utils.mtrs_to_cbls(df.X), df.Alt, kind='quadratic')
            gse = interp1d(Utils.mtrs_to_cbls(df.X), df.GSE, kind='quadratic')
            df_GS_smooth = gs(df_X_smooth)
            df_GSE_smooth = gse(df_X_smooth)



            ax.plot(df_X_smooth, df_GS_smooth, linewidth=.75, label="int")
            ax.grid(False)

            # inset axes....
            axins = ax.inset_axes([.5, .6, .5, .4], transform=None , alpha=0.5, clip_path=None)
            x1, x2, y1, y2 = 2.5, .3, 0, 2
            axins.set_xlim(x1, x2)
            axins.set_ylim(y1, y2)
            # axins.set_xticklabels([])
            # axins.set_yticklabels([1, 500])

            axins.plot(df_X_smooth, df_GSE_smooth, linewidth=.75, label="int")

            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs___hi___limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__HI__")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs__hi__limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="H")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs_hi_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(H)")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(ok_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='black', alpha=.5, linestyle='--', linewidth=.5, label="__OK__")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs_lo_limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='green', alpha=.5, linestyle='--', linewidth=.5, label="(LO)")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                        glideslope_y_component(gs__lo__limit, Utils.cbl_to_feet(gs_limits_x_axis))
                        , color='orange', alpha=.5, linestyle='--', linewidth=.5, label="LO")
            axins.plot(gs_limits_x_axis + Utils.feet_to_cbl(IFLOS_correction_in_ft),
                    glideslope_y_component(gs___lo___limit, Utils.cbl_to_feet(gs_limits_x_axis))
                    , color='red', alpha=.5, linestyle='--', linewidth=.5, label="__LO__")
            # axins.
            ax.indicate_inset_zoom(axins, edgecolor="black")

        if save:
            plt.savefig('GS_example.png', bbox_inches='tight', dpi=300)
        plt.show()
