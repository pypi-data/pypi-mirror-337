'''
Plotting analysis of particle data from Gizmo simulations.

@author: Andrew Wetzel <arwetzel@gmail.com>

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

import collections
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib import colors

import utilities as ut
from . import gizmo_default
from . import gizmo_io


# --------------------------------------------------------------------------------------------------
# diagnostic
# --------------------------------------------------------------------------------------------------
def print_properties_statistics(part, species='all'):
    '''
    For each property of each species in particle catalog, print its range and median.

    Parameters
    ----------
    part : dict
        catalog of particles (use this instead of reading in)
    species : str or list
        name[s] of particle species to print
    '''
    Say = ut.io.SayClass(print_properties_statistics)

    species = ut.array.arrayize(species)
    if 'all' in species:
        species = ['dark2', 'dark', 'star', 'gas']

    species_print = [s for s in species if s in list(part)]

    species_property_dict = collections.OrderedDict()
    species_property_dict['dark2'] = ['id', 'position', 'velocity', 'mass']
    species_property_dict['dark'] = ['id', 'position', 'velocity', 'mass']
    species_property_dict['star'] = [
        'id',
        'id.child',
        'id.generation',
        'position',
        'velocity',
        'mass',
        'form.scalefactor',
        'massfraction.hydrogen',
        'massfraction.helium',
        'massfraction.metals',
    ]
    species_property_dict['gas'] = [
        'id',
        'id.child',
        'id.generation',
        'position',
        'velocity',
        'mass',
        'number.density',
        'size',
        'temperature',
        'hydrogen.neutral.fraction',
        'sfr',
        'massfraction.hydrogen',
        'massfraction.helium',
        'massfraction.metals',
    ]

    # Statistic = ut.math.StatisticClass()

    Say.say('printing minimum, median, maximum')
    for spec_name in species_print:
        Say.say(f'\n* {spec_name}')
        for prop_name in species_property_dict[spec_name]:
            try:
                prop_values = part[spec_name].prop(prop_name)
            except KeyError:
                Say.say(f'{prop_name} not in catalog')
                continue

            # Statistic.stat = Statistic.get_statistic_dict(prop_values)
            # Statistic.print_statistics()

            if 'int' in str(prop_values.dtype):
                number_format = '{:.0f}'
            elif np.abs(prop_values).max() < 1e5:
                number_format = '{:.4f}'
            else:
                number_format = '{:.1e}'

            print_string = f'{prop_name}: {number_format}, {number_format}, {number_format}'

            Say.say(
                print_string.format(prop_values.min(), np.median(prop_values), prop_values.max())
            )


# --------------------------------------------------------------------------------------------------
# visualize
# --------------------------------------------------------------------------------------------------
class ImageClass(ut.io.SayClass):
    '''
    Plot 2-D image[s], save values, write to file.
    '''

    def __init__(self):
        '''
        .
        '''
        self.histogram_valuess = None
        self.histogram_xs = None
        self.histogram_ys = None
        self.plot_file_name = None

    def plot_image_simple(
        self,
        part,
        species_name='star',
        weight_name='mass',
        dimensions_plot=[0, 1, 2],
        distance_max=20,
        distance_bin_width=0.1,
        rotation=True,
        host_index=0,
        part_indices=None,
        image_limits=[None, None],
        plot_file=False,
    ):
        '''
        Plot image of the positions of given partcle species, using either a single panel for
        2 dimensions or 3 panels for all 2-dimensional combinations.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species to plot
        weight_name : str
            property to weight positions by
        dimensions_plot : list
            dimensions to plot - if length 2, plot one v one; if length 3, plot all via 3 panels
        distance_max : float or array
            distance from center to plot [kpc]
        distance_bin_width : float
            size of pixel [kpc]
        rotation : bool or array
            whether to rotate particles
            if True, will rotate to align with principal axes defined by input species
        host_index : int
            index of host halo to get position and rotation of (if not input them)
        part_indices : array
            input selection indices for particles
        image_limits : list
            min and max limits to impose on image dynamic range (exposure)
        plot_file : bool
            whether to write figure to file and its name
        '''
        dimen_label = {0: 'x', 1: 'y', 2: 'z'}

        position_limits = [[-distance_max, distance_max] for _ in range(3)]
        position_limits = np.array(position_limits)

        if part_indices is None or len(part_indices) == 0:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        host_name = ut.catalog.get_host_name(host_index)

        if rotation is True:
            # rotate according to principal axes
            positions = part[species_name].prop(f'{host_name}.distance.principal', part_indices)
        else:
            # positions in (arbitrary) Cartesian x,y,z of simulation
            positions = part[species_name].prop(f'{host_name}.distance', part_indices)

        weights = None
        if weight_name:
            weights = part[species_name].prop(weight_name, part_indices)

        # keep only particles within distance limits
        masks = positions[:, dimensions_plot[0]] <= distance_max
        for dimen_i in dimensions_plot:
            masks *= (positions[:, dimen_i] >= -distance_max) * (
                positions[:, dimen_i] <= distance_max
            )

        positions = positions[masks]
        if weights is not None:
            weights = weights[masks]

        position_bin_number = int(np.round(2 * np.max(distance_max) / distance_bin_width))

        # set color map
        if 'dark' in species_name or species_name == 'gas' or species_name == 'star':
            color_map = plt.cm.afmhot  # pylint: disable=no-member

        # set interpolation method
        interpolation = 'bilinear'

        if len(dimensions_plot) == 2:
            fig, subplot = ut.plot.make_figure(
                1,
                left=0.22,
                right=0.98,
                bottom=0.15,
                top=0.98,
                background_color='black',
            )

            subplot.set_xlim(position_limits[dimensions_plot[0]])
            subplot.set_ylim(position_limits[dimensions_plot[1]])

            subplot.set_xlabel(f'{dimen_label[dimensions_plot[0]]} $\\left[ {{\\rm kpc}} \\right]$')
            subplot.set_ylabel(f'{dimen_label[dimensions_plot[1]]} $\\left[ {{\\rm kpc}} \\right]$')

            hist_valuess, _hist_xs, _hist_ys, hist_limits = self.get_histogram(
                'histogram',
                dimensions_plot,
                position_bin_number,
                position_limits,
                positions,
                weights,
            )

            image_limits_use = hist_limits
            if image_limits is not None and len(image_limits) > 0:
                if image_limits[0] is not None:
                    image_limits_use[0] = image_limits[0]
                if image_limits[1] is not None:
                    image_limits_use[1] = image_limits[1]

            _Image = subplot.imshow(
                hist_valuess.transpose(),
                norm=colors.LogNorm(),
                cmap=color_map,
                aspect='auto',
                interpolation=interpolation,
                extent=np.concatenate(position_limits[dimensions_plot]),
                vmin=image_limits[0],
                vmax=image_limits[1],
            )

            fig.colorbar(_Image)

            fig.gca().set_aspect('equal')

        elif len(dimensions_plot) == 3:
            fig, subplots = ut.plot.make_figure(
                1,
                [2, 2],
                left=0.22,
                right=0.97,
                bottom=0.16,
                top=0.97,
                background_color='black',
            )

            plot_dimension_iss = [
                [dimensions_plot[0], dimensions_plot[1]],
                [dimensions_plot[0], dimensions_plot[2]],
                [dimensions_plot[1], dimensions_plot[2]],
            ]

            subplot_iss = [[0, 0], [1, 0], [1, 1]]

            histogram_valuesss = []
            for plot_i, plot_dimension_is in enumerate(plot_dimension_iss):
                subplot_is = subplot_iss[plot_i]
                subplot = subplots[subplot_is[0], subplot_is[1]]

                hist_valuess, _hist_xs, _hist_ys, hist_limits = self.get_histogram(
                    'histogram',
                    plot_dimension_is,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                )

                histogram_valuesss.append(hist_valuess)

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                # ensure that tick labels do not overlap
                subplot.set_xlim(position_limits[plot_dimension_is[0]])
                subplot.set_ylim(position_limits[plot_dimension_is[1]])

                units_label = ' $\\left[ {\\rm kpc} \\right]$'
                if subplot_is == [0, 0]:
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 0]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 1]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    # aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[plot_dimension_is]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

            if part.info['simulation.name']:
                ut.plot.make_label_legend(subplots[0, 1], part.info['simulation.name'])

            hist_valuess = np.array(histogram_valuesss)

        if plot_file:
            plt.savefig('image.pdf', format='pdf')
        plt.show(block=False)

    def plot_image(
        self,
        part,
        species_name='star',
        weight_name='mass',
        image_kind='histogram',
        dimensions_plot=[0, 1, 2],
        dimensions_select=[0, 1, 2],
        distances_max=20,
        distance_bin_width=0.1,
        distance_bin_number=None,
        center_position=None,
        rotation=None,
        host_index=0,
        property_select={},
        part_indices=None,
        subsample_factor=None,
        use_column_units=None,
        image_limits=[None, None],
        background_color='black',
        hal=None,
        hal_indices=None,
        hal_position_kind='position',
        hal_radius_kind='radius',
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot image of the positions of given partcle species, using either a single panel for
        2 dimensions or 3 panels for all axis permutations.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species to plot
        weight_name : str
            property to weight positions by
        image_kind : str
            'histogram', 'histogram.3d', 'points'
        dimensions_plot : list
            dimensions to plot - if length 2, plot one v one; if length 3, plot all via 3 panels
        dimensions_select : list
            dimensions to use to select particles
            use this to set selection 'depth' of an image
        distances_max : float or array
            distance[s] from center to plot and/or cut [kpc]
        distance_bin_width : float
            size of pixel [kpc]
        distance_bin_number : int
            number of pixels from distance = 0 to max (2x this across image)
        center_position : array-like
            position of center
        rotation : bool or array
            whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes defined by input species
        host_index : int
            index of host halo to get position and rotation of (if not input them)
        property_select : dict
            (other) properties to select on: names as keys and limits as values
        part_indices : array
            input selection indices for particles
        subsample_factor : int
            factor by which periodically to sub-sample particles
        use_column_units : bool
            whether to convert to particle number / cm^2
        image_limits : list
            min and max limits to impose on image dynamic range (exposure)
        background_color : str
            name of color for background: 'white', 'black'
        hal : dict
            catalog of halos at snapshot
        hal_indices : array
            indices of halos to plot
        hal_position_kind : str
            name of position to use for center of halo
        hal_radius_kind : str
            name of radius to use for size of halo
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            path + directory where to write file
            if ends in '.pdf', override default file naming convention and use input name
        figure_index : int
            index of figure for matplotlib
        '''
        dimen_label = {0: 'x', 1: 'y', 2: 'z'}

        if dimensions_select is None or len(dimensions_select) == 0:
            dimensions_select = dimensions_plot

        if np.isscalar(distances_max):
            distances_max = [
                distances_max for dimen_i in range(part[species_name]['position'].shape[1])
            ]
        distances_max = np.array(distances_max, dtype=np.float64)

        position_limits = []
        for dimen_i in range(distances_max.shape[0]):
            position_limits.append([-distances_max[dimen_i], distances_max[dimen_i]])
        position_limits = np.array(position_limits)

        if part_indices is None or len(part_indices) == 0:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        if subsample_factor is not None and subsample_factor > 1:
            part_indices = part_indices[::subsample_factor]

        positions = np.array(part[species_name]['position'][part_indices])
        weights = None
        if weight_name:
            weights = part[species_name].prop(weight_name, part_indices)

        center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

        if center_position is not None and len(center_position) > 0:
            # re-orient to input center
            positions -= center_position
            positions *= part.snapshot['scalefactor']

            if rotation is not None:
                # rotate image
                if rotation is True:
                    # rotate according to principal axes
                    rotation_tensor = ut.particle.parse_property(part, 'rotation', None, host_index)
                elif len(rotation) > 0:
                    # use input rotation vectors
                    rotation_tensor = np.asarray(rotation)
                    if (
                        np.ndim(rotation_tensor) != 2
                        or rotation_tensor.shape[0] != positions.shape[1]
                        or rotation_tensor.shape[1] != positions.shape[1]
                    ):
                        raise ValueError(f'wrong shape for rotation = {rotation}')
                else:
                    raise ValueError(f'cannot parse rotation = {rotation}')

                positions = ut.coordinate.get_coordinates_rotated(positions, rotation_tensor)

            # keep only particles within distance limits
            masks = positions[:, dimensions_select[0]] <= distances_max[0]
            for dimen_i in dimensions_select:
                masks *= (positions[:, dimen_i] >= -distances_max[dimen_i]) * (
                    positions[:, dimen_i] <= distances_max[dimen_i]
                )

            positions = positions[masks]
            if weights is not None:
                weights = weights[masks]
        else:
            raise ValueError('need to input center_position')

        if distance_bin_width is not None and distance_bin_width > 0:
            position_bin_number = int(
                np.round(2 * np.max(distances_max[dimensions_plot]) / distance_bin_width)
            )
        elif distance_bin_number is not None and distance_bin_number > 0:
            position_bin_number = 2 * distance_bin_number
        else:
            raise ValueError('need to input either distance bin width or bin number')

        if hal is not None:
            # compile halos
            if hal_indices is None or len(hal_indices) == 0:
                hal_indices = ut.array.get_arange(hal['mass'])

            if 0 not in hal_indices:
                hal_indices = np.append(np.array([0], hal_indices.dtype), hal_indices)

            hal_positions = np.array(hal[hal_position_kind][hal_indices])
            if center_position is not None and len(center_position) > 0:
                hal_positions -= center_position
            hal_positions *= hal.snapshot['scalefactor']
            hal_radiuss = hal[hal_radius_kind][hal_indices]

            # initialize masks
            masks = hal_positions[:, dimensions_select[0]] <= distances_max[0]
            for dimen_i in dimensions_select:
                masks *= (hal_positions[:, dimen_i] >= -distances_max[dimen_i]) * (
                    hal_positions[:, dimen_i] <= distances_max[dimen_i]
                )

            hal_radiuss = hal_radiuss[masks]
            hal_positions = hal_positions[masks]

        # plot ----------
        # BYW = colors.LinearSegmentedColormap('byw', ut.plot.color_map_dict['BlackYellowWhite'])
        # plt.register_cmap(cmap=BYW)
        # BBW = colors.LinearSegmentedColormap('bbw', ut.plot.color_map_dict['BlackBlueWhite'])
        # plt.register_cmap(cmap=BBW)

        # set color map
        if background_color == 'black':
            if 'dark' in species_name:
                # color_map = plt.get_cmap('bbw')
                color_map = plt.cm.afmhot  # pylint: disable=no-member
            elif species_name == 'gas':
                color_map = plt.cm.afmhot  # pylint: disable=no-member
            elif species_name == 'star':
                # color_map = plt.get_cmap('byw')
                color_map = plt.cm.afmhot  # pylint: disable=no-member
        elif background_color == 'white':
            color_map = plt.cm.YlOrBr  # pylint: disable=no-member

        # set interpolation method
        # interpolation='nearest'
        interpolation = 'bilinear'
        # interpolation='bicubic'
        # interpolation='gaussian'

        if len(dimensions_plot) == 2:
            fig, subplot = ut.plot.make_figure(
                figure_index,
                left=0.22,
                right=0.98,
                bottom=0.15,
                top=0.98,
                background_color=background_color,
            )

            subplot.set_xlim(position_limits[dimensions_plot[0]])
            subplot.set_ylim(position_limits[dimensions_plot[1]])

            subplot.set_xlabel(f'{dimen_label[dimensions_plot[0]]} $\\left[ {{\\rm kpc}} \\right]$')
            subplot.set_ylabel(f'{dimen_label[dimensions_plot[1]]} $\\left[ {{\\rm kpc}} \\right]$')

            if 'histogram' in image_kind:
                hist_valuess, hist_xs, hist_ys, hist_limits = self.get_histogram(
                    image_kind,
                    dimensions_plot,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                    use_column_units,
                )

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[dimensions_plot]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

                # standard method
                # hist_valuess, hist_xs, hist_ys, _Image = subplot.hist2d(
                #    positions[:, dimensions_plot[0]], positions[:, dimensions_plot[1]],
                #    weights=weights, range=position_limits, bins=position_bin_number,
                #    norm=colors.LogNorm(),
                #    cmap=color_map,
                #    vmin=image_limits[0], vmax=image_limits[1],
                # )

                # plot average of property
                # hist_valuess = ut.math.Fraction.get_fraction(hist_valuess, grid_number)
                # subplot.imshow(
                #    hist_valuess.transpose(),
                #    #norm=colors.LogNorm(),
                #    cmap=color_map,
                #    aspect='auto',
                #    interpolation=interpolation,
                #    extent=np.concatenate(position_limits),
                #    vmin=np.min(weights), vmax=np.max(weights),
                # )

                fig.colorbar(_Image)

            elif image_kind == 'points':
                subplot.scatter(
                    positions[:, dimensions_plot[0]],
                    positions[:, dimensions_plot[1]],
                    marker='o',
                    c=weights,
                )
                # , markersize=2.0, markeredgecolor='red', markeredgewidth=0,
                # color='red', alpha=0.02)

            fig.gca().set_aspect('equal')

            # plot halos
            if hal is not None:
                for hal_position, hal_radius in zip(hal_positions, hal_radiuss):
                    print(hal_position, hal_radius)
                    circle = plt.Circle(
                        hal_position[dimensions_plot],
                        hal_radius,
                        color='w',
                        linewidth=1,
                        fill=False,
                    )
                    subplot.add_artist(circle)

        elif len(dimensions_plot) == 3:
            fig, subplots = ut.plot.make_figure(
                figure_index,
                [2, 2],
                left=0.22,
                right=0.97,
                bottom=0.16,
                top=0.97,
                background_color=background_color,
            )

            plot_dimension_iss = [
                [dimensions_plot[0], dimensions_plot[1]],
                [dimensions_plot[0], dimensions_plot[2]],
                [dimensions_plot[1], dimensions_plot[2]],
            ]

            subplot_iss = [[0, 0], [1, 0], [1, 1]]

            histogram_valuesss = []
            for plot_i, plot_dimension_is in enumerate(plot_dimension_iss):
                subplot_is = subplot_iss[plot_i]
                subplot = subplots[subplot_is[0], subplot_is[1]]

                hist_valuess, hist_xs, hist_ys, hist_limits = self.get_histogram(
                    image_kind,
                    plot_dimension_is,
                    position_bin_number,
                    position_limits,
                    positions,
                    weights,
                    use_column_units,
                )

                histogram_valuesss.append(hist_valuess)

                image_limits_use = hist_limits
                if image_limits is not None and len(image_limits) > 0:
                    if image_limits[0] is not None:
                        image_limits_use[0] = image_limits[0]
                    if image_limits[1] is not None:
                        image_limits_use[1] = image_limits[1]

                # ensure that tick labels do not overlap
                subplot.set_xlim(position_limits[plot_dimension_is[0]])
                subplot.set_ylim(position_limits[plot_dimension_is[1]])

                units_label = ' $\\left[ {\\rm kpc} \\right]$'
                if subplot_is == [0, 0]:
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 0]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)
                    subplot.set_ylabel(dimen_label[plot_dimension_is[1]] + units_label)
                elif subplot_is == [1, 1]:
                    subplot.set_xlabel(dimen_label[plot_dimension_is[0]] + units_label)

                _Image = subplot.imshow(
                    hist_valuess.transpose(),
                    norm=colors.LogNorm(),
                    cmap=color_map,
                    # aspect='auto',
                    interpolation=interpolation,
                    extent=np.concatenate(position_limits[plot_dimension_is]),
                    vmin=image_limits[0],
                    vmax=image_limits[1],
                )

                # default method
                # hist_valuess, hist_xs, hist_ys, _Image = subplot.hist2d(
                #    positions[:, plot_dimension_is[0]], positions[:, plot_dimension_is[1]],
                #    norm=colors.LogNorm(),
                #    weights=weights,
                #    range=position_limits, bins=position_bin_number,
                #    cmap=color_map
                # )

                # fig.colorbar(_Image)  # , ax=subplot)

                # plot halos
                if hal is not None:
                    for hal_position, hal_radius in zip(hal_positions, hal_radiuss):
                        circle = plt.Circle(
                            hal_position[plot_dimension_is],
                            hal_radius,
                            color='w',
                            linewidth=1,
                            fill=False,
                        )
                        subplot.add_artist(circle)

                    circle = plt.Circle((0, 0), 10, color='w', fill=False)
                    subplot.add_artist(circle)

                # subplot.axis('equal')
                # fig.gca().set_aspect('equal')

            if part.info['simulation.name']:
                ut.plot.make_label_legend(subplots[0, 1], part.info['simulation.name'])

            hist_valuess = np.array(histogram_valuesss)

        # get name and directory to write plot file
        if '.pdf' in plot_directory:
            # use input file name, write in current directory
            plot_file_name = plot_directory
            plot_directory = '.'
        elif plot_file_name is True or plot_file_name == '':
            # generate default file name
            prefix = part.info['simulation.name']

            prop = 'position'
            for dimen_i in dimensions_plot:
                prop += '.' + dimen_label[dimen_i]
            prop += '_d.{:.0f}'.format(np.max(distances_max[dimensions_plot]))

            plot_file_name = ut.plot.get_file_name(
                weight_name, prop, species_name, 'redshift', part.snapshot, prefix=prefix
            )

            # if 'histogram' in image_kind:
            #    plot_file_name += '_i.{:.1f}-{:.1f}'.format(
            #        np.log10(image_limits_use[0]), np.log10(image_limits_use[1])
            #    )
        ut.plot.parse_output(plot_file_name, plot_directory)

        self.histogram_valuess = hist_valuess
        self.histogram_xs = hist_xs
        self.histogram_ys = hist_ys
        self.plot_file_name = plot_file_name

    def get_histogram(
        self,
        image_kind,
        dimension_list,
        position_bin_number,
        position_limits,
        positions,
        weights,
        use_column_units=False,
    ):
        '''
        Get 2-D histogram, either by summing all partiles along 3rd dimension or computing the
        highest density along 3rd dimension.

        Parameters
        ----------
        image_kind : str
            'histogram', 'histogram.3d'
        dimension_list : list
            indices of dimensions to plot
            if length 2, plot one v other, if length 3, plot all via 3 panels
        position_bin_number : int
            number of pixels/bins across image
        position_limits : list or list of lists
            min and max values of position to compute
        positions : array
            3-D positions
        weights : array
            weight for each position
        use_column_units : bool
            whether to convert to [number / cm^2]
        '''
        if '3d' in image_kind:
            # calculate maximum local density along projected dimension
            hist_valuess, (hist_xs, hist_ys, hist_zs) = np.histogramdd(
                positions, position_bin_number, position_limits, weights=weights
            )
            # convert to 3-d density
            hist_valuess /= np.diff(hist_xs)[0] * np.diff(hist_ys)[0] * np.diff(hist_zs)[0]

            dimension_project = np.setdiff1d([0, 1, 2], dimension_list)

            # compute maximum density
            hist_valuess = np.max(hist_valuess, dimension_project)

        else:
            # project along single dimension
            hist_valuess, hist_xs, hist_ys = np.histogram2d(
                positions[:, dimension_list[0]],
                positions[:, dimension_list[1]],
                position_bin_number,
                position_limits[dimension_list],
                weights=weights,
            )

            # convert to surface density
            hist_valuess /= np.diff(hist_xs)[0] * np.diff(hist_ys)[0]

            # convert to number density
            if use_column_units:
                hist_valuess *= ut.constant.hydrogen_per_sun * ut.constant.kpc_per_cm**2
                grid_number = hist_valuess.size
                lls_number = np.sum((hist_valuess > 1e17) * (hist_valuess < 2e20))
                dla_number = np.sum(hist_valuess > 2e20)
                self.say(
                    'covering fraction: LLS = {:.2e}, DLA = {:.2e}'.format(
                        lls_number / grid_number, dla_number / grid_number
                    )
                )

        masks = hist_valuess > 0
        self.say(
            'histogram min, med, max = {:.3e}, {:.3e}, {:.3e}'.format(
                hist_valuess[masks].min(), np.median(hist_valuess[masks]), hist_valuess[masks].max()
            )
        )

        hist_limits = np.array([hist_valuess[masks].min(), hist_valuess[masks].max()])

        return hist_valuess, hist_xs, hist_ys, hist_limits

    def print_values(self):
        '''
        Write 2-D histogram values of image to file.
        '''
        file_name = self.plot_file_name + '.txt'

        with open(file_name, 'w', encoding='utf-8') as file_out:
            Write = ut.io.WriteClass(file_out, print_stdout=False)
            Write.write(
                '# pixel (smoothing) scale is {:.2f} kpc'.format(
                    self.histogram_xs[1] - self.histogram_xs[0]
                )
            )
            for ix in range(self.histogram_xs.size - 1):
                x = self.histogram_xs[ix] + 0.5 * (
                    self.histogram_xs[ix + 1] - self.histogram_xs[ix]
                )
                for iy in range(self.histogram_ys.size - 1):
                    y = self.histogram_ys[iy] + 0.5 * (
                        self.histogram_ys[iy + 1] - self.histogram_ys[iy]
                    )
                    Write.write(
                        '{:.3f} {:.3f} {:.3e} {:.3e} {:.3e}'.format(
                            x,
                            y,
                            self.histogram_valuess[0, ix, iy],
                            self.histogram_valuess[1, ix, iy],
                            self.histogram_valuess[2, ix, iy],
                        )
                    )


Image = ImageClass()


# --------------------------------------------------------------------------------------------------
# general properties
# --------------------------------------------------------------------------------------------------
def plot_property_distribution(
    parts,
    species_name='gas',
    property_name='density',
    property_limits=None,
    property_bin_width=None,
    property_bin_number=100,
    property_log_scale=True,
    property_statistic='probability',
    weight_property=None,
    distance_limits=None,
    center_positions=None,
    center_velocities=None,
    host_index=0,
    property_select={},
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=None,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of property.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_bin_number : int
        number of bins within limits (use this or property_bin_width)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str
        statistic to plot: 'probability', 'probability.cum', 'probability.norm', 'histogram',
        'histogram.cum'
    weight_property : str
        property to weight each particle by
    distance_limits : list
        min and max limits for distance from galaxy
    center_positions : array or list of arrays
        position[s] of galaxy center[s]
    center_velocities : array or list of arrays
        velocity[s] of galaxy center[s]
    host_index : int
        index of host halo to get position and velocity of (if not input)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write plot file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_property_distribution)

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)
    if 'velocity' in property_name:
        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        if distance_limits:
            # [kpc physical]
            distances = ut.coordinate.get_distances(
                part[species_name]['position'][part_indices],
                center_positions[part_i],
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )
            part_indices = part_indices[ut.array.get_indices(distances, distance_limits)]

        if 'velocity' in property_name:
            orb = ut.particle.get_orbit_dictionary(
                part,
                species_name,
                part_indices,
                center_positions[part_i],
                center_velocities[part_i],
                host_index,
            )
            prop_values = orb[property_name]
        else:
            prop_values = part[species_name].prop(property_name, part_indices)

        if weight_property is not None and len(weight_property):
            weights = part[species_name].prop(weight_property, part_indices)
        else:
            weights = None

        Say.say(f'keeping {prop_values.size} {species_name} particles')

        Stat.append_to_dictionary(
            prop_values,
            property_limits,
            property_bin_width,
            property_bin_number,
            property_log_scale,
            weights,
        )

        Stat.print_statistics(-1)
        print()

    color_names = ut.plot.get_colors(len(parts))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array([Stat.distr[property_statistic][part_i] for part_i in range(len(parts))])

    ut.plot.set_axes_scaling_limits(
        subplot,
        property_log_scale,
        property_limits,
        prop_values,
        axis_y_log_scale,
        axis_y_limits,
        y_values,
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, property_log_scale, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        subplot.plot(
            Stat.distr['bin.mid'][part_i],
            Stat.distr[property_statistic][part_i],
            color=color_names[part_i],
            alpha=0.8,
            label=part.info['simulation.name'],
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_density_distribution(
    parts,
    species_name='gas',
    property_name='number.density',
    property_limits=[0.1, 1e5],
    property_bin_width=0.1,
    property_log_scale=True,
    property_statistic='probability',
    weight_properties=['mass', 'sfr'],
    property_select={
        'host.distance.principal.cylindrical.rad': [0, 15],
        'host.distance.principal.cylindrical.vert': [-3, 3],
    },
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=None,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of gas density.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str
        statistic to plot: 'probability', 'probability.cum', 'probability.norm', 'histogram',
        'histogram.cum'
    weight_property : str or list
        property[s] to weight each particle by
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write plot file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_property_distribution)

    if isinstance(parts, dict):
        parts = [parts]
    if np.isscalar(weight_properties):
        weight_properties = [weight_properties]

    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        prop_values = part[species_name].prop(property_name, part_indices)

        Say.say(f'keeping {prop_values.size} {species_name} particles')

        for weight_property in weight_properties:
            weights = part[species_name].prop(weight_property, part_indices)

            Stat.append_to_dictionary(
                prop_values,
                property_limits,
                property_bin_width,
                None,
                property_log_scale,
                weights,
            )

            # Stat.print_statistics(-1)
            # print()

    color_names = ut.plot.get_colors(len(parts))
    line_styles = ut.plot.get_line_styles(len(weight_properties))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array(
        [Stat.distr[property_statistic][i] for i in range(len(parts) * len(weight_properties))]
    )

    ut.plot.set_axes_scaling_limits(
        subplot,
        property_log_scale,
        property_limits,
        prop_values,
        axis_y_log_scale,
        axis_y_limits,
        y_values,
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, property_log_scale, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        for weight_i, weight_property in enumerate(weight_properties):
            i = part_i * 2 + weight_i
            subplot.plot(
                Stat.distr['bin.mid'][i],
                Stat.distr[property_statistic][i],
                color=color_names[part_i],
                linestyle=line_styles[weight_i],
                alpha=0.8,
                label=part.info['simulation.name'],
            )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_velocity_v_age(
    part,
    species_name='star',
    x_property_name='age',
    x_property_limits=[0, 13.5],
    x_property_bin_width=0.25,
    x_property_log_scale=False,
    y_property_limits=[0, 70],
    y_property_log_scale=False,
    center_position=None,
    host_index=0,
    part_indices=None,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    .
    '''
    center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

    if part_indices is None or len(part_indices) == 0:
        part_indices = ut.array.get_arange(part[species_name].prop(x_property_name))

    distances = part[species_name].prop('host.distance.principal.cylindridal', part_indices)
    part_indices = ut.array.get_indices(distances[:, 0], [7, 9], part_indices)
    part_indices = ut.array.get_indices(distances[:, 2], [-1, 1], part_indices)

    y_prop_values = part[species_name].prop('host.velocity.principal.cylindrical', part_indices)[
        :, 2
    ]

    Bin = ut.binning.BinClass(
        x_property_limits, x_property_bin_width, log_scale=x_property_log_scale
    )

    ages = part[species_name].prop(x_property_name, part_indices)
    ages_future = ages * 10 ** np.random.normal(0, 0.04, ages.size)
    ages_now = ages * 10 ** np.random.normal(0, 0.08, ages.size)
    ages_past = ages * 10 ** np.random.normal(0, 0.18, ages.size)

    stat = Bin.get_statistics_of_array(ages, y_prop_values)
    stat_future = Bin.get_statistics_of_array(ages_future, y_prop_values)
    stat_now = Bin.get_statistics_of_array(ages_now, y_prop_values)
    stat_past = Bin.get_statistics_of_array(ages_past, y_prop_values)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        x_property_log_scale,
        x_property_limits,
        ages,
        y_property_log_scale,
        y_property_limits,
        y_prop_values,
    )

    # if x_property_log_scale:
    #    _x_prop_values = ut.math.get_log(ages)
    if y_property_log_scale:
        y_prop_values = ut.math.get_log(y_prop_values)

    axis_x_label = ut.plot.Label.get_label(
        x_property_name, species_name=species_name, get_words=True
    )
    subplot.set_xlabel(axis_x_label)
    subplot.set_ylabel('$\\sigma_v$ [km/s]')

    color_names = ut.plot.get_colors(4)

    stat_name = 'std'
    subplot.plot(
        stat['bin.mid'], 0.5 * stat[stat_name], color='black', alpha=0.7, label='no age uncertainty'
    )
    subplot.plot(
        stat['bin.mid'],
        0.5 * stat_future[stat_name],
        color=color_names[1],
        alpha=0.7,
        label='10% age uncertainty',
    )
    subplot.plot(
        stat['bin.mid'],
        0.5 * stat_now[stat_name],
        color=color_names[2],
        alpha=0.7,
        label='20% age uncertainty',
    )
    subplot.plot(
        stat['bin.mid'],
        0.5 * stat_past[stat_name],
        color=color_names[3],
        alpha=0.7,
        label='50% age uncertainty',
    )

    ut.plot.make_legends(subplot)

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = 'test'
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_property_v_property(
    part,
    species_name='gas',
    x_property_name='number.density',
    x_property_limits=None,
    x_property_log_scale=True,
    y_property_name='temperature',
    y_property_limits=None,
    y_property_log_scale=True,
    property_bin_number=150,
    weight_property='mass',
    cut_percent=0,
    host_distance_limits=[0, 300],
    center_position=None,
    host_index=0,
    property_select={},
    part_indices=None,
    draw_statistics=False,
    plot_file_name=False,
    plot_directory='.',
    add_simulation_name=False,
    figure_index=1,
):
    '''
    Plot property v property.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    x_property_name : str
        property name for x-axis
    x_property_limits : list
        min and max limits to impose on x_property_name
    x_property_log_scale : bool
        whether to use logarithmic scaling for x axis
    y_property_name : str
        property name for y-axis
    y_property_limits : list
        min and max limits to impose on y_property_name
    y_property_log_scale : bool
        whether to use logarithmic scaling for y axis
    property_bin_number : int
        number of bins for histogram along each axis
    weight_property : str
        property to weight each particle by
    host_distance_limits : list
        min and max limits for distance from galaxy
    center_position : array
        position of galaxy center
    host_index : int
        index of host galaxy/halo to get position of (if not input)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indices : array
        indices of particles from which to select
    draw_statistics : bool
        whether to draw statistics (such as median) on figure
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    add_simulation_name : bool
        whether to add name of simulation to figure name
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_property_v_property)

    center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

    if part_indices is None or len(part_indices) == 0:
        part_indices = ut.array.get_arange(part[species_name].prop(x_property_name))

    if property_select:
        part_indices = ut.catalog.get_indices_catalog(
            part[species_name], property_select, part_indices
        )

    if (
        len(center_position) > 0
        and host_distance_limits is not None
        and len(host_distance_limits) > 0
    ):
        distances = ut.coordinate.get_distances(
            part[species_name]['position'][part_indices],
            center_position,
            part.info['box.length'],
            part.snapshot['scalefactor'],
            total_distance=True,
        )  # [kpc phy]
        part_indices = part_indices[ut.array.get_indices(distances, host_distance_limits)]

    x_prop_values = part[species_name].prop(x_property_name, part_indices)
    y_prop_values = part[species_name].prop(y_property_name, part_indices)
    weights = None
    if weight_property is not None and len(weight_property) > 0:
        weights = part[species_name].prop(weight_property, part_indices)

    part_indices = ut.array.get_arange(part_indices)

    if x_property_limits:
        part_indices = ut.array.get_indices(x_prop_values, x_property_limits, part_indices)

    if y_property_limits:
        part_indices = ut.array.get_indices(y_prop_values, y_property_limits, part_indices)

    if cut_percent > 0:
        x_limits = ut.array.get_limits(x_prop_values[part_indices], cut_percent=cut_percent)
        y_limits = ut.array.get_limits(y_prop_values[part_indices], cut_percent=cut_percent)
        part_indices = ut.array.get_indices(x_prop_values, x_limits, part_indices)
        part_indices = ut.array.get_indices(y_prop_values, y_limits, part_indices)

    x_prop_values = x_prop_values[part_indices]
    y_prop_values = y_prop_values[part_indices]
    if weight_property is not None and len(weight_property) > 0:
        weights = weights[part_indices]

    Say.say(f'keeping {x_prop_values.size} particles')

    if draw_statistics:
        stat_bin_number = int(np.round(property_bin_number / 10))
        Bin = ut.binning.BinClass(
            x_property_limits, None, stat_bin_number, False, x_property_log_scale
        )
        stat = Bin.get_statistics_of_array(x_prop_values, y_prop_values)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    axis_x_limits, axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        x_property_log_scale,
        x_property_limits,
        x_prop_values,
        y_property_log_scale,
        y_property_limits,
        y_prop_values,
    )

    axis_x_label = ut.plot.Label.get_label(
        x_property_name, species_name=species_name, get_words=True
    )
    subplot.set_xlabel(axis_x_label)

    axis_y_label = ut.plot.Label.get_label(
        y_property_name, species_name=species_name, get_words=True
    )
    subplot.set_ylabel(axis_y_label)

    if x_property_log_scale:
        axis_x_log_limits = ut.math.get_log(axis_x_limits)
        axis_x_bins = np.logspace(axis_x_log_limits[0], axis_x_log_limits[1], property_bin_number)
    else:
        axis_x_bins = np.linspace(axis_x_limits[0], axis_x_limits[1], property_bin_number)
    if y_property_log_scale:
        axis_y_log_limits = ut.math.get_log(axis_y_limits)
        axis_y_bins = np.logspace(axis_y_log_limits[0], axis_y_log_limits[1], property_bin_number)
    else:
        axis_y_bins = np.linspace(axis_y_limits[0], axis_y_limits[1], property_bin_number)

    color_map = plt.cm.inferno_r  # pylint: disable=no-member
    # color_map = plt.cm.gist_heat_r  # pylint: disable=no-member
    # color_map = plt.cm.afmhot_r  # pylint: disable=no-member

    _valuess, _xs, _ys, _Image = plt.hist2d(
        x_prop_values,
        y_prop_values,
        # property_bin_number,
        [axis_x_bins, axis_y_bins],
        [axis_x_limits, axis_y_limits],
        norm=colors.LogNorm(),
        weights=weights,
        cmin=None,
        cmax=None,
        cmap=color_map,
    )

    """
    valuess, _xs, _ys = np.histogram2d(
        x_prop_values, y_prop_values, property_bin_number, [axis_x_limits, axis_y_limits],
        weights=weights)

    subplot.imshow(
        valuess.transpose(),
        norm=colors.LogNorm(),
        cmap=color_map,
        aspect='auto',
        interpolation='nearest',
        #interpolation='none',
        extent=(axis_x_limits[0], axis_x_limits[1], axis_y_limits[0], axis_y_limits[1]),
        #vmin=valuess.min(), vmax=valuess.max(),
        #label=label,
    )
    plt.colorbar()
    """

    if draw_statistics:
        print(stat['bin.mid'])
        subplot.plot(stat['bin.mid'], stat['median'], color='black', linestyle='-', alpha=0.4)
        subplot.plot(stat['bin.mid'], stat['percent.16'], color='black', linestyle='--', alpha=0.3)
        subplot.plot(stat['bin.mid'], stat['percent.84'], color='black', linestyle='--', alpha=0.3)

    # distance legend
    if host_distance_limits is not None and len(host_distance_limits) > 0:
        label = ut.plot.Label.get_label('radius', property_limits=host_distance_limits)
        ut.plot.make_label_legend(subplot, label, 'best')

    if plot_file_name is True or plot_file_name == '':
        if add_simulation_name:
            prefix = part.info['simulation.name']
        else:
            prefix = ''

        plot_file_name = ut.plot.get_file_name(
            y_property_name,
            x_property_name,
            species_name,
            snapshot_dict=part.snapshot,
            host_distance_limits=host_distance_limits,
            prefix=prefix,
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_property_v_distance(
    parts,
    species_name='dark',
    property_name='mass',
    property_statistic='sum',
    property_log_scale=True,
    property_limits=None,
    weight_property='mass',
    distance_limits=[0.1, 300],
    distance_bin_width=0.02,
    distance_log_scale=True,
    dimension_number=3,
    rotation=None,
    other_axis_distance_limits=None,
    center_positions=None,
    center_velocities=None,
    host_index=0,
    property_select={},
    part_indicess=None,
    distance_reference=None,
    plot_nfw=False,
    plot_fit=False,
    fit_distance_limits=None,
    print_values=False,
    get_values=False,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    parts : dict or list
        catalog[s] of particles (can be different simulations or snapshots)
    species_name : str
        name of particle species to compute mass from: 'dark', 'star', 'gas', 'baryon', 'total'
    property_name : str
        property to get profile of
    property_statistic : str
        statistic/type to plot: sum, sum.cum, density, density.cum, vel.circ, sum.fraction,
        sum.cum.fraction, median, average
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    weight_property : str
        property to weight each particle by
    property_limits : list
        limits to impose on y-axis
    distance_limits : list
        min and max distance for binning
    distance_bin_width : float
        width of distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    dimension_number : int
        number of spatial dimensions for profile. if 1, get profile along minor axis.
        if 2, get profile along 2 major axes
    rotation : bool or array
        whether to rotate particles - two options:
        (a) if input array of eigen-vectors, will define rotation axes
        (b) if True, will rotate to align with principal axes stored in species dictionary
    other_axis_distance_limits : float
        min and max distances along other axis[s] to keep particles [kpc physical]
    center_positions : array or list of arrays
        position of center for each particle catalog
    center_velocities : array or list of arrays
        velocity of center for each particle catalog
    host_index : int
        index of host halo to get position and/or velocity of (if not input them)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    distance_reference : float
        reference distance at which to draw vertical line
    plot_nfw : bool
        whether to overplot NFW profile: density ~ 1 / r
    plot_fit : bool
        whether to overplot linear fit
    fit_distance_limits : list
        min and max distance for fit
    print_values : bool
        whether to print values plotted
    get_values : bool
        whether to return values plotted
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    if 'velocity' in property_name:
        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )
    else:
        center_velocities = [center_velocities for _ in center_positions]
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    SpeciesProfile = ut.particle.SpeciesProfileClass(
        distance_limits,
        width=distance_bin_width,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    pros = []

    for part_i, part in enumerate(parts):
        pros_part = SpeciesProfile.get_profiles(
            part,
            species_name,
            property_name,
            property_statistic,
            weight_property,
            host_index,
            center_positions[part_i],
            center_velocities[part_i],
            rotation,
            other_axis_distance_limits,
            property_select,
            part_indicess[part_i],
        )

        pros.append(pros_part)

    if print_values:
        # print results
        print(pros[0][species_name]['distance'])
        for part_i, pro in enumerate(pros):
            print(pro[species_name][property_statistic])

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = [pro[species_name][property_statistic] for pro in pros]
    _axis_x_limits, axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        property_log_scale,
        property_limits,
        y_values,
    )

    if dimension_number in [2, 3]:
        axis_x_label = 'radius'
    elif dimension_number == 1:
        axis_x_label = 'height'
    axis_x_label = ut.plot.Label.get_label(axis_x_label, get_words=True)
    subplot.set_xlabel(axis_x_label)

    if property_statistic == 'vel.circ':
        label_property_name = 'vel.circ'
    else:
        label_property_name = property_name
    axis_y_label = ut.plot.Label.get_label(
        label_property_name, property_statistic, species_name, dimension_number=dimension_number
    )
    subplot.set_ylabel(axis_y_label)

    color_names = ut.plot.get_colors(len(parts))

    if (
        'fraction' in property_statistic
        or 'beta' in property_name
        or 'velocity.rad' in property_name
    ):
        if 'fraction' in property_statistic:
            y_values = [1, 1]
        elif 'beta' in property_name:
            y_values = [0, 0]
        elif 'velocity.rad' in property_name:
            y_values = [0, 0]
        subplot.plot(distance_limits, y_values, color='black', linestyle=':', alpha=0.3)

    if distance_reference is not None:
        subplot.plot(
            [distance_reference, distance_reference],
            axis_y_limits,
            color='black',
            linestyle=':',
            alpha=0.6,
        )

    if plot_nfw:
        pro = pros[0]
        distances_nfw = pro[species_name]['distance']
        # normalize to outermost distance bin
        densities_nfw = (
            np.ones(pro[species_name]['distance'].size) * pro[species_name][property_statistic][-1]
        )
        densities_nfw *= pro[species_name]['distance'][-1] / pro[species_name]['distance']
        subplot.plot(distances_nfw, densities_nfw, color='black', linestyle=':', alpha=0.6)

    # plot profiles
    if len(pros) == 1:
        alpha = None
        linewidth = 3.5
    else:
        alpha = 0.7
        linewidth = None

    for part_i, pro in enumerate(pros):
        color = color_names[part_i]

        label = parts[part_i].info['simulation.name']
        if len(pros) > 1 and parts[0].info['simulation.name'] == parts[1].info['simulation.name']:
            label = '$z={:.1f}$'.format(parts[part_i].snapshot['redshift'])

        masks = pro[species_name][property_statistic] != 0  # plot only non-zero values
        subplot.plot(
            pro[species_name]['distance'][masks],
            pro[species_name][property_statistic][masks],
            color=color,
            alpha=alpha,
            linewidth=linewidth,
            label=label,
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_fit:
        xs = pro[species_name]['distance']
        ys = pro[species_name][property_statistic]

        masks = np.isfinite(xs)
        if fit_distance_limits is not None and len(fit_distance_limits) > 0:
            masks = (xs >= min(fit_distance_limits)) * (xs < max(fit_distance_limits))

        fit_kind = 'exponential'
        # fit_kind = 'sech2.single'
        # fit_kind = 'sech2.double'

        from scipy.optimize import curve_fit
        from scipy import stats

        if fit_kind == 'exponential':
            if distance_log_scale:
                xs = np.log10(xs)
            if property_log_scale:
                ys = np.log10(ys)

            slope, intercept, _r_value, _p_value, _std_err = stats.linregress(xs[masks], ys[masks])

            print('# raw fit: slope = {:.3f}, intercept = {:.3f}'.format(slope, intercept))
            if property_log_scale and not distance_log_scale:
                print('# exponential fit:')
                print('  scale length = {:.3f} kpc'.format(-1 * np.log10(np.e) / slope))
                print('  normalization = 10^{:.2f} Msun / kpc^2'.format(intercept))

            ys_fit = intercept + slope * xs

            if distance_log_scale:
                xs = 10**xs
            if property_log_scale:
                ys_fit = 10**ys_fit

        elif fit_kind == 'sech2.single':

            def disk_height_single(xs, a, b):
                return a / np.cosh(xs / (2 * b)) ** 2

            params, _ = curve_fit(
                disk_height_single, xs[masks], ys[masks], [1e7, 0.5], bounds=[[0, 0], [1e14, 10]]
            )
            print('# single sech^2 fit:')
            print('  scale height = {:.2f} kpc'.format(params[1]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[0] / 2))

            ys_fit = disk_height_single(xs, *params)

        elif fit_kind == 'sech2.double':

            def disk_height_double(xs, a, b, c, d):
                return a / np.cosh(xs / (2 * b)) ** 2 + c / np.cosh(xs / (2 * d)) ** 2

            params, _ = curve_fit(
                disk_height_double,
                xs[masks],
                ys[masks],
                [1e8, 0.1, 1e8, 2],
                bounds=[[10, 0.01, 10, 0.2], [1e14, 3, 1e14, 5]],
            )

            print('# double sech^2 fit:')
            print('* thin scale height = {:.3f} kpc'.format(params[1]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[0] / 2))
            print('* thick scale height = {:.3f} kpc'.format(params[3]))
            print('  normalization = {:.2e} Msun / kpc'.format(params[2] / 2))

            ys_fit = disk_height_double(xs, *params)

        subplot.plot(xs, ys_fit, color='black', alpha=0.5, linewidth=3.5)

    distance_name = 'dist'
    if dimension_number == 2:
        distance_name += '.2d'
    elif dimension_number == 1:
        distance_name = 'height'

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name + '.' + property_statistic,
            distance_name,
            species_name,
            snapshot_dict=parts[0].snapshot,
        )
        plot_file_name = plot_file_name.replace('.sum', '')
        plot_file_name = plot_file_name.replace('mass.vel.circ', 'vel.circ')
        plot_file_name = plot_file_name.replace('mass.density', 'density')
    ut.plot.parse_output(plot_file_name, plot_directory)

    if get_values:
        if len(parts) == 1:
            pros = pros[0]
        return pros


def test_potential_acceleration_v_distance(
    parts,
    species_name='dark',
    property_log_scale=False,
    property_limits=[0, None],
    weight_property=None,
    distance_limits=[1, 500],
    distance_bin_width=2,
    distance_log_scale=False,
    dimension_number=3,
    rotation=None,
    other_axis_distance_limits=None,
    center_positions=None,
    center_velocities=None,
    host_index=0,
    part_indicess=None,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    .
    '''
    property_stat = 'median'

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    center_velocities = [center_velocities for _ in center_positions]
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

    SpeciesProfile = ut.particle.SpeciesProfileClass(
        distance_limits,
        width=distance_bin_width,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    pros_mass = []
    pros_pot = []
    pros_acc = []

    for part_i, part in enumerate(parts):
        # get v^2 = GM(<r)/r
        pro = SpeciesProfile.get_profiles(
            part,
            'total',
            'mass',
            'vel.circ',
            weight_property,
            host_index,
            center_positions[part_i],
            center_velocities[part_i],
            rotation,
            other_axis_distance_limits,
            None,
            part_indicess[part_i],
        )
        # convert to v^2 = GM(<r)/r
        pro['total']['vel.circ'] *= pro['total']['vel.circ']

        pros_mass.append(pro)

        # potential
        pro = SpeciesProfile.get_profiles(
            part,
            species_name,
            'potential',
            property_stat,
            weight_property,
            host_index,
            center_positions[part_i],
            center_velocities[part_i],
            rotation,
            other_axis_distance_limits,
            None,
            part_indicess[part_i],
        )
        pots = pro[species_name][property_stat]
        dists = pro[species_name]['distance']
        if distance_log_scale:
            vcirc2s = np.diff(pots) / distance_bin_width * np.log10(np.e)
        else:
            vcirc2s = np.diff(pots) / np.diff(dists)
        dists = dists[:-1] + np.diff(dists)
        if distance_log_scale is False:
            vcirc2s *= dists
        pro[species_name][property_stat] = vcirc2s
        pro[species_name]['distance'] = dists

        pros_pot.append(pro)

        # radial acceleration
        accels = part[species_name].prop('host.acceleration.spherical')
        part[species_name]['host.acceleration.rad'] = np.abs(accels[:, 0])
        # convert acceleration from [km/s / Gyr] to [km^s / s^2 / kpc]
        part[species_name]['host.acceleration.rad'] *= (
            ut.constant.kpc_per_km * ut.constant.sec_per_Gyr
        )
        pro = SpeciesProfile.get_profiles(
            part,
            species_name,
            'host.acceleration.rad',
            property_stat,
            weight_property,
            host_index,
            center_positions[part_i],
            center_velocities[part_i],
            rotation,
            other_axis_distance_limits,
            None,
            part_indicess[part_i],
        )
        pro[species_name][property_stat] *= pro[species_name]['distance']  # * 1.0227

        pros_acc.append(pro)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = [pro_mass['total']['vel.circ'] for pro_mass in pros_mass]
    _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        property_log_scale,
        property_limits,
        y_values,
    )

    axis_x_label = 'radius'
    axis_x_label = ut.plot.Label.get_label(axis_x_label, get_words=True)
    subplot.set_xlabel(axis_x_label)
    subplot.set_ylabel('$v_{{\\rm circ}}^2$')

    color_names = ut.plot.get_colors(len(parts))

    # plot profiles
    if len(pros_mass) == 1:
        alpha = None
        linewidth = 3.5
    else:
        alpha = 0.7
        linewidth = None

    for part_i, pro_mass in enumerate(pros_mass):
        pro_pot = pros_pot[part_i]
        pro_acc = pros_acc[part_i]
        color = color_names[part_i]

        if part_i == 0:
            label = parts[part_i].info['simulation.name']
            label += ' $z={:.1f}$'.format(parts[part_i].snapshot['redshift'])

        masks = pro_mass['total']['vel.circ'] != 0  # plot only non-zero values
        subplot.plot(
            pro_mass['total']['distance'][masks],
            pro_mass['total']['vel.circ'][masks],
            color=color,
            alpha=alpha,
            linewidth=linewidth,
            label=label,
        )

        masks = pro_pot[species_name][property_stat] != 0  # plot only non-zero values
        subplot.plot(
            pro_pot[species_name]['distance'][masks],
            pro_pot[species_name][property_stat][masks],
            color=color,
            alpha=alpha,
            linewidth=linewidth,
            linestyle='dashed',
            label=label,
        )

        masks = pro_acc[species_name][property_stat] != 0  # plot only non-zero values
        subplot.plot(
            pro_acc[species_name]['distance'][masks],
            pro_acc[species_name][property_stat][masks],
            color=color,
            alpha=alpha,
            linewidth=linewidth,
            linestyle='dotted',
            label=label,
        )

        p = pro_pot[species_name][property_stat]
        m = pro_mass['total']['vel.circ']
        a = pro_acc[species_name][property_stat]
        a_ave = (a[:-1] + a[1:]) / 2

        print('p/m = {:.3f}\n'.format(np.mean(p / m[:-1])))

        print('a/m = {:.3f}'.format(np.mean(a / m)))

        print('a/m = {:.3f}\n'.format(np.mean(a_ave / m[:-1])))

        print('a/p = {:.3f}'.format(np.mean(a[:-1] / p)))
        print('a/p = {:.3f}'.format(np.mean(a_ave / p)))

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    ut.plot.parse_output(plot_file_name, plot_directory)

    return pros_mass, pros_pot, pros_acc


def test_acceleration_v_distance(
    part,
    species_names='all',
    distance_limits=[0, 10],
    distance_bin_width=1,
    distance_log_scale=False,
    host_index=0,
):
    '''
    Test if |a_r| = v_tan^2 / r about center of primary host.
    '''
    if species_names == 'all':
        species_names = list(part.keys())
    elif np.isscalar(species_names):
        species_names = [species_names]

    host_name = ut.catalog.get_host_name(host_index)

    DistanceBin = ut.binning.DistanceBinClass(
        distance_limits,
        distance_bin_width,
        log_scale=distance_log_scale,
    )

    for _spec_i, spec_name in enumerate(species_names):
        pis = ut.array.get_indices(part[spec_name].prop('age'), [0, 0.1])

        accels = part[spec_name].prop('host.acceleration.spherical', pis)
        arads = np.abs(accels[:, 0])
        atans = np.sqrt(accels[:, 1] ** 2 + accels[:, 2] ** 2)
        piis = ut.array.get_indices(atans / arads, [0, 0.1])
        arads = arads[piis]
        pis = pis[piis]

        vels = part[spec_name].prop('host.velocity.spherical', pis)
        vrads = np.abs(vels[:, 0])
        vtan2s = vels[:, 1] ** 2 + vels[:, 2] ** 2
        piis = ut.array.get_indices(vrads / np.sqrt(vtan2s), [0, 0.1])
        vtan2s = vtan2s[piis]
        arads = arads[piis]
        pis = pis[piis]

        distances = part[spec_name].prop(f'{host_name}.distance.total', pis)
        dis = DistanceBin.get_bin_indices(distances)

        ratios = np.zeros(DistanceBin.number)
        for di, d in enumerate(DistanceBin.mids):
            piis = np.where(dis == di)[0]
            arad = np.median(arads[piis])
            vtan2 = np.median(vtan2s[piis])
            ratio = arad / (vtan2 / d) / 1.0227
            ratios[di] = ratio
            print('{:.1f} {:d} {:.3f}'.format(d, piis.size, ratio))

        print(np.median(ratios[ratios > 0]))


def plot_velocity_distribution(
    parts,
    species_name='star',
    property_name='velocity.tan',
    property_limits=None,
    property_bin_width=None,
    property_bin_number=100,
    property_log_scale=False,
    property_statistic='probability',
    distance_limits=[70, 90],
    center_positions=None,
    center_velocities=None,
    host_index=0,
    property_select={},
    part_indicess=None,
    axis_y_limits=None,
    axis_y_log_scale=False,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot distribution of velocities.

    Parameters
    ----------
    part : dict
        catalog of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        property name
    property_limits : list
        min and max limits of property
    property_bin_width : float
        width of property bin (use this or property_bin_number)
    property_bin_number : int
        number of bins within limits (use this or property_bin_width)
    property_log_scale : bool
        whether to use logarithmic scaling for property bins
    property_statistic : str :
        statistic to plot: 'probability', 'probability.cum', 'histogram', 'histogram.cum'
    distance_limits : list
        min and max limits for distance from galaxy
    center_positions : array or list of arrays
        position[s] of galaxy center[s]
    center_velocities : array or list of arrays
        velocity[s] of galaxy center[s]
    host_index : int
        index of host galaxy/halo to get position and/or velocity of (if not input them)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    part_indicess : array or list of arrays
        indices of particles from which to select
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    Say = ut.io.SayClass(plot_velocity_distribution)

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)
    if 'velocity' in property_name:
        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )

    Stat = ut.math.StatisticClass()

    for part_i, part in enumerate(parts):
        if part_indicess[part_i] is not None and len(part_indicess[part_i]) > 0:
            part_indices = part_indicess[part_i]
        else:
            part_indices = ut.array.get_arange(part[species_name]['position'].shape[0])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part[species_name], property_select, part_indices
            )

        if distance_limits:
            # [kpc physical]
            distances = ut.coordinate.get_distances(
                part[species_name]['position'][part_indices],
                center_positions[part_i],
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )
            part_indices = part_indices[ut.array.get_indices(distances, distance_limits)]

        if 'velocity' in property_name:
            orb = ut.particle.get_orbit_dictionary(
                part,
                species_name,
                part_indices,
                center_positions[part_i],
                center_velocities[part_i],
                host_index,
            )
            prop_values = orb[property_name]
        else:
            prop_values = part[species_name].prop(property_name, part_indices)

        Say.say(f'keeping {prop_values.size} {species_name} particles')

        Stat.append_to_dictionary(
            prop_values,
            property_limits,
            property_bin_width,
            property_bin_number,
            property_log_scale,
        )

        # Stat.print_statistics(-1)
        # print()

    color_names = ut.plot.get_colors(len(parts))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array([Stat.distr[property_statistic][part_i] for part_i in range(len(parts))])

    ut.plot.set_axes_scaling_limits(subplot, property_log_scale, property_limits, prop_values)
    ut.plot.set_axes_scaling_limits(
        subplot, None, None, None, axis_y_log_scale, axis_y_limits, y_values
    )

    axis_x_label = ut.plot.Label.get_label(property_name, species_name=species_name, get_words=True)
    subplot.set_xlabel(axis_x_label)
    axis_y_label = ut.plot.Label.get_label(
        property_name, property_statistic, species_name, get_units=False
    )
    subplot.set_ylabel(axis_y_label)

    for part_i, part in enumerate(parts):
        subplot.plot(
            Stat.distr['bin.mid'][part_i],
            Stat.distr[property_statistic][part_i],
            color=color_names[part_i],
            alpha=0.8,
            label=part.info['simulation.name'],
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            property_name, 'distribution', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def plot_neighbors_v_distance(
    parts,
    species_name='star',
    distance_limits=[0.001, 1],
    distance_bin_width=0.1,
    distance_log_scale=True,
    neig_number_max=5000,
    dimension_number=3,
    host_index=0,
    property_select={'host.distance.total': [1, 20], 'age': [0, 0.2]},
    neighbor_statistic='density.norm',
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot number of neighbors (spatial correlation) v separation/distance.

    Parameters
    ----------
    parts : dict or list
        catalog of particles at snapshot
    species_name : str
        name of particle species
    distance_limits : list
        min and max limits for particle neighbor separation distances to measure
    distance_bin_width : float
        width of separation distance bin
    distance_log_scale : bool
        whether to use logarithmic scaling for separation distance bins
    neig_number_max : int
        maximum number of neighbors to find per particle
    dimension_number : int
        number of spatial dimensions to use
    host_index : int
        index of host galaxy/halo to get position and/or velocity of (if not input them)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    property_statistic : str
        statistic to plot: 'probability', 'probability.cum', 'histogram', 'histogram.cum',
        'density.norm'
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    if isinstance(parts, dict):
        parts = [parts]

    DistanceBin = ut.binning.DistanceBinClass(
        distance_limits,
        distance_bin_width,
        log_scale=distance_log_scale,
        dimension_number=dimension_number,
    )

    pros = []
    for part_i, part in enumerate(parts):
        neig_distancess, _neig_indicess = ut.particle.get_neighbors(
            part,
            species_name,
            property_select=property_select,
            neig_distance_max=max(distance_limits),
            neig_number_max=neig_number_max,
            dimension_number=dimension_number,
            host_index=host_index,
        )
        neig_distances = neig_distancess[(neig_distancess > 0) * (neig_distancess < np.inf)]
        pro = DistanceBin.get_sum_profile(neig_distances)
        pros.append(pro)

    color_names = ut.plot.get_colors(len(parts))

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = np.array([pros[part_i][neighbor_statistic] for part_i in range(len(parts))])

    ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        axis_y_log_scale,
        axis_y_limits,
        y_values,
    )

    subplot.set_xlabel('distance [kpc]')
    # axis_y_label = ut.plot.Label.get_label(
    #    property_name, property_statistic, species_name, get_units=False
    # )
    subplot.set_ylabel('correlation ($\\xi + 1$)')

    for part_i, part in enumerate(parts):
        pro = pros[part_i]
        subplot.plot(
            pro['distance.mid'],
            pro[neighbor_statistic],
            color=color_names[part_i],
            alpha=0.8,
            label=part.info['simulation.name'],
        )

    ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = ut.plot.get_file_name(
            'neighbor', 'distance', species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def print_densities(
    parts,
    species_names=['star', 'dark', 'gas'],
    distance_limitss=[[8.0, 8.4], [0, 2 * np.pi], [-1.1, 1.1]],
    coordinate_system='cylindrical',
    center_positions=None,
    center_velocities=None,
    rotation=True,
    host_index=0,
):
    '''
    parts : dict or list
        catalog[s] of particles (can be different simulations or snapshots)
    species_names : str or list thereof
        name of particle species to compute densities of: 'dark', 'star', 'gas'
    distance_limitss : list of lists
        min and max distances/positions
    coordinate_system : str
        which coordinates to get positions in: 'cartesian' (default), 'cylindrical', 'spherical'
    center_positions : array or list of arrays
        position of center for each particle catalog
    center_velocities : array or list of arrays
        velocity of center for each particle catalog
    rotation : bool or array
        whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes stored in species dictionary
    host_index : int
        index of host galaxy/halo to get position, velocity, and/or rotation tensor (if not input)
    property_select : dict
        (other) properties to select on: names as keys and limits as values
    '''
    Say = ut.io.SayClass(print_densities)

    assert coordinate_system in ('cartesian', 'cylindrical', 'spherical')

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)
    center_velocities = ut.particle.parse_property(parts, 'velocity', center_velocities, host_index)

    for part_i, part in enumerate(parts):
        densities_2d = []
        densities_3d = []

        for spec_name in species_names:
            distances = ut.particle.get_distances_wrt_center(
                part,
                spec_name,
                None,
                center_positions[part_i],
                rotation,
                host_index,
                coordinate_system,
            )

            pis = None
            for dimen_i, distance_limits in enumerate(distance_limitss):
                pis = ut.array.get_indices(distances[:, dimen_i], distance_limits, pis)

            mass = np.sum(part[spec_name]['mass'][pis])

            # compute densities
            # compute surface area [pc^2]
            area = (
                np.pi
                * (max(distance_limitss[0]) ** 2 - min(distance_limitss[0]) ** 2)
                * ut.constant.kilo**2
            )
            area *= (max(distance_limitss[1]) - min(distance_limitss[1])) / (2 * np.pi)
            # compute volume [pc^3]
            volume = area * (max(distance_limitss[2]) - min(distance_limitss[2])) * ut.constant.kilo
            density_2d = mass / area
            density_3d = mass / volume

            Say.say(f'{spec_name}:')
            Say.say('  density_2d = {:.5f} Msun / pc^2'.format(density_2d))
            Say.say('  density_3d = {:.5f} Msun / pc^3'.format(density_3d))

            densities_2d.append(density_2d)
            densities_3d.append(density_3d)

        Say.say('total:')
        Say.say('  density_2d = {:.5f} Msun / pc^2'.format(np.sum(densities_2d)))
        Say.say('  density_3d = {:.5f} Msun / pc^3'.format(np.sum(densities_3d)))


# --------------------------------------------------------------------------------------------------
# elemental abundances, element-tracer model
# --------------------------------------------------------------------------------------------------
def plot_element_v_distance(
    parts,
    species_name='gas',
    property_name='massfraction.metals',
    property_statistic='sum',
    axis_y_log_scale=True,
    axis_y_limits=[None, None],
    distance_limits=[10, 3000],
    distance_bin_width=0.1,
    distance_log_scale=True,
    halo_radius=None,
    scale_to_halo_radius=False,
    center_positions=None,
    host_index=0,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot elemental mass or mass fraction for gas or stars v distance (in bin or cumulative).

    Parameters
    ----------
    part : dict or list
        catalog[s] of particles at snapshot
    species_name : str
        name of particle species
    property_name : str
        'massfraction.<element_name>' or 'mass.<element_name>'
    property_statistic : str
        'sum', 'sum.cum'
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    distance_limits : list
        min and max limits for distance from galaxy
    distance_bin_width : float
        width of each distance bin (in units of distance_scaling)
    distance_log_scale : bool
        whether to use logarithmic scaling for distance bins
    halo_radius : float
        radius of halo [kpc physical]
    scale_to_halo_radius : bool
        whether to scale distance to halo_radius
    center_positions : array
        position[s] of galaxy center[s] [kpc comoving]
    host_index : int
        index of host halo to get position of (if not input center_positions)
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    virial_kind = '200m'

    if isinstance(parts, dict):
        parts = [parts]

    center_positions = ut.particle.parse_property(parts, 'position', center_positions, host_index)

    distance_limits_use = np.array(distance_limits)
    if halo_radius and scale_to_halo_radius:
        distance_limits_use *= halo_radius

    DistanceBin = ut.binning.DistanceBinClass(
        distance_limits_use, distance_bin_width, log_scale=distance_log_scale
    )

    property_values = []
    for part_i, part in enumerate(parts):
        distances = ut.coordinate.get_distances(
            part[species_name]['position'],
            center_positions[part_i],
            part.info['box.length'],
            part.snapshot['scalefactor'],
            total_distance=True,
        )  # [kpc physical]

        # get profile of total mass of element
        element_mass_name = property_name.replace('massfraction.', 'mass.')
        element_masses = part[species_name].prop(element_mass_name)
        pro_element = DistanceBin.get_sum_profile(distances, element_masses)
        property_vals = pro_element[property_statistic]

        if 'mass' in property_name:
            property_values.append(property_vals)
        elif 'massfraction' in property_name:
            # get profile of total mass
            pro_mass = DistanceBin.get_sum_profile(distances, part[species_name]['mass'])
            property_values.append(property_vals / pro_mass[property_statistic])

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    ut.plot.set_axes_scaling_limits(
        subplot,
        distance_log_scale,
        distance_limits,
        None,
        axis_y_log_scale,
        axis_y_limits,
        property_values,
    )

    element_mass_label = f'M_{{\\rm Z,{species_name}}}'
    radius_label = '(r)'
    if '.cum' in property_statistic:
        radius_label = '(< r)'
    if 'massfraction' in property_name:
        axis_y_label = (
            f'${element_mass_label}{radius_label} \\, / \\,'
            + ' M_{{\\rm {species_name}}}{radius_label}$'
        )
    elif 'mass' in property_name:
        # axis_y_label = f'${metal_mass_label}(< r) \\, / \\, M_{{\\rm Z,tot}}$'
        axis_y_label = f'${element_mass_label}{radius_label} \\, [M_\\odot]$'
    # axis_y_label = '$Z \\, / \\, Z_\\odot$'
    subplot.set_ylabel(axis_y_label)

    if scale_to_halo_radius:
        axis_x_label = f'$d \\, / \\, R_{{\\rm {virial_kind}}}$'
    else:
        axis_x_label = 'distance $[\\mathrm{kpc}]$'
    subplot.set_xlabel(axis_x_label)

    color_names = ut.plot.get_colors(len(parts), use_black=False)

    xs = DistanceBin.mids
    if halo_radius and scale_to_halo_radius:
        xs /= halo_radius

    if halo_radius:
        if scale_to_halo_radius:
            x_ref = 1
        else:
            x_ref = halo_radius
        subplot.plot([x_ref, x_ref], [1e-6, 1e6], color='black', linestyle=':', alpha=0.6)

    for part_i, part in enumerate(parts):
        subplot.plot(
            xs,
            property_values[part_i],
            color=color_names[part_i],
            alpha=0.8,
            label=part.info['simulation.name'],
        )

    ut.plot.make_legends(subplot, 'best')

    if plot_file_name is True or plot_file_name == '':
        distance_name = 'dist'
        if halo_radius and scale_to_halo_radius:
            distance_name += '.' + virial_kind
        plot_file_name = ut.plot.get_file_name(
            'mass.ratio', distance_name, species_name, snapshot_dict=part.snapshot
        )
    ut.plot.parse_output(plot_file_name, plot_directory)


def test_element_to_element_ratio(
    parts, species=['star', 'gas'], element_reference='o', log_ratio=True
):
    '''
    Test element-to-element variations in abundance ratios (normalizing out the median ratio)
    for metals that FIRE tracks directly.

    Parameters
    ----------
    parts : dict or list
        catalog[s] of particles at snapshot
    species_name : str or list
        name[s] of particle species
    element_reference : str
        name of element to use as reference, to get scatter of other elements relative to it
    log_ratio : bool
        whether to compute the log ratio of elemental abundances
    '''
    Say = ut.io.SayClass(test_element_to_element_ratio)

    element_names = ['c', 'n', 'o', 'ne', 'mg', 'si', 's', 'ca', 'fe']
    element_names = [_ for _ in element_names if _ != element_reference]
    if np.isscalar(species):
        species = [species]
    if species[0] in parts:
        parts = [parts]

    Statistic = ut.math.StatisticClass()

    for element_name in element_names:
        Say.say(
            f'\n[{element_name.capitalize()}/{element_reference.capitalize()}] dex scatter'
            + ' (1-sigma, 2-sigma, 3-sigma)'
        )

        for spec_name in species:
            for part_i, part in enumerate(parts):
                element_ratios_p = part[spec_name].prop(f'massfraction.{element_name}') / part[
                    spec_name
                ].prop(f'massfraction.{element_reference}')
                if part_i == 0:
                    element_ratios = element_ratios_p
                else:
                    element_ratios = np.append(element_ratios, element_ratios_p)

            # we do not care about the absolute ratio of abundances, we care about its scatter
            element_ratios /= np.median(element_ratios)
            if log_ratio:
                element_ratios = np.log10(element_ratios)

            stat = Statistic.get_statistic_dict(element_ratios)
            Say.say(
                '* {:4}: {:.2f}, {:.2f}, {:.2f}'.format(
                    spec_name,
                    0.5 * (stat['percent.84'] - stat['percent.16']),
                    0.5 * (stat['percent.98'] - stat['percent.2']),
                    0.5 * (stat['percent.99.9'] - stat['percent.0.1']),
                )
            )


class ElementTracerClass(ut.io.SayClass):
    '''
    Class to analyze elemental abundances from element-tracers and compare to elemental abundances
    tracked directly in FIRE.
    '''

    def test_elementtracers(
        self,
        part,
        species_name='star',
        weight_property=None,
        pindices=None,
    ):
        '''
        Test element-to-element variations in abundance ratios (normalizing out the median ratio)
        for metals that FIRE tracks directly.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str or list
            name of particle species
        weight_property : str
            property to weight each abundance by. If None, do not weight.
        pindices : array
            prior indices of particles to select
        '''
        multiplier = 1  # multiply dex offset by this

        weights = None
        if weight_property is not None and len(weight_property):
            weights = part[species_name].prop(weight_property, pindices)

        self.say('{}'.format(part.info['simulation.name']))
        self.say('atr-sim popu: median, 68%, 95%')
        self.say('atr-sim part: median, 68%, 95%')
        self.say('')

        for element_name in part[species_name].ElementTracer['yield.massfractions']:
            atr_values = part[species_name].prop(
                f'metallicity.elementtracer.{element_name}', pindices
            )
            sim_values = part[species_name].prop(f'metallicity.{element_name}', pindices)
            pdifs = atr_values - sim_values

            atr_med = ut.math.percentile_weighted(atr_values, 50, weights)
            sim_med = ut.math.percentile_weighted(sim_values, 50, weights)
            pdif_med = ut.math.percentile_weighted(pdifs, 50, weights)

            p84 = ut.math.percentile_weighted(atr_values, 84, weights)
            p16 = ut.math.percentile_weighted(atr_values, 16, weights)
            atr_w68 = (p84 - p16) / 2
            p84 = ut.math.percentile_weighted(sim_values, 84, weights)
            p16 = ut.math.percentile_weighted(sim_values, 16, weights)
            sim_w68 = (p84 - p16) / 2
            p84 = ut.math.percentile_weighted(pdifs, 84, weights)
            p16 = ut.math.percentile_weighted(pdifs, 16, weights)
            pdif_w68 = (p84 - p16) / 2

            p98 = ut.math.percentile_weighted(atr_values, 97.725, weights)
            p02 = ut.math.percentile_weighted(atr_values, 2.275, weights)
            atr_w95 = (p98 - p02) / 2
            p98 = ut.math.percentile_weighted(sim_values, 97.725, weights)
            p02 = ut.math.percentile_weighted(sim_values, 2.275, weights)
            sim_w95 = (p98 - p02) / 2
            p98 = ut.math.percentile_weighted(pdifs, 97.725, weights)
            p02 = ut.math.percentile_weighted(pdifs, 2.275, weights)
            pdif_w95 = (p98 - p02) / 2

            self.say(element_name)
            # self.say('{:5.1f} {:5.2f} {:5.2f}'.format(sim_med, sim_w68, sim_w95))
            self.say(
                '{:6.3f} {:6.3f} {:6.3f}'.format(
                    (atr_med - sim_med) * multiplier,
                    (atr_w68 - sim_w68) * multiplier,
                    (atr_w95 - sim_w95) * multiplier,
                )
            )
            self.say(
                '{:6.3f} {:6.3f} {:6.3f}'.format(
                    pdif_med * multiplier, pdif_w68 * multiplier, pdif_w95 * multiplier
                )
            )
            self.say('')

    def test_elementtracers_with_progenitor_metallicity(
        self, part, species_name='star', weight_property=None, pindices=None, model='fire2.1'
    ):
        '''
        .
        '''
        from . import gizmo_elementtracer

        multiplier = 100
        progenitor_metallicities = np.arange(0.4, 2.0, 0.05)
        metallicity_initial = -5

        weights = None
        if weight_property is not None and len(weight_property):
            weights = part[species_name].prop(weight_property, pindices)

        part[species_name].ElementTracer = gizmo_elementtracer.ElementTracerClass(part.info)

        FIREYield = gizmo_elementtracer.FIREYieldClass(model)
        massfraction_initial = {}
        for element_name in FIREYield.sun_massfraction:
            massfraction_initial[element_name] = (
                10**metallicity_initial * FIREYield.sun_massfraction[element_name]
            )

        med_old = -np.inf

        print(f'offset(x{multiplier}): median, 68%, 95% | Z_proj')
        for element_name in FIREYield.element_names:
            for progenitor_metallicity in progenitor_metallicities:
                FIREYield = gizmo_elementtracer.FIREYieldClass(
                    model, progenitor_metallicity=progenitor_metallicity
                )
                element_yield_dict = FIREYield.get_element_yields(
                    part[species_name].ElementTracer['age.bins']
                )
                part[species_name].ElementTracer.assign_element_yield_massfractions(
                    element_yield_dict
                )
                part[species_name].ElementTracer.assign_element_initial_massfraction(
                    massfraction_initial
                )

                difs = part[species_name].prop(
                    f'metallicity.elementtracer.{element_name}', pindices
                ) - part[species_name].prop(f'metallicity.{element_name}', pindices)

                med = ut.math.percentile_weighted(difs, 50, weights)
                if med > 0 and med_old < 0:
                    break
                else:
                    med_old = med

                p84 = ut.math.percentile_weighted(difs, 84, weights)
                p16 = ut.math.percentile_weighted(difs, 16, weights)
                w68 = (p84 - p16) / 2
                p98 = ut.math.percentile_weighted(difs, 97.725, weights)
                p02 = ut.math.percentile_weighted(difs, 2.275, weights)
                w95 = (p98 - p02) / 2

                print(
                    '{:10}: {:5.1f}  {:4.1f} {:4.1f} | {:.2f}'.format(
                        element_name,
                        med * multiplier,
                        w68 * multiplier,
                        w95 * multiplier,
                        progenitor_metallicity,
                    )
                )

    def test_progenitor_metallicity_dependence(
        self,
        part,
        species_name='star',
        progenitor_metallicities=[0.1, 1],
        yield_model='fire2.2',
        element_names=['metals', 'carbon', 'nitrogen', 'oxygen', 'magnesium', 'iron'],
    ):
        '''
        .
        '''
        from . import gizmo_elementtracer

        metal_dicts = []

        for progenitor_metallicity in progenitor_metallicities:
            gizmo_elementtracer.initialize_elementtracers(
                part,
                species_name,
                progenitor_metallicity=progenitor_metallicity,
                yield_model=yield_model,
            )
            metal_dict = {}
            for element_name in element_names:
                metal_dict[element_name] = part[species_name].prop(
                    f'metallicity.{element_name}.elementtracer'
                )
            metal_dicts.append(metal_dict)

        for element_name in element_names:
            metal_difs = metal_dicts[1][element_name] - metal_dicts[0][element_name]

            self.say(f'\n* {element_name}')
            ut.math.print_statistics(metal_difs)

    def plot_element_distribution(
        self,
        part,
        species_name='gas',
        property_name='metallicity.fe',
        property_limits=[-4, 1],
        property_bin_width=0.1,
        property_statistic='probability',
        axis_y_limits=None,
        axis_y_log_scale=True,
        weight_property='mass',
        part_indices=None,
        verbose=True,
        plot_file_name=None,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot distribution of elemental abundance, comparing direct simulation to element-tracers.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species
        property_name : str
             name of element
        property_limits : list
            min and max limits of element
        property_bin_width : float
            width of element bin
        property_statistic : str
            statistic to plot: 'probability', 'probability.cum', 'probability.norm', 'histogram',
            'histogram.cum'
        axis_y_limits : list
            min and max limits for y axis
        axis_y_log_scale : bool
            whether to use logarithmic scaling for y axis
        weight_property : str
            property to weight each particle by
        part_indices : array
            indices of particles from which to select
        verbose : bool
            verbosity flag
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write plot file
        figure_index : int
            index of figure for matplotlib
        '''
        model_number = 2
        atr_property_name = property_name.replace('metallicity', 'metallicity.elementtracer')

        Stat = ut.math.StatisticClass()

        sim_property_values = part[species_name].prop(property_name, part_indices)
        atr_property_values = part[species_name].prop(atr_property_name, part_indices)

        weights = None
        if weight_property:
            weights = part[species_name].prop(weight_property, part_indices)

        masks = sim_property_values > -np.inf
        masks *= (sim_property_values > property_limits[0]) * (
            sim_property_values < property_limits[1]
        )
        masks *= (atr_property_values > property_limits[0]) * (
            atr_property_values < property_limits[1]
        )

        property_difs = atr_property_values[masks] - sim_property_values[masks]
        if verbose:
            ut.math.print_statistics(property_difs, weights[masks])

        sim_distr = Stat.get_distribution_dict(
            sim_property_values,
            property_limits,
            property_bin_width,
            log_scale=False,
            weights=weights,
        )

        atr_distr = Stat.get_distribution_dict(
            atr_property_values,
            property_limits,
            property_bin_width,
            log_scale=False,
            weights=weights,
        )

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        y_values = np.array([sim_distr[property_statistic], atr_distr[property_statistic]])

        ut.plot.set_axes_scaling_limits(
            subplot, False, property_limits, None, axis_y_log_scale, axis_y_limits, y_values
        )

        axis_x_label = ut.plot.Label.get_label(
            property_name, species_name=species_name, get_words=True
        )
        subplot.set_xlabel(axis_x_label)
        axis_y_label = ut.plot.Label.get_label(
            property_name, property_statistic, species_name, get_units=False
        )
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(model_number)

        subplot.plot(
            sim_distr['bin.mid'],
            sim_distr[property_statistic],
            color=color_names[0],
            alpha=0.8,
            label='FIRE',
        )

        plt.arrow(
            np.median(sim_property_values), 0, 0, 0.15, width=0.01, color=color_names[0], alpha=0.8
        )

        subplot.plot(
            atr_distr['bin.mid'],
            atr_distr[property_statistic],
            color=color_names[1],
            alpha=0.8,
            label='tracer',
        )

        plt.arrow(
            np.median(atr_property_values), 0, 0, 0.15, width=0.01, color=color_names[1], alpha=0.8
        )

        ut.plot.make_legends(subplot)  # time_value=parts.snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                property_name, 'distribution', species_name, snapshot_dict=part.snapshot
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_element_v_element(
        self,
        part,
        species_name='star',
        x_property_name='metallicity.fe',
        x_property_limits=[-4, 1],
        x_property_width=0.1,
        y_property_name='metallicity.mg - metallicity.fe',
        y_property_limits=None,
        weight_property='mass',
        part_indices=None,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot elemental abundance v elemental abundance.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species
        x_property_name : str
            name of element on x-axis
        x_property_limits : list
            min and max limits to impose
        x_property_width : float
            width of x-axis bin
        y_property_name : str
            name of element[s] on y-axis
        y_property_limits : list
            min and max limits to impose
        weight_property : str
            property by which to weight each particle
        part_indices : array
            indices of particles from which to select
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        model_number = 2
        atr_x_property_name = x_property_name.replace('metallicity', 'metallicity.elementtracer')
        atr_y_property_name = y_property_name.replace('metallicity', 'metallicity.elementtracer')

        if x_property_limits is not None and len(x_property_limits) > 0:
            part_indices = ut.array.get_indices(
                part[species_name].prop(x_property_name), x_property_limits, part_indices
            )
            part_indices = ut.array.get_indices(
                part[species_name].prop(atr_x_property_name), x_property_limits, part_indices
            )

        weights = None
        if weight_property:
            weights = part[species_name].prop(weight_property, part_indices)

        Bin = ut.binning.BinClass(x_property_limits, x_property_width)

        sim_stat = Bin.get_statistics_of_array(
            part[species_name].prop(x_property_name, part_indices),
            part[species_name].prop(y_property_name, part_indices),
            weights,
        )
        atr_stat = Bin.get_statistics_of_array(
            part[species_name].prop(atr_x_property_name, part_indices),
            part[species_name].prop(atr_y_property_name, part_indices),
            weights,
        )

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        y_values = [
            part[species_name].prop(y_property_name, part_indices),
            part[species_name].prop(atr_y_property_name, part_indices),
        ]

        ut.plot.set_axes_scaling_limits(
            subplot, False, x_property_limits, None, False, y_property_limits, y_values
        )

        axis_x_label = ut.plot.Label.get_label(x_property_name, species_name=species_name)
        subplot.set_xlabel(axis_x_label)

        axis_y_label = ut.plot.Label.get_label(y_property_name, species_name=species_name)
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(model_number)

        ut.plot.draw_stats(
            subplot, sim_stat, 'bin.mid', 'median', 2, color=color_names[0], label='FIRE'
        )
        ut.plot.draw_stats(
            subplot, atr_stat, 'bin.mid', 'median', 2, color=color_names[1], label='tracer'
        )

        print(ut.io.get_string_from_numbers(atr_stat['median'] - sim_stat['median']))

        print('median {:.3f}'.format(np.mean(atr_stat['median'] - sim_stat['median'])))

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                y_property_name,
                x_property_name,
                species_name,
                snapshot_dict=part.snapshot,
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_element_v_time(
        self,
        part,
        time_name='age',
        time_limits=[13.7, 0],
        time_width=0.1,
        property_name='metallicity.fe',
        property_limits=[-4, 1],
        weight_property='mass',
        part_indices=None,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot elemental abundance v time.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        time_name : str
            name of time property: 'age', 'time', 'redshift'
        time_limits : list
            min and max limits on time property
        time_width : float
            width of time bin
        property_name : str
            name of element[s] on y-axis
        property_limits : list
            min and max limits on property_name
        weight_property : str
            property by which to weight each particle
        part_indices : array
            indices of particles from which to select
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        species_name = 'star'
        model_number = 2
        time_log_scale = False
        atr_property_name = property_name.replace('metallicity', 'metallicity.elementtracer')

        if time_limits is not None and len(time_limits) > 0:
            part_indices = ut.array.get_indices(
                part[species_name].prop(time_name), time_limits, part_indices
            )

        weights = None
        if weight_property:
            weights = part[species_name].prop(weight_property, part_indices)

        Bin = ut.binning.BinClass(time_limits, time_width, log_scale=time_log_scale)

        sim_stat = Bin.get_statistics_of_array(
            part[species_name].prop(time_name, part_indices),
            part[species_name].prop(property_name, part_indices),
            weights,
        )
        atr_stat = Bin.get_statistics_of_array(
            part[species_name].prop(time_name, part_indices),
            part[species_name].prop(atr_property_name, part_indices),
            weights,
        )

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        y_values = [
            part[species_name].prop(property_name, part_indices),
            part[species_name].prop(atr_property_name, part_indices),
        ]

        ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, None, False, property_limits, y_values
        )

        axis_x_label = ut.plot.Label.get_label(time_name, get_words=True)
        subplot.set_xlabel(axis_x_label)

        axis_y_label = ut.plot.Label.get_label(property_name, species_name=species_name)
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(model_number)

        ut.plot.draw_stats(
            subplot, sim_stat, 'bin.mid', 'median', 2, color=color_names[0], label='FIRE'
        )
        ut.plot.draw_stats(
            subplot, atr_stat, 'bin.mid', 'median', 2, color=color_names[1], label='tracer'
        )

        print(ut.io.get_string_from_numbers(atr_stat['median'] - sim_stat['median']))

        print('median {:.3f}'.format(np.mean(atr_stat['median'] - sim_stat['median'])))

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                property_name,
                time_name,
                species_name,
                snapshot_dict=part.snapshot,
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_element_v_distance(
        self,
        part,
        species_name='star',
        property_name='metallicity.fe',
        property_statistic='median',
        property_limits=None,
        weight_property='mass',
        distance_limits=[0, 15],
        distance_bin_width=0.1,
        distance_log_scale=False,
        dimension_number=3,
        rotation=True,
        other_axis_distance_limits=None,
        part_indices=None,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        part : dict
            catalog[s] of particles
        species_name : str
            name of particle species to compute mass from: 'star', 'gas'
        property_name : str
            property to get profile of
        property_statistic : str
            statistic/type to plot: 'median', 'average'
        property_limits : list
            limits to impose on y-axis
        weight_property : str
            property to weight each particle by
        distance_limits : list
            min and max distance for binning
        distance_bin_width : float
            width of distance bin
        distance_log_scale : bool
            whether to use logarithmic scaling for distance bins
        dimension_number : int
            number of spatial dimensions for profile. if 1, get profile along minor axis.
            if 2, get profile along 2 major axes
        rotation : bool or array
            whether to rotate particles - two options:
            (a) if input array of eigen-vectors, will define rotation axes
            (b) if True, will rotate to align with principal axes stored in species dictionary
        other_axis_distance_limits : float
            min and max distances along other axis[s] to keep particles [kpc physical]
        part_indices : array
            indices of particles to select
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        model_number = 2

        atr_property_name = property_name.replace('metallicity', 'metallicity.elementtracer')

        SpeciesProfile = ut.particle.SpeciesProfileClass(
            distance_limits,
            width=distance_bin_width,
            log_scale=distance_log_scale,
            dimension_number=dimension_number,
        )

        sim_pro = SpeciesProfile.get_statistics_profiles(
            part,
            species_name,
            property_name,
            weight_property,
            rotation=rotation,
            other_axis_distance_limits=other_axis_distance_limits,
            part_indicess=part_indices,
        )[species_name]

        atr_pro = SpeciesProfile.get_statistics_profiles(
            part,
            species_name,
            atr_property_name,
            weight_property,
            rotation=rotation,
            other_axis_distance_limits=other_axis_distance_limits,
            part_indicess=part_indices,
        )[species_name]

        # print results
        print(atr_pro[property_statistic] - sim_pro[property_statistic])

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        y_values = [
            np.min(np.concatenate((sim_pro['percent.16'], atr_pro['percent.16']))),
            np.max(np.concatenate((sim_pro['percent.84'], atr_pro['percent.84']))),
        ]

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            False,
            property_limits,
            y_values,
        )

        if dimension_number in [2, 3]:
            axis_x_label = 'radius'
        elif dimension_number == 1:
            axis_x_label = 'height'
        axis_x_label = ut.plot.Label.get_label(axis_x_label, get_words=True)
        subplot.set_xlabel(axis_x_label)

        axis_y_label = ut.plot.Label.get_label(property_name, property_statistic)
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(model_number)

        ut.plot.draw_stats(
            subplot, sim_pro, 'distance.mid', 'median', 2, color=color_names[0], label='FIRE'
        )
        ut.plot.draw_stats(
            subplot, atr_pro, 'distance.mid', 'median', 2, color=color_names[1], label='tracer'
        )

        ut.plot.make_legends(subplot)

        distance_name = 'radius'
        if dimension_number == 2:
            distance_name += '.2d'
        elif dimension_number == 1:
            distance_name = 'height'

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                property_name + '.' + property_statistic,
                distance_name,
                species_name,
            )
        ut.plot.parse_output(plot_file_name, plot_directory)


ElementTracer = ElementTracerClass()


# --------------------------------------------------------------------------------------------------
# ISM
# --------------------------------------------------------------------------------------------------
class ISMClass(ut.io.SayClass):
    '''
    .
    '''

    def get_positions_sampled(
        self,
        parts,
        species_name='gas',
        property_select={},
        part_indicess=None,
        radius_limits=[3, 12],
        height_limits=[-0.1, 0.1],
        coordinate_modifier='principal',
        host_index=0,
        dimension_number=3,
        sample_number=100,
    ):
        '''
        .
        '''
        if isinstance(parts, dict):
            parts = [parts]

        positionss = []

        for part_i, part in enumerate(parts):
            part_spec = part[species_name]

            part_indices = None
            if part_indicess is not None:
                part_indices = part_indicess[part_i]

            position_name, _velocity_name = ut.particle.parse_coordinate_names(
                host_index, coordinate_modifier
            )

            if property_select:
                part_indices = ut.catalog.get_indices_catalog(
                    part_spec, property_select, part_indices
                )

            positions_cyl = None

            if radius_limits is not None and len(radius_limits) > 0:
                if positions_cyl is None:
                    positions_cyl = part_spec.prop(f'{position_name}.cylindrical')
                part_indices = ut.array.get_indices(
                    positions_cyl[:, 0], radius_limits, part_indices
                )

            if height_limits is not None and len(height_limits) > 0:
                if positions_cyl is None:
                    positions_cyl = part_spec.prop(f'{position_name}.cylindrical')
                part_indices = ut.array.get_indices(
                    positions_cyl[:, 2], height_limits, part_indices
                )

            part_indices = np.random.choice(part_indices, sample_number)

            if positions_cyl is not None:
                R_med = np.median(positions_cyl[part_indices, 0])
                Z_med = np.median(np.abs(positions_cyl[part_indices, 2]))
                self.say('  R median = {:.2f} kpc'.format(R_med))
                self.say('|Z| median = {:.2f} kpc'.format(Z_med))

            positions = part_spec.prop(position_name, part_indices)

            if dimension_number == 2:
                positions = positions[:, [0, 1]]

            positionss.append(positions)

        return np.array(positionss)

    def get_velocity_dispersion_v_distance(
        self,
        center_positionss,
        parts,
        species_name='gas',
        property_select={},
        part_indicess=None,
        weight_by_mass=True,
        neig_number_max=300000,
        distance_limits=[0.001, 2],
        distance_bin_width=0.01,
        distance_log_scale=True,
        coordinate_modifier='principal',
        host_index=0,
        periodic=False,
    ):
        '''
        .
        '''
        if np.ndim(center_positionss) == 1:
            center_positionss = [center_positionss]

        if isinstance(parts, dict):
            parts = [parts]

        assert len(center_positionss) == len(parts)

        veldisp = {}
        for part_i, part in enumerate(parts):
            center_positions = center_positionss[part_i]

            part_indices = None
            if part_indicess is not None:
                part_indices = part_indicess[part_i]

            veldisp_p = ut.particle.get_velocity_dispersion_v_distance(
                center_positions,
                part,
                species_name,
                property_select,
                part_indices,
                weight_by_mass,
                neig_number_max,
                distance_limits,
                distance_bin_width,
                distance_log_scale,
                coordinate_modifier,
                host_index,
                periodic,
            )
            veldisp_p['simulation.name'] = part.info['simulation.name']

            ut.array.append_dictionary(veldisp, veldisp_p)

        return veldisp

        # self.plot_velocity_dispersion_v_distance(
        #    veldisp, species_name, distance_limits, distance_log_scale,
        # )

    def plot_velocity_dispersion_v_distance(
        self,
        veldisp,
        veldisp_2=None,
        veldisp_3=None,
        species_name='gas',
        distance_limits=[0.003, 2],
        distance_log_scale=True,
        veldisp_limits=[1, 100],
        veldisp_log_scale=True,
        veldisp_dimen_number=3,
        plot_file_name=False,
        plot_directory='.',
    ):
        '''
        .
        '''
        part_number = len(veldisp['distance'])
        selection_number = 1
        if veldisp_2 is not None:
            selection_number = 2
            if veldisp_3 is not None:
                selection_number = 3
            part_number = 1
        distance_limits = np.array(distance_limits) * ut.constant.kilo

        dimen_factor = 1.0
        if veldisp_dimen_number == 1:
            dimen_factor /= np.sqrt(3)

        # plot ----------
        _fig, subplot = ut.plot.make_figure(right=0.94)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            veldisp_log_scale,
            veldisp_limits,
        )

        # subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(10))

        subplot.set_xlabel('radius of sphere $r$ $\\left[ {{\\rm pc}} \\right]$')
        axis_y_label = '$\\sigma_{\\rm vel,3D}(< r)$ $\\left[ {{\\rm km/s}} \\right]$'
        if veldisp_dimen_number == 1:
            axis_y_label = axis_y_label.replace('3D', '1D')
        subplot.set_ylabel(axis_y_label)

        color_names = ut.plot.get_colors(max(part_number, selection_number))

        for pi in range(part_number):
            color = color_names[pi]

            if selection_number == 1:
                label = veldisp['simulation.name'][pi]
                label = label.replace('Msun', '${\\rm M}_\\odot$')
            else:
                label = 'all'

            subplot.fill_between(
                veldisp['distance'][0] * ut.constant.kilo,
                veldisp['cum.median.16'][pi] * dimen_factor,
                veldisp['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp['distance'][0] * ut.constant.kilo,
                veldisp['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

            """
            label = veldisp['simulation.name'][pi] + ' average'
            subplot.fill_between(
                distances,
                veldisp['cum.average.16'][pi] * dimen_factor,
                veldisp['cum.average.84'][pi] * dimen_factor,
                color=color,
                alpha=0.4,
            )
            subplot.plot(
                distances,
                veldisp['cum.average.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                label=label,
                linestyle='--',
            )
            """

        if veldisp_2 is not None:
            pi = 0
            color = color_names[1]
            label = 'cold (T < 100 K)'
            subplot.fill_between(
                veldisp_2['distance'][0] * ut.constant.kilo,
                veldisp_2['cum.median.16'][pi] * dimen_factor,
                veldisp_2['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp_2['distance'][0] * ut.constant.kilo,
                veldisp_2['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

        if veldisp_3 is not None:
            pi = 0
            color = color_names[2]
            label = 'star forming'
            subplot.fill_between(
                veldisp_3['distance'][0] * ut.constant.kilo,
                veldisp_3['cum.median.16'][pi] * dimen_factor,
                veldisp_3['cum.median.84'][pi] * dimen_factor,
                color=color,
                alpha=0.25,
                edgecolor=None,
            )
            subplot.plot(
                veldisp_3['distance'][0] * ut.constant.kilo,
                veldisp_3['cum.median.50'][pi] * dimen_factor,
                color=color,
                alpha=0.8,
                linestyle='-',
                label=label,
            )

        # power law relation
        ds = np.array([50, 1000])
        sigs = 5 * dimen_factor * np.ones(ds.size)
        sigs[1] = sigs[0] * (ds[1] / ds[0]) ** (1 / 2)
        subplot.plot(
            ds,
            sigs,
            color='black',
            alpha=0.6,
            linestyle=':',
            label='$\\sigma \\propto r^{1/2}$',
        )

        ut.plot.make_legends(subplot)

        if plot_file_name is True or plot_file_name == '':
            # property_y = 'disk.orientation'
            # plot_file_name = ut.plot.get_file_name(
            #    property_y, property_name, snapshot_dict=part.snapshot
            # )
            plot_file_name = f'{species_name}_veldisp_v_rad'
        ut.plot.parse_output(plot_file_name, plot_directory)


ISM = ISMClass()


# --------------------------------------------------------------------------------------------------
# stellar mass growth v radius
# --------------------------------------------------------------------------------------------------
class MassRadiusClass(ut.io.SayClass):
    '''
    .
    '''

    def __init__(self):
        '''
        .
        '''
        self.species_name = 'star'

    def plot_age_v_distance(
        self,
        parts,
        distance_limits=[0, 16],
        distance_bin_width=0.25,
        distance_log_scale=False,
        dimension_number=2,
        height_limits=[-3, 3],
        age_limits=[0, 10],
        age_log_scale=False,
        age_statistic='median',
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot average age v radial distance (today and at formation).

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles
        species_names : str or list
            name[s] of particle species to compute: 'star', 'gas', 'dark'
        property_name : str
            which property to vary (along x-axis): 'distance', 'age'
        property_limits : list
            min and max property for binning
        property_bin_width : float
            width of property bin
        property_log_scale : bool
            whether to use logarithmic scaling for property
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        species_name = self.species_name

        if isinstance(parts, dict):
            parts = [parts]

        host_name = ut.catalog.get_host_name(host_index)

        DistanceBin = ut.binning.DistanceBinClass(
            distance_limits,
            distance_bin_width,
            log_scale=distance_log_scale,
            dimension_number=dimension_number,
        )

        stat = {
            'now': [],
            'form': [],
        }

        for part_i, part in enumerate(parts):
            ages = part[species_name].prop('age')

            # use properties at this snapshot
            masses = part[species_name].prop('mass')

            pindices = None
            if dimension_number == 3:
                distances = part[species_name].prop(f'{host_name}.distance.total')
                pindices = ut.array.get_indices(distances, distance_limits, pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'{host_name}.distance.cyl')
                pindices = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices = ut.array.get_indices(distances, distance_limits, pindices)

            stat_i = DistanceBin.get_statistics_profile(
                distances[pindices], ages[pindices], masses[pindices], verbose=True
            )
            stat['now'].append(stat_i)

            # use properties at formation
            masses = part[species_name].prop('form.mass')

            pindices = None
            if dimension_number == 3:
                distances = part[species_name].prop(f'form.{host_name}.distance.total')
                pindices = ut.array.get_indices(distances, distance_limits, pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'form.{host_name}.distance.cyl')
                pindices = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices = ut.array.get_indices(distances, distance_limits, pindices)

            stat_i = DistanceBin.get_statistics_profile(
                distances[pindices], ages[pindices], masses[pindices], verbose=True
            )
            stat['form'].append(stat_i)

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            age_log_scale,
            age_limits,
        )

        subplot.set_xlabel('radius [kpc]')
        subplot.set_ylabel('age [Gyr]')

        if len(parts) > 1:
            color_names = ut.plot.get_colors(len(parts))
        else:
            color_names = ut.plot.get_colors(2)

        for part_i, part in enumerate(parts):
            for time_i, time_kind in enumerate(['form', 'now']):
                stat_i = stat[time_kind][part_i]

                if len(parts) > 1:
                    color = color_names[part_i]
                else:
                    color = color_names[time_i]

                subplot.fill_between(
                    stat_i['distance.mid'],
                    stat_i['percent.16'],
                    stat_i['percent.84'],
                    color=color,
                    linestyle='-',
                    alpha=0.4,
                )
                subplot.plot(
                    stat_i['distance.mid'],
                    stat_i[age_statistic],
                    color=color,
                    alpha=0.7,
                    label=time_kind,
                )

        ut.plot.make_legends(subplot)

        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_massfraction_v_distance(
        self,
        parts,
        distance_limits=[0, 16],
        distance_bin_width=0.25,
        distance_log_scale=False,
        dimension_number=2,
        height_limits=[-3, 3],
        age_limits=[0, 12],
        age_bin_width=1.5,
        age_log_scale=False,
        # mass_statistic='dif',
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot average age v radial distance (today and at formation).

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles
        property_name : str
            which property to vary (along x-axis): 'distance', 'age'
        property_limits : list
            min and max property for binning
        property_bin_width : float
            width of property bin
        property_log_scale : bool
            whether to use logarithmic scaling for property
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        species_name = self.species_name

        if isinstance(parts, dict):
            parts = [parts]

        host_name = ut.catalog.get_host_name(host_index)

        DistanceBin = ut.binning.DistanceBinClass(
            distance_limits,
            distance_bin_width,
            log_scale=distance_log_scale,
            dimension_number=dimension_number,
        )

        AgeBin = ut.binning.BinClass(
            age_limits,
            age_bin_width,
            log_scale=age_log_scale,
        )

        ratio = {
            'now': np.zeros((len(parts), AgeBin.number, DistanceBin.number)),
            'form': np.zeros((len(parts), AgeBin.number, DistanceBin.number)),
        }

        for part_i, part in enumerate(parts):
            ages = part[species_name].prop('age')

            # use properties at this snapshot
            masses = part[species_name].prop('mass')

            pindices = None
            if dimension_number == 3:
                distances = part[species_name].prop(f'{host_name}.distance.total')
                pindices = ut.array.get_indices(distances, distance_limits, pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'{host_name}.distance.cyl')
                pindices = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices = ut.array.get_indices(distances, distance_limits, pindices)

            stat_all = DistanceBin.get_sum_profile(
                distances[pindices], masses[pindices], verbose=True
            )
            for age_i, age_min in enumerate(AgeBin.maxs):
                pindices_age = ut.array.get_indices(ages, [age_min, np.inf], pindices)
                stat_i = DistanceBin.get_sum_profile(
                    distances[pindices_age], masses[pindices_age], verbose=True
                )

                ratio['now'][part_i, age_i] = stat_i['sum'] / stat_all['sum']

            # use properties at formation
            masses = part[species_name].prop('form.mass')

            pindices = None
            if dimension_number == 3:
                distances = part[species_name].prop(f'form.{host_name}.distance.total')
                pindices = ut.array.get_indices(distances, distance_limits, pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'form.{host_name}.distance.cyl')
                pindices = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices = ut.array.get_indices(distances, distance_limits, pindices)

            stat_all = DistanceBin.get_sum_profile(
                distances[pindices], masses[pindices], verbose=True
            )
            for age_i, age_min in enumerate(AgeBin.maxs):
                pindices_age = ut.array.get_indices(ages, [age_min, np.inf], pindices)
                stat_i = DistanceBin.get_sum_profile(
                    distances[pindices_age], masses[pindices_age], verbose=True
                )

                ratio['form'][part_i, age_i] = stat_i['sum'] / stat_all['sum']

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            False,
            [0, 1],
        )

        subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

        subplot.set_xlabel('radius [kpc]')
        subplot.set_ylabel('$M(> age)/M_{\\rm total}$')

        if len(parts) > 1:
            color_names = ut.plot.get_colors(len(parts))
        else:
            color_names = ut.plot.get_colors(AgeBin.number)

        for part_i, part in enumerate(parts):
            for _time_i, time_kind in enumerate(['now', 'form']):
                for age_i, age_min in enumerate(AgeBin.maxs):
                    if len(parts) > 1:
                        color = color_names[part_i]
                    else:
                        color = color_names[age_i]

                    if time_kind == 'form':
                        linestyle = '-'
                        label = 'age > {:.1f} Gyr'.format(age_min)
                    elif time_kind == 'now':
                        linestyle = '--'
                        label = None

                    subplot.plot(
                        DistanceBin.mids,
                        ratio[time_kind][part_i, age_i],
                        color=color,
                        linestyle=linestyle,
                        alpha=0.7,
                        label=label,
                    )

        ut.plot.make_legends(subplot)

        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_radius_v_age(
        self,
        parts,
        age_limits=[0, 13.5],
        age_bin_width=0.5,
        age_log_scale=False,
        mass_percents=[20, 50, 90],
        mass_distance_max=30,
        distance_limits=[0, 13],
        dimension_number=2,
        height_limits=[-3, 3],
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot average age v radial distance (today and at formation).

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles
        property_name : str
            which property to vary (along x-axis): 'distance', 'age'
        property_limits : list
            min and max property for binning
        property_bin_width : float
            width of property bin
        property_log_scale : bool
            whether to use logarithmic scaling for property
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        species_name = self.species_name

        if isinstance(parts, dict):
            parts = [parts]

        host_name = ut.catalog.get_host_name(host_index)

        AgeBin = ut.binning.BinClass(
            age_limits,
            age_bin_width,
            log_scale=age_log_scale,
        )

        radius = {
            'now': np.zeros((len(parts), len(mass_percents), AgeBin.number)),
            'form': np.zeros((len(parts), len(mass_percents), AgeBin.number)),
        }

        for part_i, part in enumerate(parts):
            ages = part[species_name].prop('age')

            # use properties at this snapshot
            # masses = part[species_name].prop('mass')

            form_distance_comov = part[species_name].prop(f'form.{host_name}.distance.total')
            form_distance_comov *= part[species_name].prop('form.scalefactor')
            pindices = ut.array.get_indices(form_distance_comov, [0, 30])

            # pindices = None

            if dimension_number == 3:
                distances = part[species_name].prop(f'{host_name}.distance.total')
                pindices_d = ut.array.get_indices(distances, [0, mass_distance_max], pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'{host_name}.distance.cyl')
                pindices_d = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices_d = ut.array.get_indices(distances, [0, mass_distance_max], pindices_d)

            for age_i, age_min in enumerate(AgeBin.mins):
                # age_bin_limits = [age_min, np.inf]
                age_bin_limits = [age_min, AgeBin.maxs[age_i]]
                pindices_age = ut.array.get_indices(ages, age_bin_limits, pindices_d)
                for m_i, mass_percent in enumerate(mass_percents):
                    r = np.percentile(distances[pindices_age], mass_percent)
                    # r = ut.math.percentile_weighted(
                    #    distances[pindices_age], mass_percent, masses[pindices_age]
                    # )
                    radius['now'][part_i, m_i, age_i] = r

            # use properties at formation
            # masses = part[species_name].prop('form.mass')

            if dimension_number == 3:
                distances = part[species_name].prop(f'form.{host_name}.distance.total')
                pindices_d = ut.array.get_indices(distances, [0, mass_distance_max], pindices)
            elif dimension_number == 2:
                distances = part[species_name].prop(f'form.{host_name}.distance.cyl')
                pindices_d = ut.array.get_indices(distances[:, 2], height_limits, pindices)
                distances = distances[:, 0]
                pindices_d = ut.array.get_indices(distances, [0, mass_distance_max], pindices_d)

            for age_i, age_min in enumerate(AgeBin.mins):
                # age_bin_limits = [age_min, np.inf]
                age_bin_limits = [age_min, AgeBin.maxs[age_i]]
                pindices_age = ut.array.get_indices(ages, age_bin_limits, pindices_d)
                for m_i, mass_percent in enumerate(mass_percents):
                    r = np.percentile(distances[pindices_age], mass_percent)
                    # r = ut.math.percentile_weighted(
                    #    distances[pindices_age], mass_percent, masses[pindices_age]
                    # )
                    radius['form'][part_i, m_i, age_i] = r

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot,
            age_log_scale,
            age_limits,
            None,
            False,
            distance_limits,
        )

        subplot.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
        # subplot.yaxis.set_major_locator(ticker.AutoLocator(1))
        subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))

        subplot.set_xlabel('age [Gyr]')
        subplot.set_ylabel('radius [kpc]')

        if len(parts) > 1:
            color_names = ut.plot.get_colors(len(parts))
        else:
            color_names = ut.plot.get_colors(len(mass_percents))

        for part_i, part in enumerate(parts):
            for _time_i, time_kind in enumerate(['now', 'form']):
                for m_i, mass_percent in enumerate(mass_percents):
                    if len(parts) > 1:
                        color = color_names[part_i]
                    else:
                        color = color_names[m_i]

                    if time_kind == 'form':
                        linestyle = '-'
                        label = f'$R_{{{mass_percent}}}$'
                    elif time_kind == 'now':
                        linestyle = '--'
                        label = None

                    subplot.plot(
                        AgeBin.mins,
                        radius[time_kind][part_i, m_i],
                        color=color,
                        linestyle=linestyle,
                        alpha=0.7,
                        label=label,
                    )

        ut.plot.make_legends(subplot)

        ut.plot.parse_output(plot_file_name, plot_directory)


MassRadius = MassRadiusClass()


# --------------------------------------------------------------------------------------------------
# host galaxy disk
# --------------------------------------------------------------------------------------------------
class DiskClass(ut.io.SayClass):
    '''
    Examine the disk orientation and axis ratios.
    '''

    def plot_orientation_v_property(
        self,
        parts,
        species_names=['star', 'star.25', 'star.young'],
        property_name='distance',
        property_limits=[1, 15],
        property_bin_width=1,
        property_log_scale=False,
        reference_distance_max=8.2,
        center_positions=None,
        center_velocities=None,
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot orientation angle of the disk versus property_name.

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles (can be different simulations or snapshots)
        species_names : str or list
            name[s] of particle species to compute: 'star', 'gas', 'dark'
        property_name : str
            which property to vary (along x-axis): 'distance', 'age'
        property_limits : list
            min and max property for binning
        property_bin_width : float
            width of property bin
        property_log_scale : bool
            whether to use logarithmic scaling for property
        reference_distance_max : float
            reference distance to compute principal axes
        center_positions : array or list of arrays
            position of center for each particle catalog
        center_velocities : array or list of arrays
            velocity of center for each particle catalog
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        axis_index = 2  # which principal axis to measure orientation angle of
        gas_temperature_limits = [0, 5e4]  # [K]
        young_star_age_limits = [0, 1]  # [Gyr]

        if isinstance(parts, dict):
            parts = [parts]

        center_positions = ut.particle.parse_property(
            parts, 'position', center_positions, host_index
        )

        center_velocities = ut.particle.parse_property(
            parts, 'velocity', center_velocities, host_index
        )

        PropertyBin = ut.binning.BinClass(
            property_limits, property_bin_width, include_max=True, log_scale=property_log_scale
        )

        angles = np.zeros((len(parts), len(species_names), PropertyBin.number)) * np.nan

        for part_i, part in enumerate(parts):
            self.say('{}'.format(part.info['simulation.name']))

            # compute reference principal axes using all stars out to reference_distance
            principal_axes = ut.particle.get_principal_axes(
                part,
                'star',
                reference_distance_max,
                age_limits=[0, 1],
                center_positions=center_positions[part_i],
                center_velocities=center_velocities[part_i],
                host_index=host_index,
                verbose=False,
            )
            reference_rotation = principal_axes['rotation'][axis_index]

            for spec_i, spec_name in enumerate(species_names):
                self.say(f'  {spec_name}')

                if spec_name == 'gas':
                    part_indices = ut.array.get_indices(
                        part[spec_name]['temperature'], gas_temperature_limits
                    )
                elif 'star' in spec_name and 'young' in spec_name:
                    part_indices = ut.array.get_indices(
                        part['star'].prop('age'), young_star_age_limits
                    )
                    spec_name = 'star'
                elif 'star' in spec_name and '.25' in spec_name:
                    star_age_limits = [0, np.percentile(part['star'].prop('age'), 25)]
                    part_indices = ut.array.get_indices(part['star'].prop('age'), star_age_limits)
                    spec_name = 'star'
                else:
                    part_indices = None

                for prop_i, property_max in enumerate(PropertyBin.mins):
                    if property_name == 'distance':
                        distance_max = property_max
                    elif property_name == 'age':
                        part_indices = ut.array.get_indices(
                            part['star'].prop('age'), [0, property_max]
                        )
                        distance_max = reference_distance_max

                    principal_axes = ut.particle.get_principal_axes(
                        part,
                        spec_name,
                        distance_max,
                        center_positions=center_positions[part_i],
                        center_velocities=center_velocities[part_i],
                        host_index=host_index,
                        part_indicess=part_indices,
                        verbose=False,
                    )

                    # get orientation of axis of interest
                    axis_rotation = principal_axes['rotation'][axis_index]
                    angle = np.arccos(np.dot(axis_rotation, reference_rotation))
                    if angle is np.nan:
                        angle = 0  # sanity check, for exact alignment
                    angle *= 180 / np.pi  # [degree]
                    # if angle > 90:
                    #    Say.say(
                    #        '!   {:4.1f} kpc: {:.1f} deg (raw), min/maj = {:.2f}'.format(
                    #            property_max, angle, principal_axes['axis.ratios'][0]
                    #        )
                    #    )
                    #    angle = min(angle, 180 - angle)  # deal with possible flip

                    angles[part_i, spec_i, prop_i] = angle

                    if property_name == 'distance':
                        self.say(
                            '  {:4.1f} kpc: {:.1f} deg, min/maj = {:.2f}'.format(
                                property_max, angle, principal_axes['axis.ratios'][0]
                            )
                        )
                    elif property_name == 'age':
                        self.say('  {:4.1f} Gyr: {:.1f} deg'.format(property_max, angle))

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot, property_log_scale, property_limits, y_limits=[0, None], y_values=angles
        )

        if property_name == 'distance':
            subplot.set_xlabel('maximum radius $\\left[ {{\\rm kpc}} \\right]$')
        else:
            subplot.set_xlabel('star maximum age $\\left[ {{\\rm Gyr}} \\right]$')
        subplot.set_ylabel('disk offset angle $\\left[ {{\\rm deg}} \\right]$')

        if len(parts) > len(species_names):
            color_names = ut.plot.get_colors(len(parts))
        else:
            color_names = ut.plot.get_colors(len(species_names))

        for part_i, part in enumerate(parts):
            for spec_i, spec_name in enumerate(species_names):
                if len(parts) > len(species_names):
                    label = part.info['simulation.name']
                    color = color_names[part_i]
                else:
                    label = spec_name
                    color = color_names[spec_i]

                subplot.plot(
                    PropertyBin.mins, angles[part_i, spec_i], color=color, alpha=0.8, label=label
                )

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            property_y = 'disk.orientation'
            if len(parts) == 1:
                property_y = parts[0].info['simulation.name'] + '_' + property_y
            plot_file_name = ut.plot.get_file_name(
                property_y, property_name, snapshot_dict=part.snapshot
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_orientation_v_time(
        self,
        parts,
        time_name='time.lookback',
        time_limits=[0, 13],
        time_log_scale=False,
        refrence_snapshot_index=600,
        axis_indices=[0, 1, 2],
        angle_limits=[0, 90],
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot orientation angle[s] of the principal axes of the disk (wrt their orientations at
        refrence_snapshot_index) versus time_name.
        Requires that you have read pre-compiled host rotation tensors in host_coordinates.hdf5.

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles (can be different simulations or snapshots)
        time_name : str
            time kind to plot: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        refrence_snapshot_index : int
            index of reference snapshot, that defines angle zero point
        axis_indices : list
            which principal axes to plot the orientation angles of
            0 = minor, 1 = intermediate, 2 = major
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''

        if isinstance(parts, dict):
            parts = [parts]
        if np.isscalar(axis_indices):
            axis_indices = [axis_indices]

        angles = (
            np.zeros((len(parts), len(axis_indices), parts[0].hostz['rotation'].shape[0])) * np.nan
        )

        for part_i, part in enumerate(parts):
            rotation_tensors = part.hostz['rotation'][:, host_index]
            reference_rotation_tensor = rotation_tensors[refrence_snapshot_index]
            for axis_ii, axis_i in enumerate(axis_indices):
                angles[part_i, axis_ii] = np.dot(
                    rotation_tensors[:, axis_i], reference_rotation_tensor[axis_i]
                )

        masks = np.isfinite(angles)
        angles[masks] = np.arccos(angles[masks]) * 180 / np.pi  # [degree]

        if time_name in ['time.lookback', 'age']:
            times = parts[0].Snapshot['time'][-1] - parts[0].Snapshot['time']
        else:
            times = parts[0].Snapshot[time_name]

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, times, False, angle_limits, angles
        )

        subplot.set_xlabel(ut.plot.Label.get_label(time_name, get_words=True))
        subplot.set_ylabel('disk offset angle $\\left[ {{\\rm deg}} \\right]$')

        if len(parts) > len(axis_indices):
            color_names = ut.plot.get_colors(len(parts))
        else:
            color_names = ut.plot.get_colors(len(axis_indices))

        for part_i, part in enumerate(parts):
            for axis_ii, axis_i in enumerate(axis_indices):
                if len(parts) > len(axis_indices):
                    label = part.info['simulation.name']
                    color = color_names[part_i]
                else:
                    label = f'principal axis {axis_i}'
                    color = color_names[axis_ii]

                subplot.plot(times, angles[part_i, axis_ii], color=color, alpha=0.8, label=label)

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                'disk.orientation', time_name, snapshot_dict=part.snapshot
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_axis_ratio_v_time(
        self,
        parts,
        time_name='time.lookback',
        time_limits=[0, 13],
        time_log_scale=False,
        axis_index_numerator=2,
        axis_index_denominator=0,
        axis_ratio_limits=[1, 10],
        host_index=0,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot minor / major axis ratio of the disk versus time_name.
        Requires that you have read pre-compiled host rotation tensors in host_coordinates.hdf5.

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles (can be different simulations or snapshots)
        time_name : str
            time kind to plot: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        axis_index_numerator : int
            which principal axix to use in numerator of ratio
            0 = minor, 1 = intermediate, 2 = major
        axis_index_denominator : int
            which principal axix to use in denominator of ratio
        host_index : int
            index of host galaxy/halo to get stored position of (if not input it)
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        # Say = ut.io.SayClass(plot_disk_orientation_v_time)

        if isinstance(parts, dict):
            parts = [parts]

        axis_ratios = np.zeros((len(parts), parts[0].hostz['axis.ratios'].shape[0])) * np.nan

        for part_i, part in enumerate(parts):
            rs = part.hostz['axis.ratios']
            axis_ratios[part_i] = (
                rs[:, host_index, axis_index_numerator] / rs[:, host_index, axis_index_denominator]
            )

        if time_name in ['time.lookback', 'age']:
            times = parts[0].Snapshot['time'][-1] - parts[0].Snapshot['time']
        else:
            times = parts[0].Snapshot[time_name]

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, times, False, axis_ratio_limits, axis_ratios
        )

        subplot.set_xlabel(ut.plot.Label.get_label(time_name, get_words=True))
        subplot.set_ylabel('disk axis ratio')

        color_names = ut.plot.get_colors(len(parts))

        for part_i, part in enumerate(parts):
            color = color_names[part_i]
            label = None
            if len(parts) > 1:
                label = part.info['simulation.name']

            subplot.plot(times, axis_ratios[part_i], color=color, alpha=0.8, label=label)

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            plot_file_name = ut.plot.get_file_name(
                'disk.axis.ratio', time_name, snapshot_dict=part.snapshot
            )
        ut.plot.parse_output(plot_file_name, plot_directory)


Disk = DiskClass()


# --------------------------------------------------------------------------------------------------
# star formation history
# --------------------------------------------------------------------------------------------------
class StarFormHistoryClass(ut.io.SayClass):
    '''
    .
    '''

    def plot_star_form_history(
        self,
        parts=None,
        sfh_name='form.rate',
        time_name='time.lookback',
        time_limits=[0, 13],
        time_width=0.2,
        time_log_scale=False,
        distance_limits=[0, 15],
        center_positions=None,
        host_index=0,
        property_select={},
        part_indicess=None,
        sfh_limits=None,
        sfh_log_scale=True,
        verbose=False,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot star-formation history v time_name.

        Parameters
        ----------
        parts : dict or list
            catalog[s] of particles
        sfh_name : str
            star form kind to plot: 'form.rate', 'form.rate.specific', 'mass', 'mass.normalized'
        time_name : str
            time kind to use: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        distance_limits : list
            min and max limits of distance to select star particles
        center_positions : list or list of lists
            position[s] of galaxy centers [kpc comoving]
        host_index : int
            index of host galaxy/halo to get position of (if not input center_position)
        property_select : dict
            properties to select on: names as keys and limits as values
        part_indicess : array
            indices of particles from which to select
        sfh_limits : list
            min and max limits for y-axis
        sfh_log_scale : bool
            whether to use logarithmic scaling for SFH bins
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        if isinstance(parts, dict):
            parts = [parts]

        center_positions = ut.particle.parse_property(
            parts, 'position', center_positions, host_index
        )
        part_indicess = ut.particle.parse_property(parts, 'indices', part_indicess)

        time_limits = np.array(time_limits)
        if None in time_limits:
            if time_name == 'redshift':
                if time_limits[0] is None:
                    time_limits[0] = np.floor(parts[0].snapshot[time_name])
                if time_limits[1] is None:
                    time_limits[1] = 7
            elif time_name == 'time':
                if time_limits[0] is None:
                    time_limits[0] = 0
                elif time_limits[1] is None:
                    time_limits[1] = parts[0].snapshot[time_name]
            elif time_name == 'time.lookback':
                if time_limits[0] is None:
                    time_limits[0] = 0
                elif time_limits[1] is None:
                    # time_limits[1] = 13.6  # [Gyr]
                    time_limits[1] = parts[0]['star'].prop('age').max()  # [Gyr]

        sfh = {}

        for part_i, part in enumerate(parts):
            sfh_p = self._get_star_form_history(
                part,
                time_name,
                time_limits,
                time_width,
                time_log_scale,
                distance_limits,
                center_positions[part_i],
                host_index,
                property_select,
                part_indicess[part_i],
            )

            if part_i == 0:
                for k in sfh_p:
                    sfh[k] = []  # initialize

            for k, s in sfh_p.items():
                sfh[k].append(s)

            if verbose:
                self.say(
                    'M_star max = {}'.format(
                        ut.io.get_string_from_numbers(sfh_p['mass'].max(), 2, exponential=True)
                    )
                )

        if time_name == 'redshift' and time_log_scale:
            time_limits += 1  # convert to z + 1 so log is well-defined

        # plot ----------
        left = None
        if 'specific' in sfh_name:
            left = 0.215
        _fig, subplot = ut.plot.make_figure(figure_index, left=left, axis_secondary='x')

        y_values = None
        if sfh is not None:
            y_values = sfh[sfh_name]

        ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, None, sfh_log_scale, sfh_limits, y_values
        )

        axis_x_label = ut.plot.Label.get_label(time_name, get_words=True)
        subplot.set_xlabel(axis_x_label)

        if sfh_name == 'mass.normalized':
            axis_y_label = '$M_{\\rm star}(z) \\, / \\, M_{\\rm star}(z=0)$'
        else:
            axis_y_label = ut.plot.Label.get_label('star.' + sfh_name)
        subplot.set_ylabel(axis_y_label)

        ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, parts[0].Cosmology)

        color_names = ut.plot.get_colors(len(parts))

        for part_i, part in enumerate(parts):
            tis = sfh[sfh_name][part_i] > 0
            if time_name in ['redshift', 'time.lookback', 'age']:
                tis *= sfh[time_name][part_i] >= parts[0].snapshot[time_name] * 0.99
            else:
                tis *= sfh[time_name][part_i] <= parts[0].snapshot[time_name] * 1.01
            subplot.plot(
                sfh[time_name][part_i][tis],
                sfh[sfh_name][part_i][tis],
                color=color_names[part_i],
                alpha=0.8,
                label=part.info['simulation.name'],
            )

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            time_value = None
            if time_name == 'redshift' and min(time_limits) > 1.1 * parts[0].snapshot['redshift']:
                time_value = min(time_limits)
            plot_file_name = ut.plot.get_file_name(
                sfh_name + '.history',
                time_name,
                'star',
                'redshift',
                parts[0].snapshot,
                time_value,
            )
        ut.plot.parse_output(plot_file_name, plot_directory)

    def plot_star_form_history_galaxies(
        self,
        part=None,
        hal=None,
        gal=None,
        mass_name='star.mass',
        mass_limits=[1e5, 1e9],
        property_select={},
        hal_indices=None,
        sfh_name='mass.normalized',
        sfh_limits=None,
        sfh_log_scale=False,
        time_name='time.lookback',
        time_limits=[13.7, 0],
        time_width=0.2,
        time_log_scale=False,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot star-formation history v time_name for multiple galaxies in a halo catalog.

        Parameters
        ----------
        part : dict
            catalog of particles
        hal : dict
            catalog of halos at snapshot
        gal : dict
            catalog of galaxies in the Local Group with SFHs
        mass_name : str
            mass kind by which to select halos
        mass_limits : list
            min and max limits to impose on mass_name
        property_select : dict
            properties to select on: names as keys and limits as values
        hal_indices : index or array
            index[s] of halo[s] whose particles to plot
        sfh_name : str
            star form kind to plot: 'rate', 'rate.specific', 'mass', 'mass.normalized'
        sfh_limits : list
            min and max limits for y axis
        sfh_log_scale : bool
            whether to use logarithmic scaling for y axis
        time_name : str
            time kind to plot: 'time', 'time.lookback', 'age', 'redshift'
        time_limits : list
            min and max limits of time_name to plot
        time_width : float
            width of time_name bin
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        time_limits = np.array(time_limits)
        if part is not None:
            if time_limits[0] is None:
                time_limits[0] = part.snapshot[time_name]
            if time_limits[1] is None:
                time_limits[1] = part.snapshot[time_name]

        sfh = None
        if hal is not None:
            if hal_indices is None or not len(hal_indices) > 0:
                hal_indices = ut.array.get_indices(hal.prop('star.number'), [2, np.inf])

            if mass_limits is not None and len(mass_limits) > 0:
                hal_indices = ut.array.get_indices(hal.prop(mass_name), mass_limits, hal_indices)

            if property_select:
                hal_indices = ut.catalog.get_indices_catalog(hal, property_select, hal_indices)

            hal_indices = hal_indices[np.argsort(hal.prop(mass_name, hal_indices))]

            print(f'halo number = {hal_indices.size}')

            sfh = {}

            for hal_ii, hal_i in enumerate(hal_indices):
                part_indices = hal.prop('star.indices', hal_i)
                sfh_h = self._get_star_form_history(
                    part,
                    time_name,
                    time_limits,
                    time_width,
                    time_log_scale,
                    part_indices=part_indices,
                )

                if hal_ii == 0:
                    for k in sfh_h:
                        sfh[k] = []  # initialize

                for k, s in sfh_h.items():
                    sfh[k].append(s)

                string = 'id = {:8d}, star.mass = {:.3e}, particle.number = {}, distance = {:.0f}'
                self.say(
                    string.format(
                        hal_i,
                        sfh_h['mass'].max(),
                        part_indices.size,
                        hal.prop('host.distance', hal_i),
                    )
                )
                # print(hal.prop('position', hal_i))

            for k in sfh:
                sfh[k] = np.array(sfh[k])

            sfh['mass.normalized.median'] = np.median(sfh['mass.normalized'], 0)

        if time_name == 'redshift' and time_log_scale:
            time_limits += 1  # convert to z + 1 so log is well-defined

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index, axis_secondary='x')

        y_values = None
        if sfh is not None:
            y_values = sfh[sfh_name]

        ut.plot.set_axes_scaling_limits(
            subplot, time_log_scale, time_limits, None, sfh_log_scale, sfh_limits, y_values
        )

        subplot.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))

        axis_x_label = ut.plot.Label.get_label(time_name, get_words=True)
        subplot.set_xlabel(axis_x_label)

        if sfh_name == 'mass.normalized':
            axis_y_label = '$M_{\\rm star}(z) \\, / \\, M_{\\rm star}(z=0)$'
        else:
            axis_y_label = ut.plot.Label.get_label('star.' + sfh_name)
        subplot.set_ylabel(axis_y_label)

        ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, part.Cosmology)

        if hal is not None:
            color_names = ut.plot.get_colors(len(hal_indices))
        elif gal is not None:
            color_names = ut.plot.get_colors(len(gal.sfh))

        label = None

        # draw observed galaxies
        if gal is not None:
            import string

            gal_names = np.array(list(gal.sfh.keys()))
            gal_indices = [gal['name.to.index'][gal_name] for gal_name in gal_names]
            gal_names_sort = gal_names[np.argsort(gal['star.mass'][gal_indices])]

            for gal_i, gal_name in enumerate(gal_names_sort):
                linestyle = '-'
                if hal is not None:
                    color = 'black'
                    linewidth = 1.0 + 0.25 * gal_i
                    alpha = 0.2
                    label = None
                else:
                    color = color_names[gal_i]
                    linewidth = 1.25 + 0.25 * gal_i
                    alpha = 0.45
                    label = string.capwords(gal_name)
                    label = label.replace('Canes Venatici I', 'CVn I').replace('Ii', 'II')

                    print(label)
                subplot.plot(
                    gal.sfh[gal_name][time_name],
                    gal.sfh[gal_name][sfh_name],
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=alpha,
                    color=color,
                    label=label,
                )

        # draw simulated galaxies
        if hal is not None:
            label = '$M_{{\\rm star}} = $'
            subplot.plot(-1, -1, label=label)
            for hal_ii, hal_i in enumerate(hal_indices):
                linewidth = 2.5 + 0.1 * hal_ii
                # linewidth = 3.0
                mass = ut.io.get_string_from_numbers(sfh['mass'][hal_ii][-1], 1, exponential=True)
                label = f'${mass} \\, {{\\rm M_\\odot}}$'
                subplot.plot(
                    sfh[time_name][hal_ii],
                    sfh[sfh_name][hal_ii],
                    linewidth=linewidth,
                    color=color_names[hal_ii],
                    alpha=0.55,
                    label=label,
                )

        # subplot.plot(sfh['time'][0], sfh['mass.normalized.median'],
        #             linewidth=4.0, color='black', alpha=0.5)

        ut.plot.make_legends(subplot, time_value=part.snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            snapshot_dict = None
            if part is not None:
                snapshot_dict = part.snapshot
            time_name_file_name = 'redshift'
            if hal is None:
                time_name_file_name = None
            host_distance_limits = None
            if 'host.distance' in property_select:
                host_distance_limits = property_select['host.distance']

            plot_file_name = ut.plot.get_file_name(
                sfh_name,
                time_name,
                'star',
                time_name_file_name,
                snapshot_dict,
                host_distance_limits=host_distance_limits,
            )
            if gal is not None:
                plot_file_name += '_lg'
        ut.plot.parse_output(plot_file_name, plot_directory)

    def _get_star_form_history(
        self,
        part,
        time_name='redshift',
        time_limits=[0, 8],
        time_width=0.1,
        time_log_scale=False,
        distance_limits=None,
        center_position=None,
        host_index=0,
        property_select={},
        part_indices=None,
    ):
        '''
        Get array of times and star-formation rate at each time.

        Parameters
        ----------
        part : dict
            catalog of particles
        time_name : str
            time metric to use: 'time', 'time.lookback', 'age', 'redshift', 'scalefactor'
        time_limits : list
            min and max limits of time_name to impose
        time_width : float
            width of time_name bin (in units set by time_scaling)
        time_log_scale : bool
            whether to use logarithmic scaling for time bins
        distance_limits : list
            min and max limits of galaxy distance to select star particles
        center_position : list
            position of galaxy centers [kpc comoving]
        host_index : int
            index of host galaxy/halo to get position of (if not input it)
        property_select : dict
            dictionary with property names as keys and limits as values
        part_indices : array
            indices of star particles to select

        Returns
        -------
        sfh : dictionary
            arrays of SFH properties
        '''
        species = 'star'

        if part_indices is None:
            part_indices = ut.array.get_arange(part[species]['mass'])

        if property_select:
            part_indices = ut.catalog.get_indices_catalog(
                part['star'], property_select, part_indices
            )

        center_position = ut.particle.parse_property(part, 'position', center_position, host_index)

        if (
            center_position is not None
            and len(center_position) > 0
            and distance_limits is not None
            and len(distance_limits) > 0
            and (min(distance_limits) > 0 or max(distance_limits) < np.inf)
        ):
            distances = ut.coordinate.get_distances(
                part['star']['position'][part_indices],
                center_position,
                part.info['box.length'],
                part.snapshot['scalefactor'],
                total_distance=True,
            )  # [kpc physical]
            part_indices = part_indices[ut.array.get_indices(distances, distance_limits)]

        # get formation times of star particles, sorted from earliest
        part_indices_sort = part_indices[np.argsort(part[species].prop('form.time', part_indices))]
        form_times = part[species].prop('form.time', part_indices_sort)
        # avoid precision error with cumsum below
        form_masses = part[species].prop('form.mass', part_indices_sort).astype(np.float64)
        current_masses = part[species]['mass'][part_indices_sort].astype(np.float64)

        # get time bins, ensure are ordered from earliest
        time_dict = part.Cosmology.get_time_bins(time_name, time_limits, time_width, time_log_scale)
        time_bins = np.sort(time_dict['time'])
        time_difs = np.diff(time_bins)

        form_mass_cum_bins = np.interp(time_bins, form_times, np.cumsum(form_masses))
        form_mass_difs = np.diff(form_mass_cum_bins)
        form_rate_bins = form_mass_difs / time_difs / ut.constant.giga  # convert to [M_sun / yr]

        current_mass_cum_bins = np.interp(time_bins, form_times, np.cumsum(current_masses))
        current_mass_difs = np.diff(current_mass_cum_bins)

        # convert to midpoints of bins
        current_mass_cum_bins = (
            current_mass_cum_bins[: current_mass_cum_bins.size - 1] + 0.5 * current_mass_difs
        )
        form_mass_cum_bins = (
            form_mass_cum_bins[: form_mass_cum_bins.size - 1] + 0.5 * form_mass_difs
        )

        for k in time_dict:
            time_dict[k] = time_dict[k][: time_dict[k].size - 1] + 0.5 * np.diff(time_dict[k])

        # ensure that ordering jives with ordering of input limits
        if time_dict['time'][0] > time_dict['time'][1]:
            form_rate_bins = form_rate_bins[::-1]
            current_mass_cum_bins = current_mass_cum_bins[::-1]
            form_mass_cum_bins = form_mass_cum_bins[::-1]

        sfh = {}
        for k in time_dict:
            sfh[k] = time_dict[k]
        sfh['form.rate'] = form_rate_bins
        sfh['form.rate.specific'] = form_rate_bins / form_mass_cum_bins
        sfh['mass'] = current_mass_cum_bins
        sfh['mass.normalized'] = current_mass_cum_bins / current_mass_cum_bins.max()
        sfh['particle.number'] = form_times.size

        return sfh


def plot_star_form_cluster_fraction(
    part,
    grps,
    host_distance_limits=[0, 100],
    # host_distance_limits=None,
):
    '''
    .
    '''
    from scipy import ndimage

    assert grps[-1].info['catalog.kind'] == 'star.group'

    cluster_age_limits = grps[-1].info['fof.age']

    group_snapshot_indices = np.array([i for i, grp in enumerate(grps) if len(grp)])
    # group_snapshot_indices = group_snapshot_indices[group_snapshot_indices < 300]

    ages = part.Snapshot['time.lookback'][group_snapshot_indices]
    cluster_mass_fractions = np.zeros(group_snapshot_indices.size)

    star_ages = part['star'].prop('age')
    star_masses = part['star'].prop('mass')
    if host_distance_limits is not None:
        star_form_distances = part['star'].prop('form.host.distance.total')

    for sii, si in enumerate(group_snapshot_indices):
        print(si)

        if host_distance_limits is not None:
            distance_limits = np.array(host_distance_limits) * part.Snapshot['scalefactor'][si]

        grp = grps[si]
        if host_distance_limits is not None:
            gis = ut.array.get_indices(grp.prop('host.distance.total'), distance_limits)
            cluster_mass = grp['mass'][gis].sum()
        else:
            cluster_mass = grp['mass'].sum()

        age_limits = ages[sii] + cluster_age_limits
        pis = ut.array.get_indices(star_ages, age_limits)
        if host_distance_limits is not None:
            pis = ut.array.get_indices(star_form_distances, distance_limits, pis)
        star_mass = star_masses[pis].sum()

        cluster_mass_fractions[sii] = cluster_mass / star_mass

    _fig, subplot = ut.plot.make_figure()
    ut.plot.set_axes_scaling_limits(subplot, False, [0, 13.8], None, False, [0, 0.6])
    subplot.set_xlabel('age [Gyr]')
    subplot.set_ylabel('cluster fraction')

    subplot.plot(ages, cluster_mass_fractions)

    ys_smooth = ndimage.gaussian_filter1d(cluster_mass_fractions, 5)
    subplot.plot(ages, ys_smooth, color='black')


# --------------------------------------------------------------------------------------------------
# analysis across time
# --------------------------------------------------------------------------------------------------
def write_galaxy_properties_v_time(
    simulation_directory=gizmo_default.simulation_directory, redshifts=None, species=['star']
):
    '''
    Read snapshots and store dictionary of host galaxy properties (such as mass and radius)
    at snapshots.

    Parameters
    ----------
    simulation_directory : str
        root directory of simulation
    redshifts : array-like
        redshifts at which to get properties
            'all' = read and store all snapshots
    species : str or list
        name[s] of species to read and get properties of

    Returns
    -------
    gal : dict
        dictionary of host galaxy properties at input redshifts
    '''
    Read = gizmo_io.ReadClass()

    star_distance_max = 15

    properties_read = ['mass', 'position']

    mass_percents = [50, 90]

    simulation_directory = ut.io.get_path(simulation_directory)

    gal = {'index': [], 'redshift': [], 'scalefactor': [], 'time': [], 'time.lookback': []}

    for spec_name in species:
        gal[f'{spec_name}.position'] = []
        for mass_percent in mass_percents:
            gal['{}.radius.{:.0f}'.format(spec_name, mass_percent)] = []
            gal['{}.mass.{:.0f}'.format(spec_name, mass_percent)] = []

    if redshifts == 'all' or redshifts is None or redshifts == []:
        Snapshot = ut.simulation.SnapshotClass()
        Snapshot.read_snapshots(gizmo_default.snapshot_time_file_name, simulation_directory)
        redshifts = Snapshot['redshift']
    else:
        if np.isscalar(redshifts):
            redshifts = [redshifts]

    redshifts = np.sort(redshifts)

    for _zi, redshift in enumerate(redshifts):
        part = Read.read_snapshots(
            species, 'redshift', redshift, simulation_directory, properties=properties_read
        )

        for k in ['index', 'redshift', 'scalefactor', 'time', 'time.lookback']:
            gal[k].append(part.snapshot[k])

        # get position and velocity
        gal['star.position'].append(part.host['position'][0])

        for spec_name in species:
            for mass_percent in mass_percents:
                gal_prop = ut.particle.get_galaxy_properties(
                    part, spec_name, 'mass.percent', mass_percent, distance_max=star_distance_max
                )
                k = '{}.radius.{:.0f}'.format(spec_name, mass_percent)
                gal[k].append(gal_prop['radius'])
                k = '{}.mass.{:.0f}'.format(spec_name, mass_percent)
                gal[k].append(gal_prop['radius'])

    for prop_name in gal:
        gal[prop_name] = np.array(gal[prop_name])

    ut.io.file_pickle(simulation_directory + 'host_properties_v_time', gal)

    return gal


def plot_galaxy_property_v_time(
    gals=None,
    sfhs=None,
    Cosmology=None,
    property_name='star.mass',
    time_name='redshift',
    time_limits=[0, 8],
    time_log_scale=False,
    snapshot_subsample_factor=1,
    axis_y_limits=None,
    axis_y_log_scale=True,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    Plot host galaxy property v time_name, using tabulated dictionary of properties of progenitor
    across snapshots.

    Parameters
    ----------
    gals : dict
        tabulated dictionary of host galaxy properties
    sfhs : dict
        tabulated dictinnary of star-formation histories (computed at single snapshot)
    property_name : str
        name of star formation history property to plot:
            'rate', 'rate.specific', 'mass', 'mass.normalized'
    time_name : str
        time kind to use: 'time', 'time.lookback', 'redshift'
    time_limits : list
        min and max limits of time_name to get
    time_log_scale : bool
        whether to use logarithmic scaling for time bins
    snapshot_subsample_factor : int
        factor by which to sub-sample snapshots from gals
    axis_y_limits : list
        min and max limits for y axis
    axis_y_log_scale : bool
        whether to use logarithmic scaling for y axis
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    figure_index : int
        index of figure for matplotlib
    '''
    # Say = ut.io.SayClass(plot_galaxy_property_v_time)

    if gals is not None and isinstance(gals, dict):
        gals = [gals]

    if sfhs is not None and isinstance(sfhs, dict):
        sfhs = [sfhs]

    time_limits = np.array(time_limits)
    if time_limits[0] is None:
        time_limits[0] = gals[0][time_name].min()
    if time_limits[1] is None:
        time_limits[1] = gals[0][time_name].max()

    if time_name == 'redshift' and time_log_scale:
        time_limits += 1  # convert to z + 1 so log is well-defined

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    y_values = []
    if gals is not None:
        y_values.append(gals[0][property_name])
    if sfhs is not None:
        y_values.append(sfhs[0][time_name])
    subplot.set_ylim(ut.plot.get_axis_limits(y_values, axis_y_log_scale, axis_y_limits))

    axis_y_label = ut.plot.Label.get_label('star.mass')
    subplot.set_ylabel(axis_y_label)

    ut.plot.make_axis_secondary_time(subplot, time_name, time_limits, Cosmology)

    # colors = ut.plot.get_colors(len(gals))

    if gals is not None:
        for _gal_i, gal in enumerate(gals):
            subplot.plot(
                gal[time_name][::snapshot_subsample_factor],
                gal[property_name][::snapshot_subsample_factor],
                linewidth=3.0,
                alpha=0.9,
                # color=colors[gal_i],
                color=ut.plot.get_color('blue.mid'),
                label='main progenitor',
            )

    if sfhs is not None:
        for _sfh_i, sfh in enumerate(sfhs):
            subplot.plot(
                sfh[time_name],
                sfh['mass'],
                '--',
                linewidth=3.0,
                alpha=0.9,
                # color=colors[sfh_i],
                color=ut.plot.get_color('orange.mid'),
                label='SFH computed at $z=0$',
            )

    ut.plot.make_legends(subplot)

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = f'galaxy_{property_name}_v_{time_name}'
    ut.plot.parse_output(plot_file_name, plot_directory)


def get_galaxy_mass_profiles_v_redshift(
    directory='.',
    redshifts=[3, 2.75, 2.5, 2.25, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25, 0],
    parts=None,
):
    '''
    Read snapshots and store dictionary of galaxy/halo position, velocity, size, mass at input
    scale-factors, for Shea.

    Parameters
    ----------
    directory : str : directory of snapshot files
    redshifts : array-like : redshifts at which to get properties
    parts : list : list of particle dictionaries

    Returns
    -------
    dictionary of galaxy/halo properties at each redshift
    '''
    Read = gizmo_io.ReadClass()

    species_read = ['star', 'dark']
    properties_read = ['mass', 'position', 'velocity', 'potential']

    star_distance_max = 20
    dark_distance_max = 50

    profile_species_name = 'star'
    profile_mass_percents = [50, 90]

    gal = {
        'index': [],  # snapshot index
        'redshift': [],  # snapshot redshift
        'scalefactor': [],  # snapshot scale-factor
        'time': [],  # snapshot time [Gyr]
        'time.lookback': [],  # snapshot lookback time [Gyr]
        'star.position': [],  # position of galaxy (star) center [kpc comoving]
        'star.velocity': [],  # center-of-mass velocity of stars within R_50 [km s]
        'dark.position': [],  # position of DM center [kpc comoving]
        'dark.velocity': [],  # center-of-mass velocity of DM within 0.5 * R_200m [km/s]
        'rotation': [],  # rotation tensor of disk
        'axis.ratios': [],  # axis ratios of disk
        'profile.3d.distance': [],  # distance bins in 3-D [kpc physical]
        'profile.3d.density': [],  # density, in 3-D [M_sun / kpc ^ 3]
        'profile.major.distance': [],  # distance bins along major (R) axis [kpc physical]
        'profile.major.density': [],  # surface density, in 2-D [M_sun / kpc ^ 2]
        'profile.minor.bulge.distance': [],  # distance bins along minor (Z) axis [kpc physical]
        'profile.minor.bulge.density': [],  # density, in 1-D [M_sun / kpc]
        'profile.minor.disk.distance': [],  # distance bins along minor (Z) axis [kpc physical]
        'profile.minor.disk.density': [],  # density, in 1-D [M_sun / kpc]
    }

    for mass_percent in profile_mass_percents:
        mass_percent_name = '{:.0f}'.format(mass_percent)

        gal['radius.3d.' + mass_percent_name] = []  # stellar R_{50,90} in 3-D [kpc physical]
        gal['mass.3d.' + mass_percent_name] = []  # associated stellar mass [M_sun}

        gal['radius.major.' + mass_percent_name] = []  # stellar R_{50,90} along major axis
        gal['mass.major.' + mass_percent_name] = []  # associated stellar mass [M_sun]

        gal['radius.minor.' + mass_percent_name] = []  # stellar R_{50,90} along minor axis
        gal['mass.minor.' + mass_percent_name] = []  # associated stellar mass [M_sun]

    for z_i, redshift in enumerate(redshifts):
        if parts is not None and len(parts) > 0:
            part = parts[z_i]
        else:
            part = Read.read_snapshots(
                species_read, 'redshift', redshift, directory, properties=properties_read
            )

        for k in ['index', 'redshift', 'scalefactor', 'time', 'time.lookback']:
            gal[k].append(part.snapshot[k])

        # get position and velocity
        gal['star.position'].append(part.host['position'][0])
        gal['star.velocity'].append(part.host['velocity'][0])

        gal['dark.position'].append(
            ut.particle.get_center_positions(part, 'dark', weight_property='potential')
        )
        gal['dark.velocity'].append(
            ut.particle.get_center_velocities_or_accelerations(
                part, 'velocity', 'dark', distance_max=dark_distance_max
            )
        )

        # get radius_90 as fiducial
        gal_90 = ut.particle.get_galaxy_properties(
            part, profile_species_name, 'mass.percent', mass_percent, distance_max=star_distance_max
        )

        principal_axes = ut.particle.get_principal_axes(
            part, profile_species_name, gal_90['radius']
        )

        gal['rotation'].append(principal_axes['rotation'])
        gal['axis.ratios'].append(principal_axes['axis.ratios'])

        for mass_percent in profile_mass_percents:
            mass_percent_name = '{:.0f}'.format(mass_percent)

            gal = ut.particle.get_galaxy_properties(
                part,
                profile_species_name,
                'mass.percent',
                mass_percent,
                distance_max=star_distance_max,
            )
            gal['radius.3d.' + mass_percent_name].append(gal['radius'])
            gal['mass.3d.' + mass_percent_name].append(gal['mass'])

            gal_minor = ut.particle.get_galaxy_properties(
                part,
                profile_species_name,
                'mass.percent',
                mass_percent,
                'minor',
                star_distance_max,
                rotation_tensor=principal_axes['rotation'],
                other_axis_distance_limits=[0, gal_90['radius']],
            )
            gal['radius.minor.' + mass_percent_name].append(gal_minor['radius'])
            gal['mass.minor.' + mass_percent_name].append(gal_minor['mass'])

            gal_major = ut.particle.get_galaxy_properties(
                part,
                profile_species_name,
                'mass.percent',
                mass_percent,
                'major',
                star_distance_max,
                rotation_tensor=principal_axes['rotation'],
                other_axis_distance_limits=[0, gal_minor['radius']],
            )
            gal['radius.major.' + mass_percent_name].append(gal_major['radius'])
            gal['mass.major.' + mass_percent_name].append(gal_major['radius'])

        pro = plot_property_v_distance(
            part,
            profile_species_name,
            'mass',
            'density',
            True,
            [None, None],
            None,
            [0.05, 20],
            0.1,
            True,
            3,
            get_values=True,
        )
        for k in ['distance', 'density']:
            gal['profile.3d.' + k].append(pro[profile_species_name][k])

        pro = plot_property_v_distance(
            part,
            profile_species_name,
            'mass',
            'density',
            True,
            [None, None],
            None,
            [0.05, 20],
            0.1,
            True,
            2,
            rotation=principal_axes['rotation'],
            other_axis_distance_limits=[0, 1],
            get_values=True,
        )
        for k in ['distance', 'density']:
            gal['profile.major.' + k].append(pro[profile_species_name][k])

        pro = plot_property_v_distance(
            part,
            profile_species_name,
            'mass',
            'density',
            True,
            [None, None],
            None,
            [0.05, 20],
            0.1,
            True,
            1,
            rotation=principal_axes['rotation'],
            other_axis_distance_limits=[0, 0.05],
            get_values=True,
        )
        for k in ['distance', 'density']:
            gal['profile.minor.bulge.' + k].append(pro[profile_species_name][k])

        pro = plot_property_v_distance(
            part,
            profile_species_name,
            'mass',
            'density',
            True,
            [None, None],
            None,
            [0.05, 20],
            0.1,
            True,
            1,
            rotation=principal_axes['rotation'],
            other_axis_distance_limits=[1, 10],
            get_values=True,
        )
        for k in ['distance', 'density']:
            gal['profile.minor.disk.' + k].append(pro[profile_species_name][k])

    for prop_name in gal:
        gal[prop_name] = np.array(gal[prop_name])

    return gal


def print_galaxy_mass_v_redshift(gal):
    '''
    Print galaxy/halo position, velocity, size, mass over time for Shea.

    Parameters
    ----------
    gal : dict
        dictionary of galaxy properties across snapshots
    '''
    print('# redshift scale-factor time[Gyr] ', end='')
    print('star_position(x,y,z)[kpc comov] ', end='')
    print('star_velocity(x,y,z)[km/s] dark_velocity(x,y,z)[km/s] ', end='')
    print('R_50[kpc] M_star_50[Msun] M_gas_50[Msun] M_dark_50[Msun] ', end='')
    print('R_90[kpc] M_star_90[Msun] M_gas_90[Msun] M_dark_90[Msun]', end='\n')

    for z_i in range(gal['redshift'].size):
        print(
            '{:.5f} {:.5f} {:.5f} '.format(
                gal['redshift'][z_i], gal['scalefactor'][z_i], gal['time'][z_i]
            ),
            end='',
        )
        print(
            '{:.3f} {:.3f} {:.3f} '.format(
                gal['star.position'][z_i][0],
                gal['star.position'][z_i][1],
                gal['star.position'][z_i][2],
            ),
            end='',
        )
        print(
            '{:.3f} {:.3f} {:.3f} '.format(
                gal['star.velocity'][z_i][0],
                gal['star.velocity'][z_i][1],
                gal['star.velocity'][z_i][2],
            ),
            end='',
        )
        print(
            '{:.3f} {:.3f} {:.3f} '.format(
                gal['dark.velocity'][z_i][0],
                gal['dark.velocity'][z_i][1],
                gal['dark.velocity'][z_i][2],
            ),
            end='',
        )
        print(
            '{:.3e} {:.3e} {:.3e} {:.3e} '.format(
                gal['radius.50'][z_i],
                gal['star.mass.50'][z_i],
                gal['gas.mass.50'][z_i],
                gal['dark.mass.50'][z_i],
            ),
            end='',
        )
        print(
            '{:.3e} {:.3e} {:.3e} {:.3e}'.format(
                gal['radius.90'][z_i],
                gal['star.mass.90'][z_i],
                gal['gas.mass.90'][z_i],
                gal['dark.mass.90'][z_i],
            ),
            end='\n',
        )


def plot_gas_neutral_fraction_v_redshift(
    parts=None,
    redshift_limits=[6, 8.4],
    simulation_directory=gizmo_default.simulation_directory,
    plot_file_name=False,
    plot_directory='.',
    figure_index=1,
):
    '''
    .
    '''
    if parts is None:
        Snapshot = ut.simulation.read_snapshot_times(simulation_directory)
        snapshot_indices = ut.array.get_indices(
            Snapshot['redshift'], [min(redshift_limits) * 0.99, max(redshift_limits) * 1.01]
        )
        redshifts = Snapshot['redshift'][snapshot_indices]

        Read = gizmo_io.ReadClass()

        parts = Read.read_snapshots(
            'gas',
            'index',
            snapshot_indices,
            simulation_directory,
            properties=['mass', 'density', 'hydrogen.neutral.fraction'],
            assign_hosts=False,
        )
    else:
        snapshot_indices = np.array([part.snapshot['index'] for part in parts], np.int32)
        redshifts = parts[0].Snapshot['redshift'][snapshot_indices]

    # Statistic = ut.math.StatisticClass()

    neutral_fraction_by_mass = {}
    neutral_fraction_by_volume = {}
    for part in parts:
        values = part['gas']['hydrogen.neutral.fraction']

        # weights = None
        weights = part['gas']['mass']
        # Stat = Statistic.get_statistic_dict(values, weights=weights)
        stat = {}
        # stat['median'] = ut.math.percentile_weighted(values, 50, weights)
        # stat['percent.16'] = ut.math.percentile_weighted(values, 16, weights)
        # stat['percent.84'] = ut.math.percentile_weighted(values, 84, weights)
        stat['average'] = np.sum(values * weights) / np.sum(weights)
        stat['std'] = np.sqrt(np.sum(weights / np.sum(weights) * (values - stat['average']) ** 2))
        stat['std.lo'] = stat['average'] - stat['std']
        stat['std.hi'] = stat['average'] + stat['std']
        ut.array.append_dictionary(neutral_fraction_by_mass, stat)

        weights = part['gas']['mass'] / part['gas']['density']
        # Stat = Statistic.get_statistic_dict(values, weights=weights)
        stat = {}
        # stat['median'] = ut.math.percentile_weighted(values, 50, weights)
        # stat['percent.16'] = ut.math.percentile_weighted(values, 16, weights)
        # stat['percent.84'] = ut.math.percentile_weighted(values, 84, weights)
        stat['average'] = np.sum(values * weights) / np.sum(weights)
        stat['std'] = np.sqrt(np.sum(weights / np.sum(weights) * (values - stat['average']) ** 2))
        stat['std.lo'] = stat['average'] - stat['std']
        stat['std.hi'] = stat['average'] + stat['std']

        ut.array.append_dictionary(neutral_fraction_by_volume, stat)

    ut.array.arrayize_dictionary(neutral_fraction_by_mass)
    ut.array.arrayize_dictionary(neutral_fraction_by_volume)

    # plot ----------
    _fig, subplot = ut.plot.make_figure(figure_index)

    ut.plot.set_axes_scaling_limits(subplot, x_values=redshifts, y_limits=[0, 1])

    subplot.set_xlabel('redshift')
    subplot.set_ylabel('neutral fraction')

    color_names = ut.plot.get_colors(2)

    # name_hi = 'percent.84'
    # name_mid = 'median'
    # name_lo = 'percent.16'

    name_hi = 'std.hi'
    name_mid = 'average'
    name_lo = 'std.lo'

    subplot.fill_between(
        redshifts,
        neutral_fraction_by_mass[name_lo],
        neutral_fraction_by_mass[name_hi],
        alpha=0.4,
        color=color_names[0],
    )
    subplot.plot(redshifts, neutral_fraction_by_mass[name_mid], label='mass-weighted')

    subplot.fill_between(
        redshifts,
        neutral_fraction_by_volume[name_lo],
        neutral_fraction_by_volume[name_hi],
        alpha=0.4,
        color=color_names[1],
    )
    subplot.plot(redshifts, neutral_fraction_by_volume[name_mid], label='volume-weighted')

    ut.plot.make_legends(subplot)

    if plot_file_name is True or plot_file_name == '':
        plot_file_name = 'gas.neutral.frac_v_redshift'
    ut.plot.parse_output(plot_file_name, plot_directory)

    return parts


# --------------------------------------------------------------------------------------------------
# properties of halos
# --------------------------------------------------------------------------------------------------
class HalosClass(ut.io.SayClass):
    '''
    Analysis that uses halo catalogs.
    '''

    def assign_vel_circ_at_radius(
        self,
        part,
        hal,
        radius=0.6,
        sort_property_name='vel.circ.max',
        sort_property_value_min=20,
        halo_number_max=100,
        host_distance_limits=[1, 310],
    ):
        '''
        .
        '''
        his = ut.array.get_indices(hal.prop('mass.bound/mass'), [0.1, np.inf])
        his = ut.array.get_indices(hal['host.distance'], host_distance_limits, his)
        his = ut.array.get_indices(hal[sort_property_name], [sort_property_value_min, np.inf], his)
        self.say(f'{his.size} halos within limits')

        his = his[np.argsort(hal[sort_property_name][his])]
        his = his[::-1][:halo_number_max]

        mass_key = 'vel.circ.rad.{:.1f}'.format(radius)
        hal[mass_key] = np.zeros(hal['mass'].size)
        dark_mass = np.median(part['dark']['mass'])

        for hii, hi in enumerate(his):
            if hii > 0 and hii % 10 == 0:
                ut.io.print_flush(hii)
            pis = ut.particle.get_indices_within_coordinates(
                part, 'dark', None, [0, radius], hal['position'][hi]
            )
            hal[mass_key][hi] = ut.halo_property.get_circular_velocity(pis.size * dark_mass, radius)

    def plot_vel_circ_v_distance(
        self,
        parts=None,
        hals=None,
        part_indicesss=None,
        hal_indicess=None,
        pros=None,
        gal=None,
        total_mass_limits=None,
        star_mass_limits=[1e5, np.inf],
        host_distance_limits=[1, 310],
        sort_property_name='vel.circ.max',
        sort_property_value_min=15,
        halo_number_max=20,
        vel_circ_limits=[0, 50],
        vel_circ_log_scale=False,
        radius_limits=[0.1, 3],
        radius_bin_width=0.1,
        radius_log_scale=True,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        .
        '''
        if isinstance(hals, dict):
            hals = [hals]
        if hal_indicess is not None:
            if np.isscalar(hal_indicess):
                hal_indicess = [hal_indicess]
            if np.isscalar(hal_indicess[0]):
                hal_indicess = [hal_indicess]

        hiss = None
        if hals is not None:
            hiss = []
            for cat_i, hal in enumerate(hals):
                his = None
                if hal_indicess is not None:
                    his = hal_indicess[cat_i]
                his = ut.array.get_indices(hal.prop('mass.bound/mass'), [0.1, np.inf], his)
                his = ut.array.get_indices(hal['mass'], total_mass_limits, his)
                his = ut.array.get_indices(hal['host.distance'], host_distance_limits, his)

                if 'star.indices' in hal:
                    his = ut.array.get_indices(hal['star.mass'], star_mass_limits, his)
                else:
                    his = ut.array.get_indices(
                        hal[sort_property_name], [sort_property_value_min, np.inf], his
                    )
                    his = his[np.argsort(hal[sort_property_name][his])[::-1]]
                    his = his[:halo_number_max]

                    self.say(
                        '{} halos with {} [min, max] = [{:.3f}, {:.3f}]'.format(
                            his.size,
                            sort_property_name,
                            hal[sort_property_name][his[0]],
                            hal[sort_property_name][his[-1]],
                        )
                    )

                hiss.append(his)

        gal_indices = None
        if gal is not None:
            gal_indices = ut.array.get_indices(gal['star.mass'], star_mass_limits)
            gal_indices = ut.array.get_indices(
                gal['host.distance'], host_distance_limits, gal_indices
            )
            gal_indices = gal_indices[gal['host.name'][gal_indices] == 'MW'.encode()]

        pros = self.plot_property_v_distance(
            parts,
            hals,
            part_indicesss,
            hiss,
            pros,
            gal,
            gal_indices,
            'total',
            'mass',
            'vel.circ',
            vel_circ_log_scale,
            vel_circ_limits,
            None,
            radius_limits,
            radius_bin_width,
            radius_log_scale,
            3,
            None,
            plot_file_name,
            plot_directory,
            figure_index,
        )

        # plot_property_v_distance_halos(
        #    parts, hals, part_indicesss, hiss,
        #    None,
        #    gal, gal_indices,
        #    'star', 'velocity.total', 'std.cum', vel_circ_log_scale, True, vel_circ_limits,
        #    radius_limits, radius_bin_width, radius_log_scale, 3, False,
        #    plot_file_name, plot_directory, figure_index)

        return pros

    def plot_property_v_distance(
        self,
        parts=None,
        hals=None,
        part_indicesss=None,
        hal_indicess=None,
        pros=None,
        gal=None,
        gal_indices=None,
        species_name='total',
        property_name='mass',
        property_statistic='vel.circ',
        property_log_scale=False,
        property_limits=None,
        weight_property='mass',
        distance_limits=[0.1, 3],
        distance_bin_width=0.1,
        distance_log_scale=True,
        dimension_number=3,
        distance_reference=None,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        parts : dict or list
            catalog[s] of particles at snapshot
        hals : dict or list
            catalog[s] of halos at snapshot
        part_indicesss : array (halo catalog number x halo number x particle number)
        hal_indicess : array (halo catalog number x halo number)
            indices of halos to plot
        gal : dict
            catalog of observed galaxies
        gal_indices : array
            indices of galaxies to plot
        species_name : str
            name of particle species to compute mass from: 'dark', 'star', 'gas', 'baryon', 'total'
        property_name : str
            property to get profile of
        property_statistic : str
            statistic/type to plot: sum, sum.cum, density, density.cum, vel.circ, sum.fraction,
            sum.cum.fraction, median, ave
        property_log_scale : bool
            whether to use logarithmic scaling for property bins
        weight_property : str
            property to weight each particle by
        property_limits : list
            limits to impose on y-axis
        distance_limits : list
            min and max distance for binning
        distance_bin_width : float
            width of distance bin
        distance_log_scale : bool
            whether to use logarithmic scaling for distance bins
        dimension_number : int
            number of spatial dimensions for profile
        distance_reference : float
            reference distance at which to draw vertical line
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        if isinstance(hals, dict):
            hals = [hals]
        if hal_indicess is not None:
            if np.isscalar(hal_indicess):
                hal_indicess = [hal_indicess]
            if np.isscalar(hal_indicess[0]):
                hal_indicess = [hal_indicess]
        if isinstance(parts, dict):
            parts = [parts]

        # widen so curves extend to edge of figure
        distance_limits_bin = [
            distance_limits[0] - distance_bin_width,
            distance_limits[1] + distance_bin_width,
        ]

        SpeciesProfile = ut.particle.SpeciesProfileClass(
            distance_limits_bin,
            width=distance_bin_width,
            log_scale=distance_log_scale,
            dimension_number=dimension_number,
        )

        if pros is None:
            pros = []
            if hals is not None:
                for cat_i, hal in enumerate(hals):
                    part = parts[cat_i]
                    hal_indices = hal_indicess[cat_i]

                    if species_name == 'star' and hal['star.position'].max() > 0:
                        position_name = 'star.position'
                        velocity_name = 'star.velocity'
                    elif species_name == 'dark' and hal['dark.position'].max() > 0:
                        position_name = 'dark.position'
                        velocity_name = 'dark.velocity'
                    else:
                        # position_name = 'position'
                        # velocity_name = 'velocity'
                        position_name = 'dark.position'
                        velocity_name = 'dark.velocity'

                    pros_cat = []

                    for hal_i in hal_indices:
                        if part_indicesss is not None:
                            part_indices = part_indicesss[cat_i][hal_i]
                        elif species_name == 'star' and 'star.indices' in hal:
                            part_indices = hal['star.indices'][hal_i]
                        # elif species == 'dark' and 'dark.indices' in hal:
                        #    part_indices = hal['dark.indices'][hal_i]
                        else:
                            part_indices = None

                        pro_hal = SpeciesProfile.get_profiles(
                            part,
                            species_name,
                            property_name,
                            property_statistic,
                            weight_property,
                            center_position=hal[position_name][hal_i],
                            center_velocity=hal[velocity_name][hal_i],
                            part_indicess=part_indices,
                        )

                        pros_cat.append(pro_hal)
                    pros.append(pros_cat)

        # plot ----------
        _fig, subplot = ut.plot.make_figure(figure_index)

        y_values = []
        for pro_cat in pros:
            for pro_hal in pro_cat:
                y_values.append(pro_hal[species_name][property_statistic])

        ut.plot.set_axes_scaling_limits(
            subplot,
            distance_log_scale,
            distance_limits,
            None,
            property_log_scale,
            property_limits,
            y_values,
        )

        if distance_log_scale:
            subplot.xaxis.set_ticks([0.1, 0.2, 0.3, 0.5, 1, 2])
            subplot.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
        else:
            subplot.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))

        # subplot.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

        axis_x_label = ut.plot.Label.get_label('radius', get_words=True)
        subplot.set_xlabel(axis_x_label)

        if property_statistic in ['vel.circ']:
            label_property_name = property_statistic
        else:
            label_property_name = property_name
        axis_y_label = ut.plot.Label.get_label(
            label_property_name, property_statistic, species_name, dimension_number=dimension_number
        )
        subplot.set_ylabel(axis_y_label)

        # draw reference values
        if (
            'fraction' in property_statistic
            or 'beta' in property_name
            or 'velocity.rad' in property_name
        ):
            if 'fraction' in property_statistic:
                y_values = [1, 1]
            elif 'beta' in property_name:
                y_values = [0, 0]
            elif 'velocity.rad' in property_name:
                y_values = [0, 0]
            subplot.plot(
                distance_limits, y_values, color='black', linestyle=':', alpha=0.5, linewidth=2
            )

        if distance_reference is not None:
            subplot.plot(
                [distance_reference, distance_reference],
                property_limits,
                color='black',
                linestyle=':',
                alpha=0.6,
            )

        # draw halos
        if hals is not None:
            color_names = ut.plot.get_colors(len(hals))
            for cat_i, hal in enumerate(hals):
                hal_indices = hal_indicess[cat_i]
                for hal_ii, hal_i in enumerate(hal_indices):
                    color = color_names[cat_i]
                    linewidth = 1.9
                    alpha = 0.5

                    if (
                        pros[cat_i][hal_ii][species_name][property_statistic][0] > 12.5
                    ):  # dark vel.circ
                        color = ut.plot.get_color('blue.lite')
                        linewidth = 3.0
                        alpha = 0.8

                    if species_name == 'star':
                        linewidth = 2.0
                        alpha = 0.6
                        color = ut.plot.get_color('orange.mid')
                        if pros[cat_i][hal_ii][species_name][property_statistic][-1] > 27:
                            color = ut.plot.get_color('orange.lite')
                            linewidth = 3.5
                            alpha = 0.9

                    subplot.plot(
                        pros[cat_i][hal_ii][species_name]['distance'],
                        pros[cat_i][hal_ii][species_name][property_statistic],
                        color=color,
                        linestyle='-',
                        alpha=alpha,
                        linewidth=linewidth,
                        # label=parts[part_i].info['simulation.name'],
                    )

        # draw observed galaxies
        if gal is not None:
            gis = ut.array.get_indices(gal['star.radius.50'], distance_limits, gal_indices)
            gis = gis[gal['host.name'][gis] == 'MW'.encode()]
            print(gal['vel.circ.50'][gis] / gal['star.vel.std'][gis])
            for gal_i in gis:
                subplot.errorbar(
                    gal['star.radius.50'][gal_i],
                    gal['vel.circ.50'][gal_i],
                    [[gal['vel.circ.50.err.lo'][gal_i]], [gal['vel.circ.50.err.hi'][gal_i]]],
                    color='black',
                    marker='s',
                    markersize=10,
                    alpha=0.7,
                    capthick=2.5,
                )

        ut.plot.make_legends(subplot, time_value=parts[0].snapshot['redshift'])

        if plot_file_name is True or plot_file_name == '':
            snapshot_dict = None
            if parts is not None:
                snapshot_dict = parts[0].snapshot
            plot_file_name = ut.plot.get_file_name(
                property_name + '.' + property_statistic,
                'dist',
                species_name,
                snapshot_dict=snapshot_dict,
            )
            plot_file_name = plot_file_name.replace('.sum', '')
            plot_file_name = plot_file_name.replace('mass.vel.circ', 'vel.circ')
            plot_file_name = plot_file_name.replace('mass.density', 'density')
        ut.plot.parse_output(plot_file_name, plot_directory)

        return pros

    def plot_density_profile(
        self,
        part,
        species_name='star',
        hal=None,
        hal_index=None,
        center_position=None,
        distance_limits=[0.1, 2],
        distance_bin_width=0.1,
        plot_file_name=False,
        plot_directory='.',
        figure_index=1,
    ):
        '''
        Plot density profile for single halo/center.

        Parameters
        ----------
        part : dict
            catalog of particles at snapshot
        species_name : str
            name of particle species to plot
        hal : dict
            catalog of halos at snapshot
        hal_index : int
            index of halo in catalog
        center_position : array
            position to center profile (to use instead of halo position)
        distance_max : float
            max distance (radius) for galaxy image
        distance_bin_width : float
            length of pixel for galaxy image
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str
            directory to write figure file
        figure_index : int
            index of figure for matplotlib
        '''
        distance_log_scale = True
        dimension_number = 3

        if center_position is None:
            center_positions = []
            # center_positions.append(hal['position'][hal_index])
            if 'star.position' in hal and hal['star.position'][hal_index][0] > 0:
                center_positions.append(hal['star.position'][hal_index])
        else:
            center_positions = [center_position]

        parts = [part]
        if len(center_positions) == 2:
            parts = [part, part]

        if 'star.radius.50' in hal and hal['star.radius.50'][hal_index] > 0:
            distance_reference = hal['star.radius.50'][hal_index]
        else:
            distance_reference = None

        plot_property_v_distance(
            parts,
            species_name,
            'mass',
            'density',
            True,
            [None, None],
            None,
            distance_limits,
            distance_bin_width,
            distance_log_scale,
            dimension_number,
            center_positions=center_positions,
            part_indicess=None,
            distance_reference=distance_reference,
            plot_file_name=plot_file_name,
            plot_directory=plot_directory,
            figure_index=figure_index,
        )

    def plot_density_profiles(
        self,
        part,
        hal,
        hal_indices,
        species_name='dark',
        density_limits=None,
        distance_limits=[0.05, 1],
        distance_bin_width=0.2,
        plot_only_members=False,
        plot_file_name=False,
        plot_directory='.',
        figure_index=0,
    ):
        '''
        plot_file_name : str
            whether to write figure to file and its name. True = use default naming convention
        plot_directory : str : directory to write figure file
        figure_index : int : index of figure for matplotlib
        '''
        parts = []
        center_positions = []
        part_indicess = None
        for hal_i in hal_indices:
            parts.append(part)
            if 'star.position' in hal:
                center_positions.append(hal.prop('star.position', hal_i))
                if plot_only_members:
                    part_indicess.append(hal.prop(species_name + '.indices', hal_i))
            else:
                center_positions.append(hal.prop('position', hal_i))
                if plot_only_members:
                    part_indicess.append(hal.prop(species_name + '.indices', hal_i))

        plot_property_v_distance(
            parts,
            species_name,
            'mass',
            'density',
            True,
            density_limits,
            None,
            distance_limits,
            distance_bin_width,
            True,
            3,
            center_positions=center_positions,
            part_indicess=part_indicess,
            plot_file_name=plot_file_name,
            plot_directory=plot_directory,
            figure_index=figure_index,
        )


def explore_galaxy(
    hal,
    hal_index=None,
    part=None,
    species_plot=['star'],
    distance_max=None,
    distance_bin_width=0.2,
    distance_bin_number=None,
    plot_only_members=True,
    # plot_file_name=False,
    # plot_directory='.',
):
    '''
    Print and plot several properties of galaxies in list.

    Parameters
    ----------
    hal : dict
        catalog of halos at snapshot
    hal_index : int
        index within halo catalog
    part : dict
        atalog of particles at snapshot
    species_plot : str or dict
        which particle species to plot
    distance_max : float
        max distance (radius) for galaxy image
    distance_bin_width : float
        length of pixel for galaxy image
    distance_bin_number : int
        number of pixels for galaxy image
    plot_only_members : bool
        whether to plat only particles that are members of halo
    plot_file_name : str
        whether to write figure to file and its name. True = use default naming convention
    plot_directory : str
        directory to write figure file
    '''
    from halo_analysis import halo_plot

    halo_plot.print_properties(hal, hal_index)

    hi = hal_index

    StarFormHistory = StarFormHistoryClass()

    if part is not None:
        if not distance_max and 'star.radius.90' in hal:
            distance_max = 3 * hal.prop('star.radius.90', hi)

        if 'star' in species_plot and 'star' in part and 'star.indices' in hal:
            part_indices = None
            if plot_only_members:
                part_indices = hal.prop('star.indices', hi)

            # image of member particles
            Image.plot_image(
                part,
                'star',
                'mass',
                'histogram',
                [0, 1, 2],
                [0, 1, 2],
                distance_max,
                distance_bin_width,
                distance_bin_number,
                hal.prop('star.position', hi),
                part_indices=part_indices,
                figure_index=10,
            )

            # image of all nearby particles
            Image.plot_image(
                part,
                'star',
                'mass',
                'histogram',
                [0, 1, 2],
                [0, 1, 2],
                distance_max,
                distance_bin_width,
                distance_bin_number,
                hal.prop('star.position', hi),
                figure_index=11,
            )

            # image of all nearby particles
            Image.plot_image(
                part,
                'star',
                'mass',
                'histogram',
                [0, 1, 2],
                [0, 1, 2],
                distance_max * 5,
                distance_bin_width,
                distance_bin_number,
                hal.prop('star.position', hi),
                figure_index=12,
            )

            # distribution of total velocity
            plot_property_distribution(
                part,
                'star',
                property_name='velocity.total',
                property_limits=[0, None],
                property_bin_width=2,
                property_bin_number=None,
                property_log_scale=False,
                property_statistic='histogram',
                distance_limits=[0, distance_max],
                center_positions=hal.prop('star.position', hi),
                center_velocities=hal.prop('star.velocity', hi),
                part_indicess=part_indices,
                axis_y_limits=[0, None],
                axis_y_log_scale=False,
                figure_index=13,
            )

            plot_property_distribution(
                part,
                'star',
                property_name='metallicity.iron',
                property_limits=[-4, 0.5],
                property_bin_width=0.1,
                property_bin_number=None,
                property_log_scale=False,
                property_statistic='histogram',
                distance_limits=[0, distance_max],
                center_positions=hal.prop('star.position', hi),
                part_indicess=part_indices,
                axis_y_limits=[0, None],
                axis_y_log_scale=False,
                figure_index=14,
            )

            StarFormHistory.plot_star_form_history(
                part,
                sfh_name='mass.normalized',
                time_name='time.lookback',
                time_limits=[13.6, 0],
                time_width=0.2,
                time_log_scale=False,
                distance_limits=[0, distance_max],
                center_positions=hal.prop('star.position', hi),
                part_indicess=part_indices,
                sfh_limits=[0, 1],
                sfh_log_scale=False,
                figure_index=15,
            )

            plot_property_v_distance(
                part,
                'star',
                property_name='mass',
                property_statistic='density',
                property_log_scale=True,
                property_limits=[None, None],
                distance_limits=[0.1, distance_max],
                distance_bin_width=0.1,
                distance_log_scale=True,
                dimension_number=3,
                center_positions=hal.prop('star.position', hi),
                part_indicess=part_indices,
                distance_reference=hal.prop('star.radius.50', hi),
                figure_index=16,
            )

            plot_property_v_distance(
                part,
                'star',
                property_name='velocity.total',
                property_statistic='std.cum',
                property_log_scale=False,
                property_limits=[None, None],
                distance_limits=[0.1, distance_max],
                distance_bin_width=0.1,
                distance_log_scale=True,
                center_positions=hal.prop('star.position', hi),
                center_velocities=hal.prop('star.velocity', hi),
                part_indicess=part_indices,
                distance_reference=hal.prop('star.radius.50', hi),
                figure_index=17,
            )

            plot_property_v_distance(
                part,
                'star',
                property_name='metallicity.iron',
                property_statistic='median',
                property_log_scale=False,
                property_limits=[None, None],
                distance_limits=[0.1, distance_max],
                distance_bin_width=0.2,
                distance_log_scale=True,
                center_positions=hal.prop('star.position', hi),
                part_indicess=part_indices,
                distance_reference=hal.prop('star.radius.50', hi),
                figure_index=18,
            )

        if 'dark' in species_plot and 'dark' in part:
            part_indices = None

            if 'star.radius.50' in hal:
                distance_reference = hal.prop('star.radius.50', hi)
            else:
                distance_reference = None

            # DM image centered on stars
            Image.plot_image(
                part,
                'dark',
                'mass',
                'histogram',
                [0, 1, 2],
                [0, 1, 2],
                distance_max,
                distance_bin_width,
                distance_bin_number,
                hal.prop('star.position', hi),
                background_color='black',
                figure_index=20,
            )

            # DM image centered on DM halo
            Image.plot_image(
                part,
                'dark',
                'mass',
                'histogram',
                [0, 1, 2],
                [0, 1, 2],
                distance_max,
                distance_bin_width,
                distance_bin_number,
                hal.prop('position', hi),
                background_color='black',
                figure_index=21,
            )

            plot_property_v_distance(
                part,
                'dark',
                property_name='mass',
                property_statistic='density',
                property_log_scale=True,
                property_limits=[None, None],
                distance_limits=[0.1, distance_max],
                distance_bin_width=0.1,
                distance_log_scale=True,
                center_positions=hal.prop('position', hi),
                part_indicess=part_indices,
                distance_reference=distance_reference,
                figure_index=22,
            )

            plot_property_v_distance(
                part,
                'dark',
                property_name='mass',
                property_statistic='vel.circ',
                property_log_scale=False,
                property_limits=[None, None],
                distance_limits=[0.1, distance_max],
                distance_bin_width=0.1,
                distance_log_scale=True,
                center_positions=hal.prop('position', hi),
                part_indicess=part_indices,
                distance_reference=distance_reference,
                figure_index=23,
            )

        if 'gas' in species_plot and 'gas' in part and 'gas.indices' in hal:
            part_indices = None
            if plot_only_members:
                part_indices = hal.prop('gas.indices', hi)

            if part_indices is None or len(part_indices) >= 3:
                Image.plot_image(
                    part,
                    'gas',
                    'mass',
                    'histogram',
                    [0, 1, 2],
                    [0, 1, 2],
                    distance_max,
                    distance_bin_width,
                    distance_bin_number,
                    hal.prop('star.position', hi),
                    part_indices=part_indices,
                    figure_index=30,
                )

                Image.plot_image(
                    part,
                    'gas',
                    'mass.neutral',
                    'histogram',
                    [0, 1, 2],
                    [0, 1, 2],
                    distance_max,
                    distance_bin_width,
                    distance_bin_number,
                    hal.prop('star.position', hi),
                    part_indices=part_indices,
                    figure_index=31,
                )
            else:
                fig = plt.figure(10)
                fig.clf()
                fig = plt.figure(11)
                fig.clf()


# --------------------------------------------------------------------------------------------------
# compare simulations
# --------------------------------------------------------------------------------------------------
class CompareSimulationsClass(ut.io.SayClass):
    '''
    Analyze and plot different simulations for comparison.
    '''

    def __init__(
        self,
        galaxy_radius_limits=[0, 15],
        galaxy_profile_radius_limits=[0.1, 30],
        halo_profile_radius_limits=[0.5, 300],
        plot_directory='plot',
    ):
        '''
        Set directories and names of simulations to read.
        '''
        self.Read = gizmo_io.ReadClass()

        self.properties = ['mass', 'position', 'form.scalefactor', 'massfraction']

        self.galaxy_radius_limits = galaxy_radius_limits
        self.galaxy_profile_radius_limits = galaxy_profile_radius_limits
        self.halo_profile_radius_limits = halo_profile_radius_limits

        self.plot_directory = ut.io.get_path(plot_directory)

        self.simulation_names = []

    def _parse_inputs(self, parts=None, species=None, redshifts=None):
        '''
        parts : list
            dictionaries of particles at snapshot
        species : str or list
            name[s] of particle species to read and analyze
        redshifts : float or list
        '''
        if parts is not None and isinstance(parts, dict):
            parts = [parts]

        if species is not None and np.isscalar(species):
            species = [species]

        if redshifts is None:
            redshifts = parts[0].snapshot['redshift']
        if np.isscalar(redshifts):
            redshifts = [redshifts]

        if parts is not None and redshifts is not None and len(redshifts) > 1:
            self.say('! input particles at single snapshot but also input more than one redshift')
            self.say(
                '  analyzing just snapshot redshift = {:.3f}'.format(parts[0].snapshot['redshift'])
            )
            redshifts = [parts[0].snapshot['redshift']]

        return parts, species, redshifts

    def plot(
        self,
        parts=None,
        species=['star', 'gas', 'dark'],
        simulation_directories=None,
        redshifts=None,
        galaxy_radius_limits=None,
        plot_properties_v_distance=True,
        plot_abundances=True,
        plot_properties_v_properties=True,
        plot_histories=True,
        plot_images=True,
    ):
        '''
        Analyze and plot all quantities for all simulations at each redshift.

        Parameters
        ----------
        parts : list
            dictionaries of particles at snapshot
        species : str or list
            name[s] of particle species to read and analyze
        simulation_directories : list
            simulation directories and names/labels for figure
        redshifts : float or list
        parts, species, redshifts = self._parse_inputs(parts, species, redshifts)
        '''
        if redshifts is None or np.isscalar(redshifts):
            redshifts = [redshifts]

        for redshift in redshifts:
            if redshift is not None and redshift >= 0 and parts is None:
                parts = self.Read.read_snapshots_simulations(
                    species,
                    'redshift',
                    redshift,
                    simulation_directories,
                    properties=self.properties,
                    assign_hosts_rotation=True,
                )

            if 'star' in species:
                self.print_masses_sizes(parts, ['star'])
            if plot_properties_v_distance:
                self.plot_properties_v_distance(parts, plot_abundances=plot_abundances)
            if plot_abundances and plot_properties_v_properties:
                self.plot_properties_v_properties(parts)
            if plot_histories:
                self.plot_histories(parts, galaxy_radius_limits)
            if plot_images:
                self.plot_images(parts)

    def print_masses_sizes(self, parts, species=['star'], distance_max=20, mass_fraction=90):
        '''
        Print masses and sizes of simulations / galaxies.

        Parameters
        ----------
        parts : list of dicts
            catalogs of particles at snapshot
        species : str or list
            name[s] of particle species to read and analyze
        distance_max : float
            maximum distance from center to plot
        mass_fraction : float
            mass fraction (within distance_max) to determine edge of galaxy
        '''
        if species is not None and np.isscalar(species):
            species = [species]

        if isinstance(parts, dict):
            parts = [parts]

        gals = []
        for spec_name in ut.array.get_list_combined(species, parts[0], 'intersect'):
            for part in parts:
                gal = ut.particle.get_galaxy_properties(
                    part, spec_name, 'mass.percent', mass_fraction, 'both', distance_max
                )
                gals.append(gal)

            self.say(f'\n# species = {spec_name}')

            for part_i, part in enumerate(parts):
                gal = gals[part_i]
                self.say('\n{}'.format(part.info['simulation.name']))

                self.say(
                    '* M_{},sim = {} Msun, log = {:.2f}'.format(
                        spec_name,
                        ut.io.get_string_from_numbers(part[spec_name]['mass'].sum(), 2, True),
                        np.log10(part[spec_name]['mass'].sum()),
                    )
                )

                pindices = ut.array.get_indices(
                    part[spec_name].prop('host.distance.total'), [0, distance_max]
                )
                self.say(
                    '* M_{}(< {:.0f} kpc) = {} Msun, log = {:.2f}'.format(
                        spec_name,
                        distance_max,
                        ut.io.get_string_from_numbers(
                            part[spec_name]['mass'][pindices].sum(), 2, True
                        ),
                        np.log10(part[spec_name]['mass'][pindices].sum()),
                    )
                )

                distance_min = 50
                pindices = ut.array.get_indices(
                    part[spec_name].prop('host.distance.total'), [distance_min, np.inf]
                )
                self.say(
                    '* M_{}(> {:.0f} kpc) = {} Msun, log = {:.2f}'.format(
                        spec_name,
                        distance_min,
                        ut.io.get_string_from_numbers(
                            part[spec_name]['mass'][pindices].sum(), 2, True
                        ),
                        np.log10(part[spec_name]['mass'][pindices].sum()),
                    )
                )

                self.say(
                    '* M_{},{} = {} Msun, log = {:.2f}'.format(
                        spec_name,
                        mass_fraction,
                        ut.io.get_string_from_numbers(gal['mass'], 2, True),
                        np.log10(gal['mass']),
                    )
                )
                self.say(
                    '* R_{},{} major, minor = {:.1f}, {:.1f} kpc'.format(
                        spec_name, mass_fraction, gal['radius.major'], gal['radius.minor']
                    )
                )
        print()

    def plot_properties_v_distance(self, parts, distance_bin_width=0.1, plot_abundances=True):
        '''
        Plot profiles of various properties, comparing all simulations at each redshift.

        Parameters
        ----------
        parts : list
            dictionaries of particles at snapshot
        distance_bin_width : float
            width of distance bin
        plot_abundances : bool
            whether to plot elemental abundances
        '''
        if 'dark' in parts[0] and 'gas' in parts[0] and 'star' in parts[0]:
            plot_property_v_distance(
                parts,
                'total',
                'mass',
                'vel.circ',
                False,
                [0, None],
                None,
                [0.1, self.halo_profile_radius_limits[1]],
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            plot_property_v_distance(
                parts,
                'total',
                'mass',
                'sum.cum',
                True,
                [None, None],
                None,
                self.halo_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            plot_property_v_distance(
                parts,
                'baryon',
                'mass',
                'sum.cum.fraction',
                False,
                [0, 2],
                None,
                [10, 2000],
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

        spec_name = 'dark'
        if spec_name in parts[0]:
            plot_property_v_distance(
                parts,
                spec_name,
                'mass',
                'sum.cum',
                True,
                [None, None],
                None,
                self.halo_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            plot_property_v_distance(
                parts,
                spec_name,
                'mass',
                'density',
                True,
                [None, None],
                None,
                self.halo_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

        spec_name = 'gas'
        if spec_name in parts[0]:
            plot_property_v_distance(
                parts,
                spec_name,
                'mass',
                'sum.cum',
                True,
                [None, None],
                None,
                self.halo_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            if 'massfraction' in parts[0][spec_name] and plot_abundances:
                try:
                    plot_property_v_distance(
                        parts,
                        spec_name,
                        'metallicity.metals',
                        'median',
                        False,
                        [None, None],
                        'mass',
                        self.halo_profile_radius_limits,
                        distance_bin_width,
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )

                    plot_property_distribution(
                        parts,
                        spec_name,
                        'metallicity.metals',
                        [-5, 1.3],
                        0.1,
                        None,
                        False,
                        'probability',
                        self.halo_profile_radius_limits,
                        axis_y_limits=[1e-4, None],
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )
                except Exception:
                    pass

        spec_name = 'star'
        if spec_name in parts[0]:
            plot_property_v_distance(
                parts,
                spec_name,
                'mass',
                'sum.cum',
                True,
                [None, None],
                None,
                self.halo_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            plot_property_v_distance(
                parts,
                spec_name,
                'mass',
                'density',
                True,
                [None, None],
                None,
                self.galaxy_profile_radius_limits,
                distance_bin_width,
                plot_file_name=True,
                plot_directory=self.plot_directory,
            )

            if 'massfraction' in parts[0][spec_name] and plot_abundances:
                try:
                    plot_property_v_distance(
                        parts,
                        spec_name,
                        'metallicity.fe',
                        'median',
                        False,
                        [None, None],
                        'mass',
                        self.galaxy_profile_radius_limits,
                        distance_bin_width,
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )

                    plot_property_distribution(
                        parts,
                        spec_name,
                        'metallicity.fe',
                        [-5, 1.3],
                        0.1,
                        None,
                        False,
                        'probability',
                        self.galaxy_radius_limits,
                        axis_y_limits=[1e-4, None],
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )
                except Exception:
                    pass

                try:
                    plot_property_v_distance(
                        parts,
                        spec_name,
                        'metallicity.mg - metallicity.fe',
                        'median',
                        False,
                        [None, None],
                        'mass',
                        self.galaxy_profile_radius_limits,
                        distance_bin_width,
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )

                    plot_property_distribution(
                        parts,
                        spec_name,
                        'metallicity.mg - metallicity.fe',
                        [-1.7, 0.6],
                        0.1,
                        None,
                        False,
                        'probability',
                        self.galaxy_radius_limits,
                        axis_y_limits=[1e-4, None],
                        plot_file_name=True,
                        plot_directory=self.plot_directory,
                    )
                except Exception:
                    pass

            if 'form.scalefactor' in parts[0][spec_name] and parts[0].snapshot['redshift'] <= 5:
                plot_property_v_distance(
                    parts,
                    spec_name,
                    'age',
                    'average',
                    False,
                    [None, None],
                    'mass',
                    self.galaxy_radius_limits,
                    distance_bin_width * 2,
                    False,
                    plot_file_name=True,
                    plot_directory=self.plot_directory,
                )

    def plot_histories(self, parts, galaxy_radius_limits=[0, 15], plot_directory=None):
        '''
        Plot histories of star formation and mass.

        Parameters
        ----------
        parts : list
            dictionaries of particles at snapshot
        '''
        if galaxy_radius_limits is None or len(galaxy_radius_limits) == 0:
            galaxy_radius_limits = self.galaxy_radius_limits

        if plot_directory is None or len(plot_directory) == 0:
            plot_directory = self.plot_directory

        StarFormHistory = StarFormHistoryClass()

        if 'star' in parts[0]:
            StarFormHistory.plot_star_form_history(
                parts,
                'mass',
                'redshift',
                [None, 6],
                0.1,
                False,
                galaxy_radius_limits,
                sfh_limits=[None, None],
                plot_file_name=True,
                plot_directory=plot_directory,
            )

            StarFormHistory.plot_star_form_history(
                parts,
                'mass',
                'redshift',
                [3, 10],
                0.1,
                False,
                galaxy_radius_limits,
                sfh_limits=[None, None],
                plot_file_name=True,
                plot_directory=plot_directory,
            )

            StarFormHistory.plot_star_form_history(
                parts,
                'form.rate',
                'time.lookback',
                [None, 13],
                0.5,
                False,
                galaxy_radius_limits,
                sfh_limits=[0, None],
                sfh_log_scale=False,
                plot_file_name=True,
                plot_directory=plot_directory,
            )

            # StarFormHistory.plot_star_form_history(
            #    parts,
            #    'form.rate',
            #    'redshift',
            #    [3, 10],
            #    0.5,
            #    False,
            #    galaxy_radius_limits,
            #    sfh_limits=[0, None],
            #    sfh_log_scale=False,
            #    plot_file_name=True,
            #    plot_directory=plot_directory,
            # )

            # StarFormHistory.plot_star_form_history(
            #    parts,
            #    'form.rate.specific',
            #    'time.lookback',
            #    [None, 13],
            #    0.4,
            #    False,
            #    galaxy_radius_limits,
            #    sfh_limits=[None, None],
            #    plot_file_name=True,
            #    plot_directory=plot_directory,
            # )

    def plot_properties_v_properties(self, parts, property_bin_number=100):
        '''
        Plot property v property for each simulation.

        Parameters
        ----------
        parts : list
            dictionaries of particles at snapshot
        property_bin_number : int
            number of bins along each dimension for histogram
        '''
        plot_directory = self.plot_directory + 'property_2d'

        for part in parts:
            species_name = 'star'
            if species_name in part:
                if 'massfraction' in parts[0][species_name]:
                    try:
                        plot_property_v_property(
                            part,
                            species_name,
                            'metallicity.fe',
                            [-3, 1],
                            False,
                            'metallicity.mg - metallicity.fe',
                            [-0.5, 0.55],
                            False,
                            property_bin_number,
                            host_distance_limits=self.galaxy_radius_limits,
                            draw_statistics=False,
                            plot_file_name=True,
                            plot_directory=plot_directory,
                            add_simulation_name=True,
                        )

                        plot_property_v_property(
                            part,
                            species_name,
                            'age',
                            [0, 13.5],
                            False,
                            'metallicity.fe',
                            [-3, 1],
                            False,
                            property_bin_number,
                            host_distance_limits=self.galaxy_radius_limits,
                            draw_statistics=True,
                            plot_file_name=True,
                            plot_directory=plot_directory,
                            add_simulation_name=True,
                        )

                        plot_property_v_property(
                            part,
                            species_name,
                            'age',
                            [0, 13.5],
                            False,
                            'metallicity.mg - metallicity.fe',
                            [-0.5, 0.55],
                            False,
                            property_bin_number,
                            host_distance_limits=self.galaxy_radius_limits,
                            draw_statistics=True,
                            plot_file_name=True,
                            plot_directory=plot_directory,
                            add_simulation_name=True,
                        )
                    except Exception:
                        pass

            species_name = 'gas'
            # if species_name in part:
            #    plot_property_v_property(
            #        part, species_name,
            #        'number.density', [-4, 4], True,
            #        'temperature', [10, 1e7], True,
            #        property_bin_number, host_distance_limits=self.galaxy_radius_limits,
            #        draw_statistics=False,
            #        plot_file_name=True, plot_directory=plot_directory, add_simulation_name=True,
            #    )

    def plot_images(
        self, parts, distance_max=21, distance_bin_width=0.05, align_principal_axes=True
    ):
        '''
        Plot images of each simulation.

        Parameters
        ----------
        parts : list
            dictionaries of particles at snapshot
        distance_max : float
            maximum distance from center to plot
        distance_bin_width : float
            distance bin width (pixel size)
        align_principal_axes : bool
            whether to align plot axes with principal axes
        '''
        plot_directory = self.plot_directory + 'image'

        for part in parts:
            species_name = 'star'
            if species_name in part:
                Image.plot_image(
                    part,
                    species_name,
                    'mass',
                    'histogram',
                    [0, 1, 2],
                    [0, 1, 2],
                    distance_max,
                    distance_bin_width,
                    rotation=align_principal_axes,
                    image_limits=[10**6, 10**10.5],
                    background_color='black',
                    plot_file_name=True,
                    plot_directory=plot_directory,
                )

            species_name = 'gas'
            if species_name in part:
                Image.plot_image(
                    part,
                    species_name,
                    'mass',
                    'histogram',
                    [0, 1, 2],
                    [0, 1, 2],
                    distance_max,
                    distance_bin_width,
                    rotation=align_principal_axes,
                    image_limits=[10**4, 10**9],
                    background_color='black',
                    plot_file_name=True,
                    plot_directory=plot_directory,
                )

            species_name = 'dark'
            if species_name in part:
                Image.plot_image(
                    part,
                    species_name,
                    'mass',
                    'histogram',
                    [0, 1, 2],
                    [0, 1, 2],
                    distance_max,
                    distance_bin_width,
                    rotation=align_principal_axes,
                    image_limits=[10**5.5, 10**9],
                    background_color='black',
                    plot_file_name=True,
                    plot_directory=plot_directory,
                )


def compare_star_formation_models(
    parts,
    density_limits=[1, 1e6],
    density_bin_width=0.2,
    distance_limits=[0, 12],
    distance_bin_width=0.05,
):
    '''
    .
    '''
    # get indices of star-forming gas
    part_indicess = []
    for part in parts:
        part_indicess.append(ut.array.get_indices(part['gas']['sfr'], [1e-10, 1e10]))

    # distribution of gas densities ----------
    # plot density of star-forming gas
    plot_file_name = 'gas.sf.density_distribution_z.{:.1f}'.format(parts[0].snapshot['redshift'])
    plot_property_distribution(
        parts,
        'gas',
        'number.density',
        density_limits,
        density_bin_width,
        None,
        weight_property=None,
        part_indicess=part_indicess,
        distance_limits=None,
        plot_file_name=plot_file_name,
    )

    # plot density of star-forming gas weighted by SFR
    plot_file_name = 'gas.sf.density*sfr_distribution_z.{:.1f}'.format(
        parts[0].snapshot['redshift']
    )
    plot_property_distribution(
        parts,
        'gas',
        'number.density',
        density_limits,
        density_bin_width,
        None,
        weight_property='sfr',
        part_indicess=part_indicess,
        distance_limits=None,
        plot_file_name=plot_file_name,
    )

    # plot density of all gas
    plot_file_name = 'gas.density_distribution_z.{:.1f}'.format(parts[0].snapshot['redshift'])
    plot_property_distribution(
        parts,
        'gas',
        'number.density',
        density_limits,
        density_bin_width,
        None,
        distance_limits=distance_limits,
        plot_file_name=plot_file_name,
    )

    # image ----------
    distance_max = max(distance_limits)

    # plot image of all gas
    for part in parts:
        Image.plot_image(
            part,
            'gas',
            'mass',
            'histogram',
            [0, 1],
            distances_max=distance_max,
            distance_bin_width=distance_bin_width,
            rotation=True,
            image_limits=[2e6, 1e9],
            plot_file_name=part.info['simulation.name'] + '_gas',
        )

        # plot image of dense gas
        Image.plot_image(
            part,
            'gas',
            'mass',
            'histogram',
            [0, 1],
            distances_max=distance_max,
            distance_bin_width=distance_bin_width,
            rotation=True,
            property_select={'number.density': [10, np.inf]},
            image_limits=[2e6, 1e9],
            plot_file_name=part.info['simulation.name'] + '_gas.10cm3',
        )

        # plot image of young stars
        Image.plot_image(
            part,
            'star',
            'mass',
            'histogram',
            [0, 1],
            distances_max=distance_max,
            distance_bin_width=distance_bin_width,
            rotation=True,
            property_select={'age': [0, 0.1]},
            image_limits=[2e6, 3e8],
            plot_file_name=part.info['simulation.name'] + '_star.100Myr',
        )


def compare_resolution(
    parts=None,
    simulation_names=None,
    redshifts=[0],
    distance_limits=[0.01, 20],
    distance_bin_width=0.1,
):
    '''
    .
    '''
    if not simulation_names:
        simulation_names = []

    if np.isscalar(redshifts):
        redshifts = [redshifts]

    if parts is None:
        parts = []
        for simulation_directory, simulation_name in simulation_names:
            for redshift in redshifts:
                assign_hosts = True
                if 'res880' in simulation_directory:
                    assign_hosts = False
                Read = gizmo_io.ReadClass()
                part = Read.read_snapshots(
                    'dark',
                    'redshift',
                    redshift,
                    simulation_directory,
                    simulation_name=simulation_name,
                    properties=['position', 'mass'],
                    assign_hosts=assign_hosts,
                )
                if len(redshifts) > 1:
                    part.info['simulation.name'] += ' z={:.1f}'.format(redshift)

                parts.append(part)

    plot_property_v_distance(
        parts,
        'dark',
        'mass',
        'vel.circ',
        True,
        [None, None],
        None,
        distance_limits,
        distance_bin_width,
        plot_file_name=True,
    )

    plot_property_v_distance(
        parts,
        'dark',
        'mass',
        'density',
        True,
        [None, None],
        None,
        distance_limits,
        distance_bin_width,
        plot_file_name=True,
    )

    plot_property_v_distance(
        parts,
        'dark',
        'mass',
        'density*r',
        True,
        [None, None],
        None,
        distance_limits,
        distance_bin_width,
        plot_file_name=True,
    )

    return parts


def plot_mass_v_mass_fire3():
    '''
    .
    '''

    fire3_orig = {
        # m12b_m7e3_MHD_fire3_fireBH_Sep182021_hr_crdiffc690_sdp2e-4_gacc31_fa0.5
        'm12b_r7100': [2.1e10, 1.33e12],
        # m12f_m7e3_MHD_fire3_fireBH_Sep182021_hr_crdiffc690_sdp2e-4_gacc31_fa0.5
        'm12f_r7100': [1.4e10, 1.55e12],
        # no_mhd_no_bh
        'm12i_r7100': [1.8e10, 1.12e12],
        'm12q_r7100': [1.1e10, 1.52e12],
    }

    fire3_new = {
        'm12a_r57k': [6.4e10, 2.17e12],
        'm12d_r57k': [2.5e10, 1.51e12],
        'm12e_r57k': [6.3e10, 2.6e12],
        'm12g_r7100': [1.1e11, 2.73e12],
        'm12j_r7100': [2.1e10, 1.06e12],
        'm12k_r57k': [6.0e10, 2.38e12],
        'm12n_r7100': [4.6e10, 1.65e12],
        'm12u_r28k': [8.4e9, 7.06e11],
        'm12x_r3500': [2.82e9, 6.19e11],
    }

    # plot ----------
    _fig, subplot = ut.plot.make_figure(1)

    _axis_x_limits, _axis_y_limits = ut.plot.set_axes_scaling_limits(
        subplot,
        False,
        [0.5e12, 3.2e12],
        None,
        True,
        [2e9, 1.4e11],
    )

    subplot.set_xlabel('$M_{200m} [M_\\odot]$')
    subplot.set_ylabel('$M_{star}(< 20 kpc) [M_\\odot]$')

    subplot.xaxis.set_minor_locator(ticker.AutoMinorLocator(10))

    color_names = ut.plot.get_colors(9)

    for gal_i, gal_name in enumerate(fire3_orig):
        star_mass = fire3_orig[gal_name][0]
        halo_mass = fire3_orig[gal_name][1]
        label = gal_name.replace('_r7100', '')

        subplot.plot(
            halo_mass,
            star_mass,
            color=color_names[gal_i],
            alpha=0.7,
            label=label,
            marker='*',
            markersize=6,
        )
        # add name near point
        subplot.text(halo_mass * 1.02, star_mass * 1.02, label, fontsize=10)

    for gal_i, gal_name in enumerate(fire3_new):
        star_mass = fire3_new[gal_name][0]
        halo_mass = fire3_new[gal_name][1]
        label = gal_name.replace('_r7100', '')

        subplot.plot(
            halo_mass,
            star_mass,
            color=color_names[gal_i],
            alpha=0.7,
            label=label,
            marker='o',
            markersize=6,
        )
        subplot.text(halo_mass * 1.02, star_mass * 1.02, label, fontsize=10)

    # ut.plot.make_legends(subplot)
    ut.plot.parse_output()
