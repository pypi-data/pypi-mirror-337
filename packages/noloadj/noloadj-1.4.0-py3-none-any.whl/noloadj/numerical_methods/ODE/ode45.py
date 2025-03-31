import jax.numpy as np
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial
from jax import config
config.update("jax_enable_x64", True)


def odeint45(f,x0,vect_t,*P,M=None,T=0.,h0=1e-5,tol=1.48e-8):
    '''
    Solves an ODE system described by f with Runge-Kutta 5 (7M) algorithm, and
    eventually compute its fast Fourier Transform (FFT).

    :param f: a class inherited from ODESystem abstract class that describes the ODE system
    :param x0: Array: initial state vector
    :param vect_t: Array: time vector on which the ODE system must be solved
    :param P: tuple of Array: optimization inputs
    :param M: int: number of points to compute the FFT
    :param T: float: operating period of the system (optional)
    :param h0: float: initial step size
    :param tol: float: tolerance for optimal step size computation

    :return: Several outputs:

    - Array : state vector 'xf' values across time vector
    - Array : output vector 'yf' values across time vector
    - int/Array : configurations 'states' across time vector is the system is periodic.
    '''
    return _odeint45(f,h0,tol,M,x0,vect_t,T,*P)


def rk_step(x_prev, t_prev, h_prev,f,*P):
    '''
    An iteration of the Runge-Kutta 5 (7M) algorithm.
    An iteration of the Runge-Kutta 5 (7M) algorithm.

    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param h_prev: step size at the previous iteration
    :param f: a class that describes the ODE system
    :param P: optimization inputs
    :return: the state vector at the present iteration x_now, its estimation
        x_now_est the time t_now at the present iteration.
    '''
    k1=f.timederivatives(x_prev, t_prev,*P)
    k2 = f.timederivatives(x_prev + h_prev*0.2 * k1, t_prev + 0.2 * h_prev,*P)
    k3 = f.timederivatives(x_prev+h_prev*(3 * k1+9*k2)/40,t_prev+3*h_prev/10,*P)
    k4 = f.timederivatives(x_prev + h_prev*(44 *k1/45-56*k2/15+32*k3/9),t_prev +
           4 * h_prev / 5,*P)
    k5 = f.timederivatives(x_prev + h_prev*(19372 * k1/6561-25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729),
           t_prev + 8 * h_prev / 9,*P)
    k6 = f.timederivatives(x_prev +h_prev*(9017*k1/3168-355*k2/33+46732*k3/5247+
            49 * k4 / 176 - 5103 * k5 / 18656),t_prev + h_prev,*P)
    k7 = f.timederivatives(x_prev + h_prev*(35 * k1 / 384 + 500 * k3 / 1113 +
            125 * k4 / 192 -2187 * k5 / 6784 + 11 * k6 / 84),t_prev + h_prev,*P)

    x_now = x_prev + h_prev *(35 * k1 / 384 + 500 * k3 / 1113 + 125 * k4 / 192
             -2187 * k5 / 6784 + 11 * k6 / 84)
    x_now_est = x_prev + h_prev *(5179 * k1 / 57600 + 7571* k3/16695+393*k4/640
            - 92097 * k5 / 339200 + 187 * k6 / 2100 + k7 / 40)
    t_now = t_prev + h_prev
    return x_now, x_now_est, t_now


def optimal_step(x_now,x_now_est,h_prev,tol,x_prev):
    '''
    Computes the optimal step size for the next iteration.

    :param x_now: state vector at the present iteration
    :param x_now_est: estimation of the state vector x_now
    :param h_prev: step size from the present iteration
    :param tol: tolerance for optimal step size computation
    :param x_prev: state vector at the previous iteration
    :return: optimal step size for the next iteration
    '''
    e=np.sqrt(np.sum(((x_now-x_now_est)/
                      (tol+tol*np.maximum(np.abs(x_now),np.abs(x_prev))))**2))
    hopt=h_prev*(e)**(-1/5)
    h_now=np.minimum(1.5*h_prev,0.9*hopt)
    return h_now

def interpolation(x_prev,y_prev,t_prev,x_now,y_now,t_now,t_new):
    '''
    Computes state and output vectors at time t_new by linear interpolation.

    :param x_prev: state vector at the previous iteration
    :param y_prev: output vector at the previous iteration
    :param t_prev: time at the previous iteration
    :param x_now: state vector at the present iteration
    :param y_now: output vector at the present iteration
    :param t_now: time at the present iteration
    :param t_new: new time for present iteration
    :return: state and output vectors x_new and y_new at t_new.
    '''
    x_new=((x_prev-x_now)*t_new+(t_prev*x_now-t_now*x_prev))/(t_prev-t_now)
    y_new=((y_prev-y_now)*t_new+(t_prev*y_now-t_now*y_prev))/(t_prev-t_now)
    return x_new,y_new

def compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                      diff_var_threshold_value,diff_var_threshold_value_prev):
    '''
    Computes new time t_new and vectors x_new, y_new for which a state variable
    equals a threshold value.

    :param x_now: state vector at the present iteration
    :param x_prev: state vector at the previous iteration
    :param t_prev: time at the previous iteration
    :param t_now: time at the present iteration
    :param y_prev: output vector at the previous iteration
    :param y_now: output vector at the present iteration
    :param diff_var_threshold_value: differences between the output variable and
        the threshold value at the present iteration
    :param diff_var_threshold_value_prev: differences between the output variable
        and the threshold value at the previous iteration
    :return: new time t_new and vectors x_new, y_new
    '''
    t_new=(-t_prev*diff_var_threshold_value+t_now*diff_var_threshold_value_prev)/\
          (diff_var_threshold_value_prev-diff_var_threshold_value)
    h_new=t_new-t_prev
    x_new,y_new=interpolation(x_prev,y_prev,t_prev,x_now,y_now,t_now,t_new)
    return x_new,h_new,t_new,y_new

def interp_state_chgt(x_prev,y_prev,y_target,t_prev,x_now,y_now,t_now,f,i_prev,
                      h_prev,c_now):
    '''
    Tests if there is a changement of configuration of the ODE system at the
    present time.

    :param x_prev: state vector at the previous iteration
    :param y_prev: output vector at the previous iteration
    :param y_target: new output vector after changement of configuration
    :param t_prev: time at the previous iteration
    :param x_now: state vector at the present iteration
    :param y_now: output vector at the present iteration
    :param t_now: time at the present iteration
    :param f: a class that describes the ODE system
    :param i_prev: configuration of the system at the previous iteration
    :param h_prev: step size from the present iteration
    :param c_now: command of the ODE system for the present iteration
    :return: the new state vector x_now, outputs vector y_now, time t_now,
        the optimal step size for next iteration h_now.
    '''
    ind=np.where(np.array_equiv(y_now,y_target),-1,np.argmax(np.abs(y_now-
                                                                    y_target)))
    threshold_value=y_target[ind]
    diff_var_threshold_value=y_now[ind]-threshold_value
    diff_var_threshold_value_prev=y_prev[ind]-threshold_value
    condition = np.bitwise_and(np.sign(diff_var_threshold_value)!=np.sign(
            diff_var_threshold_value_prev),np.not_equal(ind,-1))
    condition=np.bitwise_and(condition,np.bitwise_not(np.allclose(
            diff_var_threshold_value_prev,0.)))
    x_now,h_now,t_now,y_now=cond(condition,lambda state:compute_new_point(
        x_now,x_prev,t_prev,t_now,y_prev,y_now,diff_var_threshold_value,
        diff_var_threshold_value_prev),lambda state:state,(x_now,h_prev,t_now,
                                                           y_now))
    if not isinstance(f.commande,type(None)) and not isinstance(f.state,
                                                             type(None)):
        _,x_now,y_now=f.update(x_now,y_now,t_now,c_now)
    elif isinstance(f.commande,type(None)) and not isinstance(f.state,
                                                               type(None)):
        _,x_now,y_now=f.update(x_now,y_now,t_now)
    else:
        x_now,y_now=f.update(x_now,y_now,t_now)
    return x_now,y_now,h_now,t_now

def next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P):
    '''
    Computes the state vector, output vector and time at the present iteration.

    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param y_prev: the output at the previous iteration
    :param i_prev: configuration of the system at the previous iteration
    :param c_prev: command of the system at the previous iteration
    :param h_prev: step size from the present iteration
    :param f: a class that describes the ODE system
    :param tol: tolerance for optimal step size computation
    :param T: operating period of the system (facultative)
    :param P: optimization inputs
    :return: the state vector x_now, outputs vector y_now, time t_now,
        configuration i_now, commande c_now at the present iteration,
        the optimal step size for next iteration h_now.
    '''
    if not isinstance(f.state,type(None)):
        f.state=i_prev
    if 'initialize' in f.__class__.__dict__:
        P=f.initialize(*P)
    x_now,x_now_est,t_now=rk_step(x_prev,t_prev,h_prev,f,*P)
    y_now=f.output(x_now,t_now,*P)
    y_now_est=f.output(x_now_est,t_now,*P)
    if isinstance(y_now,tuple):
        x_now,y_now=y_now
        x_now_est=y_now_est[0]
    h_now,c_now,tpdi=0.,0,0.
    if 'update' in f.__class__.__dict__ and not isinstance(f.state,type(None)):
        if not isinstance(f.commande,type(None)):
            tpdi=f.commande.next_pdi(t_now)
            c_now=f.commande.next_command(t_now)
            i_now,_,y_target=f.update(x_now,y_now,t_now,c_now)
        else:
            c_now=c_prev
            i_now,_,y_target=f.update(x_now,y_now,t_now)
        x_now,y_now,h_now,t_now=cond(np.bitwise_not(np.allclose(i_prev,i_now)),
            lambda state:interp_state_chgt(x_prev,y_prev,y_target,t_prev,x_now,
            y_now,t_now,f,i_prev,h_prev,c_now), lambda state:state,(x_now,y_now,
            h_now,t_now))

        y_now=f.output(x_now,t_now,*P)
        if len(y_now)==2:
            x_now,y_now=y_now
        h_now= optimal_step(x_now,x_now_est, h_prev, tol,x_prev)
        if not isinstance(f.commande,type(None)):
            h_now=np.minimum(tpdi-t_now,h_now)
        h_now=np.where(np.bitwise_not(np.allclose(i_prev,i_now)),1e-9,h_now) # pour accelerer code
    else:
        i_now=i_prev
        c_now=c_now
    if 'update' in f.__class__.__dict__ and isinstance(f.state,type(None)):
        _,y_target=f.update(x_now,y_now,t_now)
        x_now,y_now,h_now,t_now=interp_state_chgt(x_prev,y_prev,y_target,t_prev,
                                    x_now,y_now,t_now,f,i_prev,h_prev,c_now)
        y_now=f.output(x_now,t_now,*P)
        h_now = optimal_step(x_now, x_now_est, h_prev, tol,x_prev)
    elif not not isinstance(f.state,type(None)) and not 'update' in \
                                                        f.__class__.__dict__:
        h_now = optimal_step(x_now, x_now_est, h_prev, tol,x_prev)
    return x_now,t_now,y_now,h_now,i_now,c_now

def compute_fft(xf,yf,M):
    '''
    Compute the FFT of state variables xf and output variables yf.

    :param xf:  a matrix xf with state vector values across time
    :param yf: a matrix yf with output vector values across time
    :param M: number of points to compute the FFT
    :return: the respective FFT module and phase of xf and yf
    '''
    xfft=np.fft.fft(xf,M)*2/M # fft de x avec normalisation
    xfft=xfft.at[:,0].divide(2)
    yfft=np.fft.fft(yf,M)*2/M # fft de y avec normalisation
    yfft=yfft.at[:,0].divide(2)
    moduleX,phaseX=np.abs(xfft),np.angle(xfft) # amplitude et phase de la fft de x
    moduleY,phaseY=np.abs(yfft),np.angle(yfft) # amplitude et phase de la fft de y

    return xf,moduleX[:,0:M//2],phaseX[:,0:M//2],yf,moduleY[:,0:M//2],\
           phaseY[:,0:M//2]# on retire les frequences negatives


@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def _odeint45(f,h0,tol,M,x0,vect_t,T,*P):

    def scan_fun(state,te):

        def cond_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev,c_prev=state
            return (t_prev<te) & (h_prev>0) # condition d'arrêt de simulation

        def body_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev,c_prev=state

            x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,
                                t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P) # prochaine itération de simulation

            # to reach te
            h_now=np.minimum(h_now,te-t_prev)

            return x_now,t_now,y_now,h_now,i_now,c_now

        x_now,t_now,y_now,h_now,i_now,c_now = while_loop(cond_fn,body_fn,state)

        return (x_now,t_now,y_now,h_now,i_now,c_now),(x_now,y_now,i_now)

    if not isinstance(f.state,type(None)):
        i0=f.state
    else:
        i0=0
    if not isinstance(f.commande,type(None)):
        c0=f.commande.next_command(vect_t[0])
    else:
        c0=0
    tempP=None
    if 'initialize' in f.__class__.__dict__:
        tempP=P
        P=f.initialize(*P)
    y0=f.output(x0,vect_t[0],*P)
    if isinstance(y0,tuple):
        x0,y0=y0
    if 'initialize' in f.__class__.__dict__:
        P=tempP
    vect,(xf,yf,states)=scan(scan_fun,(x0,vect_t[0],y0,h0,i0,c0),vect_t[1:])
    if not isinstance(f.state,type(None)): #  pour eviter erreurs d'execution
        f.state=vect[4]
    xf=np.transpose(np.concatenate((x0[None], xf))) # valeurs stockées du vecteur d'état
    yf=np.transpose(np.concatenate((y0[None], yf))) # valeurs stockées du vecteur de sortie
    if not isinstance(f.state,type(None)): # si le systeme comporte plusieurs configurations
        if isinstance(i0,int):
            states=np.insert(states,0,i0) # configurations écrites sous la forme d'un entier
        else:
            states=np.transpose(np.concatenate((i0[None], states))) # configurations écrites sous la forme d'un vecteur
        if M==None: # s'il n'y a pas de simulation fréquentielle à faire
            return xf,yf,states
        else: # s'il y a une simulation fréquentielle à faire
            xf, modX, phX, yf, modY, phY = compute_fft(xf, yf, M)
            return xf, modX, phX, yf, modY, phY, states
    else: # si le système ne comporte pas plusieurs configurations
        if M==None: # s'il n'y a pas de simulation fréquentielle à faire
            return xf,yf
        else: # s'il y a une simulation fréquentielle à faire
            xf, modX, phX, yf, modY, phY = compute_fft(xf, yf, M)
            return xf, modX, phX, yf, modY, phY


@_odeint45.defjvp
def _odeint45_jvp(f,h0,tol,M, primals, tangents):
    '''
    Solves an ODE system described by df/dP with Runge-Kutta 5 (7M) algorithm.

    :param f: a class that describes the ODE system
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :param M: number of points to compute the FFT
    :param primals: tuple including initial state vector, time vector, operating
        period and optimization inputs.
    :param tangents: tuple including differentials of initial state vector,
        operating period and optimization inputs.
    :return: a matrix xf with state vector values across time, and a matrix yf
        with output vector values across time, their respective derivatives
        w.r.t P (dxf and dyf), and a matrix states with configurations across
        time for periodic systems. Eventually the FFT module and phase,
        and their derivatives w.r.t optimization inputs.
    '''
    x0, vect_t,T, *P = primals
    dx0, _,_, *dP = tangents
    nPdP = len(P)

    res = odeint45_etendu(f, nPdP, h0, tol, M, x0, dx0, vect_t, T,*P, *dP)

    if not isinstance(f.state,type(None)): #si le systeme comporte plusieurs configurations
        if M==None: # s'il n'y a pas de simulation fréquentielle à faire
            xf,dxf,yf,dyf,states=res
            return (xf,yf,states),(dxf,dyf,states)
        else: # s'il y a une simulation fréquentielle à faire
            xf,dxf,modX,phX,dmodX,dphX,yf,dyf,modY,phY,dmodY,dphY,states=res
            return (xf,modX,phX,yf,modY,phY,states),(dxf,dmodX,dphX,dmodY,dphY,
                                                     states)
    else: # si le système ne comporte pas plusieurs configurations
        if M==None: # s'il n'y a pas de simulation fréquentielle à faire
            xf,dxf,yf,dyf=res
            return (xf,yf),(dxf,dyf)
        else: # s'il y a une simulation fréquentielle à faire
            xf,dxf,modX,phX,dmodX,dphX,yf,dyf,modY,phY,dmodY,dphY=res
            return (xf,modX,phX,yf,modY,phY),(dxf,dmodX,dphX,dyf,dmodY,dphY)

def f_grads(x,dx, t, f,nPdP, *P_and_dP):
    '''
    Computes the derivatives of state vector w.r.t P.

    :param x: state vector values
    :param dx: differential of state vector
    :param t: time at present iteration
    :param f: a class that describes the ODE system
    :param nPdP: length of optimization inputs
    :param P_and_dP: optimization inputs values and differentials
    :return: the derivatives of state vector w.r.t P.
    '''
    P, dP = P_and_dP[:nPdP], P_and_dP[nPdP:]
    res, dres = jvp(f.timederivatives, (x, t, *P), (dx,0., *dP))
    return dres

def rk45_step_der(x_prev, t_prev, dx_prev,h_prev,f,nPdP,*P_and_dP):
    '''
    An iteration of the Runge-Kutta 5 (7M) algorithm for the ODE system described
    by df/dP.

    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param dx_prev: the differential of state vector at the previous iteration
    :param h: constant step size
    :param h_prev: step size for the present iteration
    :param f: a class that describes the ODE system.
    :param nPdP: length of optimization inputs
    :param P_and_dP: optimization inputs values and differentials
    :return: dx/dp and x at the present iteration.
    '''
    P=P_and_dP[:nPdP]
    k1=f.timederivatives(x_prev, t_prev,*P)
    k2 = f.timederivatives(x_prev + h_prev*0.2 * k1, t_prev + 0.2 * h_prev,*P)
    k3=f.timederivatives(x_prev + h_prev*(3*k1 +9*k2)/40,t_prev+3 *h_prev/10,*P)
    k4 = f.timederivatives(x_prev + h_prev*(44 * k1 / 45 - 56 * k2/ 15+32*k3/9),
                      t_prev + 4 * h_prev / 5,*P)
    k5 = f.timederivatives(x_prev + h_prev*(19372*k1/6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729),t_prev + 8 * h_prev / 9,*P)

    dk1 = f_grads(x_prev, dx_prev, t_prev,f,nPdP, *P_and_dP)
    dk2 = f_grads(x_prev+ h_prev*0.2 * k1, dx_prev + h_prev * 0.2 * dk1,t_prev +
                0.2 * h_prev ,f,nPdP, *P_and_dP)
    dk3 = f_grads(x_prev+ h_prev*(3 * k1 + 9 * k2) / 40,dx_prev+h_prev *(3 * dk1
                + 9 * dk2) / 40,t_prev+3 * h_prev / 10,f,nPdP, *P_and_dP)
    dk4 = f_grads(x_prev+ h_prev*(44 * k1 / 45 - 56 * k2 / 15 + 32 * k3 / 9),
                dx_prev +h_prev*(44 * dk1 / 45 - 56 * dk2 /15+32*dk3/9),
                t_prev + 4 * h_prev / 5,f,nPdP,*P_and_dP)
    dk5 = f_grads(x_prev+ h_prev*(19372 * k1 / 6561 - 25360 * k2 / 2187 +
            64448 * k3 / 6561- 212 * k4 / 729), dx_prev + h_prev *
        (19372 * dk1 / 6561 - 25360*dk2/2187+ 64448 * dk3 / 6561 - 212 * dk4
            / 729),t_prev + 8 * h_prev / 9,f,nPdP, *P_and_dP)
    dk6 = f_grads(x_prev+ h_prev*(9017 * k1 / 3168 - 355* k2 / 33+46732*k3/5247+
            49 * k4 / 176 - 5103 * k5 / 18656),dx_prev+h_prev*(9017 *
            dk1 / 3168 -355 *dk2/33 +46732*dk3/5247 + 49 * dk4 / 176 - 5103 *
            dk5 / 18656),t_prev + h_prev,f,nPdP,*P_and_dP)
    dx_now = dx_prev + h_prev *(35 * dk1 / 384 + 500 * dk3 / 1113 +
            125 * dk4 / 192 - 2187 * dk5 / 6784 + 11 * dk6 / 84)
    return dx_now

def next_der_step_simulation(x_prev,t_prev,dx_prev,x_now,t_now,h_prev,f,
                             nPdP,chgt_state,Mat,dMat,*P_and_dP):
    '''
    Computes the state vector, output vector, their derivatives and time at
    the present iteration.

    :param x_prev: the state vector at the previous iteration
    :param t_prev: the time at the previous iteration
    :param dx_prev: the differentials of the state vector at the previous iteration
    :param h: constant step size
    :param x_now: state vector at the present iteration
    :param t_now: time at the present iteration
    :param h_prev: step size for the present iteration
    :param f: a class that describes the ODE system
    :param nPdP: length of optimization inputs
    :param chgt_state: bool which indicates if system changed configuration
                       the previous iteration
    :param Mat: state matrices at the present iteration
    :param dMat: derivatives of state matrices at the present iteration
    :param P_and_dP: optimization inputs values and differentials
    :return: the derivatives of state and output vectors dx_now, dy_now, and
    state matrices Mat and their derivatives at the next iteration.
    '''
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    if 'initialize' in f.__class__.__dict__:
        P,dP = cond(chgt_state,lambda state:jvp(f.initialize, (*P,), (*dP,)),
                    lambda state:state,(Mat,dMat))
        P_and_dP=P+dP
        Mat,dMat=P,dP
        nPdP=len(P)
    dx_now=rk45_step_der(x_prev,t_prev,dx_prev,h_prev,f,nPdP,*P_and_dP)
    dx_now=np.where(np.abs(dx_now)>1e12,np.sign(dx_now)*1e12,dx_now) # pour eviter gradients trop grands
    dy_now = jvp(f.output, (x_now, t_now, *P), (dx_now, 0., *dP))[1]
    if isinstance(dy_now,tuple):
        dx_now,dy_now=dy_now
    return dx_now,dy_now,Mat,dMat

def compute_der_fft(xf,dxf,yf,dyf,M):
    '''
    Compute the FFT of state variables xf and output variables yf, and their
        derivatives w.r.t optimization inputs.

    :param xf:  a matrix xf with state vector values across time
    :param dxf: derivatives of xf w.r.t optimization inputs.
    :param yf: a matrix yf with output vector values across time
    :param dyf: derivatives of yf w.r.t optimization inputs.
    :param M: number of points to compute the FFT.
    :return: the respective FFT module and phase of xf and yf, and their derivatives
        w.r.t optimization inputs.
    '''
    xfft=np.fft.fft(xf,M)*2/M  # fft de x avec normalisation
    dxfft=np.fft.fft(dxf,M)*2/M
    xfft,dxfft=xfft.at[:,0].divide(2),dxfft.at[:,0].divide(2)
    yfft=np.fft.fft(yf,M)*2/M  # fft de x avec normalisation
    dyfft=np.fft.fft(dyf,M)*2/M
    yfft,dyfft=yfft.at[:,0].divide(2),dyfft.at[:,0].divide(2)
    moduleX,phaseX=np.abs(xfft),np.angle(xfft)  # amplitude et phase de la fft de x
    dmoduleX,dphaseX=(2*np.real(dxfft)*np.real(xfft)+2*np.imag(dxfft)*
       np.imag(xfft))/(2.*moduleX),(np.imag(dxfft)*np.real(xfft)-np.real(dxfft)*
                       np.imag(xfft))/(moduleX**2)
    moduleY,phaseY=np.abs(yfft),np.angle(yfft)  # amplitude et phase de la fft de x
    dmoduleY,dphaseY=(2*np.real(dyfft)*np.real(yfft)+2*np.imag(dyfft)*
       np.imag(yfft))/(2.*moduleY),(np.imag(dyfft)*np.real(yfft)-np.real(dyfft)*
                       np.imag(yfft))/(moduleY**2)

    return xf,dxf,moduleX[:,0:M//2],phaseX[:,0:M//2],dmoduleX[:,0:M//2],\
           dphaseX[:,0:M//2],yf,dyf,moduleY[:,0:M//2],phaseY[:,0:M//2],\
           dmoduleY[:,0:M//2],dphaseY[:,0:M//2]

def odeint45_etendu(f,nPdP,h0,tol,M,x0,dx0,vect_t,T,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    dh=vect_t[1]-vect_t[0]

    def scan_fun(state, te):

        def cond_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev2,i_prev,c_prev=state
            return (t_prev<te) & (h_prev>0) # condition d'arrêt de simulation

        def body_fn(state):
            x_prev,t_prev,y_prev,h_prev,i_prev2,i_prev,c_prev=state

            x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,
                                t_prev,y_prev,i_prev,c_prev,h_prev,f,tol,T,*P) # prochaine itération de simulation

            # to reach te
            h_now=np.minimum(h_now,te-t_prev)

            return x_now,t_now,y_now,h_now,i_prev,i_now,c_now

        x_prev,dx_prev,t_prev,y_prev,dy_prev,h_prev,i_prev,c_prev,Mat,dMat,\
            chgt_state=state
        x_now,t_now,y_now,h_now,i_prev,i_now,c_now = while_loop(
            cond_fn,body_fn, (x_prev,t_prev,y_prev,h_prev,i_prev,i_prev,c_prev))

        if not isinstance(f.state,type(None)):# pour eviter erreurs d'execution
            f.state=i_prev
        dx_now,dy_now,Mat,dMat=next_der_step_simulation(x_prev,t_prev,dx_prev,
                            x_now,t_now,dh,f,nPdP,chgt_state,Mat,dMat,*P_and_dP) # prochaine itération de calcul des gradients
        chgt_state=np.bitwise_not(np.array_equal(i_now,i_prev))

        return (x_now,dx_now,t_now,y_now,dy_now,h_now,i_now,c_now,Mat,dMat,
                chgt_state),(x_now,dx_now,y_now,dy_now,i_now)

    for element in f.__dict__.keys(): # pour eviter erreurs d'execution
        if hasattr(f.__dict__[element],'primal'):
            f.__dict__[element]=f.__dict__[element].primal
    if not isinstance(f.state,type(None)):
        i0=f.state
    else:
        i0=0
    if not isinstance(f.commande,type(None)):
        c0=f.commande.next_command(vect_t[0])
    else:
        c0=0
    tempP,tempdP,Mat,dMat=None,None,0,0
    if 'initialize' in f.__class__.__dict__:
        tempP,tempdP=P,dP
        P,dP=jvp(f.initialize,(*P,),(*dP,))
        Mat,dMat=P,dP
    y0,dy0=jvp(f.output,(x0,vect_t[0],*P),(dx0,0.,*dP))
    if isinstance(y0,tuple):
        x0,y0=y0
        dx0,dy0=dy0
    if 'initialize' in f.__class__.__dict__:
        P,dP=tempP,tempdP
    chgt_state=False
    vect,(xf,dxf,yf,dyf,states)=scan(scan_fun,(x0,dx0,vect_t[0],y0,dy0,h0,i0,
                                            c0,Mat,dMat,chgt_state),vect_t[1:]) # simulation dynamique
    if not isinstance(f.state,type(None)):# pour eviter erreurs d'execution
        f.state=vect[6]
    xf=np.transpose(np.concatenate((x0[None], xf))) # valeurs stockées du vecteur d'état
    yf=np.transpose(np.concatenate((y0[None], yf))) # valeurs stockées du vecteur de sortie
    dxf=np.transpose(np.concatenate((dx0[None], dxf))) # gradients du vecteur d'état
    dyf = np.transpose(np.concatenate((dy0[None], dyf))) # gradients du vecteur de sortie
    if not isinstance(f.state,type(None)): #si le systeme comporte plusieurs configurations
        if isinstance(i0,int):
            states=np.insert(states,0,i0) # configurations écrites sous la forme d'un entier
        else:
            states=np.transpose(np.concatenate((i0[None], states))) # configurations écrites sous la forme d'un vecteur
        if M==None: # s'il n'y a pas de simulation fréquentielle à faire
            return xf,dxf,yf,dyf,states
        else: # s'il y a une simulation fréquentielle à faire
            xf, dxf, modX, phX, dmodX,dphX, yf, dyf, modY, phY, dmodY, dphY=\
                compute_der_fft(xf,dxf,yf,dyf,M)
            return xf,dxf,modX,phX,dmodX,dphX,yf,dyf,modY,phY,dmodY,dphY,states
    else: # si le système ne comporte pas plusieurs configurations
        if M==None:# s'il n'y a pas de simulation fréquentielle à faire
            return xf,dxf,yf,dyf
        else:# s'il y a une simulation fréquentielle à faire
            xf, dxf, modX, phX, dmodX,dphX, yf, dyf, modY, phY, dmodY, dphY=\
                compute_der_fft(xf,dxf,yf,dyf,M)
            return xf,dxf,modX,phX,dmodX,dphX,yf,dyf,modY,phY,dmodY,dphY
