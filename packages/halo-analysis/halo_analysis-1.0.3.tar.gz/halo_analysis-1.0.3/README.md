# Description

Python package to read and analyze halo/galaxy catalogs (generated from Rockstar or AHF) and merger trees (generated from ConsistentTrees).


---
# Requirements

python 3, numpy, scipy, h5py, matplotlib

This package also requires the [utilities/](https://bitbucket.org/awetzel/utilities) Python package for various utility functions.


---
# Contents

## halo_analysis

### halo_io.py
* read halo files, convert from text to hdf5 format, assign particle species to dark-matter halos

### halo_plot.py
* analyze and plot halos/galaxies

### halo_select.py
* select halos from large simulations for generating initial conditions for zoom-in


## tutorials

### halo_tutorial.ipynb
* Jupyter notebook tutorial for using this package


## data

### snapshot_times.txt
* example file for storing information about snapshots: scale-factors, redshifts, times, etc


---
# Units

Unless otherwise noted, this package stores all quantities in (combinations of) these base units

* mass [M_sun]
* position [kpc comoving]
* distance, radius [kpc physical]
* time [Gyr]
* temperature [K]
* magnetic field [Gauss]
* elemental abundance [linear mass fraction]

These are the common exceptions to those standards

* velocity [km/s]
* acceleration [km/s / Gyr]
* gravitational potential [km^2 / s^2]
* rates (star formation, cooling, accretion) [M_sun / yr]
* metallicity (if converted from stored massfraction) [log10(mass_fraction / mass_fraction_solar)], using Asplund et al 2009 for Solar


---
# Installing

The easiest way to install this packages and all of its dependencies is by using `pip`:

```
python -m pip install halo_analysis
```

Alternately, to install the latest stable version from source, clone from `bitbucket`, in one of two ways:

1) either using HTTPS:

```
git clone https://bitbucket.org/awetzel/halo_analysis.git
```

2) or using SSH:

```
git clone git://bitbucket.org/awetzel/halo_analysis.git
``` 

Then do one of the following:

1) either point your PYTHONPATH to this repository (and also install and point PYTHONPATH to the [utilities/](https://bitbucket.org/awetzel/utilities) repository that it depends on)

2) or build and install this project via pip by going inside the top-level `halo_analysis/` directory and doing:

```
python -m pip install .
```


---
# Using

Once installed, you can use individual modules like this:

```
import halo_analysis as halo
halo.io
```


---
# Citing

If you use this package, please cite it, along the lines of: 'This work used HaloAnalysis (http://ascl.net/2002.014), which first was used in Wetzel et al. 2016 (https://ui.adsabs.harvard.edu/abs/2016ApJ...827L..23W).'
