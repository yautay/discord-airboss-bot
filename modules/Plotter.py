import math

import numpy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d

from modules.Keys import KeysCSV as K, KeysGRV as GRV, KeysGS as GS, KeysAoA as AoA
from modules.Utils import Utils, Bcolors


class Plotter(object):
    def __init__(self, file_path: str):
        self.__filename = file_path
        """ Time: time in seconds since start. 
                Rho: distance from rundown to player aircraft in NM.
                X : distance parallel to the carrier in meters.
                Z : distance perpendicular to the carrier in meters.
                Alt: altitude of player aircraft in feet.
                AoA: angle of attack in degrees.
                GSE: glideslope error in degrees.
                LUE: lineup error in degrees.
                Vtot: total velocity of player aircraft in knots.
                Vy: vertical (descent) velocity in ft/min.
                Gamma: angle between vector of aircraft nose and vector point in the direction of the carrier runway in degrees.
                Pitch: pitch angle of player aircraft in degrees.
                Roll: roll angle of player aircraft in degrees.
                Yaw: yaw angle of player aircraft in degrees.
                Step: Step in the groove.
                Grade: Current LSO grade.
                Points: Current points for the pass.
                Details: Detailed grading analysis."
            """
        self.__columns = [K.time(), K.rho(), K.x(), K.z(), K.alt(), K.aoa(), K.gse(), K.lue(), K.vtot(), K.vy(),
                          K.gamma(), K.pitch(), K.roll(), K.yaw(), K.step(), K.grade(), K.points(), K.details()]
        self.__data = pd.read_csv(self.__filename, usecols=self.__columns)
        self.__airframe = self.__airframe_context()

        self.__limits_aoa = self.__data_limits_aoa()
        self.__limits_grv = self.__data_limits_grv()
        self.__limits_gs = self.__data_limits_gs()

        # print("data:\n", self.__data)
        # print("airframe: ", self.__airframe_context(text=True))
        # print("AOA limits: ", self.__limits_aoa)
        # print("GRV limits:\n", self.__limits_grv)
        # print("GS limits:\n", self.__limits_gs)

    def __airframe_context(self, text: bool = False):
        """
        1: FA-18C
        2: F-14
        3: AV-8
        """
        if "FA-18C" in self.__filename:
            if text:
                return "F/A-18C"
            return 1
        elif "F-14" in self.__filename:
            if text:
                return "F-14"
            return 2
        elif "AV-8" in self.__filename:
            if text:
                return "AV-8B"
            return 9

    def __data_limits_aoa(self):
        if self.__airframe == 1:
            # F18
            return {
                AoA.slo_hi(): 9.8,
                AoA.slo_med(): 9.3,
                AoA.slo_lo(): 8.8,
                AoA.ok(): 8.1,
                AoA.fast_lo(): 7.4,
                AoA.fast_med(): 6.9,
                AoA.fast_hi(): 6.3,
            }

    def __data_limits_gs(self):
        if self.__airframe == 9:
            return {
                GS.___hi___(): 5.4,
                GS.__hi__(): 4.9,
                GS.hi(): 4.2,
                GS.gs(): 3.5,
                GS.lo(): 3,
                GS.__lo__(): 2.3,
                GS.___lo___(): 2.0,
            }
        else:
            return {
                GS.___hi___(): 5.0,
                GS.__hi__(): 4.3,
                GS.hi(): 3.9,
                GS.gs(): 3.5,
                GS.lo(): 3.2,
                GS.__lo__(): 2.9,
                GS.___lo___(): 2.6,
            }

    def __data_limits_gse(self):
        if self.__airframe == 9:
            return {
                GS.___hi___(): 1.9,
                GS.__hi__(): 1.4,
                GS.hi(): 0.7,
                GS.gs(): 0,
                GS.lo(): -0.5,
                GS.__lo__(): -1.2,
                GS.___lo___(): -1.5,
            }
        else:
            return {
                GS.___hi___(): 1.5,
                GS.__hi__(): 0.8,
                GS.hi(): 0.4,
                GS.gs(): 0,
                GS.lo(): -0.3,
                GS.__lo__(): -0.6,
                GS.___lo___(): -0.9,
            }

    @staticmethod
    def __data_limits_grv():
        return {
            GRV.___lul___(): -3,
            GRV.__lul__(): -1,
            GRV.lul(): -.5,
            GRV.ok(): 0,
            GRV.lur(): .5,
            GRV.__lur__(): 1,
            GRV.___lur___(): 3,
        }

    def plot_case1(self, file_name: str = "plot" or None, fillins: bool = False):
        def data_interpolate(smooth: int = 500, **kwargs):
            ax = kwargs["ax"]
            x = kwargs["x"]
            y = kwargs["y"]
            context = kwargs["C"]

            def downwind_stripper() -> int:
                x_max = x.max()
                # print(Bcolors.OKCYAN + "x max: " + str(x_max) + Bcolors.ENDC)
                downwind = False
                last_x = -9999
                downwind_index = None
                for i, v in x.items():
                    if v > 0:
                        if last_x <= v <= x_max:
                            last_x = v
                        elif last_x > v <= x_max:
                            if not downwind_index:
                                downwind_index = i
                            # print(i, v, "final")

                        else:
                            raise Exception("Downwind determination error!")
                # print(downwind_index)
                return downwind_index

            downwind_pool = - len(x) + downwind_stripper()

            x = x[downwind_pool:]
            y = y[downwind_pool:]

            X_smooth = np.linspace(x.iloc[:1], x.iloc[-1:], smooth)

            _f = interp1d(x, y, kind='quadratic')
            _dfs = _f(X_smooth)
            ax.plot(X_smooth, _dfs, linewidth=track_line_width, label="Track",
                    color=track_line_colour)
            # print(Bcolors.OKBLUE + context + Bcolors.ENDC)

        dta = self.__data

        # X-axis setup [cbls]
        x_axis_limit_left = 15
        x_axis_limit_right = 0
        limits_x_axis = numpy.linspace(x_axis_limit_right, x_axis_limit_left, x_axis_limit_left)

        # AoA Limits
        aoa_limits_data = self.__data_limits_aoa()
        aoa_slo_hi_limit = aoa_limits_data[AoA.slo_hi()]
        aoa_slo_med_limit = aoa_limits_data[AoA.slo_med()]
        aoa_slo_lo_limit = aoa_limits_data[AoA.slo_lo()]
        aoa_ok_limit = aoa_limits_data[AoA.ok()]
        aoa_fst_lo_limit = aoa_limits_data[AoA.fast_lo()]
        aoa_fst_med_limit = aoa_limits_data[AoA.fast_med()]
        aoa_fst_hi_limit = aoa_limits_data[AoA.fast_hi()]

        # GRV Limits
        grv_limits_data = self.__data_limits_grv()
        grv___lul___limit = grv_limits_data[GRV.___lul___()]
        grv__lul__limit = grv_limits_data[GRV.__lul__()]
        grv_lul_limit = grv_limits_data[GRV.lul()]
        grv_ok_limit = grv_limits_data[GRV.ok()]
        grv_lur_limit = grv_limits_data[GRV.lur()]
        grv__lur__limit = grv_limits_data[GRV.__lur__()]
        grv___lur___limit = grv_limits_data[GRV.___lur___()]

        # GS Limits
        gs_limits_data = self.__data_limits_gs()
        gs___hi___limit = gs_limits_data[GS.___hi___()]
        gs__hi__limit = gs_limits_data[GS.__hi__()]
        gs_hi_limit = gs_limits_data[GS.hi()]
        gs_ok_limit = gs_limits_data[GS.gs()]
        gs_lo_limit = gs_limits_data[GS.lo()]
        gs__lo__limit = gs_limits_data[GS.__lo__()]
        gs___lo___limit = gs_limits_data[GS.___lo___()]

        # GSE Limits
        gse_limits_data = self.__data_limits_gse()
        gse___hi___limit = gse_limits_data[GS.___hi___()]
        gse__hi__limit = gse_limits_data[GS.__hi__()]
        gse_hi_limit = gse_limits_data[GS.hi()]
        gse_ok_limit = gse_limits_data[GS.gs()]
        gse_lo_limit = gse_limits_data[GS.lo()]
        gse__lo__limit = gse_limits_data[GS.__lo__()]
        gse___lo___limit = gse_limits_data[GS.___lo___()]

        line_alpha = .3
        fill_alpha = .05
        track_line_width = .75
        track_line_colour = 'black'

        fig, (ax_grv, ax_gs, ax_aoa, utils) = plt.subplots(4)
        fig.set_size_inches(15, 25)
        fig.text(0.5, 0.05, self.__filename, horizontalalignment='center', verticalalignment='center',
                 color='red')


        def plot_distance_marks(axe):
            axe.axvline(x=Utils.mile_quarts(1, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1/4 Nm")
            axe.axvline(x=Utils.mile_quarts(2, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1/2 Nm'")
            axe.axvline(x=Utils.mile_quarts(3, mtrs=False, cbls=True), color='red', alpha=.75, linestyle='--',
                        linewidth=1, label="3/4 Nm'")
            axe.axvline(x=Utils.mile_quarts(4, mtrs=False, cbls=True), color='black', alpha=.15, linestyle='--',
                        linewidth=1, label="1 Nm'")

        def plotter_groove():
            grv_y_axis_limit_low = 2.5
            grv_y_axis_limit_hi = -.2
            grv_longitudinal_correction_in_ft = 290
            grv_lateral_correction_in_ft = 0

            def plotter_lue():
                axins_grv = ax_grv.inset_axes([.6, 0, .4, .4], transform=None, alpha=0.5, clip_path=None)
                x1, x2, y1, y2 = 6, 0, -4, 4
                axins_grv.set_xlim(x1, x2)
                axins_grv.set_ylim(y1, y2)
                axins_grv.text(.5, .9, "LUE [deg/cbls]", horizontalalignment='center',
                               transform=axins_grv.transAxes)

                def lue_plot_limits(limit, colour, label):
                        axins_grv.plot(
                            numpy.linspace(limit, limit),
                            color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)
                def lue_fill_limits(limit_1, limit_2, colour):
                    axins_grv.fill_between(
                        numpy.linspace(x1, x2, x1),
                        numpy.linspace(limit_1, limit_1, x1),
                        numpy.linspace(limit_2, limit_2, x1),
                        color=colour, alpha=fill_alpha)


                lue_plot_limits(grv___lul___limit, 'red', '__LUL__')
                lue_plot_limits(grv__lul__limit, 'orange', 'LUL')
                lue_plot_limits(grv_lul_limit, 'green', '(LUL)')
                lue_plot_limits(grv_lur_limit, 'green', '(LUR)')
                lue_plot_limits(grv__lur__limit, 'orange', 'LUR')
                lue_plot_limits(grv___lur___limit, 'red', '__LUL__')

                if fillins:
                    lue_fill_limits(grv___lul___limit, grv__lul__limit, 'red')
                    lue_fill_limits(grv__lul__limit, grv_lul_limit, 'orange')
                    lue_fill_limits(grv_lul_limit, grv_lur_limit, 'green')
                    lue_fill_limits(grv_lur_limit, grv__lur__limit, 'orange')
                    lue_fill_limits(grv__lur__limit, grv___lur___limit, 'red')

                data_interpolate(ax=axins_grv, x=Utils.mtrs_to_cbls(dta.X), y=dta.LUE, X=Utils.mtrs_to_cbls(dta.X),
                                 C="ins_groove")
                axins_grv.yaxis.tick_right()
                axins_grv.xaxis.tick_top()
                axins_grv.invert_yaxis()
                axins_grv.patch.set_alpha(0)
                axins_grv.grid(False)

            def grove_dev_component(grv_limit: float, x: float, fb_correction: float = 9,
                                    lateral_correction: float = grv_lateral_correction_in_ft) -> float:
                rads = math.radians(grv_limit + fb_correction)
                return math.tan(rads) * x + Utils.feet_to_cbl(lateral_correction)

            def grv_plot_limits(limit, colour, label):
                ax_grv.plot(
                    limits_x_axis + Utils.feet_to_cbl(grv_longitudinal_correction_in_ft),
                    grove_dev_component(limit, limits_x_axis),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def grv_fill_limits(limit_1, limit_2, colour):
                ax_grv.fill_between(
                    limits_x_axis + Utils.feet_to_cbl(grv_longitudinal_correction_in_ft),
                    grove_dev_component(limit_1, limits_x_axis),
                    grove_dev_component(limit_2, limits_x_axis),
                    color=colour, alpha=fill_alpha)

            ax_grv.set_ylim(grv_y_axis_limit_low, grv_y_axis_limit_hi)
            ax_grv.set_ylabel('lateral offset [Cbls]')
            ax_grv.set_xlabel("distance [Cbls]")
            ax_grv.set_xlim(x_axis_limit_right, x_axis_limit_left)

            grv_plot_limits(grv___lul___limit, 'red', '__LUL__')
            grv_plot_limits(grv__lul__limit, 'orange', 'LUL')
            grv_plot_limits(grv_lul_limit, 'green', '(LUL)')
            # grv_plot_limits(grv_ok_limit, 'black', '__OK__')
            grv_plot_limits(grv_lur_limit, 'green', '(LUR)')
            grv_plot_limits(grv__lur__limit, 'orange', 'LUR')
            grv_plot_limits(grv___lur___limit, 'red', '__LUR__')

            if fillins:
                grv_fill_limits(grv_lul_limit, grv_lur_limit, 'green')
                grv_fill_limits(grv_lul_limit, grv__lul__limit, 'orange')
                grv_fill_limits(grv_lur_limit, grv__lur__limit, 'orange')
                grv_fill_limits(grv__lul__limit, grv___lul___limit, 'red')
                grv_fill_limits(grv__lur__limit, grv___lur___limit, 'red')

            data_interpolate(ax=ax_grv, x=Utils.mtrs_to_cbls(dta.X), y=Utils.mtrs_to_cbls(dta.Z), C="groove")

            plot_distance_marks(ax_grv)
            ax_grv.invert_xaxis()
            ax_grv.grid(False)
            plotter_lue()

        def plotter_glideslope():
            gs_y_axis_limit_low = 0
            gs_y_axis_limit_hi = 850
            gs_longitudinal_correction_in_ft = 290
            gs_vertical_correction_in_ft = 0

            def plotter_gse():
                axins_gs = ax_gs.inset_axes([.6, .6, .4, .4], transform=None, alpha=0.5, clip_path=None)
                x1, x2, y1, y2 = 6, 0, gse___lo___limit - .5, gse___hi___limit + .5
                axins_gs.set_xlim(x1, x2)
                axins_gs.set_ylim(y1, y2)
                axins_gs.text(.5, .9, "GSE [deg/cbls]", horizontalalignment='center',
                              transform=axins_gs.transAxes)

                def gse_plot_limits(limit, colour, label):
                    axins_gs.plot(
                        numpy.linspace(limit, limit),
                        color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

                def gse_fill_limits(limit_1, limit_2, colour):
                    axins_gs.fill_between(
                        numpy.linspace(x1, x2, x1),
                        numpy.linspace(limit_1, limit_1, x1),
                        numpy.linspace(limit_2, limit_2, x1),
                        color=colour, alpha=fill_alpha)

                gse_plot_limits(gse___hi___limit, 'red', '__HI__')
                gse_plot_limits(gse__hi__limit, 'orange', 'H')
                gse_plot_limits(gse_hi_limit, 'green', '(H)')
                gse_plot_limits(gse_lo_limit, 'green', '(L)')
                gse_plot_limits(gse__lo__limit, 'orange', 'L')
                gse_plot_limits(gse___lo___limit, 'red', '__L__')

                if fillins:
                    gse_fill_limits(gse___hi___limit, gse__hi__limit, 'red')
                    gse_fill_limits(gse__hi__limit, gse_hi_limit, 'orange')
                    gse_fill_limits(gse_hi_limit, gse_lo_limit, 'green')
                    gse_fill_limits(gse_lo_limit, gse__lo__limit, 'orange')
                    gse_fill_limits(gse__lo__limit, gse___lo___limit, 'red')

                data_interpolate(ax=axins_gs, x=Utils.mtrs_to_cbls(dta.X), y=dta.GSE, C="ins_gs")

                axins_gs.patch.set_alpha(0)
                axins_gs.yaxis.tick_right()
                axins_gs.grid(False)

            def glideslope_alt_component(gs_limit: float, x: float) -> float:
                rads = math.radians(gs_limit)
                return math.tan(rads) * x + gs_vertical_correction_in_ft

            def gs_plot_limits(limit, colour, label):
                ax_gs.plot(
                    limits_x_axis + Utils.feet_to_cbl(gs_longitudinal_correction_in_ft),
                    glideslope_alt_component(limit, Utils.cbl_to_feet(limits_x_axis))
                    , color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def gs_fill_limits(limit_1, limit_2, colour):
                ax_gs.fill_between(
                    limits_x_axis + Utils.feet_to_cbl(gs_longitudinal_correction_in_ft),
                    glideslope_alt_component(limit_1, Utils.cbl_to_feet(limits_x_axis)),
                    glideslope_alt_component(limit_2, Utils.cbl_to_feet(limits_x_axis)),
                    color=colour, alpha=fill_alpha)

            ax_gs.set_ylim(gs_y_axis_limit_low, gs_y_axis_limit_hi)
            ax_gs.set_xlim(x_axis_limit_right, x_axis_limit_left)
            ax_gs.set_ylabel('height [feet]')
            ax_gs.set_xlabel("distance [Cbls]")

            gs_plot_limits(gs___hi___limit, 'red', '__HI__')
            gs_plot_limits(gs__hi__limit, 'orange', 'H')
            gs_plot_limits(gs_hi_limit, 'green', '(H)')
            # gs_plot_limits(gs_ok_limit, 'black', '__OK__')
            gs_plot_limits(gs_lo_limit, 'green', '(LO)')
            gs_plot_limits(gs__lo__limit, 'orange', 'LO')
            gs_plot_limits(gs___lo___limit, 'red', '__LO__')

            if fillins:
                gs_fill_limits(gs_lo_limit, gs_hi_limit, 'green')
                gs_fill_limits(gs_lo_limit, gs__lo__limit, 'orange')
                gs_fill_limits(gs_hi_limit, gs__hi__limit, 'orange')
                gs_fill_limits(gs__lo__limit, gs___lo___limit, 'red')
                gs_fill_limits(gs__hi__limit, gs___hi___limit, 'red')

            data_interpolate(ax=ax_gs, x=Utils.mtrs_to_cbls(dta.X), y=dta.Alt, C="gs")

            plot_distance_marks(ax_gs)
            ax_gs.invert_xaxis()
            ax_gs.grid(False)
            plotter_gse()

        def plotter_aoa():
            # AoA
            aoa_y_axis_limit_low = aoa_limits_data[AoA.fast_hi()] - .5
            aoa_y_axis_limit_hi = aoa_limits_data[AoA.slo_hi()] + .5
            ax_aoa.set_ylim(aoa_y_axis_limit_low, aoa_y_axis_limit_hi)
            ax_aoa.set_xlim(x_axis_limit_right, x_axis_limit_left)
            ax_aoa.set_ylabel('AoA [deg]')
            ax_aoa.set_xlabel("distance [Cbls]")

            def aoa_plot_limits(limit, colour, label):
                ax_aoa.plot(
                    numpy.linspace(limit, limit, x_axis_limit_left),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)

            def aoa_fill_limits(limit_1, limit_2, colour):
                ax_aoa.fill_between(
                    limits_x_axis,
                    numpy.linspace(limit_1, limit_1, x_axis_limit_left),
                    numpy.linspace(limit_2, limit_2, x_axis_limit_left),
                    color=colour, alpha=.03)

            aoa_plot_limits(aoa_slo_hi_limit, 'red', "__SLO__")
            aoa_plot_limits(aoa_slo_med_limit, 'orange', "SLO")
            aoa_plot_limits(aoa_slo_lo_limit, 'green', "(SLO)")
            # aoa_plot_limits(aoa_ok_limit, 'black', "__OK__")
            aoa_plot_limits(aoa_fst_lo_limit, 'green', "(F)")
            aoa_plot_limits(aoa_fst_med_limit, 'orange', "F")
            aoa_plot_limits(aoa_fst_hi_limit, 'red', "__F__")

            if fillins:
                aoa_fill_limits(aoa_slo_hi_limit, aoa_slo_med_limit, 'red')
                aoa_fill_limits(aoa_slo_med_limit, aoa_slo_lo_limit, 'orange')
                aoa_fill_limits(aoa_slo_lo_limit, aoa_fst_lo_limit, 'green')
                aoa_fill_limits(aoa_fst_lo_limit, aoa_fst_med_limit, 'orange')
                aoa_fill_limits(aoa_fst_med_limit, aoa_fst_hi_limit, 'red')

            data_interpolate(ax=ax_aoa, x=Utils.mtrs_to_cbls(dta.X), y=dta.AoA, C="aoa")

            plot_distance_marks(ax_aoa)
            ax_aoa.invert_xaxis()
            ax_aoa.grid(False)

        def plotter_utils():
            # UTILS
            utils.set_xticks([], [])
            utils.set_yticks([], [])

            utils_y_axis_limit_lo = 0
            utils_y_axis_limit_hi = 1
            utils.set_ylim(utils_y_axis_limit_lo, utils_y_axis_limit_hi)

            axins_vy = utils.inset_axes([0, 0, .5, 1], transform=None, alpha=0.5, clip_path=None)
            axins_roll = utils.inset_axes([.5, 0, .5, 1], transform=None, alpha=0.5, clip_path=None)
            vyx1, vyx2, vyy1, vyy2 = 6, 0, -400, -1500
            rx1, rx2, ry1, ry2 = 6, 0, 50, -50
            axins_vy.set_xlim(vyx1, vyx2)
            axins_vy.set_ylim(vyy1, vyy2)
            axins_roll.set_xlim(rx1, rx2)
            axins_roll.set_ylim(ry1, ry2)
            axins_roll.yaxis.tick_right()
            axins_vy.grid(False)
            axins_roll.grid(False)
            axins_roll.patch.set_alpha(0)
            axins_vy.patch.set_alpha(0)
            axins_vy.set_xticks([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6])
            axins_roll.set_xticks([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5])
            axins_vy.set_ylabel('Vertical spd [ft/min]')
            axins_vy.set_xlabel("distance [Cbls]")
            axins_roll.set_ylabel('Bank Angle [deg]')
            axins_roll.yaxis.set_label_position("right")
            axins_roll.set_xlabel("distance [Cbls]")

            def plot_lin_limits(limit, colour, label, axin):
                axin.plot(
                    numpy.linspace(limit, limit),
                    color=colour, alpha=line_alpha, linestyle='--', linewidth=1, label=label)
            def fill_lin_limits(limit_1, limit_2, colour, axin):
                axin.fill_between(
                    numpy.linspace(vyx1, vyx2, vyx1),
                    numpy.linspace(limit_1, limit_1, vyx1),
                    numpy.linspace(limit_2, limit_2, vyx1),
                    color=colour, alpha=fill_alpha)

            plot_lin_limits(-900, 'red', 'Vy limit', axins_vy)
            fill_lin_limits(-900, vyy2, 'red', axins_vy)
            axins_vy.text(.5, .75, "EXTENDED LANDING GEAR INSPECTION", horizontalalignment='center', transform=axins_vy.transAxes)

            plot_lin_limits(-2.5, 'green', 'roll limit', axins_roll)
            plot_lin_limits(2.5, 'green', 'roll limit', axins_roll)

            data_interpolate(ax=axins_vy, x=Utils.mtrs_to_cbls(dta.X), y=dta.Vy, C="ins_vy")
            data_interpolate(ax=axins_roll, x=Utils.mtrs_to_cbls(dta.X), y=dta.Roll, C="ins_roll")

        plotter_groove()
        plotter_glideslope()
        plotter_aoa()
        plotter_utils()

        plt.xlim(x_axis_limit_left, x_axis_limit_right)
        if file_name:
            plt.savefig(file_name, bbox_inches='tight', dpi=300)
            plt.savefig(file_name + "-alpha", bbox_inches='tight', dpi=300, transparent=True)
        plt.show()
