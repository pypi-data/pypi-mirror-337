#!/usr/bin/env python3

'''
Diagnose Gizmo simulations.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

import collections
import sys
import glob
import numpy as np

import utilities as ut
from . import gizmo_default
from . import gizmo_io
from . import gizmo_plot


class RuntimeClass(ut.io.SayClass):
    '''
    .
    '''

    def __init__(self):
        # dictionary of cluster name and (default) number of cores per node
        self.machine = {
            'frontera': 56,
            'stampede3': 48,
            'stampede2': 48,
            'bridges2': 64,
            'pleiades': 20,
            'pfe': 20,
            'peloton': 32,
        }

    def get_cpu_numbers(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        gizmo_out_file_name=gizmo_default.gizmo_out_file_name,
    ):
        '''
        Get number of MPI tasks and OpenMP threads from run-time file.
        If cannot find any, default to 1.

        Parameters
        ----------
        simulation_directory : str
            top-level directory of simulation
        gizmo_out_file_name : str
            name of Gizmo run-time file

        Returns
        -------
        mpi_number : int
            number of MPI tasks
        omp_number : int
            number of OpenMP threads per MPI task
        machine_name : string
            name of machine run on
        '''
        line_number_max = 100

        file_name = ut.io.get_path(simulation_directory) + gizmo_out_file_name
        path_file_names = glob.glob(file_name)
        file_read = open(path_file_names[0], 'r', encoding='utf-8')

        mpi_number = None
        omp_number = None
        machine_name = None

        for line_i, line in enumerate(file_read):
            if mpi_number is None and 'MPI tasks' in line:
                mpi_number = int(line.split()[2])
            elif omp_number is None and 'OpenMP threads' in line:
                omp_number = int(line.split()[1])
            elif machine_name is None and 'Build on' in line:
                for m in self.machine:
                    if m in line:
                        machine_name = m
                        if machine_name == 'pfe':
                            machine_name = 'pleiades'
                        break

            if mpi_number and omp_number and machine_name:
                break
            elif line_i > line_number_max:
                break

        if mpi_number:
            self.say(f'* MPI tasks = {mpi_number}')
        else:
            self.say('! unable to read number of MPI tasks')
            mpi_number = 1

        if omp_number:
            self.say(f'* OpenMP threads = {omp_number}')
        else:
            self.say('* did not read any OpenMP threads')
            omp_number = 1

        if machine_name:
            self.say(f'* machine name = {machine_name}')
        else:
            self.say('* unable to read machine name')

        return mpi_number, omp_number, machine_name

    def _get_scalefactor_string(self, scalefactor):
        if scalefactor == 1:
            scalefactor_string = '1'
        elif (10 * scalefactor) % 1 < 0.1:
            scalefactor_string = '{:.1f}'.format(scalefactor)
        elif (100 * scalefactor % 1) < 0.1:
            scalefactor_string = '{:.2f}'.format(scalefactor)
        elif (1000 * scalefactor % 1) < 0.1:
            scalefactor_string = '{:.3f}'.format(scalefactor)
        else:
            scalefactor_string = '{:.4f}'.format(scalefactor)
        return scalefactor_string

    def print_run_times(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        gizmo_out_file_name=gizmo_default.gizmo_out_file_name,
        gizmo_cpu_file_name=gizmo_default.gizmo_cpu_file_name,
        core_number=None,
        wall_time_restart=0,
        scalefactors=None,
    ):
        '''
        Print wall [and CPU] times (based on average per MPI task from cpu.txt) at scale-factors,
        for Gizmo simulation.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of snapshot files and Gizmo output files
        gizmo_out_file_name : str
            name of Gizmo run-time file
        gizmo_cpu_file_name : str
            name of Gizmo timing file
        core_number : int
            total number of CPU cores (input instead of reading from run-time file)
        wall_time_restart : float
            wall time [sec] of previous run (if restarted from snapshot)
        scalefactors : array-like
            list of scale-factors at which to print run times

        Returns
        -------
        scalefactors, redshifts, wall_times, cpu_times : arrays
        '''
        if scalefactors is None or len(scalefactors) == 0:
            scalefactors = [
                0.2,
                0.25,
                0.3,
                0.35,
                0.4,
                0.45,
                0.5,
                0.55,
                0.6,
                0.65,
                0.7,
                0.8,
                0.9,
                0.999,
                1.0,
            ]

        path_file_name = (
            ut.io.get_path(simulation_directory)
            + ut.io.get_path(snapshot_directory)
            + gizmo_cpu_file_name
        )
        file_read = open(path_file_name, 'r', encoding='utf-8')

        wall_times = []

        i = 0
        scalefactor = f'Time: {self._get_scalefactor_string(scalefactors[i])}'
        print_next_line = False

        for line in file_read:
            if print_next_line and 'total' in line:
                wall_times.append(float(line.split()[1]))
                print_next_line = False
                i += 1
                if i >= len(scalefactors):
                    break
                else:
                    scalefactor = f'Time: {self._get_scalefactor_string(scalefactors[i])}'
            elif scalefactor in line:
                print_next_line = True

        wall_times = np.array(wall_times)

        if wall_time_restart and len(wall_times) > 1:
            for i in range(1, len(wall_times)):
                if wall_times[i] < wall_times[i - 1]:
                    break
            wall_times[i:] += wall_time_restart

        wall_times /= 3600  # convert to [hr]

        if not core_number:
            # get core number from run-time file
            mpi_number, omp_number, machine_name = self.get_cpu_numbers(
                simulation_directory, gizmo_out_file_name
            )
            core_number = mpi_number * omp_number
            print_string = f'# core = {core_number} (mpi = {mpi_number}, omp = {omp_number})'
            if machine_name is not None:
                node_number = int(round(core_number / self.machine[machine_name]))
                print_string = f'{machine_name}\n' + print_string + f', node = {node_number}'
            print(print_string)
        else:
            print(f'# core = {core_number}')

        cpu_times = wall_times * core_number

        # sanity check - simulation might not have run to all input scale-factors
        scalefactors = ut.array.arrayize(scalefactors)
        scalefactors = scalefactors[: wall_times.size]
        redshifts = 1 / scalefactors - 1

        print('# scale-factor redshift wall-time[day] cpu-time[khr] run-time-percent')
        for t_i, wall_time in enumerate(wall_times):
            print(
                '{:.2f} {:5.2f} | {:6.2f}  {:7.1f}  {:3.0f}%'.format(
                    scalefactors[t_i],
                    redshifts[t_i],
                    wall_time / 24,
                    cpu_times[t_i] / 1000,
                    100 * wall_time / wall_times.max(),
                )
            )

        return scalefactors, redshifts, wall_times, cpu_times

    def print_run_times_ratios(
        self,
        simulation_directories=[gizmo_default.simulation_directory],
        snapshot_directory=gizmo_default.snapshot_directory,
        gizmo_out_file_name=gizmo_default.gizmo_out_file_name,
        gizmo_cpu_file_name=gizmo_default.gizmo_cpu_file_name,
        wall_times_restart=None,
        scalefactors=[
            0.2,
            0.25,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.55,
            0.6,
            0.65,
            0.7,
            0.75,
            0.8,
            0.9,
            1.0,
        ],
    ):
        '''
        Print ratios of wall times and CPU times (based on average per MPI taks from cpu.txt) at
        scale-factors, from different simulation directories, for Gizmo simulations.
        'reference' simulation is first in list.

        Parameters
        ----------
        simulation_directories : str or list
            top-level directory[s] of simulation[s]
        snapshot_directory : str
            directory of snapshot files and Gizmo output files
        gizmo_out_file_name : str
            name of Gizmo run-time file
        wall_times_restart : float or list
            wall time[s] [sec] of previous run[s] (if restart from snapshot)
        scalefactors : array-like
            list of scale-factors at which to print run times
        '''
        wall_timess = []
        cpu_timess = []

        if np.isscalar(simulation_directories):
            simulation_directories = [simulation_directories]

        if not wall_times_restart:
            wall_times_restart = np.zeros(len(simulation_directories))
        elif np.isscalar(wall_times_restart):
            wall_times_restart = [wall_times_restart]

        for d_i, simulation_directory in enumerate(simulation_directories):
            scalefactors, redshifts, wall_times, cpu_times = self.print_run_times(
                simulation_directory,
                snapshot_directory,
                gizmo_out_file_name,
                gizmo_cpu_file_name,
                None,
                wall_times_restart[d_i],
                scalefactors,
            )
            wall_timess.append(wall_times)
            cpu_timess.append(cpu_times)

        snapshot_number_min = np.inf
        for d_i, wall_times in enumerate(wall_timess):
            if len(wall_times) < snapshot_number_min:
                snapshot_number_min = len(wall_times)

        # sanity check - simulations might not have run to each input scale-factor
        scalefactors = scalefactors[:snapshot_number_min]
        redshifts = redshifts[:snapshot_number_min]

        print('# scale-factor redshift', end='')
        for _ in range(1, len(wall_timess)):
            print(' wall-time-ratio cpu-time-ratio', end='')
        print()

        for a_i in range(snapshot_number_min):
            print('{:.2f} {:5.2f} |'.format(scalefactors[a_i], redshifts[a_i]), end='')
            for d_i in range(1, len(wall_timess)):
                print(' {:5.1f}'.format(wall_timess[d_i][a_i] / wall_timess[0][a_i]), end='')
                print(' {:5.1f}'.format(cpu_timess[d_i][a_i] / cpu_timess[0][a_i]), end='')
            print()


class ContaminationClass(ut.io.SayClass):
    '''
    Diagnose contamination by low-resolution dark matter.
    '''

    def print_plot_contamination_v_distance_both(
        self,
        snapshot_value_kind='redshift',
        snapshot_value=0,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        track_directory=gizmo_default.track_directory,
        virial_kind='200m',
        verbose=False,
        plot_file_name=None,
    ):
        '''
        Print [and plot] contamination from low-resolution dark-matter particles around halo/galaxy
        as a function of distance.

        Parameters
        ----------
        snapshot_value_kind : str
            snapshot number kind: 'index', 'redshift', 'scalefactor'
        snapshot_value : int or float
            index (number) of snapshot file
        simulation_directory : str
            directory of simulation
        snapshot_directory: str
            directory of snapshot files within simulation_directory
        track_directory : str
            directory of files for particle pointers, formation coordinates, and host coordinates
        virial_kind : str
            virial overdensity to set halo radius
        verbose : bool
            verbosity flag
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        '''
        distance_limits_phys = [10, 3000]  # [kpc physical]
        distance_limits_halo = [0.01, 8]  # [units of R_halo]
        distance_bin_width = 0.003  # log bins by default

        Read = gizmo_io.ReadClass()
        part = Read.read_snapshots(
            ['star', 'dark', 'dark2'],
            snapshot_value_kind,
            snapshot_value,
            simulation_directory,
            snapshot_directory,
            track_directory,
            properties=['position', 'mass'],
            assign_hosts=True,
        )

        halo_prop = ut.particle.get_halo_properties(part, 'all', virial_kind)

        self.print_plot_contamination_v_distance(
            part,
            distance_limits_phys,
            distance_bin_width,
            halo_radius=halo_prop['radius'],
            scale_to_halo_radius=False,
            virial_kind=virial_kind,
            verbose=verbose,
            plot_file_name=plot_file_name,
            directory='plot',
        )

        self.print_plot_contamination_v_distance(
            part,
            distance_limits_halo,
            distance_bin_width,
            halo_radius=halo_prop['radius'],
            scale_to_halo_radius=True,
            virial_kind=virial_kind,
            verbose=verbose,
            plot_file_name=plot_file_name,
            directory='plot',
        )

    def print_plot_contamination_v_distance(
        self,
        part,
        distance_limits=[10, 3000],
        distance_bin_width=0.005,
        distance_log_scale=True,
        halo_radius=None,
        scale_to_halo_radius=False,
        virial_kind='200m',
        center_position=None,
        host_index=0,
        axis_y_limits=[0.0001, 1],
        axis_y_log_scale=True,
        verbose=False,
        plot_file_name=None,
        directory='.',
        figure_index=1,
    ):
        '''
        Print [and plot] contamination from low-resolution particles v distance from center.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        distance_limits : list
            min and max limits for distance from galaxy
        distance_bin_width : float
            width of each distance bin (in units of distance_scaling)
        distance_log_scale : bool
            whether to use log scaling for distance bins
        halo_radius : float
            radius of halo [kpc physical]
        scale_to_halo_radius : bool
            whether to scale distance to halo_radius
        virial_kind : str
            virial overdensity to set halo radius
        center_position : array
            position of galaxy/halo center
        host_index : int
            index of host halo to get position of (if not input center_position)
        axis_y_limits : list
            min and max limits for y axis
        axis_y_log_scale : bool
            whether to use logarithmic scaling for y axis
        verbose : bool
            verbosity flag
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        directory : str
            directory in which to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

        if halo_radius is None or halo_radius <= 0:
            halo_prop = ut.particle.get_halo_properties(part, 'all', virial_kind)
            halo_radius = halo_prop['radius']

        DistanceBin = ut.binning.DistanceBinClass(
            distance_limits, distance_bin_width, log_scale=distance_log_scale
        )

        profile_mass = collections.OrderedDict()
        profile_mass['total'] = {}
        for spec_name in part:
            profile_mass[spec_name] = {}

        profile_mass_frac = {}
        profile_number = {}

        for spec_name in part:
            distances = ut.coordinate.get_distances(
                part[spec_name]['position'],
                center_position,
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )  # [kpc physical]
            if scale_to_halo_radius:
                distances /= halo_radius
            profile_mass[spec_name] = DistanceBin.get_sum_profile(
                distances, part[spec_name]['mass'], verbose=False
            )

        # initialize total mass
        for prop_name in profile_mass[spec_name]:
            if 'distance' not in prop_name:
                profile_mass['total'][prop_name] = 0
            else:
                profile_mass['total'][prop_name] = profile_mass[spec_name][prop_name]

        # compute mass fractions relative to total mass
        for spec_name in part:
            for prop_name in profile_mass[spec_name]:
                if 'distance' not in prop_name:
                    profile_mass['total'][prop_name] += profile_mass[spec_name][prop_name]

        for spec_name in part:
            profile_mass_frac[spec_name] = {
                'sum': profile_mass[spec_name]['sum'] / profile_mass['total']['sum'],
                'sum.cum': profile_mass[spec_name]['sum.cum'] / profile_mass['total']['sum.cum'],
            }
            profile_number[spec_name] = {
                'sum': np.int64(
                    np.round(profile_mass[spec_name]['sum'] / part[spec_name]['mass'].min())
                ),
                'sum.cum': np.int64(
                    np.round(profile_mass[spec_name]['sum.cum'] / part[spec_name]['mass'].min())
                ),
            }

        # print diagnostics
        if scale_to_halo_radius:
            distances_halo = profile_mass['dark2']['distance.cum']
            distances_phys = distances_halo * halo_radius
        else:
            distances_phys = profile_mass['dark2']['distance.cum']
            distances_halo = distances_phys / halo_radius

        species_lowres_dark = []
        for i in range(2, 10):
            dark_name = f'dark{i}'
            if dark_name in part:
                species_lowres_dark.append(dark_name)

        if verbose:
            for spec_name in species_lowres_dark:
                self.say(f'* {spec_name}')
                if profile_mass[spec_name]['sum.cum'][-1] == 0:
                    self.say('  none. yay!')
                    continue

                if scale_to_halo_radius:
                    print_string = 'd/R_halo < {:5.2f}, d < {:6.2f} kpc: '
                else:
                    print_string = 'd < {:6.1f} kpc, d/R_halo < {:5.2f}: '
                print_string += 'mass_frac = {:.4f}, mass = {:.2e}, number = {:.0f}'

                for dist_i in range(profile_mass[spec_name]['sum.cum'].size):
                    if profile_mass[spec_name]['sum.cum'][dist_i] > 0:
                        if scale_to_halo_radius:
                            distances_0 = distances_halo[dist_i]
                            distances_1 = distances_phys[dist_i]
                        else:
                            distances_0 = distances_phys[dist_i]
                            distances_1 = distances_halo[dist_i]

                        self.say(
                            print_string.format(
                                distances_0,
                                distances_1,
                                profile_mass_frac[spec_name]['sum.cum'][dist_i],
                                profile_mass[spec_name]['sum.cum'][dist_i],
                                profile_number[spec_name]['sum.cum'][dist_i],
                            )
                        )

                        if spec_name != 'dark2':
                            # print only 1 distance bin for lower-resolution particles
                            break

        distance_max = max(distance_limits)
        print()
        print('contamination')
        species = 'dark2'
        dist_i_halo = np.searchsorted(distances_phys, halo_radius)
        if profile_number[species]['sum.cum'][dist_i_halo] > 0:
            print(
                '* {} {} particles within R_{}'.format(
                    profile_number[species]['sum.cum'][dist_i_halo], species, virial_kind
                )
            )
        else:
            print(f'* no {species} particles within R_{virial_kind}')

        masks = profile_number[species]['sum.cum'] > 0
        if np.max(masks):
            dist_i = np.where(masks)[0][0]
            print(
                '* {} closest d = {:.0f} kpc, {:.1f} R_{}'.format(
                    species, distances_phys[dist_i], distances_halo[dist_i], virial_kind
                )
            )
        else:
            print(f'* no {species} particles within distance_max = {distance_max} kpc')

        masks = profile_mass_frac[species]['sum.cum'] > 0.0001
        if np.max(masks):
            dist_i = np.where(masks)[0][0]
            print(
                '* {} mass fraction(< d) = 0.01% at d < {:.0f} kpc, {:.1f} R_{}'.format(
                    species, distances_phys[dist_i], distances_halo[dist_i], virial_kind
                )
            )
        else:
            print(f'* {species} mass fraction(< d) < 0.01% at all d < {distance_max} kpc')

        masks = profile_mass_frac[species]['sum.cum'] > 0.001
        if np.max(masks):
            dist_i = np.where(masks)[0][0]
            print(
                '* {} mass fraction(< d) =  0.1% at d < {:.0f} kpc, {:.1f} R_{}'.format(
                    species, distances_phys[dist_i], distances_halo[dist_i], virial_kind
                )
            )
        else:
            print(f'* {species} mass fraction(< d) <  0.1% at all d < {distance_max} kpc')

        masks = profile_mass_frac[species]['sum.cum'] > 0.01
        if np.max(masks):
            dist_i = np.where(masks)[0][0]
            print(
                '* {} mass fraction(< d) =    1% at d < {:.0f} kpc, {:.1f} R_{}'.format(
                    species, distances_phys[dist_i], distances_halo[dist_i], virial_kind
                )
            )
        else:
            print(f'* {species} mass fraction(< d) <    1% at all d < {distance_max} kpc')

        for spec_name in species_lowres_dark:
            if species != 'dark2' and profile_number[spec_name]['sum.cum'][dist_i_halo] > 0:
                print(
                    '! {} {} particles within R_{}'.format(
                        profile_number[species]['sum.cum'][dist_i_halo], species, virial_kind
                    )
                )
                masks = profile_number[spec_name]['sum.cum'] > 0
                if np.max(masks):
                    dist_i = np.where(masks)[0][0]
                    print(
                        '! {} closest d = {:.0f} kpc, {:.1f} R_{}'.format(
                            species, distances_phys[dist_i], distances_halo[dist_i], virial_kind
                        )
                    )

        if not plot_file_name:
            return

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        ut.plot.set_axes_scaling_limits(
            subplot, distance_log_scale, distance_limits, None, axis_y_log_scale, axis_y_limits
        )

        subplot.set_ylabel('$M_{{\\rm species}} / M_{{\\rm total}}$')
        if scale_to_halo_radius:
            axis_x_label = f'$d \\, / \\, R_{{\\rm {virial_kind}}}$'
        else:
            axis_x_label = 'distance $[\\rm kpc]$'
        subplot.set_xlabel(axis_x_label)

        colors = ut.plot.get_colors(len(species_lowres_dark), use_black=False)

        if scale_to_halo_radius:
            x_ref = 1
        else:
            x_ref = halo_radius
        subplot.plot([x_ref, x_ref], [1e-6, 1e6], color='black', linestyle=':', alpha=0.6)

        for spec_i, spec_name in enumerate(species_lowres_dark):
            subplot.plot(
                DistanceBin.mids,
                profile_mass_frac[spec_name]['sum'],
                color=colors[spec_i],
                alpha=0.7,
                label=spec_name,
            )

        ut.plot.make_legends(subplot, 'best')

        if plot_file_name is True or plot_file_name == '':
            distance_name = 'dist'
            if scale_to_halo_radius:
                distance_name += '.' + virial_kind
            plot_file_name = ut.plot.get_file_name(
                'mass.frac', distance_name, snapshot_dict=part.snapshot
            )
        ut.plot.parse_output(plot_file_name, directory)


def print_galaxy_properties(
    part=None,
    species='star',
    snapshot_value_kind='redshift',
    snapshot_value=0,
    simulation_directory=gizmo_default.simulation_directory,
    snapshot_directory=gizmo_default.snapshot_directory,
    track_directory=gizmo_default.track_directory,
):
    '''
    Print properties of galaxy at input snapshot.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species : str
        name of particle species to get properties of
    snapshot_value_kind : str
        snapshot number kind: 'index', 'redshift', 'scalefactor'
    snapshot_value : int or float
        index (number) of snapshot file
    simulation_directory : str
        directory of simulation
    snapshot_directory: str
        directory of snapshot files within simulation_directory
    track_directory : str
        directory of files for particle pointers, formation coordinates, and host coordinates
    '''

    if part is None:
        Read = gizmo_io.ReadClass()
        part = Read.read_snapshots(
            species,
            snapshot_value_kind,
            snapshot_value,
            simulation_directory,
            snapshot_directory,
            track_directory,
            assign_hosts_rotation=True,
        )

    redshift = ut.io.get_string_from_numbers(part.snapshot['redshift'], digits=1, strip=True)
    print(f'properties at z = {redshift}')

    _ = ut.particle.get_halo_properties(part, 'all', verbose=1)
    _ = ut.particle.get_galaxy_properties(part, axis_kind='both', verbose=1)


def print_particle_properties_statistics(
    species='all',
    snapshot_value_kind='redshift',
    snapshot_value=0,
    simulation_directory=gizmo_default.simulation_directory,
    snapshot_directory=gizmo_default.snapshot_directory,
    track_directory=gizmo_default.track_directory,
):
    '''
    For each property of each species in particle catalog, print range and median.

    Parameters
    ----------
    species : str or list
        name[s] of particle species to print
    snapshot_value_kind : str
        snapshot number kind: 'index', 'redshift', 'scalefactor'
    snapshot_value : int or float
        index (number) of snapshot file
    simulation_directory : str
        directory of simulation
    snapshot_directory: str
        directory of snapshot files within simulation_directory
    track_directory : str
        directory of files for particle pointers, formation coordinates, and host coordinates
    '''
    species = ut.array.arrayize(species)
    if 'all' in species:
        species = ['dark2', 'dark', 'star', 'gas']

    Read = gizmo_io.ReadClass()
    part = Read.read_snapshots(
        species,
        snapshot_value_kind,
        snapshot_value,
        simulation_directory,
        snapshot_directory,
        track_directory,
        '',
        None,
        None,
        assign_hosts=False,
        separate_dark_lowres=False,
        sort_dark_by_id=False,
    )

    gizmo_plot.print_properties_statistics(part, species)


def print_particle_property_extrema_across_snapshots(
    simulation_directory=gizmo_default.simulation_directory,
    snapshot_directory=gizmo_default.snapshot_directory,
    track_directory=gizmo_default.track_directory,
    property_dict={'gas': ['size', 'number.density']},
    snapshot_indices=None,
):
    '''
    For each input property, get its extremum at each snapshot.
    Print statistics of property across all snapshots.

    Parameters
    ----------
    simulation_directory : str
        directory of simulation
    snapshot_directory : str
        directory of snapshot files
    track_directory : str
        directory of files for particle pointers, formation coordinates, and host coordinates
    property_dict : dict
        keys = species, values are string or list of property[s]
    snapshot_indices : list
        snapshots indices to read
    '''
    elements = ['metals', 'he']

    property_statistic = {
        'size': {'function.name': 'min', 'function': np.min},
        'density': {'function.name': 'max', 'function': np.max},
        'number.density': {'function.name': 'max', 'function': np.max},
    }

    Say = ut.io.SayClass(print_particle_property_extrema_across_snapshots)

    simulation_directory = ut.io.get_path(simulation_directory)

    if snapshot_indices is None or len(snapshot_indices) == 0:
        Snapshot = ut.simulation.SnapshotClass()
        Snapshot.read_snapshots(directory=simulation_directory)
        snapshot_indices = Snapshot['index']

    species_read = property_dict.keys()

    properties_read = []
    for spec_name in property_dict:
        properties = property_dict[spec_name]
        if np.isscalar(properties):
            properties = [properties]

        prop_dict = {}
        for prop_name in property_dict[spec_name]:
            prop_dict[prop_name] = []

            prop_name_read = prop_name.replace('number.', '')
            if prop_name_read not in properties_read:
                properties_read.append(prop_name_read)

        # re-assign property list as dictionary so can store list of values
        property_dict[spec_name] = prop_dict

    Read = gizmo_io.ReadClass()

    for snapshot_i in snapshot_indices:
        try:
            part = Read.read_snapshots(
                species_read,
                'index',
                snapshot_i,
                simulation_directory,
                snapshot_directory,
                track_directory,
                '',
                properties_read,
                elements,
                assign_hosts=False,
                sort_dark_by_id=False,
            )

            for spec_name in property_dict:
                for prop_name in property_dict[spec_name]:
                    try:
                        prop_name_ext = property_statistic[prop_name]['function'](
                            part[spec_name].prop(prop_name)
                        )
                        property_dict[spec_name][prop_name].append(prop_name_ext)
                    except Exception:
                        Say.say(f'! {spec_name} {prop_name} not in particle dictionary')
        except Exception:
            Say.say(
                f'! cannot read snapshot index {snapshot_i} in'
                + f' {simulation_directory + snapshot_directory}'
            )

    Statistic = ut.math.StatisticClass()

    for spec_name in property_dict:
        for prop_name in property_dict[spec_name]:
            prop_func_name = property_statistic[prop_name]['function.name']
            prop_values = np.array(property_dict[spec_name][prop_name])
            if prop_name == 'size':
                prop_values *= 1000  # convert to [pc]

            Statistic.stat = Statistic.get_statistic_dict(prop_values)

            Say.say(f'\n{spec_name} {prop_name} {prop_func_name}:')
            for stat_name in ['min', 'percent.16', 'median', 'percent.84', 'max']:
                Say.say('{:10s} = {:.3f}'.format(stat_name, Statistic.stat[stat_name]))

            # Statistic.print_statistics()

    return property_dict


def print_summary(
    snapshot_value_kind='redshift',
    snapshot_value=0,
    simulation_directory=gizmo_default.simulation_directory,
    snapshot_directory=gizmo_default.snapshot_directory,
    track_directory=gizmo_default.track_directory,
):
    '''
    Print the most useful diagnostics.

    Parameters
    ----------
    snapshot_value_kind : str
        snapshot number kind: 'index', 'redshift', 'scalefactor'
    snapshot_value : int or float
        index (number) of snapshot file
    simulation_directory : str
        directory of simulation
    snapshot_directory: str
        directory of snapshot files within simulation_directory
    track_directory : str
        directory of files for particle pointers, formation coordinates, and host coordinates
    '''
    Read = gizmo_io.ReadClass()
    part = Read.read_snapshots(
        ['star', 'dark', 'dark2'],
        snapshot_value_kind,
        snapshot_value,
        simulation_directory,
        snapshot_directory,
        track_directory,
        properties=['position', 'mass', 'form.scalefactor'],
        assign_hosts_rotation=True,
    )

    Contamination = ContaminationClass()
    Contamination.print_plot_contamination_v_distance(part)

    print_galaxy_properties(part)

    Runtime = RuntimeClass()
    _ = Runtime.print_run_times()


# --------------------------------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------------------------------
def test_stellar_mass_loss(
    part_z0, part_z, metallicity_limits=[0.001, 10], metallicity_bin_width=0.2, form_time_width=5
):
    '''
    .
    '''
    from . import gizmo_track
    from . import gizmo_star

    Say = ut.io.SayClass(test_stellar_mass_loss)

    species = 'star'

    if 'Pointer' not in part_z.__dict__:
        ParticlePointer = gizmo_track.ParticlePointerClass()
        ParticlePointer.io_pointers(part_z)

    MetalBin = ut.binning.BinClass(
        metallicity_limits, metallicity_bin_width, include_max=True, log_scale=True
    )

    form_time_limits = [
        part_z.snapshot['time'] * 1000 - form_time_width,
        part_z.snapshot['time'] * 1000,
    ]

    part_indices_z0 = ut.array.get_indices(
        part_z0[species].prop('form.time') * 1000, form_time_limits
    )
    part_indices_z = part_z.Pointer.get_pointers('star', 'star', part_indices_z0)

    Say.say(
        '* stellar mass loss across {:.3f} Gyr in metallicity bins for {} particles'.format(
            part_z0.snapshot['time'] - part_z.snapshot['time'], part_indices_z0.size
        )
    )

    # compute metallicity using solar abundance assumed in Gizmo
    sun_massfraction = gizmo_star.get_sun_massfraction('fire2')
    metallicities = (
        part_z0[species].prop('massfraction.metals', part_indices_z0) / sun_massfraction['metals']
    )

    metal_bin_indices = MetalBin.get_bin_indices(metallicities)

    for metal_i, metallicity in enumerate(MetalBin.mids):
        masks = metal_bin_indices == metal_i
        if np.sum(masks):
            pis_z0 = part_indices_z0[masks]
            pis_z = part_indices_z[masks]

            mass_loss_fractions = (
                part_z[species]['mass'][pis_z] - part_z0[species]['mass'][pis_z0]
            ) / part_z[species]['mass'][pis_z]

            mass_loss_fractions_py = part_z0[species].prop('mass.loss.fraction', pis_z0)
            # mass_loss_fractions_py = MassLoss.get_mass_loss_fraction_from_spline(
            #    part_z0[species].prop('age', pis_z0) * 1000,
            #    metal_mass_fractions=part_z0[species].prop('massfraction.metals', pis_z0))

            Say.say(
                'Z = {:.3f}, N = {:4d} | gizmo {:.1f}%, python {:.1f}%, p/g = {:.3f}'.format(
                    metallicity,
                    pis_z0.size,
                    100 * np.median(mass_loss_fractions),
                    100 * np.median(mass_loss_fractions_py),
                    np.median(mass_loss_fractions_py / mass_loss_fractions),
                )
            )

    mass_loss_fractions = (
        part_z[species]['mass'][part_indices_z] - part_z0[species]['mass'][part_indices_z0]
    ) / part_z[species]['mass'][part_indices_z]
    mass_loss_fractions_py = part_z0[species].prop('mass.loss.fraction', part_indices_z0)
    print(
        '* all Z, N = {} | gizmo = {:.1f}%, python = {:.1f}%, p/g = {:.3f}'.format(
            part_indices_z0.size,
            100 * np.median(mass_loss_fractions),
            100 * np.median(mass_loss_fractions_py),
            np.median(mass_loss_fractions_py / mass_loss_fractions),
        )
    )


# --------------------------------------------------------------------------------------------------
# performance and scaling
# --------------------------------------------------------------------------------------------------
def plot_scaling(
    scaling_kind='strong',
    resolution='res7100',
    time_kind='core',
    axis_x_log_scale=True,
    axis_y_log_scale=True,
    file_name=False,
    directory='.',
):
    '''
    Print simulation run times (wall or core).
    'speedup' := WT(1 CPU) / WT(N CPU) =
    'efficiency' := WT(1 CPU) / WT(N CPU) / N = CT(1 CPU) / CT(N CPU)

    Parameters
    ----------
    scaling_kind : str
        'strong', 'weak'
    time_kind : str
        'node', 'core', 'wall', 'speedup', 'efficiency'
    axis_x_log_scale : bool
        whether to use logarithmic scaling for x axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    file_name : str
        whether to write figure to file and its name. True = use default naming convention
    directory : str
        directory to write figure file
    '''
    # weak_dark = {
    #    'res57000': {'particle.number': 8.82e6, 'core.number': 64,
    #                 'core.time': 385, 'wall.time': 6.0},
    #    'res7100': {'particle.number': 7.05e7, 'core.number': 512,
    #                'core.time': 7135, 'wall.time': 13.9},
    #    'res880': {'particle.number': 5.64e8, 'core.number': 2048,
    #               'core.time': 154355, 'wall.time': 75.4},
    # }

    # stampede
    # weak_baryon = {
    #    'res450000': {'particle.number': 1.10e6 * 2, 'core.number': 32,
    #                  'core.time': 1003, 'wall.time': 31.34 * 1.5},
    #    'res57000': {'particle.number': 8.82e6 * 2, 'core.number': 512,
    #                 'core.time': 33143, 'wall.time': 64.73},
    #    'res7100': {'particle.number': 7.05e7 * 2, 'core.number': 2048,
    #                'core.time': 1092193, 'wall.time': 350.88},
    #    #'res880': {'particle.number': 5.64e8 * 2, 'core.number': 8192,
    #    #           'core.time': 568228, 'wall.time': 69.4},
    #    # projected
    #    #'res880': {'particle.number': 5.64e8 * 2, 'core.number': 8192,
    #    #           'core.time': 1.95e7, 'wall.time': 2380},
    # }

    # conversion to stampede2
    weak_baryon = collections.OrderedDict()

    # weak_baryon['res450000'] = {
    #    'particle.number': 1.10e6 * 2,
    #    'node.number': 1,
    #    'node.time': 73,
    #    'wall.time': 73,
    # }
    # weak_baryon['res57000'] = {
    #    'particle.number': 8.82e6 * 2,
    #    'node.number': 8,
    #    'node.time': 1904,
    #    'wall.time': 239,
    # }
    # weak_baryon['res7100'] = {
    #    'particle.number': 7.05e7 * 2,
    #    'node.number': 64,
    #    'node.time': 52000,
    #    'wall.time': 821,
    # }

    # weak_baryon['res880'] = {
    #    'particle.number': 7.e7 * 2,
    #    'node.number': 64,
    #   'node.time': 52000,
    #    'wall.time': 821,
    # }

    # m12f to z = 1, Stampede2 equivalent node-hours
    # weak_baryon['res450000'] = {
    #    'particle.number': 8.14e7 * 2 / 64,
    #    'node.number': 1,
    #    'node.time': 73,
    #    'wall.time': 73,
    # }
    weak_baryon['res57000'] = {
        'particle.number': 8.14e7 * 2 / 8,
        'node.number': 2.5,
        'node.time': 500,
        'wall.time': 200,
    }
    weak_baryon['res7100'] = {
        'particle.number': 8.14e7 * 2,
        'node.number': 20,
        'node.time': 12511,
        'wall.time': 626,
    }
    weak_baryon['res880'] = {
        'particle.number': 7.70e8 * 2,
        'node.number': 160,
        'node.time': 500458,
        'wall.time': 3128,
    }

    strong_baryon = collections.OrderedDict()

    # convert from running to scale-factor = 0.068 to 0.1 via 2x
    strong_baryon['res880'] = {
        'particle.number': 5.64e8 * 2,
        'core.number': np.array([2048, 4096, 8192, 16384]),
        #'node.number': np.array([128, 256, 512, 1024]),
        'node.number': np.array([40, 80, 160, 320]),  # conversion to Stampede2 SKX
        'wall.time': np.array([15.55, 8.64, 4.96, 4.57]) * 2,
        #'core.time': np.array([31850, 35389, 40632, 74875]) * 2,
        'node.time': np.array([664, 737, 847, 1560]),
    }

    # did not have time to run these, so scale down from res880
    # scaled to run time to z = 3 using 2048
    # stampede
    # strong_baryon['res7100'] = {
    #    'particle.number': 7e7 * 2,
    #    'node.number': np.array([32, 64, 128, 256]),
    #    'core.number': np.array([512, 1024, 2048, 4096]),
    #    'wall.time': np.array([72.23, 40.13, 23.04, 21.22]),
    #    'core.time': np.array([36984, 41093, 47182, 86945]),
    #    'node.time': np.array([2312, 2568, 2949, 5434]),
    # }

    # conversion to stampede 2
    # half the number of nodes and multipy node time by 1.17, multiply wall time by 2.34
    # based on res57000 simulation to z = 0
    strong_baryon['res7100'] = {
        'particle.number': 7e7 * 2,
        'node.number': np.array([16, 32, 64, 128]),
        'core.number': np.array([2048, 4096, 8192, 16384]),
        'wall.time': np.array([72.23, 40.13, 23.04, 21.22]) * 2.34,
        'core.time': np.array([36984, 41093, 47182, 86945]) * 1.17,
        'node.time': np.array([2312, 2568, 2949, 5434]) * 1.17,
    }

    # plot ----------
    _fig, subplot = ut.plot.make_figure(1, left=0.22, right=0.95, top=0.96, bottom=0.16)

    if scaling_kind == 'strong':
        strong = strong_baryon[resolution]

        if time_kind == 'core':
            times = strong['core.time']
        if time_kind == 'node':
            times = strong['node.time']
        elif time_kind == 'wall':
            times = strong['wall.time']
        elif time_kind == 'speedup':
            times = strong['wall.time'][0] / strong['wall.time']
        elif time_kind == 'efficiency':
            times = strong['wall.time'][0] / strong['wall.time']

        # subplot.set_xlabel('number of cores')
        subplot.set_xlabel('number of nodes')

        if resolution == 'res880':
            # axis_x_limits = [1e2, 1.9e4]
            axis_x_limits = [10, 400]
        elif resolution == 'res7100':
            # axis_x_limits = [3e2, 1e4]
            axis_x_limits = [10, 200]

        axis_x_kind = 'core.number'
        if time_kind == 'core':
            if resolution == 'res880':
                axis_y_limits = [0, 1.6e5]
                subplot.set_ylabel('CPU time to $z = 9$ [hr]')
            elif resolution == 'res7100':
                axis_y_limits = [0, 1e5]
                subplot.set_ylabel('CPU time to $z = 3$ [hr]')
        elif time_kind == 'node':
            axis_x_kind = 'node.number'
            if resolution == 'res880':
                # axis_y_limits = [0, 1e4]
                axis_y_limits = [0, 2000]
                subplot.set_ylabel('node-hours to $z = 9$ [hr]')
            elif resolution == 'res7100':
                axis_y_limits = [0, 8000]
                subplot.set_ylabel('node-hours to $z = 3$')
        elif time_kind == 'wall':
            axis_y_limits = [0, 35]
            subplot.set_ylabel('wall time to $z = 9$ [hr]')
        elif time_kind == 'speedup':
            axis_y_limits = [0, 9000]
            subplot.set_ylabel('parallel speedup $T(1)/T(N)$')
        elif time_kind == 'efficiency':
            axis_y_limits = [0, 1.05]
            subplot.set_ylabel('parallel efficiency $T(1)/T(N)/N$')

        ut.plot.set_axes_scaling_limits(
            subplot, axis_x_log_scale, axis_x_limits, None, axis_y_log_scale, axis_y_limits
        )

        subplot.plot(strong[axis_x_kind], times, '*-', linewidth=2.0, color='blue')

        if time_kind == 'speedup':
            subplot.plot([0, 3e4], [0, 3e4], '--', linewidth=1.5, color='black')

        if resolution == 'res880':
            subplot.text(
                0.1,
                0.1,
                #'strong scaling:\nparticle number = 1.1e9',
                'strong scaling:\nparticle number = 1.5e9',
                color='black',
                transform=subplot.transAxes,
            )
        elif resolution == 'res7100':
            subplot.text(
                0.1,
                0.1,
                'strong scaling:\nparticle number = 1.5e8',
                color='black',
                transform=subplot.transAxes,
            )

    elif scaling_kind == 'weak':
        # dm_particle_numbers = np.array(
        #    [weak_dark[core_num]['particle.number'] for core_num in sorted(weak_dark.keys())])
        baryon_particle_numbers = np.array([weak_baryon[i]['particle.number'] for i in weak_baryon])

        if time_kind == 'node':
            # dm_times = np.array(
            #    [weak_dark[core_num]['core.time'] for core_num in sorted(weak_dark.keys())])
            baryon_times = np.array([weak_baryon[i]['node.time'] for i in weak_baryon])
        elif time_kind == 'wall':
            # resolutinon_ref = 'res880'
            # resolutinon_ref = 'res7100'
            # ratio_ref = (
            #    weak_baryon[resolutinon_ref]['particle.number']
            #    / weak_baryon[resolutinon_ref]['node.number']
            # )
            # dm_times = np.array(
            #    [weak_dark[core_num]['wall.time'] * ratio_ref /
            #     (weak_dark[core_num]['particle.number'] / weak_dark[core_num]['core.number'])
            #     for core_num in sorted(weak_dark.keys())])
            baryon_times = np.array([weak_baryon[i]['wall.time'] for i in weak_baryon])

        subplot.set_xlabel('number of particles')

        # axis_x_limits = [6e6, 1.5e9]
        # axis_x_limits = [1e6, 2e8]
        axis_x_limits = [1e7, 2e9]

        if time_kind == 'node':
            # axis_y_limits = [10, 2e5]
            axis_y_limits = [100, 1e6]
            subplot.set_ylabel('node-hours to $z = 1$')
        elif time_kind == 'wall':
            # axis_y_limits = [10, 1000]
            axis_y_limits = [100, 10000]
            subplot.set_ylabel('wall time to $z = 1$ [hr]')
            subplot.text(
                0.05,
                0.05,
                #'weak scaling:\nparticles / node = {:.1e}'.format(ratio_ref),
                'weak scaling:\nparticles / node = 9.4e6',
                color='black',
                transform=subplot.transAxes,
            )

        ut.plot.set_axes_scaling_limits(
            subplot, axis_x_log_scale, axis_x_limits, None, axis_y_log_scale, axis_y_limits
        )

        # subplot.plot(dm_particle_numbers, dm_times, '.-', linewidth=2.0, color='red')
        # subplot.plot(mfm_particlgizmoe_numbers[:-1], mfm_times[:-1], '*-', linewidth=2.0,
        # color='blue')
        # subplot.plot(mfm_particle_numbers[1:], mfm_times[1:], '*--', linewidth=2.0, color='blue',
        #             alpha=0.7)
        subplot.plot(baryon_particle_numbers, baryon_times, '*-', linewidth=2.0, color='blue')

    if file_name is True or file_name == '':
        file_name = 'scaling'
    ut.plot.parse_output(file_name, directory)


# --------------------------------------------------------------------------------------------------
# running from command line
# --------------------------------------------------------------------------------------------------
def main():
    '''
    .
    '''
    if len(sys.argv) <= 1:
        s = 'specify function: runtime, contamination, properties, statistics, extrema, summary'
        raise OSError(s)

    function_kind = str(sys.argv[1])
    assert (
        'runtime' in function_kind
        or 'contamination' in function_kind
        or 'propert' in function_kind
        or 'statistic' in function_kind
        or 'extrem' in function_kind
        or 'summary' in function_kind
    )

    if 'runtime' in function_kind:
        wall_time_restart = 0
        if len(sys.argv) > 2:
            wall_time_restart = float(sys.argv[2])

        scalefactors = None  # use default
        if len(sys.argv) > 3:
            scalefactor_min = float(sys.argv[3])
            scalefactor_width = 0.05
            if len(sys.argv) > 4:
                scalefactor_width = float(sys.argv[4])
            scalefactors = np.arange(scalefactor_min, 1.01, scalefactor_width)

        Runtime = RuntimeClass()
        _ = Runtime.print_run_times(wall_time_restart=wall_time_restart, scalefactors=scalefactors)

    elif 'contamination' in function_kind:
        snapshot_redshift = 0
        if len(sys.argv) > 2:
            snapshot_redshift = float(sys.argv[2])

        Contamination = ContaminationClass()
        Contamination.print_plot_contamination_v_distance_both(
            snapshot_value_kind='redshift', snapshot_value=snapshot_redshift
        )

    elif 'propert' in function_kind:
        snapshot_redshift = 0
        print_galaxy_properties()
        if len(sys.argv) > 2:
            snapshot_redshift = float(sys.argv[2])

        print_galaxy_properties(snapshot_value_kind='redshift', snapshot_value=snapshot_redshift)

    elif 'statistic' in function_kind:
        snapshot_redshift = 0
        print_galaxy_properties()
        if len(sys.argv) > 2:
            snapshot_redshift = float(sys.argv[2])

        print_particle_properties_statistics(
            snapshot_value_kind='redshift', snapshot_value=snapshot_redshift
        )

    elif 'extrem' in function_kind:
        print_particle_property_extrema_across_snapshots()

    elif 'summary' in function_kind:
        snapshot_redshift = 0
        if len(sys.argv) > 2:
            snapshot_redshift = float(sys.argv[2])
        print_summary()

    else:
        print(f'! not recognize input function_kind = {function_kind}')


if __name__ == '__main__':
    main()
