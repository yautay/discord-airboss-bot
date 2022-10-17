class Common:
    @staticmethod
    def limits():
        return "limits"


class KeysAirframes:
    @staticmethod
    def type():
        return "type"

    @staticmethod
    def f18():
        return "F/A-18C"

    @staticmethod
    def f14():
        return "F-14"

    @staticmethod
    def av8():
        return "AV-8B"


class KeysAoA(Common):
    @staticmethod
    def slo_hi():
        return "aoa___slo___limit"

    @staticmethod
    def slo_med():
        return "aoa__slo__limit"

    @staticmethod
    def slo_lo():
        return "aoa_slo_limit"

    @staticmethod
    def ok():
        return "aoa_ok"

    @staticmethod
    def fast_lo():
        return "aoa_fst_limit"

    @staticmethod
    def fast_med():
        return "aoa__fst__limit"

    @staticmethod
    def fast_hi():
        return "aoa___fst___limit"


class KeysGS(Common):
    @staticmethod
    def ___hi___():
        return "gs___hi___limit"

    @staticmethod
    def __hi__():
        return "gs__hi__limit"

    @staticmethod
    def hi():
        return "gs_hi_limit"

    @staticmethod
    def gs():
        return "gs_ok"

    @staticmethod
    def lo():
        return "gs_lo_limit"

    @staticmethod
    def __lo__():
        return "gs__lo__limit"

    @staticmethod
    def ___lo___():
        return "gs___lo___limit"


class KeysGRV(Common):
    @staticmethod
    def ___lul___():
        return "grv___lul___limit"

    @staticmethod
    def __lul__():
        return "grv__lul__limit"

    @staticmethod
    def lul():
        return "grv_lul_limit"

    @staticmethod
    def ok():
        return "grv_ok"

    @staticmethod
    def lur():
        return "grv_lur_limit"

    @staticmethod
    def __lur__():
        return "grv__lur__limit"

    @staticmethod
    def ___lur___():
        return "grv___lur___limit"


class KeysCSV:
    @staticmethod
    def time():
        return "Time"

    @staticmethod
    def rho():
        return "Rho"

    @staticmethod
    def x():
        return "X"

    @staticmethod
    def z():
        return "Z"

    @staticmethod
    def alt():
        return "Alt"

    @staticmethod
    def aoa():
        return "AoA"

    @staticmethod
    def gse():
        return "GSE"

    @staticmethod
    def lue():
        return "LUE"

    @staticmethod
    def vtot():
        return "Vtot"

    @staticmethod
    def vy():
        return "Vy"

    @staticmethod
    def gamma():
        return "Gamma"

    @staticmethod
    def pitch():
        return "Pitch"

    @staticmethod
    def roll():
        return "Roll"

    @staticmethod
    def yaw():
        return "Yaw"

    @staticmethod
    def step():
        return "Step"

    @staticmethod
    def grade():
        return "Grade"

    @staticmethod
    def points():
        return "Points"

    @staticmethod
    def details():
        return "Details"

