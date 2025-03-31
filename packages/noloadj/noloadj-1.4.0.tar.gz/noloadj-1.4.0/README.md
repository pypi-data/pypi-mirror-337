<!--
SPDX-FileCopyrightText: 2021 G2Elab / MAGE

SPDX-License-Identifier: Apache-2.0
-->

NoLOAD_Jax: Non Linear Optimization by Automatic Differentiation using Jax
==========================================================================

We are happy that you will use or develop the NoLOAD_Jax.
It is an **Open Source** project located on GitLab at https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2
It aims at **solving constrained optimization** problem for the design of engineering systems

Project Presentation
====================

**NoLOAD_Jax:** Please have a look to NoLOAD presentation : https://noload-jax.readthedocs.io/en/latest/

A scientific article presenting NoLOAD is available here:

Agobert Lucas, Hodencq Sacha, Delinchant Benoit, Gerbaud Laurent, Frederic Wurtz, “NoLOAD, Open Software for Optimal Design and Operation using Automatic Differentiation”, OIPE 2020, Poland, 09-2021. https://hal.archives-ouvertes.fr/hal-03352443

Please cite us when you use NoLOAD.

NoLOAD_Jax Community
====================

Please use the git issues system to report an error: https://gricad-gitlab.univ-grenoble-alpes.fr/design_optimization/NoLoad_v2
Otherwise you can also contact the developer team using the following email adress: benoit.delinchant@G2ELab.grenoble-inp.fr

Installation Help
=================
You can install the library as a user or as a developer. Please follow the corresponding installation steps below.

Prerequisite
------------

Please install Python 3.10 or later
https://www.python.org/downloads/


Installation as a user
----------------------
Please install NoLOAD_Jax with pip using the command prompt.   

If you are admin on Windows or working on a virtual environment
    
    pip install noloadj

If you want a local installation or you are not admin
    
    pip install --user noloadj

If you are admin on Linux:
    
    sudo pip install noloadj

Launch the examples to understand how the NoLOAD_Jax works:
	
	python noloadj/01-UnconstrainedMonoObjective.py
	python noloadj/02-ConstrainedMonoObjective.py
	python noloadj/03-ConstrainedMultiObjective.py
	python noloadj/04-ConstrainedMonoObjective2.py
	
Enjoy your time using NoLOAD_Jax !

GPU 
---
As it uses the JAX library, NoLOAD_Jax can run on CPU (Central Processor Unit) or GPU (Graphics Processor Unit), where GPU offers better performances than CPU.
On Windows, only CPU can be used. To use GPU you may run NoLOAD on Ubuntu.
If you want to use GPU, you need to install CUDA and CuDNN on your computer then write on Pycharm terminal :

    pip install --upgrade pip
    pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
    
If you use GPU, you need to put these lines at the beginning of your "optimization" file to avoid memory issues :

    import os
    os.environ['XLA_PYTHON_CLIENT_PREALLOCATE']='false'
    os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION']='0.50'
    
To have more information, please have a look to :  https://jax.readthedocs.io/en/latest/installation.html 


IPOPT Algorithm
---------------
NoLOAD_Jax runs with SLSQP optimization algorithm from Scipy.
To install IPOPT algorithm, please install an Anaconda environment and run this command on a terminal :

    conda install -c conda-forge cyipopt

Library Installation Requirements
---------------------------------
Matplotlib >= 3.0
Scipy >= 1.2
Jax >= 0.4.18
Jaxlib >= 0.4.18
Pandas >= 1.3.5
tk >= 0.1.0
openpyxl >= 3.1.2


Main Authors: 
=============
B. DELINCHANT, L. GERBAUD, F. WURTZ, L. AGOBERT


Partners:
=========
Vesta-System: http://vesta-system.fr/

Acknowledgments:
================


Licence
=======
This code is under the Apache License, Version 2.0
