'''
Utility functions for catalogs of [sub]halos or galaxies.

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

import numpy as np

from . import array, coordinate, constant, io

MASS_RATIO_200M_LL168 = np.log10(1.2)  # M_200m / M_fof(ll = 0.168)


# --------------------------------------------------------------------------------------------------
# print properties of object in catalog
# --------------------------------------------------------------------------------------------------
def print_properties(cat, index):
    '''
    Print (array) properties of object.

    Parameters
    ----------
    cat : dict
        catalog of [sub]halos / galaxies
    index : int
        object index
    '''
    for k in sorted(cat.keys()):
        print('{:24} {}'.format(k, cat[k][index]))


# --------------------------------------------------------------------------------------------------
# properties of simulation
# --------------------------------------------------------------------------------------------------
def get_is_baryonic_from_directory(simulation_directory, os):
    '''
    Check if the simulation contains baryons.

    Parameters
    ----------
    simulation_directory : str
        directory of simulation
    os : class

    Returns
    -------
    host_number : int
        number of primary hosts in simulation
    '''
    if simulation_directory == './':
        current_directory = os.getcwd()
    else:
        current_directory = simulation_directory

    baryonic = True
    if '_dm' in current_directory:
        baryonic = False

    return baryonic


# --------------------------------------------------------------------------------------------------
# properties of primary host[s]
# --------------------------------------------------------------------------------------------------
def get_host_name(host_index=0, end='.'):
    '''
    Get name of primary host in catalog.

    Parameters
    ----------
    host_index : int
        index/rank of host
    end : str
        append to end of host_name

    Returns
    -------
    host_name : str
        name of host
    '''
    assert host_index >= 0

    if host_index == 0:
        host_name = 'host'
    else:
        host_name = f'host{host_index + 1}'

    if end:
        host_name += end

    return host_name


def get_host_number_from_directory(host_number, simulation_directory, os):
    '''
    Check if 'elvis' is in directory name of simulation.
    If so, return host_number = 2.

    Parameters
    ----------
    host_number : int
        number of primary hosts in simulation
    simulation_directory : str
        directory of simulation
    os : class

    Returns
    -------
    host_number : int
        number of primary hosts in simulation
    '''
    if simulation_directory == './':
        current_directory = os.getcwd()
    elif simulation_directory.startswith('../'):
        current_directory = os.getcwd().rsplit('/', simulation_directory.count('../'))[0] + '/'
    else:
        current_directory = simulation_directory

    if host_number is True:
        host_number = 1

    if 'elvis' in current_directory and host_number < 2:
        host_number = 2
        print(f'\n* found "elvis" in simulation directory name, so assuming {host_number} hosts')

    return host_number


# --------------------------------------------------------------------------------------------------
# limits
# --------------------------------------------------------------------------------------------------
def get_sfr_limits(sfr_name='ssfr'):
    '''
    Get limits for star formation rate.

    Parameters
    ----------
    sfr_name : str
        star formation rate kind

    Returns
    -------
    sfr_limits : list
        min and max limits of SFR
    '''
    if 'ssfr' in sfr_name:
        sfr_limits = [-1e10, -7.0]
    elif sfr_name == 'dn4k':
        sfr_limits = [1.0, 2.2]
    elif sfr_name == 'h-alpha.flux':
        sfr_limits = [1e-10, 10]
    elif sfr_name == 'h-alpha.ew':
        sfr_limits = [1e-10, 3000]
    elif sfr_name in ['am-qu.spec', 'am-qu.dn4k', 'am-qu.nsa']:
        sfr_limits = [0, 1.01]
    elif sfr_name == 'g-r':
        sfr_limits = [0, 1.5]
    elif sfr_name == 'am-qu.color':
        sfr_limits = [0, 2.1]
    elif sfr_name == 'metal':
        sfr_limits = [0, 0.051]
    else:
        raise ValueError(f'not recognize sfr_name = {sfr_name}')

    return np.array(sfr_limits)


def get_sfr_bimodal_limits(sfr_name='ssfr'):
    '''
    Get limits of star formation rate for quiescent and active galaxies in dictionary.

    Parameters
    ----------
    sfr_name : str
        star formation rate kind

    Returns
    -------
    dict : low and high limits of SFR
    '''
    if 'ssfr' in sfr_name:
        sfr_break = -11
        lo_limits = [-np.inf, sfr_break]
        hi_limits = [sfr_break, -1]
    elif sfr_name == 'dn4k':
        sfr_break = 1.6
        lo_limits = [sfr_break, np.inf]
        hi_limits = [1e-10, sfr_break]
    elif sfr_name == 'h-alpha.flux':
        sfr_break = 0.8
        lo_limits = [1e-10, sfr_break]
        hi_limits = [sfr_break, np.inf]
    elif sfr_name == 'h-alpha.ew':
        sfr_break = 2
        lo_limits = [1e-10, sfr_break]
        hi_limits = [sfr_break, np.inf]
    elif sfr_name in ['am-qu.spec', 'am-qu.dn4k', 'am-qu.nsa']:
        sfr_break = 0.5
        lo_limits = [sfr_break, 1.01]
        hi_limits = [0, sfr_break]
    elif sfr_name == 'g-r':
        sfr_break = 0.76
        lo_limits = [sfr_break, np.inf]
        hi_limits = [-np.inf, sfr_break]
    elif sfr_name == 'am-qu.color':
        sfr_break = 1.5
        lo_limits = [1, 1.1]
        hi_limits = [2, 2.1]
    elif sfr_name == 'metal':
        sfr_break = 0.023
        lo_limits = [0, sfr_break]
        hi_limits = [sfr_break, np.inf]
    else:
        raise ValueError(f'not recognize sfr kind = {sfr_name}')

    return {
        'lo': lo_limits,
        'hi': hi_limits,
        'break': sfr_break,
        'sfrlo': lo_limits,
        'sfrhi': hi_limits,
    }


# --------------------------------------------------------------------------------------------------
# indices of sub-sample
# --------------------------------------------------------------------------------------------------
def assign_id_to_index(cat, id_name='id', id_min=0, dtype=None):
    '''
    Assign to catalog dictionary an array that points from object id to index in list.
    Safely set null values to -length of array.
    Do not assign pointers for ids below id_min.

    Parameters
    ----------
    cat : dict
        catalog dictionary of objects
    id_name : str
        key name for object id
    id_min : int
        minimum id in catalog
    dtype
        data type for index array
    '''
    Say = io.SayClass(assign_id_to_index)

    if id_name in cat:
        # ensure no duplicate ids
        masks = cat[id_name] >= id_min
        total_number = np.sum(masks)
        unique_number = np.unique(cat[id_name][masks]).size
        if total_number != unique_number:
            Say.say(f'! warning, {total_number - unique_number} ids are not unique')

        dtype = array.parse_int_dtype(cat[id_name].max() + 1, dtype)

        cat[id_name + '.to.index'] = array.get_array_null(cat[id_name].max() + 1, dtype=dtype)
        cat[id_name + '.to.index'][cat[id_name][masks]] = array.get_arange(
            cat[id_name], dtype=dtype
        )[masks]
    else:
        Say.say(f'catalog does not contain id key = {id_name}')


def get_indices_catalog(cat, property_dict={}, indices=None):
    '''
    Get index[s] in catalog, selecting on defined limits in input dictionary.
    Input limits: lower limit is inclusive (>=), upper limit is exclusive (<).

    Parameters
    ----------
    cat : dict
        catalog of objects
    property_dict : dict
        dictionary with property names as keys and limits as values
        example: property_dict = {'mass': [1e9, 1e10], 'radius': [0, 100]}
    indices : array
        index[s] also to select on

    Returns
    -------
    cat_indices : array
        indices in catalog
    '''
    Say = io.SayClass(get_indices_catalog)

    cat_indices = indices
    for property_name in property_dict:
        try:
            property_values = cat.prop(property_name)
        except KeyError:
            if property_name not in cat:
                Say.say(f'! {property_name} is not in catalog, cannot use for sub-sampling')
                continue
            else:
                property_values = cat[property_name]

        if property_dict[property_name] is None:
            continue
        elif np.isscalar(property_dict[property_name]):
            limits = [property_dict[property_name], np.inf]
        elif len(property_dict[property_name]) == 2:
            limits = property_dict[property_name]
        else:
            Say.say(
                'property = {} has limits = {} with length != 2, cannot use to get indices'.format(
                    property_name, property_dict[property_name]
                )
            )
            continue

        cat_indices = array.get_indices(property_values, limits, cat_indices)

    return cat_indices


def get_indices_subhalo(
    sub,
    gal_mass_name,
    gal_mass_limits=None,
    hal_mass_limits=None,
    ilk='',
    disrupt_mf=0,
    indices=None,
):
    '''
    Get index[s] in subhalo catalog selecting on defined limits.

    Parameters
    ----------
    sub : dict
        catalog of subhalos at snapshot
    gal_mass_name : str
        mass name for galaxy/subhalo
    gal_mass_limits : list
        min and max limits of galaxy/subhalo mass
    hal_mass_limits : list
        min and max limits of host halo mass
    ilk : str
        subhalo ilk
    disrupt_mf : float
        subhalo disruption mass fraction
    indices : array
        index[s] also to select on

    Returns
    -------
    indices : array
        indices in catalog
    '''
    if gal_mass_name and gal_mass_limits is not None and gal_mass_limits != []:
        indices = array.get_indices(sub[gal_mass_name], gal_mass_limits, indices)
    if hal_mass_limits is not None and hal_mass_limits != []:
        indices = array.get_indices(sub['halo.mass'], hal_mass_limits, indices)
    if disrupt_mf > 0:
        indices = array.get_indices(sub['mass.frac.min'], [disrupt_mf, np.inf], indices)
    if 'central' in ilk or 'satellite' in ilk:
        indices = get_indices_ilk(sub, ilk, indices)

    return indices


def get_indices_galaxy(
    gal,
    gal_mass_name,
    gal_mass_limits=None,
    hal_mass_limits=None,
    ilk='',
    redshift_limits=None,
    ra_limits=None,
    sfr_name='',
    sfr_limits=None,
    distance_halo_limits=None,
    indices=None,
):
    '''
    Get index[s] in galaxy catalog selecting on defined limits.

    Parameters
    ----------
    gal : dict
        galaxy catalog
    gal_mass_name : str
        galaxy mass kind
    gal_mass_limits : list
        min and max limits for gal_mass_name
    hal_mass_limits : list
        min and max limits for halo mass
    ilk : str
        galaxy ilk
    redshift_limits : list
        min and max limits for redshift
    ra_limits : list
        min and max limits for right ascension
    sfr_name : str
        SFR kind
    sfr_limits : list
        min and max limits for SFR
    distance_halo_limits : list
        min and max limits for distance / R_halo
    indices : array
        index[s] also to select on

    Returns
    -------
    indices : array
        indices in catalog
    '''
    if gal_mass_name and gal_mass_limits is not None and gal_mass_limits != []:
        indices = array.get_indices(gal[gal_mass_name], gal_mass_limits, indices)
    if hal_mass_limits is not None and hal_mass_limits != []:
        indices = array.get_indices(gal['halo.mass'], hal_mass_limits, indices)
    if ilk is not None and ilk != '':
        indices = get_indices_ilk(gal, ilk, indices)
    if redshift_limits is not None and redshift_limits != []:
        indices = array.get_indices(gal['redshift'], redshift_limits, indices)
    if sfr_name and sfr_limits is not None and sfr_limits != []:
        indices = array.get_indices(gal[sfr_name], sfr_limits, indices)
    if ra_limits is not None and ra_limits != []:
        indices = array.get_indices(gal['position'][:, 0], ra_limits, indices)
    if distance_halo_limits is not None and distance_halo_limits != []:
        indices = array.get_indices(gal['central.distance/Rhost'], distance_halo_limits, indices)

    return indices


def get_indices_ilk(cat, ilk='all', indices=None, get_masks=False):
    '''
    Get index[s] in general catalog of those of ilk type.

    Parameters
    ----------
    cat : dict
        catalog of galaxies/subhalos at snapshot
    ilk : str
        subhalo ilk: sat, sat+ejected, cen, all
    indices : array
        index[s] also to select on
    get_masks : bool
        whether to get selection indices of input indices

    Returns
    -------
    indices : array
        indices in catalog
    '''
    sat_prob_dict = {
        'central': [0.0, 0.5],
        'central.clean': [0.0, 1e-5],
        'central.clean.neig': [0.0, 1e-5],
        'satellite': [0.5, 1.01],
        'satellite.clean': [0.9, 1.01],
    }

    ilk_dict = {
        'central': [1, 2.01],
        'central.clean': 1,
        'satellite': [-4, 0.01],
        'satellite.clean': [-2, 0.01],
        'satellite.elvis': [-2, -0.1],
    }

    mass_rank_dict = {'central': 1, 'satellite': 2}

    if ilk == 'all':
        return indices

    elif ilk in sat_prob_dict or ilk in ilk_dict or ilk in mass_rank_dict:
        if 'satellite.prob' in cat:
            indices = array.get_indices(
                cat['satellite.prob'], sat_prob_dict[ilk], indices, get_masks=get_masks
            )
            if ilk == 'central.clean.neig':
                k = 'nearest.distance/Rneig'
                if k in cat:
                    indices = array.get_indices(cat[k], [4, np.inf], indices)
                else:
                    raise ValueError(f'request {ilk}, but {k} not in catalog')
        elif 'mass.rank' in cat:
            indices = array.get_indices(
                cat['mass.rank'], mass_rank_dict[ilk], indices, get_masks=get_masks
            )
        elif 'ilk' in cat:
            indices = array.get_indices(cat['ilk'], ilk_dict[ilk], indices, get_masks=get_masks)

    else:
        raise ValueError(f'not recognize ilk = {ilk}')

    return indices


def get_indices_sfr(cat, bimod_kind='lo', sfr_names='ssfr', indices=None, get_masks=False):
    '''
    Get index[s] in general catalog of those in SFR bimodality region.
    If multiple SFR kinds, get overlapping indices in both sets for quiescent, in either set for
    active.

    Parameters
    ----------
    cat : dict
        catalog of galaxies/subhalos at snapshot
    bimod_kind : str
        SFR bimodality region: lo, hi
    sfr_names : str (use spaces to cut on several)
        SFR kind[s]: ssfr, dn4k, g-r
    indices : array
        index[s] also to select on
    get_masks : bool
        whether to get selection indices of input indices

    Returns
    -------
    indices : array
        indices in catalog
    '''
    sfr_names_split = sfr_names.split()

    if len(sfr_names_split) == 1:
        bimod_limits = get_sfr_bimodal_limits(sfr_names)
        indices = array.get_indices(
            cat[sfr_names], bimod_limits[bimod_kind], indices, get_masks=get_masks
        )
    elif len(sfr_names_split) == 2:
        indices = []
        for sfr_name in sfr_names_split:
            bimod_limits = get_sfr_bimodal_limits(sfr_name)
            indices.append(array.get_indices(cat[sfr_name], bimod_limits[bimod_kind], indices))
        if 'lo' in bimod_kind:
            indices = np.intersect1d(indices[0], indices[1])
        elif 'hi' in bimod_kind:
            indices = np.union1d(indices[0], indices[1])
    else:
        raise ValueError('! not yet support > 2 SFR kinds')

    return indices


def get_indices_in_halo(sub, indices, mass_name='mass.peak', mass_limits=[1, np.inf], ilk='satellite'):
    '''
    Get index[s] of subhalos in mass range in halo (can include self).

    Parameters
    ----------
    sub : dict
        catalog of subhalos at snapshot
    indices : array
        subhalo index[s]
    mass_name : str
    mass_limits : list
        min and max limits for mass_name
    ilk : str
        subhalo ilk: 'satellite', 'all'

    Returns
    -------
    indices : array
        indices in catalog
    '''
    cen_i = sub['central.index'][indices]
    indices = array.get_indices(sub['central.index'], cen_i)
    indices = array.get_indices(sub[mass_name], mass_limits, indices)
    if ilk == 'satellite':
        indices = indices[indices != cen_i]

    return indices


# --------------------------------------------------------------------------------------------------
# velocity / redshift
# --------------------------------------------------------------------------------------------------
def get_velocity_differences(
    cat_1, cat_2, indices_1, indices_2, dimension_indices=[0, 1, 2], total_velocity=False
):
    '''
    Get relative velocity[s] [km/s] of object[s] 1 wrt 2.

    Parameters
    ----------
    cat_1 : dict
        catalog of [sub]halos at snapshot
    cat_2 : dict
        catalog of [sub]halos at snapshot
    indices_1 : array
        index[s] in cat_1
    indices_2 : array
        index[s] in cat_2
    dimension_indices : list
        indices of spatial dimensions to use
    total_velocity : bool
        whether to compute total/scalar velocity

    Returns
    -------
    velocity_difs : array
        velocity[s] (total/scalar or 3-D)
    '''
    if np.isscalar(indices_1):
        indices_1 = array.arrayize(indices_1, bit_number=32)
    if np.isscalar(indices_2):
        indices_2 = array.arrayize(indices_2, bit_number=32)

    velocity_difs = coordinate.get_velocity_differences(
        cat_1['velocity'][indices_1][:, dimension_indices],
        cat_1['velocity'][indices_2][:, dimension_indices],
        cat_1['position'][indices_1][:, dimension_indices],
        cat_2['position'][indices_2][:, dimension_indices],
        cat_1.info['box.length'],
        cat_1.snapshot['scalefactor'],
        cat_1.snapshot['time.hubble'],
        total_velocity,
    )

    return velocity_difs


def get_redshift_in_simulation(cat, indices=None, dimension_i=2):
    '''
    Get redshift of object[s] in simulation given its position and velocity.
    Redshift normalization is snapshot redshift at position[dim_i] = 0.
    Differential redshifts are valid, at least locally.

    Parameters
    ----------
    cat : dict
        catalog of [sub]halos at snapshot
    indices : array
        index[s] of [sub]halos
    dimension_i : int
        which dimension to compute redshift from

    Returns
    -------
    array : redshift[s]
    '''
    if indices is None:
        indices = array.get_arange(cat['position'][:, dimension_i])

    vels = cat['velocity'][indices][:, dimension_i]
    # add hubble flow
    vels += (
        (
            cat['position'][indices][:, dimension_i]
            * cat.snapshot['scalefactor']
            / cat.snapshot['time.hubble']
        )
        * constant.km_per_kpc
        / constant.sec_per_Gyr
    )

    return coordinate.convert_velocity_redshift('velocity', vels) + cat.snapshot['redshift']


# --------------------------------------------------------------------------------------------------
# [sub]halo history
# --------------------------------------------------------------------------------------------------
def get_tree_direction_info(ti_start=None, ti_end=None, direction_kind=''):
    '''
    Get snapshot index step (+1 or -1) and catalog dictionary key corresponding to parent / child.

    Parameters
    ----------
    ti_start : int
        starting snapshot index (forward or backward)
    ti_end : int
        ending snapshot index (forward or backward)
    direction_kind : str
        'parent', 'child'

    Returns
    -------
    ti_step : int
        1 or -1
    family_key : str
        'parent.index', 'child.index'
    '''
    if direction_kind:
        if direction_kind == 'parent':
            ti_step = 1
            family_key = 'parent.index'
        elif direction_kind == 'child':
            ti_step = -1
            family_key = 'child.index'
        else:
            raise ValueError(f'not recognize direction kind = {direction_kind}')
    else:
        if ti_end < 0:
            raise ValueError(f't_i end = {ti_end} is out of bounds')
        elif ti_end == ti_start:
            raise ValueError('t_i end = t_i start')
        if ti_end > ti_start:
            ti_step = 1
            family_key = 'parent.index'
        elif ti_end < ti_start:
            ti_step = -1
            family_key = 'child.index'

    return ti_step, family_key


def get_indices_tree(cats, ti_start, ti_end, indices=None, get_masks=False):
    '''
    Get parent / child index[s] at ti_end corresponding to input indices.
    Assign negative value to [sub]halo if cannot track all the way to end.

    Parameters
    ----------
    cats : list
        catalog of [sub]halos across snapshots
    ti_start : int
        starting snapshot index (forward or backward)
    ti_end : int
        ending snapshot index (forward or backward)
    indices : array
        [sub]halo index[s]
    get_masks : bool
        whether to return selection indices of input indices

    Returns
    -------
    array : indices of parent / child
    '''
    if ti_start == ti_end:
        return indices
    elif ti_end >= len(cats):
        raise ValueError(
            'ti.end = {} is not within {} snapshot limit = {}'.format(
                ti_end, cats.info['catalog.kind'], len(cats) - 1
            )
        )

    ti_step, tree_kind = get_tree_direction_info(ti_start, ti_end)
    if indices is None:
        get_indices_tree = array.get_arange(cats[ti_start][tree_kind])
    else:
        get_indices_tree = array.arrayize(indices, bit_number=32)

    for ti in range(ti_start, ti_end, ti_step):
        iis = array.get_indices(get_indices_tree, [0, np.inf])
        get_indices_tree[iis] = cats[ti][tree_kind][get_indices_tree[iis]]
    iis = array.get_indices(get_indices_tree, [0, np.inf])
    indices_end = (
        np.zeros(get_indices_tree.size, get_indices_tree.dtype) - 1 - cats[ti_end][tree_kind].size
    )
    indices_end[iis] = get_indices_tree[iis]

    if get_masks:
        return array.scalarize(indices_end), array.scalarize(iis)
    else:
        return array.scalarize(indices_end)


def is_in_same_halo(subs, hals, child_ti, child_si, par_ti, par_si):
    '''
    Get 1 or 0 if subhalo child's parent is in subhalo child's halo's parent.

    Parameters
    ----------
    subs : list
        catalog of subhalos across snapshots
    subs : list
        catalog of halos across snapshots
    child_ti : int
        subhalo child snapshot index
    child_si : int
        subhalo child index
    par_ti : int
        subhalo parent snapshot index
    par_si : int
        subhalo parent index

    Returns
    -------
    1 or 0 : 1 = yes is in samehalo, 0 = no is not in same halo
    '''
    if child_ti < 0 or child_si <= 0 or par_ti < 0 or par_si <= 0:
        return 0

    hi_par = subs[par_ti]['halo.index'][par_si]
    hi = subs[child_ti]['halo.index'][child_si]
    if hi_par > 0 and hi > 0:
        for ti in range(child_ti, par_ti):
            hi = hals[ti]['parent.index'][hi]
            if hi <= 0:
                return 0
        if hi_par == hi:
            return 1

    return 0


def is_orphan(hals, ti_now, ti_max, hal_index, mass_name='mass.fof', subs=None):
    '''
    Get 1 or 0 if halo was ever orphan/ejected while above mass cut.

    Parameters
    ----------
    hals : list
        catalog of halos across snapshots
    ti_now : int
        current snapshot hal_index
    ti_now : int
        maximum snapshot hal_index
    hal_index : int
        halo hal_index
    mass_name : str
        halo mass name
    subs : list
        catalog of subhalos across snapshots (for sanity check, not seem to matter much)

    Returns
    -------
    1 or 0 : int
        1 = yes is orphan, 0 = no is not orphan
    '''
    # cannot determine if too few particles
    mass_min_res = np.log10(80 * hals.info['particle.mass'])

    # 'new' halo if grew by > 50%
    mass_min = max(hals[ti_now][mass_name][hal_index] - 0.3, mass_min_res)
    par_ti, par_hi = ti_now, hal_index
    while par_ti < ti_max and par_hi > 0:
        if hals[par_ti][mass_name][par_hi] > mass_min:
            if hals[par_ti]['parent.index'][par_hi] <= 0:
                if subs is None:
                    return 1
                elif hals[par_ti]['central.index'][par_hi] <= 0:
                    return 1
                elif subs[par_ti]['parent.index'][hals[par_ti]['central.index'][par_hi]] > 0:
                    return 1
                else:
                    return 0
        par_ti, par_hi = par_ti + 1, hals[par_ti]['parent.index'][par_hi]

    return 0


def print_evolution(cats, ti_now, cat_index, ti_end=None, property_name='mass.peak'):
    '''
    Print properties of [sub]halo across snapshots.
    By default, go back in time, unles ti_now > ti_end.

    Parameters
    ----------
    cats : list
        catalog of [sub]halos across snapshots
    ti_now : int
        current snapshot cat_index
    cat_index : int
        index of [sub]halo
    ti_end : int
        ending snapshot index
    property_name : str
        property to print
    '''
    Say = io.SayClass(print_evolution)

    if ti_end is None:
        ti_end = len(cats) - 1
    elif ti_end >= len(cats):
        Say.say(
            '! ti_end = {} is not within {} snapshot limits, setting to {}'.format(
                ti_end, cats.info['catalog.kind'], len(cats) - 1
            )
        )
        ti_end = len(cats) - 1

    ti_step, tree_kind = get_tree_direction_info(ti_now, ti_end)
    if ti_now > ti_end:
        ti_end -= 1
    elif ti_now < ti_end:
        ti_end += 1

    ti = ti_now
    for ti in range(ti_now, ti_end, ti_step):
        if cats.info['catalog.kind'] == 'subhalo':
            Say.say(
                't_i {:2d} | c_i {:.6d} | ilk {:.2d} | {} {:6.3f}'.format(
                    ti,
                    cat_index,
                    cats[ti]['ilk'][cat_index],
                    property_name,
                    cats[ti][property_name][cat_index],
                )
            )
        elif cats.info['catalog.kind'] == 'halo':
            Say.say(
                't_i={:2d} z={:.4f} | c_i {:6d} | {:7.3f} {:7.3f} {:7.3f} | {} {:6.3f}'.format(
                    ti,
                    cats[ti].snapshot['redshift'],
                    cat_index,
                    cats[ti]['position'][cat_index, 0],
                    cats[ti]['position'][cat_index, 1],
                    cats[ti]['position'][cat_index, 2],
                    property_name,
                    cats[ti][property_name][cat_index],
                )
            )
        cat_index = cats[ti][tree_kind][cat_index]
        if cat_index < 0:
            break


def print_extrema_of_properties(cats):
    '''
    Print minimum and maximum value of each property in the entire catalog across snapshots.

    Parameters
    ----------
    cats : dict or list
        catalog[s] of [sub]halos at snapshot or across snapshots
    '''
    if isinstance(cats, dict):
        cats = [cats]
    for k in cats[0]:
        prop_min, prop_max = np.inf, -np.inf
        for cat in cats:
            if cat[k].size:
                if cat[k].min() < prop_min:
                    prop_min = cat[k].min()
                if cat[k].max() > prop_max:
                    prop_max = cat[k].max()
        print('# {} {:.5f}, {:.5f}'.format(k, prop_min, prop_max))


# --------------------------------------------------------------------------------------------------
# neighbors
# --------------------------------------------------------------------------------------------------
def get_neighbors(
    hal,
    mass_name='mass',
    hal_mass_limits=[1e12, 2e12],
    hal_indices=None,
    neig_distance_limits=[1, 10],
    neig_distance_scale='Rself',
    neig_mass_frac_limits=[0.25, np.inf],
    neig_mass_limits=None,
    neig_number_max=500,
    print_diagnostics=True,
):
    '''
    Find neighbors within input distance limits (in terms of physical distance or d/R_self) that
    are within given mass_name limits (can be scaled to mass_name of self).
    Return dictionary of neighbor properties.

    Parameters
    ----------
    hal : dict
        catalog of halos
    mass_name : str
        mass name, to select both centers and neighors
    hal_mass_limits : list
        min and max limits of mass_name to select centers
    hal_indices : int or list
        index[s] of center[s]
    neig_distance_limits : list
        min and max distances of neighbors [kpc physical or d/R_self]
    neig_distance_scale : str
        distance kind to select neighbors:
            '' = use physical distance
            'Rself' = use distance/Rself
    neig_mass_frac_limits : list
        min and max mass_name (relative to central) of neighbors
    neig_mass_limits : list
        min and max mass_name of neighbors
    neig_number_max : int
        maximum number of neighbors per center to search for

    Returns
    -------
    neig : dict
        neighbor properties
    '''
    halo_radius_kind = 'radius'

    neig_distance_limits = np.array(neig_distance_limits)
    neig_mass_frac_limits = np.array(neig_mass_frac_limits)

    if hal_mass_limits is not None and len(hal_mass_limits) > 0:
        hal_indices = array.get_indices(hal[mass_name], hal_mass_limits, hal_indices)

    hal_indices = np.asarray(hal_indices)

    neig_distance_max = neig_distance_limits.max()
    if 'self' in neig_distance_scale:
        neig_distance_max *= hal[halo_radius_kind][hal_indices].max()
    if 'neig' in neig_distance_scale:
        raise ValueError('cannot scale to Rneig (yet)')

    neig_mass_limits_all = [-np.inf, np.inf]
    if neig_mass_frac_limits is not None and len(neig_mass_frac_limits) > 0:
        neig_mass_limits_all = np.clip(
            neig_mass_limits_all,
            min(neig_mass_frac_limits) * np.min(hal[mass_name][hal_indices]),
            max(neig_mass_frac_limits) * np.max(hal[mass_name][hal_indices]),
        )
    if neig_mass_limits is not None and len(neig_mass_limits) > 0:
        neig_mass_limits_all = np.clip(
            neig_mass_limits_all, min(neig_mass_limits), max(neig_mass_limits)
        )

    neig_indices = array.get_indices(hal[mass_name], neig_mass_limits_all)

    # get all neighbors around all centers that are withing the overall (maximal)
    # mass and distance limits
    a = hal.snapshot['scalefactor']
    neig_distancess, neig_indicess = coordinate.get_neighbors(
        hal['position'][hal_indices] * a,
        hal['position'][neig_indices] * a,
        neig_distance_max,
        neig_number_max,
        hal.info['box.length'],
        neig_indices,
        return_lists=True,
        verbose=print_diagnostics,
    )

    neig = {}
    neig['self.index'] = hal_indices
    neig['index'] = [[] for _ in range(hal_indices.size)]
    neig['distance'] = [[] for _ in range(hal_indices.size)]
    neig['distance/Rself'] = [[] for _ in range(hal_indices.size)]
    neig['distance/Rneig'] = [[] for _ in range(hal_indices.size)]
    neig[mass_name] = [[] for _ in range(hal_indices.size)]

    # loop over all centers to apply center-by-center cuts on neighbor mass and distance
    for hii, hi in enumerate(hal_indices):
        if len(neig_indicess[hii]) > 0:
            halo_radius_i = hal[halo_radius_kind][hi]

            neig_mass_limits_i = neig_mass_frac_limits * hal[mass_name][hi]
            niis = array.get_indices(hal[mass_name][neig_indicess[hii]], neig_mass_limits_i)

            if len(niis) > 0:
                if 'self' in neig_distance_scale:
                    neig_distance_limits_i = neig_distance_limits * halo_radius_i
                else:
                    neig_distance_limits_i = neig_distance_limits
                niis = array.get_indices(neig_distancess[hii], neig_distance_limits_i, niis)

                neig['index'][hii] = neig_indicess[hii][niis]
                neig['distance'][hii] = neig_distancess[hii][niis]
                neig['distance/Rself'][hii] = neig_distancess[hii][niis] / halo_radius_i
                neig['distance/Rneig'][hii] = (
                    neig_distancess[hii][niis] / hal[halo_radius_kind][neig_indicess[hii][niis]]
                )
                neig[mass_name][hii] = hal[mass_name][neig_indicess[hii][niis]]

    return neig


class NearestNeighborClass(io.SayClass):
    '''
    Find the single nearest neighbor (minimum in distance, d/R_neig, or d/Rself) that is more
    massive than self (or above input fraction of self's mass) and store its properties.
    '''

    def __init__(self, nearest=None):
        '''
        Parameters
        ----------
        nearest : dict
            previous nearest neighbor dict
        '''
        self.nearest = nearest
        self.mass_name = None

    def assign_to_self(
        self,
        hal,
        mass_name='mass',
        mass_limits=[1, np.inf],
        neig_mass_frac_limits=[1.0, np.inf],
        neig_mass_limits=[1, np.inf],
        neig_distance_max=30000,
        neig_distance_scale='Rneig',
        neig_number_max=300,
        hal_indices=None,
        print_diagnostics=True,
    ):
        '''
        Compute and store dictionary of nearest neighbor's properties:
            index, distance [physical], distance/R_halo(neig), distance/R_halo(self), mass

        Parameters
        ----------
        hal : dict
            catalog of halos
        mass_name : str
            mass name
        mass_limits : list
            min and max limits for mass_name
        neig_mass_frac_limits : float
            min and max mass_name (wrt self) to keep neighbors
        neig_mass_limits : list
            min and max limits for neighbor mass_name
        neig_distance_max : float
            neighbor maximum distance [kpc physical]
        neig_distance_scale : str
            distance kind to use to compute nearest neighbor:
                'physical' or '' = use physical distance
                'Rneig' = use distance/Rneig
                'Rself' = use distance/Rself
        neig_number_max : int
            maximum number of neighbors per center
        hal_indices : array
            prior indices of centers
        '''
        if mass_limits is not None and len(mass_limits) > 0:
            hal_indices = array.get_indices(hal[mass_name], mass_limits, hal_indices)

        neig_mass_limits_use = [-np.inf, np.inf]
        if neig_mass_frac_limits is not None and len(neig_mass_frac_limits) > 0:
            neig_mass_limits_use = np.clip(
                neig_mass_limits_use,
                min(neig_mass_frac_limits) * min(mass_limits),
                max(neig_mass_frac_limits) * max(mass_limits),
            )
        if neig_mass_limits is not None and len(neig_mass_limits) > 0:
            neig_mass_limits_use = np.clip(
                neig_mass_limits_use, min(neig_mass_limits), max(neig_mass_limits)
            )

        neig_indices = array.get_indices(hal[mass_name], neig_mass_limits_use)

        neig = {}

        a = hal.snapshot['scalefactor']
        neig['distances'], neig['indices'] = coordinate.get_neighbors(
            hal['position'][hal_indices] * a,
            hal['position'][neig_indices] * a,
            neig_distance_max,
            neig_number_max,
            hal.info['box.length'],
            neig_indices,
            return_lists=True,
            verbose=print_diagnostics,
        )

        nearest = {
            'self.index': hal_indices,
            'index': array.get_array_null(hal_indices.size),
            'distance': np.zeros(hal_indices.size, np.float32) + np.array(np.inf, np.float32),
            'distance/Rneig': np.zeros(hal_indices.size, np.float32) + np.array(np.inf, np.float32),
            'distance/Rself': np.zeros(hal_indices.size, np.float32) + np.array(np.inf, np.float32),
            mass_name: np.zeros(hal_indices.size, np.float32),
        }

        for hii, hi in enumerate(hal_indices):
            # keep only neighbors more massive than self
            neig_masses = hal[mass_name][neig['indices'][hii]]
            masks = (neig_masses >= neig_mass_frac_limits[0] * hal[mass_name][hi]) * (
                neig_masses < neig_mass_frac_limits[1] * hal[mass_name][hi]
            )

            if len(masks) > 0 and masks.max():
                neig_indices = neig['indices'][hii][masks]
                distances_phys = neig['distances'][hii][masks]  # distance to center of neighbor
                distances_neig = distances_phys / hal['radius'][neig_indices]
                distances_self = distances_phys / hal['radius'][hi]

                if 'neig' in neig_distance_scale:
                    near_i = np.nanargmin(distances_neig)
                elif 'self' in neig_distance_scale:
                    near_i = np.nanargmin(distances_self)
                else:
                    near_i = np.nanargmin(distances_phys)

                nearest['index'][hii] = neig_indices[near_i]
                nearest['distance'][hii] = distances_phys[near_i]
                nearest['distance/Rneig'][hii] = distances_neig[near_i]
                nearest['distance/Rself'][hii] = distances_self[near_i]
                nearest[mass_name][hii] = hal[mass_name][neig_indices[near_i]]

        nearest_number = np.sum(nearest['index'] >= 0)
        self.say(
            '{} of {} ({:.1f}%) have neighboring massive halo'.format(
                nearest_number, hal_indices.size, 100 * nearest_number / hal_indices.size
            )
        )
        self.nearest = nearest
        self.mass_name = mass_name

    def assign_to_catalog(self, hal):
        '''
        Assign nearest neighbor properties to halo catalog.

        Parameters
        ----------
        hal : dict : halo catalog at snapshot
        '''
        base_name = 'nearest.'
        properties = list(self.nearest)
        properties.remove('self.index')
        for prop_name in properties:
            hal[base_name + prop_name] = (
                np.zeros(hal[self.mass_name].size, self.nearest[prop_name].dtype) - 1
            )
            hal[base_name + prop_name][self.nearest['self.index']] = self.nearest[prop_name]


NearestNeighbor = NearestNeighborClass()


def get_catalog_neighbor(
    cat,
    gal_mass_name='star.mass',
    gal_mass_limits=[9.7, np.inf],
    hal_mass_limits=None,
    ilk='',
    neig_gmass_name='star.mass',
    neig_gmass_limits=[9.7, np.inf],
    neig_hmass_limits=None,
    neig_ilk='',
    disrupt_mf=0,
    neig_number_max=2000,
    neig_distance_max=0.20,
    distance_space='real',
    neig_velocity_dif_maxs=None,
    center_indices=None,
    neig_indices=None,
):
    '''
    Get dictionary of counts, distances [kpc physical], and indices of up to neig_number_max
    neighbors within neig_distance_max.

    *** This function needs cleaning. Probably best not to use until then.

    Parameters
    ----------
    cat : dict
        catalog of [sub]halos at snapshot
    gal_mass_name : str
        galaxy mass name
    gal_mass_limits : list
        min and max limits for galaxy mass
    hal_mass_limits : list
        min and max lmits for halo mass
    ilk : str
        subhalo ilk
    neig_gmass_name : str
        neighbor mass name
    neig_gmass_limits : list
        min and max limits for neighbor galaxy mass
    neig_hmass_limits : list
        min and max limits for neighbor halo mass
    neig_ilk : str
        neighbor subhalo ilk
    disrupt_mf : float
        disruption mass fraction for both (ignore for neighbor if just cut on its halo mass)
    neig_number_max : int
        maximum number of neighbors per center
    neig_distance_max : float
        neighbor maximum distance [kpc physical]
    distance_space: str
        real, red, proj
    neig_velocity_dif_maxs : float
        neighbor line-of-sight velocity difference maximum[s] [km/s] (if distance_space = proj)
    center_indices : array
        center index[s] to pre-select
    neig_indices : array
        neighbor index[s] to pre-select

    Returns
    -------
    neig : dict
        neighbor properties
    '''
    neig = {
        'info': {
            'mass.name': gal_mass_name,
            'mass.limits': gal_mass_limits,
            'neig.mass.name': neig_gmass_name,
            'neig.mass.limits': neig_gmass_limits,
            'distance.max': neig_distance_max,
            'neig.number.max': neig_number_max,
            'neig.number.total': 0,
        },
        'self.index': [],  # index of self in [sub]halo/galaxy catalog
        # 'self.index.inv': [],    # go from index in [sub]halo/galaxy catalog to index in this list
        'number': [],  # number of neighbors within mass and distance range, up to neig_number_max
        'distances': [],  # distances of neighbors, sorted
        'indices': [],  # indices of neighbors, sorted by distance
    }
    dimension_number = 3
    redspace_dimension_i = 2

    Say = io.SayClass(get_catalog_neighbor)

    # objects around which to find neighbors
    if center_indices is None:
        center_indices = get_indices_subhalo(
            cat, gal_mass_name, gal_mass_limits, hal_mass_limits, ilk, disrupt_mf
        )

    # potential neighbor objects
    if neig_indices is None:
        if (
            neig_gmass_limits
            and neig_gmass_limits[0] <= 1
            and neig_hmass_limits
            and neig_hmass_limits[0] > 1
        ):
            # if cutting on neighbor halo mass, ignore subhalo disruption
            disrupt_mf = 0
        neig_indices = get_indices_subhalo(
            cat, neig_gmass_name, neig_gmass_limits, neig_hmass_limits, neig_ilk, disrupt_mf
        )

    positions = cat['position'][center_indices]
    neig_positions = cat['position'][neig_indices]
    neig['info']['neig.number.total'] = neig_indices.size

    if distance_space == 'red':
        # apply redshift distance_space distortions to find via sphere in redshift distance_space
        positions[:, redspace_dimension_i] = coordinate.get_positions_in_redshift_space(
            positions[:, 2],
            cat['velocity'][center_indices][:, 2],
            cat.snapshot['time.hubble'],
            cat.snapshot['redshift'],
            cat.info['box.length'],
        )
        neig_positions[:, redspace_dimension_i] = coordinate.get_positions_in_redshift_space(
            neig_positions[:, 2],
            cat['velocity'][neig_indices][:, 2],
            cat.snapshot['time.hubble'],
            cat.snapshot['redshift'],
            cat.info['box.length'],
        )
    elif distance_space == 'proj':
        # get neighbors in projection, apply line-of-sight velocity cut later if defined
        proj_dim_is = np.setdiff1d(np.arange(dimension_number), [redspace_dimension_i])
        positions = positions[:, proj_dim_is]
        neig_positions = neig_positions[:, proj_dim_is]

    a = cat.snapshot['scalefactor']
    neig['distances'], neig['indices'] = coordinate.get_neighbors(
        positions * a,
        neig_positions * a,
        neig_distance_max,
        neig_number_max,
        cat.info['box.length'],
        neig_indices,
        return_lists=True,
    )

    if neig_velocity_dif_maxs is not None:
        # keep only neighbors found in projection that are within velocity cut of center
        if distance_space != 'proj':
            raise ValueError('neig_velocity_dif_maxs defined, but distance_space is not projected')

        if np.isscalar(neig_velocity_dif_maxs):
            neig_velocity_dif_maxs = (
                np.zeros(len(neig['indices']), cat['velocity'].dtype) + neig_velocity_dif_maxs
            )

        if not np.isscalar(neig_velocity_dif_maxs):
            if len(neig_velocity_dif_maxs) != len(neig['indices']):
                raise ValueError(
                    'neig_velocity_dif_maxs size = {} but centers size = {}'.format(
                        len(neig_velocity_dif_maxs), len(neig['indices'])
                    )
                )

        neig_iss = neig['indices']
        neig_distss = neig['distances']
        neig['indices'] = []
        neig['distances'] = []
        neig_keep_number = 0
        neig_tot_number = 0
        for neig_iis, neig_is in enumerate(neig_iss):
            velocity_difs = get_velocity_differences(
                cat,
                cat,
                neig_is,
                center_indices[neig_iis],
                dimension_indices=redspace_dimension_i,
                total_velocity=True,
            )
            masks = abs(velocity_difs) < neig_velocity_dif_maxs[neig_iis]
            neig['indices'].append(neig_is[masks])
            neig['distances'].append(neig_distss[neig_iis][masks])
            neig_keep_number += masks.sum()
            neig_tot_number += masks.size

        Say.say(
            'keep {} of {} ({:.1f}%) neig within velocity difference'.format(
                neig_keep_number, neig_tot_number, 100 * neig_keep_number / neig_tot_number
            )
        )

    if 'self.index' in neig:
        neig['self.index'] = center_indices
    if 'self.index.inv' in neig:
        neig['self.index.inv'] = array.get_arange(cat[gal_mass_name])
        neig['self.index.inv'][center_indices] = array.get_arange(center_indices.size)

    return neig


# --------------------------------------------------------------------------------------------------
# mass, ordering
# --------------------------------------------------------------------------------------------------
def get_halo_radius_mass(HaloProperty, virial_kind, hal, indices):
    '''
    Get virial radius [kpc physical] for each halo.

    Parameters
    ----------
    HaloProperty : class
        class to convert halo properties
    virial_kind : str
        virial overdensity definition
            '200m' -> average density is 200m x matter
            '200c' -> average density is 200 x critical
            'vir' -> average density is Bryan & Norman
            'fof.100m' -> edge density is 100 x matter, for FoF(ll=0.168)
            'fof.60m' -> edge density is 60 x matter, for FoF(ll=0.2)
    hal : dict
        halo catalog at snapshot
    indices : array
        halo indices

    Returns
    -------
    halo_radiuss : float or array
        halo radius[s]
    '''
    if virial_kind == '200c':
        halo_radiuss = HaloProperty.get_virial_radius(
            virial_kind, hal['mass.200c'][indices], redshift=hal.snapshot['redshift']
        )

    elif 'fof' in virial_kind:
        concentrations_fof = HaloProperty.convert_concentration(
            'fof.100m', '200c', hal['c.200c'][indices], hal.snapshot['redshift']
        )

        scale_radiuss = (
            hal['mass.fof'][indices]
            / (
                4
                / 3
                * np.pi
                * HaloProperty.get_nfw_normalization(hal['c.200c'][indices], 200)
                * HaloProperty.Cosmology.get_density(
                    'critical', hal.snapshot['redshift'], 'kpc physical'
                )
                * (np.log(1 + concentrations_fof) - concentrations_fof / (1 + concentrations_fof))
            )
        ) ** (1 / 3)
        halo_radiuss = concentrations_fof * scale_radiuss

    else:
        virdic = HaloProperty.get_virial_properties(
            virial_kind,
            '200c',
            hal['mass.200c'][indices],
            concens=hal['c.200c'][indices],
            redshift=hal.snapshot['redshift'],
        )
        halo_radiuss = virdic['radius']

    return halo_radiuss


def get_virial_velocity(HaloProperty, virial_kind, hal, indices):
    '''
    Get virial circular velocity[s] [km/s] for each halo.

    Parameters
    ----------
    HaloProperty : class
        class to convert halo properties
    virial_kind : str
        virial overdensity definition
            '200m' -> average density is 200 x matter
            '200c' -> average density is 200 x critical
            'vir' -> average density is Bryan & Norman
            'fof.100m' -> edge density is 100 x matter, for FoF(ll=0.168)
            'fof.60m' -> edge density is 60 x matter, for FoF(ll=0.2)
    hal : dict
        catalog of halos at snapshot
    indices : array
        halo indices

    Returns
    -------
    vir_velocity : float or array
        virial velocity
    '''
    if virial_kind == '200c':
        halo_masses = hal['mass.200c'][indices]
        halo_radiuss = HaloProperty.get_virial_radius(
            virial_kind, hal['mass.200c'][indices], redshift=hal.snapshot['redshift']
        )

    elif 'fof' in virial_kind:
        halo_masses = hal['mass.fof'][indices]
        concens_fof = HaloProperty.convert_concentration(
            'fof.100m', '200c', hal['c.200c'][indices], hal.snapshot['redshift']
        )
        halo_radiuss = HaloProperty.get_virial_radius(
            virial_kind, hal['mass.fof'][indices], concens_fof, redshift=hal.snapshot['redshift']
        )

    else:
        virdic = HaloProperty.get_virial_properties(
            virial_kind,
            '200c',
            hal['mass.200c'][indices],
            oncens=hal['c.200c'][indices],
            redshift=hal.snapshot['redshift'],
        )
        halo_masses = virdic['mass']
        halo_radiuss = virdic['radius']

    vir_velocity = (
        (constant.grav * constant.gram_per_sun) ** 0.5
        * (halo_masses / (halo_radiuss * constant.cm_per_kpc * hal.snapshot['scalefactor'])) ** 0.5
        * constant.kilo_per_centi
    )

    return vir_velocity


# --------------------------------------------------------------------------------------------------
# mass, ordering
# --------------------------------------------------------------------------------------------------
def convert_mass(sub, mass_from='star.mass', mass_min=10, mass_to='mass.peak'):
    '''
    Get 'to' mass/magnitude corresponding to 'from' one, assuming no scatter in relation.

    Parameters
    ----------
    sub : dict
        catalog of subhalos at snapshot
    mass_from : str
        input mass kind
    mass_min : float
        input mass value
    mass_to : str
        output mass kind

    Returns
    -------
    float or array : mass[es]
    '''
    temp = -sub[mass_from]
    mass_min = -mass_min
    sis_sort = np.argsort(temp)
    si = temp[sis_sort].searchsorted(mass_min)

    return sub[mass_to][sis_sort[si]]


def get_masses_parent(cats, ti, index, par_ti=None):
    '''
    Get all parent mass[es] at par_ti, sort decreasing by mass.

    Parameters
    ----------
    cats : list
        catalog[s] of [sub]halos across snapshots
    ti : int
        snapshot index
    index : int
        [sub]halo index
    par_ti : int
        snapshot index of progenitor

    Returns
    -------
    float or array
        mass[es]
    '''

    def masses_parent_recursive(cats, ti, ci, ti_par, mass_name):
        '''
        Recursively walk each parent tree back to par_ti, append mass at par_ti.
        '''
        masses = []
        par_ti, par_ci = ti + 1, cats[ti]['parent.index'][ci]
        while 0 <= par_ti < cats.snapshot['redshift'].size and par_ci > 0:
            if par_ti >= ti_par:
                masses.append(cats[par_ti][mass_name][par_ci])
            else:
                masses += masses_parent_recursive(cats, par_ti, par_ci, par_ti, mass_name)
            par_ti, par_ci = par_ti + 1, cats[par_ti]['parent.n.index'][par_ci]
        return masses

    if par_ti is None:
        par_ti = ti + 1

    return np.sort(masses_parent_recursive(cats, ti, index, par_ti, cats.info['mass.name']))[::-1]


def assign_number_rank(cat, property_name='mass.peak'):
    '''
    Assign ranked number to objects in catalog based on given property.

    Parameters
    ----------
    cat : dict
        catalog of [sub]halos at snapshot
    prop : str
        property to rank by
    '''
    indices = array.get_arange(cat[property_name])
    indices_sort = np.argsort(cat[property_name])[::-1]
    prop_number = property_name + '.rank'
    cat[prop_number] = np.zeros(indices.size)
    cat[prop_number][indices_sort] = indices
