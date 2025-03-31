#! usr/bin/env python3
#  -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

"""
NoLOAD_Jax installation script
:version: 1.4.0
"""

from setuptools import setup, find_packages

# ------------------------------------------------------------------------------

# Module version
__version_info__ = (1, 4, 0)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
#__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------------


setup(

    name='noloadj',
    version=__version__,
    packages=["noloadj",
              "noloadj.analyse",
              "noloadj.gui",
              "noloadj.numerical_methods",
              "noloadj.numerical_methods.ODE",
              "noloadj.numerical_methods.interpolation",
              "noloadj.optimization",
              "noloadj.tutorial",
              ],
    author="B. DELINCHANT, L. GERBAUD, F. WURTZ, L.AGOBERT",
    author_email='benoit.delinchant@G2ELab.grenoble-inp.fr',
    description="solving constrained optimization problem for the design of engineering systems",
    long_description_content_type='text/markdown',
    long_description=open('README.md',encoding='UTF-8').read(),
    install_requires=[
        "Matplotlib >3.0",
        "Scipy >= 1.2",
        "Jax >= 0.4.18",
        "Jaxlib >= 0.4.18",
        "Pandas >= 1.3.5",
        "tk >= 0.1.0",
        "Openpyxl >= 3.1.2"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],

)
