# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from noloadj.optimization.iterationHandler import Iterations
from typing import Callable, Dict, List, Any
import numpy,sys
from jax import config
config.update("jax_enable_x64", True)
import jax.numpy as jnp

'''computes model with the inputs dictionnary, and give the value of output 
variables'''
def computeOnce(model: Callable[..., Dict], inputs: Dict[str, Any],
                outputs: List[str]):
    """
    Computes the outputs of the model according to the values of the given
    input variables.

    :param model: model
    :param inputs: names and values of input variables (dictionary)
    :param outputs: names of output variables (list)
    :return: values of the outputs (list)
    """
    res = model(**inputs)
    dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
    out=[]
    nans_vars=[]
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
    # sauvegarde et tracé des résultats uniquement si appel à la fonction et
    # non au gradient
    if nans_vars!=[]:
        print('Warning :',nans_vars,'is Nan')
        sys.exit(0)
    for i in range(len(out)): # POUR RETIRER LES DEVICE ARRAY
        if numpy.size(out[i])==1:
            out[i]=float(out[i])
        #else:
        #    for j in range(len(out[i])):
        #        out[i][j]=float(out[i][j])
    return out

#TODO : Harmoniser les résultats avec ceux d'une optimisation pour le tracé
# des itérations
'''computes model with the inputs dictionnary and a variable input varying in 
a range, and give the value of output variables'''
def computeParametric(model: Callable[..., Dict], variable: str,
                      range: List[float], inputs: Dict[str, Any],
                      outputs: List[str]):
    """
    Computes the outputs of the model corresponding to the values of the given
    input variables, except one varying in a range of values.

    :param model: model
    :param variable: the input that varies
    :param range: range of values in which the input varies
    :param inputs: names and values of constant input variables (dictionary)
    :param outputs: names of output variables (list)
    :return: values of the outputs (list)
    """
    iter = Iterations(None,[variable], outputs)  # permet de sauvegarder les
    # résultats au fur et à mesure (optionnel)
    for x in range:
        if inputs!=[]:
            res = model(**{variable: x}, **inputs)
        else:
            res = model(*x) # in case of model with only 1 argument
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
        # sauvegarde et tracé des résultats uniquement si appel à la fonction et
        # non au gradient
        if nans_vars != []:
            print('Warning :', nans_vars, 'is Nan')
            sys.exit(0)
        iter.updateData([x], out)
    return iter


from jax import jacfwd

def computeJacobian(model: Callable[..., Dict], inputs: Dict[str, Any],
                      outputs: List[str],Param: Dict[str, Any]={}):
    """
    Displays gradients of outputs corresponding to the values of
    the given inputs.

    :param model: model
    :param inputs: names and values of derivable input variables (dictionary)
    :param outputs: names of output variables (list)
    :param Param: names and values of non-derivable input variables (dictionary)
    :return: gradients of the outputs (list)
    """
    inputs_keys=list(inputs.keys())
    inputs_values=list(inputs.values())
    def eval_model(inputs_values):
        xList=dict(zip(inputs_keys,inputs_values))
        if Param!={}:
            res = model(**xList,**Param)
        else:
            res = model(**xList)
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
        return out

    nans_vars = []
    dout=jacfwd(eval_model)(inputs_values)
    for i in range(len(dout)): # POUR RETIRER LES DEVICE ARRAY
        for j in range(len(dout[i])):
            if numpy.size(dout[i][j])==1:
                dout[i][j]=float(dout[i][j])
            else:
                for k in range(len(dout[i][j])):
                    dout[i][j][k]=float(dout[i][j][k])
        try:
            if numpy.all(numpy.isnan(dout[i])):
                raise ValueError(i)
        except ValueError:
            nans_vars.append(outputs[i])
    if nans_vars!=[]:
        print('Warning :', nans_vars, 'is Nan')
        print('in Gradient Computation')
        sys.exit(0)
    return dout