*******************************
Optimization of Dynamic Systems
*******************************

NoLoadj can also be used to solve optimization problems with dynamic systems.
Several functions are available in the numerical_methods/ODE folder to run dymamic simulation :

- odeint44 (file : ode44) solves an ODE system with a Runge-Kutta 44 algorithm. It stores values across time. It is used for optimal control problems.
- odeint45 (file : ode45) solves an ODE system with a Runge-Kutta 45 algorithm, and eventually computes its Fast-Fourier Transform (FFT). It stores values across time.
- odeint45_extract (file : ode45_extract) solves an ODE system with a Runge-Kutta 45 algorithm, without storage of values across time. Features can be calculated from the simulation.


.. contents:: Table of Contents


Optimal control example
=======================

Let's solve the optimization problem defined below with NoLoadj :

min J(u,p)= p

s.t x1_dot=p*x3*cos(u)

    x2_dot=p*x3*sin(u)

    x3_dot=p*sin(u)

    -(0.4*x1-x2+0.2)>=0 (constraint)

    x1(1)=0 (constraint)

    x(0)=(0,0,0) (initial point)

    -4<u<4 (bounds)

    1<p<100 (bounds)

First, we need to define our ODE system in a python class, inherited from the ODESystem class (in ode_tools file) :

.. code-block:: python

    import jax.numpy as np
    from noloadj.numerical_methods.ODE.ode_tools import indice_t, ODESystem

    class Brachistochrone(ODESystem):

        def __init__(self,pas):
            ODESystem.__init__(self)
            self.pas=pas
            self.xnames=['x1','x2','x3']
            self.ynames=['x1']

        def timederivatives(self,x,t,*P): # time derivatives
            u,p=P
            x3 = self.get_indice(x, ['x3'])
            x1_dot = p * x3 * np.cos(u[indice_t(t, self.pas)])
            x2_dot = p * x3 * np.sin(u[indice_t(t, self.pas)])
            x3_dot = p * np.sin(u[indice_t(t, self.pas)])
            return np.array([x1_dot,x2_dot,x3_dot])

        def output(self,x,t,*P): # outputs
            return x[0]

The 2 attributes of the class are:

- xnames : a list with the names of state variables.
- ynames : a list with the names of output variables.

2 methods must be defined :

- timederivatives : it describes the ODE system (with as input parameters: x the state variable, t the time, then the optimization inputs).
- output : it describes the expression of the output variables (with the same inputs parameters as the derivative method).

get_indice is a method from ODESystem interface, that returns the coordinate of an array corresponding to the variable name given as input parameter.

We can then define the optimization problem with NoLoadj :

.. code-block:: python

    from noloadj.optimization.optimProblem import OptimProblem,Spec
    from noloadj.numerical_methods.ODE.ode44 import odeint44
    from noloadj.numerical_methods.ODE.ode_tools import vect_temporel

    def model(u,p,x10,x20,x30,tf,pas): # optimization model
        t_eval=vect_temporel(0,tf,pas)
        brachistochrone=Brachistochrone(pas)
        x,y = odeint44(brachistochrone,np.array([x10,x20,x30]), t_eval,u,p)
        x1,x2,x3=brachistochrone.get_indice(x,['x1','x2','x3'])
        cstr=-(0.4*x1-x2+0.2*np.ones(len(x1))) # inequality constraint
        x1f=x1[-1] # equality constraint
        J=p  # objective function
        return locals().items()

    pas=0.01 # step size
    tf=1. # final time of the simulation
    N=int(tf/pas)-1 # number of points during the simulation
    ulim,cstr=[],[]
    for i in range(N):
        ulim.append([-4,4])
        cstr.append([None,0.])

    spec=Spec(variables={'u':[0.5]*N,'p':2.0},bounds={'u':ulim,'p':[1,100]},objectives={'J':[0.,5.]},
          eq_cstr={'x1f':1.},ineq_cstr={'cstr':cstr},
          freeOutputs=['x1','x2','x3'])

    parameters={'x10':0.,'x20':0.,'x30':0.,'tf':tf,'pas':pas} # constant inputs during the simulation
    optim=OptimProblem(model=model,specifications=spec,parameters=parameters)
    result=optim.run()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 1.795235462608259
                Iterations: 10
                Function evaluations: 12
                Gradient evaluations: 10



vect_temporel is a function from ode_tools that create a time vector with an initial time, a final time and step size.
odeint44 has for input parameters :

- the class that describes the ODE system defined above.
- the initial state vector.
- the time vector.
- optimization inputs (here u and p).

It returns two matrices : one with the values of state variables across time simulation (x),
and the other with the values of output variables across time simulation (y).

Sizing of a ball
================

Let's do an optimization problem of sizing. We want to size a ball so that its throw respects some constraints.
In this case, we will use ODE function with Runge-Kutta 45 algorithms without storage of values across time simulation.

We define the ODE system below.

.. code-block:: python

    import jax.numpy as np
    from noloadj.numerical_methods.ODE.ode_tools import *
    from noloadj.numerical_methods.ODE.ode_extracted_features import *

    class Ball(ODESystem):

        def __init__(self):
            ODESystem.__init__(self)
            self.g=9.81 # fixed parameters during the simulation
            self.xnames=['x','y','vx','vy']
            self.ynames = ['x', 'y']
            self.constraints={'max_y':Max('y')} # time features to extract
            self.stop=threshold('y',0.) # stopping criteria : the threshold value to reach

        def timederivatives(self,X,t,*P):
            k,m=P
            vx, vy = self.get_indice(X, ['vx', 'vy'])
            vx_dot=-k*vx*(vx*vx+vy*vy)**0.5/m
            vy_dot=-k*vy*(vx*vx+vy*vy)**0.5/m-self.g
            return np.array([vx,vy,vx_dot,vy_dot])

        def output(self, X, t, *P):
            return X[0:2]

Other attributes appear :

- g is a constant parameter that defines the gravitational constant.
- stop is the way the simulation will stop. Here, threshold means the simulation stops when y reach the 0 value. We could have defined a simulation with a constant final time, by writting self.stop=final_time(value_of_the_final_time).
- constraints represents the features we want to extract from the time simulation. Here we want to extract the maximum value of y during the simulation.

Methods of time features are (from ode_extracted_features.py file) :

- Min(variable) : to extract the minimum value of a variable during the simulation.
- Max(variable) : to extract the maximum value of a variable during the simulation.
- moy(variable) : to extract the mean value of a variable during the simulation.
- eff(variable) : to extract the Root Mean Square value of a variable during the simulation.

The optimization problem is defined below :

.. code-block:: python

    from noloadj.optimization.optimProblem import OptimProblem,Spec
    from noloadj.numerical_methods.ODE.ode45_extract import *

    def lancer(m,R,v0,a, x0, y0):
        k=0.5*1.292*0.5*np.pi*R*R
        vx0,vy0= v0*np.cos(a),v0*np.sin(a)
        ball=Ball()
        tf,Xf,Yf,cstr = odeint45_extract(ball,np.array([x0,y0,vx0,vy0]),k,m,h0=1e-3)
        hauteur=cstr['max_y']
        xf = ball.get_indice(Xf, ['x'])
        yf = ball.get_indice(Xf, ['y'])
        return locals().items()

    spec=Spec(variables={'m':1.0,'R':0.2,'v0':10,'a':np.pi/4}, bounds={'m':[0.5,10.],'R':[0.001,1.0],'v0':[10.,100.],'a':[np.pi/6,np.pi/2]},
          objectives={'hauteur':[0.,15.]}, eq_cstr={'xf':22.0},freeOutputs=['tf','yf'])

    parameters={'x0':0.,'y0':2.}

    optim=OptimProblem(model=lancer,specifications=spec,parameters=parameters)
    result=optim.run()
    result.printResults()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 4.665653864333709
                Iterations: 45
                Function evaluations: 88
                Gradient evaluations: 44
    {'m': 3.501616266753649, 'R': 0.0010000000000001106, 'v0': 14.673249789429253, 'a': 0.5235987755982989}
    {'hauteur': 4.665653864333709, 'xf': 21.99978980784155, 'tf': 1.731263010854212, 'yf': -3.408453580717911e-15}

odeint45_extract has for input parameters :

- the class that describes the ODE system defined above.
- the initial state vector.
- optimization inputs (here u and p).
- h0 as the initial step size.

It returns the final time of the simulation (tf), the final state vector (Xf), the final output vector (Yf), and the constraints (cstr) defined in ODE class as a dictionary.

After the simulation, we can visualize the simulation of the optimal point.

.. code-block:: python

    import matplotlib.pyplot as plt
    from noloadj.ODE.numerical_methods.ode45 import *

    mopt=result.solution()[0] # post processing
    Ropt=result.solution()[1]
    vopt=result.solution()[2]
    aopt=result.solution()[3]
    print(aopt*180./np.pi)
    tf=result.getLastOutputs()['tf']
    xf=result.getLastOutputs()['xf']
    k=0.5*1.292*0.5*np.pi*Ropt*Ropt
    vx0,vy0=vopt*np.cos(aopt),vopt*np.sin(aopt)

    ball=Ball()
    X,Y= odeint45(ball,np.array([0.,2.,vx0,vy0]),vect_temporel(0.,tf,1e-2), k,
                mopt, h0=1e-4)

    x,y=ball.get_indice(X,['x','y'])
    plt.figure(figsize = (10, 8))
    plt.plot(x, y)
    plt.plot(xf, 0.0, 'ro') # the final point
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.show()

.. figure:: images/throw_ball_simulation.png

odeint45 has the same inputs parameters as odeint44, with one more : h0 as the initial step size of the simulation.


Power electronics applications
==============================

Buck converter (with time-domain features)
------------------------------------------

NoLoadj can also simulate power electronics applications until detection of their steady-state and extract fratures from it.
Let's see an example with a Buck application. The ODE system is defined below.

.. code-block:: python

    import jax.numpy as np
    from noloadj.numerical_methods.ODE.ode_tools import *
    from noloadj.numerical_methods.ODE.ode_extracted_features import *

    class buck(ODESystem):

        def __init__(self,Ve,R,alpha,T):
            ODESystem.__init__(self)
            self.Ve=Ve
            self.R=R
            self.aT=alpha*T

            self.state=1 # configuration of the dynamic model
            self.xnames=['vc','il']
            self.ynames=['id']

            self.stop=steady_state(10,self.xnames,1e-5)
            self.constraints={'vc_min':Min('vc)}
            self.commande=Creneau(alpha,T)# command in the dynamic model (predictable events)

        def timederivatives(self,x,t,*P):
            C,L=*P
            def state0():
                vc=x[0]
                vc_dot=-vc/(self.R*C)
                return np.array([vc_dot,0.])
            def state1():
                vc,il=x[0],x[1]
                vc_dot=(il-vc/self.R)/C
                il_dot=(self.Ve-vc)/L
                return np.array([vc_dot,il_dot])
            def state2():
                vc,il=x[0],x[1]
                vc_dot=(il-vc/self.R)/C
                il_dot=-vc/L
                return np.array([vc_dot,il_dot])
            return Switch(self.state,[state0,state1,state2])

        def output(self,x,t,*P): # outputs and state variables that cannot be computed with ODE
            il=x[1]
            def state0():
                id=0.
                vc=x[0]
                il=0.
                return np.array([vc,il]),np.array([id])
            def state1():
                id=0.
                return x,np.array([id])
            def state2():
                id=il
                return x,np.array([id])
            return Switch(self.state,[state0,state1,state2])

        def update(self,x,y,t,c): # to detect the changes of configuration of the dynamic model
            eps,nstate,nx,ny=1e-10,self.state,x,y
            id=ny[0]
            def state0():
                def to_state_1(state):
                    nstate,nx,ny=state
                    return 1,nx,ny
                return Condition([c==1],[to_state_1],(nstate,nx,ny))
            def state1():
                def to_state_2(state):
                    nstate,nx,ny=state
                    return 2,nx,ny
                return Condition([c==0],[to_state_2],(nstate,nx,ny))
            def state2():
                def to_state_0(state):
                    nstate,nx,ny=state
                    vc=nx[0]
                    il=0.
                    id=0.
                    return 0,np.array([vc,il]),np.array([id])
                def to_state_1(state):
                    nstate,nx,ny=state
                    return 1,nx,ny
                return Condition([id<eps,c==1],[to_state_0,to_state_1],(nstate,nx,ny)) # if-elif structure
            return Switch(self.state,[state0,state1,state2])

New attributes appear :

- Ve,R,a,T are constant parameters.
- commande defines the value of some commanded devices of the application (such as transistor). Here it is a MLI command.
- state defines the configuration of the system for the present iteration.
- stop uses the 'steady-state' method, that means the simulation will stop when the steady-state of the system was detected. The inputs parameters of this method are :
    - the number of periods that has to be compared to detect the steady-state
    - the list of state variables for which the maximum and minimum across the number of periods will be computed
    - the tolerance to detect the steady-state.

New method for the class has to be defined :

- update defines the tests needed so that the model switches fro one configuration to another.
Note that in this case, state and output vectors must be returned by output method.

Methods of time features for periodic applications are :

- Min(variable) : to extract the minimum value of a variable on a simulation period T.
- Max(variable) : to extract the maximum value of a variable on a simulation period T.
- moy(variable) : to extract the mean value of a variable on a simulation period T.
- eff(variable) : to extract the Root Mean Square value of a variable on a simulation period T.

The optimization problem is defined below :

.. code-block:: python

    from noloadj.numerical_methods.ODE.ode45_extract import *
    from noloadj.numerical_methods.ODE.ode_tools import *

    def model(L,C,Ve,R,a,T,pas):
        Buck=buck(Ve,R,a,T)
        tf,X,Y,cstr,states=odeint45_extract(Buck, np.array([0.,0.]), C, L,T=T, h0=pas)
        vc_min=cstr['vc_min']
        fobj=L+C
        return locals().items()

    from noloadj.optimization.optimProblem import Spec,OptimProblem
    spec=Spec(variables={'L':0.002,'C':1e-4},objectives={'fobj':[0.,0.1]},
              bounds={'L':[1e-3,1e-1],'C':[1e-3,1e-1]},ineq_cstr={'vc_min':[2.,4.5]},debug=True)
    parameters={'Ve':12,'R':15,'a':0.2,'T':1/5000,'pas':1e-8}
    optim=OptimProblem(model,spec,parameters)
    res=optim.run()
    res.printResults()

.. parsed-literal::
    Optimization terminated successfully 	(Exit mode 0)
                Current function value: 0.0020000000000000217
                Iterations: 2
                Function evaluations: 2
                Gradient evaluations: 2
    {'L': 0.001, 'C': 0.001000000000000022}
    {'fobj': 0.0020000000000000217, 'vc_min': 2.587396867696324}

When we call the odeint45_extract function with a periodic model, it returns another output parameter called 'states', that gives the configuration of the model for the final time.

Mono-phase rectifier (with frequency-domain features)
-----------------------------------------------------

Another power electronic system is the mono-phase rectifier, modelled with fixed topology.
The optimization of this system has frequency-domain constraints, by computing its FFT after detecting its steady-state.

.. code-block:: python

    import jax.numpy as np
    from noloadj.numerical_methods.ODE.ode_tools import *
    from noloadj.numerical_methods.ODE.ode_extracted_features import *

    class Redresseur(ODESystem):

        def __init__(self,f,R,Ve,rs):
            ODESystem.__init__(self)
            self.f=f
            self.R=R
            self.Ve=Ve
            self.rs=rs

            self.xnames=['iac','idc','vdc']
            self.ynames=['ud1','ud2','id1','id2']
            self.Ron = 1e-6
            self.Roff = 1e5
            self.state = np.array([self.Ron, self.Ron])  # [R1,R2] : values of variable parameters

            n=2 #tester un autre jeu de parametres
            self.stop=steady_state(n,['iac','idc','vdc'],1e-1)
            self.constraints={'iacmoy':moy_T('iac'), # time features
                'harm_vdc':Module_FFT('vdc',21),'THD_iac':THD('iac')} # frequency features

        def timederivatives(self,x,t,*P):
            C,ls,L=P
            vs=self.Ve*np.sin(2.*np.pi*self.f*t)
            iac,idc,vdc=self.get_indice(x,['iac','idc','vdc'])
            R1,R2=self.state
            vdc_dot=(idc-vdc/self.R)/C
            idc_dot=-(vdc+0.5*(R1+R2)*idc+0.5*(R1-R2)*iac)/L
            iac_dot=(vs+0.5*(R2-R1)*idc-0.5*(R1+R2)*iac-self.rs*iac)/ls
            return np.array([iac_dot,idc_dot,vdc_dot])

        def output(self,x,t,*P):
            iac,idc,vdc=self.get_indice(x,['iac','idc','vdc'])
            vs=self.Ve*np.sin(2.*np.pi*self.f*t)
            R1,R2=self.state
            id1=(idc+iac)/2
            id2=(idc-iac)/2
            ud1=R1*id1
            ud2=R2*id2
            return np.array([ud1,ud2,id1,id2])

        def update(self,x,y,t):
            eps,nR,nx,ny=1e-6,self.state,x,y
            ud1,ud2,id1,id2=self.get_indice(ny,['ud1','ud2','id1','id2'])

            def d1_close(state):
                nR,nx,ny=state
                R1,R2=nR
                R1=self.Ron
                return np.array([R1,R2]),nx,ny
            def d1_open(state):
                nR,nx,ny=state
                R1,R2=nR
                R1=self.Roff
                return np.array([R1,R2]),nx,ny
            def d2_close(state):
                nR,nx,ny=state
                R1,R2=nR
                R2=self.Ron
                return np.array([R1,R2]),nx,ny
            def d2_open(state):
                nR,nx,ny=state
                R1,R2=nR
                R2=self.Roff
                return np.array([R1,R2]),nx,ny

            return Condition([ud1<eps,id1<-eps,ud2<eps,id2<-eps],
                             [d1_close,d1_open,d2_close,d2_open],(nR,nx,ny))
Some attributes change compared to variable topology :

- the 'state' attribute is a vector with the values of the variable resistors of the circuit (corresponding to semi conductors).
- 'Roff' defines the value of a semi conductor that is opened.
- 'Ron' defines the value of a semi conductor that is closed.

Condition is a function from noloadj.ODE.numerical_methods.ode_tools that represents a 'if-elif' structure.

Methods to extract frequency-domain constraints (from ode_extracted_features.py file) are :

- Module_FFT(variable,nh) : the FFT module of variable for given frequencies (nh is the number or the list of harmonics desired, k=0 gives the mean value of the variable, k=1 gives the module of FFT for fundamental frequency).
- THD(variable) : the Total Harmonic Distorsion of variable

The optimization problem is defined below :

.. code-block:: python

    from noloadj.numerical_methods.ODE.ode45_extract import *
    from noloadj.numerical_methods.ODE.ode_tools import *

    def model(C,ls,L,rs,Ve,f,R,pas):
        T=1./f
        redresseur=Redresseur(f,R,Ve,rs)
        tf,X,Y,cstr,fstate=odeint45_extract(redresseur,np.array([0.,0.,0.]),C,ls,L,M=int(T/pas),T=T,h0=pas)
        fond_vdc=_cstr['harm_vdc'][1]
        harm_vdc=cstr['harm_vdc'][2::]
        vdcf=np.append(fond_vdc,harm_vdc)
        vdcf_OHz=cstr['harm_vdc'][0]
        cstr_vdc_h100=cstr['harm_vdc'][2]/vdcf_OHz
        THD_iac=cstr['THD_iac']
        fobj=L+ls+C
        return locals().items()
The odeint45_extract has in this case one input parameter in addition as before :

- M : the number of points desired for the FFT computation (on one operating simulated period).

It returns the final time of the simulation (tf), the final state vector (Xf), the final output vector (Yf), the time_domain and frequency_domain constraints (cstr)
and the final state (fstate) of the simulation.


Parameters identification
=========================

NoLoadj can also solve optimization problems in order to find the input parameters that allow desired simulation.
Let's see an example with the throw of a ball.

The ODE system for a ball throw without friction is defined below :

.. code-block:: python

    import jax.numpy as np
    from noloadj.numerical_methods.ODE.ode_tools import ODESystem

    class Balle(ODESystem):

        def __init__(self):
            ODESystem.__init__(self)
            self.xnames=['x','y','vx','vy']
            self.ynames=['x','y']

        def timederivatives(self,X, t, *P): #X=[x,y,vx,vy]
            g,=P
            vx,vy=self.get_indice(X,['vx','vy'])
            return np.array([vx,vy,0.,-g]) #x_dot=[vx,vy,0.,-g]

        def output(self, X, t, *P):
            return X[0:2]

We want to find by optimization the following values of optimization inputs :

- the initial speed for the throw of the ball : v0=19.87 m/s.
- the inclination angle for the throw : a=0.785 rad.

The 'measured data' for the desired throw of the ball is the following :

.. code-block:: python

    from noloadj.numerical_methods.ODE.ode44 import odeint44
    # optimization inputs to find
    v0=19.87
    a=np.pi/4 #0.785

    x0=np.array([0.,2.,v0*np.cos(a),v0*np.sin(a)])
    g=9.81
    time=np.linspace(0,3,300)
    X,Y=odeint44(Balle(),x0,time,g)
    xref,yref=X[0],X[1] # desired simulation

The objective function of the optimization problem is the norm between the simulation got during the optimization loop, and the desired one.
The optimization problem is defined below (the LeastSquare algorithm is used for this kind of optimization problem) :

.. code-block:: python

    from noloadj.optimization.optimProblem import OptimProblem,Spec

    def model(v0,a):
        g=9.81
        x0=np.array([0.,2.,v0*np.cos(a),v0*np.sin(a)])
        time=np.linspace(0,3,300)
        X,Y=odeint44(Balle(),x0,time,g)
        x,y=X[0],X[1]
        fobj=np.linalg.norm(y-yref)+np.linalg.norm(x-xref) # objective function
        return locals().items()

    spec=Spec(variables={'v0':10.,'a':np.pi/6},
          bounds={'v0':[10.,100.],'a':[0.,np.pi/2]},
          objectives={'fobj':[0.,1.]})

    optim=OptimProblem(model,spec)
    result=optim.run(method='LeastSquare')

.. parsed-literal::
    `xtol` termination condition is satisfied.
    Solution found:  {'v0': 19.86999986744093, 'a': 0.785398166493783}
    Value of the cost function at the solution:  1.5841150815916938e-11
    Vector of residuals at the solution:  [5.62870337e-06]
    Gradient of the cost function at the solution:  [-2.15104722e-02  2.30976610e-11]

We find by optimization the desired solution.