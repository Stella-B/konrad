# -*- coding: utf-8 -*-
"""Implementation of a radiative-convective equilibrium model (RCE).
"""
import logging
from datetime import datetime

import numpy as np

from konrad import utils
from konrad.radiation import RRTMG
from konrad.humidity import (Humidity, FixedRH)
from konrad.surface import (Surface, SurfaceHeatCapacity)
from konrad.cloud import (Cloud, ClearSky)
from konrad.convection import (Convection, HardAdjustment)
from konrad.lapserate import (LapseRate, MoistLapseRate)
from konrad.upwelling import (Upwelling, NoUpwelling)


logger = logging.getLogger(__name__)

__all__ = [
    'RCE',
]


class RCE:
    """Interface to control the radiative-convective equilibrium simulation.

    Examples:
        Create an object to setup and run a simulation:
        >>> import konrad
        >>> rce = konrad.RCE(...)
        >>> rce.run()
    """
    def __init__(self, atmosphere, radiation=None, humidity=None, surface=None,
                 cloud=None, convection=None, lapse=None, upwelling=None,
                 outfile=None, experiment='', timestep=1, delta=0.01,
                 writeevery=1, max_iterations=5000):
        """Set-up a radiative-convective model.

        Parameters:
            atmosphere (Atmosphere): `konrad.atmosphere.Atmosphere`.
            radiation (konrad.radiation): Radiation model.
                Defaults to RRTMG
            humidity (konrad.humidity): Humidity model.
                Defaults to ``konrad.humidity.FixedRH``.
            surface (konrad.surface): Surface model.
                Defaults to ``konrad.surface.SurfaceHeatCapacity``.
            cloud (konrad.cloud): Cloud model.
                Defaults to ``konrad.cloud.ClearSky``.
            convection (konrad.humidity.Convection): Convection scheme.
                Defaults to ``konrad.convection.HardAdjustment``.
            lapse (konrad.lapse.LapseRate): Lapse rate handler.
                Defaults to ``konrad.lapserate.MoistLapseRate``.
            upwelling (konrad.upwelling.Upwelling):
                TODO(sally): Please fill in doc.
            outfile (str): netCDF4 file to store output.
            experiment (str): Experiment description (stored in netCDF).
            timestep (float): Iteration time step in days.
            delta (float): Stop criterion. If the heating rate is below this
                threshold for all levels, skip further iterations.
            writeevery(int or float): Set frequency in which to write output.
                int: Every nth timestep is written.
                float: Every nth day is written.
            max_iterations (int): Maximum number of iterations.
        """
        # Sub-models.
        self.atmosphere = atmosphere
        if radiation is None:
            self.radiation = RRTMG()
        else:
            self.radiation = radiation

        self.humidity = utils.return_if_type(humidity, 'humidity',
                                             Humidity, FixedRH())
        self.surface = utils.return_if_type(surface, 'surface',
                                            Surface, SurfaceHeatCapacity())
        self.cloud = utils.return_if_type(cloud, 'cloud',
                                          Cloud, ClearSky())
        self.convection = utils.return_if_type(convection, 'convection',
                                          Convection, HardAdjustment())

        self.lapse = utils.return_if_type(lapse, 'lapse',
                                     LapseRate, MoistLapseRate())

        self.upwelling = utils.return_if_type(upwelling, 'upwelling',
                                         Upwelling, NoUpwelling())

        # Control parameters.
        self.delta = delta
        self.timestep = timestep
        self.writeevery = writeevery
        self.max_iterations = max_iterations

        # TODO: Maybe delete? One could use the return value of the radiation
        # model directly.
        self.heatingrates = None

        # Internal variables.
        self.converged = False
        self.niter = 0

        self.outfile = outfile
        self.experiment = experiment

        logging.info('Created Konrad object:\n{}'.format(self))

    def __repr__(self):
        retstr = '{}(\n'.format(self.__class__.__name__)
        # Loop over all public object attributes.
        for a in filter(lambda k: not k.startswith('_'), self.__dict__):
            retstr += '    {}={},\n'.format(a, getattr(self, a))
        retstr += ')'

        return retstr

    def get_hours_passed(self):
        """Return the number of house passed since model start.

        Returns:
            float: Hours passed since model start.
        """
        return self.niter * 24 * self.timestep

    def is_converged(self):
        """Check if the atmosphere is in radiative-convective equilibrium.

        Returns:
            bool: ``True`` if converged, else ``False``.
        """
        #TODO: Implement proper convergence criterion (e.g. include TOA).
        return np.all(np.abs(self.atmosphere['deltaT']) < self.delta)

    def check_if_write(self):
        """Check if current timestep should be appended to output netCDF.

        Do not write, if no output file is specified.

        Returns:
            bool: True, if timestep should be written.
        """
        if self.outfile is None:
            return False

        if isinstance(self.writeevery, int):
            return self.niter % self.writeevery == 0
        elif isinstance(self.writeevery, float):
            # Add `0.5 * dt` to current timestep to make float comparison more
            # robust. Otherwise `3.3 % 3 < 0.3` is True.
            r = (((self.niter + 0.5) * self.timestep) % self.writeevery)
            return r < self.timestep
        else:
            raise TypeError('Only except input of type `float` or `int`.')

    # TODO: Consider implementing netCDF writing in a cleaner way. Currently
    # variables from different Datasets are hard to distinguish. Maybe
    # dive into the group mechanism in netCDF.
    def create_outfile(self):
        """Create netCDF4 file to store simulation results."""
        data = self.atmosphere.merge(self.heatingrates, overwrite_vars='H2O')
        data.merge(self.surface, inplace=True)

        # Add experiment and date information to newly created netCDF file.
        data.attrs.update(experiment=self.experiment)
        data.attrs.update(date=datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Not all Radiation classes provide an `solar_constant` attribute.
        # For thos who do (e.g. `RRTMG`) store the value in the netCDF file.
        if hasattr(self.radiation, 'solar_constant'):
            data.attrs.update(solar_constant=self.radiation.solar_constant)

        # The `Atmosphere.to_netcdf()` function is overloaded and able to
        # handle attributes in a proper way (saving the object's class name).
        data.to_netcdf(self.outfile, mode='w', unlimited_dims=['time'])

        logger.info(f'Created "{self.outfile}".')

    def append_to_netcdf(self):
        """Append the current atmospheric state to the netCDF4 file specified
        in ``self.outfile``.
        """
        data = self.atmosphere.merge(self.heatingrates, overwrite_vars='H2O')
        data.merge(self.surface, inplace=True)

        utils.append_timestep_netcdf(
            filename=self.outfile,
            data=data,
            timestamp=self.get_hours_passed(),
            )

    def run(self):
        """Run the radiative-convective equilibrium model."""
        logger.info('Start RCE model run.')

        # Initialize surface pressure to be equal to lowest half-level
        # pressure. This is consistent with handling in PSrad.
        self.surface['pressure'] = self.atmosphere['phlev'][0]

        # Main loop to control all model iterations until maximum number is
        # reached or a given stop criterion is fulfilled.
        while self.niter < self.max_iterations:
            if self.niter % 100 == 0:
                # Write every 100th time step in loglevel INFO.
                logger.info(f'Enter iteration {self.niter}.')
            else:
                # All other iterations are only logged in DEBUG level.
                logger.debug(f'Enter iteration {self.niter}.')

            self.radiation.adjust_solar_angle(self.get_hours_passed() / 24)
            self.heatingrates = self.radiation.get_heatingrates(
                atmosphere=self.atmosphere,
                surface=self.surface,
                cloud=self.cloud,
            )

            # Apply heatingrates/fluxes to the the surface.
            self.surface.adjust(
                sw_down=self.heatingrates['sw_flxd'].values[0, 0],
                sw_up=self.heatingrates['sw_flxu'].values[0, 0],
                lw_down=self.heatingrates['lw_flxd'].values[0, 0],
                lw_up=self.heatingrates['lw_flxu'].values[0, 0],
                timestep=self.timestep,
            )

            # Save the old temperature profile. They are compared with
            # adjusted values to check if the model has converged.
            T = self.atmosphere['T'].values.copy()

            # Caculate critical lapse rate.
            lapse = self.lapse.get(self.atmosphere)

            # Apply heatingrates to temperature profile.
            self.atmosphere['T'] += (self.heatingrates['net_htngrt'] *
                                     self.timestep)

            # Convective adjustment
            self.convection.stabilize(
                atmosphere=self.atmosphere,
                lapse=lapse,
                timestep=self.timestep,
                surface=self.surface,
            )

            # Upwelling induced cooling
            self.upwelling.cool(
                atmosphere=self.atmosphere,
                radheat=self.heatingrates['net_htngrt'][0, :],
                timestep=self.timestep,
            )

            # Calculate the geopotential height field.
            self.atmosphere.calculate_height()

            # Update the humidity profile.
            self.atmosphere['H2O'][0, :] = self.humidity.get(
                    self.atmosphere,
                    surface=self.surface,
                    net_heatingrate=self.heatingrates['net_htngrt'][0, :],
                    )

            # Calculate temperature change for convergence check.
            self.atmosphere['deltaT'] = self.atmosphere['T'] - T

            # Check, if the current iteration is scheduled to be written.
            if self.check_if_write():
                # If we are in the first iteration, a new is created...
                if self.niter == 0:
                    self.create_outfile()
                # ... otherwise we just append.
                else:
                    self.append_to_netcdf()

            # Check if the model run has converged to an equilibrium state.
            if self.is_converged():
                # If the model is converged, skip further iterations. Success!
                logger.info(f'Converged after {self.niter} iterations.')
                break
            # Otherweise increase the iteration count and go on.
            else:
                self.niter += 1
        else:
            logger.info('Stopped after maximum number of iterations.')
