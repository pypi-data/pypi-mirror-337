# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0
import jax,jaxlib,types,sys
from jax import config
config.update("jax_enable_x64", True) # flottants sur 64 bits pour améliorer
# la précision
config.update('jax_debug_nans',False) # pour pouvoir debugger les "nan"
from jax import jacrev, jacfwd, jit # fonctions de calcul de jacobiens +
# "just in time" fonctionnalité pour performances
import numpy as np
import jax.numpy as jnp
from noloadj.optimization.specifications import Spec
from noloadj.optimization.iterationHandler import Iterations
from noloadj.optimization.Tools import *
from noloadj.optimization.ExportToXML import resultsToXML

'''Used to store results'''
class Results:
    """
    Class used to catch results at each model computation.

    Attributes :

    - objectives  = list : objective values
    - eq_cstr = class StructList : equality constraints values
    - ineq_cstr = class StructList : inequality constraints values
    """
    #objectives  = []  #valeurs des objectifs
    #eq_cstr: StructList = None  # valeurs des contraintes d'équalité
    #ineq_cstr: StructList = None  # valeurs des contraintes d'inégalités
    def __init__(self, results, shape, x,spec:Spec, jac):
        self.jac = jac # si le résultat est un calcul de jacobien ou non
        for i in range(len(results)):
            if np.size(results[i])==1:
                results[i]=np.float64(results[i])
        results = StructList(results, 'flattened', shape) # les résultats sont
        # sous la forme "aplatie" (fobjectif + contraintes)
        results1 = results.unflatten() # on remet les résultats sous forme
        # "normale" pour pouvoir après les exploiter
        nans_vars=[]
        for vars in spec.oNames: # si il y a des Nans dans les sorties
            try:
                if np.all(np.isnan(results1[spec.oNames.index(vars)])):
                    raise ValueError(vars)
            except ValueError:
                nans_vars.append(vars)
        if nans_vars != []:
            x_denorm = denormalize(x, spec.bounds)
            if len(spec.iNames) == 1 and len(x) != 1:
                nans_inputs = dict(zip(spec.iNames, [x_denorm]))
            elif spec.xinit_sh != [0]*len(spec.iNames) and spec.xinit_sh != []:
                var = StructList(x_denorm, 'flattened', spec.xinit_sh)
                nans_inputs = dict(zip(spec.iNames, var.unflatten()))
            else:
                nans_inputs = dict(zip(spec.iNames,x_denorm))
            print('Warning :', nans_vars, 'is Nan')
            if self.jac:
                print('in Gradient Computation')
            print('with inputs :',nans_inputs)
            sys.exit(0)
        t1 = len(spec.objectives) # nombre de fonctions objectives
        t2 = len(spec.eq_cstr) # nombre de contraintes d'égalité
        t3 = len(spec.ineq_cstr) # nombre de contraintes d'inégalité
        self.objectives = np.array(results1[:t1]) # les t1 premiers éléments
        # de results1 sont les fonctions objectives
        sh = np.shape(self.objectives) # taille des fonctions objectives
        if (t1 == 1) and len(sh) > 1 and sh[0] == 1:
            self.objectives = self.objectives[0]
        if t2 != 0: # s'il y a au moins une contrainte d'égalité
            self.eq_cstr = StructList(results1[t1:t1 + t2]) # les éléments
            # allant de t1 à t1+t2 sont les contraintes d'égalité
            sh = self.eq_cstr.shape # taille des contraintes d'égalité
            if (t2 == 1) and len(sh) > 1 and sh[0] == 1:
                self.eq_cstr.List = self.eq_cstr.List[0]
        if t3 != 0: # s'il y a au moins une contrainte d'inégalité
            self.ineq_cstr = StructList(results1[-t3:]) # les t3 derniers
            # éléments sont les contraintes d'inégalité
            sh = self.ineq_cstr.shape # taille des contraintes d'inégalité
            if (t3 == 1) and len(sh) > 1 and sh[0] == 1:
                self.ineq_cstr.List = self.ineq_cstr.List[0]

        # if t2 != 0:
        #     self.eq_cstr    = self.normalizeEq(results[t1:t1+t2],
        #     spec.eq_cstr_val)
        # if t3 != 0:
        #     self.ineq_cstr  = self.normalizeIneq(results[-t3:],
        #     spec.ineq_cstr_bnd)

    def normalizeEq(self, values, limits):
        """
        Puts the values of equality constraints between the limits given
        in inputs.

        :param values: desired values for the equality constraints
        :param limits: desiredlimits for the equality constraints
        :return: the values normalized of the equality constraints
        """
        # if limits!=0:
        #     results = (values.T  / limits).T
        # else:
        results = values
        for i in range(len(limits)):
            if limits[i] != 0:
                results[i] = values[i] / limits[i]
        return results

    def normalizeIneq(self, values, bounds):
        """
        Puts the values of inequality constraints between the limits given
        in inputs.

        :param values: desired values for the inequality constraints
        :param limits: desired limits for the inequality constraints
        :return: the values normalized of the inequality constraints
        """
        min = np.array([bnd[0] for bnd in bounds])  #TODO gérer des variables
        # plus complexes comme des vecteurs d'inconnus
        max = np.array([bnd[1] for bnd in bounds])
        # min = bounds[0]
        # max = bounds[1]
        if (self.jac):
            results = values
        else:
            results = ((values.T - min).T).T    #TODO gerer les None
        results = (results.T / (abs(max-min))).T
        return results

class Wrapper:
    """
    Class to do the link between the optimization model and the specifications.

    Attributes :

    - model : function of the model where we compute the objective and constraint functions
    - p = dict : constant parameters of the model (optional)
    - spec = class Spec : desired performances (objective functions, constraints)
    - resultsHandler = list : allows to save the results as they come in(optional)
    """

    # model  = None # fonction du modèle où l'on calcule les fonctions objectives
    # # et contraintes
    # p      = None # paramètres constants du modèle (optionnel)
    # spec : Spec  = None # les performances désirées (fonctions objectives,
    # # contraintes)
    # resultsHandler = None # permet de sauvegarder les résultats au fur et à
    # # mesure (optionnel)
    # ParetoList = [] # pour afficher plusieurs front de Pareto sur un graphe
    # constraints = [] # vecteur contraintes d'inégalité à remplir à chaque
    # # itération
    # xold   = None # vecteur x "ancien" (non mise à jour) pour les évaluations
    # # de fonctions
    # xold_g = None # vecteur x "ancien" (non mise à jour) pour les calculs de
    # # gradients
    # results_val : Results = None #valeurs des objectifs et contraintes
    # results_grad : Results = None #gradients des objectifs et contraintes
    # rawResults   = None #valeurs des sorties du modèle
    # resultsShape = None #forme du vecteur de sortie (mise à plat des résultats)
    # resultsShape_for_dico = None # shape de toutes les variables du modèle

    def __init__(self, model : 'function to compute',
                 specifications : Spec ,
                 parameters : 'a List of inputs that are not optimized' = {},
                 resultsHandler : "for real time plotting for instance" = None):
        self.model = model # fonction du modèle où l'on calcule les fonctions
        # objectives et contraintes
        self.p = parameters # paramètres constants du modèle (optionnel)
        self.spec = specifications # les performances désirées (fonctions
        # objectives, contraintes)
        if resultsHandler==True: # permet de sauvegarder les résultats au fur
            # et à mesure (optionnel)
            self.resultsHandler = Iterations(self.spec,specifications.iNames,
                                             specifications.oNames,
                                             specifications.freeOutputs)
            self.ParetoList=[]
#        elif resultsHandler != None:
#            self.resultsHandler = resultsHandler
        #else : no resultHandler => no iteration history

        self.init() # on initialise le wrapper

    def init(self):
        self.constraints=[]
        if len(self.spec.eq_cstr) != 0: # s'il y a au moins une contrainte
            # d'égalité
            self.constraints.append({'type': 'eq', # on ajoute à chaque
                    # itération l'évaluation des contraintes d'égalité
                 'fun' : self.eq_cstr_val,         # et leurs gradients
                 'jac' : self.eq_cstr_grad})
        if len(self.spec.ineq_cstr) != 0: # s'il y a au moins une contrainte
            # d'inégalité
            self.constraints.append({'type': 'ineq', # on ajoute à chaque
                        # itération l'évaluation des contraintes d'inégalité
                 'fun' : self.ineq_cstr_val,         # et leurs gradients
                 'jac' : self.ineq_cstr_grad})
        self.xold = None
        self.xold_g = None
        self.results_val = None
        self.results_grad = None
        self.rawResults = None
        self.compute_model=jit(self.compute_model_value) # on accélère le calcul du
        # modèle pour améliorer les performances
        #if self.spec.nb_entrees>=self.spec.nb_sorties: # s'il y a plus
            # d'entrées que de sorties dans le modèle
            #self.Jac_model=jit(jacrev(self.compute_model)) # on utilise le
            # mode "reverse" de la différentiation automatique
        #else: # s'il y a plus  de sorties que d'entrées dans le modèle
        self.Jac_model=jit(jacfwd(self.compute_model_jac)) # on utilise le
            # mode "forward" de la différentiation automatique
        
    ## 3 fonctions pour récupérer les VALEURS des objectifs et contraintes

    def f_val(self, x):
        """
        Gets the value of the objective function evaluated in x according to
        the compute_model method.

        :param x: the vector of optimization variables
        :return: the value of the objective function evaluated in x
        """
        if self.spec.debug:
            x_denorm=denormalize(x,self.spec.bounds)
            if len(self.spec.iNames) == 1 and len(x_denorm) != 1:
                dict_var = dict(zip(self.spec.iNames, [x_denorm]))
            elif self.spec.xinit_sh != [0] * len(self.spec.iNames) and \
                    self.spec.xinit_sh != []:
                var = StructList(x, 'flattened', self.spec.xinit_sh)
                dict_var = dict(zip(self.spec.iNames, var.unflatten()))
            else:
                dict_var = dict(zip(self.spec.iNames,x_denorm))
            print('x=',dict_var)
        if (not np.array_equal(self.xold,x)): # si le vecteur x n'a pas été
            # mis à jour
            self.results_val=Results(list(self.compute_model(x)),
                        self.resultsShape, x,self.spec, jac = False)
            # on calcule le modèle
            self.xold=np.array(x, copy=True) # on met à jour le vecteur x
        if self.spec.debug:
            print('fobj=',dict(zip(self.spec.objectives,
                                   self.results_val.objectives)))
        if len(self.spec.bounds)>0.: #normalisation de la fonction objective
            self.results_val.objectives[0]=(self.results_val.objectives[0]-
              self.spec.objectives_val[0])/(self.spec.objectives_val[1]-
                                            self.spec.objectives_val[0])
        return self.results_val.objectives #on renvoie les valeurs des objectifs

    def eq_cstr_val(self, x):
        """
        Returns the values of the equality constraints of the model evaluated
        in x according to the compute_model method.
        Handles mixed constraints (scalar + vector).

        :param x: the vector of optimization variables
        :return: returns the vector containing the subtraction between the
        equality constraints evaluated in x and the
        desired constraints given in the specifications class
        """
        if (not np.array_equal(self.xold,x)): # si le vecteur x n'a pas été
            # mis à jour
            self.results_val = Results(list(self.compute_model(x)),
                        self.resultsShape, x,self.spec, jac = False)
            # on calcule le modèle
            self.xold=np.array(x, copy=True) # on met à jour le vecteur x
        #il faut bien se mettre en dehors du if car le calcul du model aura pu
        # être fait dans une autre fonction.
        if self.spec.debug and self.spec.eq_cstr_val.List != []:
            print('eq_cstr=',dict(zip(self.spec.eq_cstr,
                                      self.results_val.eq_cstr.List)))
        if (self.spec.eq_cstr_val.List != []): # s'il y a au moins une
            # contrainte d'égalité
            eq_val_flatten=np.array(self.spec.eq_cstr_val.flatten())
            self.results_val.eq_cstr.List = np.array(
                self.results_val.eq_cstr.flatten()) - eq_val_flatten # -1
            for i in range(len(self.results_val.eq_cstr.List)):
                if eq_val_flatten[i]!=0.: # normalisation contraintes égalité
                    self.results_val.eq_cstr.List[i]/=eq_val_flatten[i]
            # pour calculer les contraintes d'égalité, on fait la soustraction
            # entre les contraintes calculées et les spécifications désirées
            # qui sont aplaties pour gérer les contraintes complexes (scalaires
            # + vectorielles) -> pour l'algorithme, il faudra que la
            # soustraction soit nulle pour que les contraintes d'égalité soient
            # respectées
        return self.results_val.eq_cstr.List # on renvoie les valeurs des
        # contraintes d'égalité

    def ineq_cstr_val(self, x):
        """
        Returns the values of the different inequality constraints of the model evaluated in x according to the compute_model method.
        Handles mixed constraints (scalar + vector).

        :param x: the vector of optimization variables
        :return: returns the vector containing the subtraction between the inequality constraints evaluated in x and the desired constraints given in the specifications class.
        """
        if (not np.array_equal(self.xold,x)): # si le vecteur x n'a pas été mis
            # à jour
            self.results_val = Results(list(self.compute_model(x)),
              self.resultsShape, x,self.spec, jac = False) # on calcule le modèle
            self.xold=np.array(x, copy=True) # on met à jour le vecteur x
        constraints=self.results_val.ineq_cstr.List
        if (self.spec.ineq_cstr_bnd.List != []):  # s'il y a au moins une
            # contrainte d'inégalité
            constraints = [] # on initialise le vecteur constraints
            for i, cstr in enumerate(self.spec.ineq_cstr_bnd.List): # on fait
                # la liste de toutes les différentes contraintes
                # d'inégalité (scalaires et vectorielles) et de leurs positions
                # dans le vecteur "specifications"
                if isinstance(cstr[0], (int, float)) or cstr[0]==None \
                        or cstr[1]==None: # si la contrainte est scalaire
                    if (cstr[0] != None): # s'il y a une borne inf
                        if cstr[1]==None:
                            constraints.append((self.results_val.ineq_cstr.List
                             [i]-cstr[0])/(1000.-cstr[0]))
                               # borne inf = 0 après normalisation
                        # on ajoute au vecteur constraints la soustraction entre
                        # la valeur de la contrainte d'inégalité obtenue et
                        # la borne inf
                        elif (cstr[1] != None): # s'il y a une borne sup en plus
                            constraints.append((cstr[1]-self.results_val.
                                ineq_cstr.List[i])/(cstr[1]-cstr[0]))
                            # sup = 1 si normalisé
                            # on ajoute au vecteur constraints la soustraction
                            # entre la borne sup et la valeur de la
                            # contrainte d'inégalité obtenue
                    else:  # on suppose que sup est différent de None ! Par
                        # contre il n'y a pas de borne inf
                        constraints.append((cstr[1]-self.results_val.
                            ineq_cstr.List[i])/(cstr[1]+1000.))
                        # sup = 1 si normalisé
                        # on ajoute au vecteur constraints la soustraction
                        # entre la borne sup et la valeur de la
                        # contrainte d'inégalité obtenue
                else: # si la contrainte est vectorielle
                    for j in range(len(cstr)): # on parcourt les différentes
                        # composantes de cette contrainte vectorielle
                        if (cstr[j][0]!= None): # s'il y a une borne inf
                            if cstr[j][1]==None:
                                constraints.append((self.results_val.ineq_cstr.
                                   List[i][j]-cstr[j][0])/(1000.-cstr[j][0])
                                )  # borne inf = 0 après normalisation
                            # on ajoute au vecteur constraints la soustraction
                            # entre la valeur de la contrainte d'inégalité
                            # obtenue et la borne inf
                            elif (cstr[j][1] != None):  # s'il y a une borne sup
                                # en plus
                                constraints.append((cstr[j][1]-self.results_val.
                                  ineq_cstr.List[i][j])/(cstr[j][1]-cstr[j][0]))
                                # sup = 1 si normalisé
                                # on ajoute au vecteur constraints la
                                # soustraction entre la borne sup et la
                                # valeur de la contrainte d'inégalité obtenue
                        else:  # on suppose que sup est différent de None !
                            # Par contre il n'y a pas de borne inf
                            constraints.append((cstr[j][1]-self.results_val.
                                ineq_cstr.List[i][j])/(cstr[j][1]+1000.))
                            # sup = 1 si normalisé
                            # on ajoute au vecteur constraints la soustraction
                            # entre la borne sup et la valeur de la
                            # contrainte d'inégalité obtenue
        if self.spec.debug and self.spec.ineq_cstr_bnd.List !=[]:
            print('ineq_cstr=',dict(zip(self.spec.ineq_cstr,
                                        self.results_val.ineq_cstr.List)))
        return constraints # on renvoie les valeurs des contraintes d'inégalité

    ## 3 fonctions pour récupérer les GRADIENTS des objectifs et contraintes

    def f_grad(self, x):
        """
        Returns the gradient of the objective function evaluated in x according
        to the Jacobian of the compute_model method.

        :param x: the vector of optimization variables
        :return: the gradient of the objective function evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)): # si le vecteur x n'a pas été
            # mis à jour
            self.results_grad = Results(list(self.Jac_model(x)),
                self.resultsShape, x,self.spec, jac = True)
            # on calcule le gradient du modèle
            self.xold_g=np.array(x, copy=True) # on met à jour le vecteur x
        if self.spec.debug:
            print('fobj_grad=',dict(zip(self.spec.objectives,
                                        [self.results_grad.objectives])))
        if len(self.spec.bounds)>0.: # normalisation gradients objectifs
            for i in range(len(self.results_grad.objectives)):
                self.results_grad.objectives[i]=self.results_grad.objectives[i]\
                    /(self.spec.objectives_val[1]-self.spec.objectives_val[0])
        return self.results_grad.objectives # on renvoie les gradients des
        # objectifs
 
    def eq_cstr_grad(self, x):
        """
        Returns the gradient of the different equality constraints of the model evaluated in x according to the Jacobian of the compute_model method.
        Handles mixed constraints (scalar + vector).

        :param x: the vector of optimization variables
        :return: the vector of gradient equality constraints evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)): # si le vecteur x n'a pas été
            # mis à jour
            self.results_grad = Results(list(self.Jac_model(x)),
                self.resultsShape, x,self.spec, jac = True) # on calcule le
            # gradient du modèle
            self.xold_g=np.array(x, copy=True) # on met à jour le vecteur x
        res=self.results_grad.eq_cstr.List
        if (self.spec.eq_cstr_val.List != []):
            res = [] # on va aplatir les gradients des contraintes complexes
        # (scalaires + vectorielles)
            for i in range(len(self.results_grad.eq_cstr.List)):# on parcourt le
            # résultat obtenu (gradient de contraintes d'égalité)
                if not isinstance(self.results_grad.eq_cstr.List[i],list): # si
                # un élément est déjà sous la forme np.array
                    res.append(self.results_grad.eq_cstr.List[i]) # on l'ajoute
                # simplement dans la nouvelle liste res
                elif isinstance(self.results_grad.eq_cstr.List[i], list):# si un
                # élément est une liste "composée"
                    for j in range(len(self.results_grad.eq_cstr.List[i])): # on
                    # parcourt chaque élément de la liste
                        res.append(self.results_grad.eq_cstr.List[i][j])# on les
                    # ajoute un par un à la liste res

            res=jnp.array(res) # normalisation gradients contraintes inégalité
            eq_val_flatten=np.array(self.spec.eq_cstr_val.flatten())
            if jnp.shape(res)==(1,):
                res=jnp.array([res])
            for k in range(len(res)):
                if eq_val_flatten[k]!=0.:
                    res=res.at[k,:].divide(eq_val_flatten[k])
        if self.spec.debug and self.spec.eq_cstr_val.List != []:
            print('eq_cstr_grad=',dict(zip(self.spec.eq_cstr,
                                           self.results_grad.eq_cstr.List)))
        return res # on renvoie les gradients des contraintes d'égalité

    def ineq_cstr_grad(self, x):
        """
        Returns the gradient of the different inequality constraints of themodel evaluated in x according to the Jacobian of the compute_model method.
        Handles mixed constraints (scalar + vector).

        :param x: the vector of optimization variables
        :return:  the vector of gradient inequality constraints evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)): # si le vecteur x n'a pas été
            # mis à jour
            self.results_grad = Results(list(self.Jac_model(x)),
                self.resultsShape, x,self.spec, jac = True) # on calcule le
            # gradient du modèle
            self.xold_g=np.array(x, copy=True) # on met à jour le vecteur x
        # on duplique les contraintes d'inégalité qui on une borne supérieure:
        res=self.results_grad.ineq_cstr.List
        if (self.spec.ineq_cstr_bnd.List != []): # s'il y a au moins une
            # contrainte d'inégalité
            res = [] # on initialise le vecteur res (gradients des contraintes
            # d'inégalité)
            for i, cstr in enumerate(self.spec.ineq_cstr_bnd.List): # on fait
                # la liste de toutes les différentes contraintes
                # d'inégalité (scalaires et vectorielles) et de leurs positions
                # dans le vecteur "specifications"
                if isinstance(cstr[0], (int, float)) or cstr[0]==None: # si la
                    # contrainte est scalaire
                    if (cstr[0] != None): # s'il y a une borne inf
                        if cstr[1]==None:
                            res.append(self.results_grad.ineq_cstr.List[i]/
                                (1000.-cstr[0]))# on ajoute le résultat tel quel
                        elif (cstr[1] != None): # s'il y a une borne sup en plus
                            res.append(-self.results_grad.ineq_cstr.List[i]/
                                        (cstr[1]-cstr[0]))
                            # on ajoute l'opposé du résultat car par défaut
                            # SLSQP : ctr>0
                    else:  # on suppose que sup est différent de None ! Par
                        # contre il n'y a pas de borne inf
                        res.append(- self.results_grad.ineq_cstr.List[i]/
                                   (cstr[1]+1000.))
                else: # si la contrainte est vectorielle
                    for j in range(len(cstr)):  # on parcourt les différentes
                        # composantes de cette contrainte vectorielle
                        if (cstr[j][0] != None):  # s'il y a une borne inf
                            if cstr[j][1]==None:
                                res.append(np.array(
                                  self.results_grad.ineq_cstr.List[i][j])/
                                  (1000.-cstr[j][0]))
                                # on ajoute le résultat tel quel
                            elif (cstr[j][1] != None): # s'il y a une borne sup
                                # en plus
                                res.append(-np.array(
                                    self.results_grad.ineq_cstr.List[i][j])/
                                           (cstr[j][1]-cstr[j][0]))
                                # on ajoute l'opposé du résultat car par défaut
                                # SLSQP : ctr>0
                        else:   # on suppose que sup est différent de None !
                            # Par contre il n'y a pas de borne inf
                            res.append(-np.array(
                                self.results_grad.ineq_cstr.List[i][j])/
                                       (cstr[j][1]+1000.))
        if self.spec.debug and self.spec.ineq_cstr_bnd.List!=[]:
            print('ineq_cstr_grad=',dict(zip(self.spec.ineq_cstr,
                                             self.results_grad.ineq_cstr.List)))
        return res # on renvoie les gradients des contraintes d'inégalité

    # fonction utilisée par minimize de scipy
    def f_val_grad(self, x):
        """
        Function used by scipy minimize.

        :param x: the vector of optimization variables
        :return: a tuple including the evaluation of the objective function
        evaluated in x and its gradient
        """
        return (self.f_val(x), self.f_grad(x))

    # wrapper permettant d'être selectif sur les sorties du modèles, en
    # particulier pour le calcul du Jacobien
    def compute_model_value(self, x):
        """
        Computes the model outputs (objective function + constraints) in x.

        :param x: the vector of optimization variables
        :return: returns a "flattened" vector out including the model outputs
        """
        if len(self.spec.bounds)>0.:
            x = denormalize(x, self.spec.bounds)
        if len(self.spec.iNames)==1 and len(x)!=1:
            xList = dict(zip(self.spec.iNames, [x]))
        elif self.spec.xinit_sh != [0] * len(self.spec.iNames) and \
                self.spec.xinit_sh != []:
            var = StructList(x, 'flattened', self.spec.xinit_sh)
            xList = dict(zip(self.spec.iNames, var.unflatten()))
        else:
            xList = dict(zip(self.spec.iNames, x))
        if self.p != {}: # s'il y a des paramètres constants
            res = self.model(**xList, **self.p) # on calcule le modèle
            # (entrées + fonctions objectives + contraintes)
        else: # s'il n'y a pas des paramètres constants
            res = self.model(**xList) # on calcule le modèle (entrées +
            # fonctions objectives + contraintes)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        for name in list(dico.keys()):#pour retirer les types 'function'/ class'
            if hasattr(dico[name],'__dict__') or isinstance(dico[name],
                                                            (dict,tuple,str)):
                del dico[name]
        out=[]
        for vars in self.spec.oNames:
            try:
                if vars not in list(dico.keys()):
                    raise KeyError(vars) #si la variable du cahier des charges
            except KeyError: # n'appartient pas aux sorties du modèle
                print('Warning :',vars,'is not in model')
                sys.exit(0)
            else:
                out.append(dico[vars])
        for i in range(len(out)): # si les contraintes sont sous la forme
            # np.array
            if jnp.size(jnp.array(out[i]))!=1:
                out[i]=list(out[i]) # on les décompose pour les mettre sous
                # forme de list
        out1 = StructList(out)  # on récupère les sorties du modèle
        self.resultsShape = out1.shape
        out2 = jnp.array(out1.flatten()) # on aplatit les sorties du modèle
        def save_dico(x,out,dico,out2): # sauvegarder les resultats
            self.rawResults=dico # pour le multi-objectif
            for i in list(self.rawResults.keys()): # affichage plus propre
                if np.size(self.rawResults[i])==1:
                    if np.iscomplex(self.rawResults[i]):
                        self.rawResults[i]=complex(self.rawResults[i])
                    else:
                        self.rawResults[i]=float(self.rawResults[i])
            for i in range(len(out)): #pour rendre plus 'propre' l'affichage
                if np.size(out[i])==1:
                    out[i]=float(out[i])
                else:
                    for j in range(len(out[i])):
                        if np.size(out[i][j])==1:
                            out[i][j]=float(out[i][j])
            if self.resultsHandler!=None: # on stocke les résultats obtenus à
            # chaque itération
                if self.spec.freeOutputs!=[]:
                    fData=[self.rawResults[vars] for vars in
                           self.spec.freeOutputs]
                else:
                    fData=[]
                if self.spec.xinit_sh!=[0]*len(self.spec.iNames):
                    # variables d'entrees vectorielles
                    var=StructList(x,'flattened',self.spec.xinit_sh)
                    self.resultsHandler.updateData(var.unflatten(),out,fData)
                else:
                    self.resultsHandler.updateData(x,out,fData)
                # on ajoute au resultsHandler le vecteur des entrées x et le
                # vecteur des sorties out
            return out2

        output_type=jax.ShapeDtypeStruct(out2.shape,out2.dtype)
        out2=jax.pure_callback(save_dico,output_type,x,out,dico,out2)
        return out2 # renvoie la sortie sous forme de jax.numpy array

    def compute_model_jac(self, x):
        """
        Computes the model outputs jacobians (objective function + constraints) in x.

        :param x: the vector of optimization variables
        :return: returns a "flattened" vector out including the model outputs
        """
        if len(self.spec.bounds)>0.:
            x = denormalize(x, self.spec.bounds)
        if len(self.spec.iNames)==1 and len(x)!=1:
            xList = dict(zip(self.spec.iNames, [x]))
        elif self.spec.xinit_sh != [0] * len(self.spec.iNames) and \
                self.spec.xinit_sh != []:
            var = StructList(x, 'flattened', self.spec.xinit_sh)
            xList = dict(zip(self.spec.iNames, var.unflatten()))
        else:
            xList = dict(zip(self.spec.iNames, x))
        if self.p != {}: # s'il y a des paramètres constants
            res = self.model(**xList, **self.p) # on calcule le modèle
            # (entrées + fonctions objectives + contraintes)
        else: # s'il n'y a pas des paramètres constants
            res = self.model(**xList) # on calcule le modèle (entrées +
            # fonctions objectives + contraintes)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        for name in list(dico.keys()):#pour retirer les types 'function'/ class'
            if hasattr(dico[name],'__dict__') or isinstance(dico[name],
                                                            (dict,tuple,str)):
                del dico[name]
        out=[]
        for vars in self.spec.oNames:
            try:
                if vars not in list(dico.keys()):
                    raise KeyError(vars) #si la variable du cahier des charges
            except KeyError: # n'appartient pas aux sorties du modèle
                print('Warning :',vars,'is not in model')
                sys.exit(0)
            else:
                out.append(dico[vars])
        for i in range(len(out)): # si les contraintes sont sous la forme
            # np.array
            if jnp.size(jnp.array(out[i]))!=1:
                out[i]=list(out[i]) # on les décompose pour les mettre sous
                # forme de list
        out1 = StructList(out)  # on récupère les sorties du modèle
        self.resultsShape = out1.shape
        out2 = jnp.array(out1.flatten()) # on aplatit les sorties du modèle
        return out2 # renvoie la sortie sous forme de jax.numpy array

    def f_penalty(self,x):
        """
        Returns a weighted function with the objectives and the constraints
        for stochastic algorithm of Scipy.

        :param x: the vector of optimization variables
        :return: the scalar weighted function
        """
        if (not np.array_equal(self.xold,x)):
            self.results_val = Results(list(self.compute_model(x)),
              self.resultsShape, x,self.spec, jac = False) #on calcule le modèle
            self.xold=np.array(x, copy=True)
            #construction de la fonction de penalité
        fobj = (self.results_val.objectives[0]-self.spec.objectives_val[0])/\
               (self.spec.objectives_val[1]-self.spec.objectives_val[0])
        if (self.spec.eq_cstr != []):
            for i in range(len(self.spec.eq_cstr)):
                if isinstance(self.spec.eq_cstr_val.List[i],(int,float)):
                    fobj = fobj + abs(self.results_val.eq_cstr.List[i]-
                     self.spec.eq_cstr_val.List[i])/np.where(self.spec.
                     eq_cstr_val.List[i]!=0.,self.spec.eq_cstr_val.List[i],1.)
                else:
                    for j in range(len(self.spec.eq_cstr_val.List[i])):
                        fobj=fobj+abs(self.results_val.eq_cstr.List[i][j]
                         -self.spec.eq_cstr_val.List[i][j])/\
                             self.spec.eq_cstr_val.List[i][j]
        if (self.spec.ineq_cstr != []):
            for i in range(len(self.spec.ineq_cstr)):
                if isinstance(self.spec.ineq_cstr_bnd.List[i][0],list):
                    for j in range(len(self.spec.ineq_cstr_bnd.List[i])):
                        if self.spec.ineq_cstr_bnd.List[i][j][1]!=None:
                            diff=self.spec.ineq_cstr_bnd.List[i][j][1]-np.where(
                                self.spec.ineq_cstr_bnd.List[i][j][0]!=None,
                                self.spec.ineq_cstr_bnd.List[i][j][0],-10000.)
                            fobj = fobj + max(self.results_val.ineq_cstr.List[i]
                               [j]-self.spec.ineq_cstr_bnd.List[i][j][1],0)/diff
                        if self.spec.ineq_cstr_bnd.List[i][j][0] != None:
                            diff=np.where(self.spec.ineq_cstr_bnd.List[i][j][1]
                                !=None,self.spec.ineq_cstr_bnd.List[i][j][1],
                                10000.)-self.spec.ineq_cstr_bnd.List[i][j][0]
                            fobj = fobj + max(self.spec.ineq_cstr_bnd.List[i][j]
                               [0]-self.results_val.ineq_cstr.List[i][j],0)/diff
                else:
                    if self.spec.ineq_cstr_bnd.List[i][1]!=None:
                        diff=self.spec.ineq_cstr_bnd.List[i][1]-np.where(
                                self.spec.ineq_cstr_bnd.List[i][0]!=None,
                                self.spec.ineq_cstr_bnd.List[i][0],-10000.)
                        fobj = fobj + max(self.results_val.ineq_cstr.
                            List[i]-self.spec.ineq_cstr_bnd.List[i][1],0)/diff
                    if self.spec.ineq_cstr_bnd.List[i][0] != None:
                        diff=np.where(self.spec.ineq_cstr_bnd.List[i][1]!=None,
                            self.spec.ineq_cstr_bnd.List[i][1],10000.)-\
                             self.spec.ineq_cstr_bnd.List[i][0]
                        fobj = fobj + max(self.spec.ineq_cstr_bnd.List[i][0]-
                            self.results_val.ineq_cstr.List[i],0)/diff
        return fobj

    def solution(self):
        """
        Returns the model inputs computed at the last iteration of the algorithm.

        :return: list of model inputs
        """
        if self.spec.xinit_sh != [0] * len(self.spec.iNames):
            return self.resultsHandler.solutions[-1].iData
        return self.resultsHandler.solutions[-1].iData.tolist()
        # sous la forme d'une liste

    def getLastInputs(self):
        """
        Returns the model inputs computed at the last iteration of the algorithm.

        :return: dictionary containing the model inputs
        """
        lastSol = self.resultsHandler.solutions[-1]
        # sous la forme d'un dictionnaire
        if len(self.resultsHandler.iNames)==1:
            dico = {self.resultsHandler.iNames[0]:
                        np.array(lastSol.iData).tolist()}
        else:
            dico={}
            for i in range(len(self.resultsHandler.iNames)):
                if np.size(lastSol.iData[i])==1:
                    dico[self.resultsHandler.iNames[i]]=float(lastSol.iData[i])
                else:
                    dico[self.resultsHandler.iNames[i]]=lastSol.iData[i]
        return dico

    def getLastOutputs(self):
        """
        Returns the outputs of the model computed at the last iteration of the
        algorithm.

        :return: dictionary containing the model outputs
        """
        lastSol = self.resultsHandler.solutions[-1] # sous la forme d'un
        # dictionnaire
        dico = {self.resultsHandler.oNames[i]:
            lastSol.oData[i] for i in range(len(self.resultsHandler.oNames))}
        if self.spec.freeOutputs !=[]:
            dico.update({self.resultsHandler.fNames[i]: lastSol.fData[i]
                         for i in range(len(self.resultsHandler.fNames))})
        return dico

    def printResults(self):
        """
        Displays the inputs and outputs of the model computed at the last
        iteration of the algorithm.

        :return: /
        """
        print(self.getLastInputs())
        print(self.getLastOutputs())

    def printAllResults(self):
        """
        Displays the inputs and outputs of the model computed at each iteration of the algorithm.

        :return: /
        """
        sols = self.resultsHandler.solutions
        for sol in sols:
            if len(self.resultsHandler.iNames)==1: # s'il n'y a qu'une seule
                # variable d'entrée
                dico = {self.resultsHandler.iNames[0]:
                            np.array(sol.iData).tolist()}
            else:
                dico = {self.resultsHandler.iNames[i]:
                   sol.iData[i] for i in range(len(self.resultsHandler.iNames))}
            print(dico)

    def getIteration(self,iternum):
        '''
        Returns the inputs and the outputs of the model computed at the number
        of iteration given in parameter.

        :param iternum: the number of iteration
        :return: dictionnaries containing the inputs and outputs
        '''
        sols=self.resultsHandler.solutions
        sol=sols[iternum-1]
        if len(self.resultsHandler.iNames)==1:
            iData={self.resultsHandler.iNames[0] : np.array(sol.iData).tolist()}
        else:
            iData={self.resultsHandler.iNames[i] : sol.iData[i]
                   for i in range(len(self.resultsHandler.iNames))}
        oData={self.resultsHandler.oNames[i] : sol.oData[i]
               for i in range(len(self.resultsHandler.oNames))}
        if self.spec.freeOutputs != []:
            fData={self.resultsHandler.fNames[i] : sol.fData[i]
                   for i in range(len(self.resultsHandler.fNames))}
            return iData,oData,fData
        else:
            return iData,oData

    def exportToXML(self, fileName):
        """
        Returns an XMLfile compatible with CADES. This can be used to plot
        geometry in GeomMaker.

        :param fileName: the filename to save XML tree
        :return: /
        """
        return resultsToXML(self.resultsHandler, fileName)


    def plotResults(self,outputs_names=[]):
        """
        Displays the results (inputs + outputs) graphically.

        :param: outputs_names : list of outputs names the user wants to plot
        :return: /
        """
        import noloadj.gui.plotIterations as pltIter
        pltIter.plotIO(self.resultsHandler,self.spec,outputs_names)

    def addParetoList(self,*args):
        '''
        Allows to display several Pareto Front in one graph.

        :param args: several result class
        :return:  /
        '''
        for result in args:
            self.ParetoList.append(result.resultsHandler)
        self.ParetoList.append(self.resultsHandler)

    def plotPareto(self,legend,title="Pareto front",nb_annotation = 5,
                   joinDots=True):
        """
        Plots a Pareto Front for a bi-objective optimization problem.

        :param legend: legend of the graph
        :param title: title of the graph
        :param nb_annotation: number of annotations
        :param joinDots: if True, do an interpolation spline.
        :return: /
        """
        import noloadj.gui.plotPareto as pp
        if self.ParetoList==[]:
            self.ParetoList.append(self.resultsHandler)
        pp.plot(self.ParetoList,self.spec.objectives,legend,title,
                self.spec,nb_annotation,joinDots)

    def plotNormalizedSolution(self):
        """
        Displays the "normalized" solution (values between 0 and 1) graphically.

        :return: /
        """
        bnd=np.transpose(self.spec.bounds)
        sols = self.solution()
        x = list(range(0,len(sols)))
        #normalize :
        mean = (bnd[1]+bnd[0])/2
        init = self.spec.xinit
        solsN = (sols-init)/(bnd[1]-bnd[0])

        import matplotlib.pyplot as plt
        plt.bar(x, solsN)
        plt.show()

    def openGUI(self):
        """
        Opens the Graphical User Interface.

        :return: /
        """
        from noloadj.gui.OpenGUI import openGUI
        openGUI(self.resultsHandler)
