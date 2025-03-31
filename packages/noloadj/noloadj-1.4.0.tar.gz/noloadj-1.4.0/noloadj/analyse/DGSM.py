# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from scipy.stats import qmc
from jax import jacfwd,jit,config
from noloadj.optimization.Tools import StructList
from typing import Callable, Dict, List, Any
from pandas import DataFrame as df
import numpy as np,sys
import jax.numpy as jnp
config.update("jax_enable_x64", True)

'''Derivative-based Global Sensitivity Measure'''

def computeDGSM(model: Callable[..., Dict], inputs: Dict[str, Any],
                outputs: List[str], deltas:Dict[str,Any],
                deltas_type:Dict[str,Any],N:int,Param: Dict[str, Any]={}):
    '''
    Compute DGSM (Derivative-based Global Sensitivity Measure) of a model.

    :param model: model
    :param inputs: dict: names and initial values of derivable input variables
    :param outputs: list: names of output variables
    :param deltas: dict: variation of derivable input variables
    :param deltas_type: dict: type of variation for each derivable input ('rel' for relative or 'abs' for absolute)
    :param N: int: number of points to compute DGSM. Must be a power of 2.
    :param Param: names and values of non-derivable input variables (dictionary)
    :return: dataframe : DGSM
    '''
    if int(bin(N)[3:])!=0: # test si N est une puissance de 2
        print('Warning :', N, 'is not a power of 2 (512, 1024, 2058, ...)')
        sys.exit(0)

    m = int(np.log(N) / np.log(2.)) # 2^(m)=N

    inputs_names,init_values=list(inputs.keys()),list(inputs.values())
    len_inputs,len_outputs=len(inputs_names),len(outputs)

    vi=np.empty((len_inputs,len_outputs))
    var=np.empty((len_inputs,len_outputs))
    b_a={}

    sampler = qmc.Sobol(d=len_inputs, scramble=False) 
    sample = sampler.random_base2(m=m) # création des échantillons [0,1]
    l_bounds,u_bounds=[],[]

    for input in inputs_names:
        index_input=inputs_names.index(input)
        if deltas_type[input]=='abs':
            l_bounds.append(init_values[index_input]-deltas[input])
            u_bounds.append(init_values[index_input]+deltas[input])
            b_a[input]=2.*deltas[input]
        elif deltas_type[input]=='rel':
            l_bounds.append(init_values[index_input]-deltas[input]*
                            init_values[index_input])
            u_bounds.append(init_values[index_input]+deltas[input]*
                            init_values[index_input])
            b_a[input]=init_values[index_input]*((1.+deltas[input])-(
                    1.-deltas[input]))

    scale_samples=qmc.scale(sample, l_bounds,u_bounds).T # mise à échelle des échantillons

    for input in inputs_names:
        index_input=inputs_names.index(input)
        inputs[input] = scale_samples[index_input]
                                  
    outputs_values = computeParametricValue(model,inputs,outputs,N,Param) # évaluation modèle N fois
    variances=np.var(outputs_values,axis=1) # calcul des variances de chaque sortie
    
    jac_values=computeParametricJacobian(model,inputs,outputs,N,Param) # gradients modèle N fois

    for input in inputs_names:
        index_input=inputs_names.index(input)

        for j in range(len_outputs):
            vi[index_input][j]=np.mean(jac_values[j*len_inputs+index_input]**2)
            var[index_input][j]=b_a[input]*b_a[input]/(np.pi*np.pi*variances[j])

    dgsm=df(vi*var,index=inputs_names,columns=outputs)

    return dgsm


def computeParametricValue(model:Callable[...,Dict],inputs_range: Dict[str,Any],
                      outputs: List[str],N:int,Param: Dict[str, Any]={}):
                      
    outputs_values=np.empty((N,len(outputs)))
    inputs={}
    
    for i in range(N):
        for key in list(inputs_range.keys()):
            inputs[key]=inputs_range[key][i]
        if Param!={}:
            res = model(**inputs,**Param)
        else:
            res = model(**inputs)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        out=[]
        nans_vars = []
        for vars in outputs:
            try:
                if vars not in list(dico.keys()):
                    raise KeyError(vars) #si la variable du cahier des charges
                if jnp.all(jnp.isnan(dico[vars])):
                    raise ValueError(vars)
            except KeyError: # n'appartient pas aux sorties du modèle
                print('Warning :',vars,'is not in model')
                sys.exit(0)
            except ValueError:
                nans_vars.append(vars)
            else:
                out.append(dico[vars])
        if nans_vars != []:
            print('Warning :', nans_vars, 'is Nan')
            sys.exit(0)
        outputs_values[i]=out

    return np.transpose(outputs_values)


def computeParametricJacobian(model:Callable[...,Dict], inputs_range:
            Dict[str,Any],outputs: List[str],N:int,Param: Dict[str, Any]={}):

    outputsjac_values=np.empty((N,len(outputs)*len(inputs_range)))
    inputs={}

    def eval_model(array_inputs):
        if Param!={}:
            res = model(*array_inputs,**Param)
        else:
            res = model(*array_inputs)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        out = []
        nans_vars = []
        for vars in outputs:
            try:
                if vars not in list(dico.keys()):
                    raise KeyError(vars)  # si la variable du cahier des charges
                #if jnp.all(jnp.isnan(dico[vars])):
                #    raise ValueError(vars)
            except KeyError:  # n'appartient pas aux sorties du modèle
                print('Warning :', vars, 'is not in model')
                sys.exit(0)
            #except ValueError:
            #    nans_vars.append(vars)
            else:
                out.append(dico[vars])
        if nans_vars != []:
            print('Warning :', nans_vars, 'is Nan')
            sys.exit(0)
        return out

    eval_model_jit=jit(eval_model)
    
    for i in range(N):
        for key in list(inputs_range.keys()):
            inputs[key]=inputs_range[key][i]

        array_inputs=jnp.array(list(inputs.values()))
        out=jacfwd(eval_model_jit)(array_inputs)
        outputsjac_values[i]=Flatten(out)

    return np.transpose(outputsjac_values)

def Flatten(vector):
    res=[]
    for i in range(len(vector)):
        for j in range(len(vector[i])):
            res.append(vector[i][j])
    return res