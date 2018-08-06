# -*- coding: utf-8 -*-
"""Physical constants.
"""
import scipy.constants as spc
import typhon.constants as tyc


# Phyiscal constants
Cp = isobaric_mass_heat_capacity = 1003.5  # J kg^-1 K^-1
g = earth_standard_gravity = spc.g  # m s^-2
stefan_boltzmann = 5.67e-8  # W m^-2 K^-4
heat_of_vaporization = Lv = 2501000  # J k^-1
specific_gas_constant_dry_air = Rd = tyc.gas_constant_dry_air  # J kg^-1 K^-1
specific_gas_constant_water_vapor = Rv = tyc.gas_constant_water_vapor  # J kg^-1 K^-1
gas_constant_ratio = epsilon = Rd / Rv  # 1
density_sea_water = 1025  # kg m^-3
specific_heat_capacity_sea_water = 4185.5  # J kg^-1 K^-1
molar_gas_constant_dry_air = molar_Rd = spc.gas_constant # J mol^-1 K^-1
avogadro = tyc.avogadro # molecules per mole

# Variable descriptions
variable_description = {
    # Atmospheric variables
    'plev': {
        'units': 'Pa',
        'standard_name': 'air_pressure',
        },
    'phlev': {
        'units': 'Pa',
        'standard_name': 'air_pressure_at_halflevel',
    },
    'time': {
        'standard_name': 'time',
        'units': 'hours since 0001-01-01 00:00:00.0',
        'calender': 'gregorian',
        },
    'T': {
        'units': 'K',
        'standard_name': 'air_temperature',
        'arts_name': 'T',
        'dims': ('time', 'plev'),
        },
    'z': {
        'units': 'm',
        'standard_name': 'geopotential_height',
        'description': 'Geopotential height calculated from atmospheric state',
        'arts_name': 'z',
        'dims': ('time', 'plev'),
        },
    'lapse': {
        'units': 'K / m',
        'standard_name': 'air_temperature_lapse_rate',
    },
    'H2O': {
        'units': '1',
        'standard_name': 'humidity_mixing_ratio',
        'arts_name': 'abs_species-H2O',
        'dims': ('time', 'plev'),
        },
    'N2O': {
        'units': '1',
        'standard_name': 'nitrogene_mixing_ratio',
        'arts_name': 'abs_species-N2O',
        'dims': ('plev',),
        'default_vmr': 306e-9,
        },
    'O3': {
        'units': '1',
        'standard_name': 'ozone_mixing_ratio',
        'arts_name': 'abs_species-O3',
        'dims': ('time', 'plev'),
        },
    'O2': {
        'units': '1',
        'standard_name': 'oxygen_mixing_ratio',
        'arts_name': 'abs_species-O2',
        'dims': ('plev',),
        'default_vmr': 0.21,
    },
    'CO2': {
        'units': '1',
        'standard_name': 'carbon_dioxide_mixing_ratio',
        'arts_name': 'abs_species-CO2',
        'dims': ('plev',),
        'default_vmr': 348e-6,
        },
    'CO': {
        'units': '1',
        'standard_name': 'carbon_monoxide_mixing_ratio',
        'arts_name': 'abs_species-CO',
        'dims': ('plev',),
        'default_vmr': 0.,
        },
    'CH4': {
        'units': '1',
        'standard_name': 'methane_mixing_ratio',
        'arts_name': 'abs_species-CH4',
        'dims': ('plev',),
        'default_vmr': 1650e-9,
        },
    'CFC11': {
        'units': '1',
        'standard_name': 'cfc11_mixing_ratio',
        'arts_name': 'abs_species-CFC11',
        'dims': ('plev',),
        'default_vmr': 0.,
    },
    'CFC12': {
        'units': '1',
        'standard_name': 'cfc12_mixing_ratio',
        'arts_name': 'abs_species-CFC12',
        'dims': ('plev',),
        'default_vmr': 0.,
    },
    'CFC22': {
        'units': '1',
        'standard_name': 'cfc22_mixing_ratio',
        'arts_name': 'abs_species-CFC22',
        'dims': ('plev',),
        'default_vmr': 0.,
    },
    'CCl4': {
        'units': '1',
        'standard_name': 'carbon_tetrachloride_mixing_ratio',
        'arts_name': 'abs_species-CCl4',
        'dims': ('plev',),
        'default_vmr': 0.,
    },
    'diabatic_convergence_max_plev': {
        'units': 'Pa',
        'standard_name': 'diabatic_convergence_max_plev',
        'description': 'Pressure level of maximum diabatic convergence',
        'dims': ('time',),
    },
    'diabatic_convergence_max_index': {
        'units': '1',
        'standard_name': 'diabatic_convergence_max_index',
        'description': 'Level index of maximum diabatic convergence',
        'dims': ('time',),
    },
    'convective_top_plev': {
        'units': 'Pa',
        'standard_name': 'convective_top_plev',
        'description': 'Pressure level of the top of convection',
        'dims': ('time',),
    },
    'convective_top_temperature': {
        'units': 'K',
        'standard_name': 'convective_top_temperature',
        'description': 'Temperature at the top of convection',
        'dims': ('time',),
    },
    # Radiative quantities
    'lw_htngrt': {
        'units': 'K / day',
        'standard_name': 'tendency_of_air_temperature_due_to_longwave_heating',
        },
    'lw_htngrt_clr': {
        'units': 'K / day',
        'standard_name': ('tendency_of_air_temperature_'
                          'due_to_longwave_heating_assuming_clear_sky'
                          ),
        },
    'lw_flxu': {
        'units': 'W / m**2',
        'standard_name': 'upwelling_longwave_flux_in_air',
        },
    'lw_flxd': {
        'units': 'W / m**2',
        'standard_name': 'downwelling_longwave_flux_in_air',
        },
    'lw_flxu_clr': {
        'units': 'W / m**2',
        'standard_name': 'upwelling_longwave_flux_in_air_assuming_clear_sky',
        },
    'lw_flxd_clr': {
        'units': 'W / m**2',
        'standard_name': 'downwelling_longwave_flux_in_air_assuming_clear_sky',
        },
    'sw_htngrt': {
        'units': 'K / day',
        'standard_name':
            'tendency_of_air_temperature_due_to_shortwave_heating',
        },
    'sw_htngrt_clr': {
        'units': 'K / day',
        'standard_name': ('tendency_of_air_temperature_'
                          'due_to_shortwave_heating_assuming_clear_sky'
                          ),
        },
    'sw_flxu': {
        'units': 'W / m**2',
        'standard_name': 'upwelling_shortwave_flux_in_air',
        },
    'sw_flxd': {
        'units': 'W / m**2',
        'standard_name': 'downwelling_shortwave_flux_in_air',
        },
    'sw_flxu_clr': {
        'units': 'W / m**2',
        'standard_name': 'upwelling_shortwave_flux_in_air_assuming_clear_sky',
        },
    'sw_flxd_clr': {
        'units': 'W / m**2',
        'standard_name':
            'downwelling_shortwave_flux_in_air_assuming_clear_sky',
        },
    'net_htngrt': {
        'units': 'K / day',
        'standard_name':
            'tendency_of_air_temperature_due_to_radiative_heating',
        },
    'toa': {
        'units': 'W / m**2',
        'standard_name':
            'radiation_budget_at_top_of_the_atmosphere',
    },
    'deltaT': {
        'units': 'K / day',
        'standard_name': 'tendency_of_air_temperature',
        },
    # Surface parameters
    'albedo': {
        'units': '1',
        'standard_name': 'surface_albedo',
    },
    'pressure': {
        'units': 'Pa',
        'standard_name': 'surface_pressure',
    },
    'temperature': {
        'units': 'K',
        'standard_name': 'surface_temperature',
    },
    'c_p': {
        'units': 'J / kg / K',
        'standard_name': 'specific_heat_capacity_sea_water',
    },
    'rho': {
        'units': 'kg / m**3',
        'standard_name': 'surface_density',
    },
    'depth': {
        'units': 'm',
        'standard_name': 'surface_depth',
    },
    'heat_capacity': {
        'units': 'J / K',
        'standard_name': 'surface_heat_capacity',
    },
}
