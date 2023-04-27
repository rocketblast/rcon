from setuptools import setup, find_namespace_packages
import os
import glob

datadir = os.path.join('data')
data_files = [(datadir, [f for f in glob.glob(os.path.join(datadir, '*'))])]

setup(
    name = 'Rocket Blast RCON',
    version = '0.2.0',
    # maintainer = '',
    # maintainer_email = '',
    author = 'Martin Danielson',
    author_email = 'martin@rocketblast.com',
    long_description = open("README.md").read(),
    keywords = 'rcon battlefield game servers socket connection',
    description = 'Library to connect to game servers over rcon protcol (Battlefield)',
    license = 'GNU Affero GPL v3',
    # platforms = '',
    url = 'https://github.com/rocketblast/rcon',
    download_url = 'https://github.com/rocketblast/rcon/downloads',
    classifiers = '',

    packages=find_namespace_packages(include=['rocketblast.*']),

    install_requires = [],
    # uncomment if you have share/data files
    #data_files = data_files,

    #use_2to3 = True, # causes issue with nosetests
)
