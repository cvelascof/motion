"""Methods for advection-based extrapolation."""

import numpy as np
import scipy.ndimage.interpolation as ip

def get_method(name):
  """Return a callable function for the extrapolation method corresponding to 
  the given name. The available options are:\n\
  
  +-------------------+--------------------------------------------------------+
  |     Name          |              Description                               |
  +===================+========================================================+
  |  semilagrangian   | implementation of the semi-Lagrangian method of        |
  |                   | Germann et al., 2002                                   |
  +-------------------+--------------------------------------------------------+
  """
  if name == "semilagrangian":
    return semilagrangian
  else:
    raise ValueError("unknown method %s, the only currently implemented method is 'semilagrangian'" % name)

def semilagrangian(R, V, num_timesteps, D_prev=None, n_iter=3, inverse=True, 
                   return_displacement=False):
  """Apply semi-Lagrangian extrapolation to a two-dimensional precipitation 
  field.
  
  Parameters
  ----------
  R : array-like
    Array of shape (m,n) containing the input precipitation field.
  V : array-like
    Array of shape (m,n,d>=2) containing the x- and y-components of the m*n 
    advection field.
  num_timesteps : int
    Number of time steps to extrapolate.
  XYD_0 : array-like
    Optional initial displacement vector field of shape (m,n,2) for the 
    extrapolation.
  n_iter : int
    Number of inner iterations in the semi-Lagrangian scheme.
  inverse : bool
    If True, the extrapolation trajectory is computed backward along the 
    flow (default), forward otherwise.
  return_displacement : bool
    If True, return the total advection velocity (displacement) between the 
    initial input field and the advected one integrated along the trajectory.
  
  Returns
  -------
  out : array or tuple
    If return_displacement=False, return the extrapolated field of shape (m,n). 
    Otherwise, return a tuple containing the extrapolated field and the total 
    displacement along the advection trajectory.
  """
  if len(R.shape) != 2:
    raise ValueError("R must be a two-dimensional array")
  
  if len(V.shape) != 3:
    raise ValueError("V must be a three-dimensional array")
  
  coeff = 1.0 if not inverse else -1.0
  
  X,Y = np.meshgrid(np.arange(V.shape[1]), np.arange(V.shape[0]))
  XY  = np.dstack([X, Y])
  
  R_e = []
  if D_prev is None:
    D = np.zeros((V.shape[0], V.shape[1], 2))
  else:
    D = D_prev.copy()
  
  for t in xrange(num_timesteps):
    V_inc = np.zeros(D.shape)
    
    for k in xrange(n_iter):
      if t > 0 or k > 0 or D_prev is not None:
        XYW = XY + D - V_inc / 2.0
        XYW = [XYW[:, :, 1], XYW[:, :, 0]]
        
        VWX = ip.map_coordinates(V[:, :, 0], XYW, mode="constant", cval=np.nan, 
                                 order=1, prefilter=False)
        VWY = ip.map_coordinates(V[:, :, 1], XYW, mode="constant", cval=np.nan, 
                                 order=1, prefilter=False)
      else:
        VWX = V[:, :, 0]
        VWY = V[:, :, 1]
      
      V_inc[:, :, 0] = VWX / n_iter
      V_inc[:, :, 1] = VWY / n_iter
      
      D += coeff * V_inc
    
    XYW = XY + D
    XYW = [XYW[:, :, 1], XYW[:, :, 0]]
    
    IW = ip.map_coordinates(R, XYW, mode="constant", cval=np.nan, order=1, 
                            prefilter=False)
    R_e.append(np.reshape(IW, R.shape))
  
  if return_displacement == False:
    return R_e
  else:
    return R_e, D