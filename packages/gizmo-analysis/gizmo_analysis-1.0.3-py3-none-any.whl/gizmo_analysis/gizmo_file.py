#!/usr/bin/env python3

'''
Manipulate files in a Gizmo simulation directory: compress, tar, delete, transfer across machines.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

import os
import sys
import glob
import numpy as np

import utilities as ut
from . import gizmo_default
from . import gizmo_io

# --------------------------------------------------------------------------------------------------
# default subsets of snapshots
# --------------------------------------------------------------------------------------------------
# default subset of 65 snapshots for FIRE-2 (not FIRE-3)
snapshot_indices_subset = [
    0,  # z = 99
    20,
    26,
    33,
    41,
    52,  # z = 10 - 6
    55,
    57,
    60,
    64,
    67,  # z = 5.8 - 5.0
    71,
    75,
    79,
    83,
    88,  # z = 4.8 - 4.0
    91,
    93,
    96,
    99,
    102,
    105,
    109,
    112,
    116,
    120,  # z = 3.9 - 3.0
    124,
    128,
    133,
    137,
    142,
    148,
    153,
    159,
    165,
    172,  # z = 2.9 - 2.0
    179,
    187,
    195,
    204,
    214,
    225,
    236,
    248,
    262,
    277,  # z = 1.9 - 1.0
    294,
    312,
    332,
    356,
    382,
    412,
    446,
    486,
    534,  # z = 0.9 - 0.1
    539,
    544,
    550,
    555,
    561,
    567,
    573,
    579,
    585,  # z = 0.09 - 0.01
    600,
]

snapshot_indices_public = [
    20,
    23,
    26,
    29,
    33,
    37,
    41,
    46,
    52,  # z = 6
    59,
    67,  # z = 5
    77,
    88,  # z = 4
    102,
    120,  # z = 3
    142,
    172,  # z = 2
    214,
    277,  # z = 1
    294,
    312,
    332,
    356,
    382,
    412,
    446,
    486,
    534,  # z = 0.1
    590,  # z = 0.0016
    591,
    592,
    593,
    594,
    595,
    596,
    597,
    598,
    599,
    600,
]


# --------------------------------------------------------------------------------------------------
# compress files
# --------------------------------------------------------------------------------------------------
class CompressClass(ut.io.SayClass):
    '''
    Compress snapshot files, losslessly, using Robert Feldmann's manipulate_hdf5 package.
    '''

    def __init__(
        self,
        manipulate_hdf5_directory='~/analysis/manipulate_hdf5',
        python_executable='python3',
    ):
        '''
        Parameters
        ----------
        analysis_directory : str
            directory of manipulate_hdf5 package
        manipulate_hdf5_directory : str
            python executable to use to run compression script
        '''
        self.executable = f'{python_executable} {manipulate_hdf5_directory}/compactify_hdf5.py -L 0'

    def compress_snapshots(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        write_directory=gizmo_default.snapshot_directory + '_comp',
        snapshot_indices=None,
        proc_number=1,
    ):
        '''
        Read snapshots in input snapshot_directory, compress them,
        write compressed snapshots to snapshot_directory + write_directory_modifier.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of snapshots
        write_directory : str
            directory to write compressed snapshots
            if same as snapshot_directory or '', over-write existing snapshots
        snapshot_indices : list
            indices of snapshots to compress. If None or 'all', compress all in snapshot_directory.
        proc_number : int
            number of parallel processes to use
        '''
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = ut.io.get_path(snapshot_directory)
        if not write_directory:
            write_directory = snapshot_directory
        else:
            write_directory = ut.io.get_path(write_directory, create_path=True)

        Read = gizmo_io.ReadClass()

        # get all snapshot file names and indices in directory
        snapshot_names_all, snapshot_indices_all = Read.get_snapshot_file_names_indices(
            simulation_directory + snapshot_directory
        )

        if np.isscalar(snapshot_indices) and isinstance(snapshot_indices, int):
            snapshot_indices = [snapshot_indices]

        if (
            snapshot_indices is None
            or isinstance(snapshot_indices, str)
            or len(snapshot_indices) == 0
        ):
            # run on all available snapshots
            snapshot_names = snapshot_names_all
        else:
            # limit to input list of snapshot indices
            snapshot_names = []
            for snapshot_name, snapshot_index in zip(snapshot_names_all, snapshot_indices_all):
                if snapshot_index in snapshot_indices:
                    snapshot_names.append(snapshot_name)

        args_list = [
            (snapshot_name, snapshot_directory, write_directory) for snapshot_name in snapshot_names
        ]

        ut.io.run_in_parallel(self._compress_snapshot, args_list, proc_number=proc_number)

    def _compress_snapshot(self, snapshot_name, snapshot_directory, write_directory):
        '''
        Compress a single snapshot (a single file or a directory with multiple files) named
        snapshot_name in snapshot_directory, write to write_directory.

        Parameters
        ----------
        snapshot_name : str
            name of snapshot (file or directory)
        snapshot_directory : str
            directory to read existing snapshot files
        write_directory : str
            directory to write compressed snapshots
            if same as snapshot_directory, over-write existing snapshots
        '''
        if 'snapdir' in snapshot_name:
            # ensure this snapdir directory exists in write directory
            path_name_write = snapshot_name.replace(snapshot_directory, write_directory)
            ut.io.get_path(path_name_write, create_path=True)
            # get name of each snapshot block file
            path_file_names = glob.glob(snapshot_name + '/*')
            path_file_names.sort()
        else:
            path_file_names = [snapshot_name]

        for path_file_name in path_file_names:
            if write_directory != snapshot_directory:
                path_file_name_write = path_file_name.replace(snapshot_directory, write_directory)
            else:
                path_file_name_write = path_file_name

            executable_i = f'{self.executable} -o {path_file_name_write} {path_file_name}'
            self.say(f'executing:  {executable_i}')
            os.system(executable_i)

    def test_compression(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        snapshot_indices=None,
        compression_level=0,
        verbose=False,
    ):
        '''
        Read headers from all snapshot files in simulation_directory + snapshot_directory to check
        if files have been compressed.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of compressed snapshot files
        snapshot_indices : list
            indices of snapshots to test. If None or 'all', test all in snapshot_directory.
        compression_level : int
        verbose : bool
        '''
        header_compression_name = 'compression.level'

        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = ut.io.get_path(snapshot_directory)

        Read = gizmo_io.ReadClass()

        compression_wrong_snapshots = []
        compression_none_snapshots = []

        snapshot_block_number = 1

        # get all snapshot file names and indices in directory
        path_file_names, file_indices = Read.get_snapshot_file_names_indices(
            simulation_directory + snapshot_directory
        )

        if 'snapdir' in path_file_names[0]:
            # get number of block files per snapshot
            snapshot_file_names = glob.glob(path_file_names[0] + '/*')
            snapshot_block_number = len(snapshot_file_names)

        if np.isscalar(snapshot_indices) and isinstance(snapshot_indices, int):
            snapshot_indices = [snapshot_indices]

        if (
            snapshot_indices is None
            or isinstance(snapshot_indices, str)
            or len(snapshot_indices) == 0
        ):
            # run on all available snapshots
            snapshot_indices = file_indices
        else:
            # limit to input list of snapshot indices
            snapshot_indices = np.intersect1d(snapshot_indices, file_indices)

        for snapshot_index in snapshot_indices:
            for snapshot_block_index in range(snapshot_block_number):
                header = Read.read_header(
                    simulation_directory,
                    snapshot_directory,
                    'index',
                    snapshot_index,
                    snapshot_block_index=snapshot_block_index,
                    verbose=verbose,
                )
                if header_compression_name in header:
                    if (
                        compression_level is not None
                        and header[header_compression_name] != compression_level
                        and snapshot_index not in compression_wrong_snapshots
                    ):
                        compression_wrong_snapshots.append(snapshot_index)
                elif snapshot_index not in compression_none_snapshots:
                    compression_none_snapshots.append(snapshot_index)

        self.say(
            '* tested {} snapshots [{}, {}]'.format(
                len(snapshot_indices), min(snapshot_indices), max(snapshot_indices)
            )
        )
        self.say(f'* {len(compression_none_snapshots)} are uncompressed')
        if len(compression_none_snapshots) > 0:
            self.say(f'{compression_none_snapshots}')  # list uncompressed snapshots
        n = len(compression_wrong_snapshots)
        self.say(f'* {n} have (wrong) compression level != {compression_level}')
        if len(compression_wrong_snapshots) > 0:
            self.say(f'{compression_wrong_snapshots}')  # list wrong-compressed snapshots


# --------------------------------------------------------------------------------------------------
# clean and archive simulation directories and files
# --------------------------------------------------------------------------------------------------
class ArchiveClass(ut.io.SayClass):
    '''
    Clean, archive, and delete simulation directories and files after a simulation has finished.
    '''

    def clean_directories(
        self,
        directories='.',
        gizmo_directory=gizmo_default.gizmo_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        restart_directory=gizmo_default.restart_directory,
        gizmo_out_file=gizmo_default.gizmo_out_file_name,
        gizmo_err_file=gizmo_default.gizmo_err_file_name,
        snapshot_scalefactor_file=gizmo_default.snapshot_scalefactor_file_name,
    ):
        '''
        Clean a simulation directory, a list of simulation directories, or a directory of multiple
        simulation directories.
        Run this after a simulation finishes.
        Remove unnecessary run-time files, and tar directories (into a single tar-ball file) that we
        generally do not need for post-processing analysis.

        Parameters
        ----------
        directories : str or list thereof
            directory[s] to run this on. can be a single simulation directory, a list of simulation
            directories, or a directory that contains multiple simulation directories for which this
            function will run recursively on each one
        gizmo_directory : str
            directory of Gizmo source code
        snapshot_directory : str
            output directory that contains snapshots
        restart_directory : str
            directory within snapshot_directory that stores restart files
        gizmo_out_file : str
            Gizmo 'out' file
        gizmo_err_file : str
            Gizmo error file
        snapshot_scalefactor_file : str
            file that contains snapshot scale-factors (only)
        '''
        gizmo_config_file_used = 'GIZMO_config.h'
        gizmo_config_file_save = (
            'gizmo_config.h'  # file to save used config settings and gizmo version
        )

        if np.isscalar(directories):
            directories = [directories]

        if gizmo_directory[-1] != '/':
            gizmo_directory += '/'
        if snapshot_directory[-1] != '/':
            snapshot_directory += '/'
        gizmo_out_file = gizmo_out_file.rstrip('*')

        cwd = os.getcwd()  # save current directory

        # move into each directory
        for directory in directories:
            directory = directory.rstrip('/')
            if directory != '.':
                self.say(f'* moving into:  {directory}/')
                os.chdir(f'{directory}')

            # check if this directory has relevant simulation directories,
            # or if need to run recursively on different simulation directories
            directory_names = glob.glob('*/')  # get names of all directories
            directory_names.sort()
            if len(directory_names) == 0:
                # this is an empty directory, exit
                self.say(f'! could not find any directories to clean in {directory}/')
                os.chdir(f'{cwd}')
                return
            elif snapshot_directory not in directory_names:
                # this is a directory of simulation directories, recursively run on each one
                for directory_name in directory_names:
                    self.clean_directories(
                        directory_name,
                        gizmo_directory,
                        snapshot_directory,
                        restart_directory,
                        gizmo_out_file,
                        gizmo_err_file,
                        snapshot_scalefactor_file,
                    )
                os.chdir(f'{cwd}')
                return

            if os.path.exists(f'{gizmo_directory}'):
                # clean directory of gizmo source code
                # save config file, move to simulation directory
                os.chdir(f'{gizmo_directory}')
                self.say(f'* cleaning + tar-ing:  {gizmo_directory}')
                os.system(f'mv {gizmo_config_file_used} ../{gizmo_config_file_save}')
                os.system('make clean')

                if os.path.exists('.git'):
                    version_control = 'git'
                elif os.path.exists('.hg'):
                    version_control = 'hg'
                else:
                    version_control = None
                # append to the gizmo_config_file the version of Gizmo used (if not already there)
                if version_control == 'git':
                    if os.system(f'grep "# git" ../{gizmo_config_file_save}') > 0:
                        os.system(
                            f'printf "\n# git version of Gizmo\n" >> ../{gizmo_config_file_save}'
                        )
                        os.system(f'git log -n 1 >> ../{gizmo_config_file_save}')
                    os.system('git gc --aggressive --prune')  # prune old commits
                elif version_control == 'hg':
                    if os.system(f'grep "# hg" ../{gizmo_config_file_save}') > 0:
                        os.system(
                            f'printf "\n# hg version of Gizmo\n" >> ../{gizmo_config_file_save}'
                        )
                        os.system(f'hg log -l 1 >> ../{gizmo_config_file_save}')

                os.system('mv ../ewald_spc_table_64_dbl.dat ../spcool_tables ../TREECOOL -t .')
                os.chdir('..')

                # tar gizmo directory
                gizmo_directory_name = gizmo_directory.rstrip('/')
                os.system(f'tar -cf {gizmo_directory_name}.tar {gizmo_directory_name}')
                os.system(f'rm -rf {gizmo_directory_name}')
            else:
                self.say(f'! could not find:  {gizmo_directory}')

            # clean output files
            os.system(f'rm -f {gizmo_err_file}')
            if os.path.exists(f'{gizmo_out_file}'):
                os.system(f'head -1000 {gizmo_out_file} > {gizmo_out_file}.txt')
                os.system(f'rm -f {gizmo_out_file}')
            os.system(f'rm -f {snapshot_scalefactor_file}')

            # clean snapshot directory
            if os.path.exists(f'{snapshot_directory}'):
                os.chdir(f'{snapshot_directory}')
                self.say(f'* cleaning:  {snapshot_directory}')
                os.system(f'rm -rf {restart_directory}')
                os.system('rm -f balance.txt energy.txt sfr.txt timings.txt')
                os.system('rm -f HIIheating.txt MomWinds.txt SNeIIheating.txt')
                os.chdir('..')
            else:
                self.say(f'! could not find:  {snapshot_directory}')

            # clean backup files
            os.system('rm -f *~ .#* ._* /#*#')

            # move back to original directory
            os.chdir(f'{cwd}')

    def tar_directories(
        self,
        directories='.',
        snapshot_directory=gizmo_default.snapshot_directory,
        job_directory=gizmo_default.gizmo_job_directory,
        ic_directory=gizmo_default.ic_directory,
        particle_track_directory=gizmo_default.track_directory,
        halo_directory='halo',
        rockstar_directory='rockstar_dm',
        rockstar_job_directory='rockstar_jobs',
        rockstar_catalog_directory='catalog',
        rockstar_hdf5_directory='catalog_hdf5',
        delete_directories=False,
        delete_tarballs=False,
        proc_number=1,
    ):
        '''
        Use tar to combine simulation sub-directories into single tar-ball files.
        Run this on a single simulation directory, a list of simulation directories,
        or a directory of multiple simulation directories.
        Run this after runing clean_directory(), to reduce the file count for archival/tape storage.
        By default, this stores the original sub-directories after tar-ring them, but you can delete
        the directories (if you are running this on the archival/tape server directly) by inputing
        delete_directories=True.
        To delete the tar-balls that this function creates (if you are on live scratch space),
        simply input delete_tarballs=True.

        Parameters
        ----------
        directories : str or list thereof
            directory[s] to run this on. can be a single simulation directory, a list of simulation
            directories, or a directory that contains multiple simulation directories for which this
            function will run recursively on each one
        snapshot_directory : str
            output directory that contains snapshot files
        job_directory : str
            directory that contains slurm/pbs job files
        ic_directory : str
            directory that contains initial condition files from MUSIC
        particle_track_directory : str
            directory of particle tracking files
        halo_directory : str
            directory of (all) halo files/directories
        rockstar_directory : str
            directory of (all) Rockstar files/directories
        rockstar_job_directory : str
            directory of Rockstar run-time log/job files
        rockstar_catalog_directory : str
            directory of Rockstar (text) halo catalog + tree files
        rockstar_hdf5_directory : str
            directory of post-processed catalog + tree hdf5 files
        delete_directories : bool
            whether to delete the (raw) directories after tar-ing them into a single file
        delete_tarballs : bool
            whether to delete existing tar-balls
            use this safely to clean the tar-balls that this function creates
        proc_number : int
            number of parallel processes for tar-ing halo directories + snapshots
        '''
        if np.isscalar(directories):
            directories = [directories]

        if proc_number > 1:
            from multiprocessing import Pool

        if snapshot_directory[-1] != '/':
            snapshot_directory += '/'

        # move to this directory
        cwd = os.getcwd()

        # move into each directory
        for directory in directories:
            directory = directory.rstrip('/')
            if directory != '.':
                self.say(f'\n\n* moving into:  {directory}/')
                os.chdir(f'{directory}')

            # check if this directory has relevant simulation directories,
            # or if need to run recursively on different simulation directories
            directory_names = glob.glob('*/')  # get names of all directories
            directory_names.sort()
            if len(directory_names) == 0:
                # this is an empty directory, exit
                self.say(f'\n! could not find any directories to tar in {directory}/')
                os.chdir(f'{cwd}')
                return
            elif snapshot_directory not in directory_names:
                # this is a directory of simulation directories, recursively run on each one
                for directory_name in directory_names:
                    self.tar_directories(
                        directory_name,
                        snapshot_directory,
                        job_directory,
                        ic_directory,
                        particle_track_directory,
                        halo_directory,
                        rockstar_directory,
                        rockstar_job_directory,
                        rockstar_catalog_directory,
                        rockstar_hdf5_directory,
                        delete_directories,
                        delete_tarballs,
                    )
                os.chdir(f'{cwd}')
                return

            # tar directory of slurm/pbs batch job files
            self._tar_directory(job_directory, delete_directories, delete_tarballs)

            # tar directory of initial conditions
            self._tar_directory(ic_directory, delete_directories, delete_tarballs)

            # tar directory of particle tracking files
            self._tar_directory(particle_track_directory, delete_directories, delete_tarballs)

            # tar directories of halo catalogs + trees
            if os.path.exists(f'{halo_directory}/{rockstar_directory}'):
                self.say(f'\n* moving into:  {halo_directory}/{rockstar_directory}/')
                os.chdir(f'{halo_directory}/{rockstar_directory}')

                halo_argss = [
                    (rockstar_job_directory, delete_directories, delete_tarballs),
                    (rockstar_hdf5_directory, delete_directories, delete_tarballs),
                    (rockstar_catalog_directory, delete_directories, delete_tarballs),
                ]

                if proc_number > 1:
                    # tar halo directories in parallel
                    # with Pool(proc_number) as pool:
                    #    pool.starmap(self._tar_directory, halo_argss)
                    pool = Pool(proc_number)
                    for halo_args in halo_argss:
                        pool.apply_async(self._tar_directory, halo_args)
                    pool.close()
                    pool.join()
                else:
                    for halo_args in halo_argss:
                        self._tar_directory(*halo_args)

                os.chdir('../..')
            else:
                self.say(f'\n! could not find:  {halo_directory}/{rockstar_directory}/')

            # tar each snapshot directory
            if os.path.exists(f'{snapshot_directory}'):
                os.chdir(f'{snapshot_directory}')

                snapshot_names = glob.glob('snapdir_*')
                if delete_tarballs:
                    # ensure get only tar files
                    snapshot_names = [s.rstrip('.tar') for s in snapshot_names if '.tar' in s]
                else:
                    # ensure not tar an existing tar file
                    snapshot_names = [s for s in snapshot_names if '.tar' not in s]
                snapshot_names.sort()
                if len(snapshot_names) > 0:
                    self.say(f'\n* moving into:  {snapshot_directory}')

                if proc_number > 1:
                    # tar snapshot directories in parallel
                    pool = Pool(proc_number)
                    for snapshot_name in snapshot_names:
                        pool.apply_async(
                            self._tar_directory,
                            (snapshot_name, delete_directories, delete_tarballs),
                        )
                    pool.close()
                    pool.join()
                else:
                    for snapshot_name in snapshot_names:
                        self._tar_directory(snapshot_name, delete_directories, delete_tarballs)

                os.chdir('..')
            else:
                self.say(f'\n! could not find:  {snapshot_directory}')

            # clean backup files
            os.system('rm -f *~ .#* ._* /#*#')

            # move back to original directory
            os.chdir(f'{cwd}')

    def _tar_directory(self, directory_name, delete_directories=False, delete_tarballs=False):
        '''
        Helper function.
        '''
        directory_name = directory_name.rstrip('/')

        if delete_tarballs:
            if os.path.exists(f'{directory_name}.tar'):
                self.say(f'\n* deleting:  {directory_name}.tar')
                os.system(f'rm -f {directory_name}.tar')
        else:
            if os.path.exists(f'{directory_name}'):
                self.say(f'* tar-ing:  {directory_name}/')
                os.system(f'tar -cf {directory_name}.tar {directory_name}')
                # with tarfile.open(f'{directory_name}.tar', 'w') as tar:
                #    tar.add(directory_name)
                if delete_directories:
                    self.say(f'* deleting:  {directory_name}/')
                    os.system(f'rm -rf {directory_name}')
            else:
                self.say(f'\n! could not find:  {directory_name}/')

    def delete_snapshots(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        snapshot_directory=gizmo_default.snapshot_directory,
        snapshot_index_limits=[1, 599],
        delete_halos=False,
    ):
        '''
        Delete all snapshots in simulation_directory/snapshot_directory/ that are within
        snapshot_index_limits, except for those in snapshot_indices_subset list.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        snapshot_directory : str
            directory of snapshot files
        snapshot_index_limits : list
            min and max snapshot indices to delete
        delete_halos : bool
            whether to delete halo catalog files at the same snapshots
        '''
        snapshot_name_base = 'snap*_{:03d}*'

        halo_name_base = 'halos_{:03d}*'
        halo_directory = 'halo/rockstar_dm/catalog/'

        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = ut.io.get_path(snapshot_directory)

        if snapshot_index_limits is None or len(snapshot_index_limits) == 0:
            snapshot_index_limits = [1, 599]
        snapshot_indices = np.arange(snapshot_index_limits[0], snapshot_index_limits[1] + 1)

        print()
        for snapshot_index in snapshot_indices:
            if snapshot_index not in snapshot_indices_subset:
                snapshot_name = (
                    simulation_directory
                    + snapshot_directory
                    + snapshot_name_base.format(snapshot_index)
                )
                self.say(f'* deleting:  {snapshot_name}')
                os.system(f'rm -rf {snapshot_name}')

                if delete_halos:
                    halo_name = (
                        simulation_directory
                        + halo_directory
                        + halo_name_base.format(snapshot_index)
                    )
                    self.say(f'* deleting:  {halo_name}')
                    os.system(f'rm -rf {halo_name}')


# --------------------------------------------------------------------------------------------------
# transfer files via globus
# --------------------------------------------------------------------------------------------------
class GlobusClass(ut.io.SayClass):
    '''
    Tranfer files via Globus command-line utility.
    '''

    def submit_transfer(
        self,
        simulation_path_directory=gizmo_default.simulation_directory,
        machine_name='flatiron',
        batch_file_name='globus_batch.txt',
    ):
        '''
        Submit transfer of simulation files via Globus command-line utility.
        Must initiate from Stampede2.

        Install Globus CLI:
            conda install -c conda-forge globus-cli
        Create bookmark:
            globus bookmark create '7961b534-3f0e-11e7-bd15-22000b9a448b:/' stampede
                '0c9d7c36-ea22-11e5-97d6-22000b9da45e:/share/wetzellab/' peloton-scratch
                'a90a2f92-c5ca-11e9-9ced-0edb67dd7a14:/fire2/public_release/' flatiron-fire2-public

        Parameters
        ----------
        simulation_path_directory : str
            '.' or full path + directory of simulation
        machine_name : str
            name of machine transfering files to
        batch_file_name : str
            name of batch file to write
        '''
        # set directory from which to transfer
        simulation_path_directory = ut.io.get_path(simulation_path_directory)
        if simulation_path_directory == './':
            simulation_path_directory = os.getcwd()
        if simulation_path_directory[-1] != '/':
            simulation_path_directory += '/'

        path_directories = simulation_path_directory.split('/')
        simulation_directory = path_directories[-2]

        # set globus transfer command
        command = 'globus transfer --sync-level=checksum --preserve-mtime --verify-checksum'
        command += f' --label "{simulation_directory}" --batch {batch_file_name}'
        # [1:] because preceeding '/' already in globus bookmark
        command += f' $(globus bookmark show stampede){simulation_path_directory[1:]}'

        # parse machine + directory to transfer to
        if machine_name == 'peloton':
            if 'elvis' in simulation_directory:
                simulation_directory_to = 'm12_elvis'
            else:
                simulation_directory_to = simulation_directory.split('_')[0]
            simulation_directory_to += '/' + simulation_directory + '/'

            command += f' $(globus bookmark show peloton-scratch){simulation_directory_to}'

            # write globus batch file
            self.write_globus_batch_file_peloton(simulation_path_directory, batch_file_name)

        elif machine_name == 'flatiron':
            simulation_directory_to = simulation_directory.replace('_r', '_res') + '/'
            if simulation_directory[0] == 'm':
                simulation_directory_to = 'core/' + simulation_directory_to
            elif simulation_directory[0] == 'A':
                simulation_directory_to = 'massive_halo/' + simulation_directory_to
            elif simulation_directory[0] == 'z':
                simulation_directory_to = 'high_redshift/' + simulation_directory_to

            command += f' $(globus bookmark show flatiron-fire2-public){simulation_directory_to}'

            # write globus batch file
            self.write_globus_batch_file_public(simulation_path_directory, batch_file_name)

        self.say(f'* executing:\n{command}\n')
        os.system(command)

    def write_globus_batch_file_peloton(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        batch_file_name='globus_batch.txt',
        snapshot_indices=snapshot_indices_subset,
    ):
        '''
        Write a batch file that sets files to transfer via globus.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        batch_file_name : str
            name of globus batch file in which to write files to transfer
        snapshot_indices : array
            snapshot_indices to transfer
        '''
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = gizmo_default.snapshot_directory
        ic_directory = gizmo_default.ic_directory

        transfer_string = ''

        # files and directories (transfer everything within)
        transfer_items = [
            'gizmo/',
            'Config.sh',
            'gizmo_config.h',
            'GIZMO_config.h',
            'gizmo_parameters.txt',
            'gizmo_parameters.txt-usedvalues',
            'gizmo.out.txt',
            'snapshot_times.txt',
            'notes.txt',
            f'{ic_directory}/',
            'track/',
            'halo/rockstar_dm/catalog_hdf5/',
        ]

        # add these files, and if a directory, everything within
        for transfer_item in transfer_items:
            if os.path.exists(simulation_directory + transfer_item):
                command = '{} {}'
                if transfer_item[-1] == '/':
                    transfer_item = transfer_item[:-1]
                    command += ' --recursive'
                transfer_string += command.format(transfer_item, transfer_item) + '\n'

        """
        # initial condition files
        file_names = glob.glob(simulation_directory + gizmo_default.ic_directory + '*')
        file_names.sort()
        for file_name in file_names:
            if '.ics' not in transfer_item:
                file_name = file_name.replace(simulation_directory, '')
                transfer_string += f'{file_name} {file_name}\n'
        """

        # add snapshot files
        for si in snapshot_indices:
            dir_name = f'{snapshot_directory}' + 'snapdir_{:03d}'.format(si)
            if os.path.exists(simulation_directory + dir_name):
                transfer_string += f'{dir_name} {dir_name} --recursive\n'
            file_name = f'{snapshot_directory}' + 'snapshot_{:03d}.hdf5'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

        with open(batch_file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(transfer_string)

    def write_globus_batch_file_public(
        self,
        simulation_directory=gizmo_default.simulation_directory,
        batch_file_name='globus_batch.txt',
        snapshot_indices=snapshot_indices_public,
    ):
        '''
        Write a batch file that sets files to transfer via globus,
        for FIRE-2 public data release at Flatiron.

        Parameters
        ----------
        simulation_directory : str
            directory of simulation
        batch_file_name : str
            name of globus batch file in which to write files to transfer
        snapshot_indices : array
            snapshot_indices to transfer
        '''
        simulation_directory = ut.io.get_path(simulation_directory)
        snapshot_directory = gizmo_default.snapshot_directory
        ic_directory = gizmo_default.ic_directory
        track_directory = gizmo_default.track_directory
        hosts_coordinates_file_name = gizmo_default.hosts_coordinates_file_name
        rockstar_directory = 'halo/rockstar_dm/'

        transfer_string = ''

        # files and directories (transfer everything within)
        transfer_items = [
            'Config.sh',
            'gizmo_config.h',
            'GIZMO_config.h',
            'gizmo_parameters.txt',
            'gizmo_parameters.txt-usedvalues',
            'snapshot_times.txt',
            f'{ic_directory}',
            f'{track_directory}{hosts_coordinates_file_name}',
            f'{track_directory}star_exsitu_flag_600.txt',
        ]

        # add these files, and if a directory, everything within
        for transfer_item in transfer_items:
            if os.path.exists(simulation_directory + transfer_item):
                command = '{} {}'
                if transfer_item[-1] == '/':
                    transfer_item = transfer_item[:-1]
                    command += ' --recursive'
                transfer_string += command.format(transfer_item, transfer_item) + '\n'

        # add snapshot files
        for si in snapshot_indices:
            dir_name = f'{snapshot_directory}' + 'snapdir_{:03d}'.format(si)
            if os.path.exists(simulation_directory + dir_name):
                transfer_string += f'{dir_name} {dir_name} --recursive\n'
            file_name = f'{snapshot_directory}' + 'snapshot_{:03d}.hdf5'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

        # add track files
        for si in snapshot_indices:
            file_name = f'{track_directory}' + 'star_gas_pointers_{:03d}.hdf5'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

        # add halo files
        for si in snapshot_indices:
            file_name = f'{rockstar_directory}' + 'catalog_hdf5/' + 'halo_{:03d}.hdf5'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

            file_name = f'{rockstar_directory}' + 'catalog_hdf5/' + 'star_{:03d}.hdf5'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

            file_name = f'{rockstar_directory}' + 'catalog/' + 'out_{:03d}.list'.format(si)
            if os.path.exists(simulation_directory + file_name):
                transfer_string += f'{file_name} {file_name}\n'

        with open(batch_file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(transfer_string)


# --------------------------------------------------------------------------------------------------
# transfer files via rsync
# --------------------------------------------------------------------------------------------------
class RsyncClass(ut.io.SayClass):
    '''
    Use rsync to copy simulations files from remote machine to local directory.
    '''

    def __init__(self):
        '''
        .
        '''
        self.rsync_command = 'rsync -ahvP --size-only '
        self.snapshot_name_base = 'snap*_{:03d}*'

    def rsync_snapshot_files(
        self,
        machine_from,
        simulation_directory_from='',
        simulation_directory_to='.',
        snapshot_indices=snapshot_indices_subset,
    ):
        '''
        Use rsync to copy snapshot files from a single simulations directory on a remote machine to
        a local simulation directory.

        Parameters
        ----------
        machine_from : str
            name of (remote) machine to copy from: 'pfe', 'stampede', 'frontera', 'peloton'
        directory_from : str
            directory to copy from
        directory_to : str
            local directory to put snapshots
        snapshot_indices : int or list
            index[s] of snapshots to transfer
        '''
        directory_from = (
            ut.io.get_path(simulation_directory_from) + gizmo_default.snapshot_directory
        )
        directory_to = (
            ut.io.get_path(simulation_directory_to) + gizmo_default.snapshot_directory + '.'
        )

        if np.isscalar(snapshot_indices):
            snapshot_indices = [snapshot_indices]

        snapshot_path_names = ''
        for snapshot_index in snapshot_indices:
            snapshot_path_names += (
                directory_from + self.snapshot_name_base.format(snapshot_index) + ' '
            )

        command = self.rsync_command + f'{machine_from}:"{snapshot_path_names}" {directory_to}'
        self.say(f'\n* executing:\n{command}\n')
        os.system(command)

        # fix file permissions (especially relevant if transfer from Stampede)
        os.system('chmod u=rw,go=r $(find . -type f); chmod u=rwX,go=rX $(find . -type d)')

    def rsync_simulation_files(
        self,
        machine_from,
        directory_from='/scratch/projects/xsede/GalaxiesOnFIRE',
        directory_to='.',
        snapshot_index=None,
    ):
        '''
        Use rsync to copy (non-snapshot) files from remote machine to local directory.
        Directory can be a single simulation directory or a directory of simulation directories.

        Parameters
        ----------
        machine_from : str
            name of (remote) machine to copy from: 'pfe', 'stampede', 'frontera', 'peloton'
        directory_from : str
            directory to copy from
        directory_to : str
            directory to copy files to
        snapshot_index : int
            which snapshot to include
        '''
        include_names = []
        if snapshot_index:
            include_names.append(
                ut.io.get_path(directory_from)
                + gizmo_default.snapshot_directory
                + self.snapshot_name_base.format(snapshot_index)
            )

        exclude_names = [
            #'output/',
            'snapdir_*',
            'snapshot_*.hdf5',
            'ewald_spc_table_64_dbl.dat',
            'spcool_tables/',
            'TREECOOL',
            'restartfiles/',
            'energy.txt',
            'balance.txt',
            'GasReturn.txt',
            'HIIheating.txt',
            'MomWinds.txt',
            'SNeIIheating.txt',
            '*.ics',
            'submit_music*',
            'input_powerspec.txt',
            'snapshot_scalefactors.txt',
            'submit_gizmo*.py',
            '*.bin',
            '*.particles',
            '*.bak',
            '*.err',
            '*.pyc',
            '*.o',
            '*.pro',
            '*.perl',
            '.ipynb_checkpoints',
            '.slurm',
            '.DS_Store',
            '*~',
            '._*',
            '#*#',
        ]

        directory_from = machine_from + ':' + ut.io.get_path(directory_from)
        directory_to = ut.io.get_path(directory_to)

        arguments = ''

        if len(include_names) > 0:
            for include_name in include_names:
                arguments += f'--include="{include_name}" '

        for exclude_name in exclude_names:
            arguments += f'--exclude="{exclude_name}" '

        command = self.rsync_command + arguments + directory_from + ' ' + directory_to + '.'
        self.say(f'\n* executing:\n{command}\n')
        os.system(command)

        # fix file permissions (especially relevant if transfer from Stampede)
        os.system('chmod u=rw,go=r $(find . -type f); chmod u=rwX,go=rX $(find . -type d)')


# --------------------------------------------------------------------------------------------------
# running from command line
# --------------------------------------------------------------------------------------------------
def main():
    '''
    .
    '''
    if len(sys.argv) <= 1:
        raise OSError('specify function to run: compress, clean, archive, delete, globus, rsync')

    function_kind = str(sys.argv[1])

    assert (
        'compress' in function_kind
        or 'clean' in function_kind
        or 'archive' in function_kind
        or 'delete' in function_kind
        or 'rsync' in function_kind
        or 'globus' in function_kind
    )

    if 'compress' in function_kind:
        simulation_directory = '.'
        if len(sys.argv) > 2:
            simulation_directory = str(sys.argv[2])

        snapshot_index_limits = [0, 600]
        if len(sys.argv) > 3:
            snapshot_index_limits[0] = int(sys.argv[3])
            if len(sys.argv) > 4:
                snapshot_index_limits[1] = int(sys.argv[4])

        snapshot_indices = np.arange(snapshot_index_limits[0], snapshot_index_limits[1] + 1)

        Compress = CompressClass()
        Compress.test_compression(simulation_directory, snapshot_indices=snapshot_indices)

    elif 'clean' in function_kind:
        directory = '.'
        if len(sys.argv) > 2:
            directory = str(sys.argv[2])

        Archive = ArchiveClass()
        Archive.clean_directories(directory)

        if 'archive' in function_kind:
            Archive.tar_directories(directory)

    elif 'archive' in function_kind:
        directory = '.'
        if len(sys.argv) > 2:
            directory = str(sys.argv[2])

        Archive = ArchiveClass()
        Archive.tar_directories(directory)

    elif 'delete' in function_kind:
        simulation_directory = '.'
        if len(sys.argv) > 2:
            simulation_directory = str(sys.argv[2])

        snapshot_index_limits = None
        if len(sys.argv) > 3:
            snapshot_index_limits = [int(sys.argv[3]), int(sys.argv[4])]

        Archive = ArchiveClass()
        Archive.delete_snapshots(simulation_directory, snapshot_index_limits=snapshot_index_limits)

    elif 'globus' in function_kind:
        directory = '.'
        if len(sys.argv) > 2:
            directory = str(sys.argv[2])

        Globus = GlobusClass()
        Globus.submit_transfer(directory)

    elif 'rsync' in function_kind:
        if len(sys.argv) < 5:
            raise OSError('imports: machine_from directory_from directory_to')

        machine_from = str(sys.argv[2])
        directory_from = str(sys.argv[3])
        directory_to = str(sys.argv[4])

        Rsync = RsyncClass()
        Rsync.rsync_simulation_files(
            machine_from,
            directory_from,
            directory_to,
            snapshot_index=600,
        )
        Rsync.rsync_snapshot_files(machine_from, directory_from, directory_to)


if __name__ == '__main__':
    main()
