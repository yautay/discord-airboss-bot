import pandas as pd
from modules.Keys import KeysCSV as K


class BasePlotter(K):
    def __init__(self, file_path: str):
        self.__filename = file_path
        self.__columns = [K.time(), K.rho(), K.x(), K.z(), K.alt(), K.aoa(), K.gse(), K.lue(), K.vtot(), K.vy(),
                          K.gamma(), K.pitch(), K.roll(), K.yaw(), K.step(), K.grade(), K.points(), K.details()]
        self.__data = pd.read_csv(self.__filename, usecols=self.__columns)
        self.__airframe = self.__airframe_context()

    def __airframe_context(self):
        """
        1: FA-18C
        2: F-14
        3: AV-8
        """
        if "FA-18C" in self.__filename:
            return 1
        elif "F-14" in self.__filename:
            return 2
        elif "AV-8" in self.__filename:
            return 9

    @property
    def data(self):
        return self.__data

    @property
    def airframe(self):
        return self.__airframe

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
