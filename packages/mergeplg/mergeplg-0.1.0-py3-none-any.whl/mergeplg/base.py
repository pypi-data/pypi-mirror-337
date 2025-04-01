"""Module for merging CML and rain gauge data with gridded data."""

from __future__ import annotations

import numpy as np
import poligrain as plg
import xarray as xr


class Base:
    """Update weights and geometry and evaluate rainfall grid at CMLs and rain gauges

    Parent class for the merging and interpolation methods. Works by keeping a copy of
    the CML and rain gauge geometry (self.x0_cml, self.x0_gauge) as well as the weights
    used to obtain values of gridded data at the CML and rain gauge positions
    (self.intersect_weights, self.get_grid_at_points).

    """

    def __init__(
        self,
        grid_point_location="center",
    ):
        """Construct base class

        Parameters
        ----------
        self.grid_point_location str
            Grid cell reference position. For instance 'center'.
        self.intersect_weights xarray.Dataset
            Weights for getting radar observations along CMLs.
        self.gauge_ids numpy.array
            Name of rain gauges, used to check if gauge weights needs to be updated.
        self.get_grid_at_points function
            Returns the grids value at the rain gauge positions.
        self.x0_cml xarray.DataArray
            Midpoint or discretized coordinates along the CMLs, depending on
            if update_ or update_block_ was used to update geometry
        self.x0_gauge xarray.DataArray
            Rain gauge coordinates.
        """
        # Location of grid point, used in intersect weights
        self.grid_point_location = grid_point_location

        # CML weights and gauge weights
        self.intersect_weights = None

        # Names of gauges, used for checking changes to rain gauges
        self.gauge_ids = None

        # Init gauge positions and names
        self.get_grid_at_points = None

        # Init coordinates for gauge and CML
        self.x0_gauge = None
        self.x0_cml = None

    def update_x0_(self, da_cml=None, da_gauge=None):
        """Update x0 geometry for CML and gauge

        This function uses the midpoint of the CML as CML reference.

        Parameters
        ----------
        da_cml: xarray.DataArray
            CML observations. Must contain the projected coordinates of the
            CML (site_0_x, site_0_y, site_1_x, da_cml.site_1_y).
        da_gauge: xarray.DataArray
            Gauge observations. Must contain the projected coordinates of the
            rain gauges (x, y).
        """
        # Check that there is CML or gauge data, if not raise an error
        if (da_cml is None) and (da_gauge is None):
            msg = "Please provide cml or gauge data"
            raise ValueError(msg)

        # If CML is present
        if da_cml is not None:
            # If geometry has not been estimated, compute for all
            if self.x0_cml is None:
                self.x0_cml = calculate_cml_midpoint(da_cml)

            # Update x0_cml, reusing x0_cml from previous iteration
            else:
                # New CML names
                cml_id_new = np.sort(da_cml.cml_id.data)

                # CML names of previous update
                cml_id_old = np.sort(self.x0_cml.cml_id.data)

                # Identify cml_id that is in the new and old array
                cml_id_keep = np.intersect1d(cml_id_new, cml_id_old)

                # Slice stored CML midpoints, keeping only new ones
                self.x0_cml = self.x0_cml.sel(cml_id=cml_id_keep)

                # Identify new cml_id
                cml_id_not_in_old = np.setdiff1d(cml_id_new, cml_id_old)

                # If new cml_ids available
                if cml_id_not_in_old.size > 0:
                    # Slice da_cml to get only missing coords
                    da_cml_add = da_cml.sel(cml_id=cml_id_not_in_old)

                    # Calculate CML midpoint for new CMLs
                    x0_cml_add = calculate_cml_midpoint(da_cml_add)

                    # Add to existing x0
                    self.x0_cml = xr.concat([self.x0_cml, x0_cml_add], dim="cml_id")

            # Update final x0_cml, this sorts self.x0_cml according to da_cml.cml_id
            self.x0_cml = self.x0_cml.sel(cml_id=da_cml.cml_id.data)

        # If gauge data is present
        if da_gauge is not None:
            # If geometry has not been estimated, compute for all
            if self.x0_gauge is None:
                self.x0_gauge = calculate_gauge_midpoint(da_gauge)
            # Update x0_gauge, reusing x0_gauge from previous iteration
            else:
                # Get names of new gauges
                gauge_id_new = da_gauge.id.data

                # Get names of gauges in previous update
                gauge_id_old = self.x0_gauge.id.data

                # Check that equal, element order is important
                if not np.array_equal(gauge_id_new, gauge_id_old):
                    # Calculate gauge coordinates
                    self.x0_gauge = calculate_gauge_midpoint(da_gauge)

    def update_x0_block_(self, discretization, da_cml=None, da_gauge=None):
        """Update x0 geometry for CML and gauge assuming block data

        This function uses the full CML geometry and makes the rain gauge look
        like a line with zero length.

        Parameters
        ----------
        discretization: int
            Number of discretized intervals for the CMLs.
        da_cml: xarray.DataArray
            CML observations. Must contain the projected coordinates
            (site_0_x, site_0_y, site_1_x, site_1_y) of the CML.
        da_gauge: xarray.DataArray
            Gauge observations. Must contain the projected coordinates (x, y).
        """
        # Check that there is radar or gauge data, if not raise an error
        if (da_cml is None) and (da_gauge is None):
            msg = "Please provide cml or gauge data"
            raise ValueError(msg)

        # If CML is present
        if da_cml is not None:
            # If intersect weights not computed, compute all weights
            if self.x0_cml is None:
                # CML coordinates along all links
                self.x0_cml = calculate_cml_line(da_cml, discretization=discretization)

            # Update weights, reusing already computed weights
            else:
                # New cml names
                cml_id_new = np.sort(da_cml.cml_id.data)

                # cml names of previous update
                cml_id_old = np.sort(self.x0_cml.cml_id.data)

                # Identify cml_id that is in the new and old array
                cml_id_keep = np.intersect1d(cml_id_new, cml_id_old)

                # Slice stored CML midpoints, keeping only new ones
                self.x0_cml = self.x0_cml.sel(cml_id=cml_id_keep)

                # Identify new cml_id
                cml_id_not_in_old = np.setdiff1d(cml_id_new, cml_id_old)

                # If new cml_ids available
                if cml_id_not_in_old.size > 0:
                    # Slice da_cml to get only missing coords
                    da_cml_add = da_cml.sel(cml_id=cml_id_not_in_old)

                    # Calculate CML geometry for new links
                    x0_cml_add = calculate_cml_line(
                        da_cml_add, discretization=discretization
                    )

                    # Add new x0 to self.x0_cml
                    self.x0_cml = xr.concat([self.x0_cml, x0_cml_add], dim="cml_id")

            # Update final x0_cml
            self.x0_cml = self.x0_cml.sel(cml_id=da_cml.cml_id.data)

        # If gauge data is present
        if da_gauge is not None:
            # If this is the first update
            if self.x0_gauge is None:
                # Calculate gauge coordinates
                x0_gauge = calculate_gauge_midpoint(da_gauge)

                # Repeat the same coordinates so that the array gets the same
                # shape as x0_cml, used for block kriging
                self.x0_gauge = x0_gauge.expand_dims(
                    disc=range(discretization + 1)
                ).transpose("id", "yx", "disc")

            else:
                # Get names of new gauges
                gauge_id_new = da_gauge.id.data

                # Get names of gauges in previous update
                gauge_id_old = self.x0_gauge.id.data

                # Check that equal, element order is important
                if not np.array_equal(gauge_id_new, gauge_id_old):
                    # Calculate gauge coordinates
                    x0_gauge = calculate_gauge_midpoint(da_gauge)

                    # As the gauge is just a point, repeat the gauge coord, this
                    # creates the block geometry
                    self.x0_gauge = x0_gauge.expand_dims(
                        disc=range(discretization + 1)
                    ).transpose("id", "yx", "disc")

    def update_weights_(self, da_grid, da_cml=None, da_gauge=None):
        """Update grid weights for CML and gauge

        Constructs the CML intersect weights, for retrieving rainfall rates along
        gridded data. Also constructs function used for getting rainfall rates

        Parameters
        ----------
        da_grid: xarray.DataArray
            Gridded rainfall data. Must contain the projected coordinates
            (x_grid, y_grid).
        da_cml: xarray.DataArray
            CML observations. Must contain the projected coordinates for the CML
            (site_0_x, site_0_y, site_1_x, site_1_y).
        da_gauge: xarray.DataArray
            Gauge observations. Must contain the projected coordinates for the
            rain gauge positions (y, x).
        """
        # Check that there is CML or gauge data, if not raise an error
        if (da_cml is None) and (da_gauge is None):
            msg = "Please provide cml or gauge data"
            raise ValueError(msg)

        # If CML is present
        if da_cml is not None:
            # If intersect weights not computed, compute all weights
            if self.intersect_weights is None:
                # Calculate CML radar grid intersection weights
                self.intersect_weights = (
                    plg.spatial.calc_sparse_intersect_weights_for_several_cmls(
                        x1_line=da_cml.site_0_x.data,
                        y1_line=da_cml.site_0_y.data,
                        x2_line=da_cml.site_1_x.data,
                        y2_line=da_cml.site_1_y.data,
                        cml_id=da_cml.cml_id.data,
                        x_grid=da_grid.x_grid.data,
                        y_grid=da_grid.y_grid.data,
                        grid_point_location=self.grid_point_location,
                    )
                )

            # Update weights, reusing already computed weights
            else:
                # New cml names
                cml_id_new = np.sort(da_cml.cml_id.data)

                # cml names of previous update
                cml_id_old = np.sort(self.intersect_weights.cml_id.data)

                # Identify cml_id that is in the new and old array
                cml_id_keep = np.intersect1d(cml_id_new, cml_id_old)

                # Slice the stored intersect weights, keeping only new ones
                self.intersect_weights = self.intersect_weights.sel(cml_id=cml_id_keep)

                # Identify new cml_id
                cml_id_not_in_old = np.setdiff1d(cml_id_new, cml_id_old)

                # If new cml_ids available
                if cml_id_not_in_old.size > 0:
                    # Slice da_cml to get only missing coords
                    da_cml_add = da_cml.sel(cml_id=cml_id_not_in_old)

                    # Intersect weights of CMLs to add
                    intersect_weights_add = (
                        plg.spatial.calc_sparse_intersect_weights_for_several_cmls(
                            x1_line=da_cml_add.site_0_x.data,
                            y1_line=da_cml_add.site_0_y.data,
                            x2_line=da_cml_add.site_1_x.data,
                            y2_line=da_cml_add.site_1_y.data,
                            cml_id=da_cml_add.cml_id.data,
                            x_grid=da_grid.x_grid.data,
                            y_grid=da_grid.y_grid.data,
                            grid_point_location=self.grid_point_location,
                        )
                    )

                    # Add new intersect weights
                    self.intersect_weights = xr.concat(
                        [self.intersect_weights, intersect_weights_add], dim="cml_id"
                    )

            # Update final self.intersect_weights
            self.intersect_weights = self.intersect_weights.sel(
                cml_id=da_cml.cml_id.data
            )

        # If gauge data is present
        if da_gauge is not None:
            # If intersect weights not computed, compute all weights
            if self.gauge_ids is None:
                # Calculate gridpoints for gauges
                self.get_grid_at_points = plg.spatial.GridAtPoints(
                    da_gridded_data=da_grid,
                    da_point_data=da_gauge,
                    nnear=1,
                    stat="best",
                )

                # Store gauge names for check
                self.gauge_ids = da_gauge.id.data

            # Update weights, if new gauge data is provided
            else:
                # Get names of new gauges
                gauge_id_new = da_gauge.id.data

                # Get names of gauges in previous update
                gauge_id_old = self.gauge_ids

                # Check that equal, element order is important
                if not np.array_equal(gauge_id_new, gauge_id_old):
                    # Calculate new gauge positions
                    self.get_grid_at_points = plg.spatial.GridAtPoints(
                        da_gridded_data=da_grid,
                        da_point_data=da_gauge,
                        nnear=1,
                        stat="best",
                    )

    def get_obs_x0_(self, da_cml=None, da_gauge=None):
        """Calculate ground observations and x0 for current state

        Returns and ordered list of x0 geometry and ground observations

        Parameters
        ----------
        da_cml: xarray.DataArray
            CML observations. Must contain the projected coordinates for the
            CML positions (site_0_x, site_0_y, site_1_x, site_1_y)
        da_gauge: xarray.DataArray
            gauge observations. Must contain the projected coordinates for the
            rain gauge positions (x, y)
        """
        # If CML and gauge data is provided
        if (da_cml is not None) and (da_gauge is not None):
            # Check that we have selected only one timestep
            if "time" in da_cml.coords:
                assert da_cml.time.size == 1, "Select only one time step"
            if "time" in da_gauge.coords:
                assert da_gauge.time.size == 1, "Select only one time step"

            # Stack instrument observations at cml and gauge in correct order
            observations_ground = np.concatenate(
                [da_cml.data.ravel(), da_gauge.data.ravel()]
            )

            # Stack x0_cml and x0_gauge in correct order
            x0 = np.vstack([self.x0_cml.data, self.x0_gauge.data])

        # If only CML data is provided
        elif da_cml is not None:
            # Check that we have selected only one timestep
            if "time" in da_cml.coords:
                assert da_cml.time.size == 1, "Select only one time step"

            # Get CML data
            observations_ground = da_cml.data.ravel()

            # Get CML coordinates
            x0 = self.x0_cml.data

        # If only rain gauge data is provided
        else:
            # Check that we have selected only one timestep
            if "time" in da_gauge.coords:
                assert da_gauge.time.size == 1, "Select only one time step"

            # Get gauge data
            observations_ground = da_gauge.data.ravel()

            # Get gauge coordinates
            x0 = self.x0_gauge.data

        # Return observations and coordinates
        return observations_ground, x0

    def get_grid_obs_x0_(self, da_grid, da_cml=None, da_gauge=None):
        """Calculate grid, ground observation and x0 for current state

        Returns and ordered list of the gridded data at the position of the
        ground observations, ground observations (CML and rain gauge) and the
        x0 geometry for the ground observations.

        Parameters
        ----------
        da_grid: xarray.DataArray
            Gridded rainfall data. Must contain the projected x_grid and Y_grid
            coordinates.
        da_cml: xarray.DataArray
            CML observations. Must contain the projected coordinates for the CML
            positions (site_0_x, site_0_y, site_1_x, site_1_y).
        da_gauge: xarray.DataArray
            Gauge observations. Must contain the projected coordinates for the rain
            gauge positions (x, y)
        """
        # If CML and gauge data is provided
        if (da_cml is not None) and (da_gauge is not None):
            # Check that we have selected only one timestep
            if "time" in da_grid.coords:
                assert da_grid.time.size == 1, "Select only one time step"
            if "time" in da_cml.coords:
                assert da_cml.time.size == 1, "Select only one time step"
            if "time" in da_gauge.coords:
                assert da_gauge.time.size == 1, "Select only one time step"

            if "time" not in da_grid.dims:
                da_grid = da_grid.copy().expand_dims("time")
            # Calculate grid along CMLs using intersect weights
            grid_cml = (
                plg.spatial.get_grid_time_series_at_intersections(
                    grid_data=da_grid,
                    intersect_weights=self.intersect_weights,
                )
            ).data.ravel()

            # Estimate grid at gauges
            grid_gauge = self.get_grid_at_points(
                da_gridded_data=da_grid,
                da_point_data=da_gauge,
            ).data.ravel()

            # Stack grid observations at cml and gauge in correct order
            grid_at_obs = np.concatenate([grid_cml, grid_gauge])

            # Stack instrument observations at cml and gauge in correct order
            observations_ground = np.concatenate(
                [da_cml.data.ravel(), da_gauge.data.ravel()]
            )

            # Stack x0_cml and x0_gauge in correct order
            x0 = np.vstack([self.x0_cml.data, self.x0_gauge.data])

        # If only CML data is provided
        elif da_cml is not None:
            # Check that we have selected only one timestep
            if "time" in da_grid.coords:
                assert da_grid.time.size == 1, "Select only one time step"
            if "time" in da_cml.coords:
                assert da_cml.time.size == 1, "Select only one time step"

            if "time" not in da_grid.dims:
                da_grid = da_grid.copy().expand_dims("time")
            # Estimate grid at cml
            grid_at_obs = (
                plg.spatial.get_grid_time_series_at_intersections(
                    grid_data=da_grid,
                    intersect_weights=self.intersect_weights,
                )
            ).data.ravel()

            # Get CML data
            observations_ground = da_cml.data.ravel()

            # Get CML coordinates
            x0 = self.x0_cml.data

        # If only rain gauge data is provided
        else:
            # Check that we have selected only one timestep
            if "time" in da_grid.coords:
                assert da_grid.time.size == 1, "Select only one time step"
            if "time" in da_gauge.coords:
                assert da_gauge.time.size == 1, "Select only one time step"

            # Estimate grid at gauges
            grid_at_obs = self.get_grid_at_points(
                da_gridded_data=da_grid,
                da_point_data=da_gauge,
            ).data.ravel()

            # Get gauge data
            observations_ground = da_gauge.data.ravel()

            # Get gauge coordinates
            x0 = self.x0_gauge.data

        # Return grid_at_observations, observations and coordinates
        return grid_at_obs, observations_ground, x0


# Functions for setting up x0 for gauges and CMLs
def calculate_cml_line(ds_cmls, discretization=8):
    """Calculate the position of points along CMLs.

    Calculates the discretized CML line coordinates by dividing the CMLs into
    discretization-number of intervals. The ds_cmls xarray object must contain the
    projected coordinates (site_0_x, site_0_y, site_1_x site_1_y) defining
    the start and end point of the CML.

    Parameters
    ----------
    ds_cmls: xarray.Dataset
        CML geometry as a xarray object. Must contain the coordinates
        (site_0_x, site_0_y, site_1_x site_1_y)
    discretization: int
        Number of intervals to discretize lines into.

    Returns
    -------
    x0: xr.DataArray
        Array with coordinates for all CMLs. The array is organized into a 3D
        matrix with the following structure:
            (number of n CMLs [0, ..., n],
             y/x-cooridnate [0(y), 1(x)],
             interval [0, ..., discretization])

    """
    # Calculate discretized positions along the lines, store in numy array
    xpos = np.zeros([ds_cmls.cml_id.size, discretization + 1])  # shape (line, position)
    ypos = np.zeros([ds_cmls.cml_id.size, discretization + 1])

    # For all CMLs
    for block_i, cml_id in enumerate(ds_cmls.cml_id):
        x_a = ds_cmls.sel(cml_id=cml_id).site_0_x.data
        y_a = ds_cmls.sel(cml_id=cml_id).site_0_y.data
        x_b = ds_cmls.sel(cml_id=cml_id).site_1_x.data
        y_b = ds_cmls.sel(cml_id=cml_id).site_1_y.data

        # for all dicretization steps in link estimate its place on the grid
        for i in range(discretization + 1):
            xpos[block_i, i] = x_a + (i / discretization) * (x_b - x_a)
            ypos[block_i, i] = y_a + (i / discretization) * (y_b - y_a)

    # Store x and y coordinates in the same array (n_cmls, y/x, discretization)
    x0_cml = np.array([ypos, xpos]).transpose([1, 0, 2])

    # Turn into xarray dataarray and return
    return xr.DataArray(
        x0_cml,
        coords={
            "cml_id": ds_cmls.cml_id.data,
            "yx": ["y", "x"],
            "discretization": np.arange(discretization + 1),
        },
    )


def calculate_cml_midpoint(da_cml):
    """Calculate DataArray with midpoints of CMLs

    Calculates the CML midpoints and stores the results in an xr.DataArray.
    The da_cml xarray object must contain the projected coordinates (site_0_x,
    site_0_y, site_1_x site_1_y) defining the start and end point of the CML.

    Parameters
    ----------
    da_cml: xarray.DataArray
        CML geometry as a xarray object. Must contain the coordinates
        (site_0_x, site_0_y, site_1_x site_1_y)

    Returns
    -------
    x0: xr.DataArray
        Array with midpoints for all CMLs. The array is organized into a 2D
        matrix with the following structure:
            (number of n CMLs [0, ..., n],
             y/x-cooridnate [y, x],
    """
    # CML midpoint coordinates as columns
    x = ((da_cml.site_0_x + da_cml.site_1_x) / 2).data
    y = ((da_cml.site_0_y + da_cml.site_1_y) / 2).data

    # CML midpoint coordinates as columns
    x0_cml = np.hstack([y.reshape(-1, 1), x.reshape(-1, 1)])

    # Create dataarray and return
    return xr.DataArray(
        x0_cml,
        coords={
            "cml_id": da_cml.cml_id.data,
            "yx": ["y", "x"],
        },
    )


def calculate_gauge_midpoint(da_gauge):
    """Calculate DataArray with coordinates of raingauge

    Calculates the gauge coordinates and stores the results in an xr.DataArray.
    The da_gauge xarray object must contain the projected coordinates (y, x)
    defining the position of the raingauge.

    Parameters
    ----------
    da_gauge: xarray.DataArray
        Gauge coordinate as a xarray object. Must contain the coordinates (y, x)

    Returns
    -------
    x0: xr.DataArray
        Array with coordinates for all gauges. The array is organized into a 2D
        matrix with the following structure:
            (number of n gauges [0, ..., n],
             y/x-cooridnate [y, x],
    """
    x0_gauge = np.hstack(
        [
            da_gauge.y.data.reshape(-1, 1),
            da_gauge.x.data.reshape(-1, 1),
        ]
    )

    # Create dataarray return
    return xr.DataArray(
        x0_gauge,
        coords={
            "id": da_gauge.id.data,
            "yx": ["y", "x"],
        },
    )
