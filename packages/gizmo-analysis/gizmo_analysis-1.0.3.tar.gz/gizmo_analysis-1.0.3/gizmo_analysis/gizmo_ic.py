#!/usr/bin/env python3

'''
Generate file of positions for zoom-in initial conditions by selecting particles at a final snapshot
and tracking them back to an initial snapshot.

@author: Andrew Wetzel

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
'''

import sys
import numpy as np
from scipy import spatial

import utilities as ut
from . import gizmo_default


# --------------------------------------------------------------------------------------------------
# generate zoom-in region for initial conditions
# --------------------------------------------------------------------------------------------------
class InitialConditionClass(ut.io.SayClass):
    '''
    Read particles from a final and an initial snapshot, and a halo catalog at the final snapshot.
    Generate text file of positions at the initial snapshot that are within the selection region at
    the final snapshot.
    '''

    def __init__(
        self, snapshot_redshifts=[0, 99], simulation_directory=gizmo_default.simulation_directory
    ):
        '''
        Parameters
        ----------
        snapshot_redshifts : list
            redshifts of initial and final snapshots
        simulation_directory : str
            base directory of simulation
        '''
        # ensure lowest-redshift snapshot is first
        self.snapshot_redshifts = np.sort(snapshot_redshifts)
        self.simulation_directory = ut.io.get_path(simulation_directory)

    def write_positions_at_initial_snapshot(
        self,
        parts=None,
        host_index=0,
        hal=None,
        hal_index=None,
        distance_max=8,
        scale_to_halo_radius=True,
        virial_kind='200m',
        region_kind='convex-hull',
        dark_mass=None,
    ):
        '''
        Select dark-matter particles at the final snapshot, write a file of their positions at
        the initial snapshot.

        If input a halo catalog (hal) and halo index (hal_index) (typically from a
        uniform-resolution DM-only simulation), select volume around that halo.

        Else, assume that working from an existing zoom-in simulation, re-select spherical volume
        around its host center.

        If you do not supply particle catalogs (parts), read them at the fiducial snapshots.

        Rule of thumb from Onorbe et al:
            given distance_pure, if region_kind in ['particles', 'convex-hull']:
                distance_max = (1.5 * refinement_number + 7) * distance_pure

        Parameters
        ----------
        parts : list of dicts
            catalogs of particles at final and initial snapshots
        host_index : int
            index of primary host halo in the particle catalog to use to get position and radius
            (if not input halo catalog)
        hal : dict
            catalog of halos at the final snapshot
        hal_index : int
            index of primary host halo
        distance_max : float
            distance from center to select particles at the final snapshot
            [kpc physical, or in units of R_halo]
        scale_to_halo_radius : bool
            whether to scale distance to halo radius
        virial_kind : str
            virial overdensity to define halo radius
        region_kind : str
            method to identify zoom-in regon at initial time: 'particles', 'convex-hull', 'cube'
        dark_mass : float
            DM particle mass (if simulation has only DM, at single resolution)
        '''

        file_name = 'ic_LX_mX_rad{:.1f}_points.txt'.format(distance_max)

        if scale_to_halo_radius:
            assert distance_max > 1 and distance_max < 30

        assert region_kind in ['particles', 'convex-hull', 'cube']

        if parts is None or len(parts) == 0:
            parts = self.read_particles()

        # ensure final catalog is at lowest redshift
        part_fin, part_ini = parts
        if part_fin.snapshot['redshift'] > part_ini.snapshot['redshift']:
            part_fin, part_ini = part_ini, part_fin

        # determine which species are in catalog
        species_names = ['dark', 'dark2', 'dark3', 'dark4', 'dark5', 'dark6']
        for spec_name in list(species_names):
            if spec_name not in part_fin:
                species_names.remove(spec_name)
                continue

            # sanity check
            if 'id.to.index' not in part_ini[spec_name]:
                if np.min(part_fin[spec_name]['id'] == part_ini[spec_name]['id']) is False:
                    self.say(f'! species = {spec_name}: ids not match in final v initial catalogs')
                    return

        # sanity check
        if dark_mass:
            if species_names != ['dark']:
                raise ValueError(
                    'input dark_mass = {:.3e} Msun, but catalog contains species = {}'.format(
                        dark_mass, species_names
                    )
                )

        self.say(f'using species: {species_names}')

        if hal is None or len(hal) == 0 or hal_index is None:
            # no input halo to use, so assume that this is an existing zoom-in simulation
            # find primary host halo center position and radius
            center_position = ut.particle.get_center_positions(
                part_fin, 'dark', center_number=host_index + 1, return_single_array=False
            )[host_index]

            halo_prop = ut.particle.get_halo_properties(
                part_fin, 'all', virial_kind, center_position=center_position
            )
            halo_radius = halo_prop['radius']

        else:
            center_position = hal['position'][hal_index]
            halo_radius = hal['radius'][hal_index]

        if scale_to_halo_radius:
            distance_max *= halo_radius

        mass_select = 0
        positions_ini = []
        spec_select_number = []
        for spec_name in species_names:
            distances = ut.coordinate.get_distances(
                part_fin[spec_name]['position'],
                center_position,
                part_fin.info['box.length'],
                part_fin.snapshot['scalefactor'],
                total_distance=True,
            )  # [kpc physical]

            indices_fin = ut.array.get_indices(distances, [0, distance_max])

            # if id-to-index array is in species dictionary
            # assume id not sorted, so have to convert between id and index
            if 'id.to.index' in part_ini[spec_name]:
                ids = part_fin[spec_name]['id'][indices_fin]
                indices_ini = part_ini[spec_name]['id.to.index'][ids]
            else:
                indices_ini = indices_fin

            positions_ini.extend(part_ini[spec_name]['position'][indices_ini])

            if 'mass' in part_ini[spec_name]:
                mass_select += part_ini[spec_name]['mass'][indices_ini].sum()
            elif dark_mass:
                mass_select += dark_mass * indices_ini.size
            else:
                raise ValueError(f'no mass for species = {spec_name} but also no input dark_mass')

            spec_select_number.append(indices_ini.size)

        positions_ini = np.array(positions_ini)
        poss_ini_limits = np.array(
            [
                [positions_ini[:, dimen_i].min(), positions_ini[:, dimen_i].max()]
                for dimen_i in range(positions_ini.shape[1])
            ]
        )

        # properties of initial volume
        density_ini = part_ini.Cosmology.get_density(
            'matter', part_ini.snapshot['redshift'], 'kpc comoving'
        )
        if part_ini.info['has.baryons']:
            # remove baryonic mass
            density_ini *= part_ini.Cosmology['omega_dm'] / part_ini.Cosmology['omega_matter']

        # convex hull
        volume_ini_chull = ut.coordinate.get_volume_of_convex_hull(positions_ini)
        mass_ini_chull = volume_ini_chull * density_ini  # assume cosmic density within volume

        # get encompassing cube (relevant for MUSIC FFT) and cuboid
        position_difs = []
        for dimen_i in range(positions_ini.shape[1]):
            position_difs.append(poss_ini_limits[dimen_i].max() - poss_ini_limits[dimen_i].min())
        volume_ini_cube = max(position_difs) ** 3
        mass_ini_cube = volume_ini_cube * density_ini  # assume cosmic density within volume

        volume_ini_cuboid = 1.0
        for dimen_i in range(positions_ini.shape[1]):
            volume_ini_cuboid *= position_difs[dimen_i]
        mass_ini_cuboid = volume_ini_cuboid * density_ini  # assume cosmic density within volume

        # MUSIC does not support header information in points file, so put in separate log file
        log_file_name = file_name.replace('.txt', '_log.txt')

        with open(log_file_name, 'w', encoding='utf-8') as file_out:
            Write = ut.io.WriteClass(file_out, print_stdout=True)

            Write.write(
                '# redshift: final = {:.3f}, initial = {:.3f}'.format(
                    part_fin.snapshot['redshift'], part_ini.snapshot['redshift']
                )
            )
            Write.write(
                '# center of region at final time = [{:.3f}, {:.3f}, {:.3f}] kpc comoving'.format(
                    center_position[0], center_position[1], center_position[2]
                )
            )
            Write.write(
                '# radius of selection region at final time = {:.3f} kpc physical'.format(
                    distance_max
                )
            )
            if scale_to_halo_radius:
                Write.write(
                    '  = {:.2f} x R_{}, R_{} = {:.2f} kpc physical'.format(
                        distance_max / halo_radius, virial_kind, virial_kind, halo_radius
                    )
                )
            Write.write(
                '# number of particles in selection region at final time = {}'.format(
                    np.sum(spec_select_number)
                )
            )
            for spec_i, spec_name in enumerate(species_names):
                Write.write(
                    '  species {:6}: number = {}'.format(spec_name, spec_select_number[spec_i])
                )
            Write.write('# mass from all dark-matter particles:')
            if 'mass' in part_ini['dark']:
                mass_dark_all = part_ini['dark']['mass'].sum()
            else:
                mass_dark_all = dark_mass * part_ini['dark']['id'].size
            Write.write('  at highest-resolution = {:.2e} M_sun'.format(mass_dark_all))
            Write.write('  in selection region at final time = {:.2e} M_sun'.format(mass_select))

            Write.write('# within convex hull at initial time')
            Write.write('  mass = {:.2e} M_sun'.format(mass_ini_chull))
            Write.write(
                '  volume = {:.1f} Mpc^3 comoving'.format(
                    volume_ini_chull * ut.constant.mega_per_kilo**3
                )
            )

            Write.write('# within encompassing cuboid at initial time')
            Write.write('  mass = {:.2e} M_sun'.format(mass_ini_cuboid))
            Write.write(
                '  volume = {:.1f} Mpc^3 comoving'.format(
                    volume_ini_cuboid * ut.constant.mega_per_kilo**3
                )
            )

            Write.write('# within encompassing cube at initial time (for MUSIC FFT)')
            Write.write('  mass = {:.2e} M_sun'.format(mass_ini_cube))
            Write.write(
                '  volume = {:.1f} Mpc^3 comoving'.format(
                    volume_ini_cube * ut.constant.mega_per_kilo**3
                )
            )

            Write.write('# position range at initial time')
            for dimen_i in range(positions_ini.shape[1]):
                string = (
                    '  {} [min, max, width] = [{:.2f}, {:.2f}, {:.2f}] kpc comoving\n'
                    + '        [{:.9f}, {:.9f}, {:.9f}] box units'
                )
                pos_min = np.min(poss_ini_limits[dimen_i])
                pos_max = np.max(poss_ini_limits[dimen_i])
                pos_width = np.max(poss_ini_limits[dimen_i]) - np.min(poss_ini_limits[dimen_i])
                Write.write(
                    string.format(
                        dimen_i,
                        pos_min,
                        pos_max,
                        pos_width,
                        pos_min / part_ini.info['box.length'],
                        pos_max / part_ini.info['box.length'],
                        pos_width / part_ini.info['box.length'],
                    )
                )

            positions_ini /= part_ini.info['box.length']  # renormalize to box units

            if region_kind == 'convex-hull':
                # use convex hull to define initial region to reduce memory
                ConvexHull = spatial.ConvexHull(positions_ini)  # pylint: disable=no-member
                positions_ini = positions_ini[ConvexHull.vertices]
                Write.write(
                    f'# using convex hull with {positions_ini.shape[0]} vertices for initial volume'
                )

        with open(file_name, 'w', encoding='utf-8') as file_out:
            for pi in range(positions_ini.shape[0]):
                file_out.write(
                    '{:.8f} {:.8f} {:.8f}\n'.format(
                        positions_ini[pi, 0], positions_ini[pi, 1], positions_ini[pi, 2]
                    )
                )

    def read_halos_and_particles(self, mass_limits=[1e11, np.inf]):
        '''
        Read halos at the final snapshot and particles at the final and the initial snapshot.

        Parameters
        ----------
        mass_limits : list
            min and max halo mass to assign low-res DM mass

        Returns
        -------
        hal : dictionary class
            catalog of halos at final snapshot
        parts : list of dictionaries
            catalogs of particles at initial and final snapshots
        '''
        from halo_analysis import halo_io

        hal = self.read_halos(mass_limits)
        parts = self.read_particles()

        if (
            'dark2' in parts[0]
            and 'mass' in parts[0]['dark2']
            and len(parts[0]['dark2']['mass']) > 0
        ):
            Particle = halo_io.ParticleClass()
            Particle.assign_lowres_mass(hal, parts[0])

        return hal, parts

    def read_halos(
        self, mass_limits=[1e11, np.inf], file_kind='hdf5', assign_nearest_neighbor=True
    ):
        '''
        Read catalog of halos at the final snapshot.

        Parameters
        ----------
        mass_limits : list
            min and max halo mass to assign low-res DM mass
        file_kind : str
            kind of halo file: 'hdf5', 'out', 'ascii', 'hlist'
        assign_nearest_neighbor : bool
            whether to assign nearest neighboring halo

        Returns
        -------
        hal : dictionary class
            catalog of halos at the final snapshot
        '''
        from halo_analysis import halo_io

        hal = halo_io.IO.read_catalogs(
            'redshift', self.snapshot_redshifts[0], self.simulation_directory, file_kind=file_kind
        )

        if assign_nearest_neighbor:
            # assign nearest neighbor that is more massive
            halo_io.IO.assign_nearest_neighbor(
                hal, 'mass', mass_limits, [1, np.inf], 3000, 'Rneig', 10000
            )

        return hal

    def read_particles(self, properties=['position', 'mass', 'id'], sort_dark_by_id=True):
        '''
        Read particles at the final and the initial snapshot.

        Parameters
        ----------
        properties : str or list
            name[s] of particle properties to read
        sort_dark_by_id : bool
            whether to sort dark-matter particles by id

        Returns
        -------
        parts : list
            catalogs of particles at initial and final snapshots
        '''
        from . import gizmo_io

        snapshot_redshifts = np.sort(self.snapshot_redshifts)

        Read = gizmo_io.ReadClass()

        parts = []

        for snapshot_redshift in snapshot_redshifts:
            part = Read.read_snapshots(
                'all',
                'redshift',
                snapshot_redshift,
                self.simulation_directory,
                properties=properties,
                assign_hosts=False,
                sort_dark_by_id=sort_dark_by_id,
            )

            # if not sort dark particles, assign id-to-index coversion to track across snapshots
            if not sort_dark_by_id and snapshot_redshift == self.snapshot_redshifts[-1]:
                for spec_name in part:
                    self.say(f'assigning id-to-index to species: {spec_name}')
                    ut.catalog.assign_id_to_index(part[spec_name])

            parts.append(part)

        return parts


# --------------------------------------------------------------------------------------------------
# run from command line
# --------------------------------------------------------------------------------------------------
def main():
    '''.'''
    if len(sys.argv) <= 1:
        raise OSError('must specify selection radius, in terms of R_200m')

    distance_max = float(sys.argv[1])

    InitialCondition = InitialConditionClass()
    InitialCondition.write_positions_at_initial_snapshot(distance_max=distance_max)


if __name__ == '__main__':
    main()
