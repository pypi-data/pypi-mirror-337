# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from scipy.stats import qmc,norm
from jax import config
from noloadj.analyse.DGSM import computeParametricValue,computeParametricJacobian
from typing import Callable, Dict, List, Any
from pandas import DataFrame as df
import numpy as np,sys
config.update("jax_enable_x64", True)

'''1st_order Sobol indices'''

def computeSobol(model: Callable[..., Dict], inputs: Dict[str, Any],
                outputs: List[str], deltas:Dict[str,Any],
                deltas_type:Dict[str,Any],N:int,Param: Dict[str, Any]={}):
    '''
    Compute 1st-order Sobol indices of a model.

    :param model: model
    :param inputs: dict: names and initial values of derivable input variables
    :param outputs: list: names of output variables
    :param deltas: dict: variation of derivable input variables
    :param deltas_type: dict: type of variation for each derivable input ('rel' for relative or 'abs' for absolute)
    :param N: int: number of points to compute DGSM. Must be a power of 2.
    :param Param: names and values of non-derivable input variables (dictionary)
    :return: dataframe : Sobol indices
    '''
    if int(bin(N)[3:])!=0: # test si N est une puissance de 2
        print('Warning :', N, 'is not a power of 2 (512, 1024, 2058, ...)')
        sys.exit(0)

    inputs_names,init_values=list(inputs.keys()),list(inputs.values())
    len_inputs,len_outputs=len(inputs_names),len(outputs)
    step=2*len_inputs+2
    nb=int(step*N)

    Si=np.empty((len_inputs,len_outputs))

    sampled=sample(len_inputs,N) #= qmc.Sobol(d=len_inputs, scramble=False).random(nb) # création des échantillons [0,1]
    l_bounds,u_bounds=[],[]

    for input in inputs_names:
        index_input=inputs_names.index(input)
        if deltas_type[input]=='abs':
            l_bounds.append(init_values[index_input]-deltas[input])
            u_bounds.append(init_values[index_input]+deltas[input])
        elif deltas_type[input]=='rel':
            l_bounds.append(init_values[index_input]-deltas[input]*
                            init_values[index_input])
            u_bounds.append(init_values[index_input]+deltas[input]*
                            init_values[index_input])

    scale_samples=qmc.scale(sampled, l_bounds,u_bounds).T # mise à échelle des échantillons

    for input in inputs_names:
        index_input=inputs_names.index(input)
        inputs[input] = scale_samples[index_input]
                                  
    outputs_values = computeParametricValue(model,inputs,outputs,nb,Param) # évaluation modèle nb fois

    for j in range(len_outputs):
        out=outputs_values[j]
        out=(out-np.mean(out))/np.std(out)
        A=out[0:nb:step]
        B=out[step-1:nb:step]
        var=np.var(np.r_[A, B])
        for i in range(len_inputs):
            AB=out[i+1:nb:step]
            res=B*(AB-A)
            Si[i,j]=np.mean(res)/var

    Sobol=df(Si,index=inputs_names,columns=outputs)

    return Sobol


def sample(len_inputs,N):
    base_sequence = qmc.Sobol(d=2*len_inputs).random(N)
    sobol_sequence = np.zeros([(2*len_inputs + 2) * N, len_inputs])
    index = 0

    for i in range(N):
        for j in range(len_inputs):
            sobol_sequence[index,j] = base_sequence[i,j]
        index += 1

        for k in range(len_inputs):
            for j in range(len_inputs):
                if j == k:
                    sobol_sequence[index,j] = base_sequence[i,j+len_inputs]
                else:
                    sobol_sequence[index,j] = base_sequence[i,j]
            index += 1

        for k in range(len_inputs):
            for j in range(len_inputs):
                if j == k:
                    sobol_sequence[index,j] = base_sequence[i,j]
                else:
                    sobol_sequence[index,j] = base_sequence[i,j+len_inputs]

            index += 1

        for j in range(len_inputs):
            sobol_sequence[index,j] = base_sequence[i,j+len_inputs]
        index += 1

    return sobol_sequence
