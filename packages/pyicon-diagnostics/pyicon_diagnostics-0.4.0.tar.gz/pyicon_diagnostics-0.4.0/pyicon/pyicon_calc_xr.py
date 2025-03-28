import warnings
import numpy as np
import xarray as xr
from itertools import product


def convert_tgrid_data(
    ds_tg_in, check_previous_conversion=True, set_dim_order=None, old_dim_behaviour=None
):
    """Convert xarray grid file to grid file compatible with pyicon function.

    Parameters
    ----------
    ds_tg_in : xr.Dataset
        raw, unprocessed tgrid

    check_previous_conversion : bool
        check whether the dataset has already been converted and raise an error
        if so

    set_dim_order : bool or list
        Transpose the dataset so dimensions appear in the standard pyicon
        order, or the order listed

    old_dim_behaviour : bool or None
        If True labels "nc", "ne" and "nv" will not be corrected. If False
        they will be corrected and the DeprecationWarning will be silenced. If
        None a DeprecationWarning is triggered. Note that setting
        old_dim_behaviour will render the returned ds_IcD incompatible with
        other pyicon functions.


    Returns
    -------
    ds_IcD : xr.Dataset
        A tgrid dataset compatible with pyicon functions


    Notes
    -----
    Open classical ICON grid file by:
    ds_tg = xr.open_dataset(fpath_tg, chunks=dict())

    Then convert by:
    ds_IcD = pyic.convert_tgrid_data(ds_tg)
    """

    # make deep copy of ds_tg_in to avoid glaobal modifications if during this function call
    ds_tg = ds_tg_in.copy(deep=True)

    if old_dim_behaviour is None:
        warnings.warn(
            "The default behaviour for convert_tgrid has recently \
                       changed. It now corrects the dimension labels 'nc', \
                      'ne' and 'nv'. You should check your code for references\
                       to these dimension labels and update things accordingly.\
                      If you wish to use the old dimension behaviour, please \
                      set `old_dim_behaviour=True`, however, note that the \
                      returned dataset will not be compatible with other \
                      calc_xr functions. To silence this warning, set \
                      `old_dim_behaviour=False`.",
            DeprecationWarning,
        )

    if check_previous_conversion:
        if "converted_tgrid" in ds_tg.attrs:
            raise ValueError(
                "ds_tg has previously been converted by this function, \
                 applying the function again will lead to undocumented \
                 behaviour. To proceed, set 'check_previous_conversion=False'"
            )

    ds_IcD = xr.Dataset()

    # --- constants (from src/shared/mo_physical_constants.f90)
    ds_IcD["grid_sphere_radius"] = 6.371229e6
    ds_IcD["grav"] = 9.80665
    ds_IcD["earth_angular_velocity"] = 7.29212e-05
    ds_IcD["rho0"] = 1025.022
    ds_IcD["rhoi"] = 917.0
    ds_IcD["rhos"] = 300.0
    ds_IcD["sal_ref"] = 35.0
    ds_IcD["sal_ice"] = 5.0
    rcpl = 3.1733
    cpd = 1004.64
    ds_IcD["cp"] = (rcpl + 1.0) * cpd
    ds_IcD["tref"] = 273.15
    ds_IcD["tmelt"] = 273.15
    ds_IcD["tfreeze"] = -1.9
    ds_IcD["alf"] = 2.8345e6 - 2.5008e6  # [J/kg]   latent heat for fusion

    # --- distances and areas
    ds_IcD["cell_area"] = ds_tg["cell_area"]
    ds_IcD["cell_area_p"] = ds_tg["cell_area_p"]
    ds_IcD["dual_area"] = ds_tg["dual_area"]
    ds_IcD["edge_length"] = ds_tg["edge_length"]
    ds_IcD["dual_edge_length"] = ds_tg["dual_edge_length"]
    ds_IcD["edge_cell_distance"] = ds_tg["edge_cell_distance"].transpose()
    # --- neighbor information
    ds_IcD["vertex_of_cell"] = ds_tg["vertex_of_cell"].transpose() - 1
    ds_IcD["edge_of_cell"] = ds_tg["edge_of_cell"].transpose() - 1
    ds_IcD["vertices_of_vertex"] = ds_tg["vertices_of_vertex"].transpose() - 1
    ds_IcD["edges_of_vertex"] = ds_tg["edges_of_vertex"].transpose() - 1
    ds_IcD["edge_vertices"] = ds_tg["edge_vertices"].transpose() - 1
    ds_IcD["adjacent_cell_of_edge"] = ds_tg["adjacent_cell_of_edge"].transpose() - 1
    ds_IcD["cells_of_vertex"] = ds_tg["cells_of_vertex"].transpose() - 1
    ds_IcD["adjacent_cell_of_cell"] = ds_tg["neighbor_cell_index"].transpose() - 1
    # --- orientation
    ds_IcD["orientation_of_normal"] = ds_tg["orientation_of_normal"].transpose()
    ds_IcD["edge_orientation"] = ds_tg["edge_orientation"].transpose()
    ds_IcD["tangent_orientation"] = ds_tg["edge_system_orientation"].transpose()

    # --- masks
    ds_IcD["cell_sea_land_mask"] = ds_tg["cell_sea_land_mask"]
    ds_IcD["edge_sea_land_mask"] = ds_tg["edge_sea_land_mask"]

    # --- coordinates
    ds_IcD["cell_cart_vec"] = xr.concat(
        [
            ds_tg["cell_circumcenter_cartesian_x"],
            ds_tg["cell_circumcenter_cartesian_y"],
            ds_tg["cell_circumcenter_cartesian_z"],
        ],
        dim="cart",
    ).transpose()

    ds_IcD["vert_cart_vec"] = xr.concat(
        [
            ds_tg["cartesian_x_vertices"],
            ds_tg["cartesian_y_vertices"],
            ds_tg["cartesian_z_vertices"],
        ],
        dim="cart",
    ).transpose()

    ds_IcD["edge_cart_vec"] = xr.concat(
        [
            ds_tg["edge_middle_cartesian_x"],
            ds_tg["edge_middle_cartesian_y"],
            ds_tg["edge_middle_cartesian_z"],
        ],
        dim="cart",
    ).transpose()

    ds_IcD["dual_edge_cart_vec"] = xr.concat(
        [
            ds_tg["edge_dual_middle_cartesian_x"],
            ds_tg["edge_dual_middle_cartesian_y"],
            ds_tg["edge_dual_middle_cartesian_z"],
        ],
        dim="cart",
    ).transpose()

    ds_IcD["edge_prim_norm"] = xr.concat(
        [
            ds_tg["edge_primal_normal_cartesian_x"],
            ds_tg["edge_primal_normal_cartesian_y"],
            ds_tg["edge_primal_normal_cartesian_z"],
        ],
        dim="cart",
    ).transpose()

    for point, dim in product("ecv", ("lat", "lon")):
        coord = point + dim
        ds_IcD[coord] *= 180.0 / np.pi
        ds_IcD[coord].attrs["units"] = "degrees"

    ds_IcD["fc"] = (
        2.0 * ds_IcD.earth_angular_velocity * np.sin(ds_IcD.clat * np.pi / 180.0)
    )
    ds_IcD["fe"] = (
        2.0 * ds_IcD.earth_angular_velocity * np.sin(ds_IcD.elat * np.pi / 180.0)
    )
    ds_IcD["fv"] = (
        2.0 * ds_IcD.earth_angular_velocity * np.sin(ds_IcD.vlat * np.pi / 180.0)
    )

    try:
        ds_IcD = ds_IcD.rename({"ncells": "cell"})
    except ValueError:
        pass

    # Default dimension names are messy and often wrong. Let's rename them.
    dim_name_remappings = {
        "vertex_of_cell": {"nv": "nv_c"},
        "edge_vertices": {"nc": "nv_e"},
        "vertices_of_vertex": {"ne": "nv_v"},
        "edge_of_cell": {"nv": "ne_c"},
        "edges_of_vertex": {"ne": "ne_v"},
        "adjacent_cell_of_edge": {"nc": "nc_e"},
        "cells_of_vertex": {"ne": "nc_v"},
        "edge_cell_distance": {"nc": "nc_e"},
        "orientation_of_normal": {"nv": "ne_c"},
        "edge_orientation": {"ne": "ne_v"},
        "adjacent_cell_of_cell": {"nv": "nc_c"},
    }

    for variable in dim_name_remappings:
        ds_IcD[variable] = ds_IcD[variable].rename(dim_name_remappings[variable])

    ds_IcD.attrs["converted_tgrid"] = True
    ds_tg.attrs["converted_tgrid"] = True

    if set_dim_order is None:
        standard_order = ["cell", "vertex", "edge", "nc", "nv", "ne", "cart", ...]
        ds_IcD = ds_IcD.transpose(*standard_order, missing_dims="ignore")
    elif set_dim_order:
        ds_IcD = ds_IcD.transpose(*set_dim_order, missing_dims="ignore")

    return ds_IcD


def _print_verbose(verbose=1, message="", verbose_stage=1):
    """Prints message depending on verbosity"""
    if verbose >= verbose_stage:
        print(message)
    return


def xr_crop_tgrid(ds_tg, ireg_c, verbose=1):
    """Crop a grid file.

    Parameters
    ----------
    ds_tg : xr.Dataset
        dataset containing the grid file

    ireg_c : np.array
        list of cell indices which should by in cropped domain


    Returns
    -------
    ds_tg_cut: xarray Dataset, which contains (most of) the cropped grid variables.


    Examples
    --------

    >>> ds_tg = xr.open_mfdataset(fpath_tgrid)
    >>> clon = ds_tg.clon.compute().data * 180./np.pi
    >>> clat = ds_tg.clat.compute().data * 180./np.pi
    >>>
    >>> lon_reg_3 = [6, 10]
    >>> lat_reg_3 = [-32, -30]
    >>> ireg_c = np.where(
    ...    (clon>lon_reg[0]) & (clon<=lon_reg[1]) & (clat>lat_reg[0]) & (clat<=lat_reg[1])
    ... )[0]
    >>>
    >>> ds_tg_cut = pyic.xr_crop_tgrid(ds_tg, ireg_c)
    """

    if ("converted_tgrid" in ds_tg.attrs) and ds_tg.attrs["converted_tgrid"]:
        offset = 0
    else:
        offset = 1

    # --- find edges and vertices belonging to cells of cutted domain
    _print_verbose(verbose, "find edges")
    vertex_of_cell = ds_tg.vertex_of_cell.isel(cell=ireg_c).compute().data - offset
    edge_of_cell = ds_tg.edge_of_cell.isel(cell=ireg_c).compute().data - offset
    ireg_e, inde = np.unique(edge_of_cell, return_index=True)
    ireg_v, indv = np.unique(vertex_of_cell, return_index=True)

    ireg_c = ireg_c.astype("int32")
    ireg_e = ireg_e.astype("int32")
    ireg_v = ireg_v.astype("int32")

    # --- new dataset with cutted coordinates
    _print_verbose(verbose, "cut coordinates")
    ds_tg_cut = xr.Dataset(
        coords=dict(
            clon=ds_tg["clon"][ireg_c],
            clat=ds_tg["clat"][ireg_c],
            elon=ds_tg["elon"][ireg_e],
            elat=ds_tg["elat"][ireg_e],
            vlon=ds_tg["vlon"][ireg_v],
            vlat=ds_tg["vlat"][ireg_v],
        )
    )
    ds_tg_cut["ireg_c"] = xr.DataArray(ireg_c, dims=["cell"])
    ds_tg_cut["ireg_e"] = xr.DataArray(ireg_e, dims=["edge"])
    ds_tg_cut["ireg_v"] = xr.DataArray(ireg_v, dims=["vertex"])

    # --- re-index
    _print_verbose(verbose, "reindex")
    reindex_c = np.zeros_like(ds_tg.clon, dtype="int32") - offset
    reindex_c[ireg_c] = np.arange(ireg_c.size, dtype="int32")
    reindex_e = np.zeros_like(ds_tg.elon, dtype="int32") - offset
    reindex_e[ireg_e] = np.arange(ireg_e.size, dtype="int32")
    reindex_v = np.zeros_like(ds_tg.vlon, dtype="int32") - offset
    reindex_v[ireg_v] = np.arange(ireg_v.size, dtype="int32")

    var = "vertex_of_cell"
    da = ds_tg[var].isel(cell=ireg_c) - offset
    data = reindex_v[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "edge_vertices"
    da = ds_tg[var].isel(edge=ireg_e) - offset
    data = reindex_v[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "vertices_of_vertex"
    da = ds_tg[var].isel(vertex=ireg_v) - offset
    data = reindex_v[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "edge_of_cell"
    da = ds_tg[var].isel(cell=ireg_c) - offset
    data = reindex_e[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "edges_of_vertex"
    da = ds_tg[var].isel(vertex=ireg_v) - offset
    data = reindex_e[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "adjacent_cell_of_edge"
    da = ds_tg[var].isel(edge=ireg_e) - offset
    data = reindex_c[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    var = "cells_of_vertex"
    da = ds_tg[var].isel(vertex=ireg_v) - offset
    data = reindex_c[da.data.flatten().astype("int32")].reshape(da.shape)
    ds_tg_cut[var] = xr.DataArray(data + offset, dims=da.dims)

    reindex_vars = [
        "vertex_of_cell",
        "vertices_of_vertex",
        "edge_of_cell",
        "edges_of_vertex",
        "adjacent_cell_of_edge",
        "cells_of_vertex",
        "edge_vertices",
    ]

    reindex_dict = {
        "vertex_of_cell": {"from": "c", "to": "v"},
        "vertices_of_vertex": {"from": "v", "to": "v"},
        "edge_of_cell": {"from": "c", "to": "e"},
        "edges_of_vertex": {"from": "v", "to": "e"},
        "adjacent_cell_of_edge": {"from": "e", "to": "c"},
        "cells_of_vertex": {"from": "v", "to": "c"},
        "edge_vertices": {"from": "e", "to": "v"},
    }

    # --- cut all variables remaining
    for var in ds_tg.keys():
        if var not in reindex_vars:
            var_cut = False
            if "vertex" in ds_tg[var].dims:
                ds_tg_cut[var] = ds_tg[var].isel(vertex=ireg_v)
                var_cut = True
            if "cell" in ds_tg[var].dims:
                ds_tg_cut[var] = ds_tg[var].isel(cell=ireg_c)
                var_cut = True
            if "edge" in ds_tg[var].dims:
                ds_tg_cut[var] = ds_tg[var].isel(edge=ireg_e)
                var_cut = True
            if not var_cut:
                ds_tg_cut[var] = ds_tg[var]
    return ds_tg_cut


## Functions to map between 3D Cartesian and 2D local vectors
def xr_calc_2dlocal_from_3d(ds_IcD, p_vn_c):
    """Transform vector from cartesian to spherical basis at a cell center

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    p_vn_c : xr.Dataset
        dataset containing cartesian representation of
        vector. Should have the dimension 'cart'


    Returns
    -------
    uo : xr.DataArray
        zonal component of vector

    vo : xr.DataArray
        meridional component of vector


    Notes
    -----
    The 3D vector passed is not (u, v, w) where w is the local
    vertical.

    """
    sinLon = np.sin(ds_IcD.clon * np.pi / 180.0)
    cosLon = np.cos(ds_IcD.clon * np.pi / 180.0)
    sinLat = np.sin(ds_IcD.clat * np.pi / 180.0)
    cosLat = np.cos(ds_IcD.clat * np.pi / 180.0)

    u1 = p_vn_c.isel(cart=0)
    u2 = p_vn_c.isel(cart=1)
    u3 = p_vn_c.isel(cart=2)

    uo = u2 * cosLon - u1 * sinLon
    vo = -(u1 * cosLon + u2 * sinLon) * sinLat + u3 * cosLat

    return uo, vo


def xr_calc_3d_from_2dlocal(ds_IcD, uo, vo):
    """Transform vector from spherical to cartesian basis at a cell center

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    uo : xr.DataArray
        zonal component

    vo : xr.DataArray
        meridional component

    Returns
    -------
    p_vn_c : xr.DataArray
        representation of the horizontal vector in a cartesian basis.


    Notes
    -----
    The components of the returned vector *are not* zonal, meridional and vertical.
    This function transforms a locally horizontal vector from a spherical representation
    to a cartesian representation.

    """
    sinLon = np.sin(ds_IcD.clon * np.pi / 180.0)
    cosLon = np.cos(ds_IcD.clon * np.pi / 180.0)
    sinLat = np.sin(ds_IcD.clat * np.pi / 180.0)
    cosLat = np.cos(ds_IcD.clat * np.pi / 180.0)

    u1 = -uo * sinLon - vo * sinLat * cosLon
    u2 = uo * cosLon - vo * sinLat * sinLon
    u3 = vo * cosLat

    new_dims = list(uo.dims) + ["cart"]
    p_vn_c = xr.concat([u1, u2, u3], dim="cart", coords="minimal").transpose(*new_dims)
    return p_vn_c


## Mapping between cells and edges
def xr_calc_edge2cell_coeff_cc_t(ds_IcD):
    """Calculates the cell to edge coefficients

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    edge2cell_coeff_cc_t : xr.DataArray
        coefficients used in mapping cells to edges
    """
    dist_vector = ds_IcD.edge_cart_vec - ds_IcD.cell_cart_vec.isel(
        cell=ds_IcD.adjacent_cell_of_edge
    )
    orientation = (dist_vector * ds_IcD.edge_prim_norm).sum(dim="cart")
    dist_vector *= np.sign(orientation)
    edge2cell_coeff_cc_t = (
        ds_IcD.edge_prim_norm
        * ds_IcD.grid_sphere_radius
        * np.sqrt((dist_vector**2).sum(dim="cart"))
        / ds_IcD.dual_edge_length
    )
    edge2cell_coeff_cc_t = edge2cell_coeff_cc_t.transpose("edge", "nc_e", "cart")
    return edge2cell_coeff_cc_t


def xr_cell2edges(ds_IcD, p_vn_c, edge2cell_coeff_cc_t=None):
    """Remaps vector from cell center to edges

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    p_vn_c : xr.DataArray
        locally horizontal vector on cell center in cartesian
        representation.

    edge2cell_coeff_cc_t : xr.DataArray or None
        coefficients used in mapping cells to edges


    Returns
    -------
    ptp_vn : xr.DataArray
        vector p_vn_c remapped to edges
    """
    if edge2cell_coeff_cc_t is None:
        edge2cell_coeff_cc_t = xr_calc_edge2cell_coeff_cc_t(ds_IcD)
    ic0 = ds_IcD.adjacent_cell_of_edge.isel(nc_e=0).data
    ic1 = ds_IcD.adjacent_cell_of_edge.isel(nc_e=1).data
    ptp_vn = (
        p_vn_c.isel(cell=ic0).rename({"cell": "edge"})  # .chunk(dict(edge=ic0.size))
        * edge2cell_coeff_cc_t.isel(nc_e=0)
    ).sum(dim="cart") + (
        p_vn_c.isel(cell=ic1).rename({"cell": "edge"})  # .chunk(dict(edge=ic0.size))
        * edge2cell_coeff_cc_t.isel(nc_e=1)
    ).sum(
        dim="cart"
    )
    return ptp_vn


## Mapping between edges and cells
def xr_calc_fixed_volume_norm(ds_IcD):
    """Calculates the fixed volume of a grid cell divided by grid_sphere_radius.

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    fixed_vol_norm : xr.DataArray
        volume of grid cell
    """
    dist_vector = (
        ds_IcD.edge_cart_vec.isel(edge=ds_IcD.edge_of_cell) - ds_IcD.cell_cart_vec
    )
    norm = np.sqrt((dist_vector**2).sum(dim="cart"))
    fixed_vol_norm = (
        0.5
        * norm
        * ds_IcD.edge_length.isel(edge=ds_IcD.edge_of_cell)
        / ds_IcD.grid_sphere_radius
    )
    fixed_vol_norm = fixed_vol_norm.sum(dim="ne_c")
    return fixed_vol_norm


def xr_calc_edge2cell_coeff_cc(ds_IcD):
    """Calculates the edge to cell coefficients

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    edge2cell_coeff_cc : xr.DataArray
        coefficients used in mapping edges to cells
    """
    dist_vector = (
        ds_IcD.edge_cart_vec.isel(edge=ds_IcD.edge_of_cell) - ds_IcD.cell_cart_vec
    )
    edge2cell_coeff_cc = (
        dist_vector
        * ds_IcD.edge_length.isel(edge=ds_IcD.edge_of_cell)
        / ds_IcD.grid_sphere_radius
        * ds_IcD.orientation_of_normal
    )
    edge2cell_coeff_cc = edge2cell_coeff_cc.compute()
    return edge2cell_coeff_cc


def xr_edges2cell(ds_IcD, ve, dze, dzc, edge2cell_coeff_cc=None, fixed_vol_norm=None):
    """Remaps vector from edges to cell

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    ve : xr.DataArray
        vector on edges

    dze : xr.DataArray
        vertical grid spacing at edge midpoint

    dzc : xr.DataArray
        vertical grid spacing at cell centre

    edge2cell_coeff_cc : xr.DataArray or None
        coefficients used in mapping edges to cells

    fixed_vol_norm : xr.DataArray or None
        volume of grid cell


    Returns
    -------
    p_vn_c : xr.DataArray
        cartesian representation of vector ve on cell centres
    """
    if fixed_vol_norm is None:
        fixed_vol_norm = xr_calc_fixed_volume_norm(ds_IcD)
    if edge2cell_coeff_cc is None:
        edge2cell_coeff_cc = xr_calc_edge2cell_coeff_cc(ds_IcD)
    # if ve.dims != dze.dims:
    #  raise ValueError('::: Dims of ve and dze have to be the same!:::')
    p_vn_c = (
        edge2cell_coeff_cc
        * ve.isel(edge=ds_IcD.edge_of_cell)
        # * ds_fx.prism_thick_e.isel(edge=ds_IcD.edge_of_cell)
        * dze.isel(edge=ds_IcD.edge_of_cell)
    ).sum(dim="ne_c")
    if "depth" in p_vn_c.dims:
        p_vn_c = p_vn_c.transpose("depth", "cell", "cart")

    p_vn_c = p_vn_c / (
        fixed_vol_norm
        # * ds_fx.prism_thick_c
        * dzc
    )
    return p_vn_c


## Mapping between edges and edges
def xr_calc_edge2edge_viacell_coeff(ds_IcD):
    """Calculate coefficients for mapping edge vectors to edge vectors

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info
    """
    raise NotImplementedError("")
    # FIXME: Continue here
    edge2edge_viacell_coeff = ()
    return edge2edge_viacell_coeff


def xr_edges2edges_via_cell(ds_IcD, vn_e, dze="const"):
    """Maps edges to edges via a cell

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    vn_e : xr.DataArray
        vector at edge

    dze : xr.DataArray or 'const'
    """
    raise NotImplementedError("")
    # FIXME: Continue here
    out_vn_e = ()
    return out_vn_e


def xr_edges2edges_via_cell_scalar(ds_IcD, vn_e, scalar, dze="const"):
    """Calculates flux of scalar at edges

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    vn_e : xr.DataArray
        vector at edge

    scalar : xr.DataArray
        scalar at cell centre

    dze : xr.DataArray or 'const'
    """
    raise NotImplementedError("")
    # FIXME: Continue here
    out_vn_e = ()
    return out_vn_e


## Divergence
def xr_calc_div_coeff(ds_IcD):
    """Calculates coefficients for calculating divergence

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    div_coeff : xr.DataArray
        coefficients for calculating divergence
    """
    div_coeff = (
        ds_IcD.edge_length.isel(edge=ds_IcD.edge_of_cell)
        * ds_IcD.orientation_of_normal
        / ds_IcD.cell_area
    )
    return div_coeff


def xr_calc_div(ds_IcD, vector, div_coeff=None):
    """Calculates coefficients for calculating divergence

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    vector : xr.DataArray
        vector at cell edges

    div_coeff : xr.DataArray
        coefficients for calculating divergence

    Returns
    -------
    div_of_vector : xr.DataArray
        divergence of vector at cell centers

    """
    if div_coeff is None:
        div_coeff = xr_calc_div_coeff(ds_IcD)
    div_of_vector = (vector.isel(edge=ds_IcD.edge_of_cell) * div_coeff).sum(dim="ne_c")
    return div_of_vector


## Gradient
def xr_calc_grad_coeff(ds_IcD):
    """Calculates coefficients for calculating gradient

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    grad_coeff : xr.DataArray
        coefficients for calculating gradient
    """
    grad_coeff = 1.0 / ds_IcD.dual_edge_length
    return grad_coeff


def xr_calc_grad(ds_IcD, scalar, grad_coeff=None):
    """Calculates coefficients for calculating gradient

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    scalar : xr.DataArray
        scalar at cell center

    grad_coeff : xr.DataArray
        coefficients for calculating gradient


    Returns
    -------
    grad_of_scalar : xr.DataArray
        horizontal gradient of scalar at edges
    """
    if grad_coeff is None:
        grad_coeff = xr_calc_grad_coeff(ds_IcD)
    grad_of_scalar = (
        scalar.isel(cell=ds_IcD.adjacent_cell_of_edge.isel(nc_e=1))
        - scalar.isel(cell=ds_IcD.adjacent_cell_of_edge.isel(nc_e=0))
    ) * grad_coeff
    return grad_of_scalar


# Curl
def xr_calc_rot_coeff(ds_IcD):
    """Calculates coefficients used in calculating the curl

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info


    Returns
    -------
    curl_coeffs : xr.DataArray
        coefficients for calculating curls
    """
    curl_coeffs = (
        ds_IcD["edge_orientation"]
        * ds_IcD["dual_edge_length"].isel(edge=ds_IcD["edges_of_vertex"].compute())
        / ds_IcD["dual_area"]
    )
    return curl_coeffs


def xr_calc_curl(ds_IcD, vector, rot_coeff=None):
    """Calculates the vertical component of the curl

    Parameters
    ----------
    ds_IcD : xr.Dataset
        pyicon dataset containing coordinate info

    vector : xr.DataArray
        Dataarray containing vector variable on cell edges.

    rot_coeff : xr.DataArray or None
        Array containing dims ("vertex", "ne_v")


    Returns
    -------
    curl_vec : xr.DataArray
        vertical component of the curl of the vector defined on vertex points


    Notes
    -----
    We calculate the curl through the use of Stokes'/Green's theorem. A similar
    procedure can be used to calculate the horizontal components of the curl
    (oriented along cell edges and defined at intermediate Z levels.) This will
    be implemented in a future release.

    If you're using this function on large datasets, performance gains may be
    made if you play around with the dimension order.

    """
    assert "edge" in vector.dims

    if rot_coeff is None:
        rot_coeff = xr_calc_rot_coeff(ds_IcD)

    curl_vec = (vector.isel(edge=ds_IcD["edges_of_vertex"].compute()) * rot_coeff).sum(
        dim="ne_v"
    )
    return curl_vec
