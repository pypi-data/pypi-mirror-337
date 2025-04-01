'''
Default names and values for files and directories used throughout this package.
If you prefer a different default, change it here, and it should propagate througout the package.
Some names have wildcards, such as '*', or '!', these represent name bases, generally for finding
any/all such files in a directory via glob.

@author: Andrew Wetzel <arwetzel@gmail.com>
'''

# base directory of a simulation
# setting to '.' assumes that you are running analysis from within a simulation directory
simulation_directory = '.'

# directory of all halo files, typically the first directory within simulation_directory
halo_directory = 'halo/'

# directory of all rockstar files (needs to include root halo_directory if within it)
rockstar_directory = halo_directory + 'rockstar_dm/'

# directory of rockstar raw text files, within rockstar_directory
rockstar_catalog_directory = 'catalog/'

# directory of rockstar processed hdf5 files, within rockstar_directory
rockstar_catalog_hdf5_directory = 'catalog_hdf5/'

# directory of rockstar processed hdf5 files
rockstar_job_directory = 'rockstar_jobs/'

# default subset of 64 snapshots indices on which to run halo finder and particle assignment
# relevant for FIRE-2 (not FIRE-3) snapshots
snapshot_indices_subset = [
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
    600,  # z = 0
]
