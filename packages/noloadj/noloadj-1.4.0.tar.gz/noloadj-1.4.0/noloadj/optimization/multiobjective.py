# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from noloadj.optimization.wrapper import *
from noloadj.optimization.specifications import Spec
from noloadj.optimization.paretoTools import getXorYmid
from noloadj.optimization import optimProblem


class Pareto:
    """
    pts = list : list of 2D points
    vars = List : optimization variables values
    """
    pts  = []    #list of pt2D
    vars = []
    def __init__(self):
        self.pts = []
        self.vars = []


class EpsilonConstraint:
    """
    w = class Wrapper 
    spec = class Spec 
    fobjs = list : list of objective functions
    fobjs = list : list of bounds of objective functions
    pareto = class Pareto
    disp = bool :set to True to print convergence messages
    optimMethod = str : 'IPOPT' or 'SLSQP' algorithm
    """
    w : Wrapper = None  #wrapper
    spec : Spec = None  #specifications
    fobjs    = None
    pareto: Pareto = None

    def __init__(self, wrapper,optimMethod,disp):
        self.optimMethod=optimMethod
        self.w = wrapper
        self.spec = wrapper.spec
        self.disp=disp
        if (len(wrapper.spec.objectives)!=2): #TODO gérer une exception
            print("Pareto can only be applied to bi-objective specifications")
            return
        self.pareto = Pareto()
        self.fobjs = [wrapper.spec.objectives[0], wrapper.spec.objectives[1]]
        self.fobjs_val=[[self.spec.objectives_val[0][0],
                         self.spec.objectives_val[0][1]],
            [self.spec.objectives_val[1][0],self.spec.objectives_val[1][1]]]
        self.resultsHandler = wrapper.resultsHandler    #la sauvegarde des
        # points de calcul sera géré par le pareto
        self.w.resultsHandler = None # à remettre à la fin


    def optim2D_weighting(self, x0, optimNb=5, options=None):
        '''
        Solves a 2D optimization problem by using "ponderation" method.

        :param x0: initial values of optimization variables
        :param optimNb: number of optimization points wished
        :param options: options of simulation such as ftol, disp and maxiter
        :return: class pareto of reached points
        '''
        # ALGO
        # On fait varier un poid de 0 à 1 entre les 2 objectifs : f=a.f1+(1-a)f2
        # pour cela, il faut créer une nouvelle variable dans le modèle et
        # recalculer son Jacobien df=a.df1+(1-a)df2

        model=self.w.model
        def decorateur(model):
            def model_extended(*x,**p):
                param=p['param']
                del p['param']
                res=model(*x,**p)
                res={k:v for k,v in res.__iter__()}
                fobj=param*res[self.fobjs[0]]+(1-param)*res[self.fobjs[1]]
                res['fobj']=fobj
                return res.items()
            return model_extended
        self.w.model=decorateur(model)

        self.optim_with_param(0.0,x0,options) #left
        [xM,ym]=self.pareto.pts[0] # normalisation
        xmax,ymin=xM,ym
        xM,ym=1.,0.

        self.optim_with_param(1.0,x0,options) #right
        [xm,yM]=self.pareto.pts[1] # normalisation
        ymax,xmin=yM,xm
        yM,xm=1.,0.

        otherspts=optimNb-2
        i=0 # initialisation de l'algorithme de dichotomie
        left,right=0,1

        while i<otherspts: #dichotomie
            param=(left+right)/2
            self.optim_with_param(param,x0,options)
            [xmid,ymid]=self.pareto.pts[i+2]
            xmid,ymid=(xmid-xmin)/(xmax-xmin),(ymid-ymin)/(ymax-ymin)
            normidleft=np.sqrt((xM-xmid)**2+(ym-ymid)**2)
            normidright=np.sqrt((xm-xmid)**2+(yM-ymid)**2)
            if normidright<normidleft:
                xm,yM=xmid,ymid
                right=param
            else:
                xM,ym=xmid,ymid
                left=param
            i+=1
            x0=self.pareto.vars[-1] # dernier point calculé

        # à la fin
        self.w.model=model
        self.exclude_dominated_points()
        self.w.resultsHandler=self.resultsHandler
        return self.pareto


    def optim_with_param(self,a,x0,options):
        '''
        Solves a ponderated objective optimization problem with fobj=a*f1+(1-a)*f2.

        :param a: coefficient of ponderation
        :param x0:  initial values of optimization variables
        :param options: options of simulation
        :return: /
        '''
        self.w.p['param']=a
        self.spec.removeObjective(self.fobjs[1]) # on remplace les fonctions
        self.spec.objectives[0] = 'fobj' # objectives par l'unique fobj
        self.spec.computeAttributes()

        if self.optimMethod=='SLSQP':
            result=optimProblem.SLSQP(self.w,x0,options,self.disp)
        elif self.optimMethod=='IPOPT':
            result=optimProblem.IPOPT(self.w,x0,options)

        self.spec.objectives = [self.fobjs[0], self.fobjs[1]] # on remet les
        self.spec.objectives_val=[[self.fobjs_val[0][0],self.fobjs_val[0][1]],
                    [self.fobjs_val[1][0],self.fobjs_val[1][1]]]
        self.spec.computeAttributes()# fonctions objectives pour pouvoir
        self.saveSolution(result) # sauvergarder les points de Pareto
        del self.w.p['param']


    def optim2D(self, x0, optimNb=5, options=None):
        """
        Solves a 2D optimization problem (with two objective functions) by
        using "epsilon constraint" method.

        :param x0: initial values of optimization variables
        :param optimNb: number of optimization points wished
        :param options: options of simulation such as ftol, disp and maxiter
        :return: class pareto of reached points
        """
        #ALGO
        # init : réaliser 2 optim sur chaque objectifs avec l'autre
        # objectif libre => utopia0
        # init : faire une sous contrainte au milieu
        # itérer : en recherchant la distance la plus grande entre 2 solutions
        #   et en fixant l'objectif dont la projection est la plus grande,
        #   au milieu de cette projection
        # convergence : nombre de point atteint

        #2 optim sans contraintes :
        #optim du premier objectif, suppression du 2ème objectif (objectif 1)
        self.modifySpec_Optim(x0, options, 1)
        xm = self.pareto.pts[0][0]
        yM = self.pareto.pts[0][1]

        #optim du 2ème objectif, suppression du 1er objectif (objectif 0)
        self.modifySpec_Optim(x0, options, 0)
        xM = self.pareto.pts[1][0]
        ym = self.pareto.pts[1][1]

        normX = xM-xm
        normY = yM-ym

        #optimisation avec l'autre objectif contraint
        x0 = self.pareto.vars[0]    # on part de la solution optimale pour
        # fobX et on contraint sa valeur en augmentant
        x0 = self.modifySpec_Optim(x0, options, 0, (2*xm+xM)/3)   #calcul un
        # peu à gauche du milieu (mieux que le milieu pour une courbe)

        #on reinitialise x0 à la valeur d'extremité du pareto trouvée au début.
        for i in range(1,optimNb-2):
            obj, point = getXorYmid(self.pareto.pts, normX, normY, xm, ym)
            x0 = self.modifySpec_Optim(x0, options, obj, point)
            #print("add a point :"+ str(obj) +" / " + str(point))

        #à la fin
        self.exclude_dominated_points()
        self.w.resultsHandler = self.resultsHandler
        return self.pareto

    def optim2D_basic(self, x0, optimNb=10, options=None):
        """
        Solves a 2D optimization problem (with two objective functions) by
        doing two optimizations for each objective function with the other
        objective function fixed.

        Then computes the biggest distance between the two solutions.
        :param x0: initial values of optimization variables
        :param optimNb: number of optimization points wished - Must be PAIR
        :param options: options of simulation such as ftol, disp and maxiter
        :return: number of reached points
        """
        #ALGO
        # init : réaliser 2 optim sur chaque objectifs avec l'autre objectif
        # libre => utopia0
        # itérer : 2 optim sur chaque objectif avec l'autre objectif fixé entre
        # utopia et la valeur précédente.
        # convergence : utopia n'évolue plus, ou budget en temps ou en nombre
        # de calcul, ou en point sur le front.

        #2 optim sans contraintes :
        #optim du premier objectif, suppression du 2ème objectif (objectif 1)

        self.modifySpec_Optim(x0, options, 1)
        xm = self.pareto.pts[0][0]
        yM = self.pareto.pts[0][1]

        #optim du 2ème objectif, suppression du 1er objectif (objectif 0)
        self.modifySpec_Optim(x0, options, 0)
        xM = self.pareto.pts[1][0]
        ym = self.pareto.pts[1][1]

        #iterations d'optimisation avec l'autre objectif contraint
        #version où on connait le nombre de points sur le Pareto et on reparti
        # sur les 2 axes
        nbpts = int((optimNb-2)/2)
        if nbpts<1:
            nbpts=1
        x0 = self.pareto.vars[1]    # on part de la solution optimale pour fobY
        # et on contraint sa valeur en augmentant
        for i in range(1,nbpts+1):
            point = ym + i * (yM-ym)/(nbpts+1)
            # optim du premier objectif, suppression du 2ème objectif et mise
            # en contrainte
            x0 = self.modifySpec_Optim(x0, options, 1, point)

        #on reinitialise x0 à la valeur d'extremité du pareto trouvée au début.
        x0 = self.pareto.vars[0]
        for i in range(1,nbpts+1):
            point = xm + i * (xM-xm)/(nbpts+1)
            # optim du 2ème objectif, suppression du 1ème objectif et mise en
            # contrainte
            x0 = self.modifySpec_Optim(x0, options, 0, point)

        #à la fin
        self.exclude_dominated_points()
        self.w.resultsHandler = self.resultsHandler
        return self.pareto

    #for Epsilon Constraint
    def modifySpec_Optim(self, x0, options, obj, cstrVal=None):
        """
        Modifies the optimization specifications by removing an objective
        function and appends it as a constraint.

        :param x0: initial values of optimization variables
        :param options: options of simulation such as ftol, disp and maxiter
        :param obj: the index on the objective function wished
        (0 for the first, 1 for the second)
        :param cstrVal: value of the objective function "fixed"
        :return: the vector x of optimized inputs
        """
        self.spec.removeObjective(self.fobjs[obj])
        if cstrVal!=None:
            self.spec.appendConstraint(self.fobjs[obj], cstrVal)
        if self.optimMethod=='SLSQP':
            result=optimProblem.SLSQP(self.w,x0,options,self.disp,0)
        elif self.optimMethod=='IPOPT':
            result=optimProblem.IPOPT(self.w,x0,options,0) #1D optim
        #IF Singular matrix C in LSQ subproblem    (Exit mode 6)

        self.spec.insertObjective(obj, self.fobjs[obj],self.fobjs_val[obj])
        if cstrVal != None:
            self.spec.removeLastEqConstraint()
        self.saveSolution(result)
        return result.x

    def saveSolution(self, result): #doit bien être appelé après avoir remis
        # les 2 objectifs dans les spec.
        """
        Saves the solution of the "modifySpec_Optim" function in the
        pareto class.

        :param result : the vector x of optimized inputs
        :return: /
        """
        out =[self.w.rawResults[vars] for vars in self.spec.oNames]
        fOut = [self.w.rawResults[vars] for vars in self.spec.freeOutputs]
        xopt = result.x
        xopt = np.where(np.abs(xopt)<1e-15,0.,xopt)
        self.resultsHandler.updateData(xopt, out, fOut)
        self.pareto.pts.append([out[0], out[1]])
        self.pareto.vars.append(xopt)

    def exclude_dominated_points(self):
        """Filters a list of points in the Pareto front to exclude any dominated points.
        """
        pareto_pts=self.pareto.pts
        for i, point1 in enumerate(pareto_pts):
            dominated = False
            for j, point2 in enumerate(pareto_pts):
                if i == j:
                    continue
                if all(p1 >= p2 for p1, p2 in zip(point1, point2)):
                    dominated = True
                    break
            if dominated:
                self.pareto.pts.pop(i)
                self.pareto.vars.pop(i)
                self.resultsHandler.solutions.pop(i)
