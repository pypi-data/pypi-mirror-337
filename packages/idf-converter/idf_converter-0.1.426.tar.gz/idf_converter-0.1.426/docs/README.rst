IDF converter is a set of Python tools to convert satellite, in-situ and
numerical model data into Intermediary Data Format, i.e. self-contained,
CF-compliant NetCDF files that are easier to analyse than the original files.

The IDF files produced by the converter can also be visualised using SEAScope,
a viewer which offers advanced rendering functionalities that ease the
detection of synergies between several sources of observations and simulations
(available on Linux, Windows and macOS).

For more information about the Intermediate Data Format (IDF), please read the
`IDF specifications document`_

You can download SEAScope and some examples of IDF files on the
`SEAScope website`_.

.. _IDF specifications document: https://seascope.oceandatalab.com/docs/idf_specifications_1.5.pdf
.. _SEAScope website: https://seascope.oceandatalab.com


Changelog
=========

0.1.426 (2025-03-31)
--------------------

* The ``swot/L3`` reader now supports variable name changes introduced in v2.0
  of the SWOT L3 products.

* A ``postprocessor`` output option has been added to allow a hook to be called
  just before the IDF content is written in a file. The syntax is the same as
  for hooks that modify/add output variables (the method to call is defined
  with the ``using`` keyword). This option is meant for advanced users who want
  to exploit IDF content without writing data as NetCDF file (for memory-only
  uses, serialization in another format, integration in a GIS, etc...)

* The output option ``id_suffix`` now behaves as expected when it is set to
  ``INPUT_FILENAME``.

0.1.419 (2024-08-27)
--------------------

* Min and max values defined for the flag masking mechanism are now cast to the
  same type as the flag variable.

* The ``sentinel3/olci/L2`` reader now accepts a ``mask_low_specular_angle``
  option to mask values based on the specular angle. By default the option is
  disabled, but it can be set to ``yes`` so that variables ``CHL_NN``,
  ``CHL_OC4ME``, ``KD490`` and ``KD490_M07`` are masked where the specular
  angle is strictly below 9°.
  The value of this option can also be set to ``MIN_ANGLE:VAR1[, VAR2, ...]``,
  where ``MIN_ANGLE`` is the specular angle value below which data will be
  masked, and ``VAR1[, VAR2, ...]`` is a comma-separated list of variable names
  on which the mask must be applied.

* The ``swot/L3`` reader now supports "unsmoothed" input files with a 250m
  spatial resolution. The ``roughness`` and ``ssha_unedited_nolr`` variables
  can be requested for these files by including these identifiers in the
  ``variables`` input option (the converter will compute them from the
  ``sigma0`` and ``ssha_unedited`` variables).

* Support for Python 3.12 has been added.

0.1.394 (2024-02-09)
--------------------

* Sentinel-1 L1 GeoTIFF files are now explicitly accessed with read-only
  permissions. In some cases the reader tried to read these files using
  ``tifffile.memmap`` which uses read-write permissions by default, causing
  problems when opening archived files.

* Readers for Sentinel-1 L2 data (``sentinel1/L2/owi`` and
  ``sentinel1/L2/rvl``) now consider input files that do not include an
  ``IPFversion`` global attribute as having an IPF version < 3.40, therefore
  the temporal coverage is extracted from the SAFE name instead of the
  ``firstMeasurementTime`` and ``lastMeasurementTime`` global attributes.

* Limitations and workarounds related to the size of the along-track dimension
  have been removed for Sentinel-3 SRAL 20Hz (``sentinel3/sral/L2``) and
  Sentinel-6 P4 L2 (``sentinel6/p4/L2``).

* Rain mask computation in ``sentinel6/p4/L2`` reader was incorrect and has
  been fixed.

* Generic reader for NetCDF lat/lon regular grids (``netcdf/grid/latlon``) has
  been modified to translate geographical boundaries expressed with the
  ``easternmost_longitude``, ``westernmost_longitude``,
  ``northernmost_latitude`` and ``southernmost_latitude`` global attributes
  into their equivalent in IDF specifications (i.e. ``geospatial_lon_max``,
  ``geospatial_lon_min``, ``geospatial_lat_max`` and ``geospatial_lat_min``).
  If these attributes cannot be parsed as finite floating point numbers, the
  reader will act as if they were not defined.

* ``remove_out_of_bounds_coordinates`` output option added to generic reader for
  NetCDF lat/lon regular grids (``netcdf/grid/latlon``). When this option is
  set to "yes", the reader will ignore rows and columns of the input file if
  their location is outside the geographical boundaries defined in the global
  attributes.

* The generic readers for NetCDF regular grids (``netcdf/grid/latlon`` and
  ``netcdf/grib/yx``) now support input files with time variables containing
  some masked values. Data associated with the masked time values will be
  ignored.

* Support for shifting rows/columns has been improved in generic readers for
  NetCDF regular grids (``netcdf/grid/latlon`` and ``netcdf/grib/yx``).

* Reader ``osisaf/sic`` has been renamed ``osisaf/l3/sic``. It has also been
  adapted to read temporal coverage from the input file and to support the
  latest version of the OSI-SAF L3 sea ice concentration products.

* Reader ``cmems/drifter`` has been adapted to support format changes
  introduced in the CMEMS 013 048 product on November 2023.

* Reader ``swot/L3`` added to convert SWOT L3 data samples released by CNES.

* RMax value is now included in the IDF output when converting IBTrACS data
  (version tailored for the MAXSS ESA project) with the ``ìbtracs`` reader.

* An extraneous invalid time values was previously processed in the reader for
  World Ocean Atlas 2018 monthly data (``woa/monthly``). It is not the case
  anymore.

* Datetime parsing method now supports cases wherein a space precedes the "Z"
  timezone indicator.

* Code involving ``scipy`` has been modernized to fix deprecation warnings.

* Many changes through the codebase to handle underflows and other numerical
  errors reported in recent of Numpy.

* Code does not support breaking changes introduced in ``shapely`` 2.0, package
  dependencies have been adapted accordingly.

* Checks performed on NetCDF version when writing time-dependent IDF files
  (trajectories, altimeter traces, ...) did not support version names
  containing dashes, it has been fixed.

* No warning was issued when creating IDF files using the swath data model if
  the requested density for GCPs along the cell axis exceeded the density of
  the geolocation information in the input file. The problem is now correctly
  reported to the user.

0.1.333 (2023-02-20)
--------------------

* Sentinel-3 SRAL L2 reader failed to convert 20Hz data because the brightness
  temperature variables are only available at 1Hz. The reader has been adapted
  to skip these variables when converting 20Hz data.

* The underflow workaround in the downscaling process would only work if all
  values were positive due to a typo, it has been fixed.

0.1.330 (2023-02-10)
--------------------
* Support added for brightness temperature variables in the Sentinel-3 SRAL L2
  reader.

* Reader for Sentinel-3 OLCI L2 Chlorophyll-a data did not interpret flags
  correctly for data generated after February 2021 (baseline 003), it has been
  adapted to support these data too.

* The transform method for computing an anomaly based on a climatology file has
  a new "interpolate" boolean option: when set to False the converter will
  consider that the climatology file is defined on the same grid as the file to
  convert (interpolating the climatology file is costly in terms of memory, so
  performing this interpolation once as a pre-processing step can save a lot of
  resources when converting many files with the same grid, images from
  geostationnary satellites for example).

* Compression options were only applied to the full resolution IDF, the
  converter now also applies them to the downscaled IDFs.

* Minimal version for the netCDF4 dependency set to 1.6.0 and above (required
  for propagating compression options).

* Bugfix for underflow errors that may arise in the downscaling process.

0.1.312 (2022-10-06)
--------------------

* Readers for Sentinel-1 L2 data have been modified to include the name of the
  L2 SAFE as a global attribute (named L2_SAFE) in the output IDF file. This
  only applies when the input file was located in a directory layout matching
  the SAFE specifications.

0.1.309 (2022-10-03)
--------------------

* Readers for Sentinel-1 L2 data have been modified to avoid naming conflicts
  for granules from the same datatake and inaccurate temporal coverage for
  files generated with versions of the Instrument Processing Facility (IPF)
  below 3.40.

0.1.308 (2022-09-09)
--------------------

* Initial version
