class Utils(object):

    @staticmethod
    def mtrs_to_nm(mtrs: float) -> float:
        return mtrs / 1852

    @staticmethod
    def cbl_to_feet(cbls: float) -> float:
        return cbls * 607.61155

    @staticmethod
    def feet_to_cbl(feet: float) -> float:
        return feet / 607.61155

    @staticmethod
    def mtrs_to_cbls(mtrs: float) -> float:
        return mtrs / 185.2

    @staticmethod
    def mtrs_to_feet(mtrs: float) -> float:
        return mtrs * 3.2808399

    @staticmethod
    def nm_to_mtrs(nm: float) -> float:
        return nm * 1852

    @staticmethod
    def nm_to_cbls(nm: float) -> float:
        return nm * 10

    @staticmethod
    def nm_to_feet(nm: float) -> float:
        return nm * 6076.11549

    @staticmethod
    def mile_quarts(quarts: int, mtrs: bool = True, nm: bool = False, cbls: bool = False, feet: bool = False) -> float:
        mile_decimal = quarts / 4
        if mtrs:
            return Utils.nm_to_mtrs(mile_decimal)
        elif nm:
            return mile_decimal
        elif cbls:
            return Utils.nm_to_cbls(mile_decimal)
        elif feet:
            return Utils.nm_to_feet(mile_decimal)


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

