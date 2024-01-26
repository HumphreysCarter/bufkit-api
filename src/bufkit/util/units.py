from metpy.units import units as ureg


class units:

    def __new__(cls, param):
        """
        Takes a string of the parameter name and returns a metpy unit object for
        the parameter, if one exists.

        Unit key is based on http://www.meteo.psu.edu/bufkit/bufkit_parameters.txt.
        """
        # Create a new instance of the class
        instance = super(units, cls)

        # Unit definitions
        units_key = {'slat': ureg.degrees, 'slon': ureg.degrees, 'selv': ureg.meters, 'stim': ureg.hours,
                     'show': ureg.dimensionless, 'lift': ureg.dimensionless, 'swet': ureg.dimensionless,
                     'kinx': ureg.dimensionless, 'lclp': ureg.hPa, 'pwat': ureg.mm, 'totl': ureg.dimensionless,
                     'cape': (ureg.joules / ureg.kg), 'lclt': ureg.kelvin, 'cins': (ureg.joules / ureg.kg),
                     'eqlv': ureg.hPa, 'lfct': ureg.hPa, 'brch': ureg.dimensionless, 'pres': ureg.hPa,
                     'tmpc': ureg.degC, 'tmwc': ureg.degC, 'dwpc': ureg.degC, 'thte': ureg.kelvin, 'drct': ureg.degrees,
                     'sknt': ureg.knots, 'omeg': (ureg.Pa / ureg.seconds), 'cfrl': ureg.percent, 'hght': ureg.meters,
                     'pmsl': ureg.hPa, 'pres': ureg.hPa, 'sktc': ureg.degC, 'stc1': ureg.kelvin,
                     'snfl': (ureg.mm), 'wtns': ureg.percent, 'p01m': ureg.mm, 'c01m': ureg.mm, 'stc2': ureg.kelvin,
                     'lcld': ureg.percent, 'mcld': ureg.percent, 'hcld': ureg.percent, 'snra': ureg.percent,
                     'uwnd': (ureg.meter / ureg.seconds), 'vwnd': (ureg.meter / ureg.seconds), 'r01m': ureg.mm,
                     'bfgr': ureg.mm, 't2ms': ureg.degC, 'q2ms': ureg.dimensionless, 'wxts': ureg.dimensionless,
                     'wxtp': ureg.dimensionless, 'wxtz': ureg.dimensionless, 'wxtr': ureg.dimensionless,
                     'ustm': (ureg.meter / ureg.seconds), 'vstm': (ureg.meter / ureg.seconds),
                     'hlcy': ((ureg.meter * ureg.meter) / (ureg.seconds * ureg.seconds)), 'sllh': ureg.mm,
                     'wsym': ureg.dimensionless, 'cdbp': ureg.hPa, 'vsbk': ureg.km, 'td2m': ureg.degC}

        if param.lower() in units_key.keys():
            return units_key[param.lower()]

        return None
