# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from typing import List
import pandas as pd

class Solution:
    """
    Class used to store optimization inputs and outputs for an iteration.

    Attributes :

    - iData = list : model inputs (optimization variables) values
    - oData = list : model outputs (objective functions + constraints) values
    - fData = list : free outputs values
    """
    # iData = []
    # oData = []
    # fData = []

    def __init__(self, inp, out, freeOutputs=[]):
        self.iData = inp
        self.oData = out
        self.fData = freeOutputs



class Iterations:
    """
    Class used to store optimization inputs and outputs for each iteration.

    Attributes :

    - solutions: class Solution
    - iNames = list : model inputs
    - oNames = list : model outputs
    - fNames = list : model free outputs names
    - objectives = dict : objective functions of the model
    - eq_cstr = dict : equality constraints of the model
    - ineq_cstr = dict : inequality constraints of the model
    - bounds = dict : range of values of inputs
    """
    # solutions: Solution = []
    # iNames = [] # noms des entrées du modèle
    # oNames = [] # noms des sorties du modèle
    # fNames = [] # noms des sorties 'libres' du modèle
    # objectives = {} # fonctions objectives du modèle
    # eq_cstr = {} # contraintes d'égalité
    # ineq_cstr = {} # contraintes d'inégalité
    # bounds = {} # domaine de recherche

    def __init__(self, spec,iNames, oNames, fNames=[], handler = None):
        self.iNames = iNames
        self.oNames = oNames
        self.fNames = fNames
        self.solutions = []
        if spec!=None:
            if len(spec.objectives)==1:
                self.objectives=dict(zip(spec.objectives,[spec.objectives_val]))
            else:
                self.objectives=dict(zip(spec.objectives,spec.objectives_val))
            self.eq_cstr=spec.dict_eq_cstr
            self.ineq_cstr=spec.dict_ineq_cstr
            self.bounds=spec.dict_bounds
        self.handler = handler #TODO : n'est plus utilisé. Modifier la création
        # automatique du Handler (dans constructeur Wrapper) lorsqu'il s'agit
        # d'un affichage dynamique : dynamicPlot.update

    def updateData(self, inp, out, freeOutputs=[]):
        """
        Adds the inputs and outputs of the model computed at each iteration to
        the Solution class.

        :param inp: list of model inputs
        :param out: list of model outputs
        :param freeOutputs: list of freeOutputs (optional)
        :return: /
        """
        self.solutions.append(Solution(inp.copy(), out.copy(),
                                       freeOutputs.copy()))
        if (self.handler):
            self.handler(self.solutions)

    def print(self):
        """
        Returns the optimization variables values for each iteration of the optimization problem.

        :return: a dataframe with the optimization variables values for each iteration of the optimization problem.
        """
        liste=[]
        res_inp=[sol.iData for sol in self.solutions]
        res_out=[sol.oData for sol in self.solutions]
        if self.fNames !=[]:
            res_fout=[sol.fData for sol in self.solutions]
        for i in range(len(self.solutions)):
            dict={}
            for j in range(len(self.iNames)):
                dict[self.iNames[j]]=res_inp[i][j]
            for k in range(len(self.oNames)):
                dict[self.oNames[k]]=res_out[i][k]
            if self.fNames!=[]:
                for l in range(len(self.fNames)):
                    dict[self.fNames[l]]=res_fout[i][l]
            liste.append(dict)
        return pd.DataFrame(liste)
    def printSpec(self):
        """
        Returns the specifications of the optimization problem with a dataframe.

        :return: a dataframe including the specifications of the optimization problem.
        """
        df=pd.DataFrame(columns=["Value","In_Out","Type"],
                        index=list(set(self.iNames+self.oNames+self.fNames)))
        df.index.name = 'Name'
        for i in list(self.bounds.keys()):
            df.loc[i,"Value"] = self.bounds[i]
            df.loc[i,"In_Out"] = 'Input'
            df.loc[i,"Type"] = 'bounds'
        for i in list(self.objectives.keys()):
            df.loc[i,"Value"] = self.objectives[i]
            df.loc[i,"In_Out"] = 'Output'
            df.loc[i,"Type"] = 'objective'
        if self.eq_cstr!={}:
            for i in list(self.eq_cstr.keys()):
                df.loc[i,"Value"] = self.eq_cstr[i]
                df.loc[i,"In_Out"] = 'Output'
                df.loc[i,"Type"] = 'eq_cstr'
        if self.ineq_cstr!={}:
            for i in list(self.ineq_cstr.keys()):
                df.loc[i,"Value"] = self.ineq_cstr[i]
                df.loc[i,"In_Out"] = 'Output'
                df.loc[i,"Type"] = 'ineq_cstr'
        if self.fNames!=[]:
            for i in self.fNames:
                df.loc[i,"In_Out"] = 'Output'
                df.loc[i,"Type"] = 'free'
        return df

    def plotXY(self):
        import noloadj.gui.plotIterations as pi
        pi.plotXY(self)
    def plotIO(self):
        import noloadj.gui.plotIterations as pi
        pi.plotIO(self)


def printHandler(sols:List[Solution]):
    """
    Displays the inputs and outputs of the model computed during the last
    iteration.

    :param sols: class Solution
    :return: /
    """
    sols
    print(sols[-1].iData)
    print(sols[-1].oData)
    if sols.fData != []:
        print(sols[-1].fData)



