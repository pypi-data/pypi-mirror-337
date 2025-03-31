# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from noloadj.analyse.Sobol import computeSobol
from noloadj.analyse.simulation import computeOnce,computeJacobian,\
    computeParametric
from noloadj.analyse.DGSM import computeDGSM
import numpy as np
import jax.numpy as jnp

def rosenbrock(x,y):
    fobj=(1-x)*(1-x)+100*(y-x*x)**2
    ctr1=(x-1)**3-y+1
    ctr2=x+y-2
    return locals().items()

def Ishigami(x1,x2,x3,A,B):
    Y=jnp.sin(x1)+A*jnp.sin(x2)*jnp.sin(x2)+B*jnp.sin(x1)*(x3**4)
    return locals().items()


# Compute outputs
inputs = {'x': 1.0, 'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']
results = computeOnce(model=rosenbrock, inputs=inputs, outputs=outputs)
print(outputs, '=', results)


# Compute Parametric
inputs = {'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']

variable = 'x'
values = np.arange(-1.5, 1.5, 0.1)  # [-1.5, -1.4, ..., 1.5]
iter = computeParametric(rosenbrock, variable, values, inputs, outputs)

df = iter.print()
print(df)
iter.plotXY()

# Compute Gradients
inputs = {'x': 1.0, 'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']
dfobj,dctr1,dctr2 = computeJacobian(model=rosenbrock, inputs=inputs,
                                    outputs=outputs)
print('dfobj =', dfobj)
print('dctr1 =', dctr1)
print('dctr2 =', dctr2)

# Compute DGSM
inputs = {'x1': 0., 'x2': 0., 'x3': 0.}
deltas = {'x1': jnp.pi, 'x2': jnp.pi, 'x3': jnp.pi}
deltas_type = {'x1': 'abs', 'x2': 'abs', 'x3': 'abs'}
outputs = ['Y']
Param = {'A': 7., 'B': 0.1}
DGSM = computeDGSM(model=Ishigami, inputs=inputs, outputs=outputs,
                   deltas=deltas, deltas_type=deltas_type, N=1024,Param=Param)
print('DGSM=', DGSM)

# Compute Sobol 1st-order indices
inputs = {'x1': 0., 'x2': 0., 'x3': 0.}
deltas = {'x1': jnp.pi, 'x2': jnp.pi, 'x3': jnp.pi}
deltas_type = {'x1': 'abs', 'x2': 'abs', 'x3': 'abs'}
outputs = ['Y']
Param = {'A': 7., 'B': 0.1}
Sobol = computeSobol(model=Ishigami, inputs=inputs, outputs=outputs,
                   deltas=deltas, deltas_type=deltas_type, N=1024,Param=Param)
print('Sobol=',Sobol)

