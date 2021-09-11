from metpy.units import units

class unit:

    self.units_key={'slat':units.degrees, 'slon':units.degrees, 'selv':units.meters, 'stim':units.hours, 'show':units.dimensionless, 'lift':units.dimensionless, 'swet':units.dimensionless,
           'kinx':units.dimensionless, 'lclp':units.hPa, 'pwat':units.mm, 'totl':units.dimensionless, 'cape':(units.joules / units.kg), 'lclt':units.kelvin, 'cins':(units.joules / units.kg),
           'eqlv':units.hPa, 'lfct':units.hPa, 'brch':units.dimensionless, 'pres':units.hPa, 'tmpc':units.degC, 'tmwc':units.degC, 'dwpc':units.degC, 'thte':units.kelvin, 'drct':units.degrees,
           'sknt':units.knots, 'omeg':(units.Pa / units.seconds), 'cfrl':units.percent, 'hght':units.meters, 'pmsl':units.hPa, 'pres':units.hPa, 'sktc':units.degC, 'stc1':units.kelvin,
           'snfl':(units.mm), 'wtns':units.percent, 'p01m':units.mm, 'c01m':units.mm, 'stc2':units.kelvin, 'lcld':units.percent, 'mcld':units.percent, 'hcld':units.percent, 'snra':units.percent,
           'uwnd':(units.meter / units.seconds), 'vwnd':(units.meter / units.seconds), 'r01m':units.mm, 'bfgr':units.mm, 't2ms':units.degC, 'q2ms':units.dimensionless, 'wxts':units.dimensionless,
           'wxtp':units.dimensionless, 'wxtz':units.dimensionless, 'wxtr':units.dimensionless, 'ustm':(units.meter / units.seconds), 'vstm':(units.meter / units.seconds),
           'hlcy':((units.meter * units.meter ) / (units.seconds * units.seconds)), 'sllh':units.mm, 'wsym':units.dimensionless, 'cdbp':units.hPa, 'vsbk':units.km, 'td2m':units.degC}

    def __init__(param):
        """
        Takes a string of the parameter name and returns a metpy unit object for
        the parameter, if one exists.

        Unit key is based on http://www.meteo.psu.edu/bufkit/bufkit_parameters.txt.
        """
        if param.lower() in self.units_key.keys():
            return self.units_key[param]

        return None
