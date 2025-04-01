# Description

Python package of utility functions that are useful in analyzing various datasets, in particular, catalogs of particles or galaxies/halos from cosmological simulations. (The GizmoAnalysis and HaloAnalysis packages depend on this package.)


---
# Requirements

python 3, numpy, scipy, h5py, matplotlib


---
# Content

## lower-level utilities

### array.py 
* create, manipulate, analyze arrays

### binning.py
* binning of array data

### constant.py
* physical constants and unit conversions

### coordinate.py
* manipulate positions and velocities

### io.py
* read, write, print during run time

### math.py 
* math, statistics, and fitting

### plot.py
* supplementary functions for plotting with matplotlib


## higher-level utilities

### catalog.py
* analyze catalogs of halos/galaxies

### cosmology.py
* calculate cosmological values, including cosmic density, distance, age, volume

### halo_property.py
* calculate halo properties at different radii, convert between virial definitions

### orbit.py
* compute orbital quantities such as peri/apo-centric distance, orbital time, in a given gravitational potential

### particle.py
* high-level analysis of N-body particle data

### simulation.py
* tools to help set up and run a simulation


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


The easiest way to install this packages is by using `pip`:

```
python -m pip install utilities_awetzel

```

Alternately, to install the latest stable version from source, clone from `bitbucket`:

```
git clone git://bitbucket.org/awetzel/utilities.git
```

then either point your PYTHONPATH to this repository or you build and install this project via pip by going inside the top-level `utilities` directory and:

```
python -m pip install .
```


---
# Using

Once installed, you can use individual modules like this:

```
import utilities as ut
ut.particle
```
