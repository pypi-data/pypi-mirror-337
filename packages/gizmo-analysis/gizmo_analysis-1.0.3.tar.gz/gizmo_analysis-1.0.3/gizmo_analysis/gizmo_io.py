'''
Read Gizmo snapshots, intended for use with FIRE simulations.

@author:
    Andrew Wetzel <arwetzel@gmail.com>
    Shea Garrison-Kimmel <sheagk@gmail.com>
    Andrew Emerick <aemerick11@gmail.com>

----------
Units

Unless otherwise noted, this package stores all quantities in (combinations of) these base units
    mass [M_sun]
    position [kpc comoving]
    distance, radius [kpc physical]
    time [Gyr]
    temperature [K]
    magnetic field [Gauss]
    elemental abundance [linear mass fraction]

These are the common exceptions to those standards
    velocity [km/s]
    acceleration [km/s / Gyr]
    gravitational potential [km^2 / s^2]
    rates (star formation, cooling, accretion) [M_sun / yr]
    metallicity (if converted from stored massfraction)
        [log10(mass_fraction / mass_fraction_solar)], using Asplund et al 2009 for Solar

----------
Reading a snapshot

Within a simulation directory, read all particles in a snapshot at redshift 0 via:
    part = gizmo.io.Read.read_snapshots('all', 'redshift', 0)
part is a dictionary, with a key for each particle species. So, access star particle dictionary via:
    part['star']
part['star'] is dictionary, with each property of particles as a key. For example:
    part['star']['mass']
returns a numpy array of masses, one for each star particle, while
    part['star']['position']
returns a numpy array of positions, of dimension particle_number x 3.

If you want the code to compute and store the principal axes ratios and rotation tensor,
computed via the moment of inertia tensor of the tellar distribution (disk) of each host galaxy:
    part = gizmo.io.Read.read_snapshots('all', 'redshift', 0, assign_hosts_rotation=True)

----------
Particle species

The available particle species in a cosmological simulation are:
    part['dark'] : dark matter at the highest resolution
    part['dark2'] : dark matter at lower resolution (outside of the zoom-in region)
    part['gas'] : gas
    part['star'] : stars
    part['blackhole'] : black holes (if the simulation contains them)

----------
Default/stored particle properties

Access these via:
    part[species_name][property_name]
For example:
    part['star']['position']

All particle species have the following properties:
    'id' : ID (indexing starts at 0)
    'position' : 3-D position, along simulations's (arbitrary) x,y,z grid [kpc comoving]
    'velocity' : 3-D velocity, along simulations's (arbitrary) x,y,z grid [km/s physical/peculiar]
    'acceleration' : 3-D acceleration, along simulations's (arbitrary) x,y,z grid [km/s / Gyr]
    'mass' : mass [M_sun]
    'potential' : gravitational potential (computed via all particles in the box) [km^2 / s^2]

Star particles and gas cells have two additional IDs
(because a gas cell splits if it gets too massive, and a star particle inherits these IDs):
    'id.child' : child ID
    'id.generation' : generation ID
Gizmo initializes id.child and id.generation to 0 for all gas cells.
Each time a gas cell splits into two, one cell retains the same id.child,
the other cell gets: id.child += 2 ^ id.generation.
Both cells then get id.generation += 1.
Because Gizmo stores id.child as a 32-bit int, this allows for a maximum of 30 generations,
then id.child aliases back to 0.
Thus, a particle with id.generation > 30 may not have a uniqe id.child.

Star particle and gas cells also have:
    'massfraction' : fraction of the mass that is in different elemental abundances,
        stored as an array for each particle, with indexes as follows:
        0 = all metals (everything not H, He)
        1 = He, 2 = C, 3 = N, 4 = O, 5 = Ne, 6 = Mg, 7 = Si, 8 = S, 9 = Ca, 10 = Fe

Star particles also have:
  'form.scalefactor' : expansion scale-factor when the star particle formed [0 to 1]

Gas cells also have:
    'temperature' : [K]
    'density' : [M_sun / kpc^3]
    'size' : kernel (smoothing) length [kpc physical]
    'electron.fraction' : average number of free electrons per proton (per hydrogen nucleon)
    'hydrogen.neutral.fraction' : fraction of hydrogen that is neutral (not ionized)
    'sfr' : instantaneous star formation rate [M_sun / yr]
    'magnetic.field' : 3-D vector of magnetic field [Gauss]

----------
Derived properties

part is a ParticleDictionaryClass that can compute derived properties on the fly.
Call derived (or stored) properties via:
    part[species_name].prop(property_name)
For example:
    part['star'].prop('metallicity.fe')
You also can call stored properties via part[species_name].prop(property_name).
It will know that it is a stored property and return as is.
For example, part['star'].prop('position') is the same as part['star']['position'].

See ParticleDictionaryClass.prop() for full options for parsing of derived properties.
Some useful examples:

    part[species_name].prop('host.distance') :
        3-D distance from primary galaxy center along simulation's (arbitrary) x,y,z [kpc physical]
    part[species_name].prop('host.distance.total') : total (scalar) distance [kpc physical]
    part[species_name].prop('host.distance.principal') :
        3-D distance aligned with the galaxy principal (major, intermed, minor) axes [kpc physial]
    part[species_name].prop('host.distance.principal.cylindrical') :
        same, but in cylindrical coordinates [kpc physical]:
            along the major axes R (positive definite)
            azimuthal angle phi (0 to 2 * pi)
            vertical height wrt the disk Z (signed)

    part[species_name].prop('host.velocity') :
        3-D velocity wrt primary galaxy center along simulation's (arbitrary) x,y,z axes [km/s]
    part[species_name].prop('host.velocity.total') : total (scalar) velocity [km/s]
    part[species_name].prop('host.velocity.principal') :
        3-D velocity aligned with the galaxy principal (major, intermed, minor) axes [km/s]
    part[species_name].prop('host.velocity.principal.cylindrical') :
        same, but in cylindrical coordinates [km/s]:
            along the major axes v_R (signed)
            along the azimuth v_phi (signed)
            along the vertical wrt the disk v_Z (signed)

    part['star'].prop('form.time') : time of the Universe when star particle formed [Gyr]
    part['star'].prop('age') :
        age of star particle at current snapshot (current_time - formation_time) [Gyr]

    part['star'].prop('form.mass') : mass of star particle when it formed [M_sun]
    part['star'].prop('mass.loss') : mass loss since formation of star particle [M_sun]

    part['gas'].prop('number.density') :
        gas number density [hydrogen atoms / cm^3]

    part['gas' or 'star'].prop('metallicity.iron') :
        iron abundance [Fe/H] :=
            log10((mass_iron / mass_hydrogen)_particle / (mass_iron / mass_hydrogen)_sun)
        as scaled to Solar (Asplund et al 2009)
        this works for all abundances: 'metallicity.carbon', 'metallicity.magnesium', etc
    part['gas' or 'star'].prop('metallicity.magnesium - metallicity.iron') : [Mg/Fe]
        also can compute arithmetic combinations

    part['gas' or 'star'].prop('mass.hydrogen') : total hydrogen mass in particle [M_sun]
    part['gas' or 'star'].prop('mass.oxygen') : total oxygen mass in particle [M_sun]
    etc
'''

import os
import collections
import h5py
import numpy as np

import utilities as ut
from . import gizmo_default
from . import gizmo_track

# default FIRE model for stellar evolution to assume throughout
FIRE_MODEL_DEFAULT = 'fire2'


# --------------------------------------------------------------------------------------------------
# particle dictionary class
# --------------------------------------------------------------------------------------------------
class ParticleDictionaryClass(dict):
    '''
    Dictionary class to store particle data.
    This functions like a normal dictionary in terms of storing default properties of particles,
    but it also allows greater flexibility for storing meta-data (such as snapshot
    information and cosmological parameters) and for calling derived properties via .prop().
    '''

    def __init__(self):
        # internal dictionary, to translate element name to index in particle element array
        self._element_index = collections.OrderedDict()
        self._element_index['metals'] = 0
        self._element_index['helium'] = self._element_index['he'] = 1
        self._element_index['carbon'] = self._element_index['c'] = 2
        self._element_index['nitrogen'] = self._element_index['n'] = 3
        self._element_index['oxygen'] = self._element_index['o'] = 4
        self._element_index['neon'] = self._element_index['ne'] = 5
        self._element_index['magnesium'] = self._element_index['mg'] = 6
        self._element_index['silicon'] = self._element_index['si'] = 7
        self._element_index['sulfur'] = self._element_index['s'] = 8
        self._element_index['calcium'] = self._element_index['ca'] = 9
        self._element_index['iron'] = self._element_index['fe'] = 10
        # r-process 'toy' models
        self._element_index['rprocess1'] = 11
        self._element_index['rprocess2'] = 12
        self._element_index['rprocess3'] = 13
        self._element_index['rprocess4'] = 14

        self.info = {}  # meta-data about simulation and particle catalog
        self.snapshot = {}  # information about current snapshot
        self.Snapshot = None  # information about all snapshots
        self.Cosmology = None  # information about cosmology and cosmological functions
        # properties of host galaxy/halo[s]
        self.host = {
            'position': [],
            'velocity': [],
            'acceleration': [],
            'rotation': [],
            'axis.ratios': [],
        }

        # for gas
        # adiabatic index (ratio of secific heats) to convert specific intern energy to temperature
        self.adiabatic_index = None

        # for stars and gas
        self.MassLoss = None  # relevant for stars
        self.ElementTracer = None  # relevant for stars and gas
        # use to convert id and id.child to pointer indices and species
        self._id0_to_index = None  # array of pointer indices for particles with id.child = 0
        self._id0_to_species = None  # array of pointer species for particles with id.child = 0
        self._ids_to_index = None  # dict of pointer indices for particles with id.child > 0
        self._ids_to_species = None  # dict of pointer species for particles with id.child > 0

    def prop(self, property_name, indices=None, _dict_only=False):
        '''
        Get property, either stored in self's dictionary or derive it from stored properties.
        Can compute basic mathematical manipulations/combinations, for example:
            'log temperature', 'temperature / density', 'abs position'

        Parameters
        ----------
        property_name : str
            name of property
        indices : array
            indices of particles to get properties of
        _dict_only : bool
            require property_name to be in self's dict - avoids endless recursion
            primarily for internal/recursive usage of this function

        Returns
        -------
        values : float or array
            depending on dimensionality of input indices
        '''
        # parsing general to all catalogs ----------
        property_name = property_name.strip()  # strip white space

        # if input is in self dictionary, return as is
        if property_name in self:
            if indices is not None:
                return self[property_name][indices]
            else:
                return self[property_name]
        elif _dict_only:
            raise KeyError(f'property = {property_name} is not in self\'s dictionary')

        # math relation, combining more than one property
        if (
            '/' in property_name
            or '*' in property_name
            or '+' in property_name
            or '-' in property_name
        ):
            prop_names = property_name

            for delimiter in ['/', '*', '+', '-']:
                if delimiter in property_name:
                    prop_names = prop_names.split(delimiter)
                    break

            if len(prop_names) == 1:
                raise KeyError(f'not sure how to parse property = {property_name}')

            # make copy so not change values in input catalog
            prop_values = np.array(self.prop(prop_names[0], indices))

            for prop_name in prop_names[1:]:
                if '/' in property_name:
                    if np.isscalar(prop_values):
                        if self.prop(prop_name, indices) == 0:
                            prop_values = np.nan
                        else:
                            prop_values = prop_values / self.prop(prop_name, indices)
                    else:
                        masks = self.prop(prop_name, indices) != 0
                        prop_values[masks] = (
                            prop_values[masks] / self.prop(prop_name, indices)[masks]
                        )
                        masks = self.prop(prop_name, indices) == 0
                        prop_values[masks] = np.nan
                if '*' in property_name:
                    prop_values = prop_values * self.prop(prop_name, indices)
                if '+' in property_name:
                    prop_values = prop_values + self.prop(prop_name, indices)
                if '-' in property_name:
                    prop_values = prop_values - self.prop(prop_name, indices)

            if prop_values.size == 1:
                prop_values = np.float64(prop_values)

            return prop_values

        # math transformation of single property
        if property_name[:3] == 'log':
            return ut.math.get_log(self.prop(property_name.replace('log', ''), indices))

        if property_name[:3] == 'abs':
            return np.abs(self.prop(property_name.replace('abs', ''), indices))

        # parsing specific to this catalog ----------
        # stellar mass loss
        if ('mass' in property_name and 'form' in property_name) or 'mass.loss' in property_name:
            if (
                'fire.model' in self.info
                and isinstance(self.info['fire.model'], str)
                and len(self.info['fire.model']) > 0
            ):
                fire_model = self.info['fire.model']
            else:
                fire_model = FIRE_MODEL_DEFAULT

            if 'MassLoss' not in self.__dict__ or self.MassLoss is None:
                from . import gizmo_star

                # create class to compute/store stellar mass loss as a function of age, metallicity
                self.MassLoss = gizmo_star.MassLossClass(model=fire_model)

            # fractional mass loss since formation
            if 'fire2' in fire_model:
                metal_mass_fractions = self.prop('massfraction.metals', indices)
            elif 'fire3' in fire_model:
                metal_mass_fractions = self.prop('massfraction.iron', indices)
            values = self.MassLoss.get_mass_loss_from_spline(
                self.prop('age', indices) * 1000,
                metal_mass_fractions=metal_mass_fractions,
            )

            if 'mass.loss' in property_name:
                if 'fraction' in property_name:
                    pass
                else:
                    values *= self.prop('mass', indices, _dict_only=True) / (
                        1 - values
                    )  # mass loss
            elif 'mass' in property_name and 'form' in property_name:
                values = self.prop('mass', indices, _dict_only=True) / (
                    1 - values
                )  # formation mass

            return values

        # mass of single element
        if 'mass.' in property_name:
            # mass from individual element
            values = self.prop('mass', indices, _dict_only=True) * self.prop(
                property_name.replace('mass.', 'massfraction.'), indices
            )

            if property_name == 'mass.hydrogen.neutral':
                # mass from neutral hydrogen (excluding helium, metals, and ionized hydrogen)
                values = values * self.prop('hydrogen.neutral.fraction', indices, _dict_only=True)

            elif property_name == 'mass.hydrogen.ionized':
                # mass from neutral hydrogen (excluding helium, metals, and ionized hydrogen)
                values = values * (
                    1 - self.prop('hydrogen.neutral.fraction', indices, _dict_only=True)
                )

            return values

        # elemental abundance
        if 'massfraction' in property_name or 'metallicity' in property_name:
            return self._get_abundances(property_name, indices)

        if 'number.density' in property_name:
            values = (
                self.prop('density', indices, _dict_only=True)
                * ut.constant.proton_per_sun
                * ut.constant.kpc_per_cm**3
            )

            if 'hydrogen' in property_name:
                # number density of hydrogen, using actual hydrogen mass of each particle [cm ^ -3]
                values = values * self.prop('massfraction.hydrogen', indices)
            else:
                # number density of 'hydrogen', assuming solar metallicity for particles [cm ^ -3]
                values = values * ut.constant.sun_massfraction['hydrogen']

            return values

        if 'size' in property_name:
            # default size := inter-particle spacing = (mass / density)^(1/3) [kpc]
            f = (np.pi / 3) ** (1 / 3) / 2  # 0.5077, converts from default size to full extent

            if 'size' in self:
                values = self.prop('size', indices, _dict_only=True)
            else:
                values = (
                    self.prop('mass', indices, _dict_only=True)
                    / self.prop('density', indices, _dict_only=True)
                ) ** (1 / 3)

            if 'plummer' in property_name:
                # convert to plummer equivalent
                values = values / f / 2.8
            elif 'max' in property_name:
                # convert to maximum extent of kernel (radius of compact support)
                values = values / f

            if '.pc' in property_name:
                # convert to [pc]
                values = values * 1000

            return values

        if 'volume' in property_name:
            # volume := mass / density [kpc^3]
            if 'size' in self:
                return self.prop('size', indices, _dict_only=True) ** 3
            else:
                return self.prop('mass', indices, _dict_only=True) / self.prop(
                    'density', indices, _dict_only=True
                )

            if '.pc' in property_name:
                # convert to [pc^3]
                values = values * 1e9

        # free-fall time of gas cell := (3 pi / (32 G rho)) ^ 0.5
        if 'time.freefall' in property_name:
            values = self.prop('density', indices, _dict_only=True)  # [M_sun / kpc ^ 3]
            values = (3 * np.pi / (32 * ut.constant.grav_kpc_msun_Gyr * values)) ** 0.5  # [Gyr]

            return values

        # hydrogen ionized fraction
        if property_name == 'hydrogen.ionized.fraction':
            return 1 - self.prop('hydrogen.neutral.fraction', indices, _dict_only=True)

        if 'magnetic' in property_name and (
            'energy' in property_name or 'pressure' in property_name
        ):
            # magnetic field: energy density = pressure = B^2 / (8 pi)
            # convert from stored [Gauss] to [erg / cm^3]
            values = self.prop('magnetic.field', indices, _dict_only=True)
            values = np.sum(values**2, 1) / (8 * np.pi)

            if 'energy' in property_name and 'density' not in property_name:
                # total energy in magnetic field [erg]
                values = values * self.prop('volume', indices) * ut.constant.cm_per_kpc**3

            return values

        if 'cosmicray.energy.density' in property_name:
            # energy density in cosmic rays [M_sun / kpc / Gyr^2]
            return self.prop('cosmicray.energy', indices, _dict_only=True) / (
                self.prop('volume', indices)
            )

        if 'photon.energy.density' in property_name:
            return self.prop('cosmicray.energy', indices, _dict_only=True) / (
                self.prop('volume', indices)
            )

        # mean molecular mass [g] or mass ratio [dimensionless]
        if 'molecular.mass' in property_name:
            helium_mass_fracs = self.prop('massfraction.helium', indices)
            ys_helium = helium_mass_fracs / (4 * (1 - helium_mass_fracs))
            molecular_mass_ratios = (1 + 4 * ys_helium) / (
                1 + ys_helium + self.prop('electron.fraction', indices, _dict_only=True)
            )
            values = molecular_mass_ratios

            if property_name == 'molecular.mass.ratio':
                pass
            elif property_name == 'molecular.mass':
                values *= ut.constant.proton_mass

            return values

        # internal energy of gas [cm^2 / s^2] - undo conversion to temperature
        if 'internal.energy' in property_name:
            molecular_masses = self.prop('molecular.mass', indices, _dict_only=True)

            values = self.prop('temperature') / (
                ut.constant.centi_per_kilo**2
                * (self.adiabatic_index - 1)
                * molecular_masses
                / ut.constant.boltzmann
            )

            return values

        # sound speed [km/s], for simulations that do not store it
        if 'sound.speed' in property_name:
            values = (
                np.sqrt(
                    self.adiabatic_index
                    * ut.constant.boltzmann
                    * self.prop('temperature', indices, _dict_only=True)
                    / ut.constant.proton_mass
                )
                * ut.constant.kilo_per_centi
            )

            return values

        # formation time [Gyr] or coordinates
        if (
            ('form.' in property_name or property_name == 'age')
            and 'host' not in property_name
            and 'distance' not in property_name
            and 'velocity' not in property_name
        ):
            if property_name == 'age' or ('time' in property_name and 'lookback' in property_name):
                # look-back time (stellar age) to formation
                values = self.snapshot['time'] - self.prop('form.time', indices)
            elif 'time' in property_name:
                # time (age of universe) of formation
                values = self.Cosmology.get_time(
                    self.prop('form.scalefactor', indices, _dict_only=True), 'scalefactor'
                )
            elif 'redshift' in property_name:
                # redshift of formation
                values = 1 / self.prop('form.scalefactor', indices, _dict_only=True) - 1
            elif 'snapshot' in property_name:
                # snapshot index immediately after formation
                # increase formation scale-factor slightly for safety, because scale-factors of
                # written snapshots do not exactly coincide with input scale-factors
                padding_factor = 1 + 1e-7
                values = self.Snapshot.get_snapshot_indices(
                    'scalefactor',
                    np.clip(
                        self.prop('form.scalefactor', indices, _dict_only=True) * padding_factor,
                        0,
                        1,
                    ),
                    round_kind='up',
                )

            return values

        # distance or velocity wrt the host galaxy/halo
        if 'host' in property_name and (
            'distance' in property_name
            or 'velocity' in property_name
            or 'acceleration' in property_name
        ):
            if 'host.' in property_name or 'host1.' in property_name:
                host_name = 'host.'
                host_index = 0
            elif 'host2.' in property_name:
                host_name = 'host2.'
                host_index = 1
            elif 'host3.' in property_name:
                host_name = 'host3.'
                host_index = 2
            else:
                raise ValueError(f'cannot identify host name in {property_name}')

            if 'form.' in property_name:
                # special case: coordinates wrt primary host *at formation*
                if 'distance' in property_name:
                    # 3-D distance vector wrt primary host at formation
                    values = self.prop('form.' + host_name + 'distance', indices, _dict_only=True)
                elif 'velocity' in property_name:
                    # 3-D velocity vectory wrt host at formation
                    values = self.prop('form.' + host_name + 'velocity', indices, _dict_only=True)
            else:
                # general case: coordinates wrt primary host at current snapshot
                if 'distance' in property_name:
                    # 3-D distance vector wrt the primary host
                    values = ut.coordinate.get_distances(
                        self.prop('position', indices, _dict_only=True),
                        self.host['position'][host_index],
                        self.info['box.length'],
                        self.snapshot['scalefactor'],
                    )  # [kpc physical]
                elif 'velocity' in property_name:
                    # 3-D velocity vector wrt the primary host, adding the Hubble flow
                    values = ut.coordinate.get_velocity_differences(
                        self.prop('velocity', indices, _dict_only=True),
                        self.host['velocity'][host_index],
                        self.prop('position', indices, _dict_only=True),
                        self.host['position'][host_index],
                        self.info['box.length'],
                        self.snapshot['scalefactor'],
                        self.snapshot['time.hubble'],
                    )
                elif 'acceleration' in property_name:
                    # 3-D acceleration
                    # no correction for Hubble flow
                    values = self.prop('acceleration', indices, _dict_only=True)
                    if 'acceleration' in self.host and len(self.host['acceleration']) > 0:
                        values -= self.host['acceleration']

                if 'principal' in property_name:
                    # align with host principal axes
                    assert (
                        len(self.host['rotation']) > 0
                    ), 'must assign hosts principal axes rotation tensor!'
                    values = ut.coordinate.get_coordinates_rotated(
                        values, self.host['rotation'][host_index]
                    )

            if '.cyl' in property_name or '.spher' in property_name:
                # convert to cylindrical or spherical coordinates
                if '.cyl' in property_name:
                    coordinate_system = 'cylindrical'
                elif '.spher' in property_name:
                    coordinate_system = 'spherical'

                if 'distance' in property_name:
                    values = ut.coordinate.get_positions_in_coordinate_system(
                        values, 'cartesian', coordinate_system
                    )
                elif 'velocity' in property_name or 'acceleration' in property_name:
                    if 'form.' in property_name:
                        # special case: coordinates wrt primary host *at formation*
                        distance_vectors = self.prop(
                            'form.' + host_name + 'distance', indices, _dict_only=True
                        )
                    elif 'principal' in property_name:
                        distance_vectors = self.prop(host_name + 'distance.principal', indices)
                    else:
                        distance_vectors = self.prop(host_name + 'distance', indices)
                    values = ut.coordinate.get_velocities_in_coordinate_system(
                        values, distance_vectors, 'cartesian', coordinate_system
                    )

                if '.rad' in property_name:
                    values = values[:, 0]
                elif '.azi' in property_name:
                    values = values[:, 1]
                elif '.ver' in property_name:
                    values = values[:, 2]

            # compute total (scalar) of distance
            if '.total' in property_name:
                if len(values.shape) == 1:
                    shape_pos = 0
                else:
                    shape_pos = 1
                values = np.sqrt(np.sum(values**2, shape_pos))

            return values

        # compute total (scalar) value from 3-D for some other property
        # such as velocity, acceleration, magnetic field
        if '.total' in property_name:
            prop_name = property_name.replace('.total', '')
            try:
                values = self.prop(prop_name, indices)
                values = np.sqrt(np.sum(values**2, 1))
                return values
            except ValueError:
                pass

        # should not get this far without a return
        raise KeyError(f'not sure how to parse property = {property_name}')

    def _get_abundances(self, property_name, indices=None):
        '''
        Get element mass fraction[s] or metallicity[s], either stored in dictionary or via
        post-processing stored element-tracer mass weights.

        Parameters
        ----------
        property_name : str
            name of property to get
        indices : array [optional]
            indices of particles to get property of

        Returns
        -------
        values : float or array
            mass fraction[s] or metallicity[s]
        '''
        # special case: total alpha-element abundance - compute and return as a metallicity
        if 'alpha' in property_name:
            assert 'metallicity' in property_name
            alpha_elements = ['oxygen', 'magnesium', 'silicon', 'calcium']
            metallicity_name = 'metallicity.'
            if 'elementtracer' in property_name:
                metallicity_name += 'elementtracer.'
            metallicities = [self.prop(metallicity_name + a, indices) for a in alpha_elements]

            return np.mean(metallicities, 0)

        # special case: hydrogen (exclude helium and metals)
        elif 'hydrogen' in property_name or property_name.endswith('.h'):
            element_name = 'hydrogen'
            massfraction_name = 'massfraction.'
            if 'elementtracer' in property_name:
                massfraction_name += 'elementtracer.'
            values = (
                1
                - self.prop(massfraction_name + 'metals', indices)
                - self.prop(massfraction_name + 'helium', indices)
            )

            if 'neutral' in property_name:
                # mass fraction of neutral hydrogen (excluding Helium, metals, and ionized H)
                values = values * self.prop('hydrogen.neutral.fraction', indices, _dict_only=True)

        # normal case
        elif 'elementtracer' not in property_name:
            for element_name in property_name.split('.'):
                if element_name in self._element_index:
                    element_index = self._element_index[element_name]
                    break
            else:
                raise KeyError(f'not sure how to parse property = {property_name}')

            if indices is None:
                values = self['massfraction'][:, element_index]
            else:
                values = self['massfraction'][indices, element_index]

        # compute elemental abundances using element-tracer weights
        elif 'elementtracer' in property_name:
            assert 'ElementTracer' in self.__dict__ and self.ElementTracer is not None
            # pylint: disable=unsubscriptable-object
            assert len(self.ElementTracer['yield.massfractions']) > 0

            for element_name in property_name.split('.'):
                if element_name in ut.constant.element_name_from_symbol:
                    element_name = ut.constant.element_name_from_symbol[element_name]
                if element_name in self.ElementTracer['yield.massfractions']:
                    break  # found a match
            else:
                raise KeyError(
                    f'not sure how to parse element = {property_name}.'
                    + ' element element-tracer dictionary has these elements available:  {}'.format(
                        self.ElementTracer['yield.massfractions'].keys()
                    )
                )

            # get element-tracer weights for each particle
            # slice particle's element mass fraction array on first index for element-tracer weights
            elementtracer_index_start = self.ElementTracer['element.index.start']
            if indices is None:
                elementtracer_mass_weights = self['massfraction'][:, elementtracer_index_start:]
                _metal_massfractions = self['massfraction'][:, 0]
            else:
                elementtracer_mass_weights = self['massfraction'][
                    indices, elementtracer_index_start:
                ]
                _metal_massfractions = self['massfraction'][indices, 0]

            values = self.ElementTracer.get_element_massfractions(
                element_name, elementtracer_mass_weights, _metal_massfractions
            )

        # convert to metallicity := log10(mass_fraction / mass_fraction_solar)
        if 'metallicity' in property_name:
            values = ut.math.get_log(values / ut.constant.sun_massfraction[element_name])

        return values

    def get_pointers_from_ids(self, ids, child_ids):
        '''
        For each input id [and child id], get a pointer to the array index [and species name] of
        the particle in this dictionary catalog.
        If running from within dictionary of single particle species, such as part['star'],
        return only the pointer index for each input id.
        If running from within the meta-dictionary of multiple species, such as part,
        return the pointer index and species name for each input id.
        If input child_ids = False, will ignore child_ids altogether and use just ids, relevant
        for older simulations without child ids.

        Parameters
        ----------
        ids : array
            ids of particles
        child_ids : array
            child ids of particles
            child_ids = False will ignore child ids, for older simulations without child ids

        Returns
        -------
        pindices : array
            for each input id, the array index of the particle in this catalog
        [species : array]
            for each input id, the name of the species of the particle in this catalog
        '''
        if child_ids is not False:
            assert child_ids is not None and len(child_ids) == len(ids), 'need to input id.child'
            ids = np.asarray(ids)
            child_ids = np.asarray(child_ids)

        if 'star' in self and 'gas' in self:
            # running from within meta-dictionary that contains sub-dictionaries for stars and gas

            # initialize array to store species names
            species = np.zeros(ids.size, dtype='<U4')

            # get pointer indices for gas - particles that are stars will return null values
            pindices = self['gas'].get_pointers_from_ids(ids, child_ids)
            indices = np.where(pindices >= 0)[0]
            species[indices] = 'gas'

            # deal with ids that do not have a matched index in gas cell catalog
            # almost all should be stars, modulo any that do not exist at all in this catalog
            indices = np.where(pindices < 0)[0]
            if child_ids is False:
                cids = False
            else:
                cids = child_ids[indices]
            pindices[indices] = self['star'].get_pointers_from_ids(ids[indices], cids)
            # assign species name for ids that matched in the star particle catalog
            indices = indices[np.where(pindices[indices] >= 0)[0]]
            species[indices] = 'star'

            return pindices, species

        else:
            # running from within dictionary of single particle species
            if self._id0_to_index is None:
                self._assign_ids_to_indices()

            # get indices of particle input to assign_ids_to_indices()
            if child_ids is False:
                pindices = self._id0_to_index[ids]
            else:
                pindices = ut.array.get_array_null(ids.size)
                # use simple array pointer indices for (the majority of) particles with id.child = 0
                indices = np.where(child_ids == 0)[0]
                pids = ids[indices]
                pindices[indices] = self._id0_to_index[pids]
                # use more complex dict pointer indices for particles with id.child > 0
                indices = np.where(child_ids > 0)[0]
                pids = ids[indices]
                cids = child_ids[indices]
                for index, pid, cid in zip(indices, pids, cids):
                    if (pid, cid) in self._ids_to_index:
                        pindices[index] = self._ids_to_index[(pid, cid)]

            return pindices

    def _assign_ids_to_indices(self):
        '''
        Assign to self an array [and dictionary] to point from a particle's id [and id.child]
        to its array index in this dictionary catalog.
        '''
        id_name = 'id'
        id_child_name = 'id.child'

        # simple case: select only particles that have id.child = 0 (should be vast majority)
        # among this subset, ids are unique, so use simple array of pointer indices
        if id_child_name in self:
            pindices = np.where(self[id_child_name] == 0)[0]
        else:
            pindices = ut.array.get_arange(self[id_name].size)
        ids = self[id_name][pindices]
        # multiplier for combining stars + gas, to ensure that max id encompasses both catalogs
        id_max = int(1.5 * ids.max())
        self._id0_to_index = ut.array.get_array_null(id_max)
        self._id0_to_index[ids] = pindices

        if id_child_name in self and self[id_child_name].max() > 0:
            # complex case: deal with all particles that have id.child > 0
            # these have non-unique id, so assign dictionary look-up pointer indices
            pindices = np.where(self[id_child_name] > 0)[0]
            pids = self[id_name][pindices]
            cids = self[id_child_name][pindices]
            self._ids_to_index = {}
            for pindex, pid, cid in zip(pindices, pids, cids):
                self._ids_to_index[(pid, cid)] = pindex


# --------------------------------------------------------------------------------------------------
# read
# --------------------------------------------------------------------------------------------------
class ReadClass(ut.io.SayClass):
    '''
    Read Gizmo snapshot[s].
    '''

    def __init__(self, verbose=True):
        '''
        Set properties for snapshot files.

        Parameters
        ----------
        verbose : bool
            whether to print diagnostics during read in
        '''
        # assumed adiabatic index (ratio of specific heats) for gas
        # use only to convert between gas specific internal energy and temperature
        self.gas_adiabatic_index = 5 / 3

        # name base of snapshot files/directories, to use in glob to find all files/directories
        # safely skip files ending in '.txt' or '.ewah'
        self._snapshot_name_base = 'snap*[!.txt!.ewah]'
        self._snapshot_file_extension = '.hdf5'

        # create ordered dictionary to convert particle species name to its id,
        # set all possible species, and set the order in which to read species
        self.species_dict = collections.OrderedDict()
        self.species_dict['dark'] = 1  # dark matter at highest resolution
        self.species_dict['dark2'] = 2  # dark matter at all lower resolutions
        self.species_dict['gas'] = 0
        self.species_dict['star'] = 4
        self.species_dict['blackhole'] = 5

        self._species_all = tuple(self.species_dict.keys())
        self._species_read = list(self._species_all)

        self._verbose = verbose

    def read_snapshots(
        self,
        species='all',
        snapshot_value_kind='redshift',
        snapshot_values=0,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        track_directory=gizmo_default.track_directory,
        simulation_name='',
        properties='all',
        elements=None,
        particle_subsample_factor=None,
        separate_dark_lowres=False,
        sort_dark_by_id=False,
        convert_float32=False,
        host_number=1,
        assign_hosts=True,
        assign_hosts_rotation=False,
        assign_orbits=False,
        assign_formation_coordinates=False,
        assign_pointers=False,
        check_properties=True,
        verbose=None,
    ):
        '''
        Read given properties for given particle species from simulation snapshot file[s].
        Can read single snapshot or multiple snapshots.
        If single snapshot, return as dictionary class;
        if multiple snapshots, return as list of dictionary classes.

        Parameters
        ----------
        species : str or list
            name[s] of particle species:
                'all' = all species in file
                'dark' = dark matter at highest resolution
                'dark2' = dark matter at lower resolution
                'gas' = gas
                'star' = stars
                'blackhole' = black holes, if snapshot contains them
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift', 'scalefactor'
        snapshot_values : int or float or list
            index[s] or redshift[s] or scale-factor[s] of snapshot[s]
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of snapshot files within simulation_directory
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        simulation_name : str
            name to store for future identification
        properties : str or list
            name[s] of particle properties to read. 'all' or None = read all properties in snapshot
        elements : str or list
            name[s] of elemental abundances to read. 'all' or None = read all elements in snapshot
        particle_subsample_factor : int
            factor to periodically subsample particles, to save memory
        separate_dark_lowres : bool
            whether to separate low-resolution dark matter into separate dicts according to mass
        sort_dark_by_id : bool
            whether to sort dark-matter particles by id
        convert_float32 : bool
            whether to convert all floats to 32 bit to save memory
        host_number : int
            number of hosts to assign and compute coordinates relative to
        assign_hosts : bool or str
            whether to assign coordinates of each host.
            if a string, tells the code which method to use:
                'track' : reads host coordinates from track/host_coordinates.hdf5,
                    compiled during particle tracking using only stars in each host at z = 0
                'halo' : reads host halo coordinates from halo/rockstar_dm/catalog_hdf5/
                'mass' or 'potential' or 'massfraction.metals': assign coordinates during read in
                    via iterative zoom-in, weighting each particle by that property
            if True (default), will try a few methods in the following order of preference:
                if a baryonic simulation (or input species_name='star'), try 'track' then 'mass'
                if a DM-only simulations (or input species_name='dark'), try 'halo' then 'mass'
        assign_hosts_rotation : bool
            whether to assign principal axes rotation tensor of each host galaxy
        assign_orbits : bool
            whether to assign orbital properties wrt each host galaxy/halo
        assign_formation_coordinates : bool
            whether to assign to stars their coordindates wrt each host galaxy at formation
        assign_pointers : bool
            whether to assign pointers for tracking particles from z = 0 to this snapshot
        check_properties : bool
            whether to check sanity of particle properties after read in
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose

        Returns
        -------
        parts : dict or list
            if single snapshot, return as dictionary, else if multiple snapshots, return as list
        '''
        if verbose is None:
            verbose = self._verbose

        # parse input species to read
        if species == 'all' or species == ['all'] or not species:
            # read all species in snapshot
            species = self._species_all
        else:
            # read subsample of species in snapshot
            if np.isscalar(species):
                species = [species]  # ensure is list
            # check if input species names are valid
            for spec_name in list(species):
                if spec_name not in self.species_dict:
                    species.remove(spec_name)
                    self.say(f'! not recognize input species = {spec_name}')
        self._species_read = list(species)

        # read information about snapshot times
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = ut.io.get_path(snapshot_directory)

        if assign_hosts:
            # if 'elvis' is in simulation directory name, force 2 hosts
            host_number = ut.catalog.get_host_number_from_directory(
                host_number, simulation_directory, os
            )

        # ensure input number or list/array of numbers
        assert snapshot_values is not None and not isinstance(snapshot_values, str)
        snapshot_values = ut.array.arrayize(snapshot_values)

        Snapshot = ut.simulation.read_snapshot_times(
            simulation_directory, verbose, error_if_no_file=False
        )
        if Snapshot is None:
            # could not read file that lists all snapshots - require input snapshot index
            if snapshot_value_kind != 'index':
                raise OSError(f'cannot find file of snapshot times in {simulation_directory}')

        parts = []  # list to store particle dictionaries

        # read all input snapshots
        for snapshot_value in snapshot_values:
            if Snapshot is None:
                # if could not read list of snapshots, assume input snapshot index
                snapshot_index = snapshot_value
            else:
                snapshot_index = Snapshot.parse_snapshot_values(
                    snapshot_value_kind,
                    snapshot_value,
                    verbose,
                )

            # read header from snapshot file
            header = self.read_header(
                simulation_directory,
                snapshot_directory,
                'index',
                snapshot_index,
                simulation_name,
                verbose=verbose,
            )

            # read particles from snapshot file[s]
            part = self._read_particles(
                simulation_directory,
                snapshot_directory,
                'index',
                snapshot_index,
                properties,
                elements,
                convert_float32,
                header,
                verbose=verbose,
            )

            # assign auxilliary information to particle dictionary class
            # store header dictionary
            part.info = header
            for spec_name in part:
                part[spec_name].info = part.info

            # read/get (additional) cosmological parameters
            if header['cosmological']:
                part.Cosmology = self._get_cosmology(
                    simulation_directory,
                    header['omega_lambda'],
                    header['omega_matter'],
                    header['omega_baryon'],
                    hubble=header['hubble'],
                    verbose=verbose,
                )
                for spec_name in part:
                    part[spec_name].Cosmology = part.Cosmology

            # adjust properties for each species
            self._adjust_particle_properties(
                part,
                header,
                particle_subsample_factor,
                separate_dark_lowres,
                sort_dark_by_id,
                verbose,
            )

            # check sanity of particle properties read in
            if check_properties and verbose:
                self._check_particle_properties(part)

            # store information about snapshot time
            if header['cosmological']:
                time = part.Cosmology.get_time(header['redshift'], 'redshift')
                part.snapshot = {
                    'index': snapshot_index,
                    'redshift': header['redshift'],
                    'scalefactor': header['scalefactor'],
                    'time': time,
                    'time.lookback': part.Cosmology.get_time(0) - time,
                    'time.hubble': (
                        ut.constant.Gyr_per_sec
                        / part.Cosmology.get_hubble_parameter(header['redshift'])
                    ),
                }
            else:
                part.snapshot = {
                    'index': snapshot_index,
                    'redshift': 0,
                    'scalefactor': 1.0,
                    'time': header['time'],
                    'time.lookback': 0,
                    'time.hubble': None,
                }

            for spec_name in part:
                part[spec_name].snapshot = part.snapshot

            # store information on all snapshot times
            part.Snapshot = Snapshot
            for spec_name in part:
                part[spec_name].Snapshot = part.Snapshot

            # store each host's position, velocity, principal axes rotation tensor + axis ratios
            # store as dictionary of lists to accommodate multiple hosts
            # these already were initialized for the overlal particle class, but useful to
            # store in each species dictionary as well
            for spec_name in part:
                part[spec_name].host = {
                    'position': [],
                    'velocity': [],
                    'rotation': [],
                    'axis.ratios': [],
                }

            if assign_hosts:
                self.assign_hosts_coordinates(
                    part,
                    assign_hosts,
                    host_number=host_number,
                    assign_formation_coordinates=assign_formation_coordinates,
                    simulation_directory=simulation_directory,
                    track_directory=track_directory,
                    verbose=verbose,
                )

                # check if already read rotation tensors from particle tracking file
                if assign_hosts_rotation and len(part.host['rotation']) == 0:
                    self.assign_hosts_rotation(part, verbose=verbose)

            if assign_pointers:
                # assign star particle and gas cell pointers from z = 0 to this snapshot
                ParticlePointer = gizmo_track.ParticlePointerClass(
                    simulation_directory=simulation_directory, track_directory=track_directory
                )
                ParticlePointer.io_pointers(part, verbose=verbose)

            # store orbital properties wrt each host galaxy/halo
            if assign_orbits and ('velocity' in properties or properties == 'all'):
                self.assign_particle_orbits(
                    part,
                    'star',
                    part.host['position'],
                    part.host['velocity'],
                    verbose,
                )

            # if read only 1 snapshot, return as particle dictionary instead of list
            if len(snapshot_values) == 1:
                parts = part
            else:
                parts.append(part)
                self.say('', verbose)

        return parts

    def read_snapshots_simulations(
        self,
        species='all',
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_directories=None,
        snapshot_directory=gizmo_default.snapshot_directory,
        track_directory=gizmo_default.track_directory,
        properties='all',
        elements=('metals', 'he', 'mg', 'fe'),
        assign_hosts=True,
        assign_hosts_rotation=False,
        assign_orbits=False,
        assign_formation_coordinates=False,
        assign_pointers=False,
        check_properties=True,
        verbose=None,
    ):
        '''
        Read snapshots at the same redshift from different simulations.
        Return as list of dictionaries.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to read
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift', 'scalefactor'
        snapshot_value : int or float
            index or redshift or scale-factor of snapshot
        simulation_directories : list or dict
            list of simulation directories, or dict of simulation_directories: simulation_names
        snapshot_directory: str
            directory of snapshot files within simulation_directory
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        properties : str or list
            name[s] of particle properties to read. 'all' or None = read all properties in snapshot
        elements : str or list
            name[s] of elemental abundances to read. 'all' or None = read all elements in snapshot
        assign_hosts : bool or str
            whether to assign host coordinates.
            if a string, tells the code which method to use:
                'track' : reads host coordinates from track/host_coordinates.hdf5,
                    compiled during particle tracking using only stars in each host at z = 0
                'halo' : reads host halo coordinates from halo/rockstar_dm/catalog_hdf5/
                'mass' or 'potential' : assign coordinates during read in via iterative zoom-in,
                    weighting each particle by that property
            if True (default), will try a few methods in the following order of preference:
                if a baryonic simulation (or input species_name='star'), try 'track' then 'mass'
                if a DM-only simulations (or input species_name='dark'), try 'halo' then 'mass'
        assign_hosts_rotation : bool
            whether to assign principal axes rotation tensor of each host galaxy/halo
        assign_orbits : bool
            whether to assign orbital properties wrt each host galaxy/halo
        assign_formation_coordinates : bool
            whether to assign to stars their coordindates wrt each host galaxy at formation
        assign_pointers : bool
            whether to assign pointers for tracking particles from z = 0 to this snapshot
        check_properties : bool
            whether to check sanity of particle properties after read in
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose

        Returns
        -------
        parts : list of dictionaries
        '''
        if verbose is None:
            verbose = self._verbose

        # parse list of directories
        if isinstance(simulation_directories, dict):
            pass
        elif isinstance(simulation_directories, list) or isinstance(simulation_directories, tuple):
            if np.ndim(simulation_directories) not in [1, 2]:
                raise ValueError(
                    f'not sure how to parse simulation_directories = {simulation_directories}'
                )
            elif np.ndim(simulation_directories) == 1:
                # assign null names
                simulation_directories = {
                    simulation_directory: '' for simulation_directory in simulation_directories
                }
            elif np.ndim(simulation_directories) == 2:
                simulation_directories = {
                    simulation_directory[0]: simulation_directory[1]
                    for simulation_directory in simulation_directories
                }
        else:
            raise ValueError(
                f'not sure how to parse simulation_directories = {simulation_directories}'
            )

        # first pass, read only header, to check that can read all simulations
        bad_snapshot_value = 0
        for simulation_directory in simulation_directories:
            simulation_name = simulation_directories[simulation_directory]
            try:
                _ = self.read_header(
                    simulation_directory,
                    snapshot_directory,
                    snapshot_value_kind,
                    snapshot_value,
                    simulation_name,
                    verbose=verbose,
                )
            except IOError:
                self.say(
                    '! cannot read snapshot header at {} = {:.3f} in {}'.format(
                        snapshot_value_kind, snapshot_value, simulation_directory
                    )
                )
                bad_snapshot_value += 1

        if bad_snapshot_value:
            self.say(f'\n! cannot read {bad_snapshot_value} snapshots')
            return

        parts = []
        simulation_directories_read = []
        for simulation_directory in simulation_directories:
            simulation_name = simulation_directories[simulation_directory]
            try:
                part = self.read_snapshots(
                    species,
                    snapshot_value_kind,
                    snapshot_value,
                    simulation_directory,
                    snapshot_directory,
                    track_directory,
                    simulation_name,
                    properties,
                    elements,
                    assign_hosts=assign_hosts,
                    assign_hosts_rotation=assign_hosts_rotation,
                    assign_orbits=assign_orbits,
                    assign_formation_coordinates=assign_formation_coordinates,
                    assign_pointers=assign_pointers,
                    check_properties=check_properties,
                    verbose=verbose,
                )
            except IOError:
                self.say(
                    f'! cannot read snapshot {snapshot_value_kind}={snapshot_value} in'
                    + ' {simulation_directory}'
                )
                part = None

            if part is not None:
                if assign_orbits and 'velocity' in properties:
                    self.assign_particle_orbits(part, 'gas', verbose=verbose)

                parts.append(part)
                simulation_directories_read.append(simulation_directory)

        if len(parts) == 0:
            self.say(f'! cannot read any snapshots at {snapshot_value_kind} = {snapshot_value}')
            return

        if 'mass' in properties and 'star' in part:
            for part, simulation_directory in zip(parts, simulation_directories_read):
                self.say(
                    '{}\n* M_star simulation = {} Msun\n'.format(
                        simulation_directory,
                        ut.io.get_string_from_numbers(part['star']['mass'].sum(), 2, True),
                    ),
                    verbose,
                )

        return parts

    def read_header(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_name='',
        snapshot_block_index=0,
        verbose=None,
    ):
        '''
        Read header from snapshot file.

        Parameters
        ----------
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift'
        snapshot_value : int or float
            index (number) of snapshot file
        simulation_directory : str
            directory of simulation
        snapshot_directory: str
            directory of snapshot files within simulation_directory
        simulation_name : str
            name to store for future identification
        snapshot_block_index : int
            index of file block (if multiple files per snapshot)
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose

        Returns
        -------
        header : dictionary class
            header dictionary
        '''
        # convert name in snapshot's header dictionary to custom name
        header_name_dict = {
            'GIZMO_version': 'gizmo.version',
            # 6-element array of number of particles of each type in file
            'NumPart_ThisFile': 'particle.numbers.in.file',
            # 6-element array of total number of particles of each type (across all files)
            'NumPart_Total': 'particle.numbers.total',
            'NumPart_Total_HighWord': 'particle.numbers.total.high.word',
            # number of file blocks per snapshot
            'NumFilesPerSnapshot': 'file.number.per.snapshot',
            # numerical parameters
            'UnitLength_In_CGS': 'unit.length',
            'UnitMass_In_CGS': 'unit.mass',
            'UnitVelocity_In_CGS': 'unit.velocity',
            'Internal_UnitB_In_Gauss': 'unit.magnetic',
            'Effective_Kernel_NeighborNumber': 'kernel.number',
            'Fixed_ForceSoftening_Keplerian_Kernel_Extent': 'kernel.sizes',
            'Kernel_Function_ID': 'kernel.id',
            'TurbDiffusion_Coefficient': 'diffusion.coefficient',
            'Solar_Abundances_Adopted': 'sun.massfractions',
            'Metals_Atomic_Number_Or_Key': 'atomic.numbers',
            # mass of each particle species, if all particles are same
            # (= 0 if they are different, which is usually true)
            'MassTable': 'particle.masses',
            # time
            'Time': 'time',  # [scale-factor or Gyr/h in file]
            'Redshift': 'redshift',
            # cosmology
            'BoxSize': 'box.length',  # [kpc/h comoving in file]
            'Omega0': 'omega_matter',  # old name convention
            'OmegaLambda': 'omega_lambda',  # old name convention
            'Omega_Matter': 'omega_matter',
            'Omega_Baryon': 'omega_baryon',
            'Omega_Lambda': 'omega_lambda',
            'Omega_Radiation': 'omega_radiation',
            'HubbleParam': 'hubble',
            'ComovingIntegrationOn': 'cosmological',
            # physics flags
            'Flag_DoublePrecision': 'has.double.precision',
            'Flag_Sfr': 'has.star.formation',
            'Density_Threshold_For_SF_CodeUnits': 'sf.density.threshold',
            'Flag_Cooling': 'has.cooling',
            'Flag_StellarAge': 'has.star.age',
            'Flag_Feedback': 'has.feedback',
            'Flag_IC_Info': 'initial.condition.kind',
            'Flag_Metals': 'element.number',
            'Flag_AgeTracers': 'has.elementtracer',  # not in newer headers
            # element-tracers to assign elemental abundances in post-processing
            # will have either elementtracer.age.min + elementtracer.age.max
            # or elementtracer.age.bins
            'AgeTracer_NumberOfBins': 'elementtracer.age.bin.number',
            'AgeTracerBinStart': 'elementtracer.age.min',
            'AgeTracerBinEnd': 'elementtracer.age.max',
            'AgeTracer_CustomTimeBins': 'elementtracer.age.bins',  # or this array
            'AgeTracerEventsPerTimeBin': 'elementtracer.event.number.per.age.bin',
            # level of compression of snapshot file
            'CompactLevel': 'compression.level',
            'Compactify_Version': 'compression.version',
            'ReadMe': 'compression.readme',
        }

        header = {}  # dictionary to store header information

        if verbose is None:
            verbose = self._verbose

        # parse input values
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = simulation_directory + ut.io.get_path(snapshot_directory)

        if snapshot_value_kind == 'index':
            snapshot_index = snapshot_value
        else:
            Snapshot = ut.simulation.read_snapshot_times(simulation_directory, verbose)
            snapshot_index = Snapshot.parse_snapshot_values(
                snapshot_value_kind, snapshot_value, verbose
            )

        path_file_name = self.get_snapshot_file_names_indices(
            snapshot_directory, snapshot_index, snapshot_block_index
        )

        self.print_function_name = True
        self.say('* reading header from:  {}'.format(path_file_name.lstrip('./')), verbose)

        # open snapshot file
        with h5py.File(path_file_name, 'r') as file_read:
            header_read = file_read['Header'].attrs  # load header dictionary

            for prop_read_name in header_read:
                if prop_read_name in header_name_dict:
                    prop_save_name = header_name_dict[prop_read_name]
                else:
                    prop_save_name = prop_read_name
                header[prop_save_name] = header_read[prop_read_name]  # transfer to my header dict

        # determine if simulation is cosmological
        if 'cosmological' in header and header['cosmological']:
            assert 0 < header['hubble'] < 1
            assert 0 < header['omega_matter'] <= 1
            assert 0 < header['omega_lambda'] <= 1
        elif (
            0 < header['hubble'] < 1
            and 0 < header['omega_matter'] <= 1
            and 0 < header['omega_lambda'] <= 1
        ):
            header['cosmological'] = True  # compatible with old file headers
        else:
            header['cosmological'] = False
            self.say('assuming that simulation is not cosmological', verbose)
            self.say(
                'read: h = {:.3f}, Omega_matter,0 = {:.3f}, Omega_lambda,0 = {:.3f}'.format(
                    header['hubble'], header['omega_matter'], header['omega_lambda']
                ),
                verbose,
            )

        # if important properties not in header (old file format), initialize to None
        for prop_name in ['omega_baryon', 'omega_radiation']:
            if prop_name not in header:
                header[prop_name] = None

        # check if simulation contains baryons
        header['has.baryons'] = False
        for spec_name in self._species_all:
            if 'dark' not in spec_name:
                if header['particle.numbers.total'][self.species_dict[spec_name]] > 0:
                    header['has.baryons'] = True
                    break

        # check if simulation contains element-tracers to assign abundances in post-processing
        if 'elementtracer.age.bin.number' in header and header['elementtracer.age.bin.number'] > 0:
            header['has.elementtracer'] = True
            header['has.rprocess'] = False
            if 'elementtracer.age.bins' in header:
                header['has.elementtracer.custom'] = True
            elif 'elementtracer.age.min' in header:
                header['has.elementtracer.custom'] = False
            else:
                raise ValueError('not sure how to parse element-tracer model in snapshot header')
        else:
            header['has.elementtracer'] = False
            if header['element.number'] > 11:
                # assume simulation has r-process model enabled
                header['has.rprocess'] = True
            else:
                header['has.rprocess'] = False

        # assign simulation name
        if not simulation_name and simulation_directory != './':
            simulation_name = simulation_directory.split('/')[-2]
            simulation_name = simulation_name.replace('_', ' ')
            simulation_name = simulation_name.replace('res', 'r')
        header['simulation.name'] = simulation_name

        header['catalog.kind'] = 'particle'

        # convert header quantities
        if header['cosmological']:
            header['scalefactor'] = float(header['time'])
            del header['time']
            header['box.length/h'] = float(header['box.length'])
            header['box.length'] /= header['hubble']  # convert to [kpc comoving]
        else:
            header['time'] /= header['hubble']  # convert to [Gyr]
            header['scalefactor'] = 1.0

        self.say('snapshot contains the following number of particles:', verbose)
        # keep only species that have any particles
        read_particle_number = 0
        for spec_name in ut.array.get_list_combined(self._species_all, self._species_read):
            spec_id = self.species_dict[spec_name]
            self.say(
                '  {:9s} (id = {}): {} particles'.format(
                    spec_name, spec_id, header['particle.numbers.total'][spec_id]
                ),
                verbose,
            )

            if header['particle.numbers.total'][spec_id] > 0:
                read_particle_number += header['particle.numbers.total'][spec_id]
            elif spec_name in self._species_read:
                self._species_read.remove(spec_name)

        if read_particle_number <= 0:
            raise OSError(
                f'snapshot file[s] contain no particles of species = {self._species_read}'
            )

        self.say('', verbose)

        return header

    def _read_particles(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        properties='all',
        elements=None,
        convert_float32=False,
        header=None,
        verbose=None,
    ):
        '''
        Read from snapshot file[s] all particles of species type[s] in self._species_read list.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        snapshot_directory: str
            directory of snapshot files within simulation_directory
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift'
        snapshot_value : int or float
            index (number) of snapshot file
        properties : str or list
            name[s] of particle properties to read. 'all' or None = read all properties in snapshot
        elements : str or list
            name[s] of elemental abundances to read. 'all' or None = read all elements in snapshot
        convert_float32 : bool
            whether to convert all floats to 32 bit to save memory
        header : dict
            snapshot file header information (from previous read of file)
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose

        Returns
        -------
        part : dictionary class
            catalog of particles
        '''
        # convert name in snapshot's particle dictionary to custon name preference
        # if comment out any prop, will not read it
        property_dict = {
            # all particles ----------
            'ParticleIDs': 'id',  # indexing starts at 0
            'Coordinates': 'position',  # [kpc comoving]
            'Velocities': 'velocity',  # [km/s physical (peculiar)]
            'Masses': 'mass',  # [M_sun]
            'Potential': 'potential',  # [km^2 / s^2]
            # grav acceleration for dark matter and stars, grav + hydro acceleration for gas
            'Acceleration': 'acceleration',  # [km/s / Gyr]
            # particles with adaptive smoothing
            #'AGS-Softening': 'kernel.length',  # [kpc] (same as SmoothingLength)
            # gas ----------
            'InternalEnergy': 'temperature',  # [K] (converted from stored internal energy)
            'Density': 'density',  # [M_sun / kpc^3]
            'Pressure': 'pressure',  # [M_sun / kpc / Gyr^2]
            'SoundSpeed': 'sound.speed',  # [km/s]
            'SmoothingLength': 'size',  # radius of kernel (smoothing length) [kpc physical]
            # average number of free electrons per proton (per hydrogen nucleon)
            'ElectronAbundance': 'electron.fraction',
            # fraction of hydrogen that is neutral (not ionized)
            'NeutralHydrogenAbundance': 'hydrogen.neutral.fraction',
            'MolecularMassFraction': 'molecule.fraction',  # fraction of mass that is molecular
            'CoolingRate': 'cool.rate',  # [M_sun / yr]
            'StarFormationRate': 'sfr',  # [M_sun / yr]
            'MagneticField': 'magnetic.field',  # 3-D magnetic field [Gauss]
            # divergence of magnetic field (for testing)
            #'DivergenceOfMśgneticField': 'magnetic.field.div',
            #'DivBcleaningFunctionGradPhi': 'magnetic.field.clean.func.grad.phi', # 3-D
            #'DivBcleaningFunctionPhi': 'magnetic.field.clean.func.phi', # 1-D
            # energy of radiation in each frequency bin [M_sun kpc^2 / Gyr^2]
            'PhotonEnergy': 'photon.energy',
            'CosmicRayEnergy': 'cosmicray.energy',  # energy of cosmic rays [M_sun kpc^2 / Gyr^2]

            # star/gas ----------
            # id.generation and id.child initialized to 0 for all gas cells
            # each time a gas cell splits into two:
            #   'self' particle retains id.child, other particle gets id.child += 2 ^ id.generation
            #   both particles get id.generation += 1
            # allows maximum of 30 generations, then restarts at 0
            #   thus, particles with id.child > 2^30 are not unique anymore
            'ParticleChildIDsNumber': 'id.child',
            'ParticleIDGenerationNumber': 'id.generation',
            # mass fraction of individual elements ----------
            # 0 = all metals (everything not H, He)
            # 1 = He, 2 = C, 3 = N, 4 = O, 5 = Ne, 6 = Mg, 7 = Si, 8 = S, 9 = Ca, 10 = Fe
            'Metallicity': 'massfraction',  # linear mass fraction

            # stars ----------
            # 'time' when star particle formed
            # for cosmological sims, = scale-factor; for non-cosmological sims, = time [Gyr]
            'StellarFormationTime': 'form.scalefactor',

            # black holes ----------
            'BH_Mass': 'mass.bh',  # mass of black hole (not including disk) [M_sun]
            'BH_Mass_AlphaDisk': 'mass.disk',  # mass of accretion disk [M_sun]
            'BH_Mdot': 'accretion.rate',  # instantaneous accretion rate [M_sun / yr]
            'BH_AccretionLength': 'size',  # radius of accretion kernel [kpc physical]
            'BH_Specific_AngMom': 'specific.angular.momentum',
            'BH_NProgs': 'merge.number',  # number of BHs that merged into this one (0 if none)
        }

        # dictionary class to store properties for particle species
        part = ParticleDictionaryClass()

        # delete these classes by default, because they only apply to some particle species
        del part.MassLoss
        del part.ElementTracer
        del part.adiabatic_index

        if verbose is None:
            verbose = self._verbose

        # parse input directories
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = simulation_directory + ut.io.get_path(snapshot_directory)

        if snapshot_value_kind == 'index':
            snapshot_index = snapshot_value
        else:
            Snapshot = ut.simulation.read_snapshot_times(simulation_directory, verbose)
            snapshot_index = Snapshot.parse_snapshot_values(
                snapshot_value_kind, snapshot_value, verbose
            )

        path_file_name = self.get_snapshot_file_names_indices(snapshot_directory, snapshot_index)

        # check if need to read snapshot header information
        if not header:
            header = self.read_header(
                simulation_directory,
                snapshot_directory,
                'index',
                snapshot_index,
                verbose=verbose,
            )

        # parse input properties to read
        if properties in ['all', ['all'], None, []]:
            # read all properties (that are un-commented) in property_dict
            properties = list(property_dict.keys())
        elif properties in ['subset', ['subset']]:
            # read default sub-set of properties, should be enough for most analysis
            properties = ['mass', 'position', 'massfraction', 'form.scalefactor']
        else:
            if np.isscalar(properties):
                properties = [properties]  # ensure is list
            # make safe list of properties to read
            properties_temp = []
            for prop_name in list(properties):
                prop_name = str.lower(prop_name)
                if 'massfraction' in prop_name or 'metallicity' in prop_name:
                    prop_name = 'massfraction'  # this property has aliases, ensure default name
                for prop_read_name, prop_save_name in property_dict.items():
                    if prop_name in [
                        str.lower(prop_read_name),
                        str.lower(prop_save_name),
                    ]:
                        properties_temp.append(prop_read_name)
            properties = properties_temp
            del properties_temp

        if 'InternalEnergy' in properties:
            # to compute temperature from InternalEnergy, need He abundance and electron fraction
            for prop_name in np.setdiff1d(['ElectronAbundance', 'Metallicity'], properties):
                properties.append(prop_name)
                if prop_name == 'Metallicity' and elements is None:
                    # user asked to read temperature but not elemental abundances,
                    # so assume that they just need He for computing temperature
                    elements = ['helium']

        # parse input list of elemental abundances to read
        if elements in ['all', ['all'], [], ()]:
            elements = None
        if elements is not None:
            if np.isscalar(elements):
                elements = [elements]  # ensure is list
            elements = list(elements)
            # ensure reading specific elements for specific properties
            if 'InternalEnergy' in properties and 'he' not in elements and 'helium' not in elements:
                # need Helium to compute temperature from internal energy
                elements.append('helium')
            if 'hydrogen' in elements or 'h' in elements:
                # simulation does not store H directly - infer it by subtracting helium and metals
                elements.remove('h')
                elements.remove('hydrogen')
                elements.append('helium')
                elements.append('metals')
            # make safe list of elements to read
            elements = [str.lower(element_name) for element_name in elements]
            for element_name in elements:
                assert element_name in part._element_index
        # all subsequent calls to this element dictionary should be via each species' dictionary
        del part._element_index

        self.say('* reading the following', verbose)
        self.say(f'species: {self._species_read}', verbose)

        # open snapshot file
        with h5py.File(path_file_name, 'r') as file_read:
            part_numbers_in_file = file_read['Header'].attrs['NumPart_ThisFile']

            # loop over each particle species to read
            for spec_name in self._species_read:
                spec_id = self.species_dict[spec_name]
                part_number_tot = header['particle.numbers.total'][spec_id]

                # initialize particle dictionary class for this species
                part[spec_name] = ParticleDictionaryClass()

                # adiabatic index (ratio of specific heats) relevant only for gas
                if spec_name == 'gas':
                    part[spec_name].adiabatic_index = self.gas_adiabatic_index
                else:
                    del part[spec_name].adiabatic_index

                # mass loss relevant only for stars
                if spec_name != 'star':
                    del part[spec_name].MassLoss

                if spec_name in ['star', 'gas']:
                    if 'has.rprocess' in header and not header['has.rprocess']:
                        # simulation does not have the r-process model, so delete its index pointers
                        for element in list(part[spec_name]._element_index):
                            if element.startswith('rp'):
                                del part[spec_name]._element_index[element]

                    if 'has.elementtracer' in header and header['has.elementtracer']:
                        # simulation stored element-tracer weights for post-processing elemental
                        # abundances - initialize element element-tracer dictionary class,
                        # to store age bins and nucleosynthetic yields within this model
                        # see 'gizmo_elementtracer.py' for more info
                        from . import gizmo_elementtracer

                        # append element-tracer dictionary class to the particle species catalog
                        part[spec_name].ElementTracer = gizmo_elementtracer.ElementTracerClass(
                            header
                        )

                        """
                        if 'fire.model' in header and isinstance(header['fire.model'], str)
                            and len(header['fire.model']) > 0:
                            fire_model = header['fire.model']
                        else:
                            fire_model = FIRE_MODEL_DEFAULT
                        if 'fire3' in fire_model:
                            metallicity_initial = 0
                        else:
                            metallicity_initial = 10 ** -5
                        progenitor_metallicity = 0.6

                        # generate nucleosynthetic yield mass fractions for this model
                        FIREYield = gizmo_elementtracer.FIREYieldClass(
                            fire_model, progenitor_metallicity
                        )
                        element_yield_dict = FIREYield.get_element_yields(
                            part[spec_name].ElementTracer['age.bins']
                        )
                        # assign yields to element-tracer dictionary class
                        part[spec_name].ElementTracer.assign_element_yield_massfractions(
                            element_yield_dict
                        )
                        # set initial conditions for mass fractions for each element
                        part[spec_name].ElementTracer.assign_element_initial_massfraction(
                            FIREYield.sun_massfraction, metallicity_initial
                        )
                        """
                    else:
                        del part[spec_name].ElementTracer

                    if elements is not None:
                        # re-set element dictionary pointers if reading a subset of elements
                        element_indices_keep = []  # indices of elements to keep
                        for element_name in elements:
                            element_indices_keep.append(
                                part[spec_name]._element_index[element_name]
                            )
                        element_indices_keep = np.sort(element_indices_keep)

                        # create temporary pointer to update default pointer index array
                        element_pointers = np.arange(len(part[spec_name]._element_index))
                        for element_i, element_index in enumerate(element_indices_keep):
                            element_pointers[element_index] = element_i

                        for element_name in list(part[spec_name]._element_index):
                            element_index = part[spec_name]._element_index[element_name]
                            if element_index in element_indices_keep:
                                part[spec_name]._element_index[element_name] = element_pointers[
                                    element_index
                                ]
                            else:
                                del part[spec_name]._element_index[element_name]

                else:
                    # element index pointers and element-tracers only relevant for stars and gas
                    del part[spec_name]._element_index
                    del part[spec_name].ElementTracer

                # check if snapshot file happens not to have particles of this species
                if part_numbers_in_file[spec_id] > 0:
                    part_read = file_read['PartType' + str(spec_id)]
                    file_read_i = None
                else:
                    # this scenario should occur only for multi-file snapshot
                    if header['file.number.per.snapshot'] == 1:
                        raise OSError(f'no {spec_name} particles in snapshot file')

                    # need to read in other snapshot files until find one with particles of species
                    for file_i in range(1, header['file.number.per.snapshot']):
                        file_name_i = path_file_name.replace('.0.', f'.{file_i}.')
                        file_read_i = h5py.File(file_name_i, 'r')
                        part_numbers_in_file_i = file_read_i['Header'].attrs['NumPart_ThisFile']
                        if part_numbers_in_file_i[spec_id] > 0:
                            # found one
                            part_read = file_read_i['PartType' + str(spec_id)]
                            break
                    else:
                        # tried all files and still did not find particles of species
                        raise OSError(f'no {spec_name} particles in any snapshot file')

                # initialize dictionaries for all properties for species
                properties_to_print = []
                for prop_read_name in part_read.keys():
                    if prop_read_name in properties:
                        prop_name = property_dict[prop_read_name]

                        # determine shape of prop array
                        if len(part_read[prop_read_name].shape) == 1:
                            prop_shape = part_number_tot
                        elif len(part_read[prop_read_name].shape) == 2:
                            prop_shape = [part_number_tot, part_read[prop_read_name].shape[1]]
                            if prop_read_name == 'Metallicity' and elements is not None:
                                prop_shape = [part_number_tot, len(elements)]

                        # determine data type to store
                        prop_read_dtype = part_read[prop_read_name].dtype
                        if convert_float32 and prop_read_dtype == 'float64':
                            prop_read_dtype = np.float32

                        # initialize to -1's
                        part[spec_name][prop_name] = np.zeros(prop_shape, prop_read_dtype) - 1

                        if prop_name == 'id':
                            # initialize so calling an un-itialized value leads to error
                            part[spec_name][prop_name] -= part_number_tot

                        if prop_read_name in property_dict:
                            properties_to_print.append(property_dict[prop_read_name])
                        else:
                            properties_to_print.append(prop_read_name)

                if len(properties_to_print) != len(part_read.keys()):
                    # read only a sub-set of properties in snapshot
                    properties_to_print.sort()
                    self.say(f'{spec_name} properties: {properties_to_print}', verbose)

                # special case: particle mass is fixed and given in mass array in header
                if 'Masses' in properties and 'Masses' not in part_read:
                    prop_name = property_dict['Masses']
                    part[spec_name][prop_name] = np.zeros(part_number_tot, dtype=np.float32)

                if file_read_i is not None:
                    # close, if had to open another snapshot file to find particles of this species
                    file_read_i.close()

        if elements is not None:
            # read only a sub-set of elemental abundances
            self.say(f'elemental abundances: {elements}', verbose)

        self.say('', verbose)

        # read properties for each species ----------
        # initialize particle indices to assign to each species from each file
        part_indices_lo = np.zeros(len(self._species_read), dtype=np.int64)

        if header['file.number.per.snapshot'] == 1:
            self.say(
                '* reading particles from:\n    {}'.format(path_file_name.lstrip('./')), verbose
            )
        else:
            self.say('* reading particles from:', verbose)

        # loop over all file blocks at given snapshot
        for file_i in range(header['file.number.per.snapshot']):
            # open i'th of multiple files for snapshot
            file_name_i = path_file_name.replace('.0.', f'.{file_i}.')

            # open snapshot file
            with h5py.File(file_name_i, 'r') as file_in:
                if header['file.number.per.snapshot'] > 1:
                    self.say('  ' + file_name_i.split('/')[-1], verbose)

                part_numbers_in_file = file_in['Header'].attrs['NumPart_ThisFile']

                # read particle properties
                for spec_i, spec_name in enumerate(self._species_read):
                    spec_id = self.species_dict[spec_name]
                    if part_numbers_in_file[spec_id] > 0:
                        part_read = file_in['PartType' + str(spec_id)]

                        part_index_lo = part_indices_lo[spec_i]
                        part_index_hi = part_index_lo + part_numbers_in_file[spec_id]

                        # check if mass of species is fixed, according to header mass array
                        if 'Masses' in properties and header['particle.masses'][spec_id] > 0:
                            prop_name = property_dict['Masses']
                            part[spec_name][prop_name][part_index_lo:part_index_hi] = header[
                                'particle.masses'
                            ][spec_id]

                        for prop_read_name, prop_values in part_read.items():
                            if prop_read_name in properties:
                                prop_name = property_dict[prop_read_name]
                                if len(prop_values.shape) == 1:
                                    part[spec_name][prop_name][
                                        part_index_lo:part_index_hi
                                    ] = prop_values
                                elif len(part_read[prop_read_name].shape) == 2:
                                    if prop_read_name == 'Metallicity' and elements is not None:
                                        prop_read_name = prop_values[:, element_indices_keep]
                                    else:
                                        prop_read_name = prop_values

                                    part[spec_name][prop_name][
                                        part_index_lo:part_index_hi, :
                                    ] = prop_read_name

                        part_indices_lo[spec_i] = part_index_hi  # set indices for next file

        self.say('', verbose)

        return part

    def _adjust_particle_properties(
        self,
        part,
        header,
        particle_subsample_factor=None,
        separate_dark_lowres=True,
        sort_dark_by_id=False,
        verbose=None,
    ):
        '''
        Adjust properties for each species, including unit conversions, separating dark species by
        mass, sorting by id, and subsampling.

        Parameters
        ----------
        part : dictionary class
            catalog of particles at snapshot
        header : dict
            header dictionary
        particle_subsample_factor : int
            factor to periodically subsample particles, to save memory
        separate_dark_lowres : bool
            whether to separate low-resolution dark matter into separate dicts according to mass
        sort_dark_by_id : bool
            whether to sort dark-matter particles by id
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose
        '''
        if verbose is None:
            verbose = self._verbose

        # if dark2 contains different masses (refinements), split into separate dicts
        species_name = 'dark2'

        if species_name in part and 'mass' in part[species_name]:
            dark_lowres_masses = np.unique(part[species_name]['mass'])
            if dark_lowres_masses.size > 9:
                self.say(
                    f'! warning: {dark_lowres_masses.size} different masses of low-res dark matter'
                )

            if separate_dark_lowres and dark_lowres_masses.size > 1:
                self.say(
                    '* separating low-resolution dark matter by mass into dictionaries', verbose
                )
                dark_lowres = {}
                for prop_name in part[species_name]:
                    dark_lowres[prop_name] = np.array(part[species_name][prop_name])

                for dark_i, dark_mass in enumerate(dark_lowres_masses):
                    spec_indices = np.where(dark_lowres['mass'] == dark_mass)[0]
                    spec_name = f'dark{dark_i + 2}'

                    # initialize new particle dictionary class for low-res dark matter
                    part[spec_name] = ParticleDictionaryClass()

                    for prop_name, prop_values in dark_lowres.items():
                        part[spec_name][prop_name] = prop_values[spec_indices]
                    self.say(f'{spec_name}: {spec_indices.size} particles', verbose)

                del spec_indices
                self.say('', verbose)

        if sort_dark_by_id:
            # order dark-matter particles by id - should be conserved across snapshots
            self.say('* sorting the following dark particles by id', verbose)
            for spec_name in part:
                if 'dark' in spec_name and 'id' in part[spec_name]:
                    indices_sorted = np.argsort(part[spec_name]['id'])
                    self.say(f'{spec_name}: {indices_sorted.size} particles', verbose)
                    for prop_name in part[spec_name]:
                        part[spec_name][prop_name] = part[spec_name][prop_name][indices_sorted]
            del indices_sorted
            self.say('', verbose)

        # apply unit conversions
        mass_conversion = 1e10 / header['hubble']  # multiple by this for [M_sun]
        length_conversion = header['scalefactor'] / header['hubble']  # multiply for [kpc physical]
        time_conversion = 1 / header['hubble']  # multiply by this for [Gyr]

        for spec_name in part:
            if 'position' in part[spec_name]:
                # convert to [kpc comoving]
                part[spec_name]['position'] /= header['hubble']

            if 'velocity' in part[spec_name]:
                # convert to [km/s physical/peculiar]
                part[spec_name]['velocity'] *= np.sqrt(header['scalefactor'])

            if 'acceleration' in part[spec_name]:
                # convert to [km/s / Gyr]
                # verified that |a_r| = v_circ^2 / r = GM(<r)/r^2 = d(phi)/dr across redshift
                part[spec_name]['acceleration'] *= header['hubble']

            for prop_name in ['mass', 'mass.bh', 'mass.disk']:
                if prop_name in part[spec_name]:
                    # convert to [M_sun]
                    part[spec_name][prop_name] *= mass_conversion
                    # rename blackhole 'mass' to 'mass.total' to avoid confusion with 'mass.bh'
                    if spec_name == 'blackhole' and prop_name == 'mass':
                        part[spec_name]['mass.total'] = part[spec_name][prop_name]
                        del part[spec_name][prop_name]

            if 'accretion.rate' in part[spec_name]:
                # convert to [M_sun / yr]
                part[spec_name][prop_name] *= mass_conversion / time_conversion

            if (
                'massfraction' in part[spec_name]
                and 'ElementTracer' in part[spec_name].__dict__
                and part[spec_name].ElementTracer is not None
            ):
                # convert the element-tracer mass weights into dimensionless units of:
                # mass fraction (relative to my own mass) of winds/ejecta deposited into me
                # (as a gas cell) during each element-tracer age bin
                # element-tracer weight value of 1 therefore means that a particle received
                # winds/ejecta from its own mass of stars across the entire age bin
                elementtracer_index_start = part[spec_name].ElementTracer['element.index.start']
                part[spec_name]['massfraction'][:, elementtracer_index_start:] /= mass_conversion

            if 'size' in part[spec_name]:
                # convert to [kpc physical]
                part[spec_name]['size'] *= length_conversion
                # size in snapshot is full extent of the kernal (radius of compact support)
                # convert to mean interparticle spacing = volume^(1/3)
                part[spec_name]['size'] *= (np.pi / 3) ** (1 / 3) / 2  # 0.5077
                # convert to 1-sigma length of a Gaussian (assuming cubic spline)
                # part[spec_name]['size'] *= 0.50118
                # convert to plummer softening (assuming cubic spline)
                # part[spec_name]['size'] /= 2.8

            if 'form.scalefactor' in part[spec_name]:
                if not header['cosmological']:
                    part[spec_name]['form.scalefactor'] *= time_conversion  # convert to [Gyr]

            if 'potential' in part[spec_name]:
                # convert to [km^2 / s^2 physical]
                # verified that |a_r| = v_circ^2 / r = GM(<r)/r^2 = d(phi)/dr across redshift
                part[spec_name]['potential'] /= header['scalefactor']

            if 'density' in part[spec_name]:
                # convert to [M_sun / kpc^3 physical]
                part[spec_name]['density'] *= mass_conversion / length_conversion**3

            if 'pressure' in part[spec_name]:
                # convert to [M_sun / kpc / Gyr^2]
                part[spec_name]['pressure'] *= (
                    mass_conversion / length_conversion / time_conversion**2
                )

            if 'temperature' in part[spec_name]:
                # convert from [km^2 / s^2] to [Kelvin]
                # ignore small corrections from elements beyond He
                helium_mass_fracs = part[spec_name].prop('massfraction.helium')
                ys_helium = helium_mass_fracs / (4 * (1 - helium_mass_fracs))
                mus = (1 + 4 * ys_helium) / (1 + ys_helium + part[spec_name]['electron.fraction'])
                molecular_weights = mus * ut.constant.proton_mass
                part[spec_name]['temperature'] *= (
                    ut.constant.centi_per_kilo**2
                    * (part[spec_name].adiabatic_index - 1)
                    * molecular_weights
                    / ut.constant.boltzmann
                )
                del (helium_mass_fracs, ys_helium, mus, molecular_weights)

            if 'cosmicray.energy' in part[spec_name]:
                # convert to [M_sun kpc^2 / Gyr^2]
                part[spec_name]['cosmicray.energy'] *= (
                    mass_conversion * length_conversion**2 / time_conversion**2
                )

            if 'photon.energy' in part[spec_name]:
                # convert to [M_sun kpc^2 / Gyr^2]
                part[spec_name]['photon.energy'] *= (
                    mass_conversion * length_conversion**2 / time_conversion**2
                )

        # renormalize so potential max = 0
        renormalize_potential = False
        if renormalize_potential:
            potential_max = 0
            for spec_name in part:
                if (
                    'potential' in part[spec_name]
                    and part[spec_name]['potential'].max() > potential_max
                ):
                    potential_max = part[spec_name]['potential'].max()
            for spec_name in part:
                if 'potential' in part[spec_name]:
                    part[spec_name]['potential'] -= potential_max

        # sub-sample particles, for smaller memory
        if particle_subsample_factor is not None and particle_subsample_factor > 1:
            self.say(
                f'* periodically subsampling all particles by factor = {particle_subsample_factor}',
                verbose,
                end='\n\n',
            )
            for spec_name in part:
                for prop_name in part[spec_name]:
                    part[spec_name][prop_name] = part[spec_name][prop_name][
                        ::particle_subsample_factor
                    ]

    def get_snapshot_file_names_indices(
        self, directory, snapshot_index=None, snapshot_block_index=0
    ):
        '''
        Get name of file or directory (with relative path) and index for all snapshots in directory.
        If input valid snapshot_index, get its file name (if multiple files per snapshot, get name
        of 0th one).
        If input snapshot_index as None or 'all', get name of file/directory and index for each
        snapshot file/directory.

        Parameters
        ----------
        directory : str
            directory to check for files
        snapshot_index : int
            index of snapshot: if None or 'all', get all snapshots in directory
        snapshot_block_index : int
            index of file block (if multiple files per snapshot)
            if None or 'all', return names of all file blocks for snapshot

        Returns
        -------
        path_file_name[s] : str or list
            (relative) path + name of file[s]
        [file_indices : list of ints
            indices of snapshot files]
        '''
        directory = ut.io.get_path(directory)

        assert (
            isinstance(snapshot_block_index, int)
            or snapshot_block_index is None
            or snapshot_block_index == 'all'
        )

        # get names and indices of all snapshot files in directory
        path_file_names, file_indices = ut.io.get_file_names(
            directory + self._snapshot_name_base, (int, float)
        )

        # if ask for all snapshots, return all files/directories and indices
        if snapshot_index is None or snapshot_index == 'all':
            return path_file_names, file_indices

        # else get file name for single snapshot
        if snapshot_index < 0:
            snapshot_index = file_indices[snapshot_index]  # allow negative indexing of snapshots
        elif snapshot_index not in file_indices:
            raise OSError(f'cannot find snapshot index = {snapshot_index} in:  {path_file_names}')

        path_file_names = path_file_names[np.where(file_indices == snapshot_index)[0][0]]

        if self._snapshot_file_extension not in path_file_names:
            # got snapshot directory with multiple files
            # get file name with snapshot_block_index in name
            path_file_names = ut.io.get_file_names(
                path_file_names
                + '/'
                + self._snapshot_name_base
                + '*'
                + self._snapshot_file_extension
            )
            path_file_block_name = None

            if len(path_file_names) > 0:
                for path_file_name in path_file_names:
                    if f'.{snapshot_block_index}.' in path_file_name:
                        path_file_block_name = path_file_name

            if path_file_block_name:
                path_file_names = path_file_block_name
            else:
                raise OSError(
                    f'cannot find snapshot file block {snapshot_block_index} in:  {path_file_names}'
                )

        return path_file_names

    def _get_cosmology(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        omega_lambda=None,
        omega_matter=None,
        omega_baryon=None,
        hubble=None,
        sigma_8=None,
        n_s=None,
        verbose=None,
    ):
        '''
        Return cosmological parameters via Cosmology dictionary class.
        If input simulation_directory, (try to) read cosmological parameters from the MUSIC
        initial condition config file within this simulation_directory.
        If cannot find the MUSIC config file, use what cosmological parameters are input,
        and assume the rest from the AGORA simulation.

        Parameters
        ----------
        simulation_directory : str
            base directory of simulation
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose

        Returns
        -------
        Cosmology : dict class
            stores cosmological parameters via dict and useful functions as methods of this class
        '''

        def _get_check_value(line, value_test=None):
            frac_dif_max = 0.01
            value = float(line.split('=')[-1].strip())
            if 'h0' in line:
                value /= 100
            if value_test is not None:
                frac_dif = np.abs((value - value_test) / value)
                if frac_dif > frac_dif_max:
                    print(f'! read {line}, but previously assigned = {value_test}')
            return value

        if verbose is None:
            verbose = self._verbose

        if simulation_directory:
            # find MUSIC file, assuming named *.conf
            file_name_find = (
                ut.io.get_path(simulation_directory) + '*/' + gizmo_default.music_config_file_name
            )
            path_file_names = ut.io.get_file_names(file_name_find, verbose=False)
            if len(path_file_names) > 0:
                path_file_name = path_file_names[0]
                self.say(
                    '* reading cosmological parameters from:  {}'.format(
                        path_file_name.lstrip('./')
                    ),
                    verbose,
                    end='\n\n',
                )
                # read cosmological parameters
                with open(path_file_name, 'r', encoding='utf-8') as file_in:
                    for line in file_in:
                        line = line.lower().strip().strip('\n')  # ensure lowercase for safety
                        if 'omega_l' in line:
                            omega_lambda = _get_check_value(line, omega_lambda)
                        elif 'omega_m' in line:
                            omega_matter = _get_check_value(line, omega_matter)
                        elif 'omega_b' in line:
                            omega_baryon = _get_check_value(line, omega_baryon)
                        elif 'h0' in line:
                            hubble = _get_check_value(line, hubble)
                        elif 'sigma_8' in line:
                            sigma_8 = _get_check_value(line, sigma_8)
                        elif 'nspec' in line:
                            n_s = _get_check_value(line, n_s)
            else:
                self.say('! cannot find MUSIC config file:  {}'.format(file_name_find.lstrip('./')))

        # use cosmology from the AGORA simulation as default, if cannot find MUSIC config file
        if omega_baryon is None or sigma_8 is None or n_s is None:
            self.say('! missing cosmological parameters, assuming cosmology from AGORA')
            if omega_baryon is None:
                omega_baryon = 0.0455
                self.say(f'assuming omega_baryon = {omega_baryon}', verbose)
            if sigma_8 is None:
                sigma_8 = 0.807
                self.say(f'assuming sigma_8 = {sigma_8}', verbose)
            if n_s is None:
                n_s = 0.961
                self.say(f'assuming n_s = {n_s}', verbose)
            self.say('', verbose)

        Cosmology = ut.cosmology.CosmologyClass(
            omega_lambda, omega_matter, omega_baryon, hubble, sigma_8, n_s
        )

        return Cosmology

    def _check_particle_properties(self, part):
        '''
        Checks sanity of particle properties, print warning if they are outside given limits.

        Parameters
        ----------
        part : dictionary class
            catalog of particles
        '''
        # limits of sanity
        prop_limit = {
            'id': [0, 4e9],
            'id.child': [0, 4e9],
            'id.generation': [0, 4e9],
            'position': [0, 1e6],  # [kpc comoving]
            'velocity': [-1e5, 1e5],  # [km/s]
            'mass': [9, 1e11],  # [M_sun]
            'potential': [-1e9, 1e9],  # [km^2 / s^2]
            'temperature': [0.1, 1e9],  # [K]
            'density': [0, 1e14],  # [M_sun / kpc^3]
            'size': [0, 1e9],  # [kpc]
            'hydrogen.neutral.fraction': [0, 1],
            'sfr': [0, 1000],  # [M_sun / yr]
            'form.scalefactor': [0, 1],
            #'massfraction': [0, 1], # has arbitrarily large values if using element-tracers
        }

        self.say('* checking sanity of particle properties')

        for spec_name in part:
            for prop_name in [k for k in prop_limit if k in part[spec_name]]:
                # exclude element-tracer fields
                # if prop_name == 'massfraction' and props.shape[1] > 11:
                #    props = props[:, :11]

                if (
                    part[spec_name][prop_name].min() < prop_limit[prop_name][0]
                    or part[spec_name][prop_name].max() > prop_limit[prop_name][1]
                ):
                    self.say(
                        '! warning: {} {} [min, max] = [{}, {}]'.format(
                            spec_name,
                            prop_name,
                            ut.io.get_string_from_numbers(part[spec_name][prop_name].min(), 3),
                            ut.io.get_string_from_numbers(part[spec_name][prop_name].max(), 3),
                        )
                    )

                elif prop_name == 'mass' and spec_name in ['star', 'gas', 'dark']:
                    m_med = np.median(part[spec_name][prop_name])
                    if (
                        part[spec_name][prop_name].min() < 0.5 * m_med
                        or part[spec_name][prop_name].max() > 4 * m_med
                    ):
                        self.say(
                            '! warning: {} {} [min, med, max] = [{}, {}, {}]'.format(
                                spec_name,
                                prop_name,
                                ut.io.get_string_from_numbers(part[spec_name][prop_name].min(), 3),
                                ut.io.get_string_from_numbers(
                                    np.median(part[spec_name][prop_name]), 3
                                ),
                                ut.io.get_string_from_numbers(part[spec_name][prop_name].max(), 3),
                            )
                        )

        print()

    def assign_hosts_coordinates(
        self,
        part,
        method=True,
        species_name='',
        part_indicess=None,
        assign_formation_coordinates=False,
        velocity_distance_max=8,
        host_number=1,
        exclusion_distance=400,
        simulation_directory=gizmo_default.simulation_directory,
        track_directory=gizmo_default.track_directory,
        verbose=None,
    ):
        '''
        Assign position [kpc comoving] and velocity [km/s] of each host galaxy/halo.
        Use species_name, if defined, else default to stars for baryonic simulation or
        dark matter for dark matter-only simulation.

        Parameters
        ----------
        part : dictionary class
            catalog of particles at snapshot
        method : str
            method to use to get host coordinates.
            if a string, tells the code which method to use:
                'track' : reads host coordinates from track/host_coordinates.hdf5,
                    compiled during particle tracking using only stars in each host at z = 0
                'halo' : reads host halo coordinates from halo/rockstar_dm/catalog_hdf5/
                'mass' or 'potential' or 'massfraction.metals' : assign coordinates during read in
                    via iterative zoom-in, weighting each particle by that property
            if True (default), will try a few methods in the following order of preference:
                if a baryonic simulation, try 'track' then 'mass'
                if a DM-only simulations, try 'halo' then 'mass'
        species_name : str
            which particle species to use to define center
            relevant only if method is 'mass' or 'potential' or 'massfraction.metals'
        part_indicess : array or list of arrays
            list of indices of particles to use to define host center coordinates
            if supply a list of arrays, use each list element for a different host
        assign_formation_coordinates : bool
            whether to assign to stars their coordindates wrt each host galaxy at formation
            (if reading hosts coordinates from file)
        velocity_distance_max : float
            maximum distance to keep particles to compute velocity
        host_number : int
            number of hosts to assign
        exclusion_distance : float
            radius around previous hosts' center position[s] to exclude particles in
            finding center of next host [kpc comoving]
        simulation_directory : str
            directory of simulation
        snapshot_directory: str
            directory of snapshot files, within simulation_directory
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose
        '''
        if verbose is None:
            verbose = self._verbose

        if method is True:
            if part.info['has.baryons']:
                method = 'track'
            else:
                method = 'halo'
        assert method in [
            True,
            'track',
            'halo',
            'mass',
            'potential',
            'massfraction.metals',
        ]

        if not species_name:
            if 'star' in part:
                species_name = 'star'
            elif 'dark' in part:
                species_name = 'dark'
            elif 'gas' in part:
                species_name = 'gas'
            elif 'blackhole' in part:
                species_name = 'blackhole'
            elif 'dark2' in part:
                species_name = 'dark2'
        assert species_name in ['star', 'dark', 'dark2', 'gas', 'blackhole']

        if method in ['track', 'halo']:
            try:
                if method == 'track':
                    # read coordinates and rotation tensor of each host across all snapshots
                    ParticleCoordinate = gizmo_track.ParticleCoordinateClass()
                    ParticleCoordinate.io_hosts_coordinates(
                        part,
                        simulation_directory,
                        track_directory,
                        assign_formation_coordinates,
                        verbose=verbose,
                    )
                    if host_number != len(part.host['position']):
                        self.say(
                            f'! warning: input host_number = {host_number},'
                            + f' but read coordinates for {len(part.host["position"])} hosts\n'
                            + f'  if you want to assign coordinates for {host_number} hosts,'
                            + ' set assign_hosts="mass"'
                        )

                elif method == 'halo':
                    self._assign_hosts_coordinates_from_halos(
                        part, host_number, simulation_directory, verbose
                    )

            except (IOError, ImportError):
                self.say('! cannot read file containing hosts coordinates')
                self.say('instead will assign hosts via iterative zoom on particle mass')
                method = 'mass'
                self._assign_hosts_coordinates_from_particles(
                    part,
                    species_name,
                    part_indicess,
                    method,
                    velocity_distance_max,
                    host_number,
                    exclusion_distance,
                    verbose,
                )

        else:
            self._assign_hosts_coordinates_from_particles(
                part,
                species_name,
                part_indicess,
                method,
                velocity_distance_max,
                host_number,
                exclusion_distance,
                verbose,
            )

        self.say('', verbose)

    def _assign_hosts_coordinates_from_particles(
        self,
        part,
        species_name,
        part_indicess,
        method='mass',
        velocity_distance_max=8,
        host_number=1,
        exclusion_distance=400,
        verbose=None,
    ):
        '''
        Utility function for assign_hosts_coordinates().
        Compute and assign host galaxy positions and velocities from the particles.
        '''
        if verbose is None:
            verbose = self._verbose

        if (
            species_name not in part
            or 'position' not in part[species_name]
            or len(part[species_name]['position']) == 0
        ):
            self.say('! did not read star or dark particles, so cannot assign any hosts')
            return

        # max radius around each host position to includer particles to compute center velocity
        if velocity_distance_max is None or velocity_distance_max <= 0:
            if species_name == 'dark':
                velocity_distance_max = 30
            else:
                velocity_distance_max = 8

        if 'position' in part[species_name]:
            # assign to particle dictionary
            part.host['position'] = ut.particle.get_center_positions(
                part,
                species_name,
                part_indicess,
                method,
                host_number,
                exclusion_distance,
                return_single_array=False,
                verbose=verbose,
            )

        if 'velocity' in part[species_name]:
            # assign to particle dictionary
            part.host['velocity'] = ut.particle.get_center_velocities_or_accelerations(
                part,
                'velocity',
                species_name,
                part_indicess,
                method,
                velocity_distance_max,
                part.host['position'],
                return_single_array=False,
                verbose=verbose,
            )

        if 'acceleration' in part[species_name]:
            # assign to particle dictionary
            part.host['acceleration'] = ut.particle.get_center_velocities_or_accelerations(
                part,
                'acceleration',
                species_name,
                part_indicess,
                method,
                velocity_distance_max,
                part.host['position'],
                return_single_array=False,
                verbose=verbose,
            )

        # assign to each particle species dictionary
        for spec_name in part:
            for host_prop_name in part.host:
                part[spec_name].host[host_prop_name] = part.host[host_prop_name]

    def _assign_hosts_coordinates_from_halos(
        self,
        part,
        host_number,
        simulation_directory=gizmo_default.simulation_directory,
        verbose=None,
    ):
        '''
        Utility function for assign_hosts_coordinates().
        Read and assign host halo positions and velocities from the halo catalog at that snapshot.
        '''
        from halo_analysis import halo_io

        if verbose is None:
            verbose = self._verbose

        hal = halo_io.IO.read_catalogs(
            'index',
            part.snapshot['index'],
            simulation_directory,
            species=None,
            host_number=host_number,
        )

        host_indices = np.array(
            [hal.prop(f'host{host_i + 1}.index', 0) for host_i in range(host_number)]
        )
        for host_prop_name in ['position', 'velocity']:
            part.host[host_prop_name] = hal[host_prop_name][host_indices]
            for spec_name in part:
                part[spec_name].host[host_prop_name] = hal[host_prop_name][host_indices]

        if verbose:
            for host_i, host_position in enumerate(part.host['position']):
                self.say(f'host{host_i + 1} position = (', end='')
                ut.io.print_array(host_position, '{:.2f}', end='')
                print(') [kpc comoving]')

            for host_i, host_velocity in enumerate(part.host['velocity']):
                self.say(f'host{host_i + 1} velocity = (', end='')
                ut.io.print_array(host_velocity, '{:.1f}', end='')
                print(') [km/s]')

    def assign_hosts_rotation(
        self,
        part,
        species_name='',
        distance_max=10,
        mass_percent=90,
        age_percent=25,
        verbose=None,
    ):
        '''
        Compute and assign rotation tensor and ratios of principal axes
        (defined via the moment of inertia tensor) for each host galaxy.
        By default, use stars for baryonic simulations, or if no stars in catalog, use gas.

        Parameters
        ----------
        part : dictionary class
            catalog of particles at snapshot
        species_name : string
            name of particle species to use to determine rotation
        distance_max : float
            maximum distance to select particles [kpc physical]
        mass_percent : float
            keep particles within the distance that encloses mass percent [0, 100] of all particles
            within distance_max
        age_percent : float
            keep youngest age_percent of (star) particles within distance cut
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose
        '''
        if verbose is None:
            verbose = self._verbose

        if not species_name:
            if 'star' in part:
                species_name = 'star'
            elif 'gas' in part:
                species_name = 'gas'
        assert species_name in ['star', 'gas', 'dark']

        principal_axes = ut.particle.get_principal_axes(
            part,
            species_name,
            distance_max,
            mass_percent,
            age_percent,
            center_positions=part.host['position'],
            center_velocities=part.host['velocity'],
            return_single_array=False,
            verbose=verbose,
        )

        if principal_axes is not None and len(principal_axes) > 0:
            for prop_name in principal_axes:
                part.host[prop_name] = principal_axes[prop_name]
                for spec_name in part:
                    part[spec_name].host[prop_name] = principal_axes[prop_name]

    def assign_particle_orbits(
        self, part, species=None, host_positions=None, host_velocities=None, verbose=None
    ):
        '''
        Assign derived orbital properties wrt each host to each particle species.

        Parameters
        ----------
        part : dictionary class
            catalog of particles at snapshot
        species : str or list
            particle species to compute
        host_positions : array or array of arrays
            position[s] of hosts
        host_velocities : array or array of arrays
            velocity[s] of hosts
        verbose : bool
            whether to print diagnostic information. if None, default to stored self._verbose
        '''
        if not species:
            species = ['star', 'gas', 'dark']
        species = ut.particle.parse_species(part, species)

        self.say(f'* assigning orbital properties wrt each host galaxy/halo to {species}', verbose)

        if host_positions is None:
            host_positions = part.host['position']
        if host_velocities is None:
            host_velocities = part.host['velocity']

        for host_i, host_position in enumerate(host_positions):
            host_velocity = host_velocities[host_i]

            orb = ut.particle.get_orbit_dictionary(
                part, species, None, host_position, host_velocity, return_single_dict=False
            )

            host_name = ut.catalog.get_host_name(host_i)

            for spec_name in species:
                for prop_name in orb[spec_name]:
                    part[spec_name][host_name + prop_name] = orb[spec_name][prop_name]


Read = ReadClass()


class WriteClass(ReadClass):
    '''
    Read Gizmo snapshot[s] and (re)write information to file.
    '''

    def write_exsitu_flag(
        self,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_directory=gizmo_default.simulation_directory,
        track_directory=gizmo_default.track_directory,
        exsitu_distance=30,
        exsitu_distance_scaling=True,
    ):
        '''
        Read single snapshot, with star coordinates at formation.
        Apply a total distance treshold to define ex-situ stars.
        Write text file that contains binary flag of whether star particle formed ex-situ.

        Parameters
        ----------
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift'
        snapshot_value : int or float
            index (number) of snapshot file
        simulation_directory : str
            directory of simulation
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        exsitu_distance : float
            minimum distance to define ex-situ stars [kpc physical or comoving]
        exsitu_distance_scaling : bool
            whether to scale exsitu_distance with scale-factor at formation
        '''
        species_name = 'star'
        file_name = f'{species_name}_exsitu_flag_{{}}.txt'

        track_directory = ut.io.get_path(track_directory)

        part = self.read_snapshots(
            species_name,
            snapshot_value_kind,
            snapshot_value,
            simulation_directory,
            track_directory=track_directory,
            properties=['form.scalefactor', 'id'],
            assign_formation_coordinates=True,
            check_properties=False,
        )

        file_path_name = track_directory + file_name.format(part.snapshot['index'])

        form_host_distance = part[species_name].prop('form.host.distance.total')

        if 'form.host2.distance' in part[species_name]:
            # simulation has multiple primary hosts - use smallest distance
            form_host2_distance = part[species_name].prop('form.host2.distance.total')
            masks = form_host2_distance < form_host_distance
            form_host_distance[masks] = form_host2_distance[masks]

        if exsitu_distance_scaling:
            # use fixed threshold in comoving distance: d_form > exsitu_distance * a kpc
            form_host_distance /= part[species_name].prop('form.scalefactor')

        exsitu_masks = 1 * (form_host_distance > exsitu_distance)

        self.say(
            '{:d} of {:d} ({:.1f}%) stars formed ex-situ'.format(
                exsitu_masks.sum(), exsitu_masks.size, 100 * exsitu_masks.sum() / exsitu_masks.size
            )
        )

        with open(file_path_name, 'w', encoding='utf-8') as file_out:
            header = '# for every star particle at snapshot {},'.format(part.snapshot['index'])
            header += ' this ex-situ flag = 1 if distance_from_host_at_formation > {:.1f}'.format(
                exsitu_distance
            )
            if exsitu_distance_scaling:
                header += ' kpc comoving\n'
            else:
                header += ' kpc physical\n'

            file_out.write(header)

            for exsitu_mask in exsitu_masks:
                file_out.write(f'{exsitu_mask}\n')

        self.say(f'wrote {file_path_name}')

    def rewrite_snapshot(
        self,
        species='gas',
        action='delete',
        value_adjust=None,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
    ):
        '''
        Read single snapshot.
        Rewrite, deleting given species and/or adjusting particle properties.

        Parameters
        ----------
        species : str or list
            name[s] of particle species to delete:
            'gas' = gas
            'dark' = dark matter at highest resolution
            'dark2' = dark matter at lower resolution
            'star' = stars
            'blackhole' = black holes
        action : str
            what to do to snapshot file: 'delete', 'velocity'
        value_adjust : float
            value by which to adjust property (if not deleting)
        snapshot_value_kind : str
            input snapshot number kind: 'index', 'redshift'
        snapshot_value : int or float
            index (number) of snapshot file
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of snapshot files within simulation_directory
        '''
        if np.isscalar(species):
            species = [species]  # ensure is list

        # read information about snapshot times ----------
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = simulation_directory + ut.io.get_path(snapshot_directory)

        Snapshot = ut.simulation.read_snapshot_times(simulation_directory, self._verbose)
        snapshot_index = Snapshot.parse_snapshot_values(
            snapshot_value_kind, snapshot_value, self._verbose
        )

        path_file_name = self.get_snapshot_file_names_indices(snapshot_directory, snapshot_index)
        self.say('* reading header from:  {}'.format(path_file_name.lstrip('./')), end='\n\n')

        # read header ----------
        # open snapshot file and parse header
        with h5py.File(path_file_name, 'r+') as file_in:
            header = file_in['Header'].attrs  # load header dictionary

            # read and delete input species ----------
            for file_i in range(header['NumFilesPerSnapshot']):
                # open i'th of multiple files for snapshot
                file_name_i = path_file_name.replace('.0.', f'.{file_i}.')
                file_read = h5py.File(file_name_i, 'r+')

                self.say('reading particles from: ' + file_name_i.split('/')[-1])

                if 'delete' in action:
                    part_number_in_file = list(header['NumPart_ThisFile'])
                    part_number = list(header['NumPart_Total'])

                # read and delete particle properties
                for _spec_i, spec_name in enumerate(species):
                    spec_id = self.species_dict[spec_name]
                    spec_read = 'PartType' + str(spec_id)
                    self.say(f'adjusting species = {spec_name}')

                    if 'delete' in action:
                        self.say(f'deleting species = {spec_name}')

                        # zero numbers in header
                        part_number_in_file[spec_id] = 0
                        part_number[spec_id] = 0

                        # delete properties
                        # for prop_name in file_in[spec_read]:
                        #    del(file_in[spec_read + '/' + prop_name])
                        #    self.say(f'  deleting {prop_name})

                        del file_read[spec_read]

                    elif 'velocity' in action and value_adjust:
                        dimension_index = 2  # boost velocity along z-axis
                        self.say(
                            '  boosting velocity along axis.{} by {:.1f} km/s'.format(
                                dimension_index, value_adjust
                            )
                        )
                        velocities = file_in[spec_read + '/' + 'Velocities']
                        scalefactor = 1 / (1 + header['Redshift'])
                        velocities[:, 2] += value_adjust / np.sqrt(scalefactor)
                        # file_in[spec_read + '/' + 'Velocities'] = velocities

                    print()

                if 'delete' in action:
                    header['NumPart_ThisFile'] = part_number_in_file
                    header['NumPart_Total'] = part_number

    def rewrite_snapshot_to_text(self, part):
        '''
        Re-write snapshot to text file, one file per particle species.

        Parameters
        ----------
        part : dict class
            catalog of particles at snapshot
        '''
        species_name = 'dark'
        file_name = 'snapshot_{}_{}.txt'.format(part.snapshot['index'], species_name)
        part_spec = part[species_name]

        with open(file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(
                '# id mass[M_sun] distance_wrt_host(x,y,z)[kpc] velocity_wrt_host(x,y,z)[km/s]\n'
            )

            for pi, pid in enumerate(part_spec['id']):
                file_out.write(
                    '{} {:.3e} {:.3f} {:.3f} {:.3f} {:.1f} {:.1f} {:.1f}\n'.format(
                        pid,
                        part_spec['mass'][pi],
                        part_spec.prop('host.distance', pi)[0],
                        part_spec.prop('host.distance', pi)[1],
                        part_spec.prop('host.distance', pi)[2],
                        part_spec.prop('host.velocity', pi)[0],
                        part_spec.prop('host.velocity', pi)[1],
                        part_spec.prop('host.velocity', pi)[2],
                    )
                )

        species_name = 'gas'
        file_name = 'snapshot_{}_{}.txt'.format(part.snapshot['index'], species_name)
        part_spec = part[species_name]

        with open(file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(
                '# id mass[M_sun] distance_wrt_host(x,y,z)[kpc] velocity_wrt_host(x,y,z)[km/s]'
                + ' density[M_sun/kpc^3] temperature[K]\n'
            )

            for pi, pid in enumerate(part_spec['id']):
                file_out.write(
                    '{} {:.3e} {:.3f} {:.3f} {:.3f} {:.1f} {:.1f} {:.1f} {:.2e} {:.2e}\n'.format(
                        pid,
                        part_spec['mass'][pi],
                        part_spec.prop('host.distance', pi)[0],
                        part_spec.prop('host.distance', pi)[1],
                        part_spec.prop('host.distance', pi)[2],
                        part_spec.prop('host.velocity', pi)[0],
                        part_spec.prop('host.velocity', pi)[1],
                        part_spec.prop('host.velocity', pi)[2],
                        part_spec['density'][pi],
                        part_spec['temperature'][pi],
                    )
                )

        species_name = 'star'
        file_name = 'snapshot_{}_{}.txt'.format(part.snapshot['index'], species_name)
        part_spec = part[species_name]

        with open(file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(
                '# id mass[M_sun] distance_wrt_host(x,y,z)[kpc] velocity_wrt_host(x,y,z)[km/s]'
                + ' age[Gyr]\n'
            )

            for pi, pid in enumerate(part_spec['id']):
                file_out.write(
                    '{} {:.3e} {:.3f} {:.3f} {:.3f} {:.1f} {:.1f} {:.1f} {:.3f}\n'.format(
                        pid,
                        part_spec['mass'][pi],
                        part_spec.prop('host.distance', pi)[0],
                        part_spec.prop('host.distance', pi)[1],
                        part_spec.prop('host.distance', pi)[2],
                        part_spec.prop('host.velocity', pi)[0],
                        part_spec.prop('host.velocity', pi)[1],
                        part_spec.prop('host.velocity', pi)[2],
                        part_spec.prop('age', pi),
                    )
                )
