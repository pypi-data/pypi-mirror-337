# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0
import jax.numpy as jnp
import numpy as np
import jax
from jax import custom_jvp
from functools import partial

'''To deal with constraints'''
class StructList:
    """
    Attributes :

    - List : list of all scalar/vector constraints
    - shape = list containing the sizes of the vectors of the different constraints (0 if scalar, from 1 if vector)
    - etat = string indicating if the list has already been flattened or not (unflattened)

    When creating an object of the class, if the state of the list is 'unflattened', the shape vector is calculated automatically. Otherwise it must be provided when creating the object.
    """
    # List = None # liste regroupant l'ensemble des contraintes scalaires et/ou
    # # vectorielles
    # shape = [] # liste regroupant les tailles des vecteurs des différentes
    # # contraintes (0 si scalaire, à partir de 1 si vectorielle)
    # etat = '' # chaîne de caractères indiquant si la liste est déjà aplatie
    # # (flattened) ou non (unflattened)

    def __init__(self, List=[], etat='unflattened', shape=[]):
        sh = []
        self.List = List
        self.etat = etat
        if self.etat == 'unflattened': # si la liste n'est pas "aplatie"
            if len(self.List) == 1 and isinstance(self.List[0], (int, float)):
                # cas : 1 contrainte scalaire
                shape = [0]
            else:
                for i in range(len(self.List)): # on parcourt les éléments
                    # de la liste des contraintes
                    if isinstance(self.List[i], (list, np.ndarray)): # si la
                        # contrainte est vectorielle
                        sh.append(len(self.List[i])) # on ajoute à la liste
                        # shape la longueur du vecteur de contraintes
                    else:   # si la contrainte est scalaire
                        sh.append(0) # on ajoute un 0
                        # (signe que la contrainte est scalaire)
                shape = sh
        self.shape = shape

    def flatten(self):
        """
        "Flattens" a list of mixed constraints (from 'unflattened' to 'flattened').

        :return: the "flattened" list
        """
        if len(self.List) == 1 and isinstance(self.List[0], (int, float)):
            # cas s: 1 contrainte scalaire
            return self.List
        res = []
        for i in range(len(self.List)): # on parcourt chaque type de
            # contrainte dans la liste
            if isinstance(self.List[i], (list, np.ndarray)): # si la
                # contrainte est vectorielle
                for j in range(len(self.List[i])): # pour chaque composante
                    # de cette contrainte vectorielle
                    res.append(self.List[i][j]) # on ajoute chaque composante
                    # au résultat final res
            else: # si la contrainte est scalaire
                res.append(self.List[i]) # on l'ajoute au résultat final res
        self.etat = 'flattened' # on change l'attribut état de la liste pour
        # signifier qu'elle a été aplatie
        self.List=res
        return res # on renvoie la liste aplatie

    def unflatten(self): # fonction pour "reformer" une liste de contraintes
        # complexes "aplatie"
        """
        "Reforms" a "flattened" list of mixed constraints (from 'flattened' to
        'unflattened').

        :return: the "reformed" list
        """
        res = []
        i = 0
        for size in self.shape: # on parcourt les éléments de "shape"
            if size == 0:  #si la contrainte est scalaire
                res.append(self.List[i])
                i = i + 1
            else: # si la contrainte est vectorielle
                res.append(self.List[i:i + size])
                i = i + size
        self.etat = 'unflattened' # on change l'attribut état de la liste pour
        # signifier qu'elle a été "reformée"
        self.List=res
        return res

def normalize(x,bounds):
    '''
    Normalizes optimization variables between 0 and 1.

    :param x: variables to optimize
    :param bounds: bounds for variables
    :return: normalized values between 0 and 1
    '''
    Tbounds = np.transpose(bounds)
    Diffbounds = Tbounds[1] - Tbounds[0]
    x=(x-Tbounds[0])/Diffbounds
    return x


def denormalize(x,bounds):
    '''
    Denormalizes the normalized variables.

    :param x: normalized variables
    :param bounds: bounds for variables
    :return: original values of optimization variables
    '''
    Tbounds=np.transpose(bounds)
    Diffbounds=Tbounds[1]-Tbounds[0]
    x=x*Diffbounds+Tbounds[0]
    return x


def normalize_bounds(bounds):
    '''
    Normalizes bounds of optimization variables between 0 and 1.

    :param bounds: original bounds of variables
    :return: normalized bounds between 0 and 1
    '''
    norm_bounds=[[0,1] for i in range(len(bounds))]
    return norm_bounds


###################################################### external functions
def compute_external_function(inputs,Extfunc,len_output):
    '''
    Executes external function in optimization loops. Gives the output of the external fucntion.

    :param inputs: JaxArray: inputs of the external function.
    :param Extfunc: An instance of the class regrouping external function.
    :param len_output: int : len of the output vector of the external function
    :return: JaxArray : output vector
    '''
    return _compute_external(inputs,len_output,Extfunc)
@partial(custom_jvp,nondiff_argnums=(1,2))
def _compute_external(inputs,len_output,Extfunc):
    output_type=jax.ShapeDtypeStruct((len_output,),'float64')
    def compute_intermediary_function(inputs):
        outputs=Extfunc.compute(inputs)
        return np.array(outputs)
    outputs=jax.pure_callback(compute_intermediary_function,output_type,inputs)
    return outputs

def jacobien_compute_external(len_output,Extfunc,primals,tangents):
    '''
    Executes external functions in optimization loops. Gives the derivative of output w.r.t inputs.

    :param len_output: int : len of the output vector of the external function
    :param Extfunc: An instance of the class regrouping external function.
    :param primals: JaxArray: inputs of the external function.
    :param tangents: JaxArray: differential inputs of the external function.
    :return: JaxArray : derivative of output vector w.r.t inputs.
    '''
    inputs,=primals
    dinputs,=tangents
    output_type=jax.ShapeDtypeStruct((len_output,),'float64')
    def compute_intermediary_function(inputs):
        outputs=Extfunc.compute(inputs)
        return np.array(outputs)
    def jacobian_intermediary_function(inputs):
        gradients=Extfunc.jacobian(inputs)
        return np.array(gradients)
    outputs=jax.pure_callback(compute_intermediary_function,output_type,inputs)
    gradient_type=jax.ShapeDtypeStruct((len_output,len(inputs)),'float64')
    gradients=jax.pure_callback(jacobian_intermediary_function,gradient_type,
                                inputs)
    return outputs,jax.numpy.dot(gradients,dinputs)

_compute_external.defjvp(jacobien_compute_external)
#####################################################

def Print(elements):
    from jax import debug
    debug.print('{}',elements)


if __name__ == "__main__":
    seq = [1, [1], [2,3], 4, [5, 6, 7], np.array([1, 2])] #, [[1], 2, [3, [4]]]]
    print("original:\t", seq)
    seq2 = StructList(seq)
    res = seq2.flatten()
    print("flattened:\t", res)
    print("shape:\t\t", seq2.shape)
    seq3 = StructList(res,'flattened',seq2.shape)
    res2 = seq3.unflatten()
    print("unflattened:", res2)
